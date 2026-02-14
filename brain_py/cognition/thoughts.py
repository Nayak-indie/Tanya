# brain_py/cognition/thoughts.py

class InnerThoughtEngine:
    def __init__(self):
        self.last_thought = None

    def think(self, context: str):
        self.last_thought = f"Analyzing context: {context}"

    def doubt(self, reason: str):
        self.last_thought = f"Uncertainty detected: {reason}"

    def plan(self, goal: str):
        self.last_thought = f"Planning steps to achieve: {goal}"

    def reflect(self):
        return self.last_thought
