"""
background_runner.py
===================
Tanya's 24/7 background operation system.
Runs curiosity, learning, and consolidation loops autonomously.
"""

import time
import threading
from typing import Optional
from brain_py.memory.memory_core import MemoryCore
from brain_py.autonomy.curiosity_loop import CuriosityLoop
from brain_py.skills.skill_learner import SkillLearner
from brain_py.memory.consolidator import MemoryConsolidator


class BackgroundRunner:
    """
    Manages Tanya's autonomous background operations.
    
    Runs three parallel loops:
    1. Curiosity Loop - researches when idle
    2. Consolidation Loop - organizes memory when idle  
    3. Skill Learning - learns new capabilities
    
    All loops run in background threads and don't block the main chat.
    """

    def __init__(
        self, 
        memory: MemoryCore,
        curiosity_interval_minutes: int = 10,
        consolidate_interval_minutes: int = 60,
        ollama_url: str = "http://localhost:11434"
    ):
        self.memory = memory
        self.ollama_url = ollama_url
        
        # Initialize components
        self.curiosity = CuriosityLoop(memory, min_idle_minutes=curiosity_interval_minutes)
        self.skill_learner = SkillLearner(memory)
        self.consolidator = MemoryConsolidator(memory)
        
        # State
        self.running = False
        self.threads = []
        self.log = []

    def start(self):
        """Start all background loops."""
        if self.running:
            return {"status": "already_running"}
        
        self.running = True
        
        # Start background threads
        loops = [
            ("curiosity", self._curiosity_loop, 60),  # Check every 60s
            ("consolidation", self._consolidation_loop, 300),  # Check every 5min
            ("skill_check", self._skill_check_loop, 600),  # Check every 10min
        ]
        
        for name, func, interval in loops:
            t = threading.Thread(target=self._run_loop, args=(name, func, interval), daemon=True)
            t.start()
            self.threads.append(t)
        
        self._log("started", "All background loops started")
        
        return {"status": "started", "loops": ["curiosity", "consolidation", "skill_check"]}

    def stop(self):
        """Stop all background loops."""
        self.running = False
        self._log("stopped", "All background loops stopped")
        return {"status": "stopped"}

    def _run_loop(self, name: str, func, interval: int):
        """Run a loop with sleep."""
        while self.running:
            try:
                if name == "curiosity" and self.curiosity.should_activate():
                    result = func()
                    self._log(name, result)
                elif name == "consolidation" and self.consolidator.should_consolidate():
                    result = func()
                    self._log(name, result)
                elif name == "skill_check":
                    # Check for pending skill requests
                    result = func()
                    if result.get("learned"):
                        self._log(name, result)
            except Exception as e:
                self._log(f"{name}_error", str(e))
            
            time.sleep(interval)

    def _curiosity_loop(self) -> dict:
        """Run curiosity cycle."""
        return self.curiosity.activate(self.ollama_url)

    def _consolidation_loop(self) -> dict:
        """Run memory consolidation."""
        return self.consolidator.consolidate(self.ollama_url)

    def _skill_check_loop(self) -> dict:
        """Check for pending skill learning requests."""
        # Check knowledge gaps
        gaps = self.skill_learner.get_knowledge_gaps()
        
        learned = []
        for gap in gaps[:1]:  # Learn one at a time
            if "request" in gap:
                result = self.skill_learner.learn_and_register(
                    gap["request"], 
                    self.ollama_url
                )
                learned.append(result)
        
        return {"status": "checked", "learned": learned}

    def request_skill_learning(self, description: str) -> dict:
        """Queue a skill for Tanya to learn."""
        gaps = self.memory.recall("knowledge_gaps", [])
        gaps.append({"request": description, "timestamp": time.time()})
        self.memory.remember("knowledge_gaps", gaps)
        
        return {"status": "queued", "request": description}

    def _log(self, event: str, data):
        """Log background activity."""
        entry = {"event": event, "data": data, "timestamp": time.time()}
        self.log.append(entry)
        # Keep last 50 entries
        if len(self.log) > 50:
            self.log = self.log[-50:]

    def get_status(self) -> dict:
        """Return status of all background systems."""
        return {
            "running": self.running,
            "curiosity": self.curiosity.get_status(),
            "consolidator": self.consolidator.get_status(),
            "learned_skills": self.skill_learner.get_learned_skills(),
            "recent_activity": self.log[-5:] if self.log else []
        }

    def trigger_curiosity(self) -> dict:
        """Manually trigger curiosity cycle."""
        return self.curiosity.activate(self.ollama_url)

    def trigger_consolidation(self) -> dict:
        """Manually trigger memory consolidation."""
        return self.consolidator.consolidate(self.ollama_url)
