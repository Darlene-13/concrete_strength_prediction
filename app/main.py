"""
FastAPI application entry point.
Defines routes, handles startup/shutdown, wires everything together.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(BASE_DIR, 'src')
sys.path.insert(0, SRC_DIR)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from schemas import ConcreteInput, PredictionOutput
from model_service import load_model, predict


@asynccontextmanager
async def lifespan(app: FastAPI):
    # STARTUP
    app.state.model = load_model()
    print("Model loaded and API ready")
    yield
    # SHUTDOWN
    print("API shutting down")


app = FastAPI(
    title="Concrete Strength Prediction API",
    description="Predicts concrete compressive strength from mix ingredients",
    version="1.0.0",
    lifespan=lifespan
)


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "model_loaded": app.state.model is not None
    }


@app.post("/predict", response_model=PredictionOutput)
def predict_strength(input_data: ConcreteInput):
    try:
        result = predict(app.state.model, input_data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))