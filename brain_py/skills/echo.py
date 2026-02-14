"""
echo.py
-------
Skill for echoing text and providing system information.
"""


class Echo:
    """
    Repeats text or returns canned responses.
    """

    def repeat(self, text: str):
        """Echo text back with Tanya signature."""
        return f"Tanya says: {text}"

    def greet(self, name: str = "User"):
        """Greeting response."""
        return f"Hello, {name}! Tanya at your service."

    # Legacy method for backward compatibility
    def info(self) -> dict:
        """
        Provide system information.
        """
        return {
            "status": "success",
            "system_info": {
                "name": "Tanya",
                "version": "0.1.0",
                "description": "Agentic reasoning system with skills",
                "available_skills": ["FileManager", "Calculator", "Echo"]
            }
        }
