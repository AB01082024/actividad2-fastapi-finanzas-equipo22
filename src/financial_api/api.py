"""
API financiera educativa con FastAPI.
Expone endpoints para consultar datos de mercado y obtener predicciones
del modelo de tendencia (sube/baja).

Esta API es una herramienta academica de analisis de senales financieras.
NO constituye asesoria financiera ni recomendacion de compra o venta.
"""

import json
import joblib
import pandas as pd
from pathlib import Path
from fastapi import FastAPI, HTTPException

from src.financial_api.schemas import (
    PredictionRequest,
    PredictionResponse,
    HealthResponse,
    ModelMetadataResponse,
    MarketDataResponse,
)

app = FastAPI(
    title="Financial API - Actividad Integradora 2",
    description="API educativa de analisis de tendencia financiera con FastAPI, yfinance y Docker",
    version="1.0.0",
)

ARTIFACTS_PATH = Path("artifacts")
PROCESSED_DATA_PATH = Path("data/processed")

FEATURE_COLUMNS = ["return", "ma_5", "ma_20", "volatility"]

# Cargamos el modelo UNA sola vez cuando arranca la API (no en cada peticion)
model = None
model_metadata = None

try:
    model = joblib.load(ARTIFACTS_PATH / "model.joblib")
    with open(ARTIFACTS_PATH / "model_metadata.json") as f:
        model_metadata = json.load(f)
except FileNotFoundError:
    print("Advertencia: modelo no encontrado. Ejecuta primero train.py")


@app.get("/")
def root():
    """Puerta de entrada de la API."""
    return {"message": "Hola mundo, la API financiera esta activa"}


@app.get("/health", response_model=HealthResponse)
def health():
    """Verifica que la API este viva y que el modelo este disponible."""
    return HealthResponse(
        status="ok",
        model_loaded=model is not None,
    )


@app.get("/market-data/{symbol}", response_model=MarketDataResponse)
def get_market_data(symbol: str):
    """Devuelve las features/datos mas recientes de un simbolo."""
    file_path = PROCESSED_DATA_PATH / f"{symbol.upper()}_features.csv"

    if not file_path.exists():
        raise HTTPException(status_code=404, detail=f"No hay datos para el simbolo {symbol}")

    df = pd.read_csv(file_path, index_col=0, parse_dates=True)
    last_row = df.iloc[-1]

    return MarketDataResponse(
        symbol=symbol.upper(),
        last_close=float(last_row["Close"]),
        last_return=float(last_row["return"]),
        ma_5=float(last_row["ma_5"]),
        ma_20=float(last_row["ma_20"]),
        volatility=float(last_row["volatility"]),
    )


@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    """Recibe un simbolo y devuelve la prediccion de tendencia del modelo."""
    if model is None:
        raise HTTPException(status_code=503, detail="El modelo no esta disponible")

    file_path = PROCESSED_DATA_PATH / f"{request.symbol.upper()}_features.csv"
    if not file_path.exists():
        raise HTTPException(status_code=404, detail=f"No hay datos para el simbolo {request.symbol}")

    df = pd.read_csv(file_path, index_col=0, parse_dates=True)
    last_row = df.iloc[-1]

    X = last_row[FEATURE_COLUMNS].values.reshape(1, -1)

    prediction = model.predict(X)[0]
    probability_up = model.predict_proba(X)[0][1]

    return PredictionResponse(
        symbol=request.symbol.upper(),
        prediction="up" if prediction == 1 else "down",
        probability_up=round(float(probability_up), 4),
        model_version=model_metadata["model_version"],
        prediction_horizon="next_day",
    )


@app.get("/model/metadata", response_model=ModelMetadataResponse)
def get_model_metadata():
    """Devuelve informacion sobre el modelo entrenado."""
    if model_metadata is None:
        raise HTTPException(status_code=503, detail="Metadatos del modelo no disponibles")

    return ModelMetadataResponse(**model_metadata)
