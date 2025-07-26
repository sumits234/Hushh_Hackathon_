import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
import os

st.set_page_config(page_title="🤖 AI Job Assistant", layout="wide")
st.title("🤖 AI Job Application Chat Assistant")

# === Load API Key ===
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    st.error("❌ Please set OPENAI_API_KEY in your .env file.")
    st.stop()

# === LangChain LLM Setup ===
llm = ChatOpenAI(
    openai_api_key=OPENAI_API_KEY,
    temperature=0.7,
    model_name="gpt-3.5-turbo"
)

memory = ConversationBufferMemory()
chat_chain = ConversationChain(llm=llm, memory=memory, verbose=False)

# === Chat UI ===
user_input = st.chat_input("Ask me about your job applications, interviews, resume...")

if user_input:
    with st.spinner("Thinking..."):
        response = chat_chain.run(user_input)
        st.chat_message("user").write(user_input)
        st.chat_message("assistant").write(response)
