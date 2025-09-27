import streamlit as st
from io import BytesIO
from utils import load_env_vars
from ocr import extract_text_from_image
from summarizer import summarize_text
from notion_client import NotionClientWrapper

st.set_page_config(page_title="Mnemosyne — The Goddess of Memory", layout="centered")

st.title("🧠 Mnemosyne — Screenshot ➜ Structured Memory ➜ Notion")

cfg = load_env_vars()
missing = [k for k in ("OPENAI_API_KEY","NOTION_API_KEY","NOTION_DB_ID","AZURE_VISION_ENDPOINT","AZURE_VISION_KEY") if not cfg.get(k)]
if missing:
    st.info(f"ℹ️ Missing configs: {', '.join(missing)}. You can still test with local OCR if Tesseract is installed.")

uploaded = st.file_uploader("Upload screenshot (PNG/JPG)", type=["png","jpg","jpeg"])
title = st.text_input("Title for Notion entry", value="Mnemosyne Entry")

if uploaded:
    st.image(uploaded, caption="Preview", use_container_width=True)
    if st.button("Run OCR ➜ Summarize ➜ Send to Notion"):
        with st.spinner("Extracting text..."):
            bytes_data = uploaded.read()
            text = extract_text_from_image(bytes_data)
        st.subheader("OCR Text")
        st.code(text or "(no text found)")

        with st.spinner("Summarizing..."):
            summary = summarize_text(text)
        st.subheader("Summary")
        st.write(summary)

        try:
            notion = NotionClientWrapper(cfg["NOTION_API_KEY"], cfg["NOTION_DB_ID"])
            notion.add_entry(title, summary)
            st.success("✅ Saved to Notion!")
        except Exception as e:
            st.error(f"Notion error: {e}")

st.caption("Tip: Configure Azure Vision for best OCR accuracy; otherwise local Tesseract will only work on your laptop.")
