import os
from openai import OpenAI
from PIL import Image
import requests
from io import BytesIO
import base64

def edit_image(image, prompt, api_key=None):
    """
    Edit an image using OpenAI DALL-E API with mask-based editing
    
    Args:
        image (PIL.Image): The original image to edit
        prompt (str): Instructions for editing the image
        api_key (str): OpenAI API key
    
    Returns:
        PIL.Image: The edited image
    """
    
    if not api_key:
        raise ValueError(" OpenAI API key is required. Please provide it in the sidebar.")
    
    if not prompt or not prompt.strip():
        raise ValueError(" Edit instructions cannot be empty")
    
    try:
        # Initialize OpenAI client
        client = OpenAI(api_key=api_key)
        
        # Convert PIL image to RGB if necessary
        if image.mode in ('RGBA', 'LA', 'P'):
            rgb_image = Image.new('RGB', image.size, (255, 255, 255))
            rgb_image.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
            image = rgb_image
        
        # Save image to bytes
        img_byte_arr = BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        
        # Create a temporary file for the API
        temp_image_path = "/tmp/edit_image.png"
        image.save(temp_image_path)
        
        print(f" Editing image with prompt: {prompt[:100]}...")
        
        # Use DALL-E 3 with the image_edits endpoint
        with open(temp_image_path, "rb") as img_file:
            response = client.images.edit(
                image=img_file,
                prompt=prompt,
                model="dall-e-2",  # Image editing only works with DALL-E 2
                n=1,
                size="1024x1024"
            )
        
        # Download and return the edited image
        edited_image_url = response.data[0].url
        edited_image_response = requests.get(edited_image_url)
        edited_image = Image.open(BytesIO(edited_image_response.content))
        
        print(f" Image edited successfully!")
        
        # Clean up temp file
        if os.path.exists(temp_image_path):
            os.remove(temp_image_path)
        
        return edited_image
    
    except ValueError as e:
        print(f" Validation Error: {str(e)}")
        raise
    except Exception as e:
        error_msg = str(e)
        if "invalid_api_key" in error_msg or "401" in error_msg:
            raise ValueError(" Invalid API Key! Please check your OpenAI API key in the sidebar.")
        elif "rate_limit" in error_msg or "429" in error_msg:
            raise ValueError(" Rate limit exceeded. Please wait and try again.")
        elif "invalid_request" in error_msg:
            raise ValueError(f" Image format not supported or editing not possible. Try a different image.")
        else:
            raise ValueError(f" Error editing image: {error_msg}")


def create_variation(image, api_key=None):
    """
    Create a variation of an image using OpenAI DALL-E
    
    Args:
        image (PIL.Image): The original image
        api_key (str): OpenAI API key
    
    Returns:
        PIL.Image: A variation of the image
    """
    
    if not api_key:
        raise ValueError(" OpenAI API key is required.")
    
    try:
        client = OpenAI(api_key=api_key)
        
        # Convert image to RGB
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Save to bytes
        img_byte_arr = BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        
        print(f" Creating image variation...")
        
        response = client.images.create_variation(
            image=img_byte_arr,
            model="dall-e-2",
            n=1,
            size="1024x1024"
        )
        
        # Download and return variation
        variation_url = response.data[0].url
        variation_response = requests.get(variation_url)
        variation_image = Image.open(BytesIO(variation_response.content))
        
        print(f" Variation created successfully!")
        
        return variation_image
    
    except Exception as e:
        print(f" Error creating variation: {str(e)}")
        raise
