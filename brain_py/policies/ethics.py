"""
ethics.py
---------
Enforces Tanya’s ethical constraints.
"""

class EthicsPolicy:
    def __init__(self):
        self.rules = [
            "do no harm",
            "follow authority",
            "ask if unsure"
        ]

    def check(self, action: dict) -> bool:
        # Placeholder logic
        return True
