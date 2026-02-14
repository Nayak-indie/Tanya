import sqlite3
import json
from datetime import datetime

class MemoryStore:
    """
    Persistent memory backend for Tanya using SQLite.
    Stores all events, proposals, and outcomes.
    """

    def __init__(self, db_path="tanya_memory.db"):
        self.db_path = db_path
        self._conn = sqlite3.connect(self.db_path)
        self._cursor = self._conn.cursor()
        self._setup_tables()

    def _setup_tables(self):
        """Create memory table if it doesn't exist."""
        try:
            self._cursor.execute("""
                CREATE TABLE IF NOT EXISTS memory (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    event TEXT,
                    payload TEXT,
                    proposal TEXT,
                    outcome TEXT
                )
            """)
            self._conn.commit()
        except sqlite3.OperationalError as e:
            print(f"Error creating table: {e}")

    def store(self, record: dict):
        """
        Save a single event record.
        record = {
            'event': 'USER_INPUT',
            'payload': {...},
            'proposal': {...},
            'outcome': {...}
        }
        """
        try:
            timestamp = datetime.utcnow().isoformat()
            self._cursor.execute("""
                INSERT INTO memory (timestamp, event, payload, proposal, outcome)
                VALUES (?, ?, ?, ?, ?)
            """, (
                timestamp,
                record.get("event", ""),
                json.dumps(record.get("payload", {})),
                json.dumps(record.get("proposal", {})),
                json.dumps(record.get("outcome", {}))
            ))
            self._conn.commit()
        except (sqlite3.OperationalError, json.JSONDecodeError) as e:
            print(f"Error storing record: {e}")

    def recall_recent(self, n=5):
        """Return the last n events as a list of dicts."""
        try:
            self._cursor.execute("""
                SELECT timestamp, event, payload, proposal, outcome
                FROM memory
                ORDER BY id DESC
                LIMIT ?
            """, (n,))
            rows = self._cursor.fetchall()
            results = []
            for ts, event, payload, proposal, outcome in rows:
                results.append({
                    "timestamp": ts,
                    "event": event,
                    "payload": json.loads(payload),
                    "proposal": json.loads(proposal),
                    "outcome": json.loads(outcome)
                })
            return results
        except (sqlite3.OperationalError, json.JSONDecodeError) as e:
            print(f"Error recalling recent: {e}")
            return []

    def fetch_recent(self, limit=10):
        """
        Backward compatibility wrapper. Use recall_recent() instead.
        """
        return self.recall_recent(n=limit)

    def search(self, keyword: str):
        """Return all events where payload or proposal contains the keyword."""
        try:
            self._cursor.execute("""
                SELECT timestamp, event, payload, proposal, outcome
                FROM memory
            """)
            rows = self._cursor.fetchall()
            results = []
            for ts, event, payload, proposal, outcome in rows:
                payload_data = json.loads(payload)
                proposal_data = json.loads(proposal)
                if (keyword.lower() in json.dumps(payload_data).lower()
                    or keyword.lower() in json.dumps(proposal_data).lower()):
                    results.append({
                        "timestamp": ts,
                        "event": event,
                        "payload": payload_data,
                        "proposal": proposal_data,
                        "outcome": json.loads(outcome)
                    })
            return results
        except (sqlite3.OperationalError, json.JSONDecodeError) as e:
            print(f"Error searching memory: {e}")
            return []

    def all(self):
        """Return everything in memory."""
        return self.recall_recent(n=10000)

    def clear(self):
        """Clear all persistent memory (use with caution)."""
        try:
            self._cursor.execute("DELETE FROM memory")
            self._conn.commit()
            print("Memory cleared.")
        except sqlite3.OperationalError as e:
            print(f"Error clearing memory: {e}")

    def find_events(self, event_name: str):
        """Return all stored events where event type matches event_name."""
        try:
            self._cursor.execute("""
                SELECT timestamp, event, payload, proposal, outcome
                FROM memory
                WHERE event = ?
            """, (event_name,))
            rows = self._cursor.fetchall()
            results = []
            for ts, event, payload, proposal, outcome in rows:
                results.append({
                    "timestamp": ts,
                    "event": event,
                    "payload": json.loads(payload),
                    "proposal": json.loads(proposal),
                    "outcome": json.loads(outcome)
                })
            return results
        except (sqlite3.OperationalError, json.JSONDecodeError) as e:
            print(f"Error finding events: {e}")
            return []

    def close(self):
        """Close database connection."""
        try:
            self._conn.close()
        except sqlite3.ProgrammingError as e:
            print(f"Error closing connection: {e}")

