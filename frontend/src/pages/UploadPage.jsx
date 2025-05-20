import React from 'react';
import { FaCloudUploadAlt } from 'react-icons/fa';

const UploadPage = () => {
  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold text-gray-800 mb-6">Upload to Social Media</h1>
      
      <div className="bg-white rounded-lg shadow-md p-6">
        <p className="text-gray-600 mb-4">
          This page will allow you to upload your generated content to various social media platforms.
          The upload functionality is coming soon in the next update.
        </p>
        
        <div className="flex items-center justify-center border-2 border-dashed border-gray-300 rounded-lg p-12 mt-6">
          <div className="text-center">
            <FaCloudUploadAlt className="mx-auto text-5xl text-gray-400 mb-3" />
            <h3 className="text-lg font-medium text-gray-700">Upload Feature Coming Soon</h3>
            <p className="text-gray-500 mt-1">
              We're building integrations with YouTube, TikTok, and Instagram.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default UploadPage;
