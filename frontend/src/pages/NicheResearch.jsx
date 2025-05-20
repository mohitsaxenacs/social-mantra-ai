import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { ScatterChart, Scatter, XAxis, YAxis, ZAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Label } from 'recharts';
import { FaSearch, FaExclamationTriangle, FaArrowLeft, FaInfoCircle } from 'react-icons/fa';

// Import API functions
import { fetchTrendingNiches, fetchLowCompetitionNiches, fetchAiFriendlyNiches, searchNiche } from '../api/youtubeApi';

// Custom tooltip component for the scatter chart
const CustomTooltip = ({ active, payload }) => {
  if (active && payload && payload.length) {
    const data = payload[0].payload;
    return (
      <div className="bg-white p-3 shadow-md rounded-md border border-gray-200">
        <p className="font-bold text-gray-800">{data.name}</p>
        <p className="text-sm text-gray-600">Traffic: {data.traffic_potential ? data.traffic_potential.toFixed(1) : 'N/A'}</p>
        <p className="text-sm text-gray-600">Competition: {data.competition ? data.competition.toFixed(1) : 'N/A'}</p>
        <p className="text-sm text-gray-600">Opportunity Score: {data.score ? data.score.toFixed(1) : 'N/A'}</p>
        <p className="text-sm text-gray-600">Avg. Views: {data.avg_views_formatted || 'N/A'}</p>
        <p className="text-sm text-gray-600">Videos: {data.video_count}</p>
      </div>
    );
  }
  return null;
};

const NicheCard = ({ niche, onClick, isSelected }) => {
  // Handle missing data gracefully
  const competition = niche.competition !== null ? niche.competition : 'N/A';
  const trafficPotential = niche.traffic_potential !== null ? niche.traffic_potential : 'N/A';
  const score = niche.score !== null ? niche.score : 'N/A';
  
  // Determine competition level text and color
  let competitionLevel = 'Unknown';
  let competitionColor = 'text-gray-500';
  
  if (competition !== 'N/A') {
    if (competition < 30) {
      competitionLevel = 'Low';
      competitionColor = 'text-green-600';
    } else if (competition < 70) {
      competitionLevel = 'Medium';
      competitionColor = 'text-yellow-600';
    } else {
      competitionLevel = 'High';
      competitionColor = 'text-red-600';
    }
  }
  
  return (
    <div 
      className={`bg-white rounded-lg shadow-md p-4 cursor-pointer transition-all ${isSelected ? 'ring-2 ring-primary-500' : 'hover:shadow-lg'}`}
      onClick={onClick}
    >
      <h3 className="text-lg font-semibold text-gray-800">{niche.name}</h3>
      
      <div className="mt-3 grid grid-cols-3 gap-2">
        <div>
          <p className="text-xs text-gray-500">Avg. Views</p>
          <p className="font-medium">{niche.avg_views_formatted}</p>
        </div>
        
        <div>
          <p className="text-xs text-gray-500">Competition</p>
          <p className={`font-medium ${competitionColor}`}>
            {competition !== 'N/A' ? `${Math.round(competition)}% (${competitionLevel})` : 'N/A'}
          </p>
        </div>
        
        <div>
          <p className="text-xs text-gray-500">Opportunity</p>
          <p className="font-medium">
            {score !== 'N/A' ? `${Math.round(score)}/100` : 'N/A'}
          </p>
        </div>
      </div>
      
      {/* Data quality indicator */}
      <div className="mt-2 flex items-center">
        <span className={`inline-block w-2 h-2 rounded-full mr-1 ${niche.data_quality === 'high' ? 'bg-green-500' : niche.data_quality === 'medium' ? 'bg-yellow-500' : 'bg-red-500'}`}></span>
        <span className="text-xs text-gray-500">{niche.video_count} videos analyzed</span>
      </div>
    </div>
  );
};

