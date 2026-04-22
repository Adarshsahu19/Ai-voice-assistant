# Voice Assistant Studio

A full-stack AI voice assistant project with:

- FastAPI backend
- Browser-based frontend
- Voice input through the Web Speech API
- Spoken responses through Speech Synthesis
- Session memory
- Local tool actions
- Optional OpenAI-compatible LLM integration

## Stack

- Backend: FastAPI, httpx, Jinja2
- Frontend: HTML, CSS, vanilla JavaScript
- Voice UX: Browser SpeechRecognition and speechSynthesis APIs

## Project Structure

```text
app/
  api/
  core/
  services/
static/
  css/
  js/
templates/
```

## Run Locally

1. Create a virtual environment:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Copy environment settings:

```powershell
Copy-Item .env.example .env
```

4. Start the server:

```powershell
uvicorn app.main:app --reload
```

5. Open `http://127.0.0.1:8000`

## OpenAI Mode

To enable LLM-backed replies, add your values in `.env`:

```env
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4o-mini
OPENAI_BASE_URL=https://api.openai.com/v1
```

If no API key is set, the assistant still works using a local fallback response engine.

## API Endpoints

- `GET /api/health`
- `POST /api/session`
- `POST /api/assistant/message`

## Suggested Next Upgrades

- Add real-time streaming with WebSockets
- Add Whisper or browser audio upload transcription
- Add authentication and user accounts
- Add vector memory or database-backed chat history
- Add integrations for weather, email, calendar, and search

## Deploy From GitHub

This repository now includes deployment files for Docker, Render, and Railway.

### Option 1: Render

1. Push the repo to GitHub.
2. In Render, create a new `Web Service` from the GitHub repo.
3. Render will detect `render.yaml`, or you can set:

```text
Build Command: pip install -r requirements.txt
Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

4. Add environment variables:

```text
APP_ENV=production
APP_DEBUG=false
APP_NAME=Voice Assistant Studio
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4o-mini
OPENAI_BASE_URL=https://api.openai.com/v1
```

### Option 2: Railway

1. Create a new project from the GitHub repo.
2. Railway will use `railway.json`.
3. Add the same environment variables listed above.

### Option 3: Docker

Build and run locally or on any container host:

```powershell
docker build -t voice-assistant-studio .
docker run -p 8000:8000 --env-file .env voice-assistant-studio
```

### Important Note

Browser speech recognition support depends on the client browser. Deployment makes the web app public, but speech-to-text still depends on browser support such as Chrome or Edge.
