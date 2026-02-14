"""
system_prompt_manager.py
-----------------------
Allows Tanya to update and persist her system prompt based on user conversations and preferences.
"""
import os
import json

PROMPT_FILE = "tanya_system_prompt.json"

# Load the current system prompt
def load_system_prompt():
    if os.path.exists(PROMPT_FILE):
        with open(PROMPT_FILE, "r", encoding="utf-8") as f:
            return json.load(f).get("prompt", "")
    return ""

# Save a new system prompt
def save_system_prompt(prompt):
    with open(PROMPT_FILE, "w", encoding="utf-8") as f:
        json.dump({"prompt": prompt}, f, ensure_ascii=False, indent=2)

# Update the system prompt (append or replace)
def update_system_prompt(new_info, mode="append"):
    current = load_system_prompt()
    if mode == "replace" or not current:
        save_system_prompt(new_info)
    else:
        updated = current.strip() + "\n" + new_info.strip()
        save_system_prompt(updated)

# Example usage:
# update_system_prompt("You should always greet Vinayak cheerfully.")
# print(load_system_prompt())
