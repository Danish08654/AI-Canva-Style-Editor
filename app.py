import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import streamlit as st
from PIL import Image
import requests
from io import BytesIO
from services.generator import generate_image
from services.editor import edit_image
from services.prompt_engine import enhance_prompt

#  PAGE CONFIG 
st.set_page_config(
    page_title="AI Image Genrator and Editor",
    page_icon="",
    layout="wide"
)

#  HEADER 
st.markdown(
    "<h1 style='text-align:center;'>AI Image Genrator and Editor</h1>",
    unsafe_allow_html=True
)

st.markdown("---")

#  MODE 
mode = st.radio(
    "Choose Mode",
    [" Generate Image", " Edit Image"],
    horizontal=True
)

#  GENERATE MODE
if mode == " Generate Image":

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader(" Prompt Panel")

        prompt = st.text_area(
            "Describe your image",
            placeholder="e.g. futuristic city at night",
            height=150
        )

        generate_btn = st.button(" Generate Image")

    with col2:
        st.subheader(" Output Preview")

        if generate_btn and prompt:

            with st.spinner("Generating..."):

                final_prompt = enhance_prompt(prompt)

                image_url = generate_image(final_prompt)

                img = Image.open(BytesIO(requests.get(image_url).content))

                st.image(img, use_container_width=150)


#  EDIT MODE
else:

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader(" Upload Panel")

        uploaded = st.file_uploader(
            "Upload Image",
            type=["png", "jpg", "jpeg"]
        )

        prompt = st.text_area(
            "Edit Instructions",
            placeholder="e.g. change background to beach",
            height=150
        )

        edit_btn = st.button(" Edit Image")

    with col2:
        st.subheader(" Output Preview")

        if uploaded:
            image = Image.open(uploaded)
            st.image(image, caption="Original Image", use_container_width=True)

        if uploaded and edit_btn:

            with st.spinner("Applying AI edit..."):

                final_prompt = enhance_prompt(prompt)

                result = edit_image(image, final_prompt)

                st.image(result, caption="Edited Image", use_container_width=True)
