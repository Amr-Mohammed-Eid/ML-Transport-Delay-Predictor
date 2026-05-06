"""
FastAPI Backend for Transport Delay Prediction
RESTful API for the React frontend
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict
import sys
import os
import pandas as pd

# Add parent directory to path to import shared modules
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from backend import data, models

app = FastAPI(
    title="Transport Delay Prediction API",
    description="API for predicting bus delays using machine learning models",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for caching (in production, use proper caching)
_models_cache = None
_scaler_cache = None
_encoders_cache = None
_metadata_cache = None
_data_cache = None
_route_counts_cache = None


def get_models():
    """Get or load models (cached)"""
    global _models_cache, _scaler_cache, _encoders_cache, _metadata_cache
    if _models_cache is None:
        _models_cache, _scaler_cache, le_route, le_time_of_day, le_weather, le_weather_severity, _metadata_cache = models.load_models()
        _encoders_cache = {
            'route': le_route,
            'time_of_day': le_time_of_day,
            'weather': le_weather,
            'weather_severity': le_weather_severity
        }
    return _models_cache, _scaler_cache, _encoders_cache, _metadata_cache


def get_data():
    """Get or load data (cached)"""
    global _data_cache, _route_counts_cache
    if _data_cache is None:
        _data_cache = data.load_data()
        _route_counts_cache = data.get_route_counts(_data_cache)
    return _data_cache, _route_counts_cache


# Pydantic models for request/response
class PredictionRequest(BaseModel):
    route_id: str
    scheduled_time: str  # Format: "YYYY-MM-DD HH:MM:SS"
    weather: str
    passenger_count: float
    latitude: float
    longitude: float
    model_name: Optional[str] = "xgboost"


class PredictionResponse(BaseModel):
    prediction: float
    model_name: str
    status: str
    emoji: str


class AllPredictionsResponse(BaseModel):
    predictions: Dict[str, Dict[str, float]]


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Transport Delay Prediction API"}


@app.get("/api/stats")
async def get_stats():
    """Get dashboard statistics"""
    try:
        df, _ = get_data()
        stats = data.compute_dashboard_stats(df)
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/routes")
async def get_routes():
    """Get list of all routes"""
    try:
        df, _ = get_data()
        routes = sorted(df['route_id'].unique().tolist())
        return {"routes": routes}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/delay-by-route")
async def get_delay_by_route():
    """Get delay statistics by route"""
    try:
        df, _ = get_data()
        result = data.compute_delay_by_route(df)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/delay-by-weather")
async def get_delay_by_weather():
    """Get delay statistics by weather"""
    try:
        df, _ = get_data()
        result = data.compute_delay_by_weather(df)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/delay-distribution")
async def get_delay_distribution():
    """Get delay distribution for histogram"""
    try:
        df, _ = get_data()
        delays = data.get_delay_distribution(df)
        return {"delays": delays}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/correlation")
async def get_correlation():
    """Get correlation matrix"""
    try:
        df, _ = get_data()
        corr_matrix = data.compute_correlation_matrix(df)
        # Convert nested dict to list format for easier frontend handling
        numeric_cols = ['delay_minutes', 'passenger_count', 'latitude', 'longitude']
        matrix_data = []
        for col1 in numeric_cols:
            row = []
            for col2 in numeric_cols:
                row.append(corr_matrix.get(col1, {}).get(col2, 0))
            matrix_data.append(row)
        return {
            "matrix": matrix_data,
            "columns": numeric_cols,
            "rows": numeric_cols
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/predict", response_model=PredictionResponse)
async def predict_delay(request: PredictionRequest):
    """Make delay prediction"""
    try:
        models_dict, scaler, encoders, metadata = get_models()
        _, route_counts = get_data()
        
        # Prepare input data
        input_data = {
            'route_id': request.route_id,
            'scheduled_time': request.scheduled_time,
            'weather': request.weather,
            'passenger_count': request.passenger_count,
            'latitude': request.latitude,
            'longitude': request.longitude
        }
        
        # Make prediction
        prediction = models.predict_delay(
            models_dict, scaler,
            encoders['route'], encoders['time_of_day'],
            encoders['weather'], encoders['weather_severity'],
            route_counts, input_data, request.model_name
        )
        
        # Determine status
        if prediction < 0:
            status = "Early"
            emoji = "🟢"
        elif prediction < 30:
            status = "On Time"
            emoji = "🟢"
        elif prediction < 60:
            status = "Minor Delay"
            emoji = "🟡"
        else:
            status = "Significant Delay"
            emoji = "🔴"
        
        return PredictionResponse(
            prediction=prediction,
            model_name=request.model_name,
            status=status,
            emoji=emoji
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/predict/all", response_model=AllPredictionsResponse)
async def predict_all_models_endpoint(request: PredictionRequest):
    """Get predictions from all models"""
    try:
        models_dict, scaler, encoders, metadata = get_models()
        _, route_counts = get_data()
        
        # Prepare input data
        input_data = {
            'route_id': request.route_id,
            'scheduled_time': request.scheduled_time,
            'weather': request.weather,
            'passenger_count': request.passenger_count,
            'latitude': request.latitude,
            'longitude': request.longitude
        }
        
        # Get predictions from all models
        predictions = models.predict_all_models(
            models_dict, scaler,
            encoders['route'], encoders['time_of_day'],
            encoders['weather'], encoders['weather_severity'],
            route_counts, input_data, metadata
        )
        
        return AllPredictionsResponse(predictions=predictions)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/models/performance")
async def get_model_performance():
    """Get model performance metrics"""
    try:
        _, _, _, metadata = get_models()
        return {
            "test_mae": metadata['test_mae'],
            "test_r2": metadata['test_r2']
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/data/preview")
async def get_data_preview(page: int = 1, page_size: int = 20):
    """Get dataset preview with pagination"""
    try:
        df, _ = get_data()
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        
        # Convert to dict for JSON serialization
        preview_df = df.iloc[start_idx:end_idx]
        records = preview_df.to_dict(orient='records')
        
        # Convert datetime objects to strings
        for record in records:
            if 'scheduled_time' in record:
                record['scheduled_time'] = str(record['scheduled_time'])
            if 'actual_time' in record:
                record['actual_time'] = str(record['actual_time'])
        
        return {
            "records": records,
            "page": page,
            "page_size": page_size,
            "total_records": len(df),
            "total_pages": (len(df) + page_size - 1) // page_size
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/data/filter")
async def filter_data(
    route_id: Optional[str] = None,
    weather: Optional[str] = None,
    max_delay: Optional[float] = None
):
    """Filter dataset by route, weather, and max delay"""
    try:
        df, _ = get_data()
        filtered_df = df.copy()
        
        if route_id:
            filtered_df = filtered_df[filtered_df['route_id'] == route_id]
        if weather:
            filtered_df = filtered_df[filtered_df['weather'] == weather]
        if max_delay is not None:
            filtered_df = filtered_df[filtered_df['delay_minutes'] <= max_delay]
        
        records = filtered_df.to_dict(orient='records')
        
        # Convert datetime objects to strings
        for record in records:
            if 'scheduled_time' in record:
                record['scheduled_time'] = str(record['scheduled_time'])
            if 'actual_time' in record:
                record['actual_time'] = str(record['actual_time'])
        
        return {
            "records": records,
            "count": len(filtered_df)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/data/statistics")
async def get_statistics():
    """Get dataset statistics"""
    try:
        df, _ = get_data()
        
        # Delay statistics
        delay_stats = df['delay_minutes'].describe().to_dict()
        
        # Passenger count statistics
        passenger_stats = df['passenger_count'].describe().to_dict()
        
        # Delay by route
        delay_by_route = df.groupby('route_id')['delay_minutes'].agg(['mean', 'median', 'std', 'count'])
        delay_by_route_dict = delay_by_route.sort_values('mean', ascending=False).to_dict(orient='index')
        
        # Delay by weather
        delay_by_weather = df.groupby('weather')['delay_minutes'].agg(['mean', 'median', 'std', 'count'])
        delay_by_weather_dict = delay_by_weather.sort_values('mean', ascending=False).to_dict(orient='index')
        
        return {
            "delay_stats": {k: float(v) if not pd.isna(v) else None for k, v in delay_stats.items()},
            "passenger_stats": {k: float(v) if not pd.isna(v) else None for k, v in passenger_stats.items()},
            "delay_by_route": {k: {k2: float(v2) if not pd.isna(v2) else None for k2, v2 in v.items()} 
                              for k, v in delay_by_route_dict.items()},
            "delay_by_weather": {k: {k2: float(v2) if not pd.isna(v2) else None for k2, v2 in v.items()} 
                                for k, v in delay_by_weather_dict.items()}
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/data/routes-list")
async def get_routes_list():
    """Get list of unique routes for filtering"""
    try:
        df, _ = get_data()
        return {"routes": sorted(df['route_id'].unique().tolist())}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/data/weather-list")
async def get_weather_list():
    """Get list of unique weather conditions for filtering"""
    try:
        df, _ = get_data()
        return {"weather": sorted(df['weather'].unique().tolist())}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

