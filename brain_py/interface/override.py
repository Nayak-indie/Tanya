"""
override.py
-----------
User override interpreter for Tanya.
Maps natural language → intent / goal / autonomy control.
"""

class UserOverride:
    def __init__(self, orchestrator):
        self.orch = orchestrator

    def interpret(self, text: str) -> bool:
        """
        Returns True if override was handled.
        """

        text = text.lower().strip()

        # ---- STOP / RESUME AUTONOMY ----
        if text in ("stop autonomy", "pause autonomy"):
            if self.orch.autonomy:
                self.orch.autonomy.pause()
                print("[OVERRIDE] Autonomy paused by user.")
            else:
                print("[AUTONOMY] No autonomy loop active.")
            return True

        if text in ("resume autonomy", "start autonomy"):
            self.orch.alive = True
            print("[OVERRIDE] Autonomy resumed by user.")
            return True

        # ---- GOAL COMMANDS ----
        if text.startswith("set goal"):
            goal_name = text.replace("set goal", "").strip()
            if goal_name:
                self.orch.goals.set_goal(
                    name=goal_name.upper(),
                    priority=0.8,
                    source="user"
                )
                print(f"[OVERRIDE] Goal set by user: {goal_name.upper()}")
                return True

        if text in ("clear goal", "remove goal"):
            self.orch.goals.clear_active_goal()
            print("[OVERRIDE] Active goal cleared by user.")
            return True

        # ---- INTENT FOCUS ----
        if text.startswith("focus on"):
            intent_name = text.replace("focus on", "").strip()
            if intent_name:
                self.orch.intent.set_intent(
                    name=intent_name.upper(),
                    priority=0.7,
                    source="user"
                )
                print(f"[OVERRIDE] Intent focused by user: {intent_name.upper()}")
                return True

        # ---- INTROSPECTION ----
        if text in ("what is your goal", "current goal"):
            goal = self.orch.goals.get_active_goal()
            if goal:
                print(f"[GOAL] Active goal: {goal.name}")
            else:
                print("[GOAL] No active goal.")
            return True

        if text in ("current intent", "what is your intent"):
            intent = self.orch.intent.get_intent()
            if intent:
                print(f"[INTENT] Current intent: {intent['name']}")
            else:
                print("[INTENT] No current intent set.")
            return True

        return False
