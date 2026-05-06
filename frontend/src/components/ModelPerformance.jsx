import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { getModelPerformance } from '../services/api';
import Plot from 'react-plotly.js';
import AnimatedCard from './AnimatedCard';
import { LoadingSpinner } from './LoadingSpinner';
import { staggerContainer, staggerItem } from '../utils/animations';

function ModelPerformance() {
  const [performance, setPerformance] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadPerformance();
  }, []);

  const loadPerformance = async () => {
    try {
      setLoading(true);
      const res = await getModelPerformance();
      setPerformance(res.data);
      setError(null);
    } catch (err) {
      setError(err.message || 'Failed to load model performance');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="loading">
        <LoadingSpinner />
        <p style={{ marginTop: '1rem' }}>Loading model performance...</p>
      </div>
    );
  }

  if (error) {
    return <div className="error">Error: {error}</div>;
  }

  if (!performance) {
    return <div className="error">No performance data available</div>;
  }

  const modelNames = Object.keys(performance.test_mae || {}).map((name) =>
    name.replace('_', ' ').toUpperCase()
  );
  const maeValues = Object.values(performance.test_mae || {});
  const r2Values = Object.values(performance.test_r2 || {});

  const bestModel = Object.entries(performance.test_mae || {}).reduce((a, b) =>
    performance.test_mae[a[0]] < performance.test_mae[b[0]] ? a : b
  )[0];

  const bestModelMetrics = [
    { label: 'Best Model', value: bestModel.replace('_', ' ').toUpperCase(), suffix: '' },
    { label: 'Test MAE', value: performance.test_mae[bestModel]?.toFixed(2), suffix: ' min' },
    { label: 'Test R²', value: performance.test_r2[bestModel]?.toFixed(4), suffix: '' },
  ];

  return (
    <div>
      <motion.div
        className="page-header"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <h1>🤖 Model Performance</h1>
        <p>Compare the performance of different machine learning models</p>
      </motion.div>

      <AnimatedCard delay={0.1}>
        <h2>🏆 Best Model</h2>
        <motion.div
          className="metrics-grid"
          variants={staggerContainer}
          initial="initial"
          animate="animate"
        >
          {bestModelMetrics.map((metric, index) => (
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
      </AnimatedCard>

      <motion.div
        className="charts-grid"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.3, duration: 0.5 }}
      >
        <AnimatedCard delay={0.4}>
          <h2>Mean Absolute Error Comparison</h2>
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.5, duration: 0.5 }}
          >
            <Plot
              data={[
                {
                  x: modelNames,
                  y: maeValues,
                  type: 'bar',
                  marker: { color: '#4682B4' },
                },
              ]}
              layout={{
                title: 'MAE Comparison (Lower is Better)',
                xaxis: { title: 'Model' },
                yaxis: { title: 'MAE (minutes)' },
                height: 400,
                plot_bgcolor: 'rgba(0,0,0,0)',
                paper_bgcolor: 'rgba(0,0,0,0)',
              }}
              config={{ displayModeBar: false }}
            />
          </motion.div>
        </AnimatedCard>

        <AnimatedCard delay={0.5}>
          <h2>R² Score Comparison</h2>
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.6, duration: 0.5 }}
          >
            <Plot
              data={[
                {
                  x: modelNames,
                  y: r2Values,
                  type: 'bar',
                  marker: { color: '#FF7F50' },
                },
              ]}
              layout={{
                title: 'R² Score Comparison (Higher is Better)',
                xaxis: { title: 'Model' },
                yaxis: { title: 'R² Score' },
                height: 400,
                plot_bgcolor: 'rgba(0,0,0,0)',
                paper_bgcolor: 'rgba(0,0,0,0)',
              }}
              config={{ displayModeBar: false }}
            />
          </motion.div>
        </AnimatedCard>
      </motion.div>

      <AnimatedCard delay={0.6}>
        <h2>Model Comparison Table</h2>
        <div className="table-container">
          <motion.table
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.7 }}
          >
            <thead>
              <tr>
                <th>Model</th>
                <th>Test MAE (minutes)</th>
                <th>Test R² Score</th>
              </tr>
            </thead>
            <tbody>
              {Object.entries(performance.test_mae || {}).map(([modelName, mae], index) => (
                <motion.tr
                  key={modelName}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.8 + index * 0.1 }}
                  whileHover={{ backgroundColor: 'rgba(0, 0, 0, 0.02)' }}
                >
                  <td>{modelName.replace('_', ' ').toUpperCase()}</td>
                  <td>{mae.toFixed(2)}</td>
                  <td>{performance.test_r2[modelName]?.toFixed(4)}</td>
                </motion.tr>
              ))}
            </tbody>
          </motion.table>
        </div>
      </AnimatedCard>
    </div>
  );
}

export default ModelPerformance;
