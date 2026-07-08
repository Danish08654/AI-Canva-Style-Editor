from gradio_client import Client, handle_file
from PIL import Image
import tempfile
import os

SPACE_NAME = "Rd786/DanishZulfiqar"

# Create client only once
client = Client(SPACE_NAME)


def edit_image(image: Image.Image, prompt: str, api_key: str = "") -> Image.Image:
    """
    Send image to Hugging Face Gradio Space and return edited image.
    """

    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            temp_path = tmp.name
            image.save(temp_path)

        result = client.predict(
            handle_file(temp_path),
            prompt,
            api_name="/predict",
        )

        return Image.open(result).convert("RGB")

    except Exception as e:
        raise RuntimeError(f"Image editing failed:\n{e}")

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
