# projectState.md — NeuroTune Navigation Memory

> Last updated: 2026-02-13
> Source of truth: `docs/agents_setup.md`

---

## 1. Current Phase: Phase 1 — Audio Engine Feasibility (MVP)

**Objective:** Prove that the browser can synthesize binaural beats and isochronic tones in real-time using Tone.js, and that a local LLM (via HuggingFace Transformers) can produce valid modulation parameters with acceptable latency.

**Success Criteria:**
- A Next.js page renders player controls and plays a binaural beat (two sine waves, e.g., 440Hz L / 444Hz R = 4Hz theta).
- Tone.js isochronic tone overlay with automated volume pulsing at a target frequency.
- FastAPI endpoint accepts a session intent string, queries a local HF model, and returns a valid JSON schedule (`target_bpm`, `ramp_duration`, `binaural_freq`).
- Round-trip latency (user click → LLM response → parameter applied to audio) under 3 seconds on local hardware.

---

## 2. Active Task: Scaffold the Next.js + Tone.js Audio Prototype

**What to build right now:**
1. Initialize a Next.js project under `/frontend`.
2. Install `tone`, `@reduxjs/toolkit`, and `react-redux`.
3. Create `lib/synth.ts` — a minimal Tone.js module that exposes:
   - `startBinauralBeat(baseFreq, beatFreq)` — plays L/R oscillators.
   - `startIsochronicTone(freq, pulseRate)` — plays a pulsing tone.
   - `stop()` — disposes all active nodes.
4. Create a `PlayerControls.tsx` component that wires play/pause/frequency sliders to `synth.ts`.
5. Verify audio output works in Chrome/Firefox.

---

## 3. Backlog (Prioritized)

| # | Task | Why It's Next |
|---|------|---------------|
| 1 | **FastAPI skeleton + HF Transformers integration** | Stand up `/backend/main.py`, create `/llm_engine` module, load a local HF model via `transformers` pipeline, validate JSON response with Pydantic. |
| 2 | **WebSocket bridge (backend → frontend)** | Pipe LLM-generated modulation schedules to the frontend in real-time so Tone.js can ramp parameters without polling. |
| 3 | **MySQL schema + SQLAlchemy models** | Define `users`, `sessions`, `library`, `prompts` tables. Connect via `asyncmy` or `aiomysql`. |
| 4 | **Local file loader + librosa analysis** | `/backend/audio_processor` scans a local directory, extracts BPM/key per track via librosa, stores metadata in MySQL. |
| 5 | **Session feedback loop** | After a session ends, collect user rating, store it, feed it back into future LLM prompts for personalization. |

---

## 4. Context Dump — Hard Constraints & Decisions

| Constraint | Detail |
|------------|--------|
| **AI role** | "Conductor" not "Musician" — LLM outputs parameters (BPM, freq, ramp), frontend synthesizes audio. LLM never generates raw audio. |
| **Audio engine** | Tone.js in the browser. No server-side audio generation. Zero-latency synthesis. |
| **Frontend framework** | Next.js (React). App Router assumed unless stated otherwise. |
| **State management** | Redux Toolkit + react-redux. |
| **Backend framework** | FastAPI (Python). Async-first. |
| **Database** | MySQL. |
| **Local LLM** | HuggingFace Transformers running locally. Model loaded via `transformers` pipeline in the backend process. |
| **Audio analysis** | librosa for BPM/key detection on user-uploaded tracks. |
| **Data science** | pandas + scikit-learn for clustering user feedback. |
| **Real-time comms** | FastAPI WebSockets for pushing modulation schedules to frontend. |
| **Deployment** | Locally hostable. No cloud dependency. |

---

## 5. Known Risks

| Risk | Mitigation |
|------|------------|
| HF model inference latency too high for real-time feel | Pre-generate session schedules before playback starts; use WebSocket to stream incremental updates. |
| LLM returns malformed JSON | Strict Pydantic validation on all LLM responses; fallback to sane defaults. |
| Tone.js browser compatibility | Test on Chrome + Firefox early; document any Safari AudioContext restrictions. |
| librosa analysis is slow on large libraries | Run analysis as a background job on first scan; cache results in MySQL `library` table. |
| HF model requires significant RAM/VRAM | Start with a small model (e.g., TinyLlama, phi-2); document minimum hardware requirements. |
| MySQL adds setup friction for local dev | Provide a Docker Compose file with MySQL service; document manual install as fallback. |

---

## 6. Codebase Drift Warning

The current codebase (`/api`, `/app`) reflects an older architecture (Flutter frontend, SQLite, no LLM integration). **Do not reference existing code as authoritative.** The pivot described in `agents_setup.md` supersedes it. New work should go into `/backend` and `/frontend` directories per the revised structure.
