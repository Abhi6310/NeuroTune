"use client";

import { useEffect, useCallback, useState } from "react";
import { useRouter } from "next/navigation";
import { useAppDispatch, useAppSelector } from "@/stores/hooks";
import {
  sessionEnded,
  feedbackSubmitted,
  tick,
  stepChanged,
} from "@/stores/sessionSlice";
import { stopAll, updateBinauralBeat, setVolume } from "@/lib/synth";
import { endSession } from "@/lib/api";
import PlayerControls from "@/components/PlayerControls";
import AudioVisualizer from "@/components/AudioVisualizer";
import SessionTimer from "@/components/SessionTimer";
import FeedbackModal from "@/components/FeedbackModal";

const CARRIER_FREQ = 200;

export default function SessionPage() {
  const router = useRouter();
  const dispatch = useAppDispatch();
  const { status, sessionId, schedule, currentStep, currentStepIndex, elapsedSec, startedAt } =
    useAppSelector((s) => s.session);

  const [volumeLevel, setVolumeLevel] = useState(0.3);

  // Redirect to dashboard when no active session — covers direct URL access and post-feedback reset
  useEffect(() => {
    if (status === "idle") router.replace("/");
  }, [status, router]);

  // Timer anchored to startedAt from Redux so elapsed is accurate if the component remounts
  useEffect(() => {
    if (status !== "playing" || startedAt === null) return;

    const interval = setInterval(() => {
      dispatch(tick(Math.floor((Date.now() - startedAt) / 1000)));
    }, 1000);

    return () => clearInterval(interval);
  }, [status, startedAt, dispatch]);

  useEffect(() => {
    if (!schedule || status !== "playing") return;

    const steps = schedule.steps;
    for (let i = steps.length - 1; i >= 0; i--) {
      if (elapsedSec >= steps[i].timestamp_sec) {
        if (i !== currentStepIndex) {
          dispatch(stepChanged({ step: steps[i], index: i }));
          updateBinauralBeat(CARRIER_FREQ, steps[i].binaural_freq, steps[i].ramp_duration_sec);
        }
        break;
      }
    }
  }, [elapsedSec, schedule, status, currentStepIndex, dispatch]);

  // Dispose audio on unmount — guard against navigating away mid-session
  useEffect(() => {
    return () => stopAll();
  }, []);

  const handleStop = useCallback(() => {
    stopAll();
    dispatch(sessionEnded());
  }, [dispatch]);

  const handleVolumeChange = useCallback((newVolume: number) => {
    setVolumeLevel(newVolume);
    setVolume(newVolume);
  }, []);

  const handleFeedbackSubmit = useCallback(
    async (rating: number, feedbackNote: string) => {
      if (sessionId !== null) {
        try {
          await endSession(sessionId, rating, feedbackNote);
        } catch {
          // Best effort — feedback loss is acceptable; don't block navigation
        }
      }
      dispatch(feedbackSubmitted());
    },
    [sessionId, dispatch]
  );

  const handleFeedbackSkip = useCallback(() => {
    dispatch(feedbackSubmitted());
  }, [dispatch]);

  if (status === "idle") return null;

  return (
    <main className="max-w-2xl mx-auto p-10 font-mono text-white bg-black min-h-screen">
      <h1 className="text-3xl font-bold mb-2">NeuroTune</h1>
      <p className="text-zinc-400 mb-8">{schedule?.intent ?? "Session active"}</p>

      <div className="space-y-6">
        <AudioVisualizer isActive={status === "playing"} />

        <SessionTimer
          elapsedSec={elapsedSec}
          totalSec={schedule?.total_duration_sec ?? 0}
        />

        <PlayerControls
          status={status}
          onStop={handleStop}
          volume={volumeLevel}
          onVolumeChange={handleVolumeChange}
        />

        {currentStep && status === "playing" && (
          <div className="p-4 border border-zinc-700 rounded-lg bg-zinc-900">
            <h3 className="text-lg font-semibold mb-3">Now Playing</h3>
            <div className="grid grid-cols-2 gap-2 text-sm">
              <p className="text-zinc-400">Step:</p>
              <p>{currentStepIndex + 1} / {schedule?.steps.length}</p>
              <p className="text-zinc-400">Binaural Freq:</p>
              <p className="text-emerald-400 font-bold">{currentStep.binaural_freq} Hz</p>
              <p className="text-zinc-400">Target BPM:</p>
              <p>{currentStep.target_bpm}</p>
              <p className="text-zinc-400">Carrier:</p>
              <p>
                {CARRIER_FREQ} Hz L / {CARRIER_FREQ + currentStep.binaural_freq} Hz R
              </p>
            </div>
          </div>
        )}
      </div>

      {status === "ended" && (
        <FeedbackModal onSubmit={handleFeedbackSubmit} onClose={handleFeedbackSkip} />
      )}
    </main>
  );
}
