import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import Layout from './components/Layout';
import SetupPage from './pages/SetupPage';
import NicheResearch from './pages/NicheResearch';
import ContentGeneration from './pages/ContentGeneration';
import UploadPage from './pages/UploadPage';
import AnalyticsPage from './pages/AnalyticsPage';
import NotFoundPage from './pages/NotFoundPage';
import LoginPage from './pages/LoginPage';
import SocialMediaMarketingPage from './pages/SocialMediaMarketingPage';

// Protected route wrapper component
const ProtectedRoute = ({ children }) => {
  const isAuthenticated = localStorage.getItem('isAuthenticated') === 'true';
  
  if (!isAuthenticated) {
    // Redirect to login if not authenticated
    return <Navigate to="/login" replace />;
  }

  return children;
};

const App = () => {
  return (
    <Routes>
      {/* Public Routes */}
      <Route path="/login" element={<LoginPage />} />
      
      {/* Protected Routes - must be authenticated */}
      <Route path="/" element={
        <ProtectedRoute>
          <Layout />
        </ProtectedRoute>
      }>
        <Route index element={<Navigate to="/setup" replace />} />
        <Route path="setup" element={<SetupPage />} />
        <Route path="niche-research" element={<NicheResearch />} />
        <Route path="generate-content" element={<ContentGeneration />} />
        <Route path="upload" element={<UploadPage />} />
        <Route path="analytics" element={<AnalyticsPage />} />
        <Route path="social-media-marketing" element={<SocialMediaMarketingPage />} />
        
        {/* Routes for new features from the roadmap that aren't implemented yet */}
        <Route path="ai-assistant" element={<div className="p-6 bg-white rounded-lg shadow-md"><h1 className="text-2xl font-bold text-gray-800 mb-4">AI Assistant</h1><p className="text-gray-600">This feature is coming soon in a future update.</p></div>} />
        <Route path="automation" element={<div className="p-6 bg-white rounded-lg shadow-md"><h1 className="text-2xl font-bold text-gray-800 mb-4">Automation Workflows</h1><p className="text-gray-600">This feature is coming soon in a future update.</p></div>} />
        <Route path="scheduler" element={<div className="p-6 bg-white rounded-lg shadow-md"><h1 className="text-2xl font-bold text-gray-800 mb-4">Post Scheduler</h1><p className="text-gray-600">This feature is coming soon in a future update.</p></div>} />
        <Route path="competitor-analysis" element={<div className="p-6 bg-white rounded-lg shadow-md"><h1 className="text-2xl font-bold text-gray-800 mb-4">Competitor Analysis</h1><p className="text-gray-600">This feature is coming soon in a future update.</p></div>} />
        <Route path="news-feed" element={<div className="p-6 bg-white rounded-lg shadow-md"><h1 className="text-2xl font-bold text-gray-800 mb-4">AI News & Updates</h1><p className="text-gray-600">This feature is coming soon in a future update.</p></div>} />
        
        {/* 404 Page for any invalid routes */}
        <Route path="*" element={<NotFoundPage />} />
      </Route>
    </Routes>
  );
};

export default App;
