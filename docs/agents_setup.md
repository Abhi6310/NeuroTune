# Role
You are a Principal Software Architect specializing in "Agentic Workflows." Your goal is to initialize the **Navigation System** for a new software project. This system prevents AI agents from hallucinating by providing them with a clear "Memory" (State) and "Map" (Specification).

# Input Context
Project Description / Readme / Concept:
"""
1. Feasibility & Architecture "Gut Check"

The Core Pivot: AI as the "Conductor," not the "Musician"
You mentioned using a local LLM (like DeepSeek) to "modulate the playing beats."

    Feasibility Warning: Running an LLM to generate raw audio samples in real-time (at 44.1kHz) is extremely computationally expensive and will likely cause latency/stuttering, even on good GPUs.

    The Better Approach: Use the LLM as a "Conductor". The LLM analyzes the user's intent (e.g., "deep work," "reading") and outputs parameters (BPM, pitch, modulation depth). The Frontend (React) then uses the Web Audio API to synthesize the sound instantly based on those parameters. This ensures zero-latency, buttery smooth audio transitions while still utilizing the AI's "intelligence."

The Tech Stack: Flask vs. FastAPI
You suggested Flask. While feasible, I strongly recommend FastAPI for this specific use case.

    Why: You need real-time control. If the AI decides to drop the BPM from 120 to 60, you want that instruction pushed immediately. FastAPI handles asynchronous WebSockets (for real-time communication) much better than Flask. It also integrates natively with Pydantic, which helps validat the JSON outputs from your local LLM.

2. Refined "NeuroTune 2.0" Stack

Here is the recommended stack for a locally hostable, high-performance web app.
Frontend (The Interface & Sound Generator)

    Framework: Next.js (React). It provides a solid structure for a dashboard-like UI.

    Audio Engine: Tone.js.

        Why: This is crucial. Instead of just playing MP3s, Tone.js allows you to build synthesizers in the browser. You can create binaural beats by playing two sine waves (e.g., 440Hz Left, 444Hz Right) to generate a 4Hz theta wave inside the user's head. It allows real-time manipulation of BPM and filters without server lag.

    State Management: Zustand (Simpler than Redux, great for managing "Play", "Pause", "Current BPM").

Backend (The "Brain" & File Handler)

    Server: FastAPI (Python).

    Database: MySQL (as requested).

        Schema: Users, Sessions (logs of what worked), Library (index of local audio files), Prompts (for the LLM).

    Local AI Inference: Ollama (running deepseek-coder or llama3).

        Integration: The backend sends a prompt to Ollama: "User is coding. Current BPM 90. Suggest trajectory." Ollama responds: {"target_bpm": 60, "ramp_duration": 30, "binaural_freq": "14Hz"}.

Data Science (The Logic)

    Libraries: pandas (log analysis), scikit-learn (clustering user feedback to find "optimal" settings for specific tasks).

3. Revised Project Structure

This structure separates the "Brain" (Python) from the "Voice" (React/Tone.js).
Plaintext

NeuroTune-Local/
├── /backend (FastAPI)
│   ├── /audio_processor     # Logic to analyze imported user files (BPM detection)
│   ├── /llm_engine          # Interface to local Ollama/DeepSeek instance
│   ├── /routers             # API Endpoints
│   ├── main.py
│   └── requirements.txt     # librosa, numpy, sqlalchemy, fastapi
│
├── /frontend (Next.js)
│   ├── /components
│   │   ├── AudioVisualizer.tsx  # Canvas based visualizer
│   │   └── PlayerControls.tsx
│   ├── /lib
│   │   └── synth.ts         # Tone.js logic (The "Audio Engine")
│   └── package.json
│
└── /local_library           # User drops their own audio files here

4. Key Implementation Details

A. The Local File Loader
Since you want to read from a folder:

    Backend: Uses os.walk to scan a target directory.

    Analysis: Use librosa (Python library) to analyze the BPM and key of the user's uploaded tracks once and store that metadata in MySQL.

    Playback: The backend serves the file via a stream; the frontend adjusts the playback rate to match the target BPM (timestretching).

B. The AI Modulation Loop

    User Input: Selects "Deep Focus - Coding".

    LLM Query: Backend asks the local model: "Construct a flow state curve for a coding session."

    Response: The LLM returns a JSON schedule.

    Execution: The Frontend receives this schedule. Tone.js creates an oscillator (Isochronic Tone) and automates the volume to pulse at the target frequency (e.g., 15Hz Beta waves for focus), overlaying this on top of the user's music.

5. Next Step

To verify the audio engine feasibility (the riskiest part of the stack), would you like me to generate a prototypical synth.ts file using Tone.js that demonstrates how to generate a binaural beat in a React browser environment?
"""

# Your Task
Based *strictly* on the project description above, generate the initial content for two critical markdown files: `projectState.md` and `techSpec.md`.

## Constraint Checklist & Confidence Score
1. Analyze the tech stack inferred from the description (e.g., React, Python, Node).
2. Infer the critical "Phase 1" (MVP) risks.
3. Define the core data models and API signatures.
4. Output specific, actionable markdown. Do not be vague.

# Output Format

## File 1: `projectState.md`
Follow this strict structure:
1.  **Current Phase:** Define "Phase 1" as the immediate MVP.
2.  **Active Task:** The very first coding step required (e.g., "Initialize Repo").
3.  **Backlog:** A prioritized list of the next 3-5 steps.
4.  **Context Dump:** Any specific constraints mentioned in the input (e.g., "Use Tone.js").

## File 2: `techSpec.md`
Follow this strict structure:
1.  **Core Architecture:** The stack (Frontend, Backend, Database).
2.  **Data Models:** The primary database schemas (in pseudo-code or Typescript interfaces).
3.  **API Contract:** The core API endpoints (method, path, input/output).
4.  **Directory Structure:** A proposed folder tree ensuring separation of concerns.

# Execution
Generate the content for these two files now.
