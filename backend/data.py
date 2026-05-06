"""
Data loading and preprocessing functions
Shared between Streamlit and FastAPI
"""
import pandas as pd
import numpy as np
import os


def load_data():
    """Load the cleaned dataset"""
    data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'cleaned_transport_dataset.csv')
    df = pd.read_csv(data_path)
    df['scheduled_time'] = pd.to_datetime(df['scheduled_time'])
    df['actual_time'] = pd.to_datetime(df['actual_time'])
    return df


def get_route_counts(df):
    """Get route counts"""
    return df['route_id'].value_counts().to_dict()


def compute_dashboard_stats(df):
    """Pre-compute dashboard statistics"""
    return {
        'total_records': int(len(df)),
        'mean_delay': float(df['delay_minutes'].mean()),
        'median_delay': float(df['delay_minutes'].median()),
        'max_delay': float(df['delay_minutes'].max()),
        'unique_routes': int(len(df['route_id'].unique()))
    }


def compute_delay_by_route(df):
    """Pre-compute delay by route aggregation"""
    delay_by_route = df.groupby('route_id')['delay_minutes'].mean().sort_values(ascending=False)
    return {
        'routes': delay_by_route.index.tolist(),
        'delays': delay_by_route.values.tolist()
    }


def compute_delay_by_weather(df):
    """Pre-compute delay by weather aggregation"""
    delay_by_weather = df.groupby('weather')['delay_minutes'].mean().sort_values(ascending=False)
    return {
        'weather': delay_by_weather.index.tolist(),
        'delays': delay_by_weather.values.tolist()
    }


def compute_correlation_matrix(df):
    """Pre-compute correlation matrix"""
    numeric_cols = ['delay_minutes', 'passenger_count', 'latitude', 'longitude']
    corr_matrix = df[numeric_cols].corr()
    return corr_matrix.to_dict()


def get_delay_distribution(df, bins=50):
    """Get delay distribution for histogram"""
    delays = df['delay_minutes'].dropna().tolist()
    return delays

