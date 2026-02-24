"use client";

interface SessionTimerProps {
  elapsedSec: number;
  totalSec: number;
}

function toMMSS(totalSeconds: number): string {
  const minutes = Math.floor(totalSeconds / 60).toString().padStart(2, "0");
  const seconds = (totalSeconds % 60).toString().padStart(2, "0");
  return `${minutes}:${seconds}`;
}

export default function SessionTimer({ elapsedSec, totalSec }: SessionTimerProps) {
  const remainingSec = Math.max(0, totalSec - elapsedSec);
  const progressPct = totalSec > 0 ? Math.min(elapsedSec / totalSec, 1) * 100 : 0;

  return (
    <div className="space-y-2">
      <div className="flex justify-between text-sm text-zinc-400">
        <span>
          Elapsed: <span className="text-white font-mono">{toMMSS(elapsedSec)}</span>
        </span>
        <span>
          Remaining: <span className="text-white font-mono">{toMMSS(remainingSec)}</span>
        </span>
      </div>
      <div className="h-1.5 w-full bg-zinc-800 rounded-full overflow-hidden">
        <div
          className="h-full bg-emerald-500 rounded-full transition-all duration-1000"
          style={{ width: `${progressPct}%` }}
        />
      </div>
    </div>
  );
}
