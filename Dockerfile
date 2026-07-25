FROM python:3.11-slim

WORKDIR /app

# Instalar Poetry
RUN pip install --no-cache-dir poetry

# Copiar solo los archivos de dependencias primero (mejora la velocidad de reconstruccion)
COPY pyproject.toml poetry.lock ./

# Instalar dependencias sin crear un entorno virtual adicional (ya estamos en un contenedor aislado)
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi --only main --no-root

# Copiar el resto del proyecto (codigo, datos locales, modelo entrenado)
COPY . .

EXPOSE 8000

CMD ["uvicorn", "src.financial_api.api:app", "--host", "0.0.0.0", "--port", "8000"]
