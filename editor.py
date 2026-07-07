import requests
from PIL import Image
from io import BytesIO
import base64
import json


# Free HF Inference API — InstructPix2Pix for instruction-based editing
HF_EDIT_API_URL = "https://api-inference.huggingface.co/models/timbrooks/instruct-pix2pix"


def _image_to_base64(image: Image.Image) -> str:
    """Convert a PIL Image to a base64-encoded PNG string."""
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")


def _resize_for_editing(image: Image.Image, max_side: int = 512) -> Image.Image:
    """
    Resize image so the longest side is max_side, preserving aspect ratio.
    instruct-pix2pix works best at 512x512.
    """
    w, h = image.size
    if max(w, h) <= max_side:
        return image
    scale = max_side / max(w, h)
    new_w = int(w * scale) & ~1   # ensure even dimensions
    new_h = int(h * scale) & ~1
    return image.resize((new_w, new_h), Image.LANCZOS)


def edit_image(image: Image.Image, prompt: str, api_key: str = "") -> Image.Image:
    """
    Edit an image using Hugging Face instruct-pix2pix.
    Returns a PIL Image object.
    """
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    # Resize and convert to RGB
    image = _resize_for_editing(image.convert("RGB"))
    image_b64 = _image_to_base64(image)

    payload = {
        "inputs": prompt,
        "image": image_b64,
        "parameters": {
            "num_inference_steps": 20,
            "image_guidance_scale": 1.5,
            "guidance_scale": 7.5,
        }
    }

    response = requests.post(HF_EDIT_API_URL, headers=headers, data=json.dumps(payload), timeout=120)

    if response.status_code == 503:
        raise RuntimeError(
            "Editing model is loading. Please wait 20–30 seconds and try again."
        )
    if response.status_code == 401:
        raise RuntimeError(
            "Invalid or missing Hugging Face API token. "
            "Get a free token at https://huggingface.co/settings/tokens"
        )
    if response.status_code != 200:
        raise RuntimeError(
            f"Hugging Face API error {response.status_code}: {response.text[:300]}"
        )

    result = Image.open(BytesIO(response.content)).convert("RGB")
    return result
