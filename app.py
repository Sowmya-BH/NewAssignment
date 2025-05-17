import streamlit as st
from openai import OpenAI
import google.generativeai as genai
import anthropic
from groq import Groq

# # ============== GLOBAL CONFIGURATION ==============
# PROVIDER_MODELS = {
#     "DeepSeek": "deepseek-chat",
#     "Gemini": "gemini-2.0-flash",
#     "Claude": "claude-3-opus-20240229",
#     "Groq": "Gemma-7b-It"  # Current working model
# }

# # ============== CLIENT INITIALIZATION ==============
# def get_llm_client(provider):
#     """Initialize the correct client for the selected provider"""
#     if provider == "DeepSeek":
#         return OpenAI(
#             base_url="https://api.deepseek.com",
#             api_key=st.secrets['DEEPSEEK_API_KEY']
#         )
#     elif provider == "Gemini":
#         genai.configure(api_key=st.secrets['GOOGLE_API_KEY'])
#         return genai.GenerativeModel(PROVIDER_MODELS["Gemini"])
#     elif provider == "Claude":
#         return anthropic.Client(st.secrets['CLAUDE_API_KEY'])
#     elif provider == "Groq":
#         return Groq(api_key=st.secrets['GROQ_API_KEY'])

# # ============== STREAMLIT UI ==============
# st.sidebar.markdown("## LLM Configuration")
# selected_provider = st.sidebar.selectbox(
#     "Choose Provider",
#     list(PROVIDER_MODELS.keys()),
#     index=0
# )

# # Dynamic model selection
# if selected_provider == "Claude":
#     PROVIDER_MODELS["Claude"] = st.sidebar.selectbox(
#         "Claude Model",
#         ["claude-3-opus-20240229", "claude-3-sonnet-20240229"]
#     )
# elif selected_provider == "Groq":
#     PROVIDER_MODELS["Groq"] = st.sidebar.selectbox(
#         "Groq Model",
#         ['Llama3-8b-8192', 'Llama3-70b-8192','Gemma-7b-It'],
#         index=0
#     )

# # ============== CHAT PROCESSING ==============
# def generate_response(provider, client, prompt):
#     full_response = ""
#     placeholder = st.empty()
    
#     try:
#         if provider == "DeepSeek":
#             response = client.chat.completions.create(
#                 model=PROVIDER_MODELS["DeepSeek"],
#                 messages=[{"role": "system", "content": "You're helpful"}] + st.session_state.chat_history,
#                 stream=True
#             )
#             for chunk in response:
#                 full_response += chunk.choices[0].delta.content or ""
#                 placeholder.markdown(full_response + "▌")

#         elif provider == "Groq":
#             response = client.chat.completions.create(
#                 model=PROVIDER_MODELS["Groq"],  # Use the selected Groq model
#                 messages=[{"role": "system", "content": "Be helpful"}] + st.session_state.chat_history,
#                 stream=True
#             )
#             for chunk in response:
#                 full_response += chunk.choices[0].delta.content or ""
#                 placeholder.markdown(full_response + "▌")
        
#         # [Other providers...]
        
#         return full_response
    
#     except Exception as e:
#         st.error(f"API Error: {str(e)}")
#         raise

# # ============== MAIN CHAT INTERFACE ==============
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []

# for msg in st.session_state.chat_history:
#     with st.chat_message(msg["role"]):
#         st.write(msg["content"])

# if prompt := st.chat_input("Ask me anything"):
#     st.session_state.chat_history.append({"role": "user", "content": prompt})
    
#     with st.chat_message("user"):
#         st.write(prompt)
    
#     with st.chat_message("assistant"):
#         try:
#             client = get_llm_client(selected_provider)
#             response = generate_response(selected_provider, client, prompt)
#             st.session_state.chat_history.append({"role": "assistant", "content": response})
#         except Exception as e:
#             st.error(f"Response generation failed: {str(e)}")

# # Clear chat button
# with st.sidebar:
#     if st.button("🧹 Clear Chat"):
#         st.session_state.chat_history = []
#         st.rerun()







import streamlit as st
from openai import OpenAI  # For DeepSeek/Groq
import google.generativeai as genai  # For Gemini
import anthropic  # For Claude
from groq import Groq  # For Groq
# https://github.com/AbeTavarez/DeepSeekChatbot/blob/main/app.py
# ====================== LLM Initialization ======================
def get_llm_client(provider):
    """Returns the correct client/model for the selected provider"""
    if provider == "DeepSeek":
        return OpenAI(
            base_url="https://api.deepseek.com",
            api_key=st.secrets['DEEPSEEK_API_KEY']
        )
    elif provider == "Gemini":
        genai.configure(api_key=st.secrets['GOOGLE_API_KEY'])
        return genai.GenerativeModel("gemini-2.0-flash")
    elif provider == "Claude":
        return anthropic.Client(st.secrets['CLAUDE_API_KEY'])
    elif provider == "Groq":
