import os
from dotenv import load_dotenv

def load_env_vars():
    # Loads .env locally; on Azure, App Settings are already in env
    load_dotenv()
    cfg = {
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
        "GEMINI_API_KEY": os.getenv("GEMINI_API_KEY"),
        "NOTION_API_KEY": os.getenv("NOTION_API_KEY"),
        "NOTION_DB_ID": os.getenv("NOTION_DB_ID"),
        "AZURE_VISION_ENDPOINT": os.getenv("AZURE_VISION_ENDPOINT"),
        "AZURE_VISION_KEY": os.getenv("AZURE_VISION_KEY"),
    }
    missing = [k for k, v in cfg.items() if v in (None, "")]
    if missing:
        # Only warn; Streamlit UI will still load and show a warning
        print(f"[warn] Missing env vars: {missing}")
    return cfg
