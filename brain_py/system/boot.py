from brain_py.system.events import Event, EventType


def boot_event() -> Event:
    return Event(
        type=EventType.SYSTEM_BOOT,
        payload={"message": "Tanya initialized"}
    )
