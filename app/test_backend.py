from ocr import extract_text_from_image
from summarizer import summarize_text_gemini
from notion_wrapper import NotionClientWrapper
from utils import load_env_vars

from summarizer import summarize_text_gemini



def main():
    cfg = load_env_vars()


    sample_text = """
    Mnemosyne is the Greek goddess of memory. In this project, screenshots are
    processed into structured notes using OCR, summarized with Gemini AI, and stored in Notion.
    """

    print("=== Original Text ===")
    print(sample_text)

    print("\n=== Gemini Summary ===")
    print(summarize_text_gemini(sample_text))

    # Test OCR
    text = extract_text_from_image("data/sample_screenshot.png")
    print("=== OCR RESULT ===")
    print(text)

    # Test summarizer
    summary = summarize_text_gemini(text)
    print("\n=== SUMMARY ===")
    print(summary)

    # Test Notion save
    notion = NotionClientWrapper(cfg["NOTION_API_KEY"], cfg["NOTION_DB_ID"])
    notion.add_entry("Test Entry", summary)
    print("\n✅ Saved to Notion!")

if __name__ == "__main__":
    main()
