from huggingface_hub import InferenceClient
from PIL import Image


def generate_image(
    prompt: str,
    model: str = "black-forest-labs/FLUX.1-schnell",
    size: str = "1024x1024",
    api_key: str = "",
) -> Image.Image:
    """
    Generate an image using Hugging Face Inference Providers.
    """

    if not api_key:
        raise RuntimeError(
            "Hugging Face token is required.\n"
            "Get one from https://huggingface.co/settings/tokens"
        )

    client = InferenceClient(api_key=api_key)

    image = client.text_to_image(
        prompt=prompt,
        model=model,
    )

    return image
