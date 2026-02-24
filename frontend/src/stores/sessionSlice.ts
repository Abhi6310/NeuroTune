import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { ModulationSchedule, ModulationStep } from "@/lib/api";

interface SessionState {
  status: "idle" | "loading" | "playing" | "ended";
  sessionId: number | null;
  intent: string;
  schedule: ModulationSchedule | null;
  currentStep: ModulationStep | null;
  currentStepIndex: number;
  elapsedSec: number;
  startedAt: number | null; // unix timestamp ms for session page to compute elapsed
  error: string | null;
  latencyMs: number | null;
}

const initialState: SessionState = {
  status: "idle",
  sessionId: null,
  intent: "Deep Focus - Coding",
  schedule: null,
  currentStep: null,
  currentStepIndex: 0,
  elapsedSec: 0,
  startedAt: null,
  error: null,
  latencyMs: null,
};

const sessionSlice = createSlice({
  name: "session",
  initialState,
  reducers: {
    setIntent(state, action: PayloadAction<string>) {
      state.intent = action.payload;
    },
    setLoading(state) {
      state.status = "loading";
      state.error = null;
    },
    sessionStarted(
      state,
      action: PayloadAction<{
        schedule: ModulationSchedule;
        latencyMs: number;
        sessionId: number;
        startedAt: number;
      }>
    ) {
      state.status = "playing";
      state.sessionId = action.payload.sessionId;
      state.schedule = action.payload.schedule;
      state.currentStep = action.payload.schedule.steps[0];
      state.currentStepIndex = 0;
      state.latencyMs = action.payload.latencyMs;
      state.elapsedSec = 0;
      state.startedAt = action.payload.startedAt;
    },
    sessionFailed(state, action: PayloadAction<string>) {
      state.status = "idle";
      state.error = action.payload;
    },
    sessionEnded(state) {
      state.status = "ended";
    },
    feedbackSubmitted(state) {
      return { ...initialState, intent: state.intent };
    },
    tick(state, action: PayloadAction<number>) {
      state.elapsedSec = action.payload;
    },
    stepChanged(
      state,
      action: PayloadAction<{ step: ModulationStep; index: number }>
    ) {
      state.currentStep = action.payload.step;
      state.currentStepIndex = action.payload.index;
    },
  },
});

export const {
  setIntent,
  setLoading,
  sessionStarted,
  sessionFailed,
  sessionEnded,
  feedbackSubmitted,
  tick,
  stepChanged,
} = sessionSlice.actions;

export default sessionSlice.reducer;
