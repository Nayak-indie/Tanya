"""
rust_bridge.py
---------------
Handles communication with Tanya's Rust core.
Provides fast skill execution, memory operations, and reasoning.
"""

import os
import json
import subprocess
from typing import Dict, Any, Optional


class RustBridge:
    """
    Bridge to Tanya's Rust core backend.
    Provides high-performance alternatives to Python implementations.
    """
    
    def __init__(self, core_path: Optional[str] = None):
        """
        Initialize the Rust bridge.
        
        Args:
            core_path: Path to the compiled Tanya core binary.
                      If None, tries default locations.
        """
        self.core_path = core_path or self._find_core()
        self.available = self.core_path is not None and os.path.exists(self.core_path)
    
    def _find_core(self) -> Optional[str]:
        """Find the compiled core binary."""
        # Check common locations
        paths = [
            "./core_rust/target/debug/tanya-core",
            "./target/debug/tanya-core",
            os.path.expanduser("~/Tanya/core_rust/target/debug/tanya-core"),
        ]
        for path in paths:
            if os.path.exists(path):
                return path
        return None
    
    def is_available(self) -> bool:
        """Check if Rust core is available."""
        return self.available
    
    def send_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send a task to the Rust core.
        
        Args:
            task: Dict with 'action' and 'params'
        
        Returns:
            Result dict from the core
        """
        if not self.available:
            return {"status": "unavailable", "result": "Rust core not compiled"}
        
        try:
            # For now, support basic commands via stdin/stdout
            action = task.get("action", "")
            
            if action == "echo":
                text = task.get("params", {}).get("text", "")
                result = subprocess.run(
                    [self.core_path],
                    input=f"echo {text}\nquit\n",
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                return {"status": "done", "result": result.stdout}
            
            elif action == "list_skills":
                result = subprocess.run(
                    [self.core_path],
                    input="list\nquit\n",
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                return {"status": "done", "result": result.stdout}
            
            return {"status": "unsupported", "result": f"Action '{action}' not implemented in Rust core"}
        
        except subprocess.TimeoutExpired:
            return {"status": "fail", "result": "Core execution timeout"}
        except Exception as e:
            return {"status": "fail", "result": str(e)}
    
    def execute_skill(self, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a skill via Rust core."""
        return self.send_task({"action": action, "params": params})
    
    def get_status(self) -> Dict[str, Any]:
        """Get Rust core status."""
        return {
            "available": self.available,
            "path": self.core_path,
            "version": "0.1.0"
        }


# Global bridge instance
_bridge: Optional[RustBridge] = None


def get_bridge() -> RustBridge:
    """Get the global Rust bridge instance."""
    global _bridge
    if _bridge is None:
        _bridge = RustBridge()
    return _bridge
