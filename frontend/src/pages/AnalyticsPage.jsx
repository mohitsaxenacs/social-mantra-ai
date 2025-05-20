import React from 'react';
import { FaChartBar, FaChartLine, FaChartPie } from 'react-icons/fa';

const AnalyticsPage = () => {
  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold text-gray-800 mb-6">Analytics Dashboard</h1>
      
      <div className="bg-white rounded-lg shadow-md p-6">
        <p className="text-gray-600 mb-4">
          This page will show analytics and performance data for your published content.
          The analytics dashboard is coming soon in the next update.
        </p>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6">
          <div className="bg-gray-50 p-4 rounded-lg text-center">
            <FaChartBar className="mx-auto text-3xl text-primary-500 mb-2" />
            <h3 className="font-medium text-gray-700">Performance Metrics</h3>
            <p className="text-sm text-gray-500 mt-1">Coming soon</p>
          </div>
          
          <div className="bg-gray-50 p-4 rounded-lg text-center">
            <FaChartLine className="mx-auto text-3xl text-primary-500 mb-2" />
            <h3 className="font-medium text-gray-700">Growth Tracking</h3>
            <p className="text-sm text-gray-500 mt-1">Coming soon</p>
          </div>
          
          <div className="bg-gray-50 p-4 rounded-lg text-center">
            <FaChartPie className="mx-auto text-3xl text-primary-500 mb-2" />
            <h3 className="font-medium text-gray-700">Audience Insights</h3>
            <p className="text-sm text-gray-500 mt-1">Coming soon</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AnalyticsPage;
