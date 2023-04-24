import streamlit as st
import openai
# Set page configuration
st.set_page_config(
    page_title="AI Translation App",
    page_icon=":earth_americas:",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.title("AI Translation App")
st.subheader("Translate text from English to French")
openai.api_key="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"
input = st.text_input("Enter text to translate: ")
default_prompt = "Translate the text from English to"
French:\nText:{}\nTranslation:".format(input)
def translate(input_prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=input_prompt,
        temperature=0.9,
        max_tokens=100,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stop=["\n"]
    )
    return response["choices"][0]["text"].strip()
if st.button("Submit"):
    st.write("==Output==")
    inp_prompt = default_prompt
    output = translate(inp_prompt)
    st.write(output)
