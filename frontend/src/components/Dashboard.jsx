import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { getStats, getDelayByRoute, getDelayByWeather, getDelayDistribution } from '../services/api';
import Plot from 'react-plotly.js';
import AnimatedCard from './AnimatedCard';
import { LoadingSpinner } from './LoadingSpinner';
import { staggerContainer, staggerItem } from '../utils/animations';

function Dashboard() {
  const [stats, setStats] = useState(null);
  const [delayByRoute, setDelayByRoute] = useState(null);
  const [delayByWeather, setDelayByWeather] = useState(null);
  const [delayDistribution, setDelayDistribution] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const [statsRes, routeRes, weatherRes, distRes] = await Promise.all([
        getStats(),
        getDelayByRoute(),
        getDelayByWeather(),
        getDelayDistribution(),
      ]);

      setStats(statsRes.data);
      setDelayByRoute(routeRes.data);
      setDelayByWeather(weatherRes.data);
      setDelayDistribution(distRes.data);
      setError(null);
    } catch (err) {
      setError(err.message || 'Failed to load dashboard data');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="loading">
        <LoadingSpinner />
        <p style={{ marginTop: '1rem' }}>Loading dashboard...</p>
      </div>
    );
  }

  if (error) {
    return <div className="error">Error: {error}</div>;
  }

  const metrics = [
    { label: 'Total Records', value: stats?.total_records?.toLocaleString() || 0, suffix: '' },
    { label: 'Mean Delay', value: stats?.mean_delay?.toFixed(1) || 0, suffix: ' min' },
    { label: 'Median Delay', value: stats?.median_delay?.toFixed(1) || 0, suffix: ' min' },
    { label: 'Max Delay', value: stats?.max_delay?.toFixed(1) || 0, suffix: ' min' },
  ];

  return (
    <div>
      <motion.div
        className="page-header"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <h1>Dashboard Overview</h1>
        <p>AI-Powered Bus Delay Analysis & Prediction System</p>
      </motion.div>

      <motion.div
        className="metrics-grid"
        variants={staggerContainer}
        initial="initial"
        animate="animate"
      >
        {metrics.map((metric, index) => (
          <motion.div
            key={metric.label}
            className="metric-card"
            variants={staggerItem}
            whileHover={{ scale: 1.02, y: -4 }}
            transition={{ type: 'spring', stiffness: 300, damping: 20 }}
          >
            <div className="metric-label">{metric.label}</div>
            <div className="metric-value">
              {metric.value}
              {metric.suffix}
            </div>
          </motion.div>
        ))}
      </motion.div>

      {/* Charts with Fade-in Animation */}
      <motion.div
        className="charts-grid"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.4, duration: 0.5 }}
      >
        <AnimatedCard delay={0.5}>
          <h2>Delay Distribution</h2>
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.6, duration: 0.5 }}
          >
            <Plot
              data={[
                {
                  x: delayDistribution?.delays || [],
                  type: 'histogram',
                  nbinsx: 50,
                  marker: { color: '#4682B4' },
                },
              ]}
              layout={{
                title: 'Distribution of Bus Delays',
                xaxis: { title: 'Delay (minutes)' },
                yaxis: { title: 'Frequency' },
                height: 400,
                plot_bgcolor: 'rgba(0,0,0,0)',
                paper_bgcolor: 'rgba(0,0,0,0)',
              }}
              config={{ displayModeBar: false }}
            />
          </motion.div>
        </AnimatedCard>

        <AnimatedCard delay={0.6}>
          <h2>Delay by Route</h2>
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.7, duration: 0.5 }}
          >
            <Plot
              data={[
                {
                  x: delayByRoute?.routes || [],
                  y: delayByRoute?.delays || [],
                  type: 'bar',
                  marker: { color: '#4682B4' },
                },
              ]}
              layout={{
                title: 'Average Delay by Route',
                xaxis: { title: 'Route ID' },
                yaxis: { title: 'Average Delay (minutes)' },
                height: 400,
                plot_bgcolor: 'rgba(0,0,0,0)',
                paper_bgcolor: 'rgba(0,0,0,0)',
              }}
              config={{ displayModeBar: false }}
            />
          </motion.div>
        </AnimatedCard>

        <AnimatedCard delay={0.7}>
          <h2>Delay by Weather</h2>
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.8, duration: 0.5 }}
          >
            <Plot
              data={[
                {
                  x: delayByWeather?.weather || [],
                  y: delayByWeather?.delays || [],
                  type: 'bar',
                  marker: { color: '#FF7F50' },
                },
              ]}
              layout={{
                title: 'Average Delay by Weather Condition',
                xaxis: { title: 'Weather' },
                yaxis: { title: 'Average Delay (minutes)' },
                height: 400,
                plot_bgcolor: 'rgba(0,0,0,0)',
                paper_bgcolor: 'rgba(0,0,0,0)',
              }}
              config={{ displayModeBar: false }}
            />
          </motion.div>
        </AnimatedCard>
      </motion.div>
    </div>
  );
}

export default Dashboard;
