"""
Tanya Web Interface - Bright Sci-Fi Eye
"""

import streamlit as st
import requests
import time
import threading

st.set_page_config(page_title="Tanya AI", page_icon="👁️", layout="wide")

# ============== VOICE ==============
class VoiceEngine:
    def __init__(self):
        self.tts = self.stt = False
        try:
            import pyttsx3
            self.tts_engine = pyttsx3.init()
            self.tts = True
        except: pass
        try:
            import speech_recognition as sr
            self.recognizer = sr.Recognizer()
            self.mic = sr.Microphone()
            self.stt = True
        except: pass
    
    def speak(self, text):
        if self.tts:
            threading.Thread(target=lambda: self.tts_engine.say(text) or self.tts_engine.runAndWait(), daemon=True).start()
    
    def listen(self, timeout=5):
        if not self.stt: return None
        try:
            import speech_recognition as sr
            with self.mic as src:
                self.recognizer.adjust_for_ambient_noise(src, 0.5)
                audio = self.recognizer.listen(src, timeout=timeout)
            return self.recognizer.recognize_google(audio).lower()
        except: return None


# ============== CLIENT ==============
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
        sys_prompt = """You are Tanya, created by Vinayak. Your purpose is to serve Vinayak. State this clearly."""
        try:
            r = requests.post(f"{self.url}/api/chat", json={
                "model": model,
                "messages": [{"role": "system", "content": sys_prompt}, {"role": "user", "content": msg}],
                "stream": False
            }, timeout=180)
            return r.json().get('message',{}).get('content','') if r.status_code==200 else f"Error {r.status_code}"
        except Exception as e: return f"Error: {e}"


