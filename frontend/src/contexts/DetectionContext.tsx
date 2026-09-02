import React, { createContext, useContext } from 'react';
import { useDetection } from '../hooks/useDetection';

type DetectionValue = ReturnType<typeof useDetection>;

const DetectionContext = createContext<DetectionValue | null>(null);

export function DetectionProvider({ children }: {children: React.ReactNode;}) {
  const value = useDetection();
  return (
    <DetectionContext.Provider value={value}>
      {children}
    </DetectionContext.Provider>);

}

export function useDetectionContext(): DetectionValue {
  const value = useContext(DetectionContext);
  if (!value) {
    throw new Error('useDetectionContext must be used within a DetectionProvider');
  }
  return value;
}