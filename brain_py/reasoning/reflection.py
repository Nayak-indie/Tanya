"""
reflection.py
--------------
Analyze past actions and outcomes to identify patterns and lessons.
Enables Tanya to learn and adapt her future proposals.
"""


class Reflection:
    """
    Analyze past actions and outcomes.
    Helps Tanya learn from memory.
    """

    def __init__(self, memory, review_limit=10):
        """
        Args:
            memory: MemoryStore instance for accessing persistent memory
            review_limit: How many recent events to review (default 10)
        """
        self.memory = memory
        self.review_limit = review_limit

    def review_recent(self):
        """
        Returns recent events for reflection analysis.
        """
        return self.memory.recall_recent(n=self.review_limit)

    def analyze(self):
        """
        Simple reflection: detect failed tasks, errors, or patterns.
        Returns list of insights about what went wrong.
        """
        recent = self.review_recent()
        insights = []
        
        for record in recent:
            outcome = record.get("outcome", {})
            event = record.get("event", "unknown")
            
            # Detect failed outcomes
            if isinstance(outcome, dict):
                if outcome.get("status") == "failed" or outcome.get("status") == "error":
                    insights.append({
                        "type": "failure",
                        "event": event,
                        "problem": outcome.get("reason", outcome.get("message", "unknown error")),
                        "timestamp": record.get("timestamp")
                    })
            # Detect string errors (from skill responses)
            elif isinstance(outcome, str) and ("error" in outcome.lower() or "failed" in outcome.lower()):
                insights.append({
                    "type": "error",
                    "event": event,
                    "problem": outcome,
                    "timestamp": record.get("timestamp")
                })
        
        return insights

    def summarize(self):
        """
        Provide a high-level summary of recent memory activity.
        """
        recent = self.review_recent()
        summary = {
            "total_events": len(recent),
            "events_by_type": {},
            "success_count": 0,
            "failure_count": 0
        }
        
        for record in recent:
            event_type = record.get("event", "unknown")
            summary["events_by_type"][event_type] = summary["events_by_type"].get(event_type, 0) + 1
            
            outcome = record.get("outcome", {})
            if isinstance(outcome, dict) and outcome.get("status") == "success":
                summary["success_count"] += 1
            elif isinstance(outcome, dict) and outcome.get("status") in ["failed", "error"]:
                summary["failure_count"] += 1
        
        return summary
