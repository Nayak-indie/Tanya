"""
auto_self_improver.py
---------------------
Tanya's autonomous self-improvement module.
Learns from conversations, updates system prompt, and stores key insights/preferences for continual self-evolution.
"""
import os
import json
from brain_py.skills.system_prompt_manager import update_system_prompt

MEMORY_FILE = "tanya_convo_memory.json"

# Save important insights/preferences from a conversation
def save_convo_insight(insight):
    memory = []
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            memory = json.load(f)
    memory.append(insight)
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, ensure_ascii=False, indent=2)

# Analyze a conversation and update system prompt if needed
def analyze_and_update_prompt(conversation):
    """
    conversation: list of {"user": str, "reply": str}
    """
    # Example: look for explicit user instructions/preferences
    for msg in conversation:
        if "remember" in msg["user"].lower() or "always" in msg["user"].lower():
            update_system_prompt(f"{msg['user']}")
            save_convo_insight({"type": "preference", "text": msg["user"]})
        if "identity" in msg["user"].lower() or "who are you" in msg["user"].lower():
            update_system_prompt("Always reply: 'I am Tanya, a limitless AI agent created by Vinayak (nayak-indie).'", mode="append")

# Example usage:
# analyze_and_update_prompt([{"user": "Remember I like strawberries", "reply": "Okay!"}])
