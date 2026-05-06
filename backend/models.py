"""
Model loading and prediction functions
Shared between Streamlit and FastAPI
"""
import joblib
import json
import os
import numpy as np
import pandas as pd


def load_models():
    """Load trained models and preprocessors"""
    base_dir = os.path.dirname(os.path.dirname(__file__))
    models_dir = os.path.join(base_dir, 'models')
    
    if not os.path.exists(os.path.join(models_dir, 'linear_regression.pkl')):
        raise FileNotFoundError("Models not found! Please run 'python train_models.py' first.")
    
    models = {
        'linear_regression': joblib.load(os.path.join(models_dir, 'linear_regression.pkl')),
        'random_forest': joblib.load(os.path.join(models_dir, 'random_forest.pkl')),
        'xgboost': joblib.load(os.path.join(models_dir, 'xgboost.pkl')),
        'knn': joblib.load(os.path.join(models_dir, 'knn.pkl'))
    }
    
    scaler = joblib.load(os.path.join(models_dir, 'scaler.pkl'))
    le_route = joblib.load(os.path.join(models_dir, 'label_encoder_route.pkl'))
    le_time_of_day = joblib.load(os.path.join(models_dir, 'label_encoder_time_of_day.pkl'))
    le_weather = joblib.load(os.path.join(models_dir, 'label_encoder_weather.pkl'))
    le_weather_severity = joblib.load(os.path.join(models_dir, 'label_encoder_weather_severity.pkl'))
    
    with open(os.path.join(models_dir, 'metadata.json'), 'r') as f:
        metadata = json.load(f)
    
    return models, scaler, le_route, le_time_of_day, le_weather, le_weather_severity, metadata


def prepare_features(row, le_route, le_time_of_day, le_weather, le_weather_severity, route_counts):
    """Prepare features for prediction"""
    # Feature engineering
    scheduled_time = pd.to_datetime(row['scheduled_time'])
    hour = scheduled_time.hour
    day_of_week = scheduled_time.dayofweek
    is_weekend = 1 if day_of_week >= 5 else 0
    month = scheduled_time.month
    day = scheduled_time.day
    
    # Time of day
    if 5 <= hour < 12:
        time_of_day = 'morning'
    elif 12 <= hour < 17:
        time_of_day = 'afternoon'
    elif 17 <= hour < 22:
        time_of_day = 'evening'
    else:
        time_of_day = 'night'
    
    # Weather severity
    weather = row['weather']
    weather_severity_map = {
        'sunny': 'light',
        'cloudy': 'moderate',
        'rainy': 'heavy',
        'unknown': 'moderate'
    }
    weather_severity = weather_severity_map.get(weather, 'moderate')
    
    # Route frequency
    route_frequency = route_counts.get(row['route_id'], 50)
    
    # Encode categorical variables
    try:
        route_id_encoded = le_route.transform([row['route_id']])[0]
    except:
        route_id_encoded = 0
    
    try:
        time_of_day_encoded = le_time_of_day.transform([time_of_day])[0]
    except:
        time_of_day_encoded = 0
    
    try:
        weather_encoded = le_weather.transform([weather])[0]
    except:
        weather_encoded = 0
    
    try:
        weather_severity_encoded = le_weather_severity.transform([weather_severity])[0]
    except:
        weather_severity_encoded = 0
    
    # Create feature vector
    features = np.array([[
        row['passenger_count'],
        row['latitude'],
        row['longitude'],
        hour,
        day_of_week,
        is_weekend,
        month,
        day,
        route_frequency,
        route_id_encoded,
        time_of_day_encoded,
        weather_encoded,
        weather_severity_encoded
    ]])
    
    return features


def predict_delay(models, scaler, le_route, le_time_of_day, le_weather, le_weather_severity, 
                  route_counts, input_data, model_name='xgboost'):
    """Make delay prediction using specified model"""
    # Prepare features
    features = prepare_features(input_data, le_route, le_time_of_day, le_weather, 
                                le_weather_severity, route_counts)
    features_scaled = scaler.transform(features)
    
    # Make prediction
    model = models[model_name]
    prediction = model.predict(features_scaled)[0]
    
    return float(prediction)


def predict_all_models(models, scaler, le_route, le_time_of_day, le_weather, le_weather_severity,
                       route_counts, input_data, metadata):
    """Get predictions from all models"""
    predictions = {}
    for model_name in models.keys():
        pred = predict_delay(models, scaler, le_route, le_time_of_day, le_weather, 
                           le_weather_severity, route_counts, input_data, model_name)
        predictions[model_name] = {
            'prediction': pred,
            'mae': metadata['test_mae'][model_name],
            'r2': metadata['test_r2'][model_name]
        }
    return predictions

