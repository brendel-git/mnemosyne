from openai import OpenAI
from utils import load_env_vars

def summarize_text(text: str) -> str:
    if not text or not text.strip():
        return "No text to summarize."

    cfg = load_env_vars()
    client = OpenAI(api_key=cfg["OPENAI_API_KEY"])

    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Summarize text into concise, clear bullet points."},
            {"role": "user", "content": text[:12000]}  # guardrail
        ],
        max_tokens=220,
        temperature=0.2,
    )
    return resp.choices[0].message.content.strip()
