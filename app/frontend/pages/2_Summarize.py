import streamlit as st
from summarizer import summarize_text_gemini

st.title("✍️ Summarize")

if "ocr_text" not in st.session_state:
    st.warning("⚠️ Please upload and run OCR first (see page 1).")
else:
    if st.button("Summarize with Gemini"):
        with st.spinner("Summarizing..."):
            summary = summarize_text_gemini(st.session_state["ocr_text"])
        st.session_state["summary"] = summary
        st.success("✅ Summarization complete")
        st.text_area("Summary", summary, height=200)
