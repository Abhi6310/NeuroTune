"use client";

import { useEffect, useRef } from "react";
import * as Tone from "tone";
import { connectNode, disconnectNode } from "@/lib/synth";

interface AudioVisualizerProps {
  isActive: boolean;
}

export default function AudioVisualizer({ isActive }: AudioVisualizerProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const animationFrameRef = useRef<number | null>(null);

  useEffect(() => {
    if (!isActive) return;

    const analyser = new Tone.Analyser("waveform", 256);
    connectNode(analyser);

    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const draw = () => {
      const waveformValues = analyser.getValue() as Float32Array;
      const canvasWidth = canvas.width;
      const canvasHeight = canvas.height;

      ctx.fillStyle = "#09090b";
      ctx.fillRect(0, 0, canvasWidth, canvasHeight);

      ctx.strokeStyle = "#10b981";
      ctx.lineWidth = 2;
      ctx.beginPath();
      for (let i = 0; i < waveformValues.length; i++) {
        const x = (i / waveformValues.length) * canvasWidth;
        const y = ((waveformValues[i] + 1) / 2) * canvasHeight;
        i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
      }
      ctx.stroke();

      animationFrameRef.current = requestAnimationFrame(draw);
    };

    animationFrameRef.current = requestAnimationFrame(draw);

    return () => {
      if (animationFrameRef.current) cancelAnimationFrame(animationFrameRef.current);
      disconnectNode(analyser);
      analyser.dispose();
    };
  }, [isActive]);

  return (
    <canvas
      ref={canvasRef}
      width={600}
      height={80}
      className="w-full rounded border border-zinc-800 bg-zinc-950"
    />
  );
}
