from ocr import extract_text_from_image
from summarizer import summarize_text_gemini
from notion_wrapper import NotionClientWrapper
from utils import load_env_vars


def main():
    cfg = load_env_vars()

    # -----------------------
    # 1. Test summarizer only
    # -----------------------
    sample_text = """
    Mnemosyne is the Greek goddess of memory. In this project, screenshots are
    processed into structured notes using OCR, summarized with Gemini AI, and stored in Notion.
    """
    print("=== Sample Text ===")
    print(sample_text)

    gemini_summary = summarize_text_gemini(sample_text)
    print("\n=== Gemini Summary ===")
    print(gemini_summary)

    # -----------------------
    # 2. Test OCR
    # -----------------------
    try:
        text = extract_text_from_image("data/sample_screenshot.png")
        print("\n=== OCR RESULT ===")
        print(text)
    except Exception as e:
        print("\n⚠️ OCR test skipped or failed:", e)
        text = sample_text  # fallback so pipeline still works

    # -----------------------
    # 3. Test summarizer on OCR output
    # -----------------------
    summary = summarize_text_gemini(text)
    print("\n=== OCR Summary ===")
    print(summary)

    # -----------------------
    # 4. Test Notion Connection
    # -----------------------
    try:
        notion = NotionClientWrapper(cfg["NOTION_API_KEY"], cfg["NOTION_DB_ID"])
        notion.add_entry("Test Entry", summary)
        print("\n✅ Successfully saved to Notion!")
    except Exception as e:
        print("\n❌ Notion connection failed:", e)


if __name__ == "__main__":
    main()
