import torch
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
from PIL import Image

_pipeline = None


def _load_pipeline():
    global _pipeline
    if _pipeline is not None:
        return _pipeline

    model_id = "runwayml/stable-diffusion-v1-5"
    device = "cuda" if torch.cuda.is_available() else "cpu"
    dtype = torch.float16 if torch.cuda.is_available() else torch.float32

    pipe = StableDiffusionPipeline.from_pretrained(
        model_id,
        torch_dtype=dtype,
        safety_checker=None,
        requires_safety_checker=False,
    )
    pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
    pipe = pipe.to(device)

    if device == "cpu":
        pipe.enable_attention_slicing()

    _pipeline = pipe
    return _pipeline


def generate_image(prompt: str, model: str = "sd15", size: str = "512x512", api_key: str = "") -> Image.Image:
    """
    Generate an image locally using Stable Diffusion v1.5.
    First call downloads the model (~4GB). Subsequent calls are fast.
    """
    try:
        width, height = map(int, size.split("x"))
    except ValueError:
        width, height = 512, 512

    width = min(width, 768)
    height = min(height, 768)

    pipe = _load_pipeline()

    result = pipe(
        prompt=prompt,
        width=width,
        height=height,
        num_inference_steps=25,
        guidance_scale=7.5,
    )
    return result.images[0]
