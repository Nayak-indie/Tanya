"""
intent.py
---------
Represents Tanya's current cognitive intent.
Intent is short-term, focused, and replaceable.
"""

import datetime
from typing import Optional, Dict, Any


class IntentModel:
    def __init__(self):
        self.current_intent: Optional[Dict[str, Any]] = None

    def set_intent(self, name: str, priority: float = 0.5, source: str = "system"):
        """
        Set or replace the current intent.
        """
        self.current_intent = {
            "name": name.upper(),
            "priority": float(priority),
            "source": source,
            "created_at": str(datetime.datetime.now())
        }

    def clear_intent(self):
        """Clear current intent."""
        self.current_intent = None

    def has_intent(self) -> bool:
        return self.current_intent is not None

    def get_intent(self) -> Optional[Dict[str, Any]]:
        return self.current_intent

    def summarize(self) -> Dict[str, Any]:
        """
        Lightweight summary for autonomy / planner.
        """
        if not self.current_intent:
            return {"active": False}

        return {
            "active": True,
            "name": self.current_intent["name"],
            "priority": self.current_intent["priority"],
            "source": self.current_intent["source"]
        }

    def boost_priority(self, amount: float):
        """Boost the current intent's priority by a small amount."""
        if self.current_intent:
            self.current_intent["priority"] = min(1.0, self.current_intent["priority"] + amount)
