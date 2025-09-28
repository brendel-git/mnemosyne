import io, requests
from PIL import Image
from utils import load_env_vars


def extract_text_from_image(image_input: str | bytes) -> str:
    """
    Extract text from an image.
    - If Azure Document Intelligence env vars are set, use Azure OCR.
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

    # Prefer Azure Document Intelligence if configured
    if cfg.get("AZURE_VISION_ENDPOINT") and cfg.get("AZURE_VISION_KEY"):
        return _azure_read(image_bytes, cfg["AZURE_VISION_ENDPOINT"], cfg["AZURE_VISION_KEY"])

    # Fallback: local pytesseract
    try:
        import pytesseract
        img = Image.open(io.BytesIO(image_bytes))
        return pytesseract.image_to_string(img).strip()
    except Exception as e:
        raise RuntimeError(
            "OCR failed. Configure Azure Document Intelligence or install Tesseract."
        ) from e


def _azure_read(image_bytes: bytes, endpoint: str, key: str) -> str:
    """
    Azure Document Intelligence OCR (prebuilt-read model).
    Uses async API: POST -> poll Operation-Location until result.
    """
    url = f"{endpoint.rstrip('/')}/formrecognizer/documentModels/prebuilt-read:analyze"
    params = {"api-version": "2023-07-31"}
    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/octet-stream",
    }

    # Step 1: submit request
    post = requests.post(url, params=params, headers=headers, data=image_bytes, timeout=30)
    post.raise_for_status()

    op_location = post.headers.get("Operation-Location")
    if not op_location:
        raise RuntimeError("Azure OCR: missing Operation-Location in response headers")

    # Step 2: poll until result ready
    for _ in range(30):  # up to ~30 seconds
        res = requests.get(op_location, headers={"Ocp-Apim-Subscription-Key": key}, timeout=30)
        res.raise_for_status()
        j = res.json()
        status = j.get("status", "").lower()

        if status == "succeeded":
            # Step 3: extract text
            lines_out = []
            for page in j.get("analyzeResult", {}).get("pages", []):
                for line in page.get("lines", []):
                    lines_out.append(line.get("content", ""))
            return "\n".join(lines_out).strip()

        if status == "failed":
            raise RuntimeError(f"Azure OCR failed: {j}")

        import time
        time.sleep(1)

    raise TimeoutError("Azure OCR timed out after polling")
