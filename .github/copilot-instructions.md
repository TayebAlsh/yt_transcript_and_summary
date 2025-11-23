# YouTube Transcript and Summary - AI Coding Agent Instructions

## Architecture Overview
This project provides YouTube video transcription and summarization with CLI and Streamlit web GUI. Core logic in `yt_transcribe_and_summarize.py` handles transcription (captions → Whisper fallback), summarization (Hugging Face transformers → sumy fallback), and multi-format export (MD, PDF, HTML, JSON). GUI in `streamlit_app.py` wraps core functions for user interaction.

Data flow: URL → video ID → fetch captions (fast, no GPU) → fallback to audio download + Whisper transcription → optional pyannote diarization → chunked summarization → structured content export.

## Key Components
- **Transcription**: `fetch_captions()` prioritizes official YouTube captions; falls back to `download_audio()` + `transcribe_with_whisper()` for GPU-accelerated local processing.
- **Summarization**: `summarize_transcript()` uses transformers pipeline with token-aware chunking; falls back to LexRank if unavailable.
- **Export**: `export_content()` generates formats via `generate_content()` dict; PDF uses WeasyPrint, HTML via markdown-it.
- **GUI**: Streamlit app imports core functions, displays results with expandable transcripts, provides download buttons using temp files.

## Critical Workflows
- **CLI Run**: `python yt_transcribe_and_summarize.py "https://youtu.be/VIDEO_ID" --whisper-model medium --format pdf --diarization` (requires HF_TOKEN env var for diarization).
- **GUI Run**: `streamlit run streamlit_app.py` (launches web interface for batch processing with previews).
- **Setup**: `pip install -r requirements.txt`; ensure ffmpeg installed; optional `.env` with `HF_TOKEN` for speaker diarization.
- **Testing**: Run smoke check task `python3 yt_transcribe_and_summarize.py -h` to verify imports and help output.

## Project Conventions
- **Optional Dependencies**: Wrap imports in try-except (e.g., `try: import whisper except: whisper = None`); check for None before use with user-friendly messages.
- **Fallback Patterns**: Always provide fallbacks (captions → Whisper; transformers → sumy; CPU if no GPU).
- **Data Structures**: Use `dataclass` for `Summary` (tldr, detailed) and `Segment` (start, end, text, speaker); convert to dicts for export.
- **Output Structure**: Content dict with keys: title, url, tldr, detailed, transcript, segments (list of dicts with start/end/text/speaker).
- **Error Handling**: Graceful degradation; print warnings for missing deps; continue processing other URLs in batch.
- **File Naming**: Sanitize titles for filenames (e.g., `re.sub(r"[^\w\-]+", "_", title)[:80]`).
- **Markdown Format**: TLTR section, detailed summary, collapsible full/timestamped transcripts using `<details>` tags.

## Integration Points
- **YouTube APIs**: `youtube_transcript_api` for captions (no auth); `yt_dlp` for audio download.
- **AI Models**: OpenAI Whisper for transcription; Hugging Face transformers for summarization; pyannote.audio for diarization (requires HF_TOKEN).
- **Export Libraries**: `weasyprint` for PDF; `markdown_it` for HTML; standard `json` for JSON.
- **Environment**: Load `.env` with `python-dotenv`; detect GPU via `torch.cuda.is_available()` or MPS.

Reference: `README.md` for usage examples; `plan.md` for implementation phases; `requirements.txt` for dependencies.