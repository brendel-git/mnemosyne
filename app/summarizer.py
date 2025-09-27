import google.generativeai as genai
from utils import load_env_vars

def summarize_text_gemini(text: str) -> str:
    if not text or not text.strip():
        return "No text to summarize."

    cfg = load_env_vars()
    genai.configure(api_key=cfg["GEMINI_API_KEY"])

    model = genai.GenerativeModel("gemini-1.5-flash")  # or gemini-1.5-pro

    response = model.generate_content(
        f"Summarize this text into concise, clear bullet points:\n\n{text[:8000]}"
    )

    return response.text.strip()
