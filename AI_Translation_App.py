import streamlit as st
import openai

# Set your API key securely (Streamlit Cloud: set this in Secrets)
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Set Streamlit page title
st.set_page_config(page_title="Spanish to English Book Translator")

st.title("📚 Spanish to English Book Translator")
st.markdown("Upload a plain text (.txt) file in Spanish. This app will translate it into English using OpenAI GPT-4.")

# File upload
uploaded_file = st.file_uploader("Upload a Spanish text file", type=["txt"])

if uploaded_file is not None:
    # Read the uploaded text file
    raw_text = uploaded_file.read().decode("utf-8")
    st.success("File uploaded successfully.")

    # Optional: Show original text preview
    with st.expander("View original Spanish text"):
        st.text_area("Original text (first 500 characters):", raw_text[:500], height=200)

    # Split text into manageable chunks (adjust word count for longer texts)
    def split_into_chunks(text, max_words=800):
        words = text.split()
        return [" ".join(words[i:i + max_words]) for i in range(0, len(words), max_words)]

    text_chunks = split_into_chunks(raw_text)

    # Translate chunks using OpenAI
    st.info("Translating... This may take a while for large files.")
    translated_chunks = []
    progress = st.progress(0)

    for i, chunk in enumerate(text_chunks):
        prompt = f"""You are a professional literary translator.
Translate the following Spanish text into English.

Text:
{chunk}

English Translation:"""

from openai import OpenAI
client = OpenAI(api_key=...)

from openai import OpenAI
client = OpenAI(api_key=...)

try:
    response = client.chat.completions.create(
        model="gpt-4",
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

    # Display translated result
    st.subheader("✅ Translated Text")
    st.text_area("Translation (preview):", full_translation[:1500], height=300)

    # Offer download as .txt
    st.download_button(
        label="📥 Download Translated Text",
        data=full_translation,
        file_name="translated_text.txt",
        mime="text/plain"
    )
