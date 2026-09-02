import React from 'react';
import { UploadPanel } from './UploadPanel';
import type { DetectionStage, DetectionStatus } from '../types/detection';

interface HeroProps {
  status: DetectionStatus;
  stage: DetectionStage;
  fileName: string | null;
  previewUrl: string | null;
  error: string | null;
  onSelect: (file: File | null | undefined) => void;
  onAnalyze: () => void;
  onReset: () => void;
}

export function Hero(props: HeroProps) {
  return (
    <section
      id="detection"
      aria-labelledby="hero-headline"
      className="border-b border-rule">
      
      <div className="mx-auto grid max-w-spread gap-10 px-5 py-12 sm:px-8 lg:grid-cols-12 lg:gap-14 lg:px-12 lg:py-20">
        <div className="lg:col-span-7 lg:pr-10">
          <div className="flex items-baseline gap-5 border-b border-ink pb-2">
            <p className="font-mono text-[10px] uppercase tracking-label text-ink">
              Assessment / 001
            </p>
            <p className="font-mono text-[10px] uppercase tracking-label text-gray-soft">
              3-class classifier
            </p>
          </div>

          <h1
            id="hero-headline"
            className="mt-7 font-display uppercase leading-[0.92] tracking-[-0.015em] text-ink"
            style={{ fontSize: 'clamp(2.9rem, 7.1vw, 6.6rem)' }}>
            
            Not everything
            <br />
            you see is{' '}
            <span className="italic lowercase tracking-[-0.02em]">real.</span>
          </h1>

          <div className="mt-8 grid gap-8 sm:grid-cols-12">
            <p className="max-w-[46ch] text-[16px] leading-[1.6] text-graphite sm:col-span-8 sm:text-[17px]">
              Upload an image and let our detection model assess whether it
              appears authentic, face-swapped, or synthetically generated.
            </p>
            <div className="sm:col-span-4 sm:border-l sm:border-rule sm:pl-5">
              <p className="font-mono text-[10px] uppercase tracking-label text-gray-soft">
                Note
              </p>
              <p className="mt-2 font-mono text-[11px] leading-[1.6] text-graphite">
                No account required. Images are not retained.
              </p>
            </div>
          </div>
        </div>

        <div className="lg:col-span-5">
          <UploadPanel {...props} />
        </div>
      </div>
    </section>);

}