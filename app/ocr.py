import io, time, requests
from PIL import Image
from utils import load_env_vars

def extract_text_from_image(image_input: str | bytes) -> str:
    """
    Extract text from an image.
    - If Azure Vision env vars set, use Azure OCR.
    - Else, fallback to local Tesseract.
    """

    cfg = load_env_vars()

    # Convert input to bytes
    if isinstance(image_input, (bytes, bytearray)):
        image_bytes = image_input
    else:
        with Image.open(image_input) as im:
            buf = io.BytesIO()
            im.save(buf, format="PNG")
            image_bytes = buf.getvalue()

    # Prefer Azure Vision
    if cfg["AZURE_VISION_ENDPOINT"] and cfg["AZURE_VISION_KEY"]:
        return _azure_read(image_bytes, cfg["AZURE_VISION_ENDPOINT"], cfg["AZURE_VISION_KEY"])

    # Fallback: local pytesseract
    try:
        import pytesseract
        img = Image.open(io.BytesIO(image_bytes))
        return pytesseract.image_to_string(img).strip()
    except Exception as e:
        raise RuntimeError("OCR failed. Configure Azure Vision or install Tesseract.") from e

def _azure_read(image_bytes: bytes, endpoint: str, key: str) -> str:
    """Azure Computer Vision OCR (Read API v3.2)."""
    url = f"{endpoint.rstrip('/')}/vision/v3.2/read/analyze"
    headers = {"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/octet-stream"}
    post = requests.post(url, headers=headers, data=image_bytes, timeout=30)
    post.raise_for_status()

    op_location = post.headers.get("Operation-Location")
    if not op_location:
        raise RuntimeError("Azure Vision missing Operation-Location header")

    # Poll for result
    for _ in range(30):
        res = requests.get(op_location, headers={"Ocp-Apim-Subscription-Key": key}, timeout=30)
        res.raise_for_status()
        j = res.json()
        status = j.get("status", "").lower()
        if status == "succeeded":
            lines_out = []
            ar = j.get("analyzeResult", {})
            if "readResults" in ar:
                for page in ar["readResults"]:
                    for line in page.get("lines", []):
                        lines_out.append(line.get("text", ""))
            return "\n".join(lines_out).strip()
        if status == "failed":
            raise RuntimeError(f"Azure Vision failed: {j}")
        time.sleep(1)

    raise TimeoutError("Azure Vision OCR timed out")
