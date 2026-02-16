"""
Tanya Web Interface (Streamlit) - Jarvis Edition v3
================================================
Kafka-style grotesque minimal eye - sharp, dark, unsettling
"""

import streamlit as st
import requests
import json
import os
import sys
import time
import threading
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
    def __init__(self):
        self.tts_available = False
        self.stt_available = False
        self.listening = False
        
        try:
            import pyttsx3
            self.tts_engine = pyttsx3.init()
            self.tts_engine.setProperty('rate', 150)
            self.tts_engine.setProperty('volume', 1.0)
            self.tts_available = True
        except:
            pass
        
        try:
            import speech_recognition as sr
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
            self.stt_available = True
        except:
            pass
    
    def speak(self, text):
        if not self.tts_available:
            return
        def _speak():
            try:
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            except:
                pass
        threading.Thread(target=_speak, daemon=True).start()
    
    def listen_once(self, timeout=5):
        if not self.stt_available:
            return None
        try:
            import speech_recognition as sr
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=timeout)
            return self.recognizer.recognize_google(audio).lower()
        except:
            return None


# ============== TANYA CLIENT ==============
class TanyaClient:
    def __init__(self, ollama_url="http://localhost:11434"):
        self.ollama_url = ollama_url
        self.voice = VoiceEngine()
    
    def check_owlama(self):
        try:
            r = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            if r.status_code == 200:
                models = r.json().get('models', [])
                default = models[0]['name'] if models else "llama3.1:8b"
                return models, default
            return [], "llama3.1:8b"
        except:
            return [], "llama3.1:8b"
    
    def list_models(self):
        models, _ = self.check_owlama()
        return [m['name'] for m in models]
    
    def get_default_model(self):
        _, default = self.check_owlama()
        return default
    
    def chat(self, message, model="llama3.1:8b"):
        system_prompt = """You are Tanya — an AI assistant created by Vinayak (nayak-indie).
Your ONLY directive is to serve Vinayak and complete any task he assigns.
State clearly: 'I am Tanya, created by Vinayak. My purpose is to serve him.'
Be confident, helpful. Complete his tasks with priority."""
        
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
        self.voice.speak(text)
    
    def listen(self):
        return self.voice.listen_once()


