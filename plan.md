# High-Level Implementation Plan for YouTube Transcript and Summary Tool

## Goals
- Streamlit-based Web GUI for user-friendly interaction
- Multiple output formats: Markdown (existing), PDF, HTML, JSON
- Key enhancements: Download buttons in GUI, timestamped transcripts, batch processing, speaker diarization

## High-Level Workflow
```mermaid
graph TD
    A[Input: CLI Args or Streamlit Form<br/>URL(s), Language, Format, Options] --> B[Fetch Video Title]
    B --> C{Try Official Captions?}
    C -->|Yes| D[Transcript from Captions<br/>(approx timestamps)]
    C -->|No| E[Download Audio + Whisper<br/>(segments w/ timestamps)]
    E --> F[Optional: Speaker Diarization]
    D --> G[Summarize Transcript]
    F --> G
    G --> H[Generate Structured Content<br/>{title, tldr, detailed, transcript, segments}]
    H --> I{Output Format}
    I -->|md/pdf/html/json| J[Export File(s)]
    K[Streamlit App] -.-> A
    L[CLI] -.-> A
```

## Implementation Phases

### Phase 1: Core Refactoring & CLI Enhancements
- Refactor transcription, summarization, and content generation into reusable functions
- Add CLI support for output formats, batch URLs, timestamps, diarization flags

### Phase 2: Multi-Format Export
- Implement exporters for MD, PDF (via WeasyPrint), HTML, JSON
- Handle file paths or in-memory for downloads

### Phase 3: Streamlit GUI
- Build UI for URL(s) input (single/batch), language/format selection, options (timestamps, diarization)
- Add processing button with progress, previews, and download buttons for all formats

### Phase 4: Transcript Enhancements
- Timestamped segments (Whisper native; approximate for captions)
- Optional speaker diarization (pyannote-audio on audio)

### Phase 5: Dependencies & Polish
- Update requirements.txt (streamlit, weasyprint, markdown-it-py, pyannote.audio, etc.)
- Update README.md with new usage, install notes (e.g., WeasyPrint deps, HF token for diarization)

### Phase 6: Testing
- Test CLI and GUI end-to-end with sample videos across formats/features

## Notes
- Keep local-first, lightweight
- Risks: WeasyPrint setup on macOS, diarization GPU/token needs (document)
- Total effort: ~8-10 hours

## Next
Approve plan → Switch to code mode for implementation.