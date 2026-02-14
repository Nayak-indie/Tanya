"""
retrain_model.py
----------------
Tanya's self-automation script for model retraining using conversation and feedback data.
This script:
- Aggregates user conversations, preferences, and satisfaction feedback
- Formats them as a fine-tuning dataset (instruction–response pairs, with optional weights)
- (Optionally) triggers a local fine-tuning process (e.g., using Hugging Face or llama.cpp tools)
- Exports a new GGUF model file
"""

import os
import json
from datetime import datetime
from brain_py.system.log import log_info

# Paths to data
USER_MODEL_FILE = "tanya_user_model.json"
CONVO_MEMORY_FILE = "tanya_convo_memory.json"
DATASET_FILE = "tanya_finetune_dataset.jsonl"

# 1. Aggregate data
def aggregate_data():
    data = []
    if os.path.exists(USER_MODEL_FILE):
        with open(USER_MODEL_FILE, "r", encoding="utf-8") as f:
            user_model = json.load(f)
            for fb in user_model.get("feedback", []):
                data.append({"instruction": fb["text"], "response": "", "weight": 1 if fb["sentiment"] == "positive" else 0})
    if os.path.exists(CONVO_MEMORY_FILE):
        with open(CONVO_MEMORY_FILE, "r", encoding="utf-8") as f:
            for entry in json.load(f):
                data.append({"instruction": entry.get("user", ""), "response": entry.get("reply", ""), "weight": 1})
    return data

# 2. Format as dataset
def save_dataset(data):
    with open(DATASET_FILE, "w", encoding="utf-8") as f:
        for item in data:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
    log_info(f"Dataset saved to {DATASET_FILE}")

# 3. (Optional) Trigger fine-tuning (placeholder)
def retrain_model():
    data = aggregate_data()
    save_dataset(data)
    # Here you would call your local fine-tuning tool, e.g.:
    # os.system(f"python finetune_script.py --data {DATASET_FILE} --output new_model.gguf")
    log_info("Model retraining would be triggered here (customize as needed).")

if __name__ == "__main__":
    retrain_model()
