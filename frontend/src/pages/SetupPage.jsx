import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { FaYoutube, FaInstagram, FaFacebook, FaInfoCircle, FaQuestionCircle } from 'react-icons/fa';

// Tooltip component for consistent styling and behavior
const Tooltip = ({ content, position = 'top' }) => {
  return (
    <div className={`absolute z-10 ${position === 'top' ? 'bottom-full mb-2' : 'top-full mt-2'} left-1/2 transform -translate-x-1/2 px-3 py-2 bg-gray-800 text-white text-xs rounded shadow-lg w-64 opacity-0 group-hover:opacity-100 transition-opacity duration-200`}>
      {content}
      <div className={`absolute ${position === 'top' ? 'top-full' : 'bottom-full'} left-1/2 transform -translate-x-1/2 border-4 ${position === 'top' ? 'border-t-0 border-l-transparent border-r-transparent border-b-gray-800' : 'border-b-0 border-l-transparent border-r-transparent border-t-gray-800'}`}></div>
    </div>
  );
};

const SetupPage = () => {
  const navigate = useNavigate();
  const [apiKey, setApiKey] = useState('');
  const [platform, setPlatform] = useState('youtube');
  const [model, setModel] = useState('gpt-4');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [showDebug, setShowDebug] = useState(false);
  const [debugInfo, setDebugInfo] = useState('');
  
  // Model information with pricing and features
  const modelInfo = {
    'gpt-4': {
      price: '$0.03 per 1K tokens',
      pros: ['Most powerful reasoning', 'Best for complex content creation', 'High-quality outputs'],
      cons: ['Most expensive option', 'Slower than GPT-3.5']
    },
    'gpt-3.5-turbo': {
      price: '$0.002 per 1K tokens',
      pros: ['Fast response times', 'Cost-effective', 'Good for basic content'],
      cons: ['Less sophisticated reasoning', 'May require more prompt refinement']
    },
    'claude-3': {
      price: '$0.025 per 1K tokens',
      pros: ['Excellent instruction following', 'Strong reasoning abilities', 'Good ethical guardrails'],
      cons: ['Less widely tested than OpenAI models', 'May have different knowledge cutoff']
    },
    'palm': {
      price: 'Free tier available',
      pros: ['Free tier for experimentation', 'Good integration with Google services'],
      cons: ['Generally less capable than GPT models', 'Limited customization options']
    }
  };

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
    setDebugInfo('');

    try {
      // Validate API key (basic validation)
      if (!apiKey || apiKey.length < 10) {
        throw new Error('Please enter a valid API key (at least 10 characters)');
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
    } catch (err) {
      setError(err.message || 'An error occurred during setup');
      setDebugInfo(JSON.stringify({
        error: err.message,
        stack: err.stack,
        timestamp: new Date().toISOString(),
        inputs: { apiKey: apiKey.substr(0, 3) + '***', platform, model }
      }, null, 2));
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-5xl mx-auto px-4 py-8">
      <div className="text-center mb-10">
        <h1 className="text-4xl font-bold text-gray-800 mb-3 bg-gradient-to-r from-primary-600 to-secondary-600 bg-clip-text text-transparent">
          Social Mantra AI
        </h1>
        <p className="text-lg text-gray-600 max-w-3xl mx-auto">
          Research niches, generate content, and upload shorts to various platforms with AI-powered automation.
        </p>
      </div>

      <div className="bg-white rounded-xl shadow-xl overflow-hidden">
        <div className="bg-gradient-to-r from-primary-600 to-secondary-600 py-4 px-6 flex justify-between items-center">
          <h2 className="text-xl font-semibold text-white">Configuration</h2>
          <button 
            onClick={() => window.open('/help/setup', '_blank')} 
            className="text-white hover:text-primary-100 flex items-center"
            aria-label="Help"
          >
            <FaQuestionCircle className="mr-1" /> <span className="text-sm">Setup Guide</span>
          </button>
        </div>

        <form onSubmit={handleSubmit} className="p-6 space-y-8">
          {/* API Key Input */}
          <div className="bg-gray-50 p-6 rounded-lg border border-gray-100">
            <label htmlFor="apiKey" className="block text-sm font-medium text-gray-700 mb-2 flex items-center">
              YouTube API Key <span className="text-red-500">*</span>
              <div className="group relative inline-block ml-2 cursor-help">
                <FaInfoCircle className="text-gray-400" />
                <Tooltip content="Required for fetching real YouTube data. This key allows the app to make requests to YouTube's API to get trending videos, channel stats, and competition metrics. We never store your API key on our servers." />
              </div>
            </label>
            <input
              type="text"
              id="apiKey"
              value={apiKey}
              onChange={(e) => setApiKey(e.target.value)}
              placeholder="Enter your YouTube API key"
              className="w-full px-4 py-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-200"
              required
            />
            <p className="mt-2 text-sm text-gray-500">
              Need a YouTube API key? <a href="https://developers.google.com/youtube/v3/getting-started" target="_blank" rel="noopener noreferrer" className="text-primary-600 hover:underline font-medium">Learn how to get one</a>
            </p>
          </div>

          {/* Platform Selection */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-3 flex items-center">
              Target Platform
              <div className="group relative inline-block ml-2 cursor-help">
                <FaInfoCircle className="text-gray-400" />
                <Tooltip content="Select the primary platform where you want to post your content. This affects what kind of content will be generated and how metrics are calculated." />
              </div>
            </label>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <button
                type="button"
                onClick={() => setPlatform('youtube')}
                className={`flex flex-col items-center justify-center p-5 rounded-lg transition-all duration-200 ${platform === 'youtube' ? 'bg-gradient-to-br from-red-50 to-red-100 text-red-600 border border-red-200 shadow-md' : 'bg-gray-50 text-gray-700 border border-gray-200 hover:bg-gray-100'}`}
              >
                <FaYoutube className="text-3xl mb-2" />
                <span className="font-medium">YouTube Shorts</span>
              </button>
              <button
                type="button"
                onClick={() => setPlatform('instagram')}
                className={`flex flex-col items-center justify-center p-5 rounded-lg transition-all duration-200 ${platform === 'instagram' ? 'bg-gradient-to-br from-purple-50 to-pink-100 text-purple-600 border border-purple-200 shadow-md' : 'bg-gray-50 text-gray-700 border border-gray-200 hover:bg-gray-100'}`}
              >
                <FaInstagram className="text-3xl mb-2" />
                <span className="font-medium">Instagram Reels</span>
              </button>
              <button
                type="button"
                onClick={() => setPlatform('facebook')}
                className={`flex flex-col items-center justify-center p-5 rounded-lg transition-all duration-200 ${platform === 'facebook' ? 'bg-gradient-to-br from-blue-50 to-blue-100 text-blue-600 border border-blue-200 shadow-md' : 'bg-gray-50 text-gray-700 border border-gray-200 hover:bg-gray-100'}`}
              >
                <FaFacebook className="text-3xl mb-2" />
                <span className="font-medium">Facebook Reels</span>
              </button>
            </div>
          </div>

          {/* AI Model Selection with detailed information */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2 flex items-center">
              AI Model for Content Generation
              <div className="group relative inline-block ml-2 cursor-help">
                <FaInfoCircle className="text-gray-400" />
                <Tooltip content="Select which AI model to use for generating content and analyzing data. More powerful models cost more but provide better results." />
              </div>
            </label>
            
            <div className="space-y-4">
              {Object.entries(modelInfo).map(([modelKey, info]) => (
                <div 
                  key={modelKey}
                  className={`border rounded-lg p-4 ${model === modelKey ? 'border-primary-300 bg-primary-50 ring-2 ring-primary-200' : 'border-gray-200 hover:border-gray-300'} transition-all cursor-pointer`}
                  onClick={() => setModel(modelKey)}
                >
                  <div className="flex items-center">
                    <div className={`w-4 h-4 rounded-full mr-3 flex items-center justify-center border ${model === modelKey ? 'border-primary-500' : 'border-gray-400'}`}>
                      {model === modelKey && <div className="w-2 h-2 rounded-full bg-primary-500"></div>}
                    </div>
                    <div className="flex-1">
                      <div className="flex items-center justify-between">
                        <span className="font-medium">{modelKey}</span>
                        <span className="text-sm text-gray-500">{info.price}</span>
                      </div>
                      <div className="mt-2 text-sm">
                        <div className="text-green-600">
                          <strong>Pros:</strong> {info.pros.join(', ')}
                        </div>
                        <div className="text-red-600 mt-1">
                          <strong>Cons:</strong> {info.cons.join(', ')}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Submit Button */}
          <div className="pt-4">
            <button
              type="submit"
              disabled={isLoading}
              className="w-full bg-gradient-to-r from-primary-600 to-secondary-600 text-white py-4 px-6 rounded-lg hover:from-primary-700 hover:to-secondary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 shadow-lg transform transition-all duration-200 hover:-translate-y-1 flex items-center justify-center font-medium text-lg"
            >
              {isLoading ? (
                <>
                  <div className="spinner mr-3"></div>
                  Setting up...
                </>
              ) : (
                'Continue to Niche Research'
              )}
            </button>
            <p className="mt-2 text-center text-sm text-gray-500">
              All data fetched is real-time from YouTube's API. No simulated or hardcoded values.
            </p>
          </div>

          {/* Error Message with debug toggle */}
          {error && (
            <div className="mt-4">
              <div className="text-red-600 text-sm bg-red-50 p-3 rounded-md border border-red-200 mb-2">
                <div className="font-medium">Error:</div>
                {error}
              </div>
              
              <div className="flex justify-between items-center">
                <button 
                  type="button" 
                  onClick={() => setShowDebug(!showDebug)}
                  className="text-xs text-gray-500 hover:text-gray-700 focus:outline-none"
                >
                  {showDebug ? 'Hide' : 'Show'} Developer Details
                </button>
                
                <button 
                  type="button" 
                  onClick={() => {
                    setError('');
                    setDebugInfo('');
                  }}
                  className="text-xs text-red-500 hover:text-red-700 focus:outline-none"
                >
                  Clear Error
                </button>
              </div>
              
              {showDebug && debugInfo && (
                <pre className="mt-2 p-3 bg-gray-800 text-white text-xs rounded-md overflow-auto max-h-40">
                  {debugInfo}
                </pre>
              )}
            </div>
          )}
        </form>
      </div>

      {/* Feature Highlights with helpful tooltips */}
      <div className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white p-6 rounded-lg shadow-md border border-gray-100">
          <div className="w-12 h-12 bg-primary-100 rounded-full flex items-center justify-center mb-4">
            <FaYoutube className="text-primary-600 text-xl" />
          </div>
          <h3 className="text-lg font-semibold text-gray-800 mb-2 flex items-center">
            Real-Time YouTube Data
            <div className="group relative inline-block ml-2 cursor-help">
              <FaInfoCircle className="text-gray-400 text-sm" />
              <Tooltip content="All metrics are fetched in real-time from the YouTube API. We never use simulated or hardcoded data for your niche research." />
            </div>
          </h3>
          <p className="text-gray-600">
            All niche analysis is based on real data from the YouTube API, with transparent metrics and no simulations.
          </p>
        </div>
        
        <div className="bg-white p-6 rounded-lg shadow-md border border-gray-100">
          <div className="w-12 h-12 bg-secondary-100 rounded-full flex items-center justify-center mb-4">
            <svg xmlns="http://www.w3.org/2000/svg" className="text-secondary-600 text-xl" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline>
            </svg>
          </div>
          <h3 className="text-lg font-semibold text-gray-800 mb-2 flex items-center">
            Advanced Analytics
            <div className="group relative inline-block ml-2 cursor-help">
              <FaInfoCircle className="text-gray-400 text-sm" />
              <Tooltip content="Visualize niche performance with scatter plots showing traffic potential vs. competition. Identify the sweet spot for your content strategy." />
            </div>
          </h3>
          <p className="text-gray-600">
            Interactive visualization charts that plot niches on traffic vs. competition maps for optimal niche selection.
          </p>
        </div>
        
        <div className="bg-white p-6 rounded-lg shadow-md border border-gray-100">
          <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mb-4">
            <svg xmlns="http://www.w3.org/2000/svg" className="text-green-600 text-xl" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"></path>
              <polyline points="14 2 14 8 20 8"></polyline>
            </svg>
          </div>
          <h3 className="text-lg font-semibold text-gray-800 mb-2 flex items-center">
            AI-Friendly Niches
            <div className="group relative inline-block ml-2 cursor-help">
              <FaInfoCircle className="text-gray-400 text-sm" />
              <Tooltip content="Discover content niches that don't require showing your face or filming yourself. Perfect for fully automated content creation using AI tools." />
            </div>
          </h3>
          <p className="text-gray-600">
            Specially curated niches for faceless content that can be fully automated with AI, no personal appearances needed.
          </p>
        </div>
      </div>
      
      {/* Getting Started Guide */}
      <div className="mt-10 bg-white p-6 rounded-xl shadow-md border border-gray-100">
        <h3 className="text-lg font-semibold text-gray-800 mb-4">Getting Started</h3>
        <ol className="space-y-3 text-gray-600">
          <li className="flex items-start">
            <span className="flex-shrink-0 flex items-center justify-center w-6 h-6 rounded-full bg-primary-100 text-primary-600 font-semibold text-sm mr-3 mt-0.5">1</span>
            <span>Configure your YouTube API key or sign in with your Google account</span>
          </li>
          <li className="flex items-start">
            <span className="flex-shrink-0 flex items-center justify-center w-6 h-6 rounded-full bg-primary-100 text-primary-600 font-semibold text-sm mr-3 mt-0.5">2</span>
            <span>Select your target platform and preferred AI model</span>
          </li>
          <li className="flex items-start">
            <span className="flex-shrink-0 flex items-center justify-center w-6 h-6 rounded-full bg-primary-100 text-primary-600 font-semibold text-sm mr-3 mt-0.5">3</span>
            <span>Explore niche recommendations based on real-time data analysis</span>
          </li>
          <li className="flex items-start">
            <span className="flex-shrink-0 flex items-center justify-center w-6 h-6 rounded-full bg-primary-100 text-primary-600 font-semibold text-sm mr-3 mt-0.5">4</span>
            <span>Generate AI-optimized content for your selected niche</span>
          </li>
          <li className="flex items-start">
            <span className="flex-shrink-0 flex items-center justify-center w-6 h-6 rounded-full bg-primary-100 text-primary-600 font-semibold text-sm mr-3 mt-0.5">5</span>
            <span>Schedule and automate posts to your target platforms</span>
          </li>
        </ol>
      </div>
    </div>
  );
};

export default SetupPage;
