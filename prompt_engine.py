def enhance_prompt(prompt: str) -> str:

    if not prompt or prompt.strip() == "":
        return "a high quality professional cinematic image"

    prompt = prompt.strip()

    enhanced = (
        "ultra realistic, 8k, highly detailed, cinematic lighting, "
        "professional photography, sharp focus, "
        f"{prompt}, "
        "high quality, trending art style"
    )

    return enhanced