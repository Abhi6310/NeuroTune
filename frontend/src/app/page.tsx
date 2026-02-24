"use client";

import { useCallback } from "react";
import { useRouter } from "next/navigation";
import { startSession } from "@/lib/api";
import { startBinauralBeat } from "@/lib/synth";
import { useAppDispatch, useAppSelector } from "@/stores/hooks";
import {
  setIntent,
  setLoading,
  sessionStarted,
  sessionFailed,
} from "@/stores/sessionSlice";
import PlayerControls from "@/components/PlayerControls";

const CARRIER_FREQ = 200;

export default function Home() {
  const router = useRouter();
  const dispatch = useAppDispatch();
  const { status, intent, error, latencyMs } = useAppSelector((s) => s.session);

  const handleStart = useCallback(async () => {
    dispatch(setLoading());
    const requestStartMs = performance.now();

    try {
      const res = await startSession(intent, 25);
      const schedule = res.data.schedule;

      dispatch(
        sessionStarted({
          schedule,
          sessionId: res.data.session_id,
          startedAt: Date.now(),
          latencyMs: Math.round(performance.now() - requestStartMs),
        })
      );

      await startBinauralBeat(CARRIER_FREQ, schedule.steps[0].binaural_freq, 0.3);
      router.push("/session");
    } catch (e: unknown) {
      dispatch(sessionFailed(e instanceof Error ? e.message : "Unknown error"));
    }
  }, [intent, dispatch, router]);

  return (
    <main className="max-w-2xl mx-auto p-10 font-mono text-white bg-black min-h-screen">
      <h1 className="text-3xl font-bold mb-2">NeuroTune</h1>
      <p className="text-zinc-400 mb-8">Personalized brain-state audio</p>

      <PlayerControls
        status={status}
        intent={intent}
        onIntentChange={(newIntent) => dispatch(setIntent(newIntent))}
        onStart={handleStart}
      />

      {error && <p className="text-red-400 mt-4 text-sm">Error: {error}</p>}

      {latencyMs !== null && (
        <p className="mt-4 text-sm">
          Schedule latency:{" "}
          <span className="font-bold">{latencyMs}ms</span>
          <span className={latencyMs < 3000 ? "text-emerald-400 ml-2" : "text-red-400 ml-2"}>
            {latencyMs < 3000 ? "PASS" : "FAIL — over 3s"}
          </span>
        </p>
      )}
    </main>
  );
}