#         MODELS["Groq"] = st.sidebar.selectbox("Model", ['Llama3-8b-8192', 'Llama3-70b-8192','Gemma-7b-It']
# )
        return Groq(api_key=st.secrets['GROQ_API_KEY'])

# ====================== Message Format Converters ======================
def convert_to_gemini_messages(history):
    """Convert OpenAI-format messages to Gemini format"""
    gemini_messages = []
    for msg in history:
        if msg["role"] == "user":
            gemini_messages.append({"role": "user", "parts": [{"text": msg["content"]}]})
        else:
            gemini_messages.append({"role": "model", "parts": [{"text": msg["content"]}]})
    return gemini_messages

def convert_to_claude_messages(history):
    """Convert messages to Claude format"""
    return [{"role": msg["role"], "content": msg["content"]} for msg in history]

# ====================== UI Setup ======================
st.sidebar.markdown("## LLM Selection")
llm_provider = st.sidebar.selectbox(
    "Choose Provider",
    ["DeepSeek", "Gemini", "Claude", "Groq"],
    index=0
)

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ====================== Chat Processing ======================
def generate_response(provider, client, prompt):
    """Generate response using the selected provider"""
    full_response = ""
    placeholder = st.empty()
    
    try:
        if provider == "DeepSeek":
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[{"role": "system", "content": "You're helpful"}] + st.session_state.chat_history,
                stream=True
            )
            for chunk in response:
                full_response += chunk.choices[0].delta.content or ""
                placeholder.markdown(full_response + "▌")
        
        elif provider == "Gemini":
            # Convert messages to Gemini format
            messages = convert_to_gemini_messages(st.session_state.chat_history)
            response = client.generate_content(
                contents=messages + [{"role": "user", "parts": [{"text": prompt}]}],
                stream=True
            )
            for chunk in response:
                full_response += chunk.text
                placeholder.markdown(full_response )
        
        elif provider == "Claude":
            response = client.messages.stream(
                model="claude-3-opus-20240229",
                messages=convert_to_claude_messages(st.session_state.chat_history),
                max_tokens=1000,
                system="You're a helpful assistant"
            )
            for chunk in response:
                if chunk.content:
                    full_response += chunk.content[0].text
                    placeholder.markdown(full_response + "▌")
        
        elif provider == "Groq":
            response = client.chat.completions.create(
                model= "Llama3-8b-8192",
                messages=[{"role": "system", "content": "Be helpful"}] + st.session_state.chat_history,
                stream=True
            )
            for chunk in response:
                full_response += chunk.choices[0].delta.content or ""
                placeholder.markdown(full_response + "▌")
        
        return full_response
    
    except Exception as e:
        st.error(f"Error generating response: {str(e)}")
        raise

# ====================== Main Chat Interface ======================
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("Ask me anything"):
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.write(prompt)
    
    with st.chat_message("assistant"):
        try:
            client = get_llm_client(llm_provider)
            response = generate_response(llm_provider, client, prompt)
            st.session_state.chat_history.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"Failed to get response: {str(e)}")
            print(f"Error with {llm_provider}: {e}")

