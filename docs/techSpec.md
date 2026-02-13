# techSpec.md — NeuroTune Technical Specification

> Last updated: 2026-02-13
> Source of truth: `docs/agents_setup.md`

---

## 1. Core Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    USER (Browser)                        │
│  ┌───────────────────────────────────────────────────┐  │
│  │  Next.js Frontend                                 │  │
│  │  ┌─────────────┐  ┌────────────┐  ┌───────────┐  │  │
│  │  │ Tone.js     │  │ Redux Toolkit    │  │ UI        │  │  │
│  │  │ Audio       │←─│ State      │←─│ Components│  │  │
│  │  │ Engine      │  │ Store      │  │           │  │  │
│  │  └─────────────┘  └─────┬──────┘  └───────────┘  │  │
│  └──────────────────────────┼────────────────────────┘  │
│                             │ WebSocket / REST           │
└─────────────────────────────┼───────────────────────────┘
                              │
┌─────────────────────────────┼───────────────────────────┐
│  FastAPI Backend            │                            │
│  ┌──────────┐  ┌────────────┴──┐  ┌──────────────────┐  │
│  │ Routers  │  │ LLM Engine    │  │ Audio Processor   │  │
│  │ (REST +  │  │ (HF model)      │  │ (librosa)         │  │
│  │  WS)     │  └───────────────┘  └──────────────────┘  │
│  └────┬─────┘                                            │
│       │                                                  │
│  ┌────┴──────────────┐  ┌────────────────────────────┐  │
│  │ SQLAlchemy ORM    │  │ Local File System           │  │
│  │ (MySQL)           │  │ /local_library              │  │
│  └───────────────────┘  └────────────────────────────┘  │
└──────────────────────────────────────────────────────────┘
```

### Stack Summary

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend | Next.js (React) | Dashboard UI, session controls |
| Audio | Tone.js | Browser-based synthesis (binaural beats, isochronic tones, playback) |
| State | Redux Toolkit | Client-side state (playback status, BPM, session params) |
| Backend | FastAPI (Python) | REST API, WebSocket server, LLM orchestration |
| Database | MySQL | Users, sessions, audio library metadata, prompt templates |
| LLM | HuggingFace Transformers (local) | Generate modulation schedules from session intent |
| Audio Analysis | librosa | BPM/key detection for user-uploaded tracks |
| Data Science | pandas, scikit-learn | User feedback clustering, optimal setting inference |

---

## 2. Data Models (MySQL)

### 2.1 `users`

```sql
CREATE TABLE users (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    username      VARCHAR(50)  NOT NULL UNIQUE,
    email         VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    neurotype     ENUM('adhd', 'autism', 'anxiety', 'depression', 'neurotypical', 'other') DEFAULT 'neurotypical',
    preferences   JSON,          -- volume, sensory prefs, default session type
    created_at    DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_active   DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_active     BOOLEAN DEFAULT TRUE
);
```

### 2.2 `sessions`

```sql
CREATE TABLE sessions (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    user_id       INT NOT NULL,
    intent        VARCHAR(100) NOT NULL,   -- e.g. "deep_focus_coding", "reading", "sleep"
    schedule      JSON NOT NULL,           -- LLM-generated modulation schedule
    duration_sec  INT,                     -- actual session length
    started_at    DATETIME DEFAULT CURRENT_TIMESTAMP,
    ended_at      DATETIME,
    rating        TINYINT,                 -- 1-5 post-session user rating
    feedback_note TEXT,                    -- optional freeform feedback
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

### 2.3 `library`

```sql
CREATE TABLE library (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    file_path     VARCHAR(512) NOT NULL UNIQUE,  -- path in /local_library
    filename      VARCHAR(255) NOT NULL,
    format        VARCHAR(10),                   -- wav, flac, mp3
    duration_sec  FLOAT,
    bpm           FLOAT,                         -- detected by librosa
    key_signature VARCHAR(10),                   -- detected by librosa
    tags          JSON,                          -- user-assigned or auto-tagged
    analyzed_at   DATETIME,
    created_at    DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### 2.4 `prompts`

```sql
CREATE TABLE prompts (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    name          VARCHAR(100) NOT NULL UNIQUE,  -- e.g. "coding_flow_curve"
    template      TEXT NOT NULL,                 -- prompt template with {placeholders}
    model         VARCHAR(100) DEFAULT 'TinyLlama/TinyLlama-1.1B-Chat-v1.0',  -- HuggingFace model ID
    version       INT DEFAULT 1,
    is_active     BOOLEAN DEFAULT TRUE,
    created_at    DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at    DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

---

## 3. API Contract

### 3.1 REST Endpoints

#### Health & Info

| Method | Path | Description | Response |
|--------|------|-------------|----------|
| `GET` | `/` | API health check | `{ status: "ok", version: "1.0.0" }` |
| `GET` | `/health` | DB + LLM connectivity check | `{ api: "ok", db: "ok", llm: "ok" }` |

#### Auth

| Method | Path | Input | Output |
|--------|------|-------|--------|
| `POST` | `/auth/register` | `{ username, email, password, neurotype? }` | `{ user_id, token }` |
| `POST` | `/auth/login` | `{ email, password }` | `{ token, expires_in }` |
| `GET` | `/auth/me` | Bearer token | `User` object |

#### Sessions

| Method | Path | Input | Output |
|--------|------|-------|--------|
| `POST` | `/sessions/start` | `{ intent, user_id }` | `{ session_id, schedule }` — triggers LLM to generate schedule |
| `PATCH` | `/sessions/{id}/end` | `{ rating?, feedback_note? }` | `{ session_id, duration_sec }` |
| `GET` | `/sessions/history` | Query: `user_id`, `limit`, `offset` | `Session[]` |

#### Library

| Method | Path | Input | Output |
|--------|------|-------|--------|
| `POST` | `/library/scan` | `{ directory_path }` | `{ tracks_found, tracks_analyzed }` — triggers librosa scan |
| `GET` | `/library` | Query: `bpm_min`, `bpm_max`, `format`, `limit` | `LibraryTrack[]` |
| `GET` | `/library/{id}/stream` | — | Audio file stream (chunked) |

#### LLM

| Method | Path | Input | Output |
|--------|------|-------|--------|
| `POST` | `/llm/generate-schedule` | `{ intent, current_bpm?, duration_min? }` | `ModulationSchedule` |

### 3.2 WebSocket Endpoint

| Path | Direction | Payload |
|------|-----------|---------|
| `ws://.../ws/session/{session_id}` | Server → Client | Streamed `ModulationUpdate` frames |

#### ModulationSchedule (Pydantic)

```python
class ModulationStep(BaseModel):
    timestamp_sec: float         # seconds from session start
    target_bpm: int              # 40-200
    binaural_freq: float         # Hz (e.g., 4.0 for theta, 14.0 for beta)
    ramp_duration_sec: float     # seconds to transition to this step
    layer: str                   # "binaural" | "isochronic" | "ambient"

class ModulationSchedule(BaseModel):
    intent: str
    total_duration_sec: int
    steps: list[ModulationStep]
```

---

## 4. Directory Structure

```
NeuroTune/
│
├── /backend                        # FastAPI (Python)
│   ├── main.py                     # App factory, startup events, CORS, WS
│   ├── config.py                   # Pydantic Settings (DB URL, HF model ID, etc.)
│   ├── requirements.txt            # fastapi, uvicorn, sqlalchemy, asyncmy, librosa, pydantic, transformers, torch
│   │
│   ├── /routers
│   │   ├── auth.py                 # /auth/* endpoints
│   │   ├── sessions.py             # /sessions/* endpoints
│   │   ├── library.py              # /library/* endpoints
│   │   └── llm.py                  # /llm/* endpoints + WebSocket handler
│   │
│   ├── /models
│   │   ├── orm.py                  # SQLAlchemy table definitions
│   │   └── schemas.py              # Pydantic request/response models
│   │
│   ├── /db
│   │   ├── database.py             # Engine, async session factory
│   │   └── queries.py              # CRUD query classes
│   │
│   ├── /llm_engine
│   │   ├── client.py               # HF Transformers pipeline loader + inference
│   │   ├── prompts.py              # Prompt template loading + formatting
│   │   └── validator.py            # Pydantic validation of LLM JSON output
│   │
│   ├── /audio_processor
│   │   ├── scanner.py              # os.walk directory scanner
│   │   └── analyzer.py             # librosa BPM/key extraction
│   │
│   └── /tests
│       ├── test_auth.py
│       ├── test_sessions.py
│       └── test_llm.py
│
├── /frontend                       # Next.js (React + Tone.js)
│   ├── package.json                # next, react, tone, @reduxjs/toolkit, react-redux
│   ├── next.config.js
│   ├── tsconfig.json
│   │
│   ├── /app                        # Next.js App Router
│   │   ├── layout.tsx
│   │   ├── page.tsx                # Landing / dashboard
│   │   └── /session
│   │       └── page.tsx            # Active session view
│   │
│   ├── /components
│   │   ├── PlayerControls.tsx      # Play, pause, frequency sliders
│   │   ├── AudioVisualizer.tsx     # Canvas-based waveform/spectrum display
│   │   ├── SessionTimer.tsx        # Countdown / elapsed time
│   │   └── FeedbackModal.tsx       # Post-session rating UI
│   │
│   ├── /lib
│   │   ├── synth.ts                # Tone.js audio engine (binaural, isochronic, ambient)
│   │   ├── wsClient.ts             # WebSocket client for receiving modulation updates
│   │   └── api.ts                  # REST client (fetch wrapper)
│   │
│   ├── /stores
│   │   └── sessionSlice.ts         # Redux slice (playback state, current params)
│   │
│   └── /styles
│       └── globals.css
│
├── /local_library                  # User drops audio files here (WAV, FLAC, MP3)
│
├── /docs
│   ├── agents_setup.md             # Agent initialization prompt (source of truth)
│   ├── projectState.md             # Navigation memory (this file's sibling)
│   ├── techSpec.md                 # This file
│   ├── code_guide.md               # Agent coding standards
│   └── jarvis.md                   # JARVIS assistant prompt
│
├── /scripts
│   ├── setup_db.py                 # MySQL schema init + seed data
│   └── docker-compose.yml          # MySQL service
│
├── .env.example                    # DB_URL, HF_MODEL_ID, SECRET_KEY
├── .gitignore
└── README.md
```

---

## 5. Key Integration Patterns

### 5.1 The AI Modulation Loop

```
User selects intent ("Deep Focus - Coding")
        │
        ▼
POST /sessions/start { intent: "coding" }
        │
        ▼
Backend loads prompt template from `prompts` table
        │
        ▼
Backend sends prompt to local HF model: "Construct a flow state curve for a coding session."
        │
        ▼
Model returns JSON → Pydantic validates → ModulationSchedule
        │
        ▼
Schedule returned to frontend via REST (initial) + WebSocket (updates)
        │
        ▼
Tone.js reads schedule steps, ramps oscillators at each timestamp
        │
        ▼
Session ends → user rates → stored in `sessions` table → informs future prompts
```

### 5.2 Frontend Audio Disposal

Per `code_guide.md` Section 6.1 — Tone.js objects **must** be disposed on component unmount:

```typescript
// In synth.ts
const oscillators: Tone.Oscillator[] = [];

export function stop() {
    oscillators.forEach(osc => { osc.stop(); osc.dispose(); });
    oscillators.length = 0;
}

// In React component
useEffect(() => {
    return () => stop();  // cleanup on unmount
}, []);
```

### 5.3 LLM Response Validation

All LLM responses pass through Pydantic before reaching the frontend:

```python
# llm_engine/validator.py
import json
from models.schemas import ModulationSchedule

def parse_llm_response(raw: str) -> ModulationSchedule:
    data = json.loads(raw)
    return ModulationSchedule(**data)  # raises ValidationError if malformed
```
