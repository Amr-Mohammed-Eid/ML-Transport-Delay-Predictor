"""
Model Training Script for Transport Delay Prediction
Trains and saves models for use in the Streamlit frontend
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import xgboost as xgb
import joblib
import os

print("Loading cleaned dataset...")
df_final = pd.read_csv('cleaned_transport_dataset.csv')

# Convert to datetime for feature engineering
df_analysis = df_final.copy()
df_analysis['scheduled_time'] = pd.to_datetime(df_analysis['scheduled_time'])
df_analysis['actual_time'] = pd.to_datetime(df_analysis['actual_time'])

# Feature engineering
df_features = df_analysis.copy()

def get_time_of_day(hour):
    if 5 <= hour < 12:
        return 'morning'
    elif 12 <= hour < 17:
        return 'afternoon'
    elif 17 <= hour < 22:
        return 'evening'
    else:
        return 'night'

df_features['hour'] = df_features['scheduled_time'].dt.hour
df_features['time_of_day'] = df_features['hour'].apply(get_time_of_day)
df_features['day_of_week'] = df_features['scheduled_time'].dt.dayofweek
df_features['is_weekend'] = (df_features['day_of_week'] >= 5).astype(int)
df_features['day_type'] = df_features['is_weekend'].map({0: 'weekday', 1: 'weekend'})

def get_weather_severity(weather):
    severity_map = {
        'sunny': 'light',
        'cloudy': 'moderate',
        'rainy': 'heavy',
        'unknown': 'moderate'
    }
    return severity_map.get(weather, 'moderate')

df_features['weather_severity'] = df_features['weather'].apply(get_weather_severity)
route_counts = df_features['route_id'].value_counts()
df_features['route_frequency'] = df_features['route_id'].map(route_counts)
df_features['month'] = df_features['scheduled_time'].dt.month
df_features['day'] = df_features['scheduled_time'].dt.day

# Prepare features
feature_columns = [
    'passenger_count',
    'latitude',
    'longitude',
    'hour',
    'day_of_week',
    'is_weekend',
    'month',
    'day',
    'route_frequency'
]

# Encode categorical variables
le_route = LabelEncoder()
le_time_of_day = LabelEncoder()
le_weather = LabelEncoder()
le_weather_severity = LabelEncoder()

df_features['route_id_encoded'] = le_route.fit_transform(df_features['route_id'])
df_features['time_of_day_encoded'] = le_time_of_day.fit_transform(df_features['time_of_day'])
df_features['weather_encoded'] = le_weather.fit_transform(df_features['weather'])
df_features['weather_severity_encoded'] = le_weather_severity.fit_transform(df_features['weather_severity'])

feature_columns.extend([
    'route_id_encoded',
    'time_of_day_encoded',
    'weather_encoded',
    'weather_severity_encoded'
])

# Create feature matrix and target
X = df_features[feature_columns].copy()
y = df_features['delay_minutes'].copy()

# Remove rows with NaN
valid_mask = ~y.isna()
X = X[valid_mask].copy()
y = y[valid_mask].copy()
feature_nan_mask = ~X.isnull().any(axis=1)
X = X[feature_nan_mask].copy()
y = y[feature_nan_mask].copy()

print(f"Dataset shape: X={X.shape}, y={y.shape}")

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, shuffle=True
)

# Standardize features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train models
print("\nTraining Linear Regression...")
lr_model = LinearRegression()
lr_model.fit(X_train_scaled, y_train)
y_test_pred_lr = lr_model.predict(X_test_scaled)
lr_test_mae = mean_absolute_error(y_test, y_test_pred_lr)
lr_test_r2 = r2_score(y_test, y_test_pred_lr)
print(f"  Test MAE: {lr_test_mae:.4f}, R²: {lr_test_r2:.4f}")

print("Training Random Forest...")
rf_model = RandomForestRegressor(
    n_estimators=100,
    max_depth=10,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1
)
rf_model.fit(X_train_scaled, y_train)
y_test_pred_rf = rf_model.predict(X_test_scaled)
rf_test_mae = mean_absolute_error(y_test, y_test_pred_rf)
rf_test_r2 = r2_score(y_test, y_test_pred_rf)
print(f"  Test MAE: {rf_test_mae:.4f}, R²: {rf_test_r2:.4f}")

print("Training XGBoost...")
xgb_model = xgb.XGBRegressor(
    n_estimators=100,
    max_depth=6,
    learning_rate=0.1,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
    n_jobs=-1
)
xgb_model.fit(X_train_scaled, y_train)
y_test_pred_xgb = xgb_model.predict(X_test_scaled)
xgb_test_mae = mean_absolute_error(y_test, y_test_pred_xgb)
xgb_test_r2 = r2_score(y_test, y_test_pred_xgb)
print(f"  Test MAE: {xgb_test_mae:.4f}, R²: {xgb_test_r2:.4f}")

print("Training kNN Regression...")
knn_model = KNeighborsRegressor(
    n_neighbors=5,
    weights='distance',
    algorithm='auto',
    leaf_size=30,
    p=2,  # Euclidean distance
    metric='minkowski',
    n_jobs=-1
)
knn_model.fit(X_train_scaled, y_train)
y_test_pred_knn = knn_model.predict(X_test_scaled)
knn_test_mae = mean_absolute_error(y_test, y_test_pred_knn)
knn_test_r2 = r2_score(y_test, y_test_pred_knn)
print(f"  Test MAE: {knn_test_mae:.4f}, R²: {knn_test_r2:.4f}")

# Save models and preprocessors
os.makedirs('models', exist_ok=True)

print("\nSaving models and preprocessors...")
joblib.dump(lr_model, 'models/linear_regression.pkl')
joblib.dump(rf_model, 'models/random_forest.pkl')
joblib.dump(xgb_model, 'models/xgboost.pkl')
joblib.dump(knn_model, 'models/knn.pkl')
joblib.dump(scaler, 'models/scaler.pkl')
joblib.dump(le_route, 'models/label_encoder_route.pkl')
joblib.dump(le_time_of_day, 'models/label_encoder_time_of_day.pkl')
joblib.dump(le_weather, 'models/label_encoder_weather.pkl')
joblib.dump(le_weather_severity, 'models/label_encoder_weather_severity.pkl')

# Save feature columns and metadata
import json
metadata = {
    'feature_columns': feature_columns,
    'test_mae': {
        'linear_regression': float(lr_test_mae),
        'random_forest': float(rf_test_mae),
        'xgboost': float(xgb_test_mae),
        'knn': float(knn_test_mae)
    },
    'test_r2': {
        'linear_regression': float(lr_test_r2),
        'random_forest': float(rf_test_r2),
        'xgboost': float(xgb_test_r2),
        'knn': float(knn_test_r2)
    }
}

with open('models/metadata.json', 'w') as f:
    json.dump(metadata, f, indent=2)

print("✓ Models saved successfully!")
print("✓ Ready to use in Streamlit frontend")