# Clear chat button
with st.sidebar:
    if st.button("🧹 Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()



# import streamlit as st
# from openai import OpenAI  # For DeepSeek/Groq
# import google.generativeai as genai  # For Gemini
# import anthropic  # For Claude
# from groq import Groq  # For Groq
# st.title("🐳 DeepSeek")
# st.subheader("❔⍰❓☑️💬✅🤖Hi, How can I help you today",divider='blue')

# # ====================== Sidebar UI ==================
# st.sidebar.markdown("## Parameters")
# st.sidebar.divider()
# temp = st.sidebar.slider("Temperature", 0.0, 1.0, value=0.5)

# # ====================== Sidebar UI- LLM Selection ======================
# st.sidebar.markdown("## LLM Selection")
# llm_provider = st.sidebar.selectbox(
#     "Choose LLM Provider",
#     ["DeepSeek", "Gemini", "Claude", "Groq"],
#     index=0
# )


# # ====================== Provider-Specific Setup ======================
# def get_llm_client(provider):
#     """Returns the correct client for the selected provider"""
#     if provider == "DeepSeek":
#         return OpenAI(
#             base_url="https://api.deepseek.com",
#             api_key=st.secrets['DEEPSEEK_API_KEY']
#         )
#     elif provider == "Gemini":
#         genai.configure(api_key=st.secrets['GOOGLE_API_KEY'])
#         return genai.GenerativeModel('gemini-pro')  # Return model directly
#     # elif provider == "Claude":
#     #     return anthropic.Client(st.secrets['CLAUDE_API_KEY'])
#     elif provider == "Groq":
#         return Groq(api_key=st.secrets['GROQ_API_KEY'])
#     else:
#         raise ValueError("Invalid provider")
    
    

# # ====================== Unified Chat Interface ======================
# st.title("Multi-LLM Chat Assistant")
# st.subheader(f"Currently using: {llm_provider}", divider='blue')



# # # Display chat history
# # for msg in st.session_state.chat_history:
# #     with st.chat_message(msg["role"]):
# #         st.write(msg["content"])


# # ========================= API Client ===================
# # =================== API Client ==============
# # client = OpenAI(
# #     base_url="https://api.deepseek.com",
# #     api_key=st.secrets['DEEPSEEK_API_KEY']
# # )



# # ====== Chat History =======
# # Initialize chat history
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []


# if st.sidebar.button("💣 Reset Everything"):
#     for key in list(st.session_state.keys()):
#         del st.session_state[key]
#     st.rerun()


# def render_chat_history_messages():
#     print(st.session_state.chat_history)
    
#     if len(st.session_state.chat_history) > 0:
#         for message in st.session_state.chat_history:
#             with st.chat_message(message["role"]):
#                 st.write(message["content"])

# render_chat_history_messages()


# # ================================= Chat Processing ===========================
# def process_response(provider, client, prompt):
#     """Handle provider-specific response generation"""
#     full_response = ""
#     placeholder = st.empty()
    
#     if provider == "DeepSeek":
#         response = client.chat.completions.create(
#             model="deepseek-chat",
#             messages=[{"role": "system", "content": "You're helpful"}] + st.session_state.chat_history,
#             stream=True
#         )
#         for chunk in response:
#             full_response += chunk.choices[0].delta.content or ""
#             placeholder.markdown(full_response + "▌")
    
#     elif provider == "Gemini":
#         # Note: Gemini client is the model itself in this implementation
#         response = client.generate_content(
#             st.session_state.chat_history[-2:] + [{"role": "user", "parts": [prompt]}],
#             stream=True
#         )
#         for chunk in response:
#             full_response += chunk.text
#             placeholder.markdown(full_response + "▌")
    
#     elif provider == "Claude":
#         with client.messages.stream(
#             model="claude-3-opus-20240229",
#             messages=st.session_state.chat_history,
#             max_tokens=1000
#         ) as stream:
#             for chunk in stream:
#                 if chunk.content:
#                     full_response += chunk.content[0].text
#                     placeholder.markdown(full_response + "▌")
    
#     elif provider == "Groq":
#         response = client.chat.completions.create(
#             model="mixtral-8x7b-32768",
#             messages=[{"role": "system", "content": "Be helpful"}] + st.session_state.chat_history,
#             stream=True
#         )
#         for chunk in response:
#             full_response += chunk.choices[0].delta.content or ""
#             placeholder.markdown(full_response + "▌")
    
#     placeholder.markdown(full_response)
#     return full_response
#   # Final message


#         # # display the assistant message
#         # with st.chat_message("assistant",avatar='↪️'):
#         #     # placeholder for the llm response
#         #     client = get_llm_client(llm_provider)
#         #     placeholder = st.empty()
#         #     full_response = ""

#         #     # Prepare messages for API (ensure valid roles)
#         #     chat_completion = client.chat.completions.create(
#         #     model="deepseek-chat",
#         #     messages=[
#         #         {"role": "system", "content": "You're a helpful assistant"}
#         #     ] + st.session_state.chat_history,
#         #     stream=True,
#         #     temperature=temp
#         #     )

#         # st.session_state.chat_history.append(
#         #     {"role": "assistant", "content": full_response}
#         #     )


#     #         # Update the message in real-time with a typing cursor
#     #         placeholder.markdown(full_response + "▌")
        
#     #     # Final update without cursor
#     #     placeholder.markdown(full_response)
    
#     # # Add assistant's full response to history
#     # st.session_state.chat_history.append({"role": "assistant", "content": full_response})

# # ====================== Main Chat Interface ======================
# for msg in st.session_state.chat_history:
#     with st.chat_message(msg["role"]):
#         st.write(msg["content"])

# if prompt := st.chat_input("Ask me anything"):
#     st.session_state.chat_history.append({"role": "user", "content": prompt})
    
#     with st.chat_message("user"):
#         st.write(prompt)
    
#     with st.chat_message("assistant"):
#         try:
#             client = get_llm_client(llm_provider)
#             response = process_response(llm_provider, client, prompt)
#             st.session_state.chat_history.append({"role": "assistant", "content": response})
#         except Exception as e:
#             st.error(f"Error: {str(e)}")
#             print(f"Error with {llm_provider}: {e}")