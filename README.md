# Transport Delay Predictor

AI-Powered Bus Delay Analysis & Prediction System

This project provides multiple interfaces for predicting and analyzing bus delays using machine learning models:
- **Streamlit App**: Quick prototyping and data exploration
- **React + FastAPI**: Modern web application with RESTful API

## Features

- 🚌 Predict bus delays using multiple ML models (Linear Regression, Random Forest, XGBoost, kNN)
- 📊 Interactive dashboards with visualizations
- 📈 Comprehensive data analysis tools
- 🤖 Model performance comparison
- 🔮 Real-time delay predictions

## Project Structure

```
project-root/
├── app.py                    # Streamlit application
├── train_models.py          # Model training script
├── models/                   # Trained ML models
├── backend/                  # FastAPI backend
│   ├── main.py              # FastAPI application
│   ├── models.py            # Model loading functions
│   ├── data.py              # Data processing functions
│   └── requirements.txt     # Backend dependencies
└── frontend/                 # React frontend
    ├── src/
    │   ├── App.jsx          # Main app component
    │   ├── components/       # React components
    │   └── services/        # API service layer
    └── package.json         # Frontend dependencies
```

## Prerequisites

- Python 3.8+
- Node.js 16+ and npm
- Trained ML models (run `train_models.py` first)

## Installation

### 1. Install Python Dependencies

```bash
# Install main dependencies
pip install -r requirements.txt

# Install backend dependencies
pip install -r backend/requirements.txt
```

### 2. Train Models

```bash
python train_models.py
```

This will create the `models/` directory with trained models and preprocessors.

### 3. Install Frontend Dependencies

```bash
cd frontend
npm install
```

## Running the Applications

### Option 1: Streamlit App (Quick Start)

```bash
streamlit run app.py
```

The app will be available at `http://localhost:8501`

### Option 2: React + FastAPI (Full Stack)

#### Terminal 1: Start FastAPI Backend

```bash
cd backend
uvicorn main:app --reload --port 8000
```

The API will be available at:
- API: `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`
- Alternative Docs: `http://localhost:8000/redoc`

#### Terminal 2: Start React Frontend

```bash
cd frontend
npm start
```

The frontend will be available at `http://localhost:3000`

### Option 3: Run Both Systems

You can run both Streamlit and React+FastAPI simultaneously:
- Streamlit: `http://localhost:8501`
- React: `http://localhost:3000`
- FastAPI: `http://localhost:8000`

## API Endpoints

### Health & Stats
- `GET /api/health` - Health check
- `GET /api/stats` - Dashboard statistics
- `GET /api/routes` - List all routes

### Predictions
- `POST /api/predict` - Make delay prediction
- `POST /api/predict/all` - Get predictions from all models

### Data Analysis
- `GET /api/delay-by-route` - Delay statistics by route
- `GET /api/delay-by-weather` - Delay statistics by weather
- `GET /api/delay-distribution` - Delay distribution data
- `GET /api/correlation` - Correlation matrix
- `GET /api/data/preview` - Dataset preview with pagination
- `GET /api/data/filter` - Filter dataset

### Model Performance
- `GET /api/models/performance` - Model performance metrics

## Models

The system uses four machine learning models:

1. **Linear Regression** - Baseline model
2. **Random Forest** - Ensemble method
3. **XGBoost** - Gradient boosting (best performance)
4. **kNN** - Instance-based learning

## Development

### Backend Development

The FastAPI backend uses shared modules (`backend/models.py` and `backend/data.py`) that are also imported by the Streamlit app. This ensures consistency between both interfaces.

### Frontend Development

The React frontend uses:
- React Router for navigation
- Axios for API calls
- Plotly.js for visualizations
- Modern CSS for styling

### Environment Variables

Create `frontend/.env`:
```
REACT_APP_API_URL=http://localhost:8000
```

## Troubleshooting

### Models Not Found
If you see "Models not found" error:
```bash
python train_models.py
```

### CORS Errors
If React frontend can't connect to FastAPI:
- Ensure FastAPI is running on port 8000
- Check `backend/main.py` CORS configuration
- Verify `REACT_APP_API_URL` in `frontend/.env`

### Port Already in Use
- Streamlit: Change port with `streamlit run app.py --server.port 8502`
- FastAPI: Change port in `uvicorn` command
- React: Change port in `package.json` or use `PORT=3001 npm start`

## License

This project is part of an AI course assignment.

## Authors

[Amr Mohamed]