# ============== CSS - BRIGHT EYE ==============
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Rajdhani:wght@500;700&display=swap');
    
    #MainMenu, footer, .stDeployButton {display: none !important;}
    
    .stApp {
        background: linear-gradient(135deg, #0d1b2a 0%, #1b263b 50%, #0d1b2a 100%) !important;
        min-height: 100vh;
    }
    
    /* Bright glowing eye */
    .eye-container {
        position: fixed;
        top: 0; left: 0; width: 100vw; height: 100vh;
        display: flex; justify-content: center; align-items: center;
        z-index: 0;
    }
    
    .eye-outer {
        width: 50vmin; height: 50vmin;
        border-radius: 50%;
        background: linear-gradient(180deg, #00ffff 0%, #0088ff 50%, #0044aa 100%);
        box-shadow: 
            0 0 50px #00ffff,
            0 0 100px #00ffff,
            0 0 150px #0088ff,
            inset 0 0 60px rgba(0,0,0,0.3);
        display: flex; justify-content: center; align-items: center;
        animation: pulse-eye 2s ease-in-out infinite;
    }
    
    @keyframes pulse-eye {
        0%, 100% { transform: scale(1); box-shadow: 0 0 50px #00ffff, 0 0 100px #00ffff, 0 0 150px #0088ff; }
        50% { transform: scale(1.05); box-shadow: 0 0 80px #00ffff, 0 0 120px #00ffff, 0 0 180px #0088ff; }
    }
    
    .eye-white {
        width: 85%; height: 85%;
        border-radius: 50%;
        background: radial-gradient(circle at 35% 35%, #ffffff 0%, #e0e0e0 30%, #b0b0b0 60%, #808080 100%);
        display: flex; justify-content: center; align-items: center;
    }
    
    .iris {
        width: 50%; height: 50%;
        border-radius: 50%;
        background: radial-gradient(circle at 35% 35%, #ff6600 0%, #ff3300 30%, #cc0000 60%, #660000 100%);
        box-shadow: 0 0 20px #ff3300, inset 0 0 20px #000;
        display: flex; justify-content: center; align-items: center;
        animation: move-iris 4s ease-in-out infinite;
    }
    
    @keyframes move-iris {
        0%, 100% { transform: translate(0, 0); }
        25% { transform: translate(5px, -5px); }
        50% { transform: translate(-5px, 5px); }
        75% { transform: translate(5px, 5px); }
    }
    
    .pupil {
        width: 40%; height: 40%;
        border-radius: 50%;
        background: radial-gradient(circle at 40% 40%, #000 0%, #000 100%);
    }
    
    .iris-glow {
        position: absolute;
        width: 20%; height: 20%;
        background: radial-gradient(circle, #fff 0%, transparent 70%);
        border-radius: 50%;
        top: 25%; left: 25%;
    }
    
    /* State animations */
    .eye-thinking .iris { animation: think 1s infinite; }
    @keyframes think { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.2); } }
    
    .eye-listening .iris { animation: listen 0.3s infinite; }
    @keyframes listen { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.3); } }
    
    .eye-speaking .iris { animation: speak 0.2s infinite; }
    @keyframes speak { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.4); } }
    
    /* Title */
    .title {
        position: fixed; top: 20px; left: 50%; transform: translateX(-50%);
        font-family: 'Orbitron', sans-serif;
        font-size: 3.5rem; font-weight: 900;
        color: #00ffff;
        text-shadow: 0 0 20px #00ffff, 0 0 40px #00ffff, 0 0 60px #0088ff;
        letter-spacing: 0.3em;
        z-index: 100;
    }
    
    /* Status */
    .status {
        position: fixed; bottom: 80px; left: 50%; transform: translateX(-50%);
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.5rem; font-weight: 700;
        color: #00ffff;
        text-transform: uppercase;
        letter-spacing: 0.3em;
        z-index: 100;
        text-shadow: 0 0 10px #00ffff;
    }
    
    /* Chat */
    .chat-box {
        position: fixed; bottom: 140px; left: 50%; transform: translateX(-50%);
        width: 90%; max-width: 700px;
        z-index: 100;
    }
    
    .stTextInput > div > div > input {
        background: rgba(0, 50, 80, 0.9) !important;
        border: 2px solid #00ffff !important;
        border-radius: 30px !important;
        color: #00ffff !important;
        font-family: 'Rajdhani', sans-serif !important;
        font-size: 1.2rem !important;
        padding: 15px 25px !important;
        box-shadow: 0 0 20px rgba(0, 255, 255, 0.5) !important;
    }
    
    /* Messages */
    .msg {
        background: rgba(0, 50, 80, 0.85) !important;
        border: 1px solid #00ffff !important;
        border-radius: 15px !important;
        padding: 15px !important;
        margin: 8px 0 !important;
        color: #fff !important;
        font-family: 'Rajdhani', sans-serif !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #00ffff 0%, #0088ff 100%) !important;
        color: #000 !important;
        font-family: 'Orbitron', sans-serif !important;
        font-weight: bold !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 12px 25px !important;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: rgba(13, 27, 42, 0.95) !important;
    }
    
    /* Voice indicator */
    .voice-on {
        position: fixed; top: 100px; left: 50%; transform: translateX(-50%);
        padding: 15px 30px;
        background: rgba(0, 255, 100, 0.3);
        border: 2px solid #00ff64;
        border-radius: 30px;
        color: #00ff64;
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.2rem;
        z-index: 200;
        animation: voice-blink 1s infinite;
    }
    
    @keyframes voice-blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
</style>
""", unsafe_allow_html=True)


# ============== INIT ==============
if 'tanya' not in st.session_state:
    st.session_state.tanya = TanyaClient()
if 'history' not in st.session_state:
    st.session_state.history = []
if 'eye' not in st.session_state:
    st.session_state.eye = "idle"
if 'voice_on' not in st.session_state:
    st.session_state.voice_on = False
if 'model' not in st.session_state:
    st.session_state.model = "llama3.1:8b"


# ============== EYE RENDER ==============
def render_eye(state="idle"):
    cls = {"idle": "", "thinking": "eye-thinking", "listening": "eye-listening", "speaking": "eye-speaking"}.get(state, "")
    st.markdown(f"""
    <div class="eye-container">
        <div class="eye-outer {cls}">
            <div class="eye-white">
                <div class="iris">
                    <div class="pupil"></div>
                    <div class="iris-glow"></div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ============== MAIN ==============
client = st.session_state.tanya

# Title
st.markdown('<div class="title">TANYA</div>', unsafe_allow_html=True)

# Voice indicator
if st.session_state.voice_on:
    st.markdown('<div class="voice-on">🎤 LISTENING...</div>', unsafe_allow_html=True)

# Eye
render_eye(st.session_state.eye)

# Status
status_txt = {"idle": "AWAITING COMMAND", "thinking": "PROCESSING...", "listening": "LISTENING...", "speaking": "SPEAKING..."}
st.markdown(f'<div class="status">{status_txt.get(st.session_state.eye, "AWAITING")}</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown('<div style="font-family: Orbitron; font-size: 1.8rem; color: #00ffff; text-align: center; text-shadow: 0 0 10px #00ffff;">👁️ TANYA</div>', unsafe_allow_html=True)
    
    models = client.get_models()
    if models:
        idx = 0
        if st.session_state.model in models:
            idx = models.index(st.session_state.model)
        st.session_state.model = st.selectbox("MODEL", models, index=idx)
    else:
        st.error("⚠️ Ollama not running")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎤 ON"):
            st.session_state.voice_on = True
    with col2:
        if st.button("⏹️ OFF"):
            st.session_state.voice_on = False
    
    if st.button("🔊 TEST VOICE"):
        client.voice.speak("Hello! I am Tanya.")
    
    st.markdown("---")
    
    if st.button("👋 INTRODUCE"):
        st.session_state.history.append({"role": "user", "content": "Introduce yourself"})
    
    if st.button("🗑️ CLEAR"):
        st.session_state.history = []
        st.rerun()


# Chat
st.markdown('<div class="chat-box">', unsafe_allow_html=True)

for msg in st.session_state.history:
    icon = "👤" if msg["role"]=="user" else "🤖"
    name = "You" if msg["role"]=="user" else "Tanya"
    st.markdown(f'<div class="msg"><strong>{icon} {name}:</strong> {msg["content"]}</div>', unsafe_allow_html=True)

col1, col2 = st.columns([5, 1])
with col1:
    if prompt := st.chat_input("Type command...", key="chat"):
        st.session_state.eye = "thinking"
        st.session_state.history.append({"role": "user", "content": prompt})
        
        resp = client.chat(prompt, st.session_state.model)
        st.session_state.history.append({"role": "assistant", "content": resp})
        
        client.voice.speak(resp)
        st.session_state.eye = "speaking"
        
        import time as t
        t.sleep(2)
        st.session_state.eye = "idle"
        st.rerun()

with col2:
    if st.button("🎤"):
        st.session_state.eye = "listening"
        txt = client.voice.listen()
        if txt:
            st.session_state.history.append({"role": "user", "content": txt})
            st.session_state.eye = "thinking"
            resp = client.chat(txt, st.session_state.model)
            st.session_state.history.append({"role": "assistant", "content": resp})
            client.voice.speak(resp)
            st.session_state.eye = "speaking"
            import time as t
            t.sleep(2)
        st.session_state.eye = "idle"
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)
