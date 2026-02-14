"""
skill_registry.py
-----------------
Dynamic skill registration and discovery system.
Automatically adapts the codebase when new skills are added.
"""

import inspect
import importlib
from typing import Dict, Callable, Any


class SkillRegistry:
    """
    Central registry for all Tanya skills.
    Auto-discovers and manages skills, keeping the codebase in sync.
    """

    def __init__(self):
        self.skills: Dict[str, Dict[str, Any]] = {}
        self.skill_methods: Dict[str, Callable] = {}

    def register(self, skill_name: str, action_name: str, method: Callable, 
                 params: list = None, description: str = ""):
        """
        Register a skill with the system.
        
        Args:
            skill_name: Name of the skill class (e.g., "echo", "calculator")
            action_name: Name of the action/command (e.g., "echo", "calculate")
            method: The callable method to execute
            params: List of required parameter names
            description: Human-readable description
        """
        key = f"{skill_name}.{action_name}"
        self.skills[action_name] = {
            "skill": skill_name,
            "action": action_name,
            "method": method,
            "params": params or [],
            "description": description
        }
        self.skill_methods[action_name] = method
        print(f"[REGISTRY] Registered skill: {action_name}")
    


    def get_skill(self, action_name: str) -> Callable:
        """Get a registered skill method by action name."""
        return self.skill_methods.get(action_name)

    def list_skills(self) -> Dict[str, Dict]:
        """Return all registered skills."""
        return self.skills.copy()

    def get_planner_mappings(self) -> Dict[str, str]:
        """
        Generate keyword → action mappings for the Planner.
        Dynamically creates command keywords based on registered skills.
        """
        mappings = {}
        for action_name, skill_info in self.skills.items():
            # Create keyword variations
            keywords = [action_name, action_name[:3]]  # Full name + abbreviation
            for keyword in keywords:
                mappings[keyword] = action_name
        return mappings

    def get_dispatch_config(self) -> Dict[str, Callable]:
        """
        Generate dispatch routing table.
        Can be used by orchestrator._dispatch() for routing.
        """
        return self.skill_methods.copy()

    def validate(self) -> bool:
        """
        Validate that all registered skills are callable.
        """
        for action, method in self.skill_methods.items():
            if not callable(method):
                print(f"[REGISTRY ERROR] {action} is not callable")
                return False
        return True

    def generate_skill_docs(self) -> str:
        """
        Auto-generate documentation for all registered skills.
        """
        docs = "# Available Skills\n\n"
        for action_name, skill_info in self.skills.items():
            docs += f"## {action_name.upper()}\n"
            docs += f"Description: {skill_info.get('description', 'N/A')}\n"
            params = skill_info.get('params', [])
            if params:
                docs += f"Parameters: {', '.join(params)}\n"
            docs += "\n"
        return docs


# Global registry instance
_registry = SkillRegistry()


def get_registry() -> SkillRegistry:
    """Get the global skill registry."""
    return _registry


def register_skill(skill_name: str, action_name: str, params: list = None, description: str = ""):
    """
    Decorator for registering skills.
    
    Usage:
        @register_skill("echo", "echo", params=["text"], description="Repeat text")
        def echo_skill(text: str):
            return f"Echo: {text}"
    """
    def decorator(func: Callable) -> Callable:
        _registry.register(skill_name, action_name, func, params, description)
        return func
    return decorator
