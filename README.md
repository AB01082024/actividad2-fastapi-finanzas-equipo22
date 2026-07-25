# actividad2-fastapi-finanzas-equipo22

API financiera educativa con FastAPI, yfinance y Docker para prediccion de tendencias de mercado.

> Esta API es una herramienta academica de analisis de senales financieras.
> No constituye asesoria financiera ni recomendacion de compra o venta de activos.

## Descripcion

Servicio de inferencia que descarga datos historicos de AAPL, MSFT y TSLA con `yfinance`,
calcula variables de mercado (retornos, medias moviles, volatilidad), entrena un modelo
Random Forest para predecir si el retorno del dia siguiente sera positivo o negativo,
y expone el modelo mediante una API con FastAPI.

## Tecnologias

- FastAPI + Pydantic (contratos de entrada/salida)
- yfinance (datos historicos)
- scikit-learn (modelo Random Forest)
- pytest (pruebas automatizadas)
- Docker (contenedorizacion)
- Poetry (gestion de entorno)

## Como reproducir el proyecto desde cero

```bash
# 1. Instalar dependencias
poetry install

# 2. Descargar datos historicos
poetry run python -m src.financial_api.data

# 3. Calcular features (retornos, medias moviles, volatilidad)
poetry run python -m src.financial_api.features

# 4. Entrenar el modelo
poetry run python -m src.financial_api.train

# 5. Levantar la API localmente
poetry run uvicorn src.financial_api.api:app --reload

# 6. Ejecutar las pruebas automatizadas
poetry run pytest

# 7. Construir la imagen de Docker
docker build -t financial-api:local .

# 8. Correr el contenedor
docker run --rm -p 8000:8000 financial-api:local
```

## Endpoints

| Metodo | Ruta | Descripcion |
|---|---|---|
| GET | `/` | Verifica que la API esta activa |
| GET | `/health` | Confirma disponibilidad de la API y el modelo |
| GET | `/market-data/{symbol}` | Datos/features recientes de un simbolo |
| POST | `/predict` | Prediccion de tendencia (sube/baja) |
| GET | `/model/metadata` | Informacion del modelo entrenado |

Documentacion interactiva disponible en `/docs` una vez la API este corriendo.

## Simbolos utilizados

AAPL, MSFT, TSLA

## Equipo

Ver [TEAM.md](./TEAM.md) para roles y responsabilidades.