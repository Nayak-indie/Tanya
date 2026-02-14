"""
goals.py
--------
Long-term goal store for Tanya.
Tracks active goals, progress, and completion.
"""

class GoalStore:
    def __init__(self):
        self.active_goal = None
        self.completed_goals = []

    def set_goal(self, name: str, priority: float = 0.5, source: str = "system"):
        self.active_goal = {
            "name": name,
            "priority": priority,
            "source": source,
            "progress": 0.0
        }
        print(f"[GOALS] Set active goal: {name} (priority {priority}, source {source})")

    def clear_active_goal(self):
        if self.active_goal:
            self.completed_goals.append(self.active_goal)
            print(f"[GOALS] Completed goal: {self.active_goal['name']}")
        self.active_goal = None

    def get_active_goal(self):
        return self.active_goal

    def update_progress(self, amount: float):
        if self.active_goal:
            self.active_goal["progress"] += amount
            print(f"[GOALS] Updated progress for {self.active_goal['name']}: {self.active_goal['progress']*100:.1f}%")
            if self.active_goal["progress"] >= 1.0:
                self.clear_active_goal()
