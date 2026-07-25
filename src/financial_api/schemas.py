"""
Contratos (schemas) de entrada y salida de la API.
Pydantic valida automaticamente que los datos tengan el formato correcto.
"""

from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    """Lo que el cliente debe enviar para pedir una prediccion."""
    symbol: str = Field(..., description="Simbolo de la accion, ej: AAPL")
    prediction_horizon: int = Field(default=1, description="Dias hacia adelante a predecir")
    use_cached_data: bool = Field(default=True, description="Usar datos locales en vez de internet")


class PredictionResponse(BaseModel):
    """Lo que la API devuelve como resultado de la prediccion."""
    symbol: str
    prediction: str  # "up" o "down"
    probability_up: float
    model_version: str
    prediction_horizon: str


class HealthResponse(BaseModel):
    """Respuesta del endpoint de salud."""
    status: str
    model_loaded: bool


class ModelMetadataResponse(BaseModel):
    """Informacion sobre el modelo entrenado."""
    model_version: str
    trained_at: str
    symbols_used: list[str]
    features: list[str]
    accuracy: float
    prediction_horizon: str


class MarketDataResponse(BaseModel):
    """Datos recientes de un simbolo."""
    symbol: str
    last_close: float
    last_return: float
    ma_5: float
    ma_20: float
    volatility: float
    