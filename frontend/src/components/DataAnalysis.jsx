import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { getDataPreview, filterData, getCorrelation, getStatistics, getRoutesList, getWeatherList } from '../services/api';
import Plot from 'react-plotly.js';
import AnimatedCard from './AnimatedCard';
import { LoadingSpinner } from './LoadingSpinner';
import { staggerItem, buttonHover, buttonTap } from '../utils/animations';

function DataAnalysis() {
  const [data, setData] = useState([]);
  const [correlation, setCorrelation] = useState(null);
  const [statistics, setStatistics] = useState(null);
  const [routesList, setRoutesList] = useState([]);
  const [weatherList, setWeatherList] = useState([]);
  const [page, setPage] = useState(1);
  const [pageSize] = useState(20);
  const [totalPages, setTotalPages] = useState(1);
  const [filters, setFilters] = useState({
    route_id: [],
    weather: [],
    max_delay: '',
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filterMode, setFilterMode] = useState(false);
  const [activeTab, setActiveTab] = useState('statistics');

  useEffect(() => {
    loadInitialData();
  }, []);

  useEffect(() => {
    if (filterMode) {
      loadFilteredData();
    } else if (activeTab === 'rawdata') {
      loadData();
    }
  }, [page, filterMode, activeTab]);

  const loadInitialData = async () => {
    try {
      setLoading(true);
      await Promise.all([
        loadCorrelation(),
        loadStatistics(),
        loadRoutesList(),
        loadWeatherList(),
        loadData(),
      ]);
      setError(null);
    } catch (err) {
      setError(err.message || 'Failed to load data');
    } finally {
      setLoading(false);
    }
  };

  const loadData = async () => {
    try {
      setLoading(true);
      const res = await getDataPreview(page, pageSize);
      setData(res.data.records || []);
      setTotalPages(res.data.total_pages || 1);
      setError(null);
    } catch (err) {
      setError(err.message || 'Failed to load data');
    } finally {
      setLoading(false);
    }
  };

  const loadFilteredData = async () => {
    try {
      setLoading(true);
      const filterParams = {};
      if (filters.route_id && filters.route_id.length > 0) {
        filterParams.route_id = filters.route_id[0];
      }
      if (filters.weather && filters.weather.length > 0) {
        filterParams.weather = filters.weather[0];
      }
      if (filters.max_delay) {
        filterParams.max_delay = parseFloat(filters.max_delay);
      }

      const res = await filterData(filterParams);
      setData(res.data.records || []);
      setTotalPages(1);
      setError(null);
    } catch (err) {
      setError(err.message || 'Failed to load filtered data');
    } finally {
      setLoading(false);
    }
  };

  const loadCorrelation = async () => {
    try {
      const res = await getCorrelation();
      setCorrelation(res.data);
    } catch (err) {
      console.error('Failed to load correlation:', err);
    }
  };

  const loadStatistics = async () => {
    try {
      const res = await getStatistics();
      setStatistics(res.data);
    } catch (err) {
      console.error('Failed to load statistics:', err);
    }
  };

  const loadRoutesList = async () => {
    try {
      const res = await getRoutesList();
      setRoutesList(res.data.routes || []);
    } catch (err) {
      console.error('Failed to load routes list:', err);
    }
  };

  const loadWeatherList = async () => {
    try {
      const res = await getWeatherList();
      setWeatherList(res.data.weather || []);
    } catch (err) {
      console.error('Failed to load weather list:', err);
    }
  };

  const handleFilterChange = (e) => {
    const { name, value } = e.target;
    if (name === 'route_id' || name === 'weather') {
      const selectedOptions = Array.from(e.target.selectedOptions, option => option.value);
      setFilters((prev) => ({ ...prev, [name]: selectedOptions }));
    } else {
      setFilters((prev) => ({ ...prev, [name]: value }));
    }
  };

  const handleFilterSubmit = (e) => {
    e.preventDefault();
    setFilterMode(true);
    setPage(1);
    loadFilteredData();
  };

  const handleClearFilters = () => {
    setFilters({ route_id: [], weather: [], max_delay: '' });
    setFilterMode(false);
    setPage(1);
    loadData();
  };

  const formatStatValue = (value) => {
    if (value === null || value === undefined) return 'N/A';
    return typeof value === 'number' ? value.toFixed(2) : value;
  };

  const tabs = [
    { id: 'statistics', label: 'Statistics' },
    { id: 'exploratory', label: 'Exploratory Analysis' },
    { id: 'rawdata', label: 'Raw Data' },
  ];

  if (loading && data.length === 0 && !statistics) {
    return (
      <div className="loading">
        <LoadingSpinner />
        <p style={{ marginTop: '1rem' }}>Loading data analysis...</p>
      </div>
    );
  }

  return (
    <div>
      <motion.div
        className="page-header"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <h1>Data Analysis</h1>
        <p>Explore and analyze the transport delay dataset</p>
      </motion.div>

      <AnimatePresence>
        {error && (
          <motion.div
            className="error"
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            transition={{ duration: 0.3 }}
          >
            Error: {error}
          </motion.div>
        )}
      </AnimatePresence>

      {/* Animated Tabs */}
      <motion.div
        style={{ marginBottom: '2rem', borderBottom: '2px solid var(--color-border)' }}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.2 }}
      >
        <div style={{ display: 'flex', gap: '0.5rem' }}>
          {tabs.map((tab) => (
            <motion.button
              key={tab.id}
              className={`btn ${activeTab === tab.id ? 'btn-primary' : ''}`}
              onClick={() => setActiveTab(tab.id)}
              style={{
                marginBottom: '-2px',
                borderRadius: '0.5rem 0.5rem 0 0',
                position: 'relative',
              }}
              whileHover={buttonHover}
              whileTap={buttonTap}
            >
              {tab.label}
              {activeTab === tab.id && (
                <motion.div
                  layoutId="activeTab"
                  className="tab-indicator"
                  style={{
                    position: 'absolute',
                    bottom: '-2px',
                    left: 0,
                    right: 0,
                    height: '2px',
                    background: 'var(--color-accent)',
                  }}
                  transition={{
                    type: 'spring',
                    stiffness: 380,
                    damping: 30,
                  }}
                />
              )}
            </motion.button>
          ))}
        </div>
      </motion.div>

      {/* Tab Content with AnimatePresence */}
      <AnimatePresence mode="wait">
        {activeTab === 'statistics' && statistics && (
          <motion.div
            key="statistics"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            transition={{ duration: 0.3 }}
          >
            <AnimatedCard delay={0.1}>
              <h2>Dataset Statistics</h2>
              <div className="form-row" style={{ gridTemplateColumns: '1fr 1fr' }}>
                <motion.div
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.2 }}
                >
                  <h3 style={{ marginBottom: '1rem', color: '#495057' }}>Delay Statistics</h3>
                  <div className="table-container">
                    <motion.table
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      transition={{ delay: 0.3 }}
                    >
                      <thead>
                        <tr>
                          <th>Metric</th>
                          <th>Value</th>
                        </tr>
                      </thead>
                      <tbody>
                        {Object.entries(statistics.delay_stats || {}).map(([key, value], index) => (
                          <motion.tr
                            key={key}
                            initial={{ opacity: 0, x: -10 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ delay: 0.4 + index * 0.05 }}
                            whileHover={{ backgroundColor: 'rgba(0, 0, 0, 0.02)' }}
                          >
                            <td>{key.charAt(0).toUpperCase() + key.slice(1)}</td>
                            <td>{formatStatValue(value)}</td>
                          </motion.tr>
                        ))}
                      </tbody>
                    </motion.table>
                  </div>
                </motion.div>
                <motion.div
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.2 }}
                >
                  <h3 style={{ marginBottom: '1rem', color: '#495057' }}>Passenger Count Statistics</h3>
                  <div className="table-container">
                    <motion.table
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      transition={{ delay: 0.3 }}
                    >
                      <thead>
                        <tr>
                          <th>Metric</th>
                          <th>Value</th>
                        </tr>
                      </thead>
                      <tbody>
                        {Object.entries(statistics.passenger_stats || {}).map(([key, value], index) => (
                          <motion.tr
                            key={key}
                            initial={{ opacity: 0, x: 10 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ delay: 0.4 + index * 0.05 }}
                            whileHover={{ backgroundColor: 'rgba(0, 0, 0, 0.02)' }}
                          >
                            <td>{key.charAt(0).toUpperCase() + key.slice(1)}</td>
                            <td>{formatStatValue(value)}</td>
                          </motion.tr>
                        ))}
                      </tbody>
                    </motion.table>
                  </div>
                </motion.div>
              </div>
            </AnimatedCard>

            <AnimatedCard delay={0.3}>
              <h2>Delay by Route</h2>
              <div className="table-container">
                <motion.table
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: 0.4 }}
                >
                  <thead>
                    <tr>
                      <th>Route ID</th>
                      <th>Mean Delay</th>
                      <th>Median Delay</th>
                      <th>Std Deviation</th>
                      <th>Count</th>
                    </tr>
                  </thead>
                  <tbody>
                    {Object.entries(statistics.delay_by_route || {})
                      .sort((a, b) => (b[1].mean || 0) - (a[1].mean || 0))
                      .map(([route, stats], index) => (
                        <motion.tr
                          key={route}
                          initial={{ opacity: 0, y: 10 }}
                          animate={{ opacity: 1, y: 0 }}
                          transition={{ delay: 0.5 + index * 0.05 }}
                          whileHover={{ backgroundColor: 'rgba(0, 0, 0, 0.02)' }}
                        >
                          <td>{route}</td>
                          <td>{formatStatValue(stats.mean)}</td>
                          <td>{formatStatValue(stats.median)}</td>
                          <td>{formatStatValue(stats.std)}</td>
                          <td>{formatStatValue(stats.count)}</td>
                        </motion.tr>
                      ))}
                  </tbody>
                </motion.table>
              </div>
            </AnimatedCard>

            <AnimatedCard delay={0.4}>
              <h2>Delay by Weather</h2>
              <div className="table-container">
                <motion.table
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: 0.5 }}
                >
                  <thead>
                    <tr>
                      <th>Weather</th>
                      <th>Mean Delay</th>
                      <th>Median Delay</th>
                      <th>Std Deviation</th>
                      <th>Count</th>
                    </tr>
                  </thead>
                  <tbody>
                    {Object.entries(statistics.delay_by_weather || {})
                      .sort((a, b) => (b[1].mean || 0) - (a[1].mean || 0))
                      .map(([weather, stats], index) => (
                        <motion.tr
                          key={weather}
                          initial={{ opacity: 0, y: 10 }}
                          animate={{ opacity: 1, y: 0 }}
                          transition={{ delay: 0.6 + index * 0.05 }}
                          whileHover={{ backgroundColor: 'rgba(0, 0, 0, 0.02)' }}
                        >
                          <td>{weather}</td>
                          <td>{formatStatValue(stats.mean)}</td>
                          <td>{formatStatValue(stats.median)}</td>
                          <td>{formatStatValue(stats.std)}</td>
                          <td>{formatStatValue(stats.count)}</td>
                        </motion.tr>
                      ))}
                  </tbody>
                </motion.table>
              </div>
            </AnimatedCard>
          </motion.div>
        )}

        {activeTab === 'exploratory' && (
          <motion.div
            key="exploratory"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            transition={{ duration: 0.3 }}
          >
            {correlation && (
              <AnimatedCard delay={0.1}>
                <h2>Correlation Analysis</h2>
                <motion.div
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: 0.2, duration: 0.5 }}
                >
                  <Plot
                    data={[
                      {
                        z: correlation.matrix || [],
                        x: correlation.columns || [],
                        y: correlation.rows || [],
                        type: 'heatmap',
                        colorscale: 'RdBu',
                        zmid: 0,
                        text: correlation.matrix?.map(row => row.map(val => val.toFixed(3))),
                        texttemplate: '%{text}',
                        textfont: { size: 12 },
                        hovertemplate: 'X: %{x}<br>Y: %{y}<br>Correlation: %{z:.3f}<extra></extra>',
                      },
                    ]}
                    layout={{
                      title: 'Correlation Matrix of Numeric Features',
                      height: 500,
                      plot_bgcolor: 'rgba(0,0,0,0)',
                      paper_bgcolor: 'rgba(0,0,0,0)',
                    }}
                    config={{ displayModeBar: false }}
                  />
                </motion.div>
              </AnimatedCard>
            )}

            {correlation && (
              <AnimatedCard delay={0.2}>
                <h2>Correlation with Delay</h2>
                <motion.div
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: 0.3, duration: 0.5 }}
                >
                  <Plot
                    data={[
                      {
                        x: correlation.columns || [],
                        y: correlation.matrix?.[0] || [],
                        type: 'bar',
                        marker: { color: '#4682B4' },
                      },
                    ]}
                    layout={{
                      title: 'Correlation with Delay',
                      xaxis: { title: 'Feature' },
                      yaxis: { title: 'Correlation Coefficient' },
                      height: 400,
                      plot_bgcolor: 'rgba(0,0,0,0)',
                      paper_bgcolor: 'rgba(0,0,0,0)',
                    }}
                    config={{ displayModeBar: false }}
                  />
                </motion.div>
              </AnimatedCard>
            )}
          </motion.div>
        )}

        {activeTab === 'rawdata' && (
          <motion.div
            key="rawdata"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            transition={{ duration: 0.3 }}
          >
            <AnimatedCard delay={0.1}>
              <h2>Data Filters</h2>
              <form onSubmit={handleFilterSubmit}>
                <motion.div
                  className="form-row"
                  variants={{
                    hidden: { opacity: 0 },
                    show: {
                      opacity: 1,
                      transition: {
                        staggerChildren: 0.05,
                      },
                    },
                  }}
                  initial="hidden"
                  animate="show"
                >
                  <motion.div className="form-group" variants={staggerItem}>
                    <label>Filter by Route</label>
                    <motion.select
                      name="route_id"
                      multiple
                      value={filters.route_id}
                      onChange={handleFilterChange}
                      style={{ minHeight: '100px' }}
                      whileFocus={{ scale: 1.02 }}
                    >
                      {routesList.map((route) => (
                        <option key={route} value={route}>
                          {route}
                        </option>
                      ))}
                    </motion.select>
                    <small style={{ color: '#6c757d', fontSize: '0.875rem' }}>
                      Hold Ctrl/Cmd to select multiple
                    </small>
                  </motion.div>
                  <motion.div className="form-group" variants={staggerItem}>
                    <label>Filter by Weather</label>
                    <motion.select
                      name="weather"
                      multiple
                      value={filters.weather}
                      onChange={handleFilterChange}
                      style={{ minHeight: '100px' }}
                      whileFocus={{ scale: 1.02 }}
                    >
                      {weatherList.map((weather) => (
                        <option key={weather} value={weather}>
                          {weather}
                        </option>
                      ))}
                    </motion.select>
                    <small style={{ color: '#6c757d', fontSize: '0.875rem' }}>
                      Hold Ctrl/Cmd to select multiple
                    </small>
                  </motion.div>
                  <motion.div className="form-group" variants={staggerItem}>
                    <label>Max Delay (minutes)</label>
                    <motion.input
                      type="number"
                      name="max_delay"
                      value={filters.max_delay}
                      onChange={handleFilterChange}
                      placeholder="e.g., 100"
                      min="0"
                      whileFocus={{ scale: 1.02 }}
                    />
                  </motion.div>
                </motion.div>
                <div style={{ display: 'flex', gap: '1rem' }}>
                  <motion.button
                    type="submit"
                    className="btn btn-primary"
                    whileHover={buttonHover}
                    whileTap={buttonTap}
                  >
                    Apply Filters
                  </motion.button>
                  <motion.button
                    type="button"
                    className="btn"
                    onClick={handleClearFilters}
                    whileHover={buttonHover}
                    whileTap={buttonTap}
                  >
                    Clear Filters
                  </motion.button>
                </div>
              </form>
            </AnimatedCard>

            <AnimatedCard delay={0.2}>
              <h2>Dataset Preview</h2>
              {filterMode && (
                <motion.p
                  style={{ marginBottom: '1rem', color: '#6c757d' }}
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                >
                  Showing {data.length} filtered records
                </motion.p>
              )}
              {!filterMode && (
                <motion.p
                  style={{ marginBottom: '1rem', color: '#6c757d' }}
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                >
                  Page {page} of {totalPages}
                </motion.p>
              )}
              <div className="table-container">
                <motion.table
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: 0.3 }}
                >
                  <thead>
                    <tr>
                      <th>Route ID</th>
                      <th>Scheduled Time</th>
                      <th>Actual Time</th>
                      <th>Weather</th>
                      <th>Passenger Count</th>
                      <th>Latitude</th>
                      <th>Longitude</th>
                      <th>Delay (min)</th>
                    </tr>
                  </thead>
                  <tbody>
                    {data.length === 0 ? (
                      <tr>
                        <td colSpan="8" style={{ textAlign: 'center', padding: '2rem', color: '#6c757d' }}>
                          No data available
                        </td>
                      </tr>
                    ) : (
                      data.map((record, idx) => (
                        <motion.tr
                          key={idx}
                          initial={{ opacity: 0, y: 10 }}
                          animate={{ opacity: 1, y: 0 }}
                          transition={{ delay: 0.4 + idx * 0.02 }}
                          whileHover={{ backgroundColor: 'rgba(0, 0, 0, 0.02)' }}
                        >
                          <td>{record.route_id}</td>
                          <td>{record.scheduled_time ? new Date(record.scheduled_time).toLocaleString() : 'N/A'}</td>
                          <td>{record.actual_time ? new Date(record.actual_time).toLocaleString() : 'N/A'}</td>
                          <td>{record.weather}</td>
                          <td>{record.passenger_count}</td>
                          <td>{record.latitude?.toFixed(4)}</td>
                          <td>{record.longitude?.toFixed(4)}</td>
                          <td>{record.delay_minutes?.toFixed(2)}</td>
                        </motion.tr>
                      ))
                    )}
                  </tbody>
                </motion.table>
              </div>

              {!filterMode && (
                <motion.div
                  style={{ marginTop: '1rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: 0.5 }}
                >
                  <motion.button
                    className="btn"
                    onClick={() => setPage((p) => Math.max(1, p - 1))}
                    disabled={page === 1}
                    whileHover={page !== 1 ? buttonHover : {}}
                    whileTap={page !== 1 ? buttonTap : {}}
                  >
                    Previous
                  </motion.button>
                  <span>
                    Page {page} of {totalPages}
                  </span>
                  <motion.button
                    className="btn"
                    onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
                    disabled={page === totalPages}
                    whileHover={page !== totalPages ? buttonHover : {}}
                    whileTap={page !== totalPages ? buttonTap : {}}
                  >
                    Next
                  </motion.button>
                </motion.div>
              )}
            </AnimatedCard>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

export default DataAnalysis;
