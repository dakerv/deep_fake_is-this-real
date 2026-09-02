import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Assessment } from '../components/Assessment';
import { useDetectionContext } from '../contexts/DetectionContext';
import { sampleAssessment } from '../data/content';

export function AssessmentPage() {
  const navigate = useNavigate();
  const { assessment, reset } = useDetectionContext();
  const report = assessment ?? sampleAssessment;

  // The report opens the spread, so the reader starts at the top of it.
  useEffect(() => {
    window.scrollTo({ top: 0, behavior: 'auto' });
  }, []);

  const handleCheckAnother = () => {
    reset();
    navigate('/');
    window.scrollTo({ top: 0, behavior: 'auto' });
  };

  return (
    <Assessment
      report={report}
      isSample={!assessment}
      onCheckAnother={handleCheckAnother} />);


}