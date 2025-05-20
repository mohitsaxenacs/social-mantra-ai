import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { FaYoutube, FaInstagram, FaTiktok } from 'react-icons/fa';

const SetupPage = () => {
  const navigate = useNavigate();
  const [apiKey, setApiKey] = useState('');
  const [platform, setPlatform] = useState('youtube');
  const [model, setModel] = useState('gpt-4');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  // Load saved settings from localStorage on component mount
  useEffect(() => {
    const savedApiKey = localStorage.getItem('youtubeApiKey');
    const savedPlatform = localStorage.getItem('platform');
    const savedModel = localStorage.getItem('aiModel');

    if (savedApiKey) setApiKey(savedApiKey);
    if (savedPlatform) setPlatform(savedPlatform);
    if (savedModel) setModel(savedModel);
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    // Validate API key (basic validation)
    if (!apiKey || apiKey.length < 10) {
      setError('Please enter a valid API key');
      setIsLoading(false);
      return;
    }

    // Save settings to localStorage
    localStorage.setItem('youtubeApiKey', apiKey);
    localStorage.setItem('platform', platform);
    localStorage.setItem('aiModel', model);

    // For this demo, we're not actually validating the API key with YouTube
    // In a real app, you would make an API call to verify the key
    setTimeout(() => {
      setIsLoading(false);
      navigate('/niche-research');
    }, 1000);
  };

  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold text-gray-800 mb-6">Welcome to Social Media Shorts Automation</h1>
      <p className="text-gray-600 mb-8">
        This tool helps you research niches, generate content, and upload shorts to various platforms.
        Let's get you set up!
      </p>

      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-semibold text-gray-700 mb-4">Configuration</h2>

        <form onSubmit={handleSubmit}>
          {/* API Key Input */}
          <div className="mb-6">
            <label htmlFor="apiKey" className="block text-sm font-medium text-gray-700 mb-2">
              YouTube API Key <span className="text-red-500">*</span>
            </label>
            <input
              type="text"
              id="apiKey"
              value={apiKey}
              onChange={(e) => setApiKey(e.target.value)}
              placeholder="Enter your YouTube API key"
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
              required
            />
            <p className="mt-1 text-sm text-gray-500">
              Need a YouTube API key? <a href="https://developers.google.com/youtube/v3/getting-started" target="_blank" rel="noopener noreferrer" className="text-primary-600 hover:underline">Learn how to get one</a>
            </p>
          </div>

          {/* Platform Selection */}
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Target Platform
            </label>
            <div className="flex space-x-4">
              <button
                type="button"
                onClick={() => setPlatform('youtube')}
                className={`flex items-center justify-center px-4 py-2 rounded-md ${platform === 'youtube' ? 'bg-red-100 text-red-600 border border-red-200' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}`}
              >
                <FaYoutube className="mr-2" /> YouTube Shorts
              </button>
              <button
                type="button"
                onClick={() => setPlatform('instagram')}
                className={`flex items-center justify-center px-4 py-2 rounded-md ${platform === 'instagram' ? 'bg-purple-100 text-purple-600 border border-purple-200' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}`}
              >
                <FaInstagram className="mr-2" /> Instagram Reels
              </button>
              <button
                type="button"
                onClick={() => setPlatform('tiktok')}
                className={`flex items-center justify-center px-4 py-2 rounded-md ${platform === 'tiktok' ? 'bg-blue-100 text-blue-600 border border-blue-200' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}`}
              >
                <FaTiktok className="mr-2" /> TikTok
              </button>
            </div>
          </div>

          {/* AI Model Selection */}
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              AI Model for Content Generation
            </label>
            <select
              value={model}
              onChange={(e) => setModel(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
            >
              <option value="gpt-4">GPT-4 (Most Powerful)</option>
              <option value="gpt-3.5-turbo">GPT-3.5 Turbo (Faster)</option>
              <option value="claude-3">Claude 3 (Alternative)</option>
              <option value="palm">PaLM (Google)</option>
            </select>
          </div>

          {/* Submit Button */}
          <div className="mt-8">
            <button
              type="submit"
              disabled={isLoading}
              className="w-full bg-primary-600 text-white py-3 px-4 rounded-md hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 flex items-center justify-center"
            >
              {isLoading ? (
                <>
                  <div className="spinner mr-2"></div>
                  Setting up...
                </>
              ) : (
                'Continue to Niche Research'
              )}
            </button>
          </div>

          {/* Error Message */}
          {error && (
            <div className="mt-4 text-red-600 text-sm">{error}</div>
          )}
        </form>
      </div>
    </div>
  );
};

export default SetupPage;
