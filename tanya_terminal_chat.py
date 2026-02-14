

import sys
import os
# Ensure sensible defaults for threading and device before importing the client
os.environ.setdefault("LLAMA_N_THREADS", os.environ.get("LLAMA_N_THREADS", "8"))
os.environ.setdefault("LLAMA_DEVICE", os.environ.get("LLAMA_DEVICE", "cpu"))
# Align OMP threads for better CPU utilization
os.environ.setdefault("OMP_NUM_THREADS", os.environ.get("OMP_NUM_THREADS", os.environ.get("LLAMA_N_THREADS", "8")))

from brain_py.interface.orchestrator import Orchestrator
from brain_py.memory.memory_core import MemoryCore
from brain_py.system.events import EventType
from brain_py.skills.auto_self_improver import analyze_and_update_prompt

memory = MemoryCore()
orch = Orchestrator(memory)

# Optionally perform a blocking warm-up of the local GGUF Llama instance to avoid first-call latency.
# Set `TANYA_WARM_LLAMA=false` to skip blocking warm-up.
try:
    warm_flag = os.getenv("TANYA_WARM_LLAMA", "true").lower()
    if warm_flag in ("1", "true", "yes", "y"):
        try:
            from brain_py.skills import mixtral_client
            print("Warming local GGUF model (blocking, up to 30s)...")
            ok = mixtral_client.warmup_now(timeout=30)
            print("Warmup result:", "OK" if ok else "not available")
        except Exception:
            print("Warmup attempted but failed; continuing.")
except Exception:
    pass

print("Tanya Terminal Chat. Type 'exit' to quit.")
conversation = []

# Failsafe identity triggers
identity_triggers = [
    "who are you", "what is your name", "tell me about yourself", "your identity", "about yourself", "who r u", "who you are",
    "who ru", "who is tanya", "describe yourself", "what are you", "are you sentient", "are you self aware", "what do you do", "what can you do"
]

while True:
    try:
        user_input = input("You: ")
    except (EOFError, KeyboardInterrupt):
        print("\nGoodbye!")
        break
    if user_input.lower() in ("exit", "quit"):
        print("Goodbye!")
        break

    # Fast-path identity queries handled locally
    if any(trigger in user_input.lower() for trigger in identity_triggers):
        print(f"Tanya: {orch.self_concept}")
        # record conversation
        conversation.append({"user": user_input, "reply": orch.self_concept})
        analyze_and_update_prompt(conversation[-1:])
        continue

    # Synchronous call: block until full response received
    try:
        result = orch.handle_event(EventType.USER_INPUT, {"text": user_input})
        response = result.get("result") if isinstance(result, dict) and result.get("result") is not None else str(result) if result is not None else "(No response)"
    except Exception as e:
        response = f"[Error handling input: {e}]"

    # Print full reply at once
    print(f"Tanya: {response}")

    # record conversation and self-improve
    conversation.append({"user": user_input, "reply": response})
    try:
        analyze_and_update_prompt(conversation[-1:])
    except Exception:
        pass

    # Auto-infer feedback
    if not any(trigger in user_input.lower() for trigger in identity_triggers):
        try:
            orch.user_model.add_satisfaction(1)
            orch.user_model.add_feedback(user_input, "positive (auto-inferred)")
        except Exception:
            pass

    # Auto-retrain model in the background after every conversation (throttled)
    try:
        import threading as _threading
        from brain_py.skills import retrain_model
        if not hasattr(retrain_model, '_retrain_thread') or not retrain_model._retrain_thread.is_alive():
            retrain_model._retrain_thread = _threading.Thread(target=retrain_model.retrain_model, daemon=True)
            retrain_model._retrain_thread.start()
    except Exception:
        pass
