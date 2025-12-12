# YouTube Transcript and Summary

Transcribe a YouTube video and generate a summary with timestamps, speaker diarization, and multiple output formats.

## Features

- Fetches official YouTube captions when available (no API keys required)
- Falls back to local Whisper model for transcription
- Summarizes using local Hugging Face transformers models
- Produces structured output with TLTR, detailed summary, full transcript, and timestamped segments
- Optional speaker diarization using pyannote.audio
- Multiple output formats: Markdown, PDF, HTML, JSON
- Batch processing for multiple videos
- Web GUI powered by Streamlit with download buttons

## Requirements

- Python 3.9+
- ffmpeg for audio processing
- Sufficient GPU VRAM for Whisper models (or CPU fallback)
- Optional: Hugging Face token for diarization

## Setup

1) Install dependencies

```bash
pixi install
```

2) (Optional) Set environment variables

Create a `.env` file:

```
HF_TOKEN=your_huggingface_token_here  # For speaker diarization
```

## Usage

### CLI

Basic usage:

```bash
pixi run transcribe "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

Batch processing:

```bash
pixi run transcribe url1 url2 url3 --output ./outputs/
```

Options:

- `--format md|pdf|html|json`: Output format (default: md)
- `--lang en`: Language
- `--whisper-model tiny|base|small|medium|large`: Whisper model (default: medium)
- `--summary-model`: Hugging Face summarization model (default: facebook/bart-large-cnn)
- `--diarization`: Enable speaker diarization
- `--output`: Output file or directory

### Web GUI

Run:

```bash
pixi run web
```

Enter URLs (one per line), select options, process, and download files.

## PDF Dependencies

**macOS:**

```bash
brew install cairo pango gdk-pixbuf libffi
```

**Ubuntu:**

```bash
sudo apt install build-essential libcairo2 libpango-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info
```

## Troubleshooting

- ffmpeg not found: `brew install ffmpeg`
- Diarization requires HF_TOKEN and may need GPU
- Large Whisper models require significant VRAM

## License

MIT
