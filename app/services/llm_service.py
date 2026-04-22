from __future__ import annotations

from datetime import datetime

import httpx

from app.core.config import settings


SYSTEM_PROMPT = """You are a capable AI voice assistant for a full-stack web app.
Keep answers concise, helpful, and conversational.
When the user asks for steps, prefer a short action plan.
If the user asks something impossible without integrations, say what would be needed.
"""


class LLMService:
    async def generate_reply(self, user_text: str, history: list[dict[str, str]]) -> str:
        if settings.llm_enabled:
            reply = await self._call_openai(user_text, history)
            if reply:
                return reply
        return self._fallback_reply(user_text, history)

    async def _call_openai(self, user_text: str, history: list[dict[str, str]]) -> str | None:
        headers = {
            "Authorization": f"Bearer {settings.openai_api_key}",
            "Content-Type": "application/json",
        }
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        messages.extend({"role": item["role"], "content": item["content"]} for item in history[-8:])
        messages.append({"role": "user", "content": user_text})

        payload = {
            "model": settings.openai_model,
            "messages": messages,
            "temperature": 0.7,
        }

        try:
            async with httpx.AsyncClient(timeout=20.0) as client:
                response = await client.post(
                    f"{settings.openai_base_url.rstrip('/')}/chat/completions",
                    headers=headers,
                    json=payload,
                )
                response.raise_for_status()
                data = response.json()
        except Exception:
            return None

        try:
            return data["choices"][0]["message"]["content"].strip()
        except (KeyError, IndexError, TypeError):
            return None

    def _fallback_reply(self, user_text: str, history: list[dict[str, str]]) -> str:
        message = user_text.lower().strip()
        if not history:
            return (
                "I am ready. You can speak or type a request, and I will answer here. "
                "If you add an OpenAI API key later, I can switch from local fallback "
                "responses to a full LLM-backed mode."
            )

        if "weather" in message:
            return (
                "Weather needs a live weather API integration. I can add one next, or you can "
                "connect this app to your preferred provider."
            )

        if "email" in message or "send message" in message:
            return (
                "Sending messages safely requires an authenticated integration such as Gmail, "
                "Outlook, or Twilio. The current project is structured so those tools can be added."
            )

        if "summary" in message or "summarize" in message:
            recent = [item["content"] for item in history[-4:] if item["role"] == "user"]
            if recent:
                return "Recent topics: " + " | ".join(recent)
            return "There is not enough conversation yet for a useful summary."

        if "plan" in message or "roadmap" in message:
            return (
                "Here is a quick plan: 1. Define the goal. 2. Break it into small steps. "
                "3. Start with the highest-value task. 4. Review what changed. 5. Iterate."
            )

        return (
            "This project is running in local assistant mode right now. I understood your request as: "
            f"'{user_text}'. I can keep chatting, manage session memory, and handle browser voice input "
            "while you plug in external AI or tool integrations."
        )


llm_service = LLMService()
