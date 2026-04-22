from __future__ import annotations

from datetime import datetime


class LocalToolbox:
    """Small utility layer so the assistant can perform deterministic actions."""

    @staticmethod
    def maybe_run(user_text: str) -> str | None:
        text = user_text.lower()

        if "time" in text:
            return f"The current local server time is {datetime.now().strftime('%I:%M %p')}."

        if "date" in text or "day" in text:
            return f"Today's date is {datetime.now().strftime('%A, %B %d, %Y')}."

        if "clear memory" in text or "forget this chat" in text:
            return "__clear_memory__"

        if "help" in text and "what can you do" in text:
            return (
                "I can chat, keep session memory, respond by voice in the browser, "
                "tell you the current time or date, and route general prompts to an "
                "OpenAI-compatible model when credentials are configured."
            )

        return None
