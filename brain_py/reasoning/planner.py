"""
planner.py
----------
Convert goals + intent → actionable task sequences.
"""

class Planner:
    def __init__(self, orchestrator):
        self.orch = orchestrator

    def plan_for_goal(self, goal_name):
        """
        Return a list of tasks for a given goal.
        Each task is a dict: {"action": str, "params": dict}
        """
        goal_name = goal_name.lower()

        if goal_name == "learn me":
            return [
                {"action": "greet", "params": {"name": "Vinayak"}},
                {"action": "echo", "params": {"text": "Starting your learning session!"}},
                {"action": "memory.write", "params": {"text": "Learning session started"}}
            ]

        if goal_name == "focus on memory":
            return [
                {"action": "memory.recall", "params": {"query": ""}}
            ]

        # default fallback
        return [{"action": "echo", "params": {"text": f"Executing goal: {goal_name}"}}]
