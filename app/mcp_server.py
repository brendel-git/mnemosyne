from fastapi import FastAPI
from mcp.server.fastapi import FastAPIHandler

from summarizer import summarize_text_gemini
from notion_wrapper import NotionClientWrapper
from utils import load_env_vars

app = FastAPI()
handler = FastAPIHandler(app)

cfg = load_env_vars()

@handler.tool()
async def summarize(text: str) -> str:
    """
    Summarize text using Gemini AI.
    Args:
        text (str): raw text
    Returns:
        str: summary
    """
    return summarize_text_gemini(text)

@handler.tool()
async def save_to_notion(title: str, summary: str) -> str:
    """
    Save a summary into Notion.
    Args:
        title (str): entry title
        summary (str): summary text
    Returns:
        str: confirmation message
    """
    notion = NotionClientWrapper(cfg["NOTION_API_KEY"], cfg["NOTION_DB_ID"])
    notion.add_entry(title, summary)
    return f"✅ Saved '{title}' to Notion."
