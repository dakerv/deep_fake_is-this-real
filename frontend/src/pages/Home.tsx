import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Hero } from '../components/Hero';
import { useDetectionContext } from '../contexts/DetectionContext';

export function Home() {
  const navigate = useNavigate();
  const {
    status,
    stage,
    file,
    previewUrl,
    error,
    selectFile,
    analyze,
    reset
  } = useDetectionContext();

  // The moment an assessment is issued, the flow advances to the report.
  useEffect(() => {
    if (status === 'result') {
      navigate('/assessment', { replace: true });
    }
  }, [status, navigate]);

  return (
    <Hero
      status={status}
      stage={stage}
      fileName={file?.name ?? null}
      previewUrl={previewUrl}
      error={error}
      onSelect={selectFile}
      onAnalyze={analyze}
      onReset={reset} />);


}