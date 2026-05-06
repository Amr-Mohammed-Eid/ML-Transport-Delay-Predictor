"""
Streamlit Frontend for Transport Delay Prediction
Interactive web application for analyzing and predicting bus delays
Modernized with enhanced UI and performance optimizations
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns
from datetime import datetime, timedelta
import joblib
import json
import os

# Page configuration
st.set_page_config(
    page_title="Transport Delay Predictor",
    page_icon="🚌",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': "Transport Delay Predictor - AI-Powered Bus Delay Analysis"
    }
)

# Optimized CSS with GPU-Accelerated Animations
st.markdown("""
    <style>
    /* Global Styles - Optimized */
    .stApp {
        background: #f8f9fa;
    }
    
    .main .block-container {
        padding-top: 0 !important;
        padding-bottom: 2rem;
        margin-top: -2rem !important;
        will-change: transform, opacity;
    }
    
    /* Remove default Streamlit header spacing */
    header[data-testid="stHeader"] {
        display: none !important;
    }
    
    /* Target the first element in main container */
    .main .block-container > div:first-child {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    
    /* Remove spacing from Streamlit's markdown container */
    .main .block-container > div {
        margin-top: 0 !important;
    }
    
    .main .block-container > div:first-of-type {
        padding-top: 0 !important;
        margin-top: -1rem !important;
    }
    
    /* GPU-Accelerated Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translate3d(0, 10px, 0); }
        to { opacity: 1; transform: translate3d(0, 0, 0); }
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translate3d(-20px, 0, 0); }
        to { opacity: 1; transform: translate3d(0, 0, 0); }
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale3d(1, 1, 1); }
        50% { transform: scale3d(1.02, 1.02, 1); }
    }
    
    /* Header Styling - Optimized and Centered */
    .main-header {
        font-size: 3.5rem;
        font-weight: 800;
        color: #212529;
        text-align: center;
        margin: 0 auto 0.5rem auto !important;
        margin-top: 0 !important;
        padding: 0 1rem;
        padding-top: 0 !important;
        padding-bottom: 0.5rem !important;
        will-change: transform, opacity;
        animation: slideIn 0.4s ease-out;
        position: relative;
        display: block;
        width: 100%;
        max-width: 100%;
        line-height: 1.2;
    }
    
    .main-header::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 50%;
        transform: translate3d(-50%, 0, 0);
        width: 100px;
        height: 4px;
        background: #212529;
        will-change: width;
        animation: expandWidth 0.5s ease-out 0.2s both;
        border-radius: 2px;
    }
    
    /* Ensure header container is centered */
    .main .block-container > div:first-child {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 100%;
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    
    /* Remove any spacing from markdown elements */
    .main .block-container h1 {
        margin-top: 0 !important;
        padding-top: 0 !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Target the markdown container directly */
    .main .block-container [data-testid="stMarkdownContainer"]:first-of-type {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    
    @keyframes expandWidth {
        from { width: 0; }
        to { width: 100px; }
    }
    
    .sub-header {
        font-size: 1.2rem;
        color: #6c757d;
        text-align: center;
        margin-bottom: 1rem;
        margin-top: 0;
        font-weight: 300;
        will-change: opacity;
        animation: fadeIn 0.5s ease-out 0.1s both;
    }
    
    /* Metric Cards - Optimized with GPU acceleration */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: #212529;
        will-change: transform, opacity;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.9rem;
        font-weight: 500;
        color: #6c757d;
    }
    
    [data-testid="stMetricContainer"] {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        transition: transform 0.2s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.2s ease;
        border: 1px solid #e9ecef;
        position: relative;
        overflow: hidden;
        will-change: transform;
        backface-visibility: hidden;
    }
    
    [data-testid="stMetricContainer"]:hover {
        transform: translate3d(0, -4px, 0);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.12);
        border-color: #dee2e6;
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background-color: #ffffff;
        box-shadow: 2px 0 8px rgba(0, 0, 0, 0.05);
    }
    
    /* Button Styling - Optimized */
    .stButton > button {
        background: #212529;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 2rem;
        font-weight: 600;
        transition: transform 0.15s ease, box-shadow 0.15s ease, background 0.15s ease;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        will-change: transform;
        backface-visibility: hidden;
    }
    
    .stButton > button:hover {
        transform: translate3d(0, -2px, 0);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        background: #343a40;
    }
    
    .stButton > button:active {
        transform: translate3d(0, 0, 0);
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    /* Card Styling - Optimized */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        margin: 0.5rem 0;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        border: 1px solid #e9ecef;
        will-change: transform;
        backface-visibility: hidden;
    }
    
    .metric-card:hover {
        transform: translate3d(0, -4px, 0);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.12);
    }
    
    /* Section Headers - Optimized */
    h2 {
        color: #212529;
        font-weight: 700;
        margin-top: 2rem;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #dee2e6;
        position: relative;
        will-change: transform, opacity;
    }
    
    h2::after {
        content: '';
        position: absolute;
        bottom: -2px;
        left: 0;
        width: 60px;
        height: 2px;
        background: #212529;
        will-change: width;
    }
    
    h3 {
        color: #495057;
        font-weight: 600;
        margin-top: 1.5rem;
        will-change: opacity;
    }
    
    /* Dataframe Styling */
    .dataframe {
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
        animation: fadeIn 0.5s ease-out;
    }
    
    /* Tabs Styling with Dynamic Effects */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
        font-weight: 600;
        transition: all 0.3s ease;
        position: relative;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: #f8f9fa;
    }
    
    /* Success/Info Boxes */
    .stSuccess {
        background: #f8f9fa;
        border-left: 4px solid #212529;
        border-radius: 8px;
        padding: 1rem;
        color: #212529;
        animation: slideIn 0.4s ease-out;
    }
    
    /* Prediction Result Cards - Optimized */
    .prediction-card {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        text-align: center;
        margin: 1rem 0;
        border: 1px solid #e9ecef;
        will-change: transform;
    }
    
    /* Status Badges - Neutral Colors */
    .status-early {
        background: #e9ecef;
        color: #212529;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        display: inline-block;
        animation: fadeIn 0.5s ease-out;
        border: 1px solid #dee2e6;
    }
    
    .status-ontime {
        background: #e9ecef;
        color: #212529;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        display: inline-block;
        animation: fadeIn 0.5s ease-out;
        border: 1px solid #dee2e6;
    }
    
    .status-minor {
        background: #f8f9fa;
        color: #212529;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        display: inline-block;
        animation: fadeIn 0.5s ease-out;
        border: 1px solid #dee2e6;
    }
    
    .status-significant {
        background: #f8f9fa;
        color: #212529;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        display: inline-block;
        animation: fadeIn 0.5s ease-out;
        border: 1px solid #dee2e6;
    }
    
    /* Loading Animation */
    .stSpinner > div {
        border-color: #212529 transparent transparent transparent;
    }
    
    /* Selectbox and Input Styling */
    .stSelectbox > div > div {
        transition: all 0.3s ease;
    }
    
    .stSelectbox > div > div:hover {
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    
    /* Number Input Styling */
    .stNumberInput > div > div > input {
        transition: all 0.3s ease;
    }
    
    .stNumberInput > div > div > input:focus {
        box-shadow: 0 0 0 2px rgba(33, 37, 41, 0.2);
    }
    
    /* Divider Animation */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #dee2e6, transparent);
        animation: expandWidth 0.8s ease-out;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    /* header {visibility: hidden;} */
    
    /* Smooth Scrolling */
    html {
        scroll-behavior: smooth;
    }
    
    /* Chart Container Animation */
    .js-plotly-plot {
        animation: fadeIn 0.6s ease-out;
    }
    
    /* Dynamic Number Counter Animation */
    @keyframes numberCount {
        from { opacity: 0; transform: scale(0.8); }
        to { opacity: 1; transform: scale(1); }
    }
    
    /* Stagger Animation for Metrics */
    [data-testid="stMetricContainer"]:nth-child(1) { animation-delay: 0.1s; }
    [data-testid="stMetricContainer"]:nth-child(2) { animation-delay: 0.2s; }
    [data-testid="stMetricContainer"]:nth-child(3) { animation-delay: 0.3s; }
    [data-testid="stMetricContainer"]:nth-child(4) { animation-delay: 0.4s; }
    
    /* Optimized transitions - only for interactive elements */
    button, .stSelectbox > div, .stNumberInput > div > div > input {
        transition: transform 0.15s ease, box-shadow 0.15s ease, background-color 0.15s ease;
    }
    </style>
    
    <script>
    // Optimized dynamic interactions with debouncing
    (function() {
        'use strict';
        
        // Debounce function for performance
        function debounce(func, wait) {
            let timeout;
            return function executedFunction(...args) {
                const later = () => {
                    clearTimeout(timeout);
                    func(...args);
                };
                clearTimeout(timeout);
                timeout = setTimeout(later, wait);
            };
        }
        
        // Optimized scroll animations with requestAnimationFrame
        function initScrollAnimations() {
            const observerOptions = {
                threshold: 0.1,
                rootMargin: '0px 0px -30px 0px'
            };
            
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        requestAnimationFrame(() => {
                            entry.target.style.opacity = '1';
                            entry.target.style.transform = 'translate3d(0, 0, 0)';
                        });
                        observer.unobserve(entry.target);
                    }
                });
            }, observerOptions);
            
            // Observe sections with optimized selectors
            const sections = document.querySelectorAll('h2, h3, [data-testid="stMetricContainer"]');
            sections.forEach((el, index) => {
                el.style.opacity = '0';
                el.style.transform = 'translate3d(0, 20px, 0)';
                el.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
                el.style.willChange = 'transform, opacity';
                observer.observe(el);
            });
        }
        
        // Optimized hover effects with passive listeners
        function initHoverEffects() {
            const dataframes = document.querySelectorAll('.dataframe');
            dataframes.forEach(df => {
                df.style.willChange = 'transform';
                df.style.transition = 'transform 0.2s ease';
                
                df.addEventListener('mouseenter', function() {
                    this.style.transform = 'scale3d(1.01, 1.01, 1)';
                }, { passive: true });
                
                df.addEventListener('mouseleave', function() {
                    this.style.transform = 'scale3d(1, 1, 1)';
                }, { passive: true });
            });
        }
        
        // Initialize on DOM ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => {
                initScrollAnimations();
                initHoverEffects();
            });
        } else {
            initScrollAnimations();
            initHoverEffects();
        }
    })();
    </script>
