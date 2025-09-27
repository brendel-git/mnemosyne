import streamlit as st
from ocr import extract_text_from_image

st.title("📸 Upload & OCR")

uploaded = st.file_uploader("Upload screenshot (PNG/JPG)", type=["png","jpg","jpeg"])
if uploaded:
    st.image(uploaded, caption="Preview", use_container_width=True)
    if st.button("Run OCR"):
        with st.spinner("Extracting text..."):
            text = extract_text_from_image(uploaded.read())
        st.session_state["ocr_text"] = text
        st.success("✅ OCR complete")
        st.text_area("Extracted text", text, height=200)
