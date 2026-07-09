import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
from PIL import Image
from io import BytesIO
from generator import generate_image
from editor import edit_image
from prompt_engine import enhance_prompt

st.set_page_config(page_title="AI Image Generator & Editor", page_icon="🎨", layout="wide")

st.markdown("<h1 style='text-align:center;'> AI Image Generator & Editor</h1>", unsafe_allow_html=True)

# LOAD TOKEN 
def load_token() -> str:
    try:
        return st.secrets["HF_TOKEN"]
    except (KeyError, FileNotFoundError):
        pass
    return os.getenv("HF_TOKEN", "")

HF_TOKEN = load_token()

#  SESSION STATE INIT
# Persists the last generated/uploaded image across reruns
if "canvas_image" not in st.session_state:
    st.session_state.canvas_image = None          # PIL Image ready to edit
if "canvas_label" not in st.session_state:
    st.session_state.canvas_label = ""            # display caption
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "🖼 Generate Image"

# MODE SELECTOR 
mode = st.radio(
    "Choose Mode",
    ["🖼 Generate Image", "✏️ Edit Image"],
    index=0 if st.session_state.active_tab == "🖼 Generate Image" else 1,
    horizontal=True,
    key="mode_radio",
)
st.session_state.active_tab = mode

# GENERATE MODE
if mode == "🖼 Generate Image":
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("📝 Prompt Panel")
        prompt = st.text_area(
            "Describe your image",
            placeholder="e.g. futuristic city at night with neon lights",
            height=150,
        )
        size_choice = st.selectbox(
            "Image Size",
            ["1024x1024", "1152x896", "896x1152", "768x768"],
        )
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
                        img = generate_image(
                            prompt=final_prompt, size=size_choice, api_key=HF_TOKEN
                        )
                        # ── Persist so Edit mode can pick it up ──────────
                        st.session_state.canvas_image = img
                        st.session_state.canvas_label = "Generated Image"

                except Exception as e:
                    st.error(f"❌ Error: {e}")

        # Show image + actions whenever one is available
        if st.session_state.canvas_image is not None:
            img = st.session_state.canvas_image
            st.image(img, use_container_width=True, caption=st.session_state.canvas_label)

            buf = BytesIO()
            img.save(buf, format="PNG")
            buf.seek(0)

            dl_col, edit_col = st.columns(2)
            with dl_col:
                st.download_button(
                    "⬇️ Download Image",
                    buf,
                    "generated_image.png",
                    "image/png",
                    use_container_width=True,
                )
            with edit_col:
                if st.button("✏️ Edit This Image", use_container_width=True, type="secondary"):
                    # Switch to Edit mode with the generated image pre-loaded
                    st.session_state.active_tab = "✏️ Edit Image"
                    st.rerun()

            st.success(" Image generated successfully!")

# EDIT MODE

else:
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("📤 Image Source")

        #  Source selector
        source_options = ["⬆️ Upload an image"]
        if st.session_state.canvas_image is not None:
            source_options.insert(0, "🖼 Use last generated image")

        source = st.radio("Select image source", source_options, horizontal=True)

        uploaded = None
        working_image = None
        working_caption = ""

        if source == "⬆️ Upload an image":
            uploaded = st.file_uploader(
                "Upload an image to edit", type=["png", "jpg", "jpeg"]
            )
            if uploaded:
                working_image = Image.open(uploaded).convert("RGB")
                working_caption = "Uploaded Image"
                # Also persist in session so switching sources is smooth
                st.session_state.canvas_image = working_image
                st.session_state.canvas_label = working_caption
        else:
            # Use the previously generated image
            working_image = st.session_state.canvas_image
            working_caption = st.session_state.canvas_label or "Generated Image"

        st.markdown("---")
        st.subheader("🔧 Edit Instructions")
        edit_prompt = st.text_area(
            "Describe what to change",
            placeholder="e.g. change the background to a beach at sunset",
            height=150,
        )
        edit_btn = st.button("🪄 Apply AI Edit", type="primary", use_container_width=True)

    with col2:
        st.subheader("🖼 Preview")

        if working_image is not None:
            # Show original / current image
            left, right = st.columns(2)
            with left:
                st.image(working_image, caption=f"Source: {working_caption}", use_container_width=True)

            if edit_btn:
                if not edit_prompt.strip():
                    st.error("⚠️ Please enter edit instructions.")
                else:
                    try:
                        with st.spinner("🔄 Editing via HF Inference API…"):
                            final_prompt = enhance_prompt(edit_prompt)
                            st.info(f"✨ **Enhanced Prompt:** {final_prompt}")
                            result = edit_image(
                                image=working_image,
                                prompt=final_prompt,
                                api_key=HF_TOKEN,
                            )

                        with right:
                            st.image(result, caption=" Edited Result", use_container_width=True)

                        buf = BytesIO()
                        result.save(buf, format="PNG")
                        buf.seek(0)

                        dl_col, reuse_col = st.columns(2)
                        with dl_col:
                            st.download_button(
                                " Download Edited Image",
                                buf,
                                "edited_image.png",
                                "image/png",
                                use_container_width=True,
                            )
                        with reuse_col:
                            if st.button(
                                " Edit This Result Again",
                                use_container_width=True,
                                type="secondary",
                            ):
                                # Replace canvas with the edited result for chained edits
                                st.session_state.canvas_image = result
                                st.session_state.canvas_label = "Edited Image"
                                st.rerun()

                        st.success(" Edit applied successfully!")

                    except Exception as e:
                        st.error(f"❌ Error: {e}")
        else:
            st.info(" Upload an image or generate one first, then come here to edit it.")
