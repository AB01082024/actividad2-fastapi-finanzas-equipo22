"""
Pruebas automaticas de la API financiera.
Verifica que los contratos y endpoints principales funcionen correctamente.
"""

from fastapi.testclient import TestClient
from src.financial_api.api import app

client = TestClient(app)


def test_root():
    """La puerta de entrada debe responder con exito."""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_health():
    """El endpoint de salud debe indicar que la API y el modelo estan disponibles."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["model_loaded"] is True


def test_market_data_valid_symbol():
    """Debe devolver datos de mercado para un simbolo valido."""
    response = client.get("/market-data/AAPL")
    assert response.status_code == 200
    data = response.json()
    assert data["symbol"] == "AAPL"
    assert "last_close" in data


def test_market_data_invalid_symbol():
    """Debe devolver error 404 para un simbolo que no existe."""
    response = client.get("/market-data/NOEXISTE")
    assert response.status_code == 404


def test_predict_valid_request():
    """Debe devolver una prediccion valida (up o down) para un simbolo conocido."""
    payload = {
        "symbol": "AAPL",
        "prediction_horizon": 1,
        "use_cached_data": True,
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["prediction"] in ["up", "down"]
    assert 0 <= data["probability_up"] <= 1


def test_predict_missing_symbol():
    """Debe rechazar la peticion si falta el campo obligatorio 'symbol'."""
    response = client.post("/predict", json={})
    assert response.status_code == 422  # error de validacion de Pydantic


def test_model_metadata():
    """Debe devolver la informacion del modelo entrenado."""
    response = client.get("/model/metadata")
    assert response.status_code == 200
    data = response.json()
    assert data["model_version"] == "random_forest_v1"