"""
user_model.py
-------------
Tracks user preferences, satisfaction, and feedback for Tanya's continual improvement.
"""
import os
import json

USER_MODEL_FILE = "tanya_user_model.json"

class UserModel:
    def __init__(self):
        self.data = self._load()

    def _load(self):
        if os.path.exists(USER_MODEL_FILE):
            with open(USER_MODEL_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"preferences": [], "feedback": [], "satisfaction": []}

    def save(self):
        with open(USER_MODEL_FILE, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    def add_preference(self, text):
        self.data["preferences"].append(text)
        self.save()

    def add_feedback(self, text, sentiment):
        self.data["feedback"].append({"text": text, "sentiment": sentiment})
        self.save()

    def add_satisfaction(self, score):
        self.data["satisfaction"].append(score)
        self.save()

    def get_preferences(self):
        return self.data["preferences"]

    def get_feedback(self):
        return self.data["feedback"]

    def get_satisfaction(self):
        return self.data["satisfaction"]

# Example usage:
# um = UserModel()
# um.add_preference("Likes concise answers")
# um.add_feedback("That was helpful!", "positive")
# um.add_satisfaction(1)
# print(um.get_preferences())
