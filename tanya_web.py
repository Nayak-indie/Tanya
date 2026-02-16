"""
Tanya AI - Kafka Edition v3
============================
Continuous voice, grotesque eye, auto-listen
"""

import streamlit as st
import requests
import time
import threading
import random

st.set_page_config(page_title="Tanya AI", page_icon="👁️", layout="wide")


# ============== VOICE ==============
class VoiceEngine:
    def __init__(self):
        self.tts_ok = False
        self.stt_ok = False
        self.listening = False
        
        # TTS
        try:
            import pyttsx3
            self.tts = pyttsx3.init()
            self.tts.setProperty('rate', 150)
            self.tts.setProperty('volume', 1.0)
            self.tts_ok = True
        except:
            pass
        
        # STT
        try:
            import speech_recognition as sr
            self.rec = sr.Recognizer()
            self.mic = sr.Microphone()
            self.stt_ok = True
        except:
            pass
    
    def speak(self, text):
        if not self.tts_ok:
            return
        def _speak():
            try:
                self.tts.say(text)
                self.tts.runAndWait()
            except:
                pass
        threading.Thread(target=_speak, daemon=True).start()
    
    def listen_loop(self, callback):
        if not self.stt_ok:
            return
        
        self.listening = True
        
        def _listen():
            import speech_recognition as sr
            rec = sr.Recognizer()
            with self.mic as src:
                rec.adjust_for_ambient_noise(src, duration=0.8)
                
                while self.listening:
                    try:
                        audio = rec.listen(src, timeout=1, phrase_time_limit=15)
                        text = rec.recognize_google(audio)
                        if text and len(text.strip()) > 1:
                            callback(text.strip())
                    except:
                        continue
        
        threading.Thread(target=_listen, daemon=True).start()
    
    def stop(self):
        self.listening = False


# ============== CLIENT ==============
class TanyaClient:
    def __init__(self, url="http://localhost:11434"):
        self.url = url
        self.voice = VoiceEngine()
        self.voice_running = False
    
    def get_models(self):
        try:
            r = requests.get(f"{self.url}/api/tags", timeout=5)
            return [m['name'] for m in r.json().get('models', [])] if r.status_code==200 else []
        except: return []
    
    def chat(self, msg, model):
        sys_prompt = """You are Tanya, created by Vinayak. Your purpose is to serve Vinayak. State: "I am Tanya. I serve Vinayak." Be direct and helpful."""
        
        try:
            r = requests.post(f"{self.url}/api/chat", json={
                "model": model,
                "messages": [{"role": "system", "content": sys_prompt}, {"role": "user", "content": msg}],
                "stream": False
            }, timeout=180)
            return r.json().get('message',{}).get('content','') if r.status_code==200 else f"Error {r.status_code}"
        except Exception as e: return f"Error: {e}"


