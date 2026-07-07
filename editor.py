from huggingface_hub import InferenceClient
from PIL import Image
from io import BytesIO
import base64


def _pil_to_bytes(image: Image.Image) -> bytes:
    buf = BytesIO()
    image.save(buf, format="PNG")
    return buf.getvalue()


def _resize(image: Image.Image, max_side: int = 512) -> Image.Image:
    w, h = image.size
    if max(w, h) <= max_side:
        return image
    scale = max_side / max(w, h)
    return image.resize((int(w * scale) & ~1, int(h * scale) & ~1), Image.LANCZOS)


def edit_image(image: Image.Image, prompt: str, api_key: str = "") -> Image.Image:
    """
    Edit an image using HF Serverless Inference API (image-to-image task).
    Uses stabilityai/stable-diffusion-xl-refiner-1.0 for img2img.
    Requires a free HF token from https://huggingface.co/settings/tokens
    """
    if not api_key:
        raise RuntimeError(
            "Hugging Face token is required.\n"
            "Get a FREE token at: https://huggingface.co/settings/tokens\n"
            "Then paste it in the sidebar."
        )

    image = _resize(image.convert("RGB"))

    client = InferenceClient(
        provider="hf-inference",
        api_key=api_key,
    )

    result = client.image_to_image(
        image=image,
        prompt=prompt,
        model="timbrooks/instruct-pix2pix",
    )

    return result  # PIL.Image
