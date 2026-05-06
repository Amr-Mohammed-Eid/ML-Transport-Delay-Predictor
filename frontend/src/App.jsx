import React from 'react';
import { BrowserRouter as Router, Routes, Route, useLocation } from 'react-router-dom';
import { AnimatePresence, motion } from 'framer-motion';
import Navigation from './components/Navigation';
import Dashboard from './components/Dashboard';
import Predict from './components/Predict';
import DataAnalysis from './components/DataAnalysis';
import ModelPerformance from './components/ModelPerformance';
import { pageTransition } from './utils/animations';
import './App.css';

function AppContent() {
  const location = useLocation();

  return (
    <div className="App">
      <Navigation />
      <main className="main-content">
        <AnimatePresence mode="wait">
          <Routes location={location} key={location.pathname}>
            <Route
              path="/"
              element={
                <motion.div
                  key="dashboard"
                  initial={pageTransition.initial}
                  animate={pageTransition.animate}
                  exit={pageTransition.exit}
                  transition={pageTransition.transition}
                >
                  <Dashboard />
                </motion.div>
              }
            />
            <Route
              path="/predict"
              element={
                <motion.div
                  key="predict"
                  initial={pageTransition.initial}
                  animate={pageTransition.animate}
                  exit={pageTransition.exit}
                  transition={pageTransition.transition}
                >
                  <Predict />
                </motion.div>
              }
            />
            <Route
              path="/analysis"
              element={
                <motion.div
                  key="analysis"
                  initial={pageTransition.initial}
                  animate={pageTransition.animate}
                  exit={pageTransition.exit}
                  transition={pageTransition.transition}
                >
                  <DataAnalysis />
                </motion.div>
              }
            />
            <Route
              path="/performance"
              element={
                <motion.div
                  key="performance"
                  initial={pageTransition.initial}
                  animate={pageTransition.animate}
                  exit={pageTransition.exit}
                  transition={pageTransition.transition}
                >
                  <ModelPerformance />
                </motion.div>
              }
            />
          </Routes>
        </AnimatePresence>
      </main>
    </div>
  );
}

function App() {
  return (
    <Router>
      <AppContent />
    </Router>
  );
}

export default App;

