import torch
from diffusers import StableDiffusionInstructPix2PixPipeline, EulerAncestralDiscreteScheduler
from PIL import Image

_pipeline = None


def _load_pipeline():
    global _pipeline
    if _pipeline is not None:
        return _pipeline

    model_id = "timbrooks/instruct-pix2pix"
    device = "cuda" if torch.cuda.is_available() else "cpu"
    dtype = torch.float16 if torch.cuda.is_available() else torch.float32

    pipe = StableDiffusionInstructPix2PixPipeline.from_pretrained(
        model_id,
        torch_dtype=dtype,
        safety_checker=None,
        requires_safety_checker=False,
    )
    pipe.scheduler = EulerAncestralDiscreteScheduler.from_config(pipe.scheduler.config)
    pipe = pipe.to(device)

    if device == "cpu":
        pipe.enable_attention_slicing()

    _pipeline = pipe
    return _pipeline


def _resize_for_editing(image: Image.Image, max_side: int = 512) -> Image.Image:
    w, h = image.size
    if max(w, h) <= max_side:
        return image
    scale = max_side / max(w, h)
    new_w = int(w * scale) & ~1
    new_h = int(h * scale) & ~1
    return image.resize((new_w, new_h), Image.LANCZOS)


def edit_image(image: Image.Image, prompt: str, api_key: str = "") -> Image.Image:
    """
    Edit an image locally using InstructPix2Pix.
    First call downloads the model (~3GB). Subsequent calls are fast.
    """
    image = _resize_for_editing(image.convert("RGB"))
    pipe = _load_pipeline()

    result = pipe(
        prompt=prompt,
        image=image,
        num_inference_steps=20,
        image_guidance_scale=1.5,
        guidance_scale=7.5,
    )
    return result.images[0]
