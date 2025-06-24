import streamlit as st
from llm.model_handler import query_ollama, query_bedrock
from llm.prompt_templates import FLASK_PROMPT
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
st.set_page_config(page_title="Flask LLM Obsolescence Dashboard")

# Add custom CSS for background and text styling
st.markdown(
    """
    <style>
    .main {
        background-color: #f0f2f6;
        padding: 2rem;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background-image: url('https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=1350&q=80');
        background-size: cover;
        background-position: center;
    }
    .title {
        color: #4a90e2;
        font-weight: 700;
        font-size: 2.5rem;
        margin-bottom: 1rem;
        text-shadow: 1px 1px 2px #000000aa;
    }
    .stRadio > div > label {
        font-weight: 600;
        color: #333333;
    }
    .stTextArea > label {
        font-weight: 600;
        color: #333333;
    }
    .stButton > button {
        background-color: #e63946;
        color: white;
        font-weight: 700;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: background-color 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #d62828;
    }
    .stTextArea textarea {
        font-family: 'Courier New', Courier, monospace;
        font-size: 1rem;
        color: #222222;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<h1 class="title">🔍 Prompt Evaluation for Software Obsolescence</h1>', unsafe_allow_html=True)

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

