from utils import load_env_vars
from ocr import extract_text_from_image
from summarizer import summarize_text
from notion_client import NotionClientWrapper

def main():
    cfg = load_env_vars()
    image_path = "data/sample_screenshot.png"
    text = extract_text_from_image(image_path)
    print("== OCR ==\n", text)
    summary = summarize_text(text)
    print("\n== SUMMARY ==\n", summary)
    NotionClientWrapper(cfg["NOTION_API_KEY"], cfg["NOTION_DB_ID"]).add_entry("Mnemosyne Entry", summary)
    print("\nSaved to Notion.")

if __name__ == "__main__":
    main()
