#!/usr/bin/env python3
"""YouTube Transcribe & Summarize (LOCAL GPU ONLY)

Transcribes a YouTube video using:
    1. Official captions when available (fast, no GPU required)
    2. Local Whisper model (openai-whisper) as fallback (uses GPU if available)

Then summarizes locally using a Hugging Face transformer summarization pipeline.

Output Markdown sections:
    - TLTR (single concise sentence)
    - Detailed summary (structured)
    - Full transcript (collapsible)

Usage:
    python yt_transcribe_and_summarize.py <youtube_url> \
            [--output OUTPUT.md] \
            [--lang en] \
            [--whisper-model medium] \
            [--summary-model facebook/bart-large-cnn]

Examples:
    python yt_transcribe_and_summarize.py https://www.youtube.com/watch?v=dQw4w9WgXcQ
    python yt_transcribe_and_summarize.py dQw4w9WgXcQ --whisper-model small --summary-model philschmid/bart-large-cnn-samsum

Requirements: ffmpeg, sufficient VRAM for chosen Whisper model.
"""

import argparse
import os
import re
import sys
import tempfile
import math
import json
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Dict, Any

from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound, CouldNotRetrieveTranscript
from dotenv import load_dotenv
import requests

# Local whisper
try:
    import whisper  # openai-whisper
except Exception:
    whisper = None  # type: ignore

# Summarization (transformers)
try:
    from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
except Exception:
    pipeline = None  # type: ignore
    AutoTokenizer = None  # type: ignore
    AutoModelForSeq2SeqLM = None  # type: ignore

# Fallback audio download
try:
    import yt_dlp
except Exception:
    yt_dlp = None  # type: ignore

# Torch for device detection
try:
    import torch
except Exception:
    torch = None  # type: ignore


# New format support (HTML/PDF)
try:
    from markdown_it import MarkdownIt
except ImportError:
    MarkdownIt = None  # type: ignore

try:
    from weasyprint import HTML
except Exception:
    HTML = None  # type: ignore

# Diarization
try:
    from pyannote.audio import Pipeline
except Exception:
    Pipeline = None  # type: ignore
@dataclass
class Summary:
    tldr: str
    detailed: str

@dataclass
class Segment:
    start: float
    end: float
    text: str
    speaker: Optional[str] = None


def extract_video_id(url: str) -> str:
    # Supports common YouTube URL formats
    patterns = [
        r"(?:v=|/v/|youtu\.be/|/embed/)([\w-]{11})",
        r"^([\w-]{11})$",
    ]
    for p in patterns:
        m = re.search(p, url)
        if m:
            return m.group(1)
    raise ValueError("Could not parse YouTube video ID from URL")


def fetch_captions(video_id: str, lang: str) -> Optional[List[Segment]]:
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        transcript = None
        # Try any transcript in requested language (manual or generated)
        try:
            transcript = transcript_list.find_transcript([lang])
        except NoTranscriptFound:
            pass

        # If none, pick the first available and translate if needed
        if transcript is None:
            # Prefer manually created transcripts
            preferred = None
            for t in transcript_list:
                if t.is_generated is False:
                    preferred = t
                    break
            transcript = preferred or next(iter(transcript_list), None)
            if transcript is None:
                return None
            # Try translating to target lang if different
            try:
                if transcript.language_code != lang:
                    transcript = transcript.translate(lang)
            except Exception:
                # Translation might fail; use original language
                pass

        entries = transcript.fetch()
        segments = []
        for e in entries:
            text = e.get("text", "").strip()
            if text:
                start = e.get("start", 0.0)
                duration = e.get("duration", 0.0)
                segments.append(Segment(start=start, end=start + duration, text=text))
        return segments if segments else None
    except (TranscriptsDisabled, NoTranscriptFound, CouldNotRetrieveTranscript):
        return None
    except Exception:
        return None


def download_audio(url: str, out_dir: Path) -> Optional[Path]:
    if yt_dlp is None:
        return None
    out_path = out_dir / "%(id)s.%(ext)s"
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': str(out_path),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '128',
        }],
        'quiet': True,
        'noprogress': True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            # yt-dlp returns the file path after post-processing in info dict sometimes
            # We'll glob for the id-based filename
            vid = info.get('id')
            for p in out_dir.glob(f"{vid}.*"):
                if p.suffix in {'.mp3', '.m4a', '.webm', '.wav'}:
                    return p
    except Exception:
        return None
    return None


