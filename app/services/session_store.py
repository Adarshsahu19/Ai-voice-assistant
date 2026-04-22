from __future__ import annotations

from collections import defaultdict
from datetime import UTC, datetime
from typing import Any


class SessionStore:
    def __init__(self) -> None:
        self._messages: dict[str, list[dict[str, Any]]] = defaultdict(list)

    def get_messages(self, session_id: str) -> list[dict[str, Any]]:
        return self._messages[session_id]

    def append(self, session_id: str, role: str, content: str) -> dict[str, Any]:
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now(UTC).isoformat(),
        }
        self._messages[session_id].append(message)
        return message

    def clear(self, session_id: str) -> None:
        self._messages[session_id] = []


session_store = SessionStore()
