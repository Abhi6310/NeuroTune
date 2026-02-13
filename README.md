# NeuroTune

Shifting gears from a Flutter + SQLite prototype to a locally-hosted web app. The core idea remains the same, adaptive audio for focus and meditation, tailored to neurodivergent users, but the architecture will now use a local LLM (via HuggingFace Transformers) as a "Conductor" that outputs modulation parameters (BPM, binaural frequency, ramp curves), while the browser handles real-time audio synthesis through Tone.js.

**Stack:** Next.js + Tone.js + Redux Toolkit (frontend), FastAPI + MySQL + HuggingFace Transformers (backend), librosa (audio analysis).
