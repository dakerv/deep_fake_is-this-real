import { useCallback, useEffect, useRef, useState } from 'react';
import type {
  Assessment,
  DetectionClass,
  DetectionStage,
  DetectionStatus } from
'../types/detection';

const ACCEPTED = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp'];
const MAX_BYTES = 12 * 1024 * 1024;

const STAGE_SEQUENCE: {stage: DetectionStage;label: string;at: number;}[] = [
{ stage: 'received', label: 'IMAGE RECEIVED', at: 0 },
{ stage: 'preprocessing', label: 'PREPROCESSING', at: 700 },
{ stage: 'analyzing', label: 'ANALYZING', at: 1600 },
{ stage: 'generating', label: 'GENERATING ASSESSMENT', at: 2600 }];


export const STAGE_LABELS = STAGE_SEQUENCE.map((s) => ({
  stage: s.stage,
  label: s.label
}));

function hashString(value: string): number {
  let hash = 2166136261;
  for (let i = 0; i < value.length; i += 1) {
    hash ^= value.charCodeAt(i);
    hash = Math.imul(hash, 16777619);
  }
  return Math.abs(hash);
}

/** Deterministic, plausible 3-class distribution derived from the file itself. */
function buildAssessment(file: File, imageUrl: string, id: string): Assessment {
  const seed = hashString(`${file.name}:${file.size}`);
  const order: DetectionClass[] = ['real', 'synthetic', 'swapped'];
  const predicted = order[seed % 3];
  const top = 71 + (seed >> 3) % 270 / 10;
  const remainder = 100 - top;
  const split = 0.2 + (seed >> 7) % 60 / 100;
  const others = order.filter((c) => c !== predicted);
  const raw: Record<DetectionClass, number> = {
    real: 0,
    swapped: 0,
    synthetic: 0
  };
  raw[predicted] = top;
  raw[others[0]] = remainder * split;
  raw[others[1]] = remainder * (1 - split);

  return {
    id,
    fileName: file.name,
    imageUrl,
    predicted,
    confidence: Number(top.toFixed(1)),
    scores: order.map((c) => ({
      id: c,
      label: c === 'swapped' ? 'FACE-SWAPPED' : c.toUpperCase(),
      probability: Number(raw[c].toFixed(1))
    }))
  };
}

export function useDetection() {
  const [status, setStatus] = useState<DetectionStatus>('empty');
  const [stage, setStage] = useState<DetectionStage>('received');
  const [file, setFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [assessment, setAssessment] = useState<Assessment | null>(null);
  const [error, setError] = useState<string | null>(null);
  const counter = useRef(1);
  const timers = useRef<number[]>([]);

  const clearTimers = useCallback(() => {
    timers.current.forEach((t) => window.clearTimeout(t));
    timers.current = [];
  }, []);

  useEffect(() => clearTimers, [clearTimers]);

  const reset = useCallback(() => {
    clearTimers();
    setStatus('empty');
    setStage('received');
    setFile(null);
    setPreviewUrl((url) => {
      if (url) URL.revokeObjectURL(url);
      return null;
    });
    setAssessment(null);
    setError(null);
  }, [clearTimers]);

  const selectFile = useCallback((next: File | null | undefined) => {
    clearTimers();
    setAssessment(null);
    if (!next) return;
    if (!ACCEPTED.includes(next.type.toLowerCase())) {
      setFile(null);
      setPreviewUrl(null);
      setError(
        `“${next.name}” is not a supported format. This examiner accepts JPG, PNG and WEBP images only.`
      );
      setStatus('error');
      return;
    }
    if (next.size > MAX_BYTES) {
      setFile(null);
      setPreviewUrl(null);
      setError(
        `“${next.name}” exceeds the 12 MB limit. Submit a smaller version of the image.`
      );
      setStatus('error');
      return;
    }
    setError(null);
    setFile(next);
    const url = URL.createObjectURL(next);
    setPreviewUrl((prev) => {
      if (prev) URL.revokeObjectURL(prev);
      return url;
    });
    setStatus('ready');
  }, [clearTimers]);

  const analyze = useCallback(() => {
    if (!file || !previewUrl) return;
    setStatus('analyzing');
    setStage('received');
    STAGE_SEQUENCE.forEach(({ stage: s, at }) => {
      if (at === 0) return;
      timers.current.push(window.setTimeout(() => setStage(s), at));
    });
    timers.current.push(
      window.setTimeout(() => {
        const id = String(counter.current).padStart(3, '0');
        counter.current += 1;
        setAssessment(buildAssessment(file, previewUrl, id));
        setStatus('result');
      }, 3500)
    );
  }, [file, previewUrl]);

  return {
    status,
    stage,
    file,
    previewUrl,
    assessment,
    error,
    selectFile,
    analyze,
    reset
  };
}