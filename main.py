"""
main.py - Tanya 24/7 with Active Learning
=========================================
Run with: python main.py
Or as service: systemd (see setup/systemd/tanya.service)
"""

import os
import sys
import time
import threading
from brain_py.interface.cli import CLI
from brain_py.interface.orchestrator import Orchestrator
from brain_py.system.boot import boot_event
from brain_py.system.events import EventType
from brain_py.memory.memory_core import MemoryCore
from brain_py.autonomy.background_runner import BackgroundRunner


def main():
    """Run Tanya with 24/7 background learning capabilities."""
    
    # === SETUP ===
    print("🤖 Initializing Tanya...")
    
    memory = MemoryCore()
    orchestrator = Orchestrator(memory)
    
    # Initialize background runner (24/7 loops)
    ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434")
    background = BackgroundRunner(
        memory=memory,
        curiosity_interval_minutes=10,   # Research every 10 min idle
        consolidate_interval_minutes=60,  # Consolidate every hour idle
        ollama_url=ollama_url
    )
    
    # Start background loops
    bg_status = background.start()
    print(f"[BACKGROUND] {bg_status}")
    
    # === SYSTEM BOOT ===
    boot = boot_event()
    print(f"[ORCH] Handling event: {boot.type}")
    print("[RESULT]", orchestrator.handle_event(boot.type, boot.payload))
    
    # === CHAT INTERFACE ===
    print("\n🤖 Tanya online. Type 'exit' or 'quit' to shutdown.")
    print("   Background learning active. Tanya will learn when idle.\n")
    
    # Check for voice, fall back to CLI if not available
    try:
        from brain_py.interface.voice import VoiceInterface
        voice = VoiceInterface()
        use_voice = True
        print("[VOICE] Voice interface enabled")
    except Exception as e:
        print(f"[CLI] Voice not available, using text: {e}")
        use_voice = False
        cli = CLI(orchestrator)
    
    while True:
        # Get input (voice or CLI)
        if use_voice:
            try:
                user_text = voice.listen()
            except Exception as e:
                print(f"[VOICE ERROR] {e}, switching to CLI")
                use_voice = False
                cli = CLI(orchestrator)
                user_text = cli.get_input()
        else:
            user_text = cli.get_input()
        
        if user_text.lower() in ("exit", "quit"):
            print("🤖 Tanya shutting down...")
            background.stop()
            break
        
        # Update background system (user is active)
        background.curiosity.update_activity()
        
        # === PROCESS USER INPUT ===
        
        # 1️⃣ Check for user override commands
        if orchestrator.override.interpret(user_text):
            continue
        
        # 2️⃣ Check for skill learning requests
        skill_keywords = ["learn to", "teach yourself", "figure out how", "can you"]
        if any(kw in user_text.lower() for kw in skill_keywords):
            # Queue for background learning
            background.request_skill_learning(user_text)
            print("[BACKGROUND] Skill learning queued")
        
        # 3️⃣ Normal event → orchestrator
        event = type('Event', (), {
            'type': EventType.USER_INPUT, 
            'payload': {'text': user_text}
        })()
        result = orchestrator.handle_event(event.type, event.payload)
        response = result.get("result") if isinstance(result, dict) else str(result)
        
        # 4️⃣ Output response
        if use_voice:
            try:
                voice.speak(response)
            except Exception as e:
                print(f"[TANYA] {response}")
        else:
            print(f"[TANYA] {response}")
        
        # 5️⃣ Show current state
        current_intent = orchestrator.intent.get_intent()
        active_goal = orchestrator.goals.get_active_goal()
        print(f"[INTENT] {current_intent['name'] if current_intent else 'None'}")
        print(f"[GOAL] {active_goal['name'] if active_goal else 'None'}")
        
        # 6️⃣ Feedback loop
        feedback = input("Rate response (good/bad/boring/skip): ").strip().lower()
        if feedback in ("good", "bad", "boring"):
            orchestrator.memory.remember("feedback", 
                orchestrator.memory.recall("feedback", []) + 
                [{"input": user_text, "response": response, "rating": feedback}]
            )
        
        # 7️⃣ Check background status (optional)
        if random.random() < 0.1:  # 10% chance
            status = background.get_status()
            print(f"[BACKGROUND] Curiosity: {status['curiosity']['is_active']}, "
                  f"Consolidated: {status['consolidator']['last_consolidation']}")

    print("✅ Tanya offline.")

if __name__ == "__main__":
    import random  # For status check
    main()
