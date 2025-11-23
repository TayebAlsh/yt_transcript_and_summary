# Next-Level Features to Elevate the App

## Prioritized Features (Top 7 by Impact/Effort, Local-First Focus)

### 1. YouTube Video Embed Preview (UX - High Impact, Low Effort)
**Description**: Embed the YouTube video player directly in the UI after processing for easy reference while reading summary/transcript.
**Implementation**:
- Use Streamlit's `components.html` or `st.video` with iframe: `https://www.youtube.com/embed/{video_id}?autoplay=0`.
- Insert after title display in [streamlit_app.py](streamlit_app.py:54).
- Changes: Minor addition in display loop.
- No new deps.

### 2. Local Processing History (Persistence - High Impact, Medium Effort)
**Description**: Save processed summaries locally (SQLite) with sidebar history browser. Load past results without reprocessing.
**Implementation**:
- New file: `history.py` with sqlite ops (init db, save/load content_dicts by title/url).
- UI: Sidebar expander with list of past titles, select to load/display.
- Auto-save after process, limit to 50 recent.
- Files: New [`history.py`](history.py), update [streamlit_app.py](streamlit_app.py) for sidebar/import.
- Dep: `sqlite3` (stdlib).

### 3. Live Transcript Search & Highlight (UX - High Impact, Low Effort)
**Description**: Search box to filter/highlight matching segments in timestamped transcript.
**Implementation**:
- Add text_input for search term.
- Filter segments list where text.lower().contains(search), display filtered.
- Use `st.dataframe` for interactive table or markdown with bold highlights.
- Changes: [streamlit_app.py](streamlit_app.py:66) expander.

### 4. Multiple Summary Styles (Functionality - Medium Impact, Low Effort)
**Description**: Select summary type: TLDR, Bullets, Chapters, Key Quotes.
**Implementation**:
- New selectbox in UI.
- Extend `summarize_transcript` with `style` param, use different prompts/models (e.g., chapters via timestamp grouping).
- Chapters: Group segments into topics, generate titles.
- Update [yt_transcribe_and_summarize.py](yt_transcribe_and_summarize.py:304).

### 5. Playlist/Channel Support (Functionality - High Impact, Medium Effort)
**Description**: Process entire playlists or channels by URL.
**Implementation**:
- Detect playlist/channel via yt-dlp info.
- Fetch video_ids list, process sequentially with progress.
- Batch output zip or individual files.
- Leverage existing yt_dlp in backend.

### 6. Auto Language Detection (Functionality - Medium Impact, Low Effort)
**Description**: Automatically detect video language instead of fixed "en".
**Implementation**:
- Use Whisper's `detect_language` on first audio chunk or full.
- Default lang to detected, fallback to user select.
- Update [get_transcript](yt_transcribe_and_summarize.py:256).

### 7. Dark/Light Theme Toggle (UX - Low Impact, Very Low Effort)
**Description**: User toggle for app theme.
**Implementation**:
- Use `st.session_state` and CSS injection via `st.markdown`.
- Simple button toggle.

## Overall Effort Estimate
- Total: 10-15 hours across features.
- Can implement in phases, starting with UX quick wins.

## Enhanced Workflow
```mermaid
graph TD
    A[Input: URL(s)/Playlist] --> B[Auto Lang Detect]
    B --> C[Process: Transcript + Diarization]
    C --> D[Summaries: TLDR/Bullets/Chapters]
    D --> E[Display: Embed Video + Searchable Transcript + History Save]
    E --> F[Downloads: Multi-Format]
    G[Sidebar: History/Themes] -.-> E