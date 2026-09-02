export type DetectionClass = 'real' | 'swapped' | 'synthetic';

export interface ClassScore {
  id: DetectionClass;
  label: string;
  probability: number;
}

export interface Assessment {
  id: string;
  fileName: string;
  imageUrl: string;
  predicted: DetectionClass;
  confidence: number;
  scores: ClassScore[];
}

export type DetectionStage =
'received' |
'preprocessing' |
'analyzing' |
'generating';

export type DetectionStatus =
'empty' |
'ready' |
'analyzing' |
'result' |
'error';

export const CLASS_LABELS: Record<DetectionClass, string> = {
  real: 'REAL',
  swapped: 'FACE-SWAPPED',
  synthetic: 'SYNTHETIC'
};

export const VERDICT_LABELS: Record<DetectionClass, string> = {
  real: 'LIKELY AUTHENTIC',
  swapped: 'LIKELY FACE-SWAPPED',
  synthetic: 'LIKELY SYNTHETIC'
};