# ============== KAFKA EYE CSS ==============
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;1,400&family=Metal+Mania&display=swap');
    
    #MainMenu, footer, .stDeployButton {display: none !important;}
    
    .stApp {
        background: #000 !important;
        min-height: 100vh;
    }
    
    /* Massive grotesque eye */
    .eye-wrapper {
        position: fixed;
        top: 50%; left: 50%;
        transform: translate(-50%, -50%);
        width: 90vmin; height: 90vmin;
        z-index: 0;
    }
    
    /* Wounded socket */
    .socket {
        position: absolute;
        width: 100%; height: 100%;
        clip-path: polygon(
            5% 20%, 15% 5%, 35% 0%, 50% 3%, 65% 0%, 85% 8%, 95% 25%,
            100% 50%, 98% 75%, 90% 95%, 70% 100%, 30% 98%, 10% 90%, 2% 70%, 0% 45%
        );
        background: linear-gradient(180deg, #080808 0%, #0c0c0c 50%, #050505 100%);
        border: 1px solid #111;
    }
    
    /* Fractured bone lines */
    .fracture {
        position: absolute;
        background: #0a0a0a;
    }
    .f-1 { width: 120%; height: 1px; top: 25%; left: -10%; transform: rotate(-8deg); }
    .f-2 { width: 110%; height: 1px; top: 50%; left: -5%; transform: rotate(2deg); }
    .f-3 { width: 115%; height: 1px; top: 75%; left: -8%; transform: rotate(6deg); }
    .f-v { width: 1px; height: 90%; top: 5%; left: 48%; transform: rotate(-1deg); }
    
    /* Deep wound */
    .wound {
        position: absolute;
        width: 75%; height: 75%;
        top: 12.5%; left: 12.5%;
        background: radial-gradient(ellipse at 50% 50%,
            #000 0%,
            #050505 30%,
            #080808 60%,
            #0a0a0a 100%);
        clip-path: polygon(
            8% 22%, 18% 10%, 38% 5%, 55% 8%, 72% 12%, 88% 22%,
            92% 45%, 88% 68%, 78% 85%, 55% 92%, 32% 86%, 12% 70%, 6% 48%
        );
    }
    
    /* Rotting iris */
    .iris {
        position: absolute;
        width: 40%; height: 40%;
        top: 30%; left: 30%;
        background: radial-gradient(circle at 35% 35%,
            #1a0505 0%,
            #2a0808 25%,
            #3a0a0a 50%,
            #1a0000 75%,
            #000 100%);
        border-radius: 45% 50% 45% 50%;
        box-shadow: inset 0 0 20px #000;
        animation: rot-drift 8s ease-in-out infinite;
    }
    
    @keyframes rot-drift {
        0%, 100% { transform: translate(0,0) rotate(0deg); }
        25% { transform: translate(2%, -1%) rotate(2deg); }
        50% { transform: translate(-1%, 2%) rotate(-1deg); }
        75% { transform: translate(1%, 1%) rotate(1deg); }
    }
    
    /* Empty socket */
    .pupil {
        position: absolute;
        width: 25%; height: 25%;
        top: 37.5%; left: 37.5%;
        background: #000;
        border-radius: 50%;
        box-shadow: inset 0 0 15px #000;
    }
    
    /* Bruises */
    .bruise {
        position: absolute;
        border-radius: 50%;
        filter: blur(20px);
    }
    .bruise-1 { width: 30%; height: 20%; top: -5%; right: 10%; background: rgba(20,0,0,0.3); }
    .bruise-2 { width: 25%; height: 18%; bottom: -3%; left: 15%; background: rgba(15,0,0,0.25); }
    
    /* State animations */
    .thinking .iris { animation: rot-think 1s ease-in-out infinite; }
    @keyframes rot-think { 0%, 100% { transform: scale(1); } 50% { transform: scale(0.8); } }
    
    .listening .iris { animation: rot-hear 0.3s ease-in-out infinite; }
    @keyframes rot-hear { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.15); } }
    
    .speaking .iris { animation: rot-speak 0.15s ease-in-out infinite; }
    @keyframes rot-speak { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.25); } }
    
    /* Title */
    .title {
        position: fixed; top: 15px; left: 50%; transform: translateX(-50%);
        font-family: 'Metal Mania', cursive;
        font-size: 1.8rem;
        color: #1a1a1a;
        letter-spacing: 1em;
        z-index: 100;
    }
    
    /* Status */
    .status {
        position: fixed; bottom: 50px; left: 50%; transform: translateX(-50%);
        font-family: 'EB Garamond', serif;
        font-style: italic;
        font-size: 0.8rem;
        color: #2a2a2a;
        letter-spacing: 0.5em;
        z-index: 100;
    }
    
    /* Waveform */
    .waveform {
        position: fixed; bottom: 90px; left: 50%; transform: translateX(-50%);
        width: 50%; max-width: 400px; height: 50px;
        display: flex; align-items: center; justify-content: center;
        gap: 2px; z-index: 100;
    }
    
    .wave-bar {
        width: 2px;
        background: linear-gradient(to top, #111, #333);
        border-radius: 1px;
    }
    
    /* Chat */
    .chat-box {
        position: fixed; bottom: 160px; left: 50%; transform: translateX(-50%);
        width: 90%; max-width: 500px; z-index: 100;
    }
    
    .stTextInput > div > div > input {
        background: #050505 !important;
        border: 1px solid #1a1a1a !important;
        border-radius: 0 !important;
        color: #3a3a3a !important;
        font-family: 'EB Garamond', serif !important;
        font-size: 0.9rem !important;
        padding: 10px 15px !important;
    }
    
    .msg {
        background: rgba(5,5,5,0.9) !important;
        border-left: 1px solid #111 !important;
        padding: 8px 12px !important;
        margin: 5px 0 !important;
        font-family: 'EB Garamond', serif !important;
        font-size: 0.85rem !important;
        color: #444 !important;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] { background: #050505 !important; }
</style>
""", unsafe_allow_html=True)


# ============== SESSION ==============
if 'tanya' not in st.session_state:
    st.session_state.tanya = TanyaClient()
if 'history' not in st.session_state:
    st.session_state.history = []
if 'eye_state' not in st.session_state:
    st.session_state.eye_state = "idle"
if 'model' not in st.session_state:
    st.session_state.model = "llama3.1:8b"
if 'wave' not in st.session_state:
    st.session_state.wave = [3] * 40


# ============== AUTO START VOICE ==============
client = st.session_state.tanya

if not client.voice_running and client.voice.stt_ok:
    client.voice_running = True
    
    def handle_speech(text):
        if text and len(text) > 1:
            st.session_state.history.append({"role": "user", "content": text})
            st.session_state.eye_state = "thinking"
            
            resp = client.chat(text, st.session_state.model)
            st.session_state.history.append({"role": "assistant", "content": resp})
            
            st.session_state.eye_state = "speaking"
            client.voice.speak(resp)
            
            time.sleep(3)
            st.session_state.eye_state = "idle"
    
    client.voice.listen_loop(handle_speech)


# ============== RENDER ==============
def render_eye(state):
    st.markdown(f"""
    <div class="eye-wrapper {state}">
        <div class="bruise bruise-1"></div>
        <div class="bruise bruise-2"></div>
        <div class="socket">
            <div class="fracture f-1"></div>
            <div class="fracture f-2"></div>
            <div class="fracture f-3"></div>
            <div class="fracture f-v"></div>
        </div>
        <div class="wound"></div>
        <div class="iris">
            <div class="pupil"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_wave():
    bars = ''.join([f'<div class="wave-bar" style="height:{h}px"></div>' for h in st.session_state.wave])
    st.markdown(f'<div class="waveform">{bars}</div>', unsafe_allow_html=True)


# Title
st.markdown('<div class="title">tanya</div>', unsafe_allow_html=True)

# Eye
render_eye(st.session_state.eye_state)

# Wave
render_wave()

# Status
status_map = {"idle": "awaiting...", "thinking": "processing...", "listening": "hearing...", "speaking": "speaking..."}
st.markdown(f'<div class="status">{status_map.get(st.session_state.eye_state, "...")}</div>', unsafe_allow_html=True)


# Sidebar
with st.sidebar:
    st.markdown('<div style="font-family: Metal Mania; font-size: 1.2rem; color: #1a1a1a; letter-spacing: 0.5em;">tanya</div>', unsafe_allow_html=True)
    
    models = client.get_models()
    if models:
        idx = models.index(st.session_state.model) if st.session_state.model in models else 0
        st.session_state.model = st.selectbox("model", models, index=idx)
    else:
        st.caption("ollama offline")
    
    # Voice status
    if client.voice.stt_ok:
        st.caption("🎤 mic active")
    else:
        st.caption("⚠️ mic unavailable (install pyaudio)")


# Chat
st.markdown('<div class="chat-box">', unsafe_allow_html=True)

for msg in st.session_state.history:
    name = "you" if msg["role"]=="user" else "tanya"
    st.markdown(f'<div class="msg"><strong>{name}:</strong> {msg["content"]}</div>', unsafe_allow_html=True)

if prompt := st.chat_input("...", key="main"):
    st.session_state.eye_state = "thinking"
    st.session_state.history.append({"role": "user", "content": prompt})
    
    resp = client.chat(prompt, st.session_state.model)
    st.session_state.history.append({"role": "assistant", "content": resp})
    
    st.session_state.eye_state = "speaking"
    client.voice.speak(resp)
    
    time.sleep(3)
    st.session_state.eye_state = "idle"
    st.rerun()

st.markdown('</div>', unsafe_allow_html=True)
