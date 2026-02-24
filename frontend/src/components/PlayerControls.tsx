"use client";

const INTENTS = [
  "Deep Focus - Coding",
  "Deep Focus - Reading",
  "Relaxation - Meditation",
  "Relaxation - Wind Down",
  "Sleep - Deep Rest",
];

interface PlayerControlsProps {
  status: "idle" | "loading" | "playing" | "ended";
  intent?: string;
  onIntentChange?: (intent: string) => void;
  onStart?: () => void;
  onStop?: () => void;
  volume?: number;
  onVolumeChange?: (newVolume: number) => void;
}

export default function PlayerControls({
  status,
  intent = "",
  onIntentChange,
  onStart,
  onStop,
  volume = 0.3,
  onVolumeChange,
}: PlayerControlsProps) {
  return (
    <div className="space-y-4">
      {status === "idle" && (
        <div className="flex items-center gap-2">
          <label className="text-zinc-400 text-sm">Intent</label>
          <select
            value={intent}
            onChange={(e) => onIntentChange?.(e.target.value)}
            className="bg-zinc-900 border border-zinc-700 rounded px-3 py-1.5 text-white text-sm"
          >
            {INTENTS.map((label) => (
              <option key={label} value={label}>
                {label}
              </option>
            ))}
          </select>
        </div>
      )}

      <div className="flex items-center gap-4">
        {status === "idle" && (
          <button
            onClick={onStart}
            className="bg-emerald-600 hover:bg-emerald-500 text-white px-6 py-2 rounded font-medium transition-colors"
          >
            Start Session
          </button>
        )}
        {status === "loading" && (
          <p className="text-yellow-400 animate-pulse text-sm">Generating schedule...</p>
        )}
        {status === "playing" && (
          <>
            <button
              onClick={onStop}
              className="bg-red-600 hover:bg-red-500 text-white px-6 py-2 rounded font-medium transition-colors"
            >
              Stop
            </button>
            <label className="flex items-center gap-2 text-sm text-zinc-400">
              Vol
              <input
                type="range"
                min={0}
                max={1}
                step={0.01}
                value={volume}
                onChange={(e) => onVolumeChange?.(Number(e.target.value))}
                className="w-28 accent-emerald-500"
              />
              <span className="text-white w-8">{Math.round(volume * 100)}%</span>
            </label>
          </>
        )}
      </div>
    </div>
  );
}
