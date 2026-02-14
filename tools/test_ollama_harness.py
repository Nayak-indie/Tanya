import os
import sys
import time
import threading
# ensure repo root on path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from brain_py.interface.orchestrator import Orchestrator
from brain_py.memory.memory_core import MemoryCore
from brain_py.system.events import EventType

# Patch requests.post in the mixtral_client module to simulate Ollama streaming
import brain_py.skills.mixtral_client as mc
import types

class FakeResp:
    def __init__(self, lines):
        self._lines = lines
    def raise_for_status(self):
        return
    def iter_lines(self, decode_unicode=False):
        for l in self._lines:
            yield l
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc, tb):
        return False

def fake_post(url, **kwargs):
    # produce a few JSON lines that mimic Ollama streaming
    import json as _json
    text = "Hey there! I'm Tanya — how can I help you today?"
    # split into token-like chunks
    chunks = [text[i:i+10] for i in range(0, len(text), 10)]
    # make JSON per line
    lines = [_json.dumps({"response": c}) for c in chunks]
    return FakeResp(lines)

# monkeypatch
mc.requests.post = fake_post

memory = MemoryCore()
orch = Orchestrator(memory)

queries = ["hey", "what can you do?"]
for q in queries:
    print(f"You: {q}")
    def worker(text):
        res = orch.handle_event(EventType.USER_INPUT, {"text": text})
        print("[worker returned]", res)
    t = threading.Thread(target=worker, args=(q,), daemon=True)
    t.start()
    time.sleep(0.5)

print("Ollama harness finished")
