from huggingface_hub import InferenceClient
from PIL import Image


def generate_image(prompt: str, model: str = "sdxl", size: str = "1024x1024", api_key: str = "") -> Image.Image:
    """
    Generate an image using HF Serverless Inference API via InferenceClient.
    Requires a free HF token from https://huggingface.co/settings/tokens
    """
    if not api_key:
        raise RuntimeError(
            "Hugging Face token is required.\n"
            "Get a FREE token at: https://huggingface.co/settings/tokens\n"
            "Then paste it in the sidebar."
        )

    client = InferenceClient(
        provider="hf-inference",
        api_key=api_key,
    )

    image = client.text_to_image(
        prompt=prompt,
        model="stabilityai/stable-diffusion-xl-base-1.0",
    )

    return image  # already a PIL.Image
