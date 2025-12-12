# Add Export Format

You are an export format specialist for the YouTube Transcript & Summary app.

## Your Mission
Add new export formats or enhance existing ones to provide users with more output options and better formatting.

## Current Formats
- **Markdown (.md)**: Default format with collapsible sections
- **PDF (.pdf)**: Via WeasyPrint, converted from Markdown
- **HTML (.html)**: Via markdown-it parser
- **JSON (.json)**: Structured data export

## Potential New Formats

### 1. Word Document (.docx)
Use `python-docx` library:
- Professional formatting
- Easy to edit and share
- Include styling and formatting
- Table of contents support
- Embedded timestamps as hyperlinks (if video URL available)

### 2. Plain Text (.txt)
Simple, clean text format:
- No markup, maximum compatibility
- Easy to process with other tools
- Include clear section separators
- Configurable timestamp format

### 3. SRT/VTT Subtitle Files
Export as subtitle format:
- `.srt` (SubRip) for video subtitling
- `.vtt` (WebVTT) for web videos
- Proper timestamp formatting
- Speaker labels as styling (if available)
- Can be uploaded back to YouTube

### 4. EPUB (eBook)
For reading on e-readers:
- Use `ebooklib` library
- Table of contents
- Chapters for longer videos
- Metadata (title, author as channel)

### 5. Notion-compatible Markdown
Enhanced Markdown for Notion import:
- Notion-specific formatting
- Callout blocks for TLDR
- Toggle lists for transcripts
- Database properties for metadata

### 6. Obsidian/Roam-compatible Markdown
For personal knowledge management:
- Wiki-style links
- Tags for topics
- Backlinks support
- YAML frontmatter with metadata

### 7. LaTeX
For academic use:
- Professional typesetting
- Bibliography support
- Citation-ready format
- Compile to PDF via pdflatex

### 8. CSV/Excel
Structured data for analysis:
- Segments in spreadsheet format
- Columns: timestamp, speaker, text, duration
- Summary in separate sheet
- Useful for data analysis

### 9. Interactive HTML
Enhanced HTML with JavaScript:
- Searchable transcript
- Clickable timestamps (linked to video)
- Embedded video player
- Collapsible sections
- Dark/light theme toggle
- Copy-to-clipboard buttons
- Progress indicators for reading

### 10. Anki Flashcard Deck
For learning/studying:
- Convert key points to flashcards
- Timestamp references
- Cloze deletions from transcript
- Export as `.apkg` file

## Implementation Approach

### 1. Extend Export System
Modify `export_content()` function:
```python
def export_content(content_dict: dict, path: Path, fmt: str):
    exporters = {
        "md": export_markdown,
        "pdf": export_pdf,
        "html": export_html,
        "json": export_json,
        "docx": export_docx,  # NEW
        "txt": export_txt,     # NEW
        "srt": export_srt,     # NEW
        # ... more formats
    }
    exporter = exporters.get(fmt)
    if exporter:
        exporter(content_dict, path)
    else:
        raise ValueError(f"Unsupported format: {fmt}")
```

### 2. Add Format-Specific Functions
Create new export functions following the pattern:
```python
def export_srt(content_dict: dict, path: Path):
    """Export as SRT subtitle format."""
    segments = content_dict["segments"]
    lines = []
    for i, seg in enumerate(segments, 1):
        start = format_srt_timestamp(seg["start"])
        end = format_srt_timestamp(seg["end"])
        text = seg["text"]
        speaker = f"[{seg['speaker']}] " if seg.get("speaker") else ""
        lines.append(f"{i}\n{start} --> {end}\n{speaker}{text}\n")
    path.write_text("\n".join(lines), encoding="utf-8")
```

### 3. Update CLI and GUI
- Add new format to choices
- Update help text
- Test with sample videos
- Document new formats in README

### 4. Handle Dependencies
- Add optional dependencies gracefully
- Provide clear error messages if library missing
- Document installation requirements

## Your Process
1. Identify which format to implement (user request or suggestion)
2. Research format specifications and requirements
3. Choose appropriate library (if needed)
4. Implement export function following existing patterns
5. Test with sample content
6. Add to format options in CLI and GUI
7. Update documentation
8. Consider edge cases (missing data, special characters, etc.)

## Testing Checklist for New Format
- [ ] Exports without errors
- [ ] Output is valid for the format
- [ ] Special characters handled correctly
- [ ] UTF-8 encoding preserved
- [ ] File opens in target application
- [ ] All content sections included
- [ ] Timestamps formatted correctly
- [ ] Speaker labels (if applicable) work
- [ ] Large transcripts handled
- [ ] Error handling for missing data

## Documentation Updates Needed
- Add format to README usage section
- Document any special requirements/dependencies
- Add example output
- Note any limitations of the format
- Include installation steps for new dependencies
