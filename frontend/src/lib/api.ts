const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface ModulationStep {
  timestamp_sec: number;
  target_bpm: number;
  binaural_freq: number;
  ramp_duration_sec: number;
  layer: string;
}

export interface ModulationSchedule {
  intent: string;
  total_duration_sec: number;
  steps: ModulationStep[];
}

export interface SessionStartResponse {
  success: boolean;
  message: string;
  data: {
    session_id: number;
    schedule: ModulationSchedule;
  };
}

export async function startSession(
  intent: string,
  durationMinutes: number = 25
): Promise<SessionStartResponse> {
  const res = await fetch(`${API_BASE}/sessions/start`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ intent, duration_minutes: durationMinutes }),
  });
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

export interface SessionEndResponse {
  session_id: number;
  duration_sec: number;
}

export async function endSession(
  sessionId: number,
  rating?: number,
  feedbackNote?: string
): Promise<SessionEndResponse> {
  const res = await fetch(`${API_BASE}/sessions/${sessionId}/end`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ rating, feedback_note: feedbackNote }),
  });
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

export interface SessionRecord {
  id: number;
  user_id: number | null;
  intent: string;
  duration_sec: number | null;
  started_at: string;
  ended_at: string | null;
  rating: number | null;
  feedback_note: string | null;
}

export async function getSessionHistory(
  userId: number,
  limit: number = 20,
  offset: number = 0
): Promise<{ success: boolean; data: { sessions: SessionRecord[]; limit: number; offset: number } }> {
  const params = new URLSearchParams({
    user_id: String(userId),
    limit: String(limit),
    offset: String(offset),
  });
  const res = await fetch(`${API_BASE}/sessions/history?${params}`);
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}
