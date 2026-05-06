import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Health check
export const healthCheck = () => api.get('/api/health');

// Dashboard stats
export const getStats = () => api.get('/api/stats');

// Routes
export const getRoutes = () => api.get('/api/routes');

// Delay statistics
export const getDelayByRoute = () => api.get('/api/delay-by-route');
export const getDelayByWeather = () => api.get('/api/delay-by-weather');
export const getDelayDistribution = () => api.get('/api/delay-distribution');

// Correlation
export const getCorrelation = () => api.get('/api/correlation');

// Predictions
export const predictDelay = (data) => api.post('/api/predict', data);
export const predictAllModels = (data) => api.post('/api/predict/all', data);

// Model performance
export const getModelPerformance = () => api.get('/api/models/performance');

// Data preview
export const getDataPreview = (page = 1, pageSize = 20) =>
  api.get('/api/data/preview', { params: { page, page_size: pageSize } });

// Filter data
export const filterData = (filters) =>
  api.get('/api/data/filter', { params: filters });

// Statistics
export const getStatistics = () => api.get('/api/data/statistics');

// Lists for filters
export const getRoutesList = () => api.get('/api/data/routes-list');
export const getWeatherList = () => api.get('/api/data/weather-list');

export default api;



