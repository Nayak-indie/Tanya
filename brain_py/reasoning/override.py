# brain_py/interface/override.py

class UserOverride:
    def __init__(self, orchestrator):
        self.orch = orchestrator

    def interpret(self, text: str) -> bool:
        text = text.lower().strip()

        # ---- STOP / RESUME AUTONOMY ----
        if text in ("stop autonomy", "pause autonomy"):
            self.orch.autonomy.pause()
            return True

        if text in ("resume autonomy", "start autonomy"):
            self.orch.alive = True
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
                return True

        if text in ("clear goal", "remove goal"):
            self.orch.goals.clear_active_goal()
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
                return True

        # ---- INTROSPECTION ----
        if text in ("what is your goal", "current goal"):
            goal = self.orch.goals.get_active_goal()
            if goal:
                print(f"[GOAL] Active goal: {goal.name}")
            else:
                print("[GOAL] No active goal.")
            return True

        return False
