import os
import sys
import time
import threading
# ensure repo root is on sys.path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from brain_py.interface.orchestrator import Orchestrator
from brain_py.memory.memory_core import MemoryCore
from brain_py.system.events import EventType

# Monkeypatch the mixtral_client to simulate streaming
import brain_py.skills.mixtral_client as mc

def fake_send(messages):
    parts = ["Hello", ", ", "this is Tanya."]
    out = ""
    for p in parts:
        print(p, end="", flush=True)
        out += p
        time.sleep(0.05)
    print()
    return out

mc.send_message = fake_send

memory = MemoryCore()
orch = Orchestrator(memory)

queries = ["hey", "what can you do?"]
for q in queries:
    print(f"You: {q}")
    # run in background like the terminal app
    def worker(text):
        res = orch.handle_event(EventType.USER_INPUT, {"text": text})
        print("[worker returned]", res)
    t = threading.Thread(target=worker, args=(q,), daemon=True)
    t.start()
    # wait a bit for streaming to finish
    time.sleep(0.3)

print("Test harness finished")
