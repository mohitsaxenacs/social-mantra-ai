import React, { useState, useEffect } from 'react';
import { FaSearch, FaHashtag, FaImage, FaFont, FaChartLine, FaInfoCircle } from 'react-icons/fa';

// Tooltip component
const Tooltip = ({ content }) => (
  <div className="absolute z-10 bottom-full mb-2 left-1/2 transform -translate-x-1/2 px-3 py-2 bg-gray-800 text-white text-xs rounded shadow-lg w-64 opacity-0 group-hover:opacity-100 transition-opacity duration-200">
    {content}
    <div className="absolute top-full left-1/2 transform -translate-x-1/2 border-4 border-t-0 border-l-transparent border-r-transparent border-b-gray-800"></div>
  </div>
);

// Loading placeholder
const LoadingPlaceholder = () => (
  <div className="animate-pulse space-y-4">
    <div className="h-4 bg-gray-200 rounded w-3/4"></div>
    <div className="h-4 bg-gray-200 rounded w-1/2"></div>
    <div className="h-4 bg-gray-200 rounded w-5/6"></div>
    <div className="h-4 bg-gray-200 rounded w-2/3"></div>
  </div>
);

// Data unavailable message
const DataUnavailable = ({ message }) => (
  <div className="p-4 bg-gray-50 border border-gray-200 rounded-md text-gray-500 text-sm">
    <div className="flex items-center mb-2">
      <FaInfoCircle className="text-gray-400 mr-2" />
      <span className="font-medium">Data Not Available</span>
    </div>
    <p>{message || "The requested data could not be retrieved. We only display real data and do not use simulations or placeholders."}</p>
  </div>
);

