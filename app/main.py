from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.api.routes import router
from app.core.config import settings

BASE_DIR = Path(__file__).resolve().parent.parent

app = FastAPI(title=settings.app_name, debug=settings.app_debug)
app.include_router(router, prefix="/api")

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "request": request,
            "app_name": settings.app_name,
            "provider_mode": "OpenAI" if settings.llm_enabled else "Local fallback",
        },
    )
