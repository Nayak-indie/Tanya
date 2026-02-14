"""
skills/
-------
Tanya's available skills and capabilities.
Each skill is a module implementing specific functionality.
"""

from brain_py.skills.file_manager import FileManager
from brain_py.skills.calculator import Calculator
from brain_py.skills.echo import Echo

__all__ = ["FileManager", "Calculator", "Echo"]