def transcribe_with_whisper(audio_path: Path, model_name: str = "medium") -> Optional[List[Segment]]:
    if whisper is None:
        print("Whisper library not installed. Can't transcribe.")
        return None
    try:
        # Force CPU for Whisper due to MPS compatibility issues
        device = "cpu"
        model = whisper.load_model(model_name, device=device)
        result = model.transcribe(str(audio_path))
        segments = []
        for seg in result.get("segments", []):
            text = seg.get("text", "").strip()
            if text:
                segments.append(Segment(start=seg.get("start", 0.0), end=seg.get("end", 0.0), text=text))
        return segments if segments else None
    except RuntimeError as e:
        print(f"Whisper runtime error: {e}")
        return None
    except Exception:
        return None


def add_diarization(audio_path: Path, segments: List[Segment]) -> List[Segment]:
    """Add speaker labels to segments using pyannote.audio."""
    if Pipeline is None:
        print("Pyannote not installed. Skipping diarization.")
        return segments
    try:
        # Load pipeline (requires HF token)
        pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-3.1", use_auth_token=os.getenv("HF_TOKEN"))
        # Run diarization
        diarization = pipeline(str(audio_path))
        # Assign speakers to segments
        for seg in segments:
            # Find overlapping speaker
            speakers = []
            for turn, _, speaker in diarization.itertracks(yield_label=True):
                if turn.start < seg.end and turn.end > seg.start:
                    speakers.append(speaker)
            # Take the most overlapping or first
            if speakers:
                seg.speaker = speakers[0]  # Simple: assign first overlapping speaker
        return segments
    except Exception as e:
        print(f"Diarization failed: {e}")
        return segments

def get_transcript(video_url_or_id: str, lang: str, whisper_model: str = "medium", use_diarization: bool = False) -> Optional[List[Segment]]:
    """Get transcript segments from captions or Whisper fallback."""
    video_id = extract_video_id(video_url_or_id)
    if not use_diarization:
        segments = fetch_captions(video_id, lang)
        if segments:
            return segments
    print("No official captions found or diarization requested. Attempting local Whisper transcription…")
    with tempfile.TemporaryDirectory() as td:
        audio_path = download_audio(video_url_or_id, Path(td))
        if not audio_path:
            print("Failed to download audio; cannot transcribe.")
            return None
        segments = transcribe_with_whisper(audio_path, whisper_model)
        if not segments:
            print("Local Whisper transcription failed.")
            return None
        if use_diarization:
            segments = add_diarization(audio_path, segments)
    return segments

def chunk_text(text: str, max_len: int = 6000) -> List[str]:
    # Simple chunking on sentence boundaries if possible
    sentences = re.split(r"(?<=[.!?])\s+", text)
    chunks = []
    buf = []
    cur = 0
    for s in sentences:
        if cur + len(s) + 1 > max_len and buf:
            chunks.append(" ".join(buf))
            buf = [s]
            cur = len(s) + 1
        else:
            buf.append(s)
            cur += len(s) + 1
    if buf:
        chunks.append(" ".join(buf))
    return chunks


