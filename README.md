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