""", unsafe_allow_html=True)

@st.cache_data(ttl=3600)
def load_data():
    """Load the cleaned dataset with caching"""
    df = pd.read_csv('cleaned_transport_dataset.csv')
    df['scheduled_time'] = pd.to_datetime(df['scheduled_time'])
    df['actual_time'] = pd.to_datetime(df['actual_time'])
    return df

@st.cache_data(ttl=3600)
def get_route_counts(df):
    """Get route counts - cached"""
    return df['route_id'].value_counts().to_dict()

@st.cache_data(ttl=3600)
def compute_dashboard_stats(df):
    """Pre-compute dashboard statistics"""
    return {
        'total_records': len(df),
        'mean_delay': df['delay_minutes'].mean(),
        'median_delay': df['delay_minutes'].median(),
        'max_delay': df['delay_minutes'].max(),
        'unique_routes': len(df['route_id'].unique())
    }

@st.cache_data(ttl=3600)
def compute_delay_by_route(df):
    """Pre-compute delay by route aggregation"""
    return df.groupby('route_id')['delay_minutes'].mean().sort_values(ascending=False)

@st.cache_data(ttl=3600)
def compute_delay_by_weather(df):
    """Pre-compute delay by weather aggregation"""
    return df.groupby('weather')['delay_minutes'].mean().sort_values(ascending=False)

@st.cache_data(ttl=3600)
def compute_correlation_matrix(df):
    """Pre-compute correlation matrix"""
    numeric_cols = ['delay_minutes', 'passenger_count', 'latitude', 'longitude']
    return df[numeric_cols].corr()

@st.cache_resource
def load_models():
    """Load trained models and preprocessors with caching"""
    if not os.path.exists('models/linear_regression.pkl'):
        st.error("Models not found! Please run 'python train_models.py' first.")
        return None, None, None, None, None, None, None
    
    models = {
        'linear_regression': joblib.load('models/linear_regression.pkl'),
        'random_forest': joblib.load('models/random_forest.pkl'),
        'xgboost': joblib.load('models/xgboost.pkl'),
        'knn': joblib.load('models/knn.pkl')
    }
    
    scaler = joblib.load('models/scaler.pkl')
    le_route = joblib.load('models/label_encoder_route.pkl')
    le_time_of_day = joblib.load('models/label_encoder_time_of_day.pkl')
    le_weather = joblib.load('models/label_encoder_weather.pkl')
    le_weather_severity = joblib.load('models/label_encoder_weather_severity.pkl')
    
    with open('models/metadata.json', 'r') as f:
        metadata = json.load(f)
    
    return models, scaler, le_route, le_time_of_day, le_weather, le_weather_severity, metadata

@st.cache_data
def prepare_features(row, _le_route, _le_time_of_day, _le_weather, _le_weather_severity, route_counts):
    """Prepare features for prediction with caching"""
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
        route_id_encoded = _le_route.transform([row['route_id']])[0]
    except:
        route_id_encoded = 0
    
    try:
        time_of_day_encoded = _le_time_of_day.transform([time_of_day])[0]
    except:
        time_of_day_encoded = 0
    
    try:
        weather_encoded = _le_weather.transform([weather])[0]
    except:
        weather_encoded = 0
    
    try:
        weather_severity_encoded = _le_weather_severity.transform([weather_severity])[0]
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

# Main app
def main():
    st.markdown('<h1 class="main-header">🚌 Transport Delay Predictor</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">AI-Powered Bus Delay Analysis & Prediction System</p>', unsafe_allow_html=True)
    
    # Load data
    with st.spinner("Loading data..."):
        df = load_data()
    
    # Load models
    with st.spinner("Loading models..."):
        models, scaler, le_route, le_time_of_day, le_weather, le_weather_severity, metadata = load_models()
    
    if models is None:
        st.stop()
    
    # Pre-compute stats for sidebar
    stats = compute_dashboard_stats(df)
    
    # Sidebar navigation
    st.sidebar.markdown("## 🧭 Navigation")
    st.sidebar.markdown("---")
    page = st.sidebar.radio(
        "Choose a page",
        ["📊 Dashboard", "🔮 Predict Delay", "📈 Data Analysis", "🤖 Model Performance"],
        label_visibility="collapsed"
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 Quick Stats")
    st.sidebar.metric("Total Records", f"{stats['total_records']:,}")
    st.sidebar.metric("Avg Delay", f"{stats['mean_delay']:.1f} min")
    st.sidebar.metric("Routes", stats['unique_routes'])
    
    if page == "📊 Dashboard":
        show_dashboard(df)
    
    elif page == "🔮 Predict Delay":
        show_prediction_page(df, models, scaler, le_route, le_time_of_day, le_weather, le_weather_severity, metadata)
    
    elif page == "📈 Data Analysis":
        show_data_analysis(df)
    
    elif page == "🤖 Model Performance":
        show_model_performance(metadata, df)

def show_dashboard(df):
    """Main dashboard with overview statistics - Optimized"""
    st.header("📊 Dashboard Overview")
    
    # Use pre-computed stats
    stats = compute_dashboard_stats(df)
    
    # Key metrics with modern styling
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Records",
            value=f"{stats['total_records']:,}",
            delta=None
        )
    
    with col2:
        st.metric(
            label="Mean Delay",
            value=f"{stats['mean_delay']:.1f} min",
            delta=f"{stats['mean_delay'] - stats['median_delay']:.1f} from median"
        )
    
    with col3:
        st.metric(
            label="Median Delay",
            value=f"{stats['median_delay']:.1f} min"
        )
    
    with col4:
        st.metric(
            label="Max Delay",
            value=f"{stats['max_delay']:.1f} min"
        )
    
    st.divider()
    
    # Visualizations with Plotly - Optimized
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Delay Distribution")
        fig = px.histogram(
            df,
            x='delay_minutes',
            nbins=50,
            title='Distribution of Bus Delays',
            labels={'delay_minutes': 'Delay (minutes)', 'count': 'Frequency'},
            color_discrete_sequence=['#4682B4']
        )
        fig.add_vline(
            x=stats['mean_delay'],
            line_dash="dash",
            line_color="red",
            annotation_text=f"Mean: {stats['mean_delay']:.2f} min"
        )
        fig.add_vline(
            x=stats['median_delay'],
            line_dash="dash",
            line_color="green",
            annotation_text=f"Median: {stats['median_delay']:.2f} min"
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=12),
            height=400,
            autosize=True
        )
        fig.update_traces(marker_line_width=0)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    with col2:
        st.subheader("🚏 Delay by Route")
        delay_by_route = compute_delay_by_route(df)
        fig = go.Figure(data=[
            go.Bar(
                x=delay_by_route.index,
                y=delay_by_route.values,
                marker_color='#4682B4'
            )
        ])
        fig.update_layout(
            title='Average Delay by Route',
            xaxis_title='Route ID',
            yaxis_title='Average Delay (minutes)',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=12),
            height=400,
            xaxis_tickangle=-45,
            showlegend=False,
            autosize=True
        )
        fig.update_traces(marker_line_width=0)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🌤️ Delay by Weather")
        delay_by_weather = compute_delay_by_weather(df)
        fig = go.Figure(data=[
            go.Bar(
                x=delay_by_weather.index,
                y=delay_by_weather.values,
                marker_color='#FF7F50'
            )
        ])
        fig.update_layout(
            title='Average Delay by Weather Condition',
            xaxis_title='Weather',
            yaxis_title='Average Delay (minutes)',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=12),
            height=400,
            showlegend=False,
            autosize=True
        )
        fig.update_traces(marker_line_width=0)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    with col2:
        st.subheader("👥 Delay vs Passenger Count")
        # Sample for large datasets to improve performance
        sample_df = df.sample(min(1000, len(df))) if len(df) > 1000 else df
        fig = px.scatter(
            sample_df,
            x='passenger_count',
            y='delay_minutes',
            title='Delay vs Passenger Count',
            labels={'passenger_count': 'Passenger Count', 'delay_minutes': 'Delay (minutes)'},
            color='delay_minutes',
            color_continuous_scale='Blues',
            opacity=0.5
        )
        fig.update_traces(marker=dict(line=dict(color='black', width=0.5)))
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=12),
            height=400,
            autosize=True
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    # Data preview
    st.subheader("📋 Dataset Preview")
    st.dataframe(
        df.head(20),
        width='stretch',
        hide_index=True
    )

def show_prediction_page(df, models, scaler, le_route, le_time_of_day, le_weather, le_weather_severity, metadata):
    """Page for making delay predictions"""
    st.header("🔮 Predict Bus Delay")
    st.markdown("Enter the details below to predict the expected delay for a bus trip.")
    
    # Create form for better UX
    with st.form("prediction_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            route_id = st.selectbox("Route ID", sorted(df['route_id'].unique()))
            scheduled_date = st.date_input("Scheduled Date", value=datetime.now().date())
            time_col1, time_col2 = st.columns(2)
            with time_col1:
                hour = st.number_input("Hour", min_value=0, max_value=23, value=8)
            with time_col2:
                minute = st.number_input("Minute", min_value=0, max_value=59, value=0)
            scheduled_time = datetime.combine(scheduled_date, datetime.min.time().replace(hour=hour, minute=minute))
            weather = st.selectbox("Weather Condition", ['sunny', 'cloudy', 'rainy', 'unknown'])
            passenger_count = st.number_input("Passenger Count", min_value=0, max_value=200, value=50)
        
        with col2:
            latitude = st.number_input("Latitude", min_value=23.0, max_value=26.0, value=24.5, step=0.1)
            longitude = st.number_input("Longitude", min_value=31.0, max_value=34.0, value=32.5, step=0.1)
            model_choice = st.selectbox("Select Model", ['xgboost', 'random_forest', 'linear_regression', 'knn'])
        
        submitted = st.form_submit_button("🔮 Predict Delay", type="primary", use_container_width=True)
    
    if submitted:
        with st.spinner("Making prediction..."):
            # Use cached route counts
            route_counts = get_route_counts(df)
            
            input_row = {
                'route_id': route_id,
                'scheduled_time': scheduled_time.strftime('%Y-%m-%d %H:%M:%S'),
                'weather': weather,
                'passenger_count': float(passenger_count),
                'latitude': latitude,
                'longitude': longitude
            }
            
            # Prepare features
            features = prepare_features(input_row, le_route, le_time_of_day, le_weather, le_weather_severity, route_counts)
            features_scaled = scaler.transform(features)
            
            # Make prediction
            model = models[model_choice]
            prediction = model.predict(features_scaled)[0]
            
            # Display results
            st.divider()
            st.subheader("✨ Prediction Results")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    label="Predicted Delay",
                    value=f"{prediction:.1f} minutes",
                    delta=None
                )
            
            with col2:
                if prediction < 0:
                    status = "Early"
                    status_class = "status-early"
                    emoji = "🟢"
                elif prediction < 30:
                    status = "On Time"
                    status_class = "status-ontime"
                    emoji = "🟢"
                elif prediction < 60:
                    status = "Minor Delay"
                    status_class = "status-minor"
                    emoji = "🟡"
                else:
                    status = "Significant Delay"
                    status_class = "status-significant"
                    emoji = "🔴"
                
                st.markdown(f'<div class="{status_class}">{emoji} {status}</div>', unsafe_allow_html=True)
            
            with col3:
                st.metric(
                    label="Model Used",
                    value=model_choice.replace('_', ' ').title()
                )
            
            # Visual prediction indicator
            st.markdown("### 📊 Prediction Visualization")
            fig = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = prediction,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Predicted Delay (minutes)"},
                delta = {'reference': df['delay_minutes'].mean()},
                gauge = {
                    'axis': {'range': [None, max(120, prediction + 20)]},
                    'bar': {'color': "#212529"},
                    'steps': [
                        {'range': [0, 30], 'color': "#e9ecef"},
                        {'range': [30, 60], 'color': "#ced4da"},
                        {'range': [60, 120], 'color': "#adb5bd"}
                    ],
                    'threshold': {
                        'line': {'color': "#495057", 'width': 4},
                        'thickness': 0.75,
                        'value': 60
                    }
                }
            ))
            fig.update_layout(
                height=300, 
                paper_bgcolor='rgba(0,0,0,0)', 
                plot_bgcolor='rgba(0,0,0,0)',
                autosize=True
            )
            st.plotly_chart(fig, width='stretch', config={'displayModeBar': False})
            
            # Show all model predictions for comparison
            st.subheader("🔍 All Model Predictions Comparison")
            comparison_data = []
            for model_name, model_obj in models.items():
                pred = model_obj.predict(features_scaled)[0]
                comparison_data.append({
                    'Model': model_name.replace('_', ' ').title(),
                    'Predicted Delay (min)': f"{pred:.2f}",
                    'MAE (from training)': f"{metadata['test_mae'][model_name]:.2f}",
                    'R² Score': f"{metadata['test_r2'][model_name]:.4f}"
                })
            
            comparison_df = pd.DataFrame(comparison_data)
            st.dataframe(comparison_df, width='stretch', hide_index=True)
            
            # Visual comparison
            fig = px.bar(
                comparison_df,
                x='Model',
                y='Predicted Delay (min)',
                title='Model Prediction Comparison',
                color='Model',
                color_discrete_sequence=['#4682B4', '#FF7F50', '#90EE90', '#9370DB']
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                height=400,
                showlegend=False,
                autosize=True
            )
            fig.update_traces(marker_line_width=0)
            st.plotly_chart(fig, width='stretch', config={'displayModeBar': False})

def show_data_analysis(df):
    """Page for detailed data analysis"""
    st.header("📈 Data Analysis")
    
    tab1, tab2, tab3 = st.tabs(["📊 Statistics", "🔍 Exploratory Analysis", "📋 Raw Data"])
    
    with tab1:
        st.subheader("Dataset Statistics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Delay Statistics**")
            delay_stats = df['delay_minutes'].describe()
            st.dataframe(delay_stats.to_frame().T, width='stretch', hide_index=True)
        
        with col2:
            st.write("**Passenger Count Statistics**")
            passenger_stats = df['passenger_count'].describe()
            st.dataframe(passenger_stats.to_frame().T, width='stretch', hide_index=True)
        
        st.subheader("Delay by Route")
        delay_by_route = df.groupby('route_id')['delay_minutes'].agg(['mean', 'median', 'std', 'count'])
        st.dataframe(
            delay_by_route.sort_values('mean', ascending=False),
            width='stretch'
        )
        
        st.subheader("Delay by Weather")
        delay_by_weather = df.groupby('weather')['delay_minutes'].agg(['mean', 'median', 'std', 'count'])
        st.dataframe(
            delay_by_weather.sort_values('mean', ascending=False),
            width='stretch'
        )
    
    with tab2:
        st.subheader("Correlation Analysis")
        correlation_matrix = compute_correlation_matrix(df)
        
        # Interactive heatmap with Plotly - Optimized
        fig = px.imshow(
            correlation_matrix,
            text_auto=True,
            aspect="auto",
            title='Correlation Matrix of Numeric Features',
            color_continuous_scale='RdBu',
            labels=dict(color="Correlation")
        )
        fig.update_layout(height=600, autosize=True)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        
        st.write("**Correlation with Delay:**")
        delay_corr = correlation_matrix['delay_minutes'].sort_values(ascending=False)
        fig = go.Figure(data=[
            go.Bar(
                x=delay_corr.index,
                y=delay_corr.values,
                marker_color='#4682B4'
            )
        ])
        fig.update_layout(
            title='Correlation with Delay',
            xaxis_title='Feature',
            yaxis_title='Correlation Coefficient',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=400,
            showlegend=False,
            autosize=True
        )
        fig.update_traces(marker_line_width=0)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    with tab3:
        st.subheader("Raw Dataset")
        
        # Add filters
        col1, col2, col3 = st.columns(3)
        with col1:
            route_filter = st.multiselect("Filter by Route", df['route_id'].unique())
        with col2:
            weather_filter = st.multiselect("Filter by Weather", df['weather'].unique())
        with col3:
            max_delay_filter = st.slider("Max Delay (minutes)", 0, int(df['delay_minutes'].max()), int(df['delay_minutes'].max()))
        
        filtered_df = df.copy()
        if route_filter:
            filtered_df = filtered_df[filtered_df['route_id'].isin(route_filter)]
        if weather_filter:
            filtered_df = filtered_df[filtered_df['weather'].isin(weather_filter)]
        filtered_df = filtered_df[filtered_df['delay_minutes'] <= max_delay_filter]
        
    st.dataframe(filtered_df, width='stretch', hide_index=True)

    # Download button
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="📥 Download Filtered CSV",
        data=csv,
        file_name="transport_delay_data.csv",
        mime="text/csv",
        width='stretch'
    )

def show_model_performance(metadata, df):
    """Page showing model performance metrics"""
    st.header("🤖 Model Performance")
    
    st.subheader("Model Comparison")
    
    # Create comparison dataframe
    comparison_data = []
    for model_name in ['linear_regression', 'random_forest', 'xgboost', 'knn']:
        comparison_data.append({
            'Model': model_name.replace('_', ' ').title(),
            'Test MAE (minutes)': f"{metadata['test_mae'][model_name]:.2f}",
            'Test R² Score': f"{metadata['test_r2'][model_name]:.4f}"
        })
    
    comparison_df = pd.DataFrame(comparison_data)
    st.dataframe(comparison_df, width='stretch', hide_index=True)
    
    # Visualization with Plotly
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Mean Absolute Error Comparison")
        models_list = [m.replace('_', ' ').title() for m in metadata['test_mae'].keys()]
        mae_values = list(metadata['test_mae'].values())
        fig = go.Figure(data=[
            go.Bar(
                x=models_list,
                y=mae_values,
                marker_color=['#4682B4', '#FF7F50', '#90EE90', '#9370DB']
            )
        ])
        fig.update_layout(
            title='MAE Comparison (Lower is Better)',
            xaxis_title='Model',
            yaxis_title='MAE (minutes)',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=400,
            showlegend=False,
            autosize=True
        )
        fig.update_traces(marker_line_width=0)
    st.plotly_chart(fig, width='stretch', config={'displayModeBar': False})
    
    with col2:
        st.subheader("R² Score Comparison")
        r2_values = list(metadata['test_r2'].values())
        fig = go.Figure(data=[
            go.Bar(
                x=models_list,
                y=r2_values,
                marker_color=['#4682B4', '#FF7F50', '#90EE90', '#9370DB']
            )
        ])
        fig.update_layout(
            title='R² Score Comparison (Higher is Better)',
            xaxis_title='Model',
            yaxis_title='R² Score',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=400,
            showlegend=False,
            autosize=True
        )
        fig.update_traces(marker_line_width=0)
    st.plotly_chart(fig, width='stretch', config={'displayModeBar': False})
    
    # Best model highlight
    st.subheader("🏆 Best Model")
    best_model = min(metadata['test_mae'], key=metadata['test_mae'].get)
    st.success(f"**Best Model: {best_model.replace('_', ' ').title()}**")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Test MAE", f"{metadata['test_mae'][best_model]:.2f} minutes")
    with col2:
        st.metric("Test R²", f"{metadata['test_r2'][best_model]:.4f}")

if __name__ == "__main__":
    main()
