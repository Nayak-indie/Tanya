"""
curiosity_loop.py
=================
Tanya's curiosity-driven exploration system.
Researches topics, learns proactively, stays engaged when idle.
"""

import time
import random
from typing import Optional
from brain_py.memory.memory_core import MemoryCore


class CuriosityLoop:
    """
    Proactive learning loop - Tanya explores when idle.
    
    Triggers:
    - User inactivity (no chat for X minutes)
    - Scheduled intervals
    - After processing interesting user queries
    
    Actions:
    - Research topics from memory
    - Explore new domains
    - Learn new skills
    - Self-reflect
    """

    DEFAULT_TRIGGERS = [
        "What is {topic}?",
        "Explain {topic} in simple terms",
        "Latest developments in {topic}",
        "How does {topic} work?",
    ]

    # Topics to explore based on user interests
    INTEREST_CLUSTERS = [
        "AI agents", "LLM optimization", "automation",
        "productivity", "programming", "self-improvement"
    ]

    def __init__(self, memory: MemoryCore, min_idle_minutes: int = 5):
        self.memory = memory
        self.min_idle_minutes = min_idle_minutes
        self.last_activity = time.time()
        self.is_active = False
        self.research_queue = []

    def update_activity(self):
        """Call when user interacts."""
        self.last_activity = time.time()
        self.is_active = False

    def should_activate(self) -> bool:
        """Check if curiosity should trigger."""
        idle_minutes = (time.time() - self.last_activity) / 60
        return idle_minutes >= self.min_idle_minutes and not self.is_active

    def extract_topics_from_memory(self) -> list[str]:
        """Extract topics user cares about from memory."""
        events = self.memory.recall("events", [])
        conversations = self.memory.recall("conversations", [])
        
        topics = set()
        
        # Extract from events
        for event in events[-20:]:  # Recent 20
            if "task" in event:
                topics.add(str(event["task"]))
        
        # Extract from conversations
        for conv in conversations[-10:]:
            if "text" in conv:
                # Simple keyword extraction (enhance later)
                words = conv["text"].lower().split()
                for word in words:
                    if len(word) > 5:
                        topics.add(word)
        
        return list(topics)[:5]

    def generate_research_questions(self) -> list[str]:
        """Generate questions to research."""
        topics = self.extract_topics_from_memory()
        
        if not topics:
            topics = self.INTEREST_CLUSTERS
        
        questions = []
        for topic in topics[:3]:
            template = random.choice(self.DEFAULT_TRIGGERS)
            questions.append(template.format(topic=topic))
        
        return questions

    def activate(self, ollama_url: str = "http://localhost:11434") -> dict:
        """
        Main curiosity activation - research and learn.
        Returns discovery results.
        """
        self.is_active = True
        discoveries = []

        try:
            questions = self.generate_research_questions()
            
            for question in questions:
                # Use local LLM to "think" about this
                answer = self._query_local_model(question, ollama_url)
                
                if answer:
                    discoveries.append({
                        "question": question,
                        "insight": answer[:500],  # Truncate
                        "timestamp": time.time()
                    })
                    
                    # Store as learning
                    learnings = self.memory.recall("curiosity_learnings", [])
                    learnings.append({"question": question, "answer": answer[:500]})
                    self.memory.remember("curiosity_learnings", learnings)

        finally:
            self.is_active = False
            self.last_activity = time.time()  # Reset to avoid immediate re-trigger

        return {
            "status": "curiosity_cycle_complete",
            "discoveries": discoveries,
            "topics_researched": len(discoveries)
        }

    def _query_local_model(self, prompt: str, ollama_url: str) -> Optional[str]:
        """Query local Ollama model."""
        import requests
        
        try:
            response = requests.post(
                f"{ollama_url}/api/generate",
                json={
                    "model": "llama3.1:8b",  # Or configured model
                    "prompt": f"You are Tanya, a curious AI assistant. {prompt}",
                    "stream": False
                },
                timeout=30
            )
            if response.status_code == 200:
                return response.json().get("response", "").strip()
        except Exception as e:
            print(f"[Curiosity] Model query failed: {e}")
        
        return None

    def get_status(self) -> dict:
        """Return current curiosity state."""
        idle_minutes = (time.time() - self.last_activity) / 60
        return {
            "is_active": self.is_active,
            "idle_minutes": round(idle_minutes, 1),
            "should_activate": self.should_activate(),
            "pending_research": len(self.research_queue)
        }
