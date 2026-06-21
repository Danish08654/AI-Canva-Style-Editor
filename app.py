import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
from PIL import Image
import requests
from io import BytesIO

from generator import generate_image
from editor import edit_image
from prompt_engine import enhance_prompt

# PAGE CONFIG
st.set_page_config(
    page_title="AI Image Generator and Editor",
    page_icon="",
    layout="wide"
)

# HEADER
st.markdown(
    "<h1 style='text-align:center;'> AI Image Generator and Editor</h1>",
    unsafe_allow_html=True
)
st.markdown("---")

# MODE SELECTION
mode = st.radio(
    "Choose Mode",
    [" Generate Image", " Edit Image"],
    horizontal=True
)

# GENERATE MODE
if mode == "Generate Image":
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader(" Prompt Panel")
        prompt = st.text_area(
            "Describe your image",
            placeholder="e.g. futuristic city at night with neon lights",
            height=150
        )
        
        model_choice = st.selectbox(
            "Select Image Model",
            ["dall-e-3", "dall-e-2"],
            help="DALL-E 3 provides higher quality but costs more"
        )
        
        size_choice = st.selectbox(
            "Select Image Size",
            ["1024x1024", "1792x1024", "1024x1792"] if model_choice == "dall-e-3" else ["256x256", "512x512", "1024x1024"],
            help="Larger sizes may take longer to generate"
        )
        
        generate_btn = st.button(" Generate Image", type="primary", use_container_width=True)
    
    with col2:
        st.subheader(" Output Preview")
        
        if generate_btn:
            if not prompt.strip():
                st.error(" Please enter a prompt to generate an image")
            else:
                try:
                    with st.spinner(" Generating your image..."):
                        final_prompt = enhance_prompt(prompt)
                        st.info(f" **Enhanced Prompt:** {final_prompt}")
                        
                        image_url = generate_image(
                            final_prompt,
                            model=model_choice,
                            size=size_choice,
                            api_key=st.session_state.openai_api_key
                        )
                        
                        img = Image.open(BytesIO(requests.get(image_url).content))
                        st.image(img, use_container_width=True, caption="Generated Image")
                        
                        # Download button
                        img_byte_arr = BytesIO()
                        img.save(img_byte_arr, format='PNG')
                        img_byte_arr.seek(0)
                        
                        st.download_button(
                            label="Download Image",
                            data=img_byte_arr,
                            file_name="generated_image.png",
                            mime="image/png"
                        )
                        
                        st.success("Image generated successfully!")
                
                except Exception as e:
                    st.error(f" Error generating image: {str(e)}")

# EDIT MODE
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
            placeholder="e.g. change background to beach, add sunset",
            height=150
        )
        
        edit_btn = st.button(" Apply AI Edit", type="primary", use_container_width=True)
    
    with col2:
        st.subheader(" Output Preview")
        
        if uploaded:
            image = Image.open(uploaded)
            st.image(image, caption="Original Image", use_container_width=True)
        
        if uploaded and edit_btn:
            if not prompt.strip():
                st.error("Please enter edit instructions")
            else:
                try:
                    with st.spinner(" Applying AI edit..."):
                        final_prompt = enhance_prompt(prompt)
                        st.info(f" **Enhanced Prompt:** {final_prompt}")
                        
                        result = edit_image(
                            image,
                            final_prompt,
                            api_key=st.session_state.openai_api_key
                        )
                        
                        st.image(result, caption="Edited Image", use_container_width=True)
                        
                        # Download button
                        img_byte_arr = BytesIO()
                        result.save(img_byte_arr, format='PNG')
                        img_byte_arr.seek(0)
                        
                        st.download_button(
                            label=" Download Edited Image",
                            data=img_byte_arr,
                            file_name="edited_image.png",
                            mime="image/png"
                        )
                        
                        st.success(" Image edited successfully!")
                
                except Exception as e:
                    st.error(f" Error editing image: {str(e)}")

st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:gray;'>Powered by OpenAI DALL-E | Created with Streamlit</p>",
    unsafe_allow_html=True
)