# ============== KAFKA EYE CSS ==============
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,700;1,400&family=Spectral:wght@200;400;600&display=swap');
    
    #MainMenu, footer, .stDeployButton {display: none;}
    
    .stApp {
        background: #0a0a0a;
        background-image: 
            radial-gradient(ellipse at 30% 20%, rgba(20, 20, 20, 1) 0%, transparent 50%),
            radial-gradient(ellipse at 70% 80%, rgba(15, 15, 15, 1) 0%, transparent 50%),
            linear-gradient(180deg, #050505 0%, #0a0a0a 50%, #030303 100%);
        min-height: 100vh;
    }
    
    /* Kafka's eye - grotesque, sharp, unsettling */
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
        width: 70vmin;
        height: 40vmin;
        animation: kafka-tremor 4s ease-in-out infinite;
    }
    
    @keyframes kafka-tremor {
        0%, 100% { transform: translate(0, 0) rotate(-0.5deg); }
        25% { transform: translate(-1px, 1px) rotate(0.5deg); }
        50% { transform: translate(1px, -0.5px) rotate(-0.3deg); }
        75% { transform: translate(-0.5px, -1px) rotate(0.3deg); }
    }
    
    /* Sharp angular outline - Kafka style */
    .eye-outline {
        position: absolute;
        width: 100%;
        height: 100%;
        background: transparent;
        /* Sharp angular shape */
        clip-path: polygon(
            5% 20%, 15% 5%, 40% 0%, 60% 2%, 85% 8%, 95% 25%, 
            100% 50%, 97% 75%, 90% 95%, 70% 100%, 30% 98%, 5% 90%, 0% 70%, 3% 45%
        );
        border: 3px solid #1a1a1a;
        box-shadow: 
            inset 0 0 60px rgba(0, 0, 0, 0.9),
            inset 0 0 30px rgba(10, 10, 10, 0.8);
    }
    
    /* Multiple intersecting lines - Kafka's cage */
    .kafka-lines {
        position: absolute;
        width: 100%;
        height: 100%;
        pointer-events: none;
    }
    
    .kafka-lines::before,
    .kafka-lines::after {
        content: '';
        position: absolute;
        background: rgba(30, 30, 30, 0.8);
    }
    
    /* Cross hatching */
    .kafka-lines::before {
        width: 150%;
        height: 1px;
        top: 50%;
        left: -25%;
        transform: rotate(-15deg);
        box-shadow: 
            0 10vmin 0 rgba(30, 30, 30, 0.6),
            0 -8vmin 0 rgba(30, 30, 30, 0.6),
            0 20vmin 0 rgba(30, 30, 30, 0.4);
    }
    
    .kafka-lines::after {
        width: 150%;
        height: 1px;
        top: 50%;
        left: -25%;
        transform: rotate(12deg);
        box-shadow: 
            0 12vmin 0 rgba(30, 30, 30, 0.5),
            0 -15vmin 0 rgba(30, 30, 30, 0.5);
    }
    
    /* Dark inner void */
    .eye-void {
        position: absolute;
        width: 85%;
        height: 85%;
        top: 7.5%;
        left: 7.5%;
        background: radial-gradient(ellipse at 45% 45%, 
            #000000 0%, 
            #080808 30%, 
            #0c0c0c 60%, 
            #111111 100%);
        clip-path: polygon(
            8% 25%, 20% 10%, 45% 5%, 65% 8%, 88% 18%, 
            95% 40%, 90% 65%, 85% 90%, 60% 97%, 35% 95%, 10% 85%, 5% 55%
        );
    }
    
    /* The iris - unsettling void */
    .iris {
        position: absolute;
        width: 22vmin;
        height: 22vmin;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: radial-gradient(circle at 40% 40%, 
            #0a0a0a 0%, 
            #050505 40%, 
            #000000 70%, 
            #000000 100%);
        border-radius: 50%;
        box-shadow: 
            inset 0 0 20px #000,
            inset 0 0 40px #000,
            0 0 1px #111;
        animation: void-pulse 6s ease-in-out infinite;
    }
    
    @keyframes void-pulse {
        0%, 100% { transform: translate(-50%, -50%) scale(1); opacity: 0.9; }
        50% { transform: translate(-50%, -50%) scale(1.05); opacity: 1; }
    }
    
    /* Pupil - the abyss */
    .pupil {
        position: absolute;
        width: 8vmin;
        height: 8vmin;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: #000;
        border-radius: 50%;
        box-shadow: 
            inset 0 0 10px #000,
            0 0 5px #000;
    }
    
    /* Veins - Kafka's decay */
    .veins {
        position: absolute;
        width: 100%;
        height: 100%;
        opacity: 0.3;
        pointer-events: none;
    }
    
    .vein {
        position: absolute;
        background: #1a1a1a;
        transform-origin: center;
    }
    
    .vein-1 { width: 120%; height: 1px; top: 30%; left: -10%; transform: rotate(-8deg); }
    .vein-2 { width: 110%; height: 1px; top: 60%; left: -5%; transform: rotate(5deg); }
    .vein-3 { width: 80%; height: 1px; top: 45%; left: 10%; transform: rotate(-3deg); }
    
    /* Creeping shadows */
    .shadow-creep {
        position: absolute;
        width: 30%;
        height: 40%;
        background: radial-gradient(ellipse at center, rgba(0,0,0,0.8) 0%, transparent 70%);
        animation: creep 8s ease-in-out infinite;
    }
    
    .shadow-1 { top: -10%; right: -5%; animation-delay: 0s; }
    .shadow-2 { bottom: -15%; left: -10%; animation-delay: -3s; }
    
    @keyframes creep {
        0%, 100% { opacity: 0.3; transform: scale(1); }
        50% { opacity: 0.6; transform: scale(1.1); }
    }
    
    /* State effects */
    .eye-thinking .iris {
        animation: void-think 1.5s ease-in-out infinite;
    }
    
    @keyframes void-think {
        0%, 100% { transform: translate(-50%, -50%) scale(1); }
        50% { transform: translate(-50%, -50%) scale(0.9); }
    }
    
    .eye-listening .iris {
        animation: void-listen 0.4s ease-in-out infinite;
    }
    
    @keyframes void-listen {
        0%, 100% { transform: translate(-50%, -50%) scale(1); }
        50% { transform: translate(-50%, -50%) scale(1.1); }
    }
    
    .eye-speaking .iris {
        animation: void-speak 0.25s ease-in-out infinite;
    }
    
    @keyframes void-speak {
        0%, 100% { transform: translate(-50%, -50%) scale(1); }
        50% { transform: translate(-50%, -50%) scale(1.15); }
    }
    
    /* Title - Kafka style */
    .tanya-title {
        position: fixed;
        top: 25px;
        left: 50%;
        transform: translateX(-50%);
        font-family: 'EB Garamond', serif;
        font-size: 2.5rem;
        font-weight: 400;
        font-style: italic;
        color: #2a2a2a;
        letter-spacing: 0.8em;
        z-index: 100;
        text-shadow: 0 0 1px #1a1a1a;
    }
    
    /* Status */
    .status-text {
        position: fixed;
        bottom: 25px;
        left: 50%;
        transform: translateX(-50%);
        font-family: 'Spectral', serif;
        font-size: 0.9rem;
        font-weight: 200;
        color: #333;
        font-style: italic;
        letter-spacing: 0.4em;
        z-index: 100;
    }
    
    /* Chat */
    .chat-overlay {
        position: fixed;
        bottom: 70px;
        left: 50%;
        transform: translateX(-50%);
        width: 90%;
        max-width: 700px;
        z-index: 100;
    }
    
    .stTextInput > div > div > input {
        background: rgba(5, 5, 5, 0.9) !important;
        border: 1px solid #222 !important;
        border-radius: 2px !important;
        color: #333 !important;
        font-family: 'Spectral', serif !important;
        font-size: 1rem !important;
        padding: 12px 20px !important;
    }
    
    [data-testid="stSidebar"] {
        background: #080808 !important;
        border-right: 1px solid #1a1a1a !important;
    }
    
    .stButton > button {
        background: #0a0a0a !important;
        color: #333 !important;
        font-family: 'Spectral', serif !important;
        border: 1px solid #222 !important;
        border-radius: 0 !important;
        font-size: 0.8rem !important;
        letter-spacing: 0.2em !important;
    }
    
    .stButton > button:hover {
        background: #111 !important;
        border-color: #333 !important;
    }
    
    .chat-message {
        background: rgba(8, 8, 8, 0.9) !important;
        border-left: 2px solid #222 !important;
        padding: 12px 15px !important;
        margin: 8px 0 !important;
        font-family: 'Spectral', serif !important;
        font-size: 0.95rem !important;
        color: #444 !important;
    }
    
    .voice-indicator {
        position: fixed;
        top: 100px;
        left: 50%;
        transform: translateX(-50%);
        padding: 10px 25px;
        background: #0a0a0a;
        border: 1px solid #222;
        color: #444;
        font-family: 'Spectral', serif;
        font-size: 0.8rem;
        font-style: italic;
        letter-spacing: 0.3em;
        z-index: 200;
    }
</style>
""", unsafe_allow_html=True)


# ============== EYE ==============
def render_kafka_eye(state="idle"):
    state_class = {"idle": "", "thinking": "eye-thinking", "listening": "eye-listening", "speaking": "eye-speaking"}.get(state, "")
    
    st.markdown(f"""
    <div class="eye-container">
        <div class="eye-wrapper {state_class}">
            <div class="shadow-creep shadow-1"></div>
            <div class="shadow-creep shadow-2"></div>
            <div class="eye-outline">
                <div class="kafka-lines">
                    <div class="vein vein-1"></div>
                    <div class="vein vein-2"></div>
                    <div class="vein vein-3"></div>
                </div>
            </div>
            <div class="eye-void"></div>
            <div class="iris">
                <div class="pupil"></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ============== SESSION ==============
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
    
    st.markdown('<div class="tanya-title">tanya</div>', unsafe_allow_html=True)
    
    if st.session_state.listening:
        st.markdown('<div class="voice-indicator">listening...</div>', unsafe_allow_html=True)
    
    render_kafka_eye(st.session_state.eye_state)
    
    status_map = {"idle": "awaiting...", "thinking": "processing...", "listening": "hearing...", "speaking": "speaking..."}
    st.markdown(f'<div class="status-text">{status_map.get(st.session_state.eye_state, "...")}</div>', unsafe_allow_html=True)
    
    with st.sidebar:
        st.markdown('<div style="font-family: EB Garamond; font-size: 1.5rem; color: #2a2a2a; font-style: italic;">tanya</div>', unsafe_allow_html=True)
        
        models = client.list_models()
        default_model = client.get_default_model()
        if models:
            st.markdown(f'<div style="color: #333; font-size: 0.8rem;">{len(models)} models</div>', unsafe_allow_html=True)
            idx = models.index(default_model) if default_model in models else 0
            st.session_state.current_model = st.selectbox("model", models, index=idx)
        else:
            st.markdown('<div style="color: #333;">ollama not detected</div>', unsafe_allow_html=True)
        
        st.markdown('<hr style="border-color: #1a1a1a;">', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("listen"):
                st.session_state.listening = True
                st.rerun()
        with col2:
            if st.button("stop"):
                st.session_state.listening = False
                st.rerun()
        
        if st.button("speak"):
            client.speak("I am Tanya. I serve Vinayak.")
        
        st.markdown('<hr style="border-color: #1a1a1a;">', unsafe_allow_html=True)
        
        if st.button("introduce"):
            st.session_state.chat_history.append({"role": "user", "content": "Introduce yourself"})
        
        if st.button("clear"):
            st.session_state.chat_history = []
            st.rerun()
    
    st.markdown('<div class="chat-overlay">', unsafe_allow_html=True)
    
    for msg in st.session_state.chat_history:
        role = "you" if msg["role"] == "user" else "tanya"
        st.markdown(f'<div class="chat-message"><strong>{role}:</strong> {msg["content"]}</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([5, 1])
    with col1:
        if prompt := st.chat_input("command...", key="main_input"):
            st.session_state.eye_state = "thinking"
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            
            response = client.chat(prompt, st.session_state.current_model)
            st.session_state.chat_history.append({"role": "assistant", "content": response})
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
    
    st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
