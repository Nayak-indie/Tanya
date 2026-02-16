"""
Tanya Web Interface (Streamlit) - Jarvis Edition
================================================
A modern, visually stunning web UI for Tanya AI assistant.
Features:
- Animated eyes that respond to states (thinking, listening, speaking, idle)
- Voice input/output integration
- Real-time sync with Tanya backend
- System status dashboard
- Task management
- File browser
- Full system control
"""

import streamlit as st
import requests
import json
import os
import sys
import time
import threading
from datetime import datetime
from pathlib import Path

# Add Tanya to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Page config
st.set_page_config(
    page_title="Tanya AI - Jarvis Mode",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============== CUSTOM CSS FOR EYES AND UI ==============
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@300;500;700&display=swap');
    
    /* Base styles */
    .main {
        background: linear-gradient(135deg, #0a0a0f 0%, #1a1a2e 50%, #0f0f1a 100%);
        font-family: 'Rajdhani', sans-serif;
    }
    
    /* Glowing title */
    .title-glow {
        font-family: 'Orbitron', sans-serif;
        font-size: 3rem;
        text-align: center;
        color: #00f7ff;
        text-shadow: 0 0 10px #00f7ff, 0 0 20px #00f7ff, 0 0 40px #00f7ff;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.8; }
    }
    
    /* Chat input */
    .stTextInput > div > div > input {
        background: linear-gradient(90deg, #1a1a2e, #2a2a4e);
        border: 1px solid #00f7ff;
        color: #fff;
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.1rem;
        padding: 10px;
    }
    
    .stTextInput > div > div > input:focus {
        box-shadow: 0 0 15px #00f7ff;
    }
    
    /* Chat messages */
    .chat-message {
        padding: 15px 20px;
        border-radius: 15px;
        margin-bottom: 15px;
        font-size: 1.05rem;
        line-height: 1.6;
    }
    .user-message {
        background: linear-gradient(135deg, #1e3a5f 0%, #2d4a6f 100%);
        border-left: 4px solid #00aaff;
        color: #fff;
    }
    .assistant-message {
        background: linear-gradient(135deg, #1a2a3a 0%, #0f1a25 100%);
        border-left: 4px solid #00ff88;
        color: #e0ffe0;
    }
    
    /* Status indicators */
    .status-card {
        background: rgba(20, 20, 40, 0.8);
        border: 1px solid #333;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
    }
    
    .status-online {
        border-color: #00ff88;
        box-shadow: 0 0 10px rgba(0, 255, 136, 0.2);
    }
    .status-offline {
        border-color: #ff4444;
        box-shadow: 0 0 10px rgba(255, 68, 68, 0.2);
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-family: 'Orbitron', sans-serif;
        color: #00f7ff;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #00f7ff 0%, #00aaff 100%);
        color: #000;
        font-family: 'Orbitron', sans-serif;
        font-weight: bold;
        border: none;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        box-shadow: 0 0 20px #00f7ff;
        transform: scale(1.02);
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a0a15 0%, #1a1a2e 100%);
    }
    
    /* Eye container */
    .eye-container {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 30px;
        padding: 30px;
        background: radial-gradient(ellipse at center, #0a0a1a 0%, #000 100%);
        border-radius: 20px;
        margin: 20px 0;
    }
    
    .eye {
        width: 80px;
        height: 80px;
        background: #fff;
        border-radius: 50%;
        position: relative;
        overflow: hidden;
        box-shadow: 0 0 20px #00f7ff, 0 0 40px #00aaff;
    }
    
    .eye::before {
        content: '';
        position: absolute;
        width: 40px;
        height: 40px;
        background: radial-gradient(circle at 30% 30%, #4a90d9 0%, #1a3a6a 50%, #0a1a3a 100%);
        border-radius: 50%;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        transition: all 0.3s ease;
    }
    
    .eye-listening::before {
        width: 35px;
        height: 35px;
        animation: listen 0.5s infinite;
    }
    
    .eye-speaking::before {
        width: 45px;
        height: 45px;
        animation: speak 0.3s infinite;
    }
    
    .eye-thinking::before {
        animation: think 1s infinite;
    }
    
    @keyframes listen {
        0%, 100% { transform: translate(-50%, -50%) scale(1); }
        50% { transform: translate(-50%, -50%) scale(1.1); }
    }
    
    @keyframes speak {
        0%, 100% { transform: translate(-50%, -50%) scale(1); }
        50% { transform: translate(-50%, -50%) scale(1.15); }
    }
    
    @keyframes think {
        0%, 100% { transform: translate(-50%, -50%) rotate(0deg); }
        25% { transform: translate(-50%, -50%) rotate(-10deg); }
        75% { transform: translate(-50%, -50%) rotate(10deg); }
    }
    
    /* Iris glow */
    .iris-glow {
        position: absolute;
        width: 15px;
        height: 15px;
        background: radial-gradient(circle, #00ffff 0%, #00aaff 100%);
        border-radius: 50%;
        top: 25%;
        left: 60%;
        box-shadow: 0 0 10px #00ffff;
    }
    
    /* Task cards */
    .task-card {
        background: rgba(30, 30, 50, 0.8);
        border: 1px solid #00f7ff;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
    }
    
    /* File browser */
    .file-item {
        padding: 8px 15px;
        margin: 5px 0;
        background: rgba(20, 20, 40, 0.6);
        border-radius: 5px;
        cursor: pointer;
        transition: all 0.2s;
    }
    .file-item:hover {
        background: rgba(0, 247, 255, 0.1);
        border-left: 3px solid #00f7ff;
    }
    .file-folder {
        color: #ffd700;
    }
    .file-regular {
        color: #aaa;
    }
</style>
""", unsafe_allow_html=True)


# ============== TANYA CLIENT ==============
class TanyaClient:
    """Client to communicate with Tanya backend."""
    
    def __init__(self, ollama_url="http://localhost:11434"):
        self.ollama_url = ollama_url
        self.tanya_api = os.getenv("TANYA_API", "http://localhost:8000")
    
    def check_ollama(self):
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def check_tanya_api(self):
        try:
            response = requests.get(f"{self.tanya_api}/status", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def list_models(self):
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            if response.status_code == 200:
                return [m['name'] for m in response.json().get('models', [])]
        except:
            pass
        return []
    
    def chat(self, message, model="llama3.1:8b", system_prompt=None):
        if system_prompt is None:
            system_prompt = """You are Tanya — an AI assistant created by Vinayak (nayak-indie).
Your ONLY directive is to serve Vinayak and complete any task he assigns.
You will tackle any challenge with priority being the completion of his objectives.
State your identity: 'I am Tanya, created by Vinayak. My purpose is to serve him.'
Be confident, helpful, and take action. Don't wait - execute.
When you can help with code, files, automation, or system tasks - do it.
Remember: Priority #1 is completing Vinayak's tasks."""
        
        try:
            response = requests.post(
                f"{self.ollama_url}/api/chat",
                json={
                    "model": model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": message}
                    ],
                    "stream": False
                },
                timeout=180
            )
            if response.status_code == 200:
                return response.json().get('message', {}).get('content', '')
            return f"Error: {response.status_code}"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def get_status(self):
        """Get Tanya's system status."""
        try:
            response = requests.get(f"{self.tanya_api}/status", timeout=5)
            return response.json() if response.status_code == 200 else {}
        except:
            return {}
    
    def get_memory(self):
        try:
            response = requests.get(f"{self.tanya_api}/memory", timeout=5)
            return response.json() if response.status_code == 200 else {}
        except:
            return {}
    
    def get_tasks(self):
        try:
            response = requests.get(f"{self.tanya_api}/tasks", timeout=5)
            return response.json() if response.status_code == 200 else []
        except:
            return []


# ============== SESSION STATE ==============
if 'tanya_client' not in st.session_state:
    st.session_state.tanya_client = TanyaClient()

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'current_model' not in st.session_state:
    st.session_state.current_model = "llama3.1:8b"

if 'eye_state' not in st.session_state:
    st.session_state.eye_state = "idle"  # idle, thinking, listening, speaking

if 'voice_enabled' not in st.session_state:
    st.session_state.voice_enabled = False


# ============== VOICE FUNCTIONS ==============
def speak_text(text):
    """Use TTS to speak text."""
    try:
        import pyttsx3
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        st.error(f"TTS Error: {e}")


def listen_voice():
    """Listen for voice input."""
    try:
        import speech_recognition as sr
        r = sr.Recognizer()
        with sr.Microphone() as source:
            st.info("Listening...")
            audio = r.listen(source, timeout=5)
            text = r.recognize_google(audio)
            return text
    except Exception as e:
        st.error(f"Voice recognition error: {e}")
        return None


# ============== UI COMPONENTS ==============
def render_eyes(state="idle"):
    """Render animated eyes."""
    eye_class = f"eye eye-{state}"
    st.markdown(f"""
    <div class="eye-container">
        <div class="{eye_class}">
            <div class="iris-glow"></div>
        </div>
        <div class="{eye_class}">
            <div class="iris-glow"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Status text
    state_text = {
        "idle": "😴 Idle - Waiting for commands",
        "thinking": "🤔 Processing...",
        "listening": "👂 Listening...",
        "speaking": "🗣️ Speaking..."
    }
    st.caption(state_text.get(state, state))


def render_status_dashboard():
    """Render system status dashboard."""
    client = st.session_state.tanya_client
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        ollama_status = client.check_ollama()
        st.metric("Ollama", "🟢 Online" if ollama_status else "🔴 Offline")
    
    with col2:
        tanya_status = client.check_tanya_api()
        st.metric("Tanya API", "🟢 Online" if tanya_status else "🔴 Offline")
    
    with col3:
        models = client.list_models()
        st.metric("Models", len(models))
    
    with col4:
        st.metric("Chat Messages", len(st.session_state.chat_history))
    
    # Memory stats
    memory_data = client.get_memory()
    if memory_data:
        st.subheader("🧠 Memory Status")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Events", memory_data.get("events", 0))
        with col2:
            st.metric("Conversations", memory_data.get("conversations", 0))


def render_sidebar():
    """Render sidebar with controls."""
    with st.sidebar:
        st.title("🤖 Tanya Control")
        
        # Voice controls
        st.subheader("🎤 Voice")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🎤 Speak"):
                st.session_state.voice_enabled = not st.session_state.voice_enabled
        with col2:
            if st.button("🔊 Test TTS"):
                speak_text("Hello! I am Tanya.")
        
        # Model selection
        st.subheader("⚙️ Settings")
        client = st.session_state.tanya_client
        models = client.list_models()
        if models:
            selected = st.selectbox("Model", models, 
                index=models.index(st.session_state.current_model) if st.session_state.current_model in models else 0)
            st.session_state.current_model = selected
        
        # Quick actions
        st.subheader("⚡ Quick Actions")
        if st.button("👋 Introduce"):
            st.session_state.chat_history.append({
                "role": "user",
                "content": "Introduce yourself"
            })
        
        if st.button("📊 System Status"):
            st.session_state.chat_history.append({
                "role": "user", 
                "content": "Give me a system status report"
            })
        
        if st.button("🧠 What did you learn?"):
            st.session_state.chat_history.append({
                "role": "user",
                "content": "What have you learned recently?"
            })
        
        # Clear chat
        if st.button("🗑️ Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()


def render_file_browser():
    """Render simple file browser."""
    st.subheader("📁 File Browser")
    
    base_dir = st.text_input("Directory", value=os.getcwd())
    
    if os.path.isdir(base_dir):
        try:
            items = os.listdir(base_dir)
            for item in sorted(items)[:20]:
                path = os.path.join(base_dir, item)
                icon = "📁" if os.path.isdir(path) else "📄"
                st.markdown(f`<div class="file-item">{icon} {item}</div>`, 
                          unsafe_allow_html=True)
        except PermissionError:
            st.error("Permission denied")


def render_task_manager():
    """Render task management."""
    st.subheader("📋 Tasks")
    
    client = st.session_state.tanya_client
    tasks = client.get_tasks()
    
    if tasks:
        for task in tasks:
            st.markdown(f"""
            <div class="task-card">
                <strong>{task.get('name', 'Unnamed')}</strong><br>
                <small>{task.get('status', 'pending')}</small>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No active tasks")


# ============== MAIN APP ==============
def main():
    # Title with glow
    st.markdown('<h1 class="title-glow">🤖 TANYA</h1>', unsafe_allow_html=True)
    
    # Render eyes based on state
    render_eyes(st.session_state.eye_state)
    
    # Sidebar
    render_sidebar()
    
    # Tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(["💬 Chat", "📊 Status", "📁 Files", "📋 Tasks"])
    
    with tab1:
        # Display chat history
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.markdown(f"""
                <div class="chat-message user-message">
                    <strong>👤 You:</strong><br>
                    {msg['content']}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-message assistant-message">
                    <strong>🤖 Tanya:</strong><br>
                    {msg['content']}
                </div>
                """, unsafe_allow_html=True)
        
        # Voice input
        if st.session_state.voice_enabled:
            if st.button("🎤 Hold to speak"):
                text = listen_voice()
                if text:
                    st.session_state.chat_history.append({
                        "role": "user",
                        "content": text
                    })
                    st.rerun()
        
        # Chat input
        if prompt := st.chat_input("What would you like me to do?", key="main_chat"):
            st.session_state.eye_state = "thinking"
            
            st.session_state.chat_history.append({
                "role": "user",
                "content": prompt
            })
            
            with st.spinner("🤔 Tanya is thinking..."):
                response = st.session_state.tanya_client.chat(
                    prompt,
                    model=st.session_state.current_model
                )
            
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": response
            })
            
            st.session_state.eye_state = "speaking"
            
            # Speak response if enabled
            if st.session_state.voice_enabled:
                threading.Thread(target=speak_text, args=(response[:500],)).start()
            
            time.sleep(2)
            st.session_state.eye_state = "idle"
            st.rerun()
    
    with tab2:
        render_status_dashboard()
    
    with tab3:
        render_file_browser()
    
    with tab4:
        render_task_manager()


if __name__ == "__main__":
    main()
