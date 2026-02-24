"use client";

import { useState } from "react";

interface FeedbackModalProps {
  onSubmit: (rating: number, note: string) => void;
  onClose: () => void;
}

export default function FeedbackModal({ onSubmit, onClose }: FeedbackModalProps) {
  const [rating, setRating] = useState(0);
  const [note, setNote] = useState("");

  const handleSubmit = () => {
    if (rating === 0) return;
    onSubmit(rating, note);
  };

  return (
    <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50">
      <div className="bg-zinc-900 border border-zinc-700 rounded-xl p-8 w-full max-w-md space-y-6">
        <h2 className="text-xl font-semibold text-white">Session Complete</h2>

        <div>
          <p className="text-zinc-400 text-sm mb-3">How was this session?</p>
          <div className="flex gap-2">
            {[1, 2, 3, 4, 5].map((star) => (
              <button
                key={star}
                onClick={() => setRating(star)}
                className={`text-2xl transition-colors ${
                  star <= rating ? "text-yellow-400" : "text-zinc-600 hover:text-zinc-400"
                }`}
              >
                ★
              </button>
            ))}
          </div>
        </div>

        <div>
          <label className="text-zinc-400 text-sm block mb-2">Notes (optional)</label>
          <textarea
            value={note}
            onChange={(e) => setNote(e.target.value)}
            rows={3}
            maxLength={1000}
            placeholder="How did you feel? Any observations..."
            className="w-full bg-zinc-800 border border-zinc-700 rounded px-3 py-2 text-white text-sm resize-none placeholder:text-zinc-600 focus:outline-none focus:border-zinc-500"
          />
        </div>

        <div className="flex gap-3 justify-end">
          <button
            onClick={onClose}
            className="px-4 py-2 text-sm text-zinc-400 hover:text-white transition-colors"
          >
            Skip
          </button>
          <button
            onClick={handleSubmit}
            disabled={rating === 0}
            className="px-5 py-2 text-sm bg-emerald-600 hover:bg-emerald-500 disabled:bg-zinc-700 disabled:text-zinc-500 text-white rounded font-medium transition-colors"
          >
            Submit
          </button>
        </div>
      </div>
    </div>
  );
}
