"""
skills.py
---------
Define Tanya's skills as modular, callable units.
Skills are mapped to actions/tasks.

Also integrates with brain_py.core.skill_registry for auto-discovery,
documentation generation, and validation.
"""

# Import registry for integration
from brain_py.core.skill_registry import get_registry, register_skill


class SkillStore:
    def _self_explain(self, orchestrator, params):
        """
        Explains Tanya's last action or what she learned recently.
        """
        events = getattr(orchestrator, 'memory', None)
        feedback = None
        if events:
            events_list = orchestrator.memory.recall("events", [])
            feedback = orchestrator.memory.recall("feedback", [])
            if events_list:
                last_event = events_list[-1]
                action = last_event.get("task", {}).get("action", "something")
                result = last_event.get("result", {})
                return {"status": "done", "result": f"I just performed '{action}'. Result: {result}"}
            elif feedback:
                last_feedback = feedback[-1]
                return {"status": "done", "result": f"You rated my last response as '{last_feedback['rating']}'."}
        return {"status": "done", "result": "I haven't done anything notable yet."}

    def __init__(self):
        # Predefined skills
        from brain_py.skills.file_manager import FileManager
        self.file_manager = FileManager()
        from brain_py.skills import retrain_model
        self.skills = {
            "greet": self._greet,
            "echo": self._echo,
            "memory.write": self._memory_write,
            "memory.recall": self._memory_recall,
            "skill.describe": self._describe_skills,
            "self.edit": self._self_edit,
            "self.explain": self._self_explain,
            "self.learn": self._self_learn,
            "file.create": lambda o, p: self.file_manager.create_file(p.get("path"), p.get("content", "")),
            "file.edit": lambda o, p: self.file_manager.edit_file(p.get("path"), p.get("content", "")),
            "file.delete": lambda o, p: self.file_manager.delete_file(p.get("path")),
            "file.list": lambda o, p: self.file_manager.list_files(p.get("directory", ".")),
            "file.read": lambda o, p: self.file_manager.read_file(p.get("path")),
            "model.retrain": lambda o, p: retrain_model.retrain_model(),
        }


    def _self_learn(self, orchestrator, params):
        """
        Tanya learns and self-edits based on user feedback and conversation.
        params: {"feedback": str, "code": str (optional)}
        """
        feedback = params.get("feedback")
        code = params.get("code")
        if feedback:
            # Store feedback in memory
            memory = getattr(orchestrator, 'memory', None)
            if memory:
                feedback_list = memory.recall("feedback", [])
                feedback_list.append({"feedback": feedback})
                memory.remember("feedback", feedback_list)
        if code:
            # Self-edit: append code to her own module
            try:
                with open(__file__, "a", encoding="utf-8") as f:
                    f.write("\n# Tanya self-learned:\n" + code + "\n")
                return {"status": "done", "result": "Tanya updated her code based on feedback."}
            except Exception as e:
                return {"status": "fail", "result": f"Self-edit error: {e}"}
        return {"status": "done", "result": "Tanya learned from feedback."}


    # All external API skills removed. Only local LLM (Ollama/GGUF) supported.



    def _synthesize_human(self, text1, text2):
        # Remove explicit AI labels, blend for a natural response
        t1 = text1.strip().replace('ChatGPT:', '').replace('Gemini:', '').strip()
        t2 = text2.strip().replace('ChatGPT:', '').replace('Gemini:', '').strip()
        if t1 == t2:
            return t1
        # Prefer the longer, more informative answer, or join if both are short
        if len(t1) > 100 and len(t2) > 100:
            return f"{t1}\n\n{t2}"
        if len(t1) > len(t2):
            return t1
        if len(t2) > len(t1):
            return t2
        return f"{t1}\n\n{t2}"

    def _self_edit(self, orchestrator, params):
        """
        Allows Tanya to append code or data to her own modules when instructed by the user.
        params: {"file": str, "code": str}
        """
        file = params.get("file")
        code = params.get("code")
        if not file or not code:
            return {"status": "fail", "result": "Missing file or code parameter."}
        try:
            with open(file, "a", encoding="utf-8") as f:
                f.write("\n" + code + "\n")
            return {"status": "done", "result": f"Appended code to {file}."}
        except Exception as e:
            return {"status": "fail", "result": f"Error editing {file}: {e}"}

    # ---------------- SKILL IMPLEMENTATIONS ---------------- #
    def _greet(self, orchestrator, params):
        name = params.get("name", "User")
        return {"status": "done", "result": f"Hello, {name}! Tanya at your service."}

    def _echo(self, orchestrator, params):
        text = params.get("text", "")
        return {"status": "done", "result": f"Tanya says: {text}"}

    def _memory_write(self, orchestrator, params):
        text = params.get("text", "")
        orchestrator._memory.append({"event": "USER_MEMORY", "data": text})
        return {"status": "done", "result": f"I will remember: {text}"}

    def _memory_recall(self, orchestrator, params):
        query = params.get("query", "").lower()
        matches = [m["data"] for m in orchestrator._memory if "data" in m and query in m["data"].lower()]
        if matches:
            return {"status": "done", "result": "\n".join(matches)}
        return {"status": "done", "result": f"I don't remember anything matching '{query}'."}

    def _describe_skills(self, orchestrator, params):
        return {"status": "done", "result": "\n".join(self.skills.keys())}

    # ---------------- SKILL DISPATCH ---------------- #
    def execute(self, orchestrator, action, params):
        if action in self.skills:
            return self.skills[action](orchestrator, params)
        return {"status": "fail", "result": f"No skill found for action '{action}'."}

    # ---------------- REGISTRY INTEGRATION ---------------- #
    def sync_to_registry(self):
        """Sync all skills to the global registry for auto-discovery."""
        registry = get_registry()
        for action, method in self.skills.items():
            # Try to get description from method's docstring
            desc = method.__doc__.strip().split('\n')[0] if method.__doc__ else ""
            registry.register(
                skill_name=self.__class__.__name__,
                action_name=action,
                method=method,
                description=desc
            )
        return registry

    def get_skill_docs(self) -> str:
        """Get auto-generated documentation for all skills."""
        registry = get_registry()
        # First sync to ensure registry is up to date
        self.sync_to_registry()
        return registry.generate_skill_docs()

    def validate_skills(self) -> bool:
        """Validate all registered skills are callable."""
        registry = get_registry()
        self.sync_to_registry()
        return registry.validate()
