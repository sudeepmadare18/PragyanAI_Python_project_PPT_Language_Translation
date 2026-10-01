import streamlit as st
from pptx import Presentation
from transformers import MarianMTModel, MarianTokenizer
from io import BytesIO
import os
import re

# ---------------------------------------------------------
# STREAMLIT CONFIG
# ---------------------------------------------------------

st.set_page_config(
    page_title="PPT Translator",
    page_icon="📊",
    layout="wide"
)

st.title("📊 PowerPoint Translator")
st.write("Upload a PPTX → Extract text → Translate → Download translated PPTX")


# ---------------------------------------------------------
# LANGUAGE CONFIGURATION
# ---------------------------------------------------------

LANGUAGES = {
    "English → Hindi": {
        "model": "Helsinki-NLP/opus-mt-en-hi"
    },
    "English → French": {
        "model": "Helsinki-NLP/opus-mt-en-fr"
    },
    "English → German": {
        "model": "Helsinki-NLP/opus-mt-en-de"
    },
    "English → Spanish": {
        "model": "Helsinki-NLP/opus-mt-en-es"
    },
    "English → Italian": {
        "model": "Helsinki-NLP/opus-mt-en-it"
    },
    "English → Portuguese": {
        "model": "Helsinki-NLP/opus-mt-en-ROMANCE"
    }
}


# ---------------------------------------------------------
# LOAD TRANSLATION MODEL
# ---------------------------------------------------------

@st.cache_resource
def load_translation_model(model_name):

    tokenizer = MarianTokenizer.from_pretrained(model_name)

    model = MarianMTModel.from_pretrained(model_name)

    return tokenizer, model


# ---------------------------------------------------------
# TRANSLATE TEXT
# ---------------------------------------------------------

def translate_text(text, tokenizer, model):

    if not text or not text.strip():
        return text

    try:

        # Keep line breaks
        lines = text.split("\n")

        translated_lines = []

        for line in lines:

            line = line.strip()

            if not line:
                translated_lines.append("")
                continue

            # Tokenize
            inputs = tokenizer(
                line,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=512
            )

            # Translate
            translated = model.generate(
                **inputs,
                max_length=512
            )

            result = tokenizer.decode(
                translated[0],
                skip_special_tokens=True
            )

            translated_lines.append(result)

        return "\n".join(translated_lines)

    except Exception as e:

        st.warning(f"Translation error: {e}")

        return text


# ---------------------------------------------------------
# EXTRACT TEXT FROM PPT
# ---------------------------------------------------------

def extract_text_from_ppt(prs):

    all_text = []

    for slide_number, slide in enumerate(prs.slides, start=1):

        slide_data = []

        for shape in slide.shapes:

            if hasattr(shape, "text"):

                text = shape.text.strip()

                if text:

                    slide_data.append(text)

        all_text.append({
            "slide_number": slide_number,
            "texts": slide_data
        })

    return all_text


# ---------------------------------------------------------
# CREATE TRANSLATED PPT
# ---------------------------------------------------------

def translate_ppt(
    uploaded_file,
    tokenizer,
    model,
    progress_bar
):

    uploaded_file.seek(0)

    prs = Presentation(uploaded_file)

    total_slides = len(prs.slides)

    for slide_index, slide in enumerate(prs.slides):

        shapes = list(slide.shapes)

        for shape in shapes:

            # Check if shape contains text
            if not hasattr(shape, "text_frame"):
                continue

            if not shape.has_text_frame:
                continue

            # Translate each paragraph
            for paragraph in shape.text_frame.paragraphs:

                for run in paragraph.runs:

                    original_text = run.text

                    if original_text.strip():

                        translated_text = translate_text(
                            original_text,
                            tokenizer,
                            model
                        )

                        run.text = translated_text

        progress = (slide_index + 1) / total_slides

        progress_bar.progress(
            progress,
            text=f"Translating slide {slide_index + 1}/{total_slides}"
        )

    # Save PPT into memory
    output = BytesIO()

    prs.save(output)

    output.seek(0)

    return output


# ---------------------------------------------------------
# FILE UPLOAD
# ---------------------------------------------------------

uploaded_file = st.file_uploader(
    "📁 Upload your PowerPoint file",
    type=["pptx"]
)


# ---------------------------------------------------------
# LANGUAGE SELECTION
# ---------------------------------------------------------

language_option = st.selectbox(
    "🌐 Select translation language",
    list(LANGUAGES.keys())
)


# ---------------------------------------------------------
# MAIN PROCESS
# ---------------------------------------------------------

if uploaded_file:

    st.success(
        f"Uploaded: {uploaded_file.name}"
    )

    # ---------------------------------------------
    # Extract text preview
    # ---------------------------------------------

    uploaded_file.seek(0)

    prs_preview = Presentation(uploaded_file)

    extracted_text = extract_text_from_ppt(
        prs_preview
    )

    st.subheader("📄 Extracted Text")

    for slide_data in extracted_text:

        slide_number = slide_data["slide_number"]

        with st.expander(
            f"Slide {slide_number}"
        ):

            if slide_data["texts"]:

                for text in slide_data["texts"]:

                    st.write(text)

            else:

                st.write(
                    "No text found on this slide."
                )

    # ---------------------------------------------
    # Translate button
    # ---------------------------------------------

    st.divider()

    if st.button(
        "🌐 Translate PPT",
        type="primary",
        use_container_width=True
    ):

        model_name = LANGUAGES[
            language_option
        ]["model"]

        st.info(
            f"Loading translation model for {language_option}..."
        )

        try:

            tokenizer, model = load_translation_model(
                model_name
            )

            st.success(
                "Translation model loaded successfully."
            )

            progress_bar = st.progress(
                0,
                text="Starting translation..."
            )

            translated_ppt = translate_ppt(
                uploaded_file,
                tokenizer,
                model,
                progress_bar
            )

            progress_bar.progress(
                1.0,
                text="Translation completed!"
            )

            st.success(
                "✅ PPT translation completed successfully!"
            )

            # -----------------------------------------
            # Download button
            # -----------------------------------------

            original_name = uploaded_file.name

            base_name = os.path.splitext(
                original_name
            )[0]

            # Clean language name
            target_language = language_option.split("→")[1].strip()

            output_filename = (
                f"{base_name}_translated_{target_language}.pptx"
            )

            st.download_button(
                label="⬇️ Download Translated PPT",
                data=translated_ppt.getvalue(),
                file_name=output_filename,
                mime=(
                    "application/"
                    "vnd.openxmlformats-officedocument."
                    "presentationml.presentation"
                ),
                use_container_width=True
            )

        except Exception as e:

            st.error(
                "❌ Translation failed."
            )

            st.exception(e)
