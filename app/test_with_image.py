from ocr import extract_text_from_image
from summarizer import summarize_text_gemini
from notion_wrapper import NotionClientWrapper
from utils import load_env_vars

def main():
    cfg = load_env_vars()

    # 1. OCR
    text = extract_text_from_image("data/sample_screenshots/sample.png")
    print("=== OCR RESULT ===")
    print(text)

    # 2. Summarize
    summary = summarize_text_gemini(text)
    print("\n=== GEMINI SUMMARY ===")
    print(summary)

    # 3. Save to Notion
    notion = NotionClientWrapper(cfg["NOTION_API_KEY"], cfg["NOTION_DB_ID"])
    notion.add_entry("Test Note from Screenshot", summary)
    print("\n✅ Successfully saved to Notion!")

if __name__ == "__main__":
    main()
