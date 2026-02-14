"""
calculator.py
--------------
Skill for simple mathematical operations.
"""


class Calculator:
    """
    Simple math evaluation skill.
    WARNING: eval() is used — only for trusted input.
    """

    def calculate(self, expression: str):
        """
        Evaluate a mathematical expression.
        """
        try:
            result = eval(expression, {"__builtins__": {}})
            return f"{expression} = {result}"
        except Exception as e:
            return f"Error calculating expression: {e}"

    # Legacy individual methods for backward compatibility
    def add(self, a: float, b: float) -> dict:
        """Add two numbers."""
        return {"operation": "add", "a": a, "b": b, "result": a + b}

    def subtract(self, a: float, b: float) -> dict:
        """Subtract b from a."""
        return {"operation": "subtract", "a": a, "b": b, "result": a - b}

    def multiply(self, a: float, b: float) -> dict:
        """Multiply two numbers."""
        return {"operation": "multiply", "a": a, "b": b, "result": a * b}

    def divide(self, a: float, b: float) -> dict:
        """Divide a by b."""
        if b == 0:
            return {"operation": "divide", "a": a, "b": b, "error": "Division by zero"}
        return {"operation": "divide", "a": a, "b": b, "result": a / b}

    def power(self, base: float, exponent: float) -> dict:
        """Raise base to the power of exponent."""
        return {"operation": "power", "base": base, "exponent": exponent, "result": base ** exponent}

