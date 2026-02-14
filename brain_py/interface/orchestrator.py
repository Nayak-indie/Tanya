from brain_py.interface.autonomy import AutonomyLoop
from brain_py.reasoning.intent import IntentModel
from brain_py.memory.goals import GoalStore
from brain_py.interface.override import UserOverride
from brain_py.system.events import EventType
from brain_py.skills.skills import SkillStore
from brain_py.reasoning.planner import Planner
from brain_py.memory.memory_core import MemoryCore
import time
import os

class Orchestrator:
    def __init__(self, memory: MemoryCore):
        self.alive = True
        self.intent = IntentModel()
        self.goals = GoalStore()
        self.override = UserOverride(self)
        self.autonomy = AutonomyLoop(self)
        self.memory = memory
        self.reflection = self  # placeholder for now
        self.skills = SkillStore()
        self.planner = Planner(self)
        from brain_py.skills.user_model import UserModel
        from brain_py.skills.auto_self_improver import analyze_and_update_prompt
        self.user_model = UserModel()
        self.analyze_and_update_prompt = analyze_and_update_prompt
        # Tanya's self-concept: identity statement (keeps consistent with system prompt)
        self.self_concept = (
            "I am Tanya, your assistant created by Vinayak (nayak-indie). "
            "I am helpful, concise, and can inspect files, run local tools, and reason about code and tasks. "
            "If I'm unsure, I'll say so and propose a clear next step."
        )

    # ---------------- MEMORY ---------------- #
    def _observe_and_commit(self, event_type, metadata, task, result):
        events = self.memory.recall("events", [])
        events.append({
            "event": event_type.value if hasattr(event_type, 'value') else str(event_type),
            "metadata": metadata,
            "task": task,
            "result": result,
            "timestamp": time.time()
        })
        self.memory.remember("events", events)

    def get_memory_summary(self):
        events = self.memory.recall("events", [])
        return {"total_events": len(events)}

    # ---------------- REFLECTION ---------------- #
    def analyze(self):
        # Placeholder reflection: always return empty for now
        return []

    # ---------------- DISPATCH ---------------- #
    def _dispatch(self, task):
        action = task.get("action")
        params = task.get("params", {})

        # If action is a goal, run planner
        if action == "execute_goal":
            goal_name = params.get("goal_name")
            tasks = self.planner.plan_for_goal(goal_name)
            results = []
            for t in tasks:
                result = self.skills.execute(self, t["action"], t.get("params", {}))
                results.append(result)
                self._observe_and_commit("GOAL_TASK", {"goal": goal_name}, t, result)
            return {"status": "done", "result": results}

        # otherwise normal skill execution
        # Special: allow self-edit via chat command
        if action == "self.edit":
            return self.skills.execute(self, action, params)
        return self.skills.execute(self, action, params)

    # ---------------- USER OVERRIDE ---------------- #
    def handle_override(self, text: str) -> bool:
        return self.override.interpret(text)

    # ---------------- EVENT HANDLER ---------------- #

    def handle_event(self, event_type, payload=None):
        # For simplicity, treat payload as dict

        if event_type == EventType.USER_INPUT and payload:
            text = payload.get("text", "")
            # Predict satisfaction and learn preferences
            if any(word in text.lower() for word in ["like", "prefer", "love", "hate", "dislike"]):
                self.user_model.add_preference(text)
            # Try to route to a skill if possible
            # If file access is granted and the user asks about project/folder structure, list files
            grant = os.getenv("TANYA_GRANT_FILE_ACCESS", "false").lower() in ("1", "true", "yes")
            file_query_triggers = ["file structure", "folder structure", "project structure", "list files", "tree", "what files", "show files", "directory listing"]
            if grant and any(trigger in text.lower() for trigger in file_query_triggers):
                try:
                    # use file_manager skill to list repo root
                    result = self.skills.execute(self, "file.list", {"directory": "."})
                    self.analyze_and_update_prompt([{"user": text, "reply": result.get("result", str(result))}])
                    return result
                except Exception as e:
                    return {"status": "fail", "result": f"File access error: {e}"}

            for skill in self.skills.skills:
                if skill.replace("_", " ") in text.lower() or skill in text.lower():
                    # Extract params (very basic, can be improved)
                    params = {"text": text}
                    result = self.skills.execute(self, skill, params)
                    self.analyze_and_update_prompt([{"user": text, "reply": result.get("result", str(result))}])
                    return result
            if self.handle_override(text):
                return {"status": "done", "message": "User override executed."}
            if text.lower().startswith("edit self:"):
                try:
                    _, rest = text.split(":", 1)
                    file, code = rest.strip().split(" ", 1)
                    return self.skills.execute(self, "self.edit", {"file": file, "code": code})
                except Exception as e:
                    return {"status": "fail", "result": f"Invalid self-edit command: {e}"}
            # Force Tanya's identity for self/identity/name questions
            identity_triggers = [
                "who are you", "what is your name", "tell me about yourself", "your identity", "about yourself", "who r u", "who you are"
            ]
            if any(trigger in text.lower() for trigger in identity_triggers):
                # Reflect on Tanya's self-concept
                return {"status": "done", "result": self.self_concept}
            if text.lower() in ("explain yourself", "what did you just do", "what did you learn"):
                return self.skills.execute(self, "self.explain", {})
            # Otherwise, use LLM for general chat and fallback
            from brain_py.skills.mixtral_client import send_message as mixtral_send
            try:
                messages = [{"role": "user", "content": text}]
                reply = mixtral_send(messages)
            except Exception as e:
                return {"status": "fail", "result": f"Mixtral error: {e}"}
            # Let Tanya self-improve (feedback handled in chat loop)
            self.analyze_and_update_prompt([{"user": text, "reply": reply}])
            return {"status": "done", "result": reply}

        elif event_type == EventType.SYSTEM_BOOT:
            return {"status": "done", "result": "Hello, Vinayak! Tanya at your service."}

        elif event_type == EventType.SYSTEM_SHUTDOWN:
            self.alive = False
            return {"status": "done", "result": "System shutting down."}

        elif event_type == EventType.MEMORY_WRITE and payload:
            text = payload.get("text", "")
            memories = self.memory.recall("user_memories", [])
            memories.append({"event": "USER_MEMORY", "data": text, "timestamp": time.time()})
            self.memory.remember("user_memories", memories)
            return {"status": "done", "result": f"I will remember: {text}"}

        return {"status": "noop", "message": "No task proposed."}
