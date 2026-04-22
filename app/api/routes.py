from __future__ import annotations

from uuid import uuid4

from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.core.config import settings
from app.services.llm_service import llm_service
from app.services.session_store import session_store
from app.services.tooling import LocalToolbox

router = APIRouter()


class MessageRequest(BaseModel):
    session_id: str = Field(..., min_length=1)
    message: str = Field(..., min_length=1, max_length=4000)


class MessageResponse(BaseModel):
    session_id: str
    reply: str
    messages: list[dict]
    provider_mode: str


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "app": settings.app_name}


@router.post("/session")
async def create_session() -> dict[str, str]:
    session_id = str(uuid4())
    return {"session_id": session_id}


@router.post("/assistant/message", response_model=MessageResponse)
async def assistant_message(payload: MessageRequest) -> MessageResponse:
    session_store.append(payload.session_id, "user", payload.message)
    tool_output = LocalToolbox.maybe_run(payload.message)

    if tool_output == "__clear_memory__":
        session_store.clear(payload.session_id)
        reply = "Session memory cleared. We are starting fresh."
        session_store.append(payload.session_id, "assistant", reply)
    elif tool_output:
        reply = tool_output
        session_store.append(payload.session_id, "assistant", reply)
    else:
        history = session_store.get_messages(payload.session_id)
        reply = await llm_service.generate_reply(payload.message, history[:-1])
        session_store.append(payload.session_id, "assistant", reply)

    return MessageResponse(
        session_id=payload.session_id,
        reply=reply,
        messages=session_store.get_messages(payload.session_id),
        provider_mode="openai" if settings.llm_enabled else "local-fallback",
    )
