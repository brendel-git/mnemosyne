import io, time, requests
from typing import Optional
from PIL import Image
from utils import load_env_vars

def _azure_read(image_bytes: bytes, endpoint: str, key: str) -> str:
    # Read API (stable) – POST image, poll Operation-Location
    url = f"{endpoint.rstrip('/')}/vision/v3.2/read/analyze"
    headers = {"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/octet-stream"}
    post = requests.post(url, headers=headers, data=image_bytes, timeout=30)
    post.raise_for_status()
    op_location = post.headers.get("Operation-Location")
    if not op_location:
        raise RuntimeError("Azure Vision: missing Operation-Location header")

    # Poll results
    for _ in range(30):
        res = requests.get(op_location, headers={"Ocp-Apim-Subscription-Key": key}, timeout=30)
        res.raise_for_status()
        j = res.json()
        status = j.get("status", "").lower()
        if status in ("succeeded", "failed"):
            if status == "failed":
                raise RuntimeError(f"Azure Vision failed: {j}")
            # Extract text (handles both older/newer schemas)
            lines_out = []
            ar = j.get("analyzeResult", {})
            # v3.2: analyzeResult.readResults[*].lines[*].text
            if "readResults" in ar:
                for page in ar["readResults"]:
                    for line in page.get("lines", []):
                        lines_out.append(line.get("text", ""))
            # (Some responses use 'blocks' -> 'lines')
            if not lines_out and "blocks" in ar:
                for block in ar["blocks"]:
                    for line in block.get("lines", []):
                        lines_out.append(line.get("text", ""))
            return "\n".join([t for t in lines_out if t])
        time.sleep(1)
    raise TimeoutError("Azure Vision OCR timed out")

def extract_text_from_image(image_path_or_bytes: str | bytes) -> str:
    """
    If AZURE_VISION_* present, use Azure OCR.
    Otherwise fallback to Tesseract (requires tesseract binary -> good for local dev).
    """
    cfg = load_env_vars()
    if isinstance(image_path_or_bytes, (bytes, bytearray)):
        image_bytes = image_path_or_bytes
    else:
        with Image.open(image_path_or_bytes) as im:
            buf = io.BytesIO()
            im.save(buf, format="PNG")
            image_bytes = buf.getvalue()

    if cfg.get("AZURE_VISION_ENDPOINT") and cfg.get("AZURE_VISION_KEY"):
        return _azure_read(image_bytes, cfg["AZURE_VISION_ENDPOINT"], cfg["AZURE_VISION_KEY"])

    # --- Fallback: local Tesseract (only works if tesseract is installed) ---
    try:
        import pytesseract
        from PIL import Image
        if isinstance(image_path_or_bytes, (bytes, bytearray)):
            img = Image.open(io.BytesIO(image_path_or_bytes))
        else:
            img = Image.open(image_path_or_bytes)
        return pytesseract.image_to_string(img).strip()
    except Exception as e:
        raise RuntimeError(
            "No Azure Vision configured and Tesseract fallback failed. "
            "Set AZURE_VISION_* for Azure OCR on App Service."
        ) from e
