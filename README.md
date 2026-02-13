# NeuroTune

Shifting gears from a Flutter + SQLite prototype to a locally-hosted web app. The core idea remains the same, adaptive audio for focus and meditation, tailored to neurodivergent users, but the architecture will now use a local LLM (via HuggingFace Transformers) as a "Conductor" that outputs modulation parameters (BPM, binaural frequency, ramp curves), while the browser handles real-time audio synthesis through Tone.js.

**Stack:** Next.js + Tone.js + Redux Toolkit (frontend), FastAPI + MySQL + HuggingFace Transformers (backend), librosa (audio analysis).

## Privacy & Data

Everything runs locally. No cloud APIs, no telemetry, no external calls. Audio synthesis happens in-browser via Tone.js. LLM inference runs on your own hardware through HuggingFace Transformers. Your session data, audio files, and preferences never leave your machine.

## Getting Started

**Requirements:** Python 3.10+, Node.js 20+, ~20GB disk (LLM model cache), 16GB+ RAM recommended. CUDA GPU optional for faster inference. Docker optional for MySQL (SQLite works by default).

```bash
# clone and enter project
git clone https://github.com/<your-username>/NeuroTune.git && cd NeuroTune

# backend — virtual env + dependencies
python -m venv .venv && source .venv/bin/activate
pip install -r backend/requirements.txt

# frontend — install dependencies
cd frontend && npm install && cd ..

# (optional) start MySQL via Docker
docker compose up -d
```

**Environment** is configured in `backend/config.py` with sensible defaults. Override via `.env` in project root:

| Variable         | Default                                     | Description              |
| ---------------- | ------------------------------------------- | ------------------------ |
| `DATABASE_URL`   | `sqlite+aiosqlite:///./neurotune.db`        | Async DB connection      |
| `HF_MODEL_ID`    | `deepseek-ai/DeepSeek-R1-Distill-Llama-8B` | HuggingFace model ID     |
| `HOST`           | `127.0.0.1`                                 | Backend bind address     |
| `PORT`           | `8000`                                      | Backend port             |
| `DEBUG`          | `true`                                      | Debug mode               |

SQLite works out of the box — no `.env` changes needed to get running.

```bash
# terminal 1 — backend (downloads LLM model on first run)
source .venv/bin/activate && python backend/main.py
# → http://localhost:8000  (API docs at /docs)

# terminal 2 — frontend
cd frontend && npm run dev
# → http://localhost:3000
```

## Project Structure

```text
NeuroTune/
├── backend/
│   ├── db/           # async database engine, session factory, queries
│   ├── models/       # SQLAlchemy ORM models, Pydantic request/response schemas
│   ├── llm_engine/   # LLM loading, prompt templates, output validation, fallbacks
│   └── routers/      # API endpoint handlers, WebSocket connections
├── frontend/src/
│   ├── app/          # Next.js App Router — pages, layouts, providers
│   ├── lib/          # Tone.js audio synth, REST client, WebSocket client
│   └── stores/       # Redux Toolkit store config, slices, typed hooks
└── docker-compose.yml
```
