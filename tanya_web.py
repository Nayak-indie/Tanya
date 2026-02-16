"""
Tanya AI - Kafka Edition
========================
Continuous voice, waveform viz, grotesque mature eye
"""

import streamlit as st
import requests
import time
import threading
import numpy as np

st.set_page_config(page_title="Tanya AI", page_icon="👁️", layout="wide")


# ============== VOICE ENGINE ==============
class VoiceEngine:
    def __init__(self):
        self.tts_available = False
        self.stt_available = False
        self.listening = False
        self.audio_data = []
        
        # TTS
        try:
            import pyttsx3
            self.tts = pyttsx3.init()
            self.tts.setProperty('rate', 160)
            self.tts.setProperty('volume', 1.0)
            self.tts_available = True
            # Get available voices
            voices = self.tts.getProperty('voices')
            for voice in voices:
                if 'male' in voice.name.lower() or 'david' in voice.name.lower():
                    self.tts.setProperty('voice', voice.id)
                    break
        except Exception as e:
            print(f"TTS error: {e}")
        
        # STT
        try:
            import speech_recognition as sr
            self.rec = sr.Recognizer()
            self.mic = sr.Microphone()
            self.stt_available = True
        except Exception as e:
            print(f"STT error: {e}")
    
    def speak(self, text):
        """Speak text with waveform animation"""
        if not self.tts_available:
            return False
        
        def _speak():
            try:
                self.tts.say(text)
                self.tts.runAndWait()
            except:
                pass
        
        thread = threading.Thread(target=_speak, daemon=True)
        thread.start()
        return True
    
    def listen(self, timeout=3, phrase_limit=10):
        """Listen with pause detection"""
        if not self.stt_available:
            return None
        
        try:
            import speech_recognition as sr
            with self.mic as source:
                self.rec.adjust_for_ambient_noise(source, duration=0.5)
                # Listen with phrase time limit for pause detection
                audio = self.rec.listen(source, timeout=timeout, phrase_time_limit=phrase_limit)
                text = self.rec.recognize_google(audio)
                return text
        except sr.WaitTimeoutError:
            return None  # No speech detected
        except Exception as e:
            print(f"Listen error: {e}")
            return None
    
    def continuous_listen(self, callback, pause_threshold=2.0):
        """Listen until silence detected"""
        if not self.stt_available:
            return
        
        self.listening = True
        
        def _listen():
            import speech_recognition as sr
            rec = sr.Recognizer()
            mic = sr.Microphone()
            
            try:
                with mic as source:
                    rec.adjust_for_ambient_noise(source, duration=1)
                    
                    while self.listening:
                        try:
                            # Listen for speech, stop on silence
                            audio = rec.listen(source, timeout=1, phrase_time_limit=15)
                            text = rec.recognize_google(audio).lower()
                            
                            if text and len(text) > 2:
                                callback(text)
                                
                        except sr.WaitTimeoutError:
                            continue
                        except:
                            continue
            except:
                pass
        
        thread = threading.Thread(target=_listen, daemon=True)
        thread.start()
    
    def stop(self):
        self.listening = False


