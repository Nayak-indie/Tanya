from brain_py.system.events import Event, EventType

class CLI:
    def __init__(self, orchestrator):
        self.orch = orchestrator

    def listen(self):
        """Listen for user input and return an event."""
        try:
            user_input = input(">> ").strip()

            if user_input.lower() in ("exit", "quit"):
                return Event(type=EventType.SYSTEM_SHUTDOWN, payload={})

            return Event(type=EventType.USER_INPUT, payload={"text": user_input})

        except KeyboardInterrupt:
            print("\nInterrupted. Exiting.")
            return Event(type=EventType.SYSTEM_SHUTDOWN, payload={})