// Custom AI-friendly niche card
const AiFriendlyNicheCard = ({ niche, onClick, isSelected }) => {
  return (
    <div 
      className={`bg-white rounded-lg shadow-md p-4 cursor-pointer transition-all ${isSelected ? 'ring-2 ring-secondary-500' : 'hover:shadow-lg'}`}
      onClick={onClick}
    >
      <h3 className="text-lg font-semibold text-gray-800">{niche.name}</h3>
      <p className="mt-2 text-sm text-gray-600">{niche.description}</p>
      
      <div className="mt-3">
        <h4 className="text-xs text-gray-500 uppercase">AI Advantage</h4>
        <p className="text-sm text-secondary-700">{niche.ai_advantage}</p>
      </div>
      
      <div className="mt-3">
        <h4 className="text-xs text-gray-500 uppercase">Example Topics</h4>
        <div className="flex flex-wrap gap-1 mt-1">
          {niche.example_topics.map((topic, index) => (
            <span key={index} className="inline-block px-2 py-1 bg-secondary-50 text-secondary-700 text-xs rounded-full">
              {topic}
            </span>
          ))}
        </div>
      </div>
    </div>
  );
};

const VideoExample = ({ video }) => {
  if (!video) return null;
  
  return (
    <div className="flex items-start space-x-4 p-4 border-b border-gray-200">
      {video.thumbnail ? (
        <img src={video.thumbnail} alt={video.title} className="w-32 h-18 object-cover rounded" />
      ) : (
        <div className="w-32 h-18 bg-gray-200 rounded flex items-center justify-center">
          <span className="text-gray-400">No Thumbnail</span>
        </div>
      )}
      
      <div className="flex-1">
        <h4 className="font-medium text-gray-800 line-clamp-2">{video.title}</h4>
        <p className="text-sm text-gray-500 mt-1">{video.channel_title}</p>
        <div className="flex items-center mt-2 text-sm text-gray-600 space-x-3">
          <span>{video.views ? `${video.views.toLocaleString()} views` : 'Views N/A'}</span>
          <span>{video.likes ? `${video.likes.toLocaleString()} likes` : 'Likes N/A'}</span>
          {video.engagement_rate && <span>{video.engagement_rate.toFixed(1)}% engagement</span>}
        </div>
      </div>
    </div>
  );
};

