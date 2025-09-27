import os
from dotenv import load_dotenv

def load_env_vars():
    """
    Load environment variables from .env file.
    Returns:
        dict: mapping of API keys and IDs
    """
    
    load_dotenv()
    return {
        "AZURE_VISION_ENDPOINT": os.getenv("AZURE_VISION_ENDPOINT"),
        "AZURE_VISION_KEY": os.getenv("AZURE_VISION_KEY"),
        "GEMINI_API_KEY": os.getenv("GEMINI_API_KEY"),
        "NOTION_API_KEY": os.getenv("NOTION_API_KEY"),
        "NOTION_DB_ID": os.getenv("NOTION_DB_ID"),
    }