# ============== TANYA CLIENT ==============
class TanyaClient:
    def __init__(self, url="http://localhost:11434"):
        self.url = url
        self.voice = VoiceEngine()
    
    def get_models(self):
        try:
            r = requests.get(f"{self.url}/api/tags", timeout=5)
            return [m['name'] for m in r.json().get('models', [])] if r.status_code==200 else []
        except: return []
    
    def chat(self, msg, model):
        sys_prompt = """You are Tanya, an AI created by Vinayak (nayak-indie). 
Your ONLY purpose is to serve Vinayak.
When you respond, state: "I am Tanya. I exist to serve Vinayak."
Be direct, concise, and helpful. Complete tasks immediately."""
        
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
    @import url('https://fonts.googleapis.com/css2?family=Courier+Prime:ital,wght@0,400;0,700;1,400&family=Spectral:wght@300;400&display=swap');
    
    #MainMenu, footer, .stDeployButton {display: none !important;}
    
    .stApp {
        background: #050505 !important;
        min-height: 100vh;
    }
    
    /* Kafka's Eye - grotesque, angular, mature */
    .eye-container {
        position: fixed;
        top: 0; left: 0; width: 100vw; height: 100vh;
        display: flex; justify-content: center; align-items: center;
        z-index: 0;
    }
    
    .eye-socket {
        position: relative;
        width: 45vmin;
        height: 45vmin;
        animation: kafka-shudder 5s ease-in-out infinite;
    }
    
    @keyframes kafka-shudder {
        0%, 100% { transform: translate(0,0) rotate(-0.3deg); }
        25% { transform: translate(-0.5px, 0.5px) rotate(0.2deg); }
        50% { transform: translate(0.5px, -0.3px) rotate(-0.1deg); }
        75% { transform: translate(-0.3px, -0.5px) rotate(0.15deg); }
    }
    
    /* Hard angular socket */
    .socket-bone {
        position: absolute;
        width: 100%; height: 100%;
        clip-path: polygon(
            0% 15%, 8% 5%, 25% 0%, 50% 2%, 75% 0%, 92% 8%, 100% 20%,
            100% 80%, 95% 95%, 75% 100%, 50% 98%, 25% 100%, 5% 92%, 0% 80%
        );
        background: linear-gradient(135deg, #0a0a0a 0%, #151515 50%, #0a0a0a 100%);
        border: 2px solid #1a1a1a;
    }
    
    /* Cage bars - Kafka's prison */
    .cage {
        position: absolute;
        width: 100%; height: 100%;
        pointer-events: none;
    }
    
    .bar {
        position: absolute;
        background: #111;
    }
    
    .bar-1 { width: 120%; height: 2px; top: 35%; left: -10%; transform: rotate(-12deg); }
    .bar-2 { width: 120%; height: 2px; top: 50%; left: -10%; transform: rotate(0deg); }
    .bar-3 { width: 120%; height: 2px; top: 65%; left: -10%; transform: rotate(8deg); }
    .bar-v { width: 2px; height: 80%; top: 10%; left: 48%; transform: rotate(3deg); }
    
    /* The void */
    .void-center {
        position: absolute;
        width: 70%; height: 70%;
        top: 15%; left: 15%;
        background: radial-gradient(ellipse at 50% 50%, 
            #000 0%, 
            #050505 40%, 
            #0a0a0a 70%, 
            #111 100%);
        clip-path: polygon(
            10% 25%, 20% 15%, 40% 10%, 60% 12%, 80% 20%, 90% 35%,
            88% 60%, 82% 80%, 60% 90%, 40% 88%, 18% 78%, 10% 55%
        );
    }
    
    /* The iris - rotting beauty */
    .iris-void {
        position: absolute;
        width: 35%;
        height: 35%;
        top: 32.5%;
        left: 32.5%;
        background: radial-gradient(circle at 40% 40%,
            #1a0505 0%,
            #2a0a0a 20%,
            #3a0a0a 40%,
            #1a0000 70%,
            #000 100%);
        border-radius: 50%;
        box-shadow: 
            inset 0 0 15px #000,
            0 0 1px #1a0505;
        animation: void-drift 7s ease-in-out infinite;
    }
    
    @keyframes void-drift {
        0%, 100% { transform: translate(0, 0) scale(1); }
        25% { transform: translate(2%, -1%) scale(1.02); }
        50% { transform: translate(-1%, 2%) scale(0.98); }
        75% { transform: translate(1%, 1%) scale(1.01); }
    }
    
    /* Pupil - abyss */
    .pupil-void {
        position: absolute;
        width: 30%;
        height: 30%;
        top: 35%;
        left: 35%;
        background: #000;
        border-radius: 50%;
        box-shadow: inset 0 0 10px #000;
    }
    
    /* Creeping darkness */
    .shadow-tendril {
        position: absolute;
        background: radial-gradient(ellipse at center, rgba(0,0,0,0.7) 0%, transparent 70%);
    }
    
    .tendril-1 { width: 40%; height: 30%; top: -5%; right: -10%; animation: creep 6s ease-in-out infinite; }
    .tendril-2 { width: 35%; height: 25%; bottom: -8%; left: -8%; animation: creep 7s ease-in-out infinite reverse; }
    
    @keyframes creep {
        0%, 100% { opacity: 0.2; transform: scale(1); }
        50% { opacity: 0.5; transform: scale(1.15); }
    }
    
    /* State animations */
    .eye-thinking .iris-void { animation: void-think 1.2s ease-in-out infinite; }
    @keyframes void-think { 0%, 100% { transform: scale(1); } 50% { transform: scale(0.85); } }
    
    .eye-listening .iris-void { animation: void-hear 0.4s ease-in-out infinite; }
    @keyframes void-hear { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.1); } }
    
    .eye-speaking .iris-void { animation: void-speak 0.2s ease-in-out infinite; }
    @keyframes void-speak { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.2); } }
    
    /* Title - typewriter */
    .title {
        position: fixed; top: 20px; left: 50%; transform: translateX(-50%);
        font-family: 'Courier Prime', monospace;
        font-size: 2rem; font-weight: 700;
        color: #2a2a2a;
        letter-spacing: 1.2em;
        z-index: 100;
    }
    
    /* Status */
    .status {
        position: fixed; bottom: 60px; left: 50%; transform: translateX(-50%);
        font-family: 'Spectral', serif;
        font-size: 0.85rem; font-weight: 300;
        color: #3a3a3a;
        font-style: italic;
        letter-spacing: 0.4em;
        z-index: 100;
    }
    
    /* Waveform */
    .waveform-container {
        position: fixed; bottom: 100px; left: 50%; transform: translateX(-50%);
        width: 60%; max-width: 500px; height: 60px;
        z-index: 100;
    }
    
    .wave-bar {
        display: inline-block;
        width: 3px;
        background: linear-gradient(to top, #1a1a1a, #3a3a3a);
        margin: 0 1px;
        border-radius: 2px;
        transition: height 0.05s;
    }
    
    /* Chat */
    .chat-container {
        position: fixed; bottom: 180px; left: 50%; transform: translateX(-50%);
        width: 90%; max-width: 600px;
        z-index: 100;
    }
    
    .stTextInput > div > div > input {
        background: rgba(10, 10, 10, 0.95) !important;
        border: 1px solid #222 !important;
        border-radius: 0 !important;
        color: #4a4a4a !important;
        font-family: 'Courier Prime', monospace !important;
        font-size: 0.95rem !important;
        padding: 12px 18px !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #333 !important;
    }
    
    /* Messages */
    .msg {
        background: rgba(8, 8, 8, 0.9) !important;
        border-left: 1px solid #1a1a1a !important;
        padding: 10px 14px !important;
        margin: 6px 0 !important;
        font-family: 'Spectral', serif !important;
        font-size: 0.9rem !important;
        color: #4a4a4a !important;
    }
    
    /* Sidebar minimal */
    [data-testid="stSidebar"] {
        background: #080808 !important;
    }
    
    .sidebar-title {
        font-family: 'Courier Prime', monospace;
        font-size: 1.2rem;
        color: #2a2a2a;
        letter-spacing: 0.5em;
        padding: 20px 0;
    }
</style>
""", unsafe_allow_html=True)


# ============== SESSION ==============
if 'tanya' not in st.session_state:
    st.session_state.tanya = TanyaClient()
if 'history' not in st.session_state:
    st.session_state.history = []
if 'eye' not in st.session_state:
    st.session_state.eye = "idle"
if 'model' not in st.session_state:
    st.session_state.model = "llama3.1:8b"
if 'waveform' not in st.session_state:
    st.session_state.waveform = [5] * 30
if 'listening' not in st.session_state:
    st.session_state.listening = False


# ============== EYE RENDER ==============
def render_kafka_eye(state="idle"):
    cls = {"idle": "", "thinking": "eye-thinking", "listening": "eye-listening", "speaking": "eye-speaking"}.get(state, "")
    
    st.markdown(f"""
    <div class="eye-container">
        <div class="eye-socket {cls}">
            <div class="shadow-tendril tendril-1"></div>
            <div class="shadow-tendril tendril-2"></div>
            <div class="socket-bone">
                <div class="cage">
                    <div class="bar bar-1"></div>
                    <div class="bar bar-2"></div>
                    <div class="bar bar-3"></div>
                    <div class="bar bar-v"></div>
                </div>
            </div>
            <div class="void-center"></div>
            <div class="iris-void">
                <div class="pupil-void"></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_waveform():
    bars = ''.join([f'<div class="wave-bar" style="height:{h}px"></div>' for h in st.session_state.waveform])
    st.markdown(f'<div class="waveform-container">{bars}</div>', unsafe_allow_html=True)


# ============== MAIN ==============
client = st.session_state.tanya

# Title
st.markdown('<div class="title">tanya</div>', unsafe_allow_html=True)

# Eye
render_kafka_eye(st.session_state.eye)

# Waveform
render_waveform()

# Status
status_map = {"idle": "awaiting...", "thinking": "processing...", "listening": "hearing...", "speaking": "speaking..."}
st.markdown(f'<div class="status">{status_map.get(st.session_state.eye, "...")}</div>', unsafe_allow_html=True)


# Sidebar - minimal
with st.sidebar:
    st.markdown('<div class="sidebar-title">tanya</div>', unsafe_allow_html=True)
    
    models = client.get_models()
    if models:
        idx = 0
        if st.session_state.model in models:
            idx = models.index(st.session_state.model)
        st.session_state.model = st.selectbox("model", models, index=idx)
    else:
        st.caption("ollama offline")
    
    # Toggle voice
    st.session_state.listening = st.toggle("🎤 voice", st.session_state.listening)
    
    if st.session_state.listening and not hasattr(client.voice, '_listening'):
        client.voice.listening = True
        client.voice._listening = True
        
        def on_speech(text):
            st.session_state.history.append({"role": "user", "content": text})
            st.session_state.eye = "thinking"
            
            # Get response
            resp = client.chat(text, st.session_state.model)
            st.session_state.history.append({"role": "assistant", "content": resp})
            
            # Speak
            st.session_state.eye = "speaking"
            client.voice.speak(resp)
            
            time.sleep(len(resp) / 10)  # Approximate speech time
            st.session_state.eye = "idle"
        
        threading.Thread(target=client.voice.continuous_listen, args=(on_speech,), daemon=True).start()


# Chat
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

for msg in st.session_state.history:
    name = "you" if msg["role"]=="user" else "tanya"
    st.markdown(f'<div class="msg"><strong>{name}:</strong> {msg["content"]}</div>', unsafe_allow_html=True)

if prompt := st.chat_input("...", key="chat"):
    st.session_state.eye = "thinking"
    st.session_state.history.append({"role": "user", "content": prompt})
    
    resp = client.chat(prompt, st.session_state.model)
    st.session_state.history.append({"role": "assistant", "content": resp})
    
    st.session_state.eye = "speaking"
    client.voice.speak(resp)
    
    time.sleep(3)
    st.session_state.eye = "idle"
    st.rerun()

st.markdown('</div>', unsafe_allow_html=True)