const NicheResearch = () => {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('trending');
  const [selectedNiche, setSelectedNiche] = useState(null);
  const [customNicheQuery, setCustomNicheQuery] = useState('');
  const [searchPerformed, setSearchPerformed] = useState(false);
  const [regionCode, setRegionCode] = useState('US');
  
  // Get API key from localStorage
  const apiKey = localStorage.getItem('youtubeApiKey');
  
  // Redirect to setup if no API key is found
  useEffect(() => {
    if (!apiKey) {
      navigate('/setup');
    }
  }, [apiKey, navigate]);
  
  // Fetch trending niches
  const trendingNichesQuery = useQuery(
    ['trendingNiches', apiKey, regionCode],
    () => fetchTrendingNiches(apiKey, regionCode),
    {
      enabled: !!apiKey && activeTab === 'trending',
      staleTime: 5 * 60 * 1000, // 5 minutes
      refetchOnWindowFocus: false,
      onSuccess: (data) => {
        if (data.niches && data.niches.length > 0 && !selectedNiche) {
          setSelectedNiche(data.niches[0]);
        }
      },
    }
  );
  
  // Fetch low competition niches
  const lowCompetitionNichesQuery = useQuery(
    ['lowCompetitionNiches', apiKey, regionCode],
    () => fetchLowCompetitionNiches(apiKey, regionCode),
    {
      enabled: !!apiKey && activeTab === 'low-competition',
      staleTime: 5 * 60 * 1000, // 5 minutes
      refetchOnWindowFocus: false,
      onSuccess: (data) => {
        if (data.niches && data.niches.length > 0 && !selectedNiche) {
          setSelectedNiche(data.niches[0]);
        }
      },
    }
  );
  
  // Fetch AI friendly niches
  const aiFriendlyNichesQuery = useQuery(
    ['aiFriendlyNiches'],
    fetchAiFriendlyNiches,
    {
      enabled: activeTab === 'ai-friendly',
      staleTime: 60 * 60 * 1000, // 1 hour
      refetchOnWindowFocus: false,
      onSuccess: (data) => {
        if (data.niches && data.niches.length > 0 && !selectedNiche) {
          setSelectedNiche(data.niches[0]);
        }
      },
    }
  );
  
  // Search for a custom niche
  const customNicheQueryResult = useQuery(
    ['customNiche', apiKey, customNicheQuery, regionCode],
    () => searchNiche(apiKey, customNicheQuery, regionCode),
    {
      enabled: !!apiKey && !!customNicheQuery && searchPerformed,
      staleTime: 5 * 60 * 1000, // 5 minutes
      refetchOnWindowFocus: false,
      onSuccess: (data) => {
        if (data.niche) {
          setSelectedNiche(data.niche);
          // Store videos for display
          setCustomNicheVideos(data.videos || []);
        }
      },
      onSettled: () => {
        setSearchPerformed(false);
      },
    }
  );
  
  const [customNicheVideos, setCustomNicheVideos] = useState([]);
  
  // Handle tab change
  const handleTabChange = (tab) => {
    setActiveTab(tab);
    setSelectedNiche(null);
  };
  
  // Handle custom niche search
  const handleCustomNicheSearch = (e) => {
    e.preventDefault();
    if (customNicheQuery.trim() !== '') {
      setSearchPerformed(true);
    }
  };
  
  // Get current data based on active tab
  const getCurrentData = () => {
    switch (activeTab) {
      case 'trending':
        return trendingNichesQuery.data?.niches || [];
      case 'low-competition':
        return lowCompetitionNichesQuery.data?.niches || [];
      case 'ai-friendly':
        return aiFriendlyNichesQuery.data?.niches || [];
      case 'custom':
        return customNicheQueryResult.data?.niche ? [customNicheQueryResult.data.niche] : [];
      default:
        return [];
    }
  };
  
  // Check if data is loading
  const isLoading = (
    (activeTab === 'trending' && trendingNichesQuery.isLoading) ||
    (activeTab === 'low-competition' && lowCompetitionNichesQuery.isLoading) ||
    (activeTab === 'ai-friendly' && aiFriendlyNichesQuery.isLoading) ||
    (activeTab === 'custom' && customNicheQueryResult.isLoading)
  );
  
  // Check if there was an error
  const isError = (
    (activeTab === 'trending' && trendingNichesQuery.isError) ||
    (activeTab === 'low-competition' && lowCompetitionNichesQuery.isError) ||
    (activeTab === 'ai-friendly' && aiFriendlyNichesQuery.isError) ||
    (activeTab === 'custom' && customNicheQueryResult.isError)
  );
  
  // Get error message
  const errorMessage = (
    (activeTab === 'trending' && trendingNichesQuery.error?.message) ||
    (activeTab === 'low-competition' && lowCompetitionNichesQuery.error?.message) ||
    (activeTab === 'ai-friendly' && aiFriendlyNichesQuery.error?.message) ||
    (activeTab === 'custom' && customNicheQueryResult.error?.message) ||
    'An error occurred while fetching data.'
  );
  
  // Get videos examples for the selected niche
  const getVideoExamples = () => {
    if (!selectedNiche) return [];
    
    if (activeTab === 'custom') {
      return customNicheVideos;
    }
    
    if (activeTab === 'ai-friendly') {
      return []; // AI friendly niches don't have video examples
    }
    
    if (activeTab === 'trending') {
      return selectedNiche.examples || [];
    }
    
    if (activeTab === 'low-competition') {
      return selectedNiche.examples || [];
    }
    
    return [];
  };
  
  // Prepare data for the visualization chart
  const prepareChartData = () => {
    const niches = getCurrentData();
    if (activeTab === 'ai-friendly') return []; // No chart for AI-friendly niches
    
    return niches
      .filter(niche => 
        niche.traffic_potential !== null && 
        niche.competition !== null && 
        niche.score !== null
      )
      .map(niche => ({
        name: niche.name,
        traffic_potential: niche.traffic_potential,
        competition: niche.competition,
        score: niche.score,
        video_count: niche.video_count,
        avg_views_formatted: niche.avg_views_formatted,
        z: niche.video_count, // Size of bubble based on video count
      }));
  };
  
  const chartData = prepareChartData();
  
  return (
    <div className="mb-10">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-3xl font-bold text-gray-800">Niche Research</h1>
        <button 
          onClick={() => navigate('/setup')} 
          className="flex items-center text-gray-600 hover:text-gray-800"
        >
          <FaArrowLeft className="mr-2" /> Back to Setup
        </button>
      </div>
      
      {/* Tab Navigation */}
      <div className="flex border-b border-gray-200 mb-6">
        <button
          onClick={() => handleTabChange('trending')}
          className={`py-3 px-4 font-medium ${activeTab === 'trending' ? 'text-primary-600 border-b-2 border-primary-500' : 'text-gray-500 hover:text-gray-700'}`}
        >
          Trending Niches
        </button>
        <button
          onClick={() => handleTabChange('low-competition')}
          className={`py-3 px-4 font-medium ${activeTab === 'low-competition' ? 'text-primary-600 border-b-2 border-primary-500' : 'text-gray-500 hover:text-gray-700'}`}
        >
          Low Competition Niches
        </button>
        <button
          onClick={() => handleTabChange('ai-friendly')}
          className={`py-3 px-4 font-medium ${activeTab === 'ai-friendly' ? 'text-primary-600 border-b-2 border-primary-500' : 'text-gray-500 hover:text-gray-700'}`}
        >
          AI-Friendly Niches
        </button>
        <button
          onClick={() => handleTabChange('custom')}
          className={`py-3 px-4 font-medium ${activeTab === 'custom' ? 'text-primary-600 border-b-2 border-primary-500' : 'text-gray-500 hover:text-gray-700'}`}
        >
          Custom Niche
        </button>
      </div>
      
      {/* Custom Niche Search Form (visible only when custom tab is active) */}
      {activeTab === 'custom' && (
        <div className="bg-white p-4 rounded-lg shadow-md mb-6">
          <form onSubmit={handleCustomNicheSearch} className="flex items-center">
            <input
              type="text"
              value={customNicheQuery}
              onChange={(e) => setCustomNicheQuery(e.target.value)}
              placeholder="Enter a niche to research (e.g., 'cooking tips', 'fitness routines')"
              className="flex-1 px-4 py-2 border border-gray-300 rounded-l-md focus:outline-none focus:ring-2 focus:ring-primary-500"
              required
            />
            <button
              type="submit"
              className="bg-primary-600 text-white px-4 py-2 rounded-r-md hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500"
              disabled={isLoading || !customNicheQuery.trim()}
            >
              {isLoading ? 'Searching...' : 'Search'}
            </button>
          </form>
        </div>
      )}
      
      {/* Error Message */}
      {isError && (
        <div className="bg-red-50 border-l-4 border-red-500 p-4 mb-6">
          <div className="flex items-start">
            <FaExclamationTriangle className="text-red-500 mt-1 mr-3" />
            <div>
              <h3 className="text-red-800 font-medium">Error</h3>
              <p className="text-red-700 text-sm">{errorMessage}</p>
            </div>
          </div>
        </div>
      )}
      
      {/* Loading Indicator */}
      {isLoading && (
        <div className="flex justify-center items-center p-12">
          <div className="spinner mr-4"></div>
          <p className="text-gray-600">Analyzing YouTube data...</p>
        </div>
      )}
      
      {/* Main Content */}
      {!isLoading && !isError && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Niche List (first column) */}
          <div className="lg:col-span-1 space-y-4">
            <h2 className="text-xl font-semibold text-gray-800 mb-4">
              {activeTab === 'trending' && 'Trending Niches'}
              {activeTab === 'low-competition' && 'Low Competition Niches'}
              {activeTab === 'ai-friendly' && 'AI-Friendly Niches'}
              {activeTab === 'custom' && 'Niche Analysis'}
            </h2>
            
            {getCurrentData().length > 0 ? (
              <div className="space-y-4 max-h-[600px] overflow-y-auto pr-2">
                {getCurrentData().map((niche, index) => (
                  activeTab === 'ai-friendly' ? (
                    <AiFriendlyNicheCard
                      key={`${niche.name}-${index}`}
                      niche={niche}
                      onClick={() => setSelectedNiche(niche)}
                      isSelected={selectedNiche && selectedNiche.name === niche.name}
                    />
                  ) : (
                    <NicheCard
                      key={`${niche.name}-${index}`}
                      niche={niche}
                      onClick={() => setSelectedNiche(niche)}
                      isSelected={selectedNiche && selectedNiche.name === niche.name}
                    />
                  )
                ))}
              </div>
            ) : (
              <div className="bg-gray-50 p-6 rounded-lg text-center">
                <p className="text-gray-500">
                  {activeTab === 'custom' 
                    ? 'Enter a search term to analyze a custom niche' 
                    : 'No niches found. Try a different category or region.'}
                </p>
              </div>
            )}
          </div>
          
          {/* Visualization & Details (second and third columns) */}
          <div className="lg:col-span-2">
            {selectedNiche ? (
              <div className="space-y-6">
                {/* Traffic vs Competition Chart */}
                {activeTab !== 'ai-friendly' && chartData.length > 0 && (
                  <div className="bg-white p-4 rounded-lg shadow-md">
                    <h3 className="text-lg font-semibold text-gray-800 mb-2">Traffic vs. Competition Analysis</h3>
                    <p className="text-sm text-gray-600 mb-4">
                      <FaInfoCircle className="inline mr-1" />
                      Niches in the top-left quadrant (high traffic, low competition) present the best opportunities.
                    </p>
                    <div className="h-80">
                      <ResponsiveContainer width="100%" height="100%">
                        <ScatterChart
                          margin={{ top: 20, right: 20, bottom: 20, left: 20 }}
                        >
                          <CartesianGrid strokeDasharray="3 3" opacity={0.2} />
                          <XAxis 
                            type="number" 
                            dataKey="competition" 
                            name="Competition" 
                            domain={[0, 100]}
                            label={{
                              value: 'Competition Level', 
                              position: 'insideBottom', 
                              offset: -10
                            }}
                          />
                          <YAxis 
                            type="number" 
                            dataKey="traffic_potential" 
                            name="Traffic" 
                            domain={[0, 100]}
                            label={{
                              value: 'Traffic Potential', 
                              angle: -90, 
                              position: 'insideLeft'
                            }}
                          />
                          <ZAxis 
                            type="number" 
                            dataKey="z" 
                            range={[50, 400]} 
                            name="Video Count" 
                          />
                          <Tooltip content={<CustomTooltip />} cursor={{ strokeDasharray: '3 3' }} />
                          <Scatter 
                            name="Niches" 
                            data={chartData} 
                            fill="#8884d8" 
                            fillOpacity={0.6}
                            stroke="#8884d8"
                            strokeWidth={1}
                          />
                          
                          {/* Highlight the selected niche */}
                          {selectedNiche && selectedNiche.traffic_potential !== null && selectedNiche.competition !== null && (
                            <Scatter 
                              name="Selected" 
                              data={[{
                                name: selectedNiche.name,
                                traffic_potential: selectedNiche.traffic_potential,
                                competition: selectedNiche.competition,
                                score: selectedNiche.score,
                                z: selectedNiche.video_count,
                                avg_views_formatted: selectedNiche.avg_views_formatted
                              }]} 
                              fill="#ff7300" 
                              shape="star"
                              strokeWidth={2}
                            />
                          )}
                        </ScatterChart>
                      </ResponsiveContainer>
                    </div>
                  </div>
                )}
                
                {/* Video Examples */}
                <div className="bg-white rounded-lg shadow-md overflow-hidden">
                  <div className="px-4 py-3 bg-gray-50 border-b border-gray-200">
                    <h3 className="font-medium text-gray-800">
                      {activeTab === 'ai-friendly' 
                        ? 'Example Topics for AI-Generated Content' 
                        : 'Example Videos in This Niche'}
                    </h3>
                  </div>
                  
                  {activeTab === 'ai-friendly' ? (
                    <div className="p-4">
                      <h4 className="font-medium text-gray-700 mb-2">{selectedNiche.name}</h4>
                      <p className="text-gray-600 mb-4">{selectedNiche.description}</p>
                      
                      <h5 className="text-sm font-medium text-gray-700 mb-2">Example Topics:</h5>
                      <div className="flex flex-wrap gap-2">
                        {selectedNiche.example_topics.map((topic, index) => (
                          <div key={index} className="bg-gray-100 rounded-full px-3 py-1 text-sm text-gray-700">
                            {topic}
                          </div>
                        ))}
                      </div>
                      
                      <h5 className="text-sm font-medium text-gray-700 mt-4 mb-2">AI Advantage:</h5>
                      <p className="text-gray-600">{selectedNiche.ai_advantage}</p>
                    </div>
                  ) : (
                    <div>
                      {getVideoExamples().length > 0 ? (
                        <div className="divide-y divide-gray-200 max-h-96 overflow-y-auto">
                          {getVideoExamples().map((video, index) => (
                            <VideoExample key={index} video={video} />
                          ))}
                        </div>
                      ) : (
                        <div className="p-6 text-center text-gray-500">
                          No video examples available for this niche.
                        </div>
                      )}
                    </div>
                  )}
                </div>
              </div>
            ) : (
              <div className="bg-gray-50 p-10 rounded-lg text-center">
                <p className="text-gray-500">Select a niche to view detailed analysis and examples.</p>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default NicheResearch;
