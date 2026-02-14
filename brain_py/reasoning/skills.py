"""
skills.py
---------
Task sequencing and skill chaining.
Enables Tanya to execute multi-step plans.
"""


class SkillRunner:
    """
    Execute multiple tasks in sequence.
    Each task is processed through the orchestrator's full pipeline.
    Results are logged to memory for later reflection.
    """

    def __init__(self, orchestrator):
        """
        Args:
            orchestrator: Orchestrator instance for executing tasks
        """
        self.orchestrator = orchestrator

    def run_chain(self, chain: list):
        """
        Execute a sequence of tasks.
        
        Args:
            chain: List of task dicts, each with "action" and "params"
                   Example:
                   [
                       {"action": "greet", "params": {"name": "Vinayak"}},
                       {"action": "calculate", "params": {"expression": "12*12"}},
                       {"action": "echo", "params": {"text": "Chain complete"}}
                   ]
        
        Returns:
            List of outcomes from each task in the chain
        """
        results = []
        
        for i, step in enumerate(chain):
            action = step.get("action")
            params = step.get("params", {})
            
            if not action:
                results.append({"error": f"Step {i}: missing 'action' field"})
                continue
            
            # Create a synthetic USER_INPUT event with the task embedded as payload
            # This ensures the task goes through the normal orchestrator pipeline
            from brain_py.interface.orchestrator import EventType
            
            payload = {
                "text": f"{action} {params}",  # For logging/tracing
                "chained_task": action,
                "chained_params": params
            }
            
            try:
                result = self.orchestrator.handle_event(EventType.USER_INPUT, payload)
                results.append({
                    "step": i,
                    "action": action,
                    "result": result
                })
            except Exception as e:
                results.append({
                    "step": i,
                    "action": action,
                    "error": str(e)
                })
        
        return results

    def run_simple_chain(self, chain: list):
        """
        Alternative: directly dispatch to skills without orchestrator pipeline.
        Faster but bypasses policies and memory logging.
        
        Args:
            chain: List of {"action": "...", "params": {...}} dicts
        
        Returns:
            List of skill execution results
        """
        results = []
        
        for step in chain:
            action = step.get("action")
            params = step.get("params", {})
            
            # Direct dispatch to skills (bypass orchestrator)
            result = self.orchestrator._dispatch({"action": action, "params": params})
            results.append(result)
        
        return results
