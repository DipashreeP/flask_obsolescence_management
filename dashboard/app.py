import streamlit as st
from llm.model_handler import query_ollama, query_bedrock
from llm.prompt_templates import FLASK_PROMPT

st.set_page_config(page_title="Flask LLM Obsolescence Dashboard")
st.title("🔍 Prompt Evaluation for Flask Obsolescence")

backend = st.radio("Choose backend:", ["Ollama", "Amazon Bedrock"])
code_input = st.text_area("Paste your Flask code or requirements.txt", height=250)

if st.button("Analyze Code"):
    prompt = FLASK_PROMPT.format(code=code_input)
    if backend == "Ollama":
        output = query_ollama(prompt)
    else:
        output = query_bedrock(prompt)
    st.text_area("🧠 LLM Output", output, height=200)
