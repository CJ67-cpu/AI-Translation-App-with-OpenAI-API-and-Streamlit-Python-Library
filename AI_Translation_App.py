
import streamlit as st
from openai import OpenAI
from docx import Document
from langdetect import detect, DetectorFactory
from io import BytesIO
from prompt_modules import (
    gender_module, genre_style_module, consistency_module,
    dialogue_module, idiom_module, formatting_module
)
import re

# Set consistent detection
DetectorFactory.seed = 0

# Check for API key
if "OPENAI_API_KEY" not in st.secrets:
    st.error("🔐 OPENAI_API_KEY is not set. Please add it in your Streamlit Cloud app settings under 'Secrets'.")
    st.stop()

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="Book Translator")

st.title("📚 Book Translator")
st.markdown("Upload a plain text (.txt) or Word (.docx) file in any language. This app will detect the language and translate it into English using GPT-4 or GPT-3.5 Turbo.")

# Model selection
model_choice = st.selectbox("Choose translation quality:", ["GPT-3.5 Turbo", "GPT-4 Turbo"])
model = "gpt-3.5-turbo" if model_choice == "GPT-3.5 Turbo" else "gpt-4"

# Optional style prompt
custom_instruction = st.text_input(
    "Optional: Add a style or tone instruction (e.g. 'translate like a gothic novel')",
    placeholder="Leave blank for default translation"
)

# File upload
uploaded_file = st.file_uploader("Upload a text or Word file", type=["txt", "docx"])

def read_uploaded_file(uploaded_file):
    if uploaded_file.name.endswith(".txt"):
        return uploaded_file.read().decode("utf-8")
    elif uploaded_file.name.endswith(".docx"):
        doc = Document(uploaded_file)
        return "\n".join([para.text for para in doc.paragraphs])
    else:
        st.error("Unsupported file format.")
        return ""

# Improved chunking that preserves paragraph breaks
def split_into_chunks(text, max_words=800):
    paragraphs = re.split(r'\n\s*\n', text)  # Split by blank lines = paragraphs
    chunks = []
    current_chunk = []
    current_word_count = 0

    for para in paragraphs:
        word_count = len(para.split())
        if current_word_count + word_count <= max_words:
            current_chunk.append(para)
            current_word_count += word_count
        else:
            chunks.append("\n\n".join(current_chunk))
            current_chunk = [para]
            current_word_count = word_count

    if current_chunk:
        chunks.append("\n\n".join(current_chunk))

    return chunks

if uploaded_file is not None:
    raw_text = read_uploaded_file(uploaded_file)
    st.success("File uploaded successfully.")

    # Detect language
    detected_lang = detect(raw_text)
    st.write(f"🌍 Detected language: **{detected_lang.upper()}**")

    with st.expander("View original text"):
        st.text_area("Original text (first 500 characters):", raw_text[:500], height=200)

    word_count = len(raw_text.split())
    estimated_tokens = word_count * 2

    if model == "gpt-3.5-turbo":
        cost = (estimated_tokens / 1000) * (0.0015 + 0.002)
    else:
        cost = (estimated_tokens / 1000) * (0.01 + 0.03)

    st.info(f"Estimated translation cost using {model_choice}: **${cost:.2f}** for ~{word_count} words")

    text_chunks = split_into_chunks(raw_text)

    if st.button("Translate Text"):
        st.info("Translating... This may take a while for large files.")
        translated_chunks = []
        progress = st.progress(0)

        gender_sensitive_languages = ["es", "it", "pt", "fr"]

        for i, chunk in enumerate(text_chunks):
            injected_modules = [
                consistency_module,
                dialogue_module,
                idiom_module,
                formatting_module
            ]

            if detected_lang in gender_sensitive_languages:
                injected_modules.insert(0, gender_module)

            if custom_instruction.strip():
                injected_modules.append(genre_style_module(custom_instruction.strip()))

            translation_instructions = "\n\n".join(injected_modules)

            prompt = f"""You are a professional literary translator. Translate the following text from {detected_lang} into English.

{translation_instructions}

Text:
{chunk}

English Translation:"""

            try:
                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant who translates books."},
                        {"role": "user", "content": prompt}
                    ]
                )
                translation = response.choices[0].message.content
                translated_chunks.append(translation)
            except Exception as e:
                st.error(f"Error translating chunk {i+1}: {e}")
                translated_chunks.append("[Translation failed for this part]")

            progress.progress((i + 1) / len(text_chunks))

        full_translation = "\n\n".join(translated_chunks)

        st.subheader("✅ Translated Text")
        st.text_area("Translation (preview):", full_translation[:1500], height=300)

        # Create DOCX in memory
        doc = Document()
        doc.add_heading("Translated Document", 0)

        for paragraph in full_translation.split("\n\n"):
            doc.add_paragraph(paragraph)

        buffer = BytesIO()
        doc.save(buffer)
        buffer.seek(0)

        st.download_button(
            label="📥 Download Translated .docx",
            data=buffer,
            file_name="translated_text.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )


        st.download_button(
            label="📥 Download Translated .docx",
            data=buffer,
            file_name="translated_text.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
