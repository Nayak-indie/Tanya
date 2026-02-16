"""
Tanya Web Interface (Streamlit)
--------------------------------
A modern web UI for interacting with Tanya AI assistant.
"""

import streamlit as st
import requests
import json
import os
import sys
import time
from datetime import datetime

# Add Tanya to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Page config
st.set_page_config(
    page_title="Tanya AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        background-color: #0e1117;
    }
    .stTextInput > div > div > input {
        background-color: #262730;
        color: white;
    }
    .chat-message {
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    .user-message {
        background-color: #262730;
        border-left: 4px solid #4a9eff;
    }
    .assistant-message {
        background-color: #1a1d24;
        border-left: 4px solid #00cc88;
    }
    .status-indicator {
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        margin-right: 8px;
    }
    .status-online { background-color: #00cc88; }
    .status-offline { background-color: #ff4b4b; }
    .status-thinking { background-color: #ffaa00; }
</style>
""", unsafe_allow_html=True)


class TanyaClient:
    """Client to communicate with Tanya backend."""
    
    def __init__(self, ollama_url="http://localhost:11434"):
        self.ollama_url = ollama_url
    
    def check_status(self):
        """Check if Ollama is running."""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def list_models(self):
        """List available models."""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            if response.status_code == 200:
                data = response.json()
                return [m['name'] for m in data.get('models', [])]
        except:
            pass
        return []
    
    def chat(self, message, model="llama3.2:3b", system_prompt=None):
        """Send a message and get response."""
        if system_prompt is None:
            system_prompt = """You are Tanya — an assistant created by Vinayak (nayak-indie).
State your identity clearly when asked: 'I am Tanya, your assistant created by Vinayak.'
Be confident, helpful, and concise. Prioritize answering the user's question directly.
When appropriate, reference your ability to inspect files, run local tools, and reason about code or tasks.
Do not invent facts; if unsure, state uncertainty and propose a next step."""
        
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            "stream": False
        }
        
        try:
            response = requests.post(
                f"{self.ollama_url}/api/chat",
                json=payload,
                timeout=120
            )
            if response.status_code == 200:
                data = response.json()
                return data.get('message', {}).get('content', '')
            else:
                return f"Error: {response.status_code} - {response.text}"
        except requests.exceptions.Timeout:
            return "Error: Request timed out. The model might be loading."
        except Exception as e:
            return f"Error: {str(e)}"


# Initialize client
if 'tanya_client' not in st.session_state:
    st.session_state.tanya_client = TanyaClient()

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'current_model' not in st.session_state:
    st.session_state.current_model = "llama3.2:3b"


def main():
    """Main Streamlit app."""
    
    # Sidebar
    with st.sidebar:
        st.title("🤖 Tanya AI")
        
        # Status
        st.subheader("Status")
        client = st.session_state.tanya_client
        
        if client.check_status():
            st.markdown('<span class="status-indicator status-online"></span> Ollama Online', 
                       unsafe_allow_html=True)
        else:
            st.markdown('<span class="status-indicator status-offline"></span> Ollama Offline', 
                       unsafe_allow_html=True)
            st.warning("Make sure Ollama is running: `ollama serve`")
        
        # Model selection
        st.subheader("Settings")
        models = client.list_models()
        if models:
            selected_model = st.selectbox("Model", models, index=models.index(st.session_state.current_model) if st.session_state.current_model in models else 0)
            st.session_state.current_model = selected_model
        else:
            st.info("No models loaded. Run: `ollama pull llama3.2:3b`")
        
        # Clear chat
        if st.button("🗑️ Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()
        
        # Model info
        st.subheader("Model Info")
        st.caption(f"Using: {st.session_state.current_model}")
        
        # Quick actions
        st.subheader("Quick Actions")
        if st.button("👋 Say Hello"):
            st.session_state.chat_history.append({
                "role": "user", 
                "content": "Say hello and introduce yourself"
            })
            st.rerun()
    
    # Main chat area
    st.title("💬 Chat with Tanya")
    
    # Display chat history
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f"""
            <div class="chat-message user-message">
                <strong>You:</strong><br>
                {msg['content']}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-message assistant-message">
                <strong>Tanya:</strong><br>
                {msg['content']}
            </div>
            """, unsafe_allow_html=True)
    
    # Input area
    if prompt := st.chat_input("Type your message...", key="chat_input"):
        # Add user message
        st.session_state.chat_history.append({
            "role": "user",
            "content": prompt
        })
        
        # Show thinking indicator
        with st.spinner("🤔 Tanya is thinking..."):
            # Get response
            response = st.session_state.tanya_client.chat(
                prompt, 
                model=st.session_state.current_model
            )
        
        # Add assistant response
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": response
        })
        
        # Rerun to update UI
        st.rerun()


if __name__ == "__main__":
    main()
