#!/usr/bin/env python3
"""Simple Streamlit GUI demo."""

import streamlit as st
import tempfile
import base64
from pathlib import Path

from yt_transcribe_and_summarize import (
    extract_video_id,
    fetch_video_title,
    get_transcript,
    summarize_transcript,
    generate_content,
    export_content,
)

st.title("🗣️ YouTube Transcript & Summary Demo")

# Input
urls_input = st.text_area("Enter YouTube URL(s) or ID(s), one per line", height=100)
lang = st.selectbox("Language", ["en"])
whisper_model = st.selectbox("Whisper Model", ["tiny", "base", "small", "medium", "large"], index=3)
summary_model = st.text_input("Summary Model", "facebook/bart-large-cnn")
use_diarization = st.checkbox("Enable Speaker Diarization (requires HF_TOKEN)")
output_format = st.selectbox("Output Format", ["md", "pdf", "html", "json"])

if st.button("Process", type="primary"):
    urls = [u.strip() for u in urls_input.split('\n') if u.strip()]
    if not urls:
        st.warning("Enter at least one URL")
        st.stop()

    all_contents = []
    for url in urls:
        with st.spinner(f"Processing {url}..."):
            try:
                video_id = extract_video_id(url)
                title = fetch_video_title(video_id)
                segments = get_transcript(url, lang, whisper_model, use_diarization)
                if segments:
                    summary = summarize_transcript(segments, summary_model)
                    content = generate_content(video_id, title, summary, segments)
                    all_contents.append(content)
                    st.success(f"Processed: {title}")
                else:
                    st.error(f"No transcript for {url}")
            except Exception as e:
                st.error(f"Error with {url}: {e}")

    if all_contents:
        # Display results
        for content in all_contents:
            st.markdown(f"## {content['title']}")
            st.markdown(f"Source: {content['url']}")
            st.markdown("### TLTR")
            st.markdown(content['tldr'])
            st.markdown("### Detailed Summary")
            st.markdown(content['detailed'])
            with st.expander("Full Transcript"):
                st.text(content['transcript'])
            # Timestamped
            segments = content.get('segments', [])
            if segments:
                with st.expander("Timestamped Transcript"):
                    for seg in segments:
                        start = seg.get('start', 0.0)
                        start_str = f"{int(start // 60):02d}:{start % 60:05.2f}"
                        speaker = f" [{seg.get('speaker')}]" if seg.get('speaker') else ""
                        st.markdown(f"**{start_str}{speaker}:** {seg.get('text', '')}")

        # Download buttons
        for content in all_contents:
            title = content['title']
            safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()[:50]
            filename = f"{safe_title}.{output_format}"
            with tempfile.NamedTemporaryFile(suffix=f".{output_format}", delete=False) as tmp:
                tmp_path = Path(tmp.name)
                export_content(content, tmp_path, output_format)
                with open(tmp_path, "rb") as f:
                    data = f.read()
                st.download_button(
                    label=f"Download {title} ({output_format.upper()})",
                    data=data,
                    file_name=filename,
                    mime="application/octet-stream" if output_format == "json" else f"application/{output_format}",
                    key=f"download_{safe_title}"
                )
                try:
                    tmp_path.unlink()
                except PermissionError:
                    print(f"Could not delete temp file {tmp_path} (likely downloading); will clean later.")