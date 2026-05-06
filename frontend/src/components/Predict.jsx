import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { getRoutes, predictDelay, predictAllModels } from '../services/api';
import AnimatedCard from './AnimatedCard';
import { LoadingSpinner } from './LoadingSpinner';
import { staggerItem, buttonHover, buttonTap } from '../utils/animations';

function Predict() {
  const [routes, setRoutes] = useState([]);
  const [formData, setFormData] = useState({
    route_id: '',
    scheduled_date: new Date().toISOString().split('T')[0],
    hour: 8,
    minute: 0,
    weather: 'sunny',
    passenger_count: 50,
    latitude: 24.5,
    longitude: 32.5,
    model_name: 'xgboost',
  });
  const [prediction, setPrediction] = useState(null);
  const [allPredictions, setAllPredictions] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadRoutes();
  }, []);

  const loadRoutes = async () => {
    try {
      const res = await getRoutes();
      setRoutes(res.data.routes || []);
      if (res.data.routes && res.data.routes.length > 0) {
        setFormData((prev) => ({ ...prev, route_id: res.data.routes[0] }));
      }
    } catch (err) {
      setError(err.message || 'Failed to load routes');
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: name === 'hour' || name === 'minute' || name === 'passenger_count' 
        ? parseInt(value) 
        : name === 'latitude' || name === 'longitude'
        ? parseFloat(value)
        : value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setPrediction(null);
    setAllPredictions(null);

    try {
      const scheduled_time = `${formData.scheduled_date} ${String(formData.hour).padStart(2, '0')}:${String(formData.minute).padStart(2, '0')}:00`;
      
      const requestData = {
        route_id: formData.route_id,
        scheduled_time: scheduled_time,
        weather: formData.weather,
        passenger_count: formData.passenger_count,
        latitude: formData.latitude,
        longitude: formData.longitude,
        model_name: formData.model_name,
      };

      const [predRes, allPredRes] = await Promise.all([
        predictDelay(requestData),
        predictAllModels(requestData),
      ]);

      setPrediction(predRes.data);
      setAllPredictions(allPredRes.data.predictions);
    } catch (err) {
      setError(err.message || 'Failed to make prediction');
    } finally {
      setLoading(false);
    }
  };

  const getStatusClass = (status) => {
    const statusMap = {
      'Early': 'status-early',
      'On Time': 'status-ontime',
      'Minor Delay': 'status-minor',
      'Significant Delay': 'status-significant',
    };
    return statusMap[status] || 'status-ontime';
  };

  return (
    <div>
      <motion.div
        className="page-header"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <h1>🔮 Predict Bus Delay</h1>
        <p>Enter the details below to predict the expected delay for a bus trip.</p>
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

      <AnimatedCard delay={0.1}>
        <form onSubmit={handleSubmit}>
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
              <label>Route ID</label>
              <motion.select
                name="route_id"
                value={formData.route_id}
                onChange={handleChange}
                required
                // whileFocus={{ scale: 1.02 }}
                transition={{ duration: 0.2 }}
              >
                {routes.map((route) => (
                  <option key={route} value={route}>
                    {route}
                  </option>
                ))}
              </motion.select>
            </motion.div>

            <motion.div className="form-group" variants={staggerItem}>
              <label>Scheduled Date</label>
              <motion.input
                type="date"
                name="scheduled_date"
                value={formData.scheduled_date}
                onChange={handleChange}
                required
                whileFocus={{ scale: 1.02 }}
                transition={{ duration: 0.2 }}
              />
            </motion.div>

            <motion.div className="form-group" variants={staggerItem}>
              <label>Hour</label>
              <motion.input
                type="number"
                name="hour"
                value={formData.hour}
                onChange={handleChange}
                min="0"
                max="23"
                required
                whileFocus={{ scale: 1.02 }}
                transition={{ duration: 0.2 }}
              />
            </motion.div>

            <motion.div className="form-group" variants={staggerItem}>
              <label>Minute</label>
              <motion.input
                type="number"
                name="minute"
                value={formData.minute}
                onChange={handleChange}
                min="0"
                max="59"
                required
                whileFocus={{ scale: 1.02 }}
                transition={{ duration: 0.2 }}
              />
            </motion.div>
          </motion.div>

          <motion.div
            className="form-row"
            variants={{
              hidden: { opacity: 0 },
              show: {
                opacity: 1,
                transition: {
                  staggerChildren: 0.05,
                  delayChildren: 0.2,
                },
              },
            }}
            initial="hidden"
            animate="show"
          >
            <motion.div className="form-group" variants={staggerItem}>
              <label>Weather Condition</label>
              <motion.select
                name="weather"
                value={formData.weather}
                onChange={handleChange}
                required
                whileFocus={{ scale: 1.02 }}
                transition={{ duration: 0.2 }}
              >
                <option value="sunny">Sunny</option>
                <option value="cloudy">Cloudy</option>
                <option value="rainy">Rainy</option>
                <option value="unknown">Unknown</option>
              </motion.select>
            </motion.div>

            <motion.div className="form-group" variants={staggerItem}>
              <label>Passenger Count</label>
              <motion.input
                type="number"
                name="passenger_count"
                value={formData.passenger_count}
                onChange={handleChange}
                min="0"
                max="200"
                required
                whileFocus={{ scale: 1.02 }}
                transition={{ duration: 0.2 }}
              />
            </motion.div>

            <motion.div className="form-group" variants={staggerItem}>
              <label>Latitude</label>
              <motion.input
                type="number"
                name="latitude"
                value={formData.latitude}
                onChange={handleChange}
                step="0.1"
                min="23.0"
                max="26.0"
                required
                whileFocus={{ scale: 1.02 }}
                transition={{ duration: 0.2 }}
              />
            </motion.div>

            <motion.div className="form-group" variants={staggerItem}>
              <label>Longitude</label>
              <motion.input
                type="number"
                name="longitude"
                value={formData.longitude}
                onChange={handleChange}
                step="0.1"
                min="31.0"
                max="34.0"
                required
                whileFocus={{ scale: 1.02 }}
                transition={{ duration: 0.2 }}
              />
            </motion.div>
          </motion.div>

          <motion.div
            className="form-group"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4, duration: 0.5 }}
          >
            <label>Model</label>
            <motion.select
              name="model_name"
              value={formData.model_name}
              onChange={handleChange}
              required
              whileFocus={{ scale: 1.02 }}
              transition={{ duration: 0.2 }}
            >
              <option value="xgboost">XGBoost</option>
              <option value="random_forest">Random Forest</option>
              <option value="linear_regression">Linear Regression</option>
              <option value="knn">kNN</option>
            </motion.select>
          </motion.div>

          <motion.button
            type="submit"
            className="btn btn-primary"
            disabled={loading}
            whileHover={!loading ? buttonHover : {}}
            whileTap={!loading ? buttonTap : {}}
            transition={{ duration: 0.2 }}
          >
            {loading ? (
              <>
                <LoadingSpinner size={20} color="white" />
                Predicting...
              </>
            ) : (
              '🔮 Predict Delay'
            )}
          </motion.button>
        </form>
      </AnimatedCard>

      <AnimatePresence mode="wait">
        {prediction && (
          <motion.div
            key="prediction"
            initial={{ opacity: 0, scale: 0.9, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.9, y: -20 }}
            transition={{ duration: 0.4, ease: [0.6, -0.05, 0.01, 0.99] }}
          >
            <AnimatedCard>
              <h2>✨ Prediction Results</h2>
              <div className="prediction-result">
                <motion.div
                  className="metric-label"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: 0.2 }}
                >
                  Predicted Delay
                </motion.div>
                <motion.div
                  className="prediction-value"
                  initial={{ opacity: 0, scale: 0.5 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{
                    delay: 0.3,
                    type: 'spring',
                    stiffness: 200,
                    damping: 15,
                  }}
                >
                  {prediction.prediction.toFixed(1)} minutes
                </motion.div>
                <motion.div
                  className={`status-badge ${getStatusClass(prediction.status)}`}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.4 }}
                  whileHover={{ scale: 1.05 }}
                >
                  {prediction.emoji} {prediction.status}
                </motion.div>
                <motion.div
                  className="metric-label"
                  style={{ marginTop: '1rem' }}
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: 0.5 }}
                >
                  Model: {prediction.model_name.replace('_', ' ').toUpperCase()}
                </motion.div>
              </div>
            </AnimatedCard>
          </motion.div>
        )}
      </AnimatePresence>

      <AnimatePresence>
        {allPredictions && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.4, delay: 0.2 }}
          >
            <AnimatedCard delay={0.3}>
              <h2>🔍 All Model Predictions Comparison</h2>
              <div className="table-container">
                <motion.table
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: 0.4 }}
                >
                  <thead>
                    <tr>
                      <th>Model</th>
                      <th>Predicted Delay (min)</th>
                      <th>MAE (from training)</th>
                      <th>R² Score</th>
                    </tr>
                  </thead>
                  <tbody>
                    {Object.entries(allPredictions).map(([modelName, data], index) => (
                      <motion.tr
                        key={modelName}
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: 0.5 + index * 0.1 }}
                        whileHover={{ backgroundColor: 'rgba(0, 0, 0, 0.02)' }}
                      >
                        <td>{modelName.replace('_', ' ').toUpperCase()}</td>
                        <td>{data.prediction.toFixed(2)}</td>
                        <td>{data.mae.toFixed(2)}</td>
                        <td>{data.r2.toFixed(4)}</td>
                      </motion.tr>
                    ))}
                  </tbody>
                </motion.table>
              </div>
            </AnimatedCard>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

export default Predict;
