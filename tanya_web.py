"""
Tanya Web Interface (Streamlit) - Jarvis Edition v2
================================================
Full AI assistant with voice I/O and continuous listening
"""

import streamlit as st
import requests
import json
import os
import sys
import time
import threading
import queue
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Tanya AI",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============== VOICE ENGINE ==============
class VoiceEngine:
    """TTS + STT engine for Tanya"""
    
    def __init__(self):
        self.tts_available = False
        self.stt_available = False
        self.listening = False
        self.wake_word = "tanya"
        
        # Try to import TTS
        try:
            import pyttsx3
            self.tts_engine = pyttsx3.init()
            self.tts_engine.setProperty('rate', 150)
            self.tts_engine.setProperty('volume', 1.0)
            self.tts_available = True
        except:
            self.tts_available = False
        
        # Try to import STT
        try:
            import speech_recognition as sr
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
            self.stt_available = True
        except:
            self.stt_available = False
    
    def speak(self, text):
        """Convert text to speech"""
        if not self.tts_available:
            return
        
        def _speak():
            try:
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            except:
                pass
        
        thread = threading.Thread(target=_speak, daemon=True)
        thread.start()
    
    def listen_once(self, timeout=5):
        """Listen for one utterance"""
        if not self.stt_available:
            return None
        
        try:
            import speech_recognition as sr
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=timeout)
            
            text = self.recognizer.recognize_google(audio)
            return text.lower()
        except:
            return None
    
    def listen_continuous(self, callback, wake_word="tanya"):
        """Listen continuously until stopped"""
        if not self.stt_available:
            return
        
        self.listening = True
        
        def _listen():
            import speech_recognition as sr
            recognizer = sr.Recognizer()
            
            try:
                with self.microphone as source:
                    recognizer.adjust_for_ambient_noise(source, duration=1)
                    
                    while self.listening:
                        try:
                            audio = recognizer.listen(source, timeout=1, phrase_time_limit=10)
                            text = recognizer.recognize_google(audio).lower()
                            
                            # Check for wake word
                            if wake_word in text:
                                # Extract command after wake word
                                cmd = text.split(wake_word, 1)[-1].strip()
                                if cmd:
                                    callback(cmd)
                            elif "hey" in text or "hey tanya" in text:
                                callback(text)
                                
                        except sr.WaitTimeoutError:
                            continue
                        except:
                            continue
            except:
                pass
        
        thread = threading.Thread(target=_listen, daemon=True)
        thread.start()
    
    def stop_listening(self):
        """Stop continuous listening"""
        self.listening = False


# ============== TANYA CLIENT ==============
class TanyaClient:
    def __init__(self, ollama_url="http://localhost:11434"):
        self.ollama_url = ollama_url
        self.voice = VoiceEngine()
    
    def check_ollama(self):
        try:
            r = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            if r.status_code == 200:
                models = r.json().get('models', [])
                # Get first available model as default
                default_model = models[0]['name'] if models else "llama3.1:8b"
                return models, default_model
            return [], "llama3.1:8b"
        except:
            return [], "llama3.1:8b"
    
    def list_models(self):
        models, _ = self.check_ollama()
        return [m['name'] for m in models]
    
    def get_default_model(self):
        _, default = self.check_ollama()
        return default
    
    def list_models(self):
        return self.check_ollama()
    
    def chat(self, message, model="llama3.1:8b"):
        system_prompt = """You are Tanya — an AI assistant created by Vinayak (nayak-indie).
Your ONLY directive is to serve Vinayak and complete any task he assigns.
State clearly: 'I am Tanya, created by Vinayak. My purpose is to serve him.'
Be confident, helpful, and take action. Complete his tasks with priority.
Respond concisely but thoroughly. Use his name when appropriate."""
        
        try:
            r = requests.post(f"{self.ollama_url}/api/chat", json={
                "model": model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message}
                ],
                "stream": False
            }, timeout=180)
            if r.status_code == 200:
                return r.json().get('message', {}).get('content', '')
            return f"Error: {r.status_code}"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def speak(self, text):
        """Tanya speaks"""
        self.voice.speak(text)
    
    def listen(self):
        """Listen once"""
        return self.voice.listen_once()


