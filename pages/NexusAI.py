import streamlit as st
# from openai import OpenAI
import google.generativeai as genai
import anthropic
from groq import Groq


from collections import deque
from datetime import datetime
import json

if not st.session_state.get('login_successful', False):
    st.warning("You must log in to access this page.")
    st.stop()  # Stop execution here to prevent rendering the rest of the page
# ====================== Constants & Configuration ======================
MAX_HISTORY_LENGTH = 20
SYSTEM_PROMPT = """You are a helpful and friendly chatbot named "Buddy". 
Your goal is to answer user questions clearly and concisely. 
If you don't know something, politely say "I'm sorry, I don't know" rather than making up information."""


# ====================== Session Management ======================
def load_session(timestamp):
    """Load a specific chat session from history"""
    st.session_state.load_session = timestamp
    st.rerun()
    # session = st.session_state.session_history[timestamp]
    # st.session_state.llm_provider = session["llm_provider"]
    # st.session_state.llm_provider_widget = session["llm_provider"]  # Update widget key
    # st.rerun()

    # if timestamp in st.session_state.session_history:
    #     session = st.session_state.session_history[timestamp]
       
    #     st.session_state.chat_history = deque(session["chat_history"], maxlen=MAX_HISTORY_LENGTH)
        
    #     # # Set provider BEFORE widget creation
    #     st.session_state.llm_provider = session["llm_provider"]  # 👈 Critical change
    #     st.rerun()

def save_current_session():
    """Save current chat session to session history"""
    if "chat_history" in st.session_state and len(st.session_state.chat_history) > 0:
        if "session_history" not in st.session_state:
            st.session_state.session_history = {}
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.session_history[timestamp] = {
            "chat_history": list(st.session_state.chat_history),
            "llm_provider": st.session_state.get('llm_provider', 'Gemini')
        }





# ====================== LLM Initialization ======================
def get_llm_client(provider):
    """Returns the correct client/model for the selected provider"""
    if provider == "Gemini":
        genai.configure(api_key=st.secrets['GOOGLE_API_KEY'])
        return genai.GenerativeModel("gemini-2.0-flash")
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


# ====================== UI Setup ======================
st.set_page_config(page_title="Buddy Chatbot", page_icon="💬")
# Title
st.title("💬 Hi, I'm Nexus.ai!")
st.title("How can I help you Today??")
st.markdown("<hr style='border: 1px solid #ccc; opacity: 0.5;'>", unsafe_allow_html=True)


# Initialize session state FIRST
if "chat_history" not in st.session_state:
    st.session_state.chat_history = deque(maxlen=MAX_HISTORY_LENGTH)
if "session_history" not in st.session_state:
    st.session_state.session_history = {}

# Handle session loading BEFORE rendering widgets
if "load_session" in st.session_state:
    st.write("Session History:", st.session_state.session_history)
    session = st.session_state.session_history[st.session_state.load_session]
    st.session_state.chat_history = deque(session["chat_history"], maxlen=MAX_HISTORY_LENGTH)
    st.session_state.llm_provider = session["llm_provider"]  # Set BEFORE widget
    st.session_state.llm_provider_widget = session["llm_provider"]  # Set BEFORE widget
    del st.session_state.load_session  # Remove the signal
    st.rerun()





# THEN create sidebar widgets
# Sidebar configuration
with st.sidebar:
    st.markdown("## ⚙️ Settings")
    st.markdown(f"**Today's Date:** {datetime.now().strftime('%B %d, %Y')}")


    #  llm_provider = st.selectbox(
    #     "Choose Provider",
    #     ["Gemini", "Groq"],
    #     index=0,
    #     key='llm_provider'   
    # )

    
    def on_provider_change():
        st.session_state.llm_provider = st.session_state.llm_provider_widget

    # Set default if not present
    if 'llm_provider' not in st.session_state:
        st.session_state.llm_provider = "Gemini"
    if 'llm_provider_widget' not in st.session_state:
        st.session_state.llm_provider_widget = st.session_state.llm_provider


    llm_provider = st.selectbox(
        "Choose Provider",
        ["Gemini", "Groq"],
        key='llm_provider_widget',
        on_change=on_provider_change
    )

   
    #  # Update session state when widget changes
    # if st.session_state.llm_provider_widget != st.session_state.llm_provider:
    #     st.session_state._set_item("llm_provider", st.session_state.llm_provider_widget)

    
    st.markdown("### Memory Settings")
    current_length = len(st.session_state.chat_history)
    st.write(f"Current memory: {current_length}/{MAX_HISTORY_LENGTH} messages")
    new_length = st.slider("Max conversation memory", 5, 50, MAX_HISTORY_LENGTH)
    
    if st.button("💾 Save Current Chat", help="Save this conversation to history"):
        save_current_session()
        st.success("Chat saved!")
    
    if st.button("🧹 Clear Chat", help="Reset the conversation history"):
        st.session_state.chat_history = deque(maxlen=new_length)
        st.rerun()
    
    # Session History Section
    st.markdown("## 📚 Chat History")
    if st.session_state.session_history:
        for timestamp in sorted(st.session_state.session_history.keys(), reverse=True):
            session = st.session_state.session_history[timestamp]
            preview = session["chat_history"][0]["content"][:30] + "..." if session["chat_history"] else "Empty"
            
            cols = st.columns([3, 1])
            cols[0].write(f"**{timestamp}**")
            cols[0].caption(f"{preview}")
            
            if cols[1].button("Load", key=f"load_{timestamp}"):
                with st.spinner("Loading session..."): load_session(timestamp)
                st.session_state.load_session = timestamp
                
            
            if cols[1].button("✖", key=f"delete_{timestamp}"):
                del st.session_state.session_history[timestamp]
                st.rerun()
    else:
        st.write("No saved chats yet")

# Rest of your existing code remains the same...
# [Previous chat processing and display code here]
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