def summarize_transcript(segments: List[Segment], summary_model: str = "facebook/bart-large-cnn") -> Summary:
    """Summarize using a local transformers model. Falls back to LexRank if transformers unavailable."""
    transcript = " ".join([s.text for s in segments])
    # ... rest same as before
    """Summarize using a local transformers model. Falls back to LexRank if transformers unavailable."""
    if pipeline is None:
        from sumy.parsers.plaintext import PlaintextParser
        from sumy.nlp.tokenizers import Tokenizer
        from sumy.summarizers.lex_rank import LexRankSummarizer
        parser = PlaintextParser.from_string(transcript, Tokenizer("english"))
        lex = LexRankSummarizer()
        sentences = lex(parser.document, 7)
        detailed = "\n\n".join([str(s) for s in sentences]) or transcript[:1200]
        tldr = detailed.split(". ")[0][:200]
        return Summary(tldr=tldr.strip(), detailed=detailed.strip())

    # Initialize summarizer pipeline (batching through chunks)
    tok = AutoTokenizer.from_pretrained(summary_model)
    max_input = getattr(tok, 'model_max_length', 1024)
    # Provide a safety cap
    if max_input > 4096:
        max_input = 4096

    # Split text into token-length chunks
    # Rough split by characters approximating tokens (~4 chars per token heuristic)
    approx_char_per_token = 4
    est_tokens = len(transcript) / approx_char_per_token
    if est_tokens <= max_input * 0.9:
        chunks = [transcript]
    else:
        target_chars = int(max_input * approx_char_per_token * 0.85)
        paragraphs = re.split(r"\n{2,}", transcript)
        chunks = []
        buf = []
        length = 0
        for para in paragraphs:
            if length + len(para) > target_chars and buf:
                chunks.append("\n\n".join(buf))
                buf = [para]
                length = len(para)
            else:
                buf.append(para)
                length += len(para)
        if buf:
            chunks.append("\n\n".join(buf))

    summarizer = pipeline("summarization", model=summary_model, tokenizer=tok, device=0 if torch.cuda.is_available() else ("mps" if torch.backends.mps.is_available() else -1))
    partials = []
    for c in chunks:
        # HuggingFace summarizers often have a 1024 or 2048 token limit; enforce truncation
        if len(c) > max_input * approx_char_per_token:
            c = c[: int(max_input * approx_char_per_token)]
        res = summarizer(c, max_length=300, min_length=60, do_sample=False)
        partials.append(res[0]['summary_text'].strip())

    combined = "\n\n".join(partials)

    # If multiple partials, produce a meta summary
    if len(partials) > 1:
        meta_input = combined
        if len(meta_input) > max_input * approx_char_per_token:
            meta_input = meta_input[: int(max_input * approx_char_per_token)]
        meta = summarizer(meta_input, max_length=250, min_length=60, do_sample=False)[0]['summary_text'].strip()
    else:
        meta = combined

    # TLTR heuristic: first sentence up to ~30 words
    sentences = re.split(r"(?<=[.!?])\s+", meta)
    first = sentences[0] if sentences else meta
    words = first.split()
    if len(words) > 30:
        first = " ".join(words[:30]) + "…"
    return Summary(tldr=first.strip(), detailed=meta.strip())


def _gpu_available() -> bool:
    if torch is None:
        return False
    return torch.cuda.is_available() or torch.backends.mps.is_available()


def ensure_env_loaded():
    # Still load .env in case user wants to store custom config variables
    load_dotenv(override=False)


def write_markdown(out_path: Path, title: str, video_url: str, summary: Summary, segments: List[Segment]):
    md = []
    md.append(f"# {title}\n")
    md.append(f"Source: {video_url}\n")
    md.append("\n## TLTR\n")
    md.append(f"{summary.tldr}\n")
    md.append("\n## Detailed summary\n")
    md.append(f"{summary.detailed}\n")
    md.append("\n## Full transcript\n")
    md.append("<details>\n<summary>Show transcript</summary>\n\n")
    transcript_text = " ".join([s.text for s in segments])
    md.append(transcript_text.strip())
    md.append("\n\n</details>\n")
    # Timestamped transcript
    if any(s.start is not None for s in segments):
        md.append("\n## Timestamped transcript\n")
        md.append("<details>\n<summary>Show timestamped transcript</summary>\n\n")
        for seg in segments:
            start_str = f"{int(seg.start // 60):02d}:{seg.start % 60:05.2f}"
            speaker = f" [{seg.speaker}]" if seg.speaker else ""
            md.append(f"**{start_str}{speaker}:** {seg.text}\n")
        md.append("\n</details>\n")
    out_path.write_text("\n".join(md), encoding="utf-8")


def generate_content(video_id: str, title: str, summary: Summary, segments: List[Segment]) -> dict:
    """Generate structured content dictionary for export."""
    # Convert segments to text for transcript
    transcript_text = " ".join([s.text for s in segments])
    # Also include segments for timestamped output
    segment_dicts = [{"start": s.start, "end": s.end, "text": s.text, "speaker": s.speaker} for s in segments]
    return {
        "title": title,
        "url": f"https://www.youtube.com/watch?v={video_id}",
        "tldr": summary.tldr,
        "detailed": summary.detailed,
        "transcript": transcript_text,
        "segments": segment_dicts,
    }