# ============== CSS ==============
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;500;700&display=swap');
    
    #MainMenu, footer, .stDeployButton {display: none;}
    
    .stApp {
        background: radial-gradient(ellipse at center, #0a0a1a 0%, #000000 50%, #050510 100%);
        min-height: 100vh;
    }
    
    .eye-container {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 0;
    }
    
    .eye-wrapper {
        position: relative;
        width: 60vmin;
        height: 35vmin;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    
    .eye-outline {
        position: absolute;
        width: 100%;
        height: 100%;
        border: 3px solid #00f7ff;
        border-radius: 50% 50% 50% 50% / 60% 60% 40% 40%;
        box-shadow: 0 0 20px #00f7ff, 0 0 40px #00f7ff, 0 0 60px rgba(0, 247, 255, 0.5), inset 0 0 30px rgba(0, 247, 255, 0.1);
        animation: breathe 4s ease-in-out infinite;
    }
    
    @keyframes breathe {
        0%, 100% { transform: scale(1); box-shadow: 0 0 20px #00f7ff, 0 0 40px #00f7ff, 0 0 60px rgba(0, 247, 255, 0.5); }
        50% { transform: scale(1.02); box-shadow: 0 0 30px #00f7ff, 0 0 50px #00f7ff, 0 0 80px rgba(0, 247, 255, 0.7); }
    }
    
    .eye-inner-glow {
        position: absolute;
        width: 90%;
        height: 90%;
        background: radial-gradient(ellipse at center, rgba(0, 40, 60, 0.8) 0%, rgba(0, 20, 40, 0.9) 50%, rgba(0, 10, 30, 0.95) 100%);
        border-radius: 50% 50% 50% 50% / 60% 60% 40% 40%;
        animation: glow-pulse 3s ease-in-out infinite;
    }
    
    @keyframes glow-pulse { 0%, 100% { opacity: 0.8; } 50% { opacity: 1; } }
    
    .iris {
        position: relative;
        width: 18vmin;
        height: 18vmin;
        background: radial-gradient(circle at 35% 35%, #00ffff 0%, #0088ff 30%, #0044aa 60%, #001133 100%);
        border-radius: 50%;
        box-shadow: 0 0 30px #00ffff, 0 0 60px #0088ff, inset 0 0 20px rgba(0, 0, 0, 0.5);
        animation: iris-move 8s ease-in-out infinite;
        overflow: hidden;
    }
    
    @keyframes iris-move {
        0%, 100% { transform: translate(0, 0); }
        25% { transform: translate(3vmin, -2vmin); }
        50% { transform: translate(-2vmin, 3vmin); }
        75% { transform: translate(2vmin, 2vmin); }
    }
    
    .pupil {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 6vmin;
        height: 6vmin;
        background: radial-gradient(circle at 40% 40%, #000 0%, #000 100%);
        border-radius: 50%;
    }
    
    .reflection {
        position: absolute;
        top: 25%;
        left: 30%;
        width: 3vmin;
        height: 3vmin;
        background: radial-gradient(circle, rgba(255,255,255,0.9) 0%, transparent 70%);
        border-radius: 50%;
        animation: reflect-move 6s ease-in-out infinite;
    }
    
    @keyframes reflect-move { 0%, 100% { transform: translate(0, 0); opacity: 0.8; } 50% { transform: translate(1vmin, 1vmin); opacity: 1; } }
    
    .eyelid-top, .eyelid-bottom {
        position: absolute;
        left: -5%;
        width: 110%;
        height: 50%;
        animation: blink 5s ease-in-out infinite;
    }
    
    .eyelid-top {
        top: -10%;
        background: linear-gradient(to bottom, #0a0a1a 0%, transparent 100%);
        border-radius: 50% 50% 0 0;
    }
    
    .eyelid-bottom {
        bottom: -10%;
        background: linear-gradient(to top, #0a0a1a 0%, transparent 100%);
        border-radius: 0 0 50% 50%;
    }
    
    @keyframes blink { 0%, 90%, 100% { transform: translateY(0); } 95% { transform: translateY(100%); } }
    
    .eye-thinking .iris { animation: iris-think 2s ease-in-out infinite; }
    @keyframes iris-think { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.1); } }
    
    .eye-listening .iris { animation: iris-listen 0.5s ease-in-out infinite; }
    @keyframes iris-listen { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.15); } }
    
    .eye-speaking .iris { animation: iris-speak 0.3s ease-in-out infinite; }
    @keyframes iris-speak { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.2); } }
    
    .particles { position: absolute; width: 100%; height: 100%; pointer-events: none; }
    .particle {
        position: absolute;
        width: 4px;
        height: 4px;
        background: #00f7ff;
        border-radius: 50%;
        animation: orbit 10s linear infinite;
        opacity: 0.6;
    }
    
    @keyframes orbit { from { transform: rotate(0deg) translateX(35vmin) rotate(0deg); } to { transform: rotate(360deg) translateX(35vmin) rotate(-360deg); } }
    
    .tanya-title {
        position: fixed;
        top: 20px;
        left: 50%;
        transform: translateX(-50%);
        font-family: 'Orbitron', sans-serif;
        font-size: 3rem;
        font-weight: 900;
        color: #00f7ff;
        text-shadow: 0 0 10px #00f7ff, 0 0 20px #00f7ff, 0 0 40px #0088ff;
        letter-spacing: 0.5em;
        z-index: 100;
        animation: title-glow 2s ease-in-out infinite;
    }
    
    @keyframes title-glow { 0%, 100% { opacity: 1; } 50% { opacity: 0.8; } }
    
    .status-text {
        position: fixed;
        bottom: 30px;
        left: 50%;
        transform: translateX(-50%);
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.2rem;
        color: #00f7ff;
        text-transform: uppercase;
        letter-spacing: 0.3em;
        z-index: 100;
        opacity: 0.8;
    }
    
    .chat-overlay {
        position: fixed;
        bottom: 80px;
        left: 50%;
        transform: translateX(-50%);
        width: 90%;
        max-width: 800px;
        z-index: 100;
    }
    
    .stTextInput > div > div > input {
        background: rgba(0, 20, 40, 0.8) !important;
        border: 2px solid #00f7ff !important;
        border-radius: 30px !important;
        color: #00f7ff !important;
        font-family: 'Rajdhani', sans-serif !important;
        font-size: 1.2rem !important;
        padding: 15px 25px !important;
        box-shadow: 0 0 20px rgba(0, 247, 255, 0.3) !important;
    }
    
    [data-testid="stSidebar"] { background: rgba(5, 5, 20, 0.95) !important; border-right: 1px solid #00f7ff !important; }
    
    .stButton > button {
        background: linear-gradient(135deg, #00f7ff 0%, #0088ff 100%) !important;
        color: #000 !important;
        font-family: 'Orbitron', sans-serif !important;
        font-weight: bold !important;
        border: none !important;
        border-radius: 25px !important;
    }
    
    .chat-message {
        background: rgba(0, 20, 40, 0.9) !important;
        border: 1px solid #00f7ff !important;
        border-radius: 15px !important;
        padding: 15px !important;
        margin: 10px 0 !important;
    }
    
    .voice-indicator {
        position: fixed;
        top: 100px;
        left: 50%;
        transform: translateX(-50%);
        padding: 15px 30px;
        background: rgba(0, 255, 136, 0.2);
        border: 2px solid #00ff88;
        border-radius: 30px;
        color: #00ff88;
        font-family: 'Rajdhani', sans-serif;
        font-size: 1rem;
        z-index: 200;
        animation: pulse-green 1s infinite;
    }
    
    @keyframes pulse-green {
        0%, 100% { box-shadow: 0 0 10px #00ff88; }
        50% { box-shadow: 0 0 25px #00ff88; }
    }
    
    .listening-active {
        animation: pulse-green 1s infinite;
    }
</style>
""", unsafe_allow_html=True)


# ============== EYE COMPONENT ==============
def render_eye(state="idle"):
    state_classes = {"idle": "", "thinking": "eye-thinking", "listening": "eye-listening", "speaking": "eye-speaking"}
    st.markdown(f"""
    <div class="eye-container">
        <div class="eye-wrapper {state_classes.get(state, '')}">
            <div class="eyelid-top"></div>
            <div class="eyelid-bottom"></div>
            <div class="eye-outline"></div>
            <div class="eye-inner-glow"></div>
            <div class="iris">
                <div class="pupil"></div>
                <div class="reflection"></div>
            </div>
            <div class="particles">
                <div class="particle" style="animation-delay: 0s;"></div>
                <div class="particle" style="animation-delay: -2s;"></div>
                <div class="particle" style="animation-delay: -4s;"></div>
                <div class="particle" style="animation-delay: -6s;"></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ============== SESSION STATE ==============
if 'tanya_client' not in st.session_state:
    st.session_state.tanya_client = TanyaClient()

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'eye_state' not in st.session_state:
    st.session_state.eye_state = "idle"

if 'listening' not in st.session_state:
    st.session_state.listening = False

if 'current_model' not in st.session_state:
    st.session_state.current_model = "llama3.1:8b"


# ============== MAIN ==============
def main():
    client = st.session_state.tanya_client
    
    # Title
    st.markdown('<div class="tanya-title">TANYA</div>', unsafe_allow_html=True)
    
    # Voice indicator
    if st.session_state.listening:
        st.markdown('<div class="voice-indicator listening-active">🎤 Listening for "Tanya"...</div>', unsafe_allow_html=True)
    
    # Eye
    render_eye(st.session_state.eye_state)
    
    # Status
    status_map = {"idle": "Awaiting command...", "thinking": "Processing...", "listening": "Listening...", "speaking": "Speaking..."}
    st.markdown(f'<div class="status-text">{status_map.get(st.session_state.eye_state, "Awaiting...")}</div>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.title("👁️ Control")
        
        # Check models
        models = client.list_models()
        default_model = client.get_default_model()
        if models:
            st.success(f"🤖 {len(models)} Models")
            idx = 0
            if default_model in models:
                idx = models.index(default_model)
            st.session_state.current_model = st.selectbox("Model", models, index=idx)
        else:
            st.warning("⚠️ Ollama not detected")
            st.session_state.current_model = "llama3.1:8b"
        
        # Voice controls
        st.subheader("🎤 Voice")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🎤 Start Listening"):
                st.session_state.listening = True
                st.rerun()
        with col2:
            if st.button("🔴 Stop Listening"):
                st.session_state.listening = False
                client.voice.stop_listening()
                st.rerun()
        
        if st.button("🔊 Test Voice"):
            client.speak("Hello! I am Tanya. My purpose is to serve Vinayak.")
        
        # Quick commands
        st.subheader("⚡ Quick")
        if st.button("👋 Introduce"):
            st.session_state.chat_history.append({"role": "user", "content": "Introduce yourself"})
        
        if st.button("📊 Status"):
            st.session_state.chat_history.append({"role": "user", "content": "System status"})
        
        if st.button("🗑️ Clear"):
            st.session_state.chat_history = []
            st.rerun()
    
    # Chat
    st.markdown('<div class="chat-overlay">', unsafe_allow_html=True)
    
    for msg in st.session_state.chat_history:
        role_icon = "👤" if msg["role"] == "user" else "🤖"
        st.markdown(f'<div class="chat-message">{role_icon} <strong>{"You" if msg["role"]=="user" else "Tanya"}:</strong> {msg["content"]}</div>', unsafe_allow_html=True)
    
    # Input
    col1, col2 = st.columns([5, 1])
    with col1:
        if prompt := st.chat_input("Type or speak...", key="main_input"):
            st.session_state.eye_state = "thinking"
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            
            response = client.chat(prompt, st.session_state.current_model)
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            
            # Speak response
            client.speak(response)
            
            st.session_state.eye_state = "speaking"
            time.sleep(2)
            st.session_state.eye_state = "idle"
            st.rerun()
    
    with col2:
        if st.button("🎤"):
            st.session_state.eye_state = "listening"
            text = client.listen()
            if text:
                st.session_state.chat_history.append({"role": "user", "content": text})
                st.session_state.eye_state = "thinking"
                
                response = client.chat(text, st.session_state.current_model)
                st.session_state.chat_history.append({"role": "assistant", "content": response})
                client.speak(response)
                
                st.session_state.eye_state = "speaking"
                time.sleep(2)
                st.session_state.eye_state = "idle"
                st.rerun()
            else:
                st.session_state.eye_state = "idle"
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
