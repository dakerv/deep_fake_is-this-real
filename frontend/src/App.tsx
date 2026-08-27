import React from 'react';
import {
  BrowserRouter,
  Navigate,
  Route,
  Routes,
  useLocation } from
'react-router-dom';
import { AnimatePresence, motion } from 'framer-motion';
import { Header } from './components/Header';
import { EditorialSections } from './components/EditorialSections';
import { Footer } from './components/Footer';
import { Home } from './pages/Home';
import { AssessmentPage } from './pages/AssessmentPage';
import { DetectionProvider } from './contexts/DetectionContext';

/**
 * The detection slot at the top of the spread. It holds two states of one
 * flow — the assessment intake (/) and the issued report (/assessment) —
 * and cross-fades between them in place.
 */
function DetectionFlow() {
  const location = useLocation();

  return (
    <AnimatePresence mode="wait" initial={false}>
      <motion.div
        key={location.pathname}
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: -8 }}
        transition={{ duration: 0.24, ease: [0.23, 1, 0.32, 1] }}>
        
        <Routes location={location}>
          <Route path="/" element={<Home />} />
          <Route path="/assessment" element={<AssessmentPage />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </motion.div>
    </AnimatePresence>);

}

export function App() {
  return (
    <BrowserRouter>
      <DetectionProvider>
        <div id="top" className="min-h-screen w-full bg-ivory">
          <Header />
          <main>
            <DetectionFlow />
            <EditorialSections />
          </main>
          <Footer />
        </div>
      </DetectionProvider>
    </BrowserRouter>);

}