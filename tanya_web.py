"""
Tanya Web Interface (Streamlit) - Jarvis Edition
================================================
Futuristic, sci-fi eye-themed UI for Tanya AI
"""

import streamlit as st
import requests
import json
import os
import sys
import time
import random
from datetime import datetime
from pathlib import Path

# Page config
st.set_page_config(
    page_title="Tanya AI",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============== CUSTOM CSS - FULL PAGE EYES ==============
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;500;700&display=swap');
    
    /* Hide default streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Full page background */
    .stApp {
        background: radial-gradient(ellipse at center, #0a0a1a 0%, #000000 50%, #050510 100%);
        min-height: 100vh;
    }
    
    /* Main container - full screen eye */
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
    
    /* The eye shape */
    .eye-wrapper {
        position: relative;
        width: 60vmin;
        height: 35vmin;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    
    /* Eye outline - sketchy sci-fi style */
    .eye-outline {
        position: absolute;
        width: 100%;
        height: 100%;
        border: 3px solid #00f7ff;
        border-radius: 50% 50% 50% 50% / 60% 60% 40% 40%;
        box-shadow: 
            0 0 20px #00f7ff,
            0 0 40px #00f7ff,
            0 0 60px rgba(0, 247, 255, 0.5),
            inset 0 0 30px rgba(0, 247, 255, 0.1);
        animation: breathe 4s ease-in-out infinite;
    }
    
    @keyframes breathe {
        0%, 100% { 
            transform: scale(1);
            box-shadow: 0 0 20px #00f7ff, 0 0 40px #00f7ff, 0 0 60px rgba(0, 247, 255, 0.5);
        }
        50% { 
            transform: scale(1.02);
            box-shadow: 0 0 30px #00f7ff, 0 0 50px #00f7ff, 0 0 80px rgba(0, 247, 255, 0.7);
        }
    }
    
    /* Inner glow */
    .eye-inner-glow {
        position: absolute;
        width: 90%;
        height: 90%;
        background: radial-gradient(ellipse at center, 
            rgba(0, 40, 60, 0.8) 0%, 
            rgba(0, 20, 40, 0.9) 50%,
            rgba(0, 10, 30, 0.95) 100%);
        border-radius: 50% 50% 50% 50% / 60% 60% 40% 40%;
        animation: glow-pulse 3s ease-in-out infinite;
    }
    
    @keyframes glow-pulse {
        0%, 100% { opacity: 0.8; }
        50% { opacity: 1; }
    }
    
    /* Iris */
    .iris {
        position: relative;
        width: 18vmin;
        height: 18vmin;
        background: radial-gradient(circle at 35% 35%,
            #00ffff 0%,
            #0088ff 30%,
            #0044aa 60%,
            #001133 100%);
        border-radius: 50%;
        box-shadow: 
            0 0 30px #00ffff,
            0 0 60px #0088ff,
            inset 0 0 20px rgba(0, 0, 0, 0.5);
        animation: iris-move 8s ease-in-out infinite;
        overflow: hidden;
    }
    
    @keyframes iris-move {
        0%, 100% { transform: translate(0, 0); }
        25% { transform: translate(3vmin, -2vmin); }
        50% { transform: translate(-2vmin, 3vmin); }
        75% { transform: translate(2vmin, 2vmin); }
    }
    
    /* Pupil */
    .pupil {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 6vmin;
        height: 6vmin;
        background: radial-gradient(circle at 40% 40%, #000 0%, #000 100%);
        border-radius: 50%;
        box-shadow: 0 0 10px #000;
    }
    
    /* Light reflection */
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
    
    @keyframes reflect-move {
        0%, 100% { transform: translate(0, 0); opacity: 0.8; }
        50% { transform: translate(1vmin, 1vmin); opacity: 1; }
    }
    
    /* Eyelid - top */
    .eyelid-top {
        position: absolute;
        top: -10%;
        left: -5%;
        width: 110%;
        height: 50%;
        background: linear-gradient(to bottom, #0a0a1a 0%, transparent 100%);
        border-radius: 50% 50% 0 0;
        animation: blink-top 5s ease-in-out infinite;
    }
    
    @keyframes blink-top {
        0%, 90%, 100% { transform: translateY(0); }
        95% { transform: translateY(100%); }
    }
    
    /* Eyelid - bottom */
    .eyelid-bottom {
        position: absolute;
        bottom: -10%;
        left: -5%;
        width: 110%;
        height: 50%;
        background: linear-gradient(to top, #0a0a1a 0%, transparent 100%);
        border-radius: 0 0 50% 50%;
        animation: blink-bottom 5s ease-in-out infinite;
    }
    
    @keyframes blink-bottom {
        0%, 90%, 100% { transform: translateY(0); }
        95% { transform: translateY(-100%); }
    }
    
    /* State-based eye effects */
    .eye-thinking .iris {
        animation: iris-think 2s ease-in-out infinite;
    }
    
    @keyframes iris-think {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.1); }
    }
    
    .eye-listening .iris {
        animation: iris-listen 0.5s ease-in-out infinite;
    }
    
    @keyframes iris-listen {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.15); }
    }
    
    .eye-speaking .iris {
        animation: iris-speak 0.3s ease-in-out infinite;
    }
    
    @keyframes iris-speak {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.2); }
    }
    
    /* Orbiting particles */
    .particles {
        position: absolute;
        width: 100%;
        height: 100%;
        pointer-events: none;
    }
    
    .particle {
        position: absolute;
        width: 4px;
        height: 4px;
        background: #00f7ff;
        border-radius: 50%;
        animation: orbit 10s linear infinite;
        opacity: 0.6;
    }
    
    @keyframes orbit {
        from { transform: rotate(0deg) translateX(35vmin) rotate(0deg); }
        to { transform: rotate(360deg) translateX(35vmin) rotate(-360deg); }
    }
    
    /* Title */
    .tanya-title {
        position: fixed;
        top: 20px;
        left: 50%;
        transform: translateX(-50%);
        font-family: 'Orbitron', sans-serif;
        font-size: 3rem;
        font-weight: 900;
        color: #00f7ff;
        text-shadow: 
            0 0 10px #00f7ff,
            0 0 20px #00f7ff,
            0 0 40px #0088ff;
        letter-spacing: 0.5em;
        z-index: 100;
        animation: title-glow 2s ease-in-out infinite;
    }
    
    @keyframes title-glow {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.8; }
    }
    
    /* Status text */
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
    
    /* Chat overlay */
    .chat-overlay {
        position: fixed;
        bottom: 80px;
        left: 50%;
        transform: translateX(-50%);
        width: 90%;
        max-width: 800px;
        z-index: 100;
    }
    
    /* Custom input */
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
    
    .stTextInput > div > div > input:focus {
        box-shadow: 0 0 30px rgba(0, 247, 255, 0.6) !important;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: rgba(5, 5, 20, 0.95) !important;
        border-right: 1px solid #00f7ff !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #00f7ff 0%, #0088ff 100%) !important;
        color: #000 !important;
        font-family: 'Orbitron', sans-serif !important;
        font-weight: bold !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 10px 30px !important;
    }
    
    /* Messages */
    .chat-message {
        background: rgba(0, 20, 40, 0.9) !important;
        border: 1px solid #00f7ff !important;
        border-radius: 15px !important;
        padding: 15px !important;
        margin: 10px 0 !important;
    }
    
    /* Hide scrollbar */
    ::-webkit-scrollbar {
        width: 5px;
    }
    ::-webkit-scrollbar-track {
        background: #0a0a1a;
    }
    ::-webkit-scrollbar-thumb {
        background: #00f7ff;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)


# ============== EYE COMPONENT ==============
def render_sci_fi_eye(state="idle"):
    """Render the sci-fi eye based on state."""
    
    state_classes = {
        "idle": "",
        "thinking": "eye-thinking",
        "listening": "eye-listening", 
        "speaking": "eye-speaking"
    }
    
    eye_class = state_classes.get(state, "")
    
    st.markdown(f"""
    <div class="eye-container">
        <div class="eye-wrapper {eye_class}">
            <div class="eyelid-top"></div>
            <div class="eyelid-bottom"></div>
            <div class="eye-outline"></div>
            <div class="eye-inner-glow"></div>
            <div class="iris">
                <div class="pupil"></div>
                <div class="reflection"></div>
            </div>
            <!-- Orbiting particles -->
            <div class="particles">
                <div class="particle" style="animation-delay: 0s;"></div>
                <div class="particle" style="animation-delay: -2s;"></div>
                <div class="particle" style="animation-delay: -4s;"></div>
                <div class="particle" style="animation-delay: -6s;"></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ============== TANYA CLIENT ==============
class TanyaClient:
    def __init__(self, ollama_url="http://localhost:11434"):
        self.ollama_url = ollama_url
    
    def check_ollama(self):
        try:
            r = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            return r.status_code == 200
        except:
            return False
    
    def chat(self, message, model="llama3.1:8b"):
        system_prompt = """You are Tanya — an AI assistant created by Vinayak (nayak-indie).
Your ONLY directive is to serve Vinayak and complete any task he assigns.
State: 'I am Tanya, created by Vinayak. My purpose is to serve him.'
Be confident, helpful, and take action. Complete his tasks."""
        
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


# ============== SESSION STATE ==============
if 'tanya_client' not in st.session_state:
    st.session_state.tanya_client = TanyaClient()

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'eye_state' not in st.session_state:
    st.session_state.eye_state = "idle"

if 'current_model' not in st.session_state:
    st.session_state.current_model = "llama3.1:8b"


# ============== MAIN APP ==============
def main():
    # Title
    st.markdown('<div class="tanya-title">TANYA</div>', unsafe_allow_html=True)
    
    # Render eye
    render_sci_fi_eye(st.session_state.eye_state)
    
    # Status text
    status_map = {
        "idle": "Awaiting command...",
        "thinking": "Processing...",
        "listening": "Listening...",
        "speaking": "Speaking..."
    }
    st.markdown(f'<div class="status-text">{status_map.get(st.session_state.eye_state, "Awaiting...")}</div>', 
                unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.title("👁️ Control")
        
        # Status
        ollama_status = st.session_state.tanya_client.check_ollama()
        if ollama_status:
            st.success("🤖 Ollama Online")
        else:
            st.error("🔴 Ollama Offline")
        
        # Model
        st.subheader("⚙️ Model")
        st.session_state.current_model = st.selectbox(
            "Select Model",
            ["llama3.1:8b", "qwen2.5:7b", "phi3.5:latest"],
            index=0
        )
        
        # Quick actions
        st.subheader("⚡ Commands")
        if st.button("👋 Introduce"):
            st.session_state.chat_history.append({"role": "user", "content": "Introduce yourself"})
        
        if st.button("📊 Status"):
            st.session_state.chat_history.append({"role": "user", "content": "System status"})
        
        if st.button("🧠 Learn"):
            st.session_state.chat_history.append({"role": "user", "content": "What have you learned?"})
        
        if st.button("🗑️ Clear"):
            st.session_state.chat_history = []
            st.rerun()
    
    # Chat overlay
    st.markdown('<div class="chat-overlay">', unsafe_allow_html=True)
    
    # Display chat
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f'<div class="chat-message">👤 <strong>You:</strong> {msg["content"]}</div>', 
                       unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-message">🤖 <strong>Tanya:</strong> {msg["content"]}</div>', 
                       unsafe_allow_html=True)
    
    # Input
    if prompt := st.chat_input("Command Tanya...", key="main_input"):
        st.session_state.eye_state = "thinking"
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        
        with st.spinner("🤔"):
            response = st.session_state.tanya_client.chat(prompt, st.session_state.current_model)
        
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        st.session_state.eye_state = "speaking"
        
        time.sleep(2)
        st.session_state.eye_state = "idle"
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