def markdown_to_html(content_dict: dict) -> str:
    """Convert content dict to HTML using markdown-it."""
    md = []
    md.append(f"# {content_dict['title']}\n")
    md.append(f"Source: {content_dict['url']}\n")
    md.append("\n## TLTR\n")
    md.append(f"{content_dict['tldr']}\n")
    md.append("\n## Detailed summary\n")
    md.append(f"{content_dict['detailed']}\n")
    md.append("\n## Full transcript\n")
    md.append("<details>\n<summary>Show transcript</summary>\n\n")
    md.append(content_dict['transcript'].strip())
    md.append("\n\n</details>\n")
    # Timestamped transcript
    segments = content_dict.get('segments', [])
    if segments and any(s.get('start') is not None for s in segments):
        md.append("\n## Timestamped transcript\n")
        md.append("<details>\n<summary>Show timestamped transcript</summary>\n\n")
        for seg in segments:
            start = seg.get('start', 0.0)
            start_str = f"{int(start // 60):02d}:{start % 60:05.2f}"
            speaker = f" [{seg.get('speaker')}]" if seg.get('speaker') else ""
            text = seg.get('text', '')
            md.append(f"**{start_str}{speaker}:** {text}\n")
        md.append("\n</details>\n")
    md_text = "\n".join(md)
    if MarkdownIt is None:
        # Fallback: return MD as-is (use browser raw view or something)
        return md_text
    md_parser = MarkdownIt("commonmark")
    html = md_parser.render(md_text)
    return html
def fetch_video_title(video_id: str) -> str:
    # Try oEmbed (no API key required)
    try:
        r = requests.get(
            "https://www.youtube.com/oembed",
            params={"url": f"https://www.youtube.com/watch?v={video_id}", "format": "json"},
            timeout=15,
        )
        if r.ok:
            return r.json().get("title") or f"YouTube Video {video_id}"
    except Exception:
        pass
    return f"YouTube Video {video_id}"


def export_content(content_dict: dict, path: Path, fmt: str):
    """Export content dict to specified format (md, json, html, pdf)."""
    if fmt == 'md':
        title = content_dict['title']
        url = content_dict['url']
        summary = Summary(tldr=content_dict['tldr'], detailed=content_dict['detailed'])
        segments = [Segment(start=s['start'], end=s['end'], text=s['text'], speaker=s.get('speaker')) for s in content_dict['segments']]
        write_markdown(path, title, url, summary, segments)
    elif fmt == 'json':
        path.write_text(json.dumps(content_dict, indent=2, ensure_ascii=False), encoding='utf-8')
    elif fmt == 'html':
        html = markdown_to_html(content_dict)
        path.write_text(html, encoding='utf-8')
    elif fmt == 'pdf':
        html = markdown_to_html(content_dict)
        if HTML is None:
            raise ImportError("WeasyPrint not available. Install with 'pip install weasyprint'.")
        HTML(string=html).write_pdf(str(path))
    else:
        raise ValueError(f"Unsupported format: {fmt}")

def main():
    parser = argparse.ArgumentParser(description="Local GPU transcription (Whisper) + local summarization.")
    parser.add_argument("youtube_urls", nargs='+', help="YouTube video URL(s) or 11-char ID(s)")
    parser.add_argument("--output", "-o", default=None, help="Output file path (for single video) or directory (for batch)")
    parser.add_argument("--lang", default="en", help="Preferred transcript language, e.g., en, es")
    parser.add_argument("--whisper-model", default="tiny", help="Whisper model size (tiny, base, small, medium, large)")
    parser.add_argument("--summary-model", default="facebook/bart-large-cnn", help="HuggingFace summarization model")
    parser.add_argument("--format", "-f", default="md", choices=["md", "pdf", "html", "json"], help="Output format (md, pdf, html, json)")
    parser.add_argument("--diarization", action="store_true", help="Enable speaker diarization (requires HF_TOKEN)")
    args = parser.parse_args()

    ensure_env_loaded()

    urls = args.youtube_urls
    is_batch = len(urls) > 1
    out_dir = Path(args.output) if args.output else Path.cwd()
    if is_batch and args.output and not out_dir.is_dir():
        out_dir.mkdir(parents=True, exist_ok=True)

    for url in urls:
        try:
            video_id = extract_video_id(url)
        except Exception as e:
            print(f"Error with {url}: {e}")
            continue

        title = fetch_video_title(video_id)

        segments = get_transcript(url, args.lang, args.whisper_model, args.diarization)
        if segments is None:
            print(f"Transcription failed for {url}.")
            continue
        summary = summarize_transcript(segments, args.summary_model)
        content = generate_content(video_id, title, summary, segments)

        # Output path
        safe_title = re.sub(r"[^\w\-]+", "_", title).strip("_")[:80]
        fmt = args.format
        if is_batch:
            out_path = out_dir / f"{safe_title or video_id}.{fmt}"
        else:
            out_name = args.output or f"{safe_title or video_id}.{fmt}"
            out_path = Path(out_name)

        export_content(content, out_path, fmt)
        print(f"Wrote {out_path.resolve()} ({fmt.upper()})")


if __name__ == "__main__":
    main()
