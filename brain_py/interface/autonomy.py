"""
autonomy.py
-----------
Phase 8: Goal & Intent reinforced autonomy loop for Tanya.
"""

import time
from brain_py.system.events import EventType

class AutonomyLoop:
    def __init__(self, orchestrator, max_cycles: int = 100, cycle_delay: float = 0.0):
        self.orch = orchestrator
        self.max_cycles = max_cycles
        self.cycle_delay = cycle_delay
        self.cycle_count = 0

    def run(self):
        print("[AUTONOMY] Starting autonomy loop...")
        while self.orch.alive and self.cycle_count < self.max_cycles:
            self.cycle_count += 1
            print(f"\n[AUTONOMY CYCLE {self.cycle_count}]")

            try:
                # Reflection phase
                self._reflection_phase()

                # Reasoning + Intent/Goal alignment
                proposal = self._reasoning_phase()

                # Action execution
                if proposal:
                    self._action_phase(proposal)

                # Optional rate limit
                if self.cycle_delay > 0:
                    time.sleep(self.cycle_delay)

            except Exception as e:
                print(f"[AUTONOMY ERROR] {e}")

        print("[AUTONOMY] Loop finished.")

    # ---------------- PHASES ---------------- #

    def _reflection_phase(self):
        insights = self.orch.reflection.analyze()
        if insights:
            print(f"[REFLECTION] Found {len(insights)} issues.")
        else:
            print("[REFLECTION] No issues detected. Operating normally.")

    def _reasoning_phase(self):
        """Generate next action based on current intent and active goal"""
        intent = self.orch.intent.get_intent()
        goal = self.orch.goals.get_active_goal()

        # If no intent, set default
        if not intent:
            self.orch.intent.set_intent(
                name="INITIALIZE_SYSTEM",
                priority=0.9,
                source="autonomy"
            )
            print("[REASONING] Setting initial intent and greeting user")
            return {"action": "greet", "params": {"name": "Vinayak"}}

        # If intent exists, check goal alignment
        if goal:
            # Example: choose actions that serve the goal
            if goal.is_satisfied():
                print(f"[REASONING] Goal '{goal.name}' completed. Clearing active goal.")
                self.orch.goals.clear_active_goal()
                self.orch.intent.clear_intent()
                return None
            else:
                # Planner chooses action aligned with intent + goal
                task_text = f"Working towards goal: {goal.name}"
                print(f"[REASONING] Acting under intent '{intent['name']}' for goal '{goal.name}'")
                return {"action": "echo", "params": {"text": f"Tanya says: {task_text}"}}

        # No active goal, just follow intent
        print(f"[REASONING] Acting under existing intent '{intent['name']}'")
        return {"action": "echo", "params": {"text": f"Tanya says: Maintaining intent '{intent['name']}'"}}

    def _action_phase(self, proposal):
        """Execute the proposal and reinforce intent/goal"""
        print(f"[ACTION] Executing task: {proposal['action']}")
        result = self.orch._dispatch(proposal)
        print(f"[ACTION] Result: {result}")

        # Log autonomy result + reinforce intent
        self.orch._observe_and_commit(
            EventType.USER_INPUT,
            {"cycle": self.cycle_count, "autonomous": True},
            proposal,
            result
        )

        # Optional: reinforce intent based on success
        self.orch.intent.reinforce_intent(success=True)

    # ---------------- CONTROL ---------------- #

    def pause(self):
        self.orch.alive = False
        print("[AUTONOMY] Pausing autonomy loop.")

    def get_status(self):
        intent = self.orch.intent.get_intent()
        goal = self.orch.goals.get_active_goal()
        summary = self.orch.get_memory_summary()
        return {
            "cycles_completed": self.cycle_count,
            "alive": self.orch.alive,
            "memory_events": summary.get("total_events", 0),
            "current_intent": intent["name"] if intent else None,
            "active_goal": goal.name if goal else None
        }
