import streamlit as st
import youtube

st.title("Video Summarizer")

video_link = st.text_input("Enter YouTube Video Link:")

if st.button("Generate Summary"):
    if video_link:
        with st.spinner("Generating summary..."):  # Show a spinner while processing
            summary = youtube.generate_summary(st, video_link)
            if summary:
                st.write("## Summary:")  # Display summary with formatting
                st.write(summary)  # Or st.text(summary) for plain text
    else:
        st.warning("Please enter a video link.")
