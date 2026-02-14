from brain_py.interface.cli import CLI
from brain_py.interface.orchestrator import Orchestrator
from brain_py.interface.autonomy import AutonomyLoop
from brain_py.system.boot import boot_event
from brain_py.system.events import EventType
from brain_py.memory.memory_core import MemoryCore

def main() -> None:
    """Run Tanya with full override-intent-goal integration."""
    memory = MemoryCore()
    orchestrator = Orchestrator(memory)
    cli = CLI(orchestrator)


    # ---- SYSTEM BOOT ----
    boot = boot_event()
    print(f"[ORCH] Handling event: {boot.type}")
    print("[RESULT]", orchestrator.handle_event(boot.type, boot.payload))

    # ---- CHAT INTERFACE ----
    print("\n[MAIN] Entering chat mode. Type 'exit' or 'quit' to shutdown.\n")
    from brain_py.interface.voice import VoiceInterface
    voice = VoiceInterface()
    while True:
        user_text = voice.listen()
        if user_text.lower() in ("exit", "quit"):
            print("Tanya shutting down.")
            break
        # 1️⃣ Check for user override commands first
        if orchestrator.override.interpret(user_text):
            continue  # override handled, skip normal event
        # 2️⃣ Normal event → planner → action → memory
        event = type('Event', (), {'type': EventType.USER_INPUT, 'payload': {'text': user_text}})()
        result = orchestrator.handle_event(event.type, event.payload)
        response = result.get("result") if isinstance(result, dict) else str(result)
        voice.speak(response)
        # 3️⃣ Show current intent & goal
        current_intent = orchestrator.intent.get_intent()
        active_goal = orchestrator.goals.get_active_goal()
        print(f"[INTENT] Current intent: {current_intent['name'] if current_intent else 'None'}")
        print(f"[GOAL] Active goal: {active_goal['name'] if active_goal else 'None'}")

        # 4️⃣ Ask for feedback and store it
        feedback = input("Rate Tanya's last response (good/bad/boring/skip): ").strip().lower()
        if feedback in ("good", "bad", "boring"):
            orchestrator.memory.remember("feedback", orchestrator.memory.recall("feedback", []) + [{"input": user_text, "response": response, "rating": feedback}])

if __name__ == "__main__":
    main()
