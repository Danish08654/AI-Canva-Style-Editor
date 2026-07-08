import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
from PIL import Image
from io import BytesIO

from generator import generate_image
from editor import edit_image
from prompt_engine import enhance_prompt

st.set_page_config(page_title="AI Image Generator & Editor", page_icon="🎨", layout="wide")

st.markdown("<h1 style='text-align:center;'>AI Image Generator & Editor</h1>", unsafe_allow_html=True)

st.markdown("---")

# LOAD TOKEN FROM SECRETS 
# Priority: st.secrets > environment variable > empty
def load_token() -> str:
    # 1. Streamlit secrets (secrets.toml or cloud secrets)
    try:
        return st.secrets["HF_TOKEN"]
    except (KeyError, FileNotFoundError):
        pass
    # 2. Environment variable (e.g. set in shell or Docker)
    return os.getenv("HF_TOKEN", "")

HF_TOKEN = load_token()


# MODE 
mode = st.radio("Choose Mode", ["🖼 Generate Image", "✏️ Edit Image"], horizontal=True)

# GENERATE
if mode == "🖼 Generate Image":
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("📝 Prompt Panel")
        prompt = st.text_area("Describe your image",
            placeholder="e.g. futuristic city at night with neon lights", height=150)
        size_choice = st.selectbox("Image Size",
            ["1024x1024", "1152x896", "896x1152", "768x768"])
        gen_btn = st.button("✨ Generate Image", type="primary", use_container_width=True)

    with col2:
        st.subheader("🖼 Output Preview")
        if gen_btn:
            if not prompt.strip():
                st.error("⚠️ Please enter a prompt.")
            else:
                try:
                    with st.spinner("⏳ Generating via HF Inference API…"):
                        final_prompt = enhance_prompt(prompt)
                        st.info(f"✨ **Enhanced Prompt:** {final_prompt}")
                        img = generate_image(prompt=final_prompt, size=size_choice, api_key=HF_TOKEN)
                        st.image(img, use_container_width=True, caption="Generated Image")
                        buf = BytesIO()
                        img.save(buf, format="PNG")
                        buf.seek(0)
                        st.download_button("⬇️ Download Image", buf, "generated_image.png", "image/png")
                        st.success("✅ Image generated successfully!")
                except Exception as e:
                    st.error(f"❌ Error: {e}")

#  EDIT 
else:
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("📤 Upload Panel")
        uploaded = st.file_uploader("Upload an image to edit", type=["png", "jpg", "jpeg"])
        prompt = st.text_area("Edit Instructions",
            placeholder="e.g. change the background to a beach at sunset", height=150)
        edit_btn = st.button(" Apply AI Edit", type="primary", use_container_width=True)

    with col2:
        st.subheader("🖼 Output Preview")
        if uploaded:
            image = Image.open(uploaded).convert("RGB")
            st.image(image, caption="Original Image", use_container_width=True)
        if uploaded and edit_btn:
            if not prompt.strip():
                st.error(" Please enter edit instructions.")
            else:
                try:
                    with st.spinner(" Editing via HF Inference API…"):
                        final_prompt = enhance_prompt(prompt)
                        st.info(f" **Enhanced Prompt:** {final_prompt}")
                        result = edit_image(image=image, prompt=final_prompt, api_key=HF_TOKEN)
                        st.image(result, caption="Edited Image", use_container_width=True)
                        buf = BytesIO()
                        result.save(buf, format="PNG")
                        buf.seek(0)
                        st.download_button(" Download Edited Image", buf, "edited_image.png", "image/png")
                        st.success("✅ Done!")
                except Exception as e:
                    st.error(f"❌ Error: {e}")
