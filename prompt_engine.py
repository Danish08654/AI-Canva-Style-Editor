def enhance_prompt(user_prompt):
    """
    Enhance user prompt with more descriptive details for better image generation
    
    Args:
        user_prompt (str): Original user input
    
    Returns:
        str: Enhanced prompt with additional details
    """
    
    if not user_prompt or not user_prompt.strip():
        return "A beautiful, professional, high-quality image"
    
    # Clean up the input
    user_prompt = user_prompt.strip()
    
    # Define enhancement templates based on keywords
    enhancements = {
        "style": ["professional", "cinematic", "artistic", "realistic", "abstract", "minimalist"],
        "quality": ["highly detailed", "sharp focus", "4k", "ultra high definition", "masterpiece"],
        "lighting": ["dramatic lighting", "golden hour", "neon lights", "soft lighting", "volumetric light"],
        "composition": ["rule of thirds", "centered composition", "wide angle", "close-up", "aerial view"],
        "atmosphere": ["moody", "vibrant", "serene", "energetic", "peaceful", "mysterious"]
    }
    
    enhanced = user_prompt
    
    # Add quality descriptors
    quality_phrases = [
        "highly detailed",
        "professional quality",
        "sharp focus",
        "well-composed"
    ]
    
    # Check if the prompt already has quality indicators
    has_quality = any(phrase in enhanced.lower() for phrase in quality_phrases)
    
    if not has_quality and len(enhanced) < 100:
        enhanced = f"{enhanced}, {quality_phrases[0]}, {quality_phrases[2]}"
    
    # Add style if not present
    style_keywords = ["style", "art", "render", "illustration", "photography", "painting"]
    has_style = any(keyword in enhanced.lower() for keyword in style_keywords)
    
    if not has_style and len(enhanced) < 80:
        enhanced = f"{enhanced}, professional digital art"
    
    # Ensure maximum clarity by adding key descriptors
    if "lighting" not in enhanced.lower():
        enhanced = f"{enhanced}, with professional lighting"
    
    # Add resolution hint for consistency
    if "4k" not in enhanced.lower() and "hd" not in enhanced.lower():
        enhanced = f"{enhanced}, 4k quality"
    
    return enhanced.strip()


def create_style_prompt(base_prompt, style):
    """
    Combine a base prompt with a specific art style
    
    Args:
        base_prompt (str): The original image description
        style (str): The desired art style
    
    Returns:
        str: Combined prompt with style information
    """
    
    styles = {
        "oil_painting": "oil painting style, classical, museum quality",
        "watercolor": "watercolor painting, soft colors, artistic",
        "digital_art": "digital art, modern, high quality",
        "photography": "professional photography, realistic, sharp focus",
        "illustration": "illustration style, artistic, detailed",
        "anime": "anime style, vibrant colors, dynamic",
        "pixel_art": "pixel art style, retro, 8-bit",
        "3d_render": "3D render, CGI, cinematic lighting",
        "sketch": "pencil sketch, artistic, detailed line work",
        "abstract": "abstract art, modern, creative composition"
    }
    
    selected_style = styles.get(style, style)
    
    return f"{base_prompt}, in {selected_style}"


def add_negative_prompts(prompt):
    """
    Add common negative prompts to improve image quality
    
    Args:
        prompt (str): The positive prompt
    
    Returns:
        dict: Dictionary with positive prompt and negative prompts list
    """
    
    negative_prompts = [
        "blurry",
        "low quality",
        "distorted",
        "ugly",
        "bad anatomy",
        "watermark",
        "text",
        "low resolution",
        "pixelated"
    ]
    
    return {
        "positive": prompt,
        "negative": ", ".join(negative_prompts)
    }


def optimize_for_dalle(prompt):
    """
    Optimize prompt specifically for DALL-E models
    
    Args:
        prompt (str): Original prompt
    
    Returns:
        str: DALL-E optimized prompt
    """
    
    # DALL-E works best with specific, descriptive language
    # Remove words that DALL-E struggles with
    problematic_words = [
        "don't show",
        "without",
        "no ",
        "avoid",
        "not "
    ]
    
    optimized = prompt
    
    # Replace negative instructions with positive ones
    replacements = {
        "without people": "empty scene",
        "no text": "clean background",
        "avoid blur": "sharp focus",
    }
    
    for problem, solution in replacements.items():
        if problem.lower() in optimized.lower():
            optimized = optimized.lower().replace(problem.lower(), solution)
    
    # Ensure good structure
    if len(optimized.split(",")) < 3:
        optimized = enhance_prompt(optimized)
    
    return optimized


def extract_keywords(prompt):
    """
    Extract main keywords from a prompt
    
    Args:
        prompt (str): The prompt text
    
    Returns:
        list: List of extracted keywords
    """
    
    # Common filler words to ignore
    filler_words = {
        "a", "an", "the", "is", "are", "was", "were", "be", "been",
        "and", "or", "but", "in", "on", "at", "to", "for", "of", "with",
        "by", "from", "as", "that", "this", "these", "those", "i", "you"
    }
    
    # Split by common delimiters
    words = prompt.lower().replace(",", " ").split()
    
    # Filter out filler words and keep only meaningful ones
    keywords = [word for word in words if word not in filler_words and len(word) > 2]
    
    return list(set(keywords))  # Remove duplicates


# Example usage functions for testing
def format_prompt_for_display(prompt, max_length=100):
    """
    Format prompt for display in UI
    
    Args:
        prompt (str): The prompt
        max_length (int): Maximum display length
    
    Returns:
        str: Formatted prompt
    """
    if len(prompt) > max_length:
        return prompt[:max_length] + "..."
    return prompt