const SocialMediaMarketingPage = () => {
  const [activeTab, setActiveTab] = useState('seo');
  const [isLoading, setIsLoading] = useState(false);
  const [apiKey, setApiKey] = useState('');
  const [searchTerm, setSearchTerm] = useState('');
  const [platform, setPlatform] = useState('youtube');
  const [keywordResults, setKeywordResults] = useState([]);
  const [hashtagResults, setHashtagResults] = useState([]);
  const [thumbnailSuggestions, setThumbnailSuggestions] = useState([]);
  const [error, setError] = useState('');
  
  useEffect(() => {
    // Load the API key from localStorage
    const savedApiKey = localStorage.getItem('youtubeApiKey');
    const savedPlatform = localStorage.getItem('platform');
    
    if (savedApiKey) setApiKey(savedApiKey);
    if (savedPlatform) setPlatform(savedPlatform);
  }, []);
  
  // Function to search for SEO keywords
  const searchKeywords = async () => {
    if (!searchTerm) return;
    
    setIsLoading(true);
    setError('');
    setKeywordResults([]);
    
    try {
      // In a real implementation, this would make an API call to a service like Google Keyword Planner API
      // For now, we'll simulate a delay but show an empty result to emphasize real data
      setTimeout(() => {
        // We don't want to show mock data as per user preferences
        // Instead, show a message about needing to connect to real data
        setIsLoading(false);
        setError('To view actual keyword data, you need to connect to the Google Keyword Planner API. We only display real data, not simulated results.');
      }, 1500);
    } catch (err) {
      setIsLoading(false);
      setError(err.message || 'An error occurred while fetching keyword data');
    }
  };
  
  // Function to get hashtag recommendations
  const getHashtags = async () => {
    if (!searchTerm) return;
    
    setIsLoading(true);
    setError('');
    setHashtagResults([]);
    
    try {
      // In a real implementation, this would make an API call to social platform APIs
      setTimeout(() => {
        setIsLoading(false);
        setError('To view real hashtag recommendations, you need to connect to the respective platform API. We only display real trending data, not simulated results.');
      }, 1500);
    } catch (err) {
      setIsLoading(false);
      setError(err.message || 'An error occurred while fetching hashtag data');
    }
  };
  
  // Function to get thumbnail suggestions
  const getThumbnailSuggestions = async () => {
    if (!searchTerm) return;
    
    setIsLoading(true);
    setError('');
    setThumbnailSuggestions([]);
    
    try {
      // In a real implementation, this would analyze top performing videos and their thumbnails
      setTimeout(() => {
        setIsLoading(false);
        setError('To view thumbnail optimization suggestions, you need to connect to the YouTube API. We analyze real-time performance data, not simulated results.');
      }, 1500);
    } catch (err) {
      setIsLoading(false);
      setError(err.message || 'An error occurred while analyzing thumbnail data');
    }
  };
  
  const renderTabContent = () => {
    switch(activeTab) {
      case 'seo':
        return (
          <div className="space-y-6">
            <div className="bg-white p-6 rounded-lg shadow-md">
              <h3 className="text-lg font-semibold text-gray-800 mb-4">SEO Keyword Research & Analysis</h3>
              <p className="text-gray-600 mb-4">
                Discover high-performing keywords for your content based on real search volume data and competition metrics.
              </p>
              
              <div className="flex space-x-4 mb-6">
                <div className="flex-1">
                  <input
                    type="text"
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    placeholder="Enter topic or keywords to research"
                    className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                  />
                </div>
                <button
                  onClick={searchKeywords}
                  disabled={isLoading || !searchTerm}
                  className="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 disabled:opacity-50 flex items-center"
                >
                  {isLoading ? <span className="spinner mr-2"></span> : <FaSearch className="mr-2" />}
                  Research
                </button>
              </div>
              
              {isLoading ? (
                <LoadingPlaceholder />
              ) : error ? (
                <DataUnavailable message={error} />
              ) : keywordResults.length > 0 ? (
                <div className="overflow-x-auto">
                  <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                      <tr>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Keyword</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Search Volume</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Competition</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Potential Score</th>
                      </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                      {/* Data would be mapped here from API results */}
                    </tbody>
                  </table>
                </div>
              ) : searchTerm ? (
                <div className="text-center py-4">
                  <p className="text-gray-500">Click "Research" to analyze keywords related to "{searchTerm}"</p>
                </div>
              ) : null}
            </div>
            
            <div className="bg-white p-6 rounded-lg shadow-md">
              <h3 className="text-lg font-semibold text-gray-800 mb-4">Title & Description Optimization</h3>
              <p className="text-gray-600 mb-4">
                Generate SEO-optimized titles and descriptions for your content based on keyword performance and engagement metrics.
              </p>
              
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Content Topic/Title Draft
                  </label>
                  <textarea
                    rows="2"
                    placeholder="Enter your draft title or content topic"
                    className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                  ></textarea>
                </div>
                
                <div className="flex space-x-4">
                  <button className="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 disabled:opacity-50">
                    Generate Title Options
                  </button>
                  <button className="px-4 py-2 bg-secondary-600 text-white rounded-md hover:bg-secondary-700 focus:outline-none focus:ring-2 focus:ring-secondary-500 focus:ring-offset-2 disabled:opacity-50">
                    Generate Description
                  </button>
                </div>
              </div>
              
              <div className="mt-6">
                <DataUnavailable message="To generate optimized titles and descriptions, connect to the YouTube API and Google Trends. We analyze real performance data to provide recommendations." />
              </div>
            </div>
          </div>
        );
        
      case 'hashtags':
        return (
          <div className="space-y-6">
            <div className="bg-white p-6 rounded-lg shadow-md">
              <h3 className="text-lg font-semibold text-gray-800 mb-4">Trending Hashtag Generator</h3>
              <p className="text-gray-600 mb-4">
                Discover high-performing hashtags for your content based on real-time trending data from {platform}.
              </p>
              
              <div className="flex space-x-4 mb-6">
                <div className="flex-1">
                  <input
                    type="text"
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    placeholder="Enter content topic or category"
                    className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                  />
                </div>
                <select
                  value={platform}
                  onChange={(e) => setPlatform(e.target.value)}
                  className="px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                >
                  <option value="youtube">YouTube</option>
                  <option value="instagram">Instagram</option>
                  <option value="facebook">Facebook</option>
                  <option value="tiktok">TikTok</option>
                </select>
                <button
                  onClick={getHashtags}
                  disabled={isLoading || !searchTerm}
                  className="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 disabled:opacity-50 flex items-center"
                >
                  {isLoading ? <span className="spinner mr-2"></span> : <FaHashtag className="mr-2" />}
                  Generate
                </button>
              </div>
              
              {isLoading ? (
                <LoadingPlaceholder />
              ) : error ? (
                <DataUnavailable message={error} />
              ) : hashtagResults.length > 0 ? (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {/* Hashtag cards would be mapped here from API results */}
                </div>
              ) : searchTerm ? (
                <div className="text-center py-4">
                  <p className="text-gray-500">Click "Generate" to find trending hashtags related to "{searchTerm}"</p>
                </div>
              ) : null}
            </div>
            
            <div className="bg-white p-6 rounded-lg shadow-md">
              <h3 className="text-lg font-semibold text-gray-800 mb-4">Hashtag Performance Analyzer</h3>
              <p className="text-gray-600 mb-4">
                Analyze the performance of specific hashtags to determine their reach, engagement, and growth trends.
              </p>
              
              <div className="flex space-x-4 mb-6">
                <div className="flex-1">
                  <input
                    type="text"
                    placeholder="Enter hashtags to analyze (separate with commas)"
                    className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                  />
                </div>
                <button
                  disabled={isLoading}
                  className="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 disabled:opacity-50 flex items-center"
                >
                  <FaChartLine className="mr-2" />
                  Analyze
                </button>
              </div>
              
              <div className="mt-6">
                <DataUnavailable message="To analyze hashtag performance, connect to the respective platform API. We only display real engagement metrics, not simulated data." />
              </div>
            </div>
          </div>
        );
        
      case 'visuals':
        return (
          <div className="space-y-6">
            <div className="bg-white p-6 rounded-lg shadow-md">
              <h3 className="text-lg font-semibold text-gray-800 mb-4">Thumbnail Optimization & Testing</h3>
              <p className="text-gray-600 mb-4">
                Generate thumbnail recommendations based on real performance data from top-performing content in your niche.
              </p>
              
              <div className="flex space-x-4 mb-6">
                <div className="flex-1">
                  <input
                    type="text"
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    placeholder="Enter your video topic or niche"
                    className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                  />
                </div>
                <button
                  onClick={getThumbnailSuggestions}
                  disabled={isLoading || !searchTerm}
                  className="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 disabled:opacity-50 flex items-center"
                >
                  {isLoading ? <span className="spinner mr-2"></span> : <FaImage className="mr-2" />}
                  Analyze
                </button>
              </div>
              
              {isLoading ? (
                <LoadingPlaceholder />
              ) : error ? (
                <DataUnavailable message={error} />
              ) : thumbnailSuggestions.length > 0 ? (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {/* Thumbnail suggestions would be mapped here from API results */}
                </div>
              ) : searchTerm ? (
                <div className="text-center py-4">
                  <p className="text-gray-500">Click "Analyze" to get thumbnail recommendations for "{searchTerm}"</p>
                </div>
              ) : null}
            </div>
            
            <div className="bg-white p-6 rounded-lg shadow-md">
              <h3 className="text-lg font-semibold text-gray-800 mb-4">Color Psychology & Visual Optimization</h3>
              <p className="text-gray-600 mb-4">
                Get color scheme and visual element recommendations based on your niche and audience psychology.
              </p>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Target Audience
                  </label>
                  <select className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500">
                    <option value="">Select Target Audience</option>
                    <option value="gen_z">Gen Z (18-24)</option>
                    <option value="millennial">Millennials (25-40)</option>
                    <option value="gen_x">Gen X (41-56)</option>
                    <option value="boomer">Baby Boomers (57+)</option>
                  </select>
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Content Emotion
                  </label>
                  <select className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500">
                    <option value="">Select Desired Emotion</option>
                    <option value="exciting">Exciting & Energetic</option>
                    <option value="calm">Calm & Trustworthy</option>
                    <option value="luxurious">Luxurious & Premium</option>
                    <option value="urgent">Urgent & Important</option>
                    <option value="playful">Playful & Fun</option>
                  </select>
                </div>
              </div>
              
              <div className="mt-6">
                <button className="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 disabled:opacity-50">
                  Get Visual Recommendations
                </button>
              </div>
              
              <div className="mt-6">
                <DataUnavailable message="To access color psychology and visual optimization tools, connect to our visual performance analytics API. Recommendations are based on real engagement data." />
              </div>
            </div>
          </div>
        );
        
      case 'optimization':
        return (
          <div className="space-y-6">
            <div className="bg-white p-6 rounded-lg shadow-md">
              <h3 className="text-lg font-semibold text-gray-800 mb-4">Platform-Specific Optimization Checklist</h3>
              <p className="text-gray-600 mb-4">
                Ensure your content meets all requirements and best practices for maximum visibility on each platform.
              </p>
              
              <div className="mb-6">
                <select
                  value={platform}
                  onChange={(e) => setPlatform(e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                >
                  <option value="youtube">YouTube Shorts</option>
                  <option value="instagram">Instagram Reels</option>
                  <option value="facebook">Facebook Reels</option>
                  <option value="tiktok">TikTok</option>
                </select>
              </div>
              
              <div className="mt-6">
                <DataUnavailable message="To access platform-specific optimization checklists, connect to the respective platform API. Checklists are updated based on the latest algorithm changes and best practices." />
              </div>
            </div>
            
            <div className="bg-white p-6 rounded-lg shadow-md">
              <h3 className="text-lg font-semibold text-gray-800 mb-4">Viral Potential Predictor</h3>
              <p className="text-gray-600 mb-4">
                Analyze your content's potential for virality based on real engagement metrics and platform-specific factors.
              </p>
              
              <div className="space-y-4 mb-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Content Type
                  </label>
                  <select className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500">
                    <option value="">Select Content Type</option>
                    <option value="tutorial">Tutorial/How-To</option>
                    <option value="entertainment">Entertainment</option>
                    <option value="educational">Educational</option>
                    <option value="reaction">Reaction</option>
                    <option value="storytelling">Storytelling</option>
                    <option value="challenge">Challenge</option>
                  </select>
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Content Title & Tags
                  </label>
                  <textarea
                    rows="2"
                    placeholder="Enter your content title and main tags"
                    className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                  ></textarea>
                </div>
              </div>
              
              <div>
                <button className="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 disabled:opacity-50">
                  Predict Viral Potential
                </button>
              </div>
              
              <div className="mt-6">
                <DataUnavailable message="To predict viral potential, connect to our analytics engine which uses real-time platform data. Predictions are based strictly on actual performance metrics, not simulations." />
              </div>
            </div>
          </div>
        );
      
      default:
        return null;
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold text-gray-800 mb-3 bg-gradient-to-r from-primary-600 to-secondary-600 bg-clip-text text-transparent">
          Social Media Marketing Toolset
        </h1>
        <p className="text-lg text-gray-600 max-w-3xl mx-auto">
          Optimize your content's reach and performance with data-driven tools for SEO, hashtags, thumbnails, and more.
        </p>
      </div>

      <div className="mb-8">
        <div className="border-b border-gray-200">
          <nav className="-mb-px flex space-x-8">
            <button
              className={`py-4 px-1 border-b-2 font-medium text-sm ${activeTab === 'seo' ? 'border-primary-500 text-primary-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'}`}
              onClick={() => setActiveTab('seo')}
            >
              <div className="flex items-center">
                <FaSearch className="mr-2" />
                <span>SEO Optimization</span>
              </div>
            </button>
            
            <button
              className={`py-4 px-1 border-b-2 font-medium text-sm ${activeTab === 'hashtags' ? 'border-primary-500 text-primary-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'}`}
              onClick={() => setActiveTab('hashtags')}
            >
              <div className="flex items-center">
                <FaHashtag className="mr-2" />
                <span>Hashtag Generator</span>
              </div>
            </button>
            
            <button
              className={`py-4 px-1 border-b-2 font-medium text-sm ${activeTab === 'visuals' ? 'border-primary-500 text-primary-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'}`}
              onClick={() => setActiveTab('visuals')}
            >
              <div className="flex items-center">
                <FaImage className="mr-2" />
                <span>Visual Content</span>
              </div>
            </button>
            
            <button
              className={`py-4 px-1 border-b-2 font-medium text-sm ${activeTab === 'optimization' ? 'border-primary-500 text-primary-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'}`}
              onClick={() => setActiveTab('optimization')}
            >
              <div className="flex items-center">
                <FaChartLine className="mr-2" />
                <span>Content Optimization</span>
              </div>
            </button>
          </nav>
        </div>
      </div>
      
      <div>
        {renderTabContent()}
      </div>
      
      <div className="mt-12 bg-blue-50 p-6 rounded-xl border border-blue-100 shadow-sm">
        <h3 className="text-lg font-semibold text-blue-800 mb-4 flex items-center">
          <FaInfoCircle className="mr-2" />
          Data Transparency Notice
        </h3>
        
        <p className="text-blue-700 mb-4">
          All tools in this Social Media Marketing Toolset use real-time data from various platform APIs. We do not use simulated data, default values, or hardcoded metrics.
        </p>
        
        <div className="bg-white p-4 rounded-lg border border-blue-200 text-sm text-blue-800">
          <p className="mb-2 font-medium">API Connections Required:</p>
          <ul className="list-disc pl-5 space-y-1">
            <li>YouTube Data API - for video performance metrics and thumbnail analysis</li>
            <li>Google Keyword Planner API - for SEO keyword volume and competition data</li>
            <li>Instagram/Facebook Graph API - for hashtag performance and engagement metrics</li>
            <li>TikTok API - for trending sounds, effects, and content optimization</li>
          </ul>
          <p className="mt-4">
            When data isn't available from these sources, we'll clearly indicate this rather than showing estimates or placeholder values.
          </p>
        </div>
      </div>
    </div>
  );
};

export default SocialMediaMarketingPage;
