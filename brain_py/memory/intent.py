class IntentManager:
    """Simple in-memory intent tracking."""
    def __init__(self):
        self.current_intent = None

    def get_intent(self):
        return self.current_intent

    def set_intent(self, name, priority=0.5, source="system"):
        self.current_intent = {
            "name": name,
            "priority": priority,
            "source": source
        }

    def clear_intent(self):
        self.current_intent = None

    def reinforce_intent(self, success=True):
        """Reinforce the current intent based on success/failure."""
        if self.current_intent:
            if success:
                self.current_intent["priority"] = min(1.0, self.current_intent["priority"] + 0.1)
            else:
                self.current_intent["priority"] = max(0.0, self.current_intent["priority"] - 0.1)

    def summarize(self):
        return self.current_intent or {}
