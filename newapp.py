import streamlit as st
from openai import OpenAI
import google.generativeai as genai
import anthropic
from groq import Groq
from collections import deque
from datetime import datetime

# ====================== Constants & Configuration ======================
MAX_HISTORY_LENGTH = 20
SYSTEM_PROMPT = """You are a helpful and friendly chatbot named "Buddy". 
Your goal is to answer user questions clearly and concisely. 
If you don't know something, politely say "I'm sorry, I don't know" rather than making up information."""

# ====================== LLM Initialization ======================
def get_llm_client(provider):
    """Returns the correct client/model for the selected provider"""
    # if provider == "DeepSeek":
    #     return OpenAI(
    #         base_url="https://api.deepseek.com",
    #         api_key=st.secrets['DEEPSEEK_API_KEY']
        # )
    if provider == "Gemini":
        genai.configure(api_key=st.secrets['GOOGLE_API_KEY'])
        return genai.GenerativeModel("gemini-2.0-flash")
    # elif provider == "Claude":
    #     return anthropic.Client(st.secrets['CLAUDE_API_KEY'])
    elif provider == "Groq":
        return Groq(api_key=st.secrets['GROQ_API_KEY'])

# ====================== Message Format Converters ======================
def convert_to_gemini_messages(history):
    gemini_messages = []
    for msg in history:
        if msg["role"] == "user":
            gemini_messages.append({"role": "user", "parts": [{"text": msg["content"]}]})
        else:
            gemini_messages.append({"role": "model", "parts": [{"text": msg["content"]}]})
    return gemini_messages

def convert_to_claude_messages(history):
    return [{"role": msg["role"], "content": msg["content"]} for msg in history]

# ====================== UI Setup ======================
st.set_page_config(page_title="Buddy Chatbot", page_icon="🤖")
st.title("🤖 Buddy - Your Friendly AI Assistant")

# Sidebar configuration
with st.sidebar:
    st.markdown("## ⚙️ Settings")
    st.markdown(f"**Today's Date:** {datetime.now().strftime('%B %d, %Y')}")
    
    llm_provider = st.selectbox(
        "Choose Provider",
        [ "Gemini", "Groq"],#,"DeepSeek", "Claude"],
        index=0
    )
    
    st.markdown("### Memory Settings")
    current_length = len(st.session_state.get('chat_history', deque()))
    st.write(f"Current memory: {current_length}/{MAX_HISTORY_LENGTH} messages")
    new_length = st.slider("Max conversation memory", 5, 50, MAX_HISTORY_LENGTH)
    
    if st.button("🧹 Clear Chat", help="Reset the conversation history"):
        st.session_state.chat_history = deque(maxlen=new_length)
        st.rerun()

# Initialize chat history with deque
if "chat_history" not in st.session_state:
    st.session_state.chat_history = deque(maxlen=MAX_HISTORY_LENGTH)

# ====================== Chat Processing ======================
def generate_response(provider, client, prompt):
    full_response = ""
    placeholder = st.empty()
    
    try:
        if provider == "DeepSeek":
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[{"role": "system", "content": SYSTEM_PROMPT}] + list(st.session_state.chat_history),
                stream=True
            )
            for chunk in response:
                full_response += chunk.choices[0].delta.content or ""
                placeholder.markdown(full_response + "▌")
        
        elif provider == "Gemini":
            messages = convert_to_gemini_messages([{"role": "system", "content": SYSTEM_PROMPT}] + list(st.session_state.chat_history))
            response = client.generate_content(
                contents=messages + [{"role": "user", "parts": [{"text": prompt}]}],
                stream=True
            )
            for chunk in response:
                full_response += chunk.text
                placeholder.markdown(full_response)
        
        elif provider == "Claude":
            response = client.messages.stream(
                model="claude-3-opus-20240229",
                messages=convert_to_claude_messages(st.session_state.chat_history),
                max_tokens=1000,
                system=SYSTEM_PROMPT
            )
            for chunk in response:
                if chunk.content:
                    full_response += chunk.content[0].text
                    placeholder.markdown(full_response + "▌")
        
        elif provider == "Groq":
            response = client.chat.completions.create(
                model="Llama3-8b-8192",
                messages=[{"role": "system", "content": SYSTEM_PROMPT}] + list(st.session_state.chat_history),
                stream=True
            )
            for chunk in response:
                full_response += chunk.choices[0].delta.content or ""
                placeholder.markdown(full_response + "▌")
        
        return full_response
    
    except Exception as e:
        placeholder.error(f"I'm sorry, I encountered an error: {str(e)}")
        return "I'm sorry, I'm having trouble responding right now."

# ====================== Main Chat Interface ======================
# Display chat history
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Handle new user input
if prompt := st.chat_input("Ask Buddy anything..."):
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.write(prompt)
    
    with st.chat_message("assistant"):
        client = get_llm_client(llm_provider)
        response = generate_response(llm_provider, client, prompt)
        st.session_state.chat_history.append({"role": "assistant", "content": response})