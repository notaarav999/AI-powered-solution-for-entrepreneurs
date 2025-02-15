import streamlit as st
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser

from langchain_core.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    AIMessagePromptTemplate,
    ChatPromptTemplate
)

# Custom CSS styling
st.markdown("""
<style>
    .main { background-color: #1a1a1a; color: #ffffff; }
    .sidebar .sidebar-content { background-color: #2d2d2d; }
    .stTextInput textarea { color: #ffffff !important; }
    .stSelectbox div[data-baseweb="select"], .stSelectbox svg, .stSelectbox option, div[role="listbox"] div {
        background-color: #2d2d2d !important; color: white !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("🧠 Entrepreneurial Journey Companion")
st.markdown("**A chatbot brought to you by Aarav, Achintya, Eshan**", unsafe_allow_html=True)
st.caption("🚀 Your AI-powered friend for all your entrepreneurial questions")

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    selected_model = st.selectbox(
        "Choose Model",
        ["deepseek-r1:1.5b", "deepseek-r1:3b"],
        index=0
    )
    st.divider()
    st.markdown("### Model Capabilities")
    st.markdown("""
    - Information Expert
    - Helps in providing the best strategic advice in business
    - Assists in creating a perfect business model and planning
    """)
    st.divider()
    st.markdown("Built with [Ollama](https://ollama.ai/) | [LangChain](https://python.langchain.com/)")

# Initialize the LLM engine
llm_engine = ChatOllama(
    model=selected_model,
    base_url="http://localhost:11434",
    temperature=0.3
)

# System prompt configuration
system_prompt = SystemMessagePromptTemplate.from_template(
    "You are an expert AI business assistant. Provide concise, strategic, and valuable advice for entrepreneurs."
)

# Initialize session state
if "message_log" not in st.session_state:
    st.session_state.message_log = [
        {"role": "ai", "content": "Hi! I'm your business assistant. How can I assist you with your business today? 🚀"}
    ]

# Chat container
chat_container = st.container()

# Display chat messages
with chat_container:
    for message in st.session_state.message_log:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Function to build prompt chain
def build_prompt_chain():
    prompt_sequence = [system_prompt]
    for msg in st.session_state.message_log:
        if msg["role"] == "user":
            prompt_sequence.append(HumanMessagePromptTemplate.from_template(msg["content"]))
        elif msg["role"] == "ai":
            prompt_sequence.append(AIMessagePromptTemplate.from_template(msg["content"]))
    return ChatPromptTemplate.from_messages(prompt_sequence)

# Function to generate AI response
def generate_ai_response(prompt_chain):
    processing_pipeline = prompt_chain | llm_engine | StrOutputParser()
    return processing_pipeline.invoke({})

# Capture user input
user_query = st.chat_input("Type your business question here...")

if user_query:
    # Add user message
    st.session_state.message_log.append({"role": "user", "content": user_query})
    
    # Generate AI response
    with st.spinner("🧠 Processing..."):
        prompt_chain = build_prompt_chain()
        ai_response = generate_ai_response(prompt_chain)
    
    # Add AI response
    st.session_state.message_log.append({"role": "ai", "content": ai_response})
    
    # Refresh chat display
    st.rerun()
    
    
