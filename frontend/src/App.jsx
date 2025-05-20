import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import Layout from './components/Layout';
import SetupPage from './pages/SetupPage';
import NicheResearch from './pages/NicheResearch';
import ContentGeneration from './pages/ContentGeneration';
import UploadPage from './pages/UploadPage';
import AnalyticsPage from './pages/AnalyticsPage';
import NotFoundPage from './pages/NotFoundPage';

function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<Navigate to="/setup" replace />} />
        <Route path="setup" element={<SetupPage />} />
        <Route path="niche-research" element={<NicheResearch />} />
        <Route path="generate-content" element={<ContentGeneration />} />
        <Route path="upload" element={<UploadPage />} />
        <Route path="analytics" element={<AnalyticsPage />} />
        <Route path="*" element={<NotFoundPage />} />
      </Route>
    </Routes>
  );
}

export default App;
