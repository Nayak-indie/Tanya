"""
consolidator.py
===============
Memory consolidation system - Tanya reflects and organizes thoughts when idle.
Summarizes conversations, extracts patterns, deepens understanding.
"""

import time
from typing import Optional
from brain_py.memory.memory_core import MemoryCore


class MemoryConsolidator:
    """
    Idle-time memory processing.
    
    What it does:
    - Summarizes recent conversations
    - Extracts user preferences/patterns
    - Deepens important memories
    - Prunes old/unnecessary data
    - Generates insights
    """

    def __init__(self, memory: MemoryCore):
        self.memory = memory
        self.last_consolidation = time.time()
        self.consolidation_interval = 3600  # 1 hour

    def should_consolidate(self) -> bool:
        """Check if it's time to consolidate."""
        return (time.time() - self.last_consolidation) > self.consolidation_interval

    def consolidate(self, ollama_url: str = "http://localhost:11434") -> dict:
        """
        Run full memory consolidation cycle.
        """
        results = {
            "summaries": [],
            "patterns": [],
            "insights": [],
            "pruned": 0
        }

        # 1. Summarize recent conversations
        summary = self._summarize_conversations(ollama_url)
        if summary:
            results["summaries"].append(summary)
            # Store summary
            summaries = self.memory.recall("conversation_summaries", [])
            summaries.append({"summary": summary, "timestamp": time.time()})
            self.memory.remember("conversation_summaries", summaries[-10:])  # Keep last 10

        # 2. Extract patterns
        patterns = self._extract_patterns()
        results["patterns"] = patterns

        # 3. Generate insights
        insights = self._generate_insights(ollama_url)
        results["insights"] = insights
        
        # Store insights
        stored_insights = self.memory.recall("insights", [])
        stored_insights.extend(insights)
        self.memory.remember("insights", stored_insights[-20:])

        # 4. Prune old data
        results["pruned"] = self._prune_old_data()

        self.last_consolidation = time.time()

        return results

    def _summarize_conversations(self, ollama_url: str) -> Optional[str]:
        """Summarize recent conversation history."""
        import requests
        
        conversations = self.memory.recall("conversations", [])
        
        if not conversations:
            return None
        
        # Get last 10 conversations
        recent = conversations[-10:]
        text = "\n".join([
            f"User: {c.get('user', '')}\nTanya: {c.get('assistant', '')}"
            for c in recent
        ])
        
        prompt = f"""Summarize this conversation briefly (2-3 sentences):
{text}

Focus on: What did the user want? What did we accomplish?"""

        try:
            response = requests.post(
                f"{ollama_url}/api/generate",
                json={
                    "model": "llama3.1:8b",
                    "prompt": prompt,
                    "stream": False
                },
                timeout=30
            )
            if response.status_code == 200:
                return response.json().get("response", "").strip()
        except Exception as e:
            print(f"[Consolidator] Summary failed: {e}")
        
        return None

    def _extract_patterns(self) -> list[dict]:
        """Extract patterns from memory."""
        patterns = []
        
        # Extract from events
        events = self.memory.recall("events", [])
        feedback = self.memory.recall("feedback", [])
        
        # Analyze feedback patterns
        if feedback:
            good = sum(1 for f in feedback if f.get("rating") == "good")
            bad = sum(1 for f in feedback if f.get("rating") == "bad")
            boring = sum(1 for f in feedback if f.get("rating") == "boring")
            
            patterns.append({
                "type": "feedback",
                "good": good,
                "bad": bad,
                "boring": boring,
                "total": len(feedback)
            })

        # Analyze topic frequency
        topics = {}
        for event in events:
            if "task" in event:
                task = str(event["task"])
                topics[task] = topics.get(task, 0) + 1
        
        if topics:
            patterns.append({
                "type": "topics",
                "top": sorted(topics.items(), key=lambda x: -x[1])[:5]
            })

        return patterns

    def _generate_insights(self, ollama_url: str) -> list[str]:
        """Generate deeper insights from memory."""
        import requests
        
        insights = []
        
        # Get recent learnings
        learnings = self.memory.recall("curiosity_learnings", [])
        skill_learnings = self.memory.recall("skill_learnings", [])
        
        if not learnings and not skill_learnings:
            return insights
        
        # Build context
        context = []
        for l in learnings[-5:]:
            if "question" in l:
                context.append(f"Q: {l['question']}")
        for sl in skill_learnings[-3:]:
            if "skill" in sl:
                context.append(f"Learned: {sl['skill']}")
        
        if not context:
            return insights
        
        prompt = f"""Based on what Tanya recently learned, generate 1-2 actionable insights:

{chr(10).join(context)}

What should Tanya remember or do differently?"""

        try:
            response = requests.post(
                f"{ollama_url}/api/generate",
                json={
                    "model": "llama3.1:8b",
                    "prompt": prompt,
                    "stream": False
                },
                timeout=30
            )
            if response.status_code == 200:
                result = response.json().get("response", "").strip()
                if result:
                    insights.append(result)
        except Exception as e:
            print(f"[Consolidator] Insight generation failed: {e}")

        return insights

    def _prune_old_data(self) -> int:
        """Remove old/unnecessary data."""
        pruned = 0
        
        # Prune old events (keep last 100)
        events = self.memory.recall("events", [])
        if len(events) > 100:
            self.memory.remember("events", events[-100:])
            pruned += len(events) - 100
        
        # Prune old conversations (keep last 50)
        conversations = self.memory.recall("conversations", [])
        if len(conversations) > 50:
            self.memory.remember("conversations", conversations[-50:])
            pruned += len(conversations) - 50
        
        return pruned

    def get_status(self) -> dict:
        """Return consolidator status."""
        return {
            "last_consolidation": self.last_consolidation,
            "should_consolidate": self.should_consolidate(),
            "interval_hours": self.consolidation_interval / 3600
        }
