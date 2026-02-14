import sqlite3
import json
from datetime import datetime

class SQLiteMemoryStore:
    def __init__(self, db_path="tanya_memory.db"):
        self.conn = sqlite3.connect(db_path)
        self._create_tables()
        # Make rows accessible by index only; we return structured dicts

    def _create_tables(self):
        c = self.conn.cursor()
        c.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            event_type TEXT,
            payload TEXT
        )
        """)
        c.execute("""
        CREATE TABLE IF NOT EXISTS proposals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_id INTEGER,
            proposal TEXT,
            FOREIGN KEY(event_id) REFERENCES events(id)
        )
        """)
        c.execute("""
        CREATE TABLE IF NOT EXISTS outcomes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            proposal_id INTEGER,
            outcome TEXT,
            FOREIGN KEY(proposal_id) REFERENCES proposals(id)
        )
        """
        )
        self.conn.commit()

    # Compatibility helpers for existing reflection/orchestrator code
    def recall_recent(self, n=5):
        """Mirror MemoryStore.recall_recent shape from normalized tables."""
        events = self.fetch_events(limit=n)
        records = []
        for e in events:
            full = self.fetch_full_record(e["id"]) or {}
            records.append({
                "timestamp": e.get("timestamp"),
                "event": e.get("event"),
                "payload": e.get("payload", {}),
                "proposal": (full.get("proposal", {}) or {}).get("proposal", {}),
                "outcome": full.get("outcome", {}) or {}
            })
        return records

    def fetch_recent(self, limit=10):
        return self.recall_recent(n=limit)

    def save_event(self, event_type, payload):
        ts = datetime.utcnow().isoformat()
        c = self.conn.cursor()
        c.execute(
            "INSERT INTO events (timestamp, event_type, payload) VALUES (?, ?, ?)",
            (ts, event_type, json.dumps(payload))
        )
        self.conn.commit()
        return c.lastrowid

    def save_proposal(self, event_id, proposal):
        c = self.conn.cursor()
        c.execute(
            "INSERT INTO proposals (event_id, proposal) VALUES (?, ?)",
            (event_id, json.dumps(proposal))
        )
        self.conn.commit()
        return c.lastrowid

    def save_outcome(self, proposal_id, outcome):
        c = self.conn.cursor()
        c.execute(
            "INSERT INTO outcomes (proposal_id, outcome) VALUES (?, ?)",
            (proposal_id, json.dumps(outcome))
        )
        self.conn.commit()
        return c.lastrowid

    def fetch_events(self, limit=10):
        """Return last N events with parsed payloads."""
        c = self.conn.cursor()
        c.execute("SELECT id, timestamp, event_type, payload FROM events ORDER BY id DESC LIMIT ?", (limit,))
        rows = c.fetchall()
        result = []
        for eid, ts, etype, payload in rows:
            try:
                payload_obj = json.loads(payload) if payload else {}
            except json.JSONDecodeError:
                payload_obj = {}
            result.append({
                "id": eid,
                "timestamp": ts,
                "event": etype,
                "payload": payload_obj
            })
        return result

    def fetch_full_record(self, event_id):
        """Return combined event, proposal, outcome as structured dicts."""
        c = self.conn.cursor()
        c.execute("SELECT id, timestamp, event_type, payload FROM events WHERE id=?", (event_id,))
        e = c.fetchone()
        if not e:
            return None
        eid, ts, etype, payload = e
        try:
            payload_obj = json.loads(payload) if payload else {}
        except json.JSONDecodeError:
            payload_obj = {}

        c.execute("SELECT id, event_id, proposal FROM proposals WHERE event_id=? ORDER BY id DESC LIMIT 1", (event_id,))
        p = c.fetchone()
        proposal_obj = {}
        outcome_obj = None
        proposal_id = None
        if p:
            proposal_id, _, proposal = p
            try:
                proposal_obj = json.loads(proposal) if proposal else {}
            except json.JSONDecodeError:
                proposal_obj = {}
            c.execute("SELECT id, proposal_id, outcome FROM outcomes WHERE proposal_id=? ORDER BY id DESC LIMIT 1", (proposal_id,))
            o = c.fetchone()
            if o:
                try:
                    outcome_obj = json.loads(o[2]) if o[2] else {}
                except json.JSONDecodeError:
                    outcome_obj = {}
        return {
            "event": {"id": eid, "timestamp": ts, "event": etype, "payload": payload_obj},
            "proposal": {"id": proposal_id, "event_id": event_id, "proposal": proposal_obj} if p else None,
            "outcome": outcome_obj
        }

    def search_events_by_type(self, event_type):
        """Search for events by event_type (case-insensitive) and return full records."""
        c = self.conn.cursor()
        c.execute("SELECT id, timestamp, event_type, payload FROM events WHERE upper(event_type) = upper(?)", (event_type,))
        rows = c.fetchall()
        result = []
        for eid, ts, etype, payload in rows:
            try:
                payload_obj = json.loads(payload) if payload else {}
            except json.JSONDecodeError:
                payload_obj = {}
            full = self.fetch_full_record(eid) or {}
            result.append({
                "timestamp": ts,
                "event": etype,
                "payload": payload_obj,
                "proposal": (full.get("proposal", {}) or {}).get("proposal", {}),
                "outcome": full.get("outcome", {}) or {}
            })
        return result
