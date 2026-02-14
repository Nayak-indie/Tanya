from enum import Enum
from dataclasses import dataclass
from typing import Any, Dict


class EventType(Enum):
    SYSTEM_BOOT = "system_boot"
    SYSTEM_SHUTDOWN = "system_shutdown"
    USER_INPUT = "user_input"
    MEMORY_WRITE = "memory_write"
    MEMORY_QUERY = "memory_query"
    REFLECT = "reflect"

    # Add this
    AUTONOMY_CYCLE = "autonomy_cycle"
@dataclass
class Event:
    type: EventType
    payload: Dict[str, Any]
