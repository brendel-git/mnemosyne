import streamlit as st
from utils import load_env_vars
from notion_client import NotionClientWrapper

st.title("📒 Export to Notion")

if "summary" not in st.session_state:
    st.warning("⚠️ Please generate a summary first (see page 2).")
else:
    cfg = load_env_vars()
    title = st.text_input("Title for Notion entry", value="Mnemosyne Entry")

    if st.button("Send to Notion"):
        try:
            notion = NotionClientWrapper(cfg["NOTION_API_KEY"], cfg["NOTION_DB_ID"])
            notion.add_entry(title, st.session_state["summary"])
            st.success("✅ Saved to Notion")
        except Exception as e:
            st.error(f"Error: {e}")
