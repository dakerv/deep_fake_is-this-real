import React, { useRef, useState } from 'react';
import { motion } from 'framer-motion';
import { UploadIcon, AlertTriangleIcon } from 'lucide-react';
import { STAGE_LABELS } from '../hooks/useDetection';
import type { DetectionStage, DetectionStatus } from '../types/detection';

interface UploadPanelProps {
  status: DetectionStatus;
  stage: DetectionStage;
  fileName: string | null;
  previewUrl: string | null;
  error: string | null;
  onSelect: (file: File | null | undefined) => void;
  onAnalyze: () => void;
  onReset: () => void;
}

function RegistrationMarks() {
  const corners = [
  'left-2 top-2 border-l border-t',
  'right-2 top-2 border-r border-t',
  'left-2 bottom-2 border-l border-b',
  'right-2 bottom-2 border-r border-b'];

  return (
    <>
      {corners.map((c) =>
      <span
        key={c}
        aria-hidden="true"
        className={`pointer-events-none absolute h-4 w-4 border-paper/40 ${c}`} />

      )}
    </>);

}

export function UploadPanel({
  status,
  stage,
  fileName,
  previewUrl,
  error,
  onSelect,
  onAnalyze,
  onReset
}: UploadPanelProps) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [dragging, setDragging] = useState(false);

  const browse = () => inputRef.current?.click();
  const activeIndex = STAGE_LABELS.findIndex((s) => s.stage === stage);

  return (
    <div>
      <div className="flex items-baseline justify-between border-b border-ink pb-2">
        <p className="font-mono text-[10px] uppercase tracking-label text-ink">
          Examine an image · Drop here or browse
        </p>
        <p className="hidden font-mono text-[10px] uppercase tracking-label text-gray-soft sm:block">
          Fig. A
        </p>
      </div>

      <div
        onDragOver={(e) => {
          e.preventDefault();
          setDragging(true);
        }}
        onDragLeave={() => setDragging(false)}
        onDrop={(e) => {
          e.preventDefault();
          setDragging(false);
          onSelect(e.dataTransfer.files?.[0]);
        }}
        className={`relative mt-3 bg-slate-plate transition-colors duration-200 ease-out ${
        dragging ? 'bg-slate-deep' : ''}`
        }>
        
        <RegistrationMarks />
        <input
          ref={inputRef}
          type="file"
          accept="image/jpeg,image/png,image/webp"
          className="sr-only"
          onChange={(e) => onSelect(e.target.files?.[0])} />
        

        {/* EMPTY */}
        {status === 'empty' &&
        <button
          type="button"
          onClick={browse}
          className="flex min-h-[340px] w-full flex-col items-center justify-center gap-5 px-8 py-14 text-center lg:min-h-[420px]">
          
            <span className="flex h-14 w-14 items-center justify-center border border-paper/40">
              <UploadIcon className="h-5 w-5 text-paper" strokeWidth={1.25} />
            </span>
            <span className="max-w-[22ch] font-display text-[24px] leading-[1.15] text-paper">
              Drop an image here
            </span>
            <span className="font-mono text-[10px] uppercase tracking-label text-paper/70">
              or{' '}
              <span className="text-paper underline decoration-paper/50 underline-offset-4">
                browse your device
              </span>
            </span>
          </button>
        }

        {/* READY / ANALYZING / RESULT — preview held in the plate */}
        {previewUrl && status !== 'empty' && status !== 'error' &&
        <div className="p-3">
            <div className="relative">
              <img
              src={previewUrl}
              alt={fileName ? `Selected image: ${fileName}` : 'Selected image'}
              className={`h-[300px] w-full object-cover transition-opacity duration-200 ease-out lg:h-[360px] ${
              status === 'analyzing' ? 'opacity-45' : 'opacity-100'}`
              } />
            
              {status === 'analyzing' &&
            <div className="absolute inset-0 flex items-end bg-ink/45 p-4">
                  <ol className="w-full space-y-1.5">
                    {STAGE_LABELS.map((s, i) =>
                <li
                  key={s.stage}
                  className={`flex items-center gap-3 font-mono text-[10px] uppercase tracking-label transition-colors duration-200 ease-out ${
                  i <= activeIndex ? 'text-paper' : 'text-paper/40'}`
                  }>
                  
                        <span className="w-6">{`0${i + 1}`}</span>
                        <span>{s.label}</span>
                        <span className="ml-auto text-paper/60">
                          {i < activeIndex ?
                    'complete' :
                    i === activeIndex ?
                    'in progress' :
                    ''}
                        </span>
                      </li>
                )}
                  </ol>
                </div>
            }
            </div>

            {status === 'analyzing' ?
          <div className="mt-3">
                <div className="h-[2px] w-full bg-paper/20">
                  <motion.div
                className="h-full bg-paper"
                initial={{ width: '4%' }}
                animate={{ width: '100%' }}
                transition={{ duration: 3.4, ease: 'linear' }} />
              
                </div>
                <p className="mt-2 font-mono text-[10px] uppercase tracking-label text-paper/70">
                  Working · {fileName}
                </p>
              </div> :

          <div className="mt-3 flex flex-wrap items-center justify-between gap-3">
                <div>
                  <p className="font-mono text-[10px] uppercase tracking-label text-paper">
                    {status === 'result' ? 'Assessment issued' : 'Image ready'}
                  </p>
                  <p className="mt-1 max-w-[28ch] truncate font-mono text-[10px] text-paper/60">
                    {fileName}
                  </p>
                </div>
                {status === 'ready' ?
            <div className="flex items-center gap-4">
                    <button
                type="button"
                onClick={browse}
                className="font-mono text-[10px] uppercase tracking-label text-paper/70 underline decoration-paper/40 underline-offset-4 transition-colors duration-150 ease-out hover:text-paper">
                
                      Replace
                    </button>
                    <button
                type="button"
                onClick={onAnalyze}
                className="bg-paper px-5 py-2.5 font-mono text-[10px] uppercase tracking-label text-ink transition-colors duration-150 ease-out hover:bg-ivorydeep">
                
                      Analyze image
                    </button>
                  </div> :

            <a
              href="#assessment"
              className="bg-paper px-5 py-2.5 font-mono text-[10px] uppercase tracking-label text-ink transition-colors duration-150 ease-out hover:bg-ivorydeep">
              
                    Read assessment ↓
                  </a>
            }
              </div>
          }
          </div>
        }

        {/* ERROR */}
        {status === 'error' &&
        <div className="flex min-h-[340px] flex-col justify-center gap-4 px-8 py-14 lg:min-h-[420px]">
            <div className="flex items-center gap-3 border-b border-paper/30 pb-3">
              <AlertTriangleIcon
              className="h-4 w-4 text-paper"
              strokeWidth={1.5} />
            
              <p className="font-mono text-[10px] uppercase tracking-label text-paper">
                Submission rejected
              </p>
            </div>
            <p className="max-w-[38ch] font-display text-[22px] leading-[1.25] text-paper">
              {error}
            </p>
            <div className="flex items-center gap-4">
              <button
              type="button"
              onClick={browse}
              className="bg-paper px-5 py-2.5 font-mono text-[10px] uppercase tracking-label text-ink transition-colors duration-150 ease-out hover:bg-ivorydeep">
              
                Choose another file
              </button>
              <button
              type="button"
              onClick={onReset}
              className="font-mono text-[10px] uppercase tracking-label text-paper/70 underline decoration-paper/40 underline-offset-4 transition-colors duration-150 ease-out hover:text-paper">
              
                Dismiss
              </button>
            </div>
          </div>
        }
      </div>

      <div className="mt-2 flex flex-wrap items-baseline justify-between gap-2 border-t border-rule pt-2">
        <p className="font-mono text-[10px] uppercase tracking-label text-gray-soft">
          Supported formats: JPG · PNG · WEBP
        </p>
        <p className="font-mono text-[10px] uppercase tracking-label text-gray-soft">
          Max 12 MB
        </p>
      </div>
    </div>);

}