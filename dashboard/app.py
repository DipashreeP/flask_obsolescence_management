import streamlit as st
from llm.model_handler import query_ollama, query_bedrock
from llm.prompt_templates import FLASK_PROMPT
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
st.set_page_config(page_title="Flask LLM Obsolescence Dashboard")
st.title("🔍 Prompt Evaluation for Software Obsolescence")

backend = st.radio("Choose backend:", ["Ollama", "Amazon Bedrock", "Transformers"])
code_input = st.text_area("Paste your Flask code or requirements.txt", height=250)


if st.button("Analyze Code"):
    prompt = FLASK_PROMPT.format(code=code_input)

    if backend == "Ollama":
        output = query_ollama(prompt)
    elif backend == "Amazon Bedrock":
        output = query_bedrock(prompt)
    else:
        from llm.transformer_handler import classify_obsolescence
        output = classify_obsolescence(code_input)

    st.text_area("🧠 Model Output", str(output), height=200)

