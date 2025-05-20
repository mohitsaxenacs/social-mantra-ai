import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api/youtube';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const fetchTrendingNiches = async (apiKey, regionCode = 'US') => {
  try {
    const response = await api.get('/trending-niches', {
      params: { api_key: apiKey, region_code: regionCode }
    });
    return response.data;
  } catch (error) {
    const message = error.response?.data?.detail || error.message || 'Failed to fetch trending niches';
    throw new Error(message);
  }
};

export const fetchLowCompetitionNiches = async (apiKey, regionCode = 'US') => {
  try {
    const response = await api.get('/low-competition-niches', {
      params: { api_key: apiKey, region_code: regionCode }
    });
    return response.data;
  } catch (error) {
    const message = error.response?.data?.detail || error.message || 'Failed to fetch low competition niches';
    throw new Error(message);
  }
};

export const fetchAiFriendlyNiches = async () => {
  try {
    const response = await api.get('/ai-friendly-niches');
    return response.data;
  } catch (error) {
    const message = error.response?.data?.detail || error.message || 'Failed to fetch AI-friendly niches';
    throw new Error(message);
  }
};

export const searchNiche = async (apiKey, query, regionCode = 'US') => {
  try {
    const response = await api.get('/search-niche', {
      params: { api_key: apiKey, query, region_code: regionCode }
    });
    return response.data;
  } catch (error) {
    const message = error.response?.data?.detail || error.message || 'Failed to search niche';
    throw new Error(message);
  }
};

export const fetchChannelInfo = async (apiKey, channelId) => {
  try {
    const response = await api.get(`/channel/${channelId}`, {
      params: { api_key: apiKey }
    });
    return response.data;
  } catch (error) {
    const message = error.response?.data?.detail || error.message || 'Failed to fetch channel info';
    throw new Error(message);
  }
};
