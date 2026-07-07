from gradio_client import Client, handle_file
from PIL import Image
from io import BytesIO
import tempfile

# Replace this with YOUR Space name
SPACE_NAME = "https://huggingface.co/spaces/Rd786/DanishZulfiqar"

client = Client(SPACE_NAME)

def edit_image(image: Image.Image, prompt: str, api_key: str = "") -> Image.Image:
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        image.save(tmp.name)

        result = client.predict(
            image=handle_file(tmp.name),
            prompt=prompt,
            api_name="/predict"   # This depends on the Space
        )

    return Image.open(result).convert("RGB")
