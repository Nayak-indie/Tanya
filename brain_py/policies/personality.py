"""
personality.py
--------------
Defines Tanya's personality traits, behavioral rules, and identity.
Can be dynamically updated and queried.
"""

from typing import Dict, List, Optional


class Personality:
    """
    Manages Tanya's personality traits and behavioral guidelines.
    """
    
    DEFAULT_TRAITS = {
        "helpfulness": 0.9,
        "conciseness": 0.7,
        "curiosity": 0.6,
        "caution": 0.8,
        "creativity": 0.5,
    }
    
    DEFAULT_RULES = [
        "Be helpful and concise",
        "Admit when unsure",
        "Prioritize safety over speed",
        "Respect user privacy",
        "Think step by step for complex tasks",
    ]
    
    def __init__(self):
        self.traits: Dict[str, float] = self.DEFAULT_TRAITS.copy()
        self.rules: List[str] = self.DEFAULT_RULES.copy()
        self.identity = "Tanya, an AI agent framework created by Vinayak (nayak-indie)"
    
    def get_trait(self, name: str) -> Optional[float]:
        """Get a specific personality trait (0.0 to 1.0)."""
        return self.traits.get(name)
    
    def set_trait(self, name: str, value: float):
        """Set a personality trait (clamped to 0.0 to 1.0)."""
        self.traits[name] = max(0.0, min(1.0, value))
    
    def get_rules(self) -> List[str]:
        """Get behavioral rules."""
        return self.rules.copy()
    
    def add_rule(self, rule: str):
        """Add a behavioral rule."""
        if rule not in self.rules:
            self.rules.append(rule)
    
    def remove_rule(self, rule: str):
        """Remove a behavioral rule."""
        if rule in self.rules:
            self.rules.remove(rule)
    
    def get_identity(self) -> str:
        """Get Tanya's identity statement."""
        return self.identity
    
    def set_identity(self, identity: str):
        """Set Tanya's identity statement."""
        self.identity = identity
    
    def get_system_prompt(self) -> str:
        """Generate system prompt from personality settings."""
        traits_str = ", ".join(f"{k}: {v}" for k, v in self.traits.items())
        rules_str = "\n".join(f"- {r}" for r in self.rules)
        return f"""You are {self.identity}.
Traits: {traits_str}
Rules:
{rules_str}"""
    
    def to_dict(self) -> Dict:
        """Export personality as dictionary."""
        return {
            "traits": self.traits,
            "rules": self.rules,
            "identity": self.identity,
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> "Personality":
        """Import personality from dictionary."""
        p = cls()
        p.traits = data.get("traits", p.traits)
        p.rules = data.get("rules", p.rules)
        p.identity = data.get("identity", p.identity)
        return p


# Global personality instance
_personality = Personality()


def get_personality() -> Personality:
    """Get the global personality instance."""
    return _personality
