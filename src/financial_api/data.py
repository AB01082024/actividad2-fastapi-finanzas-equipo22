"""
Módulo de ingesta de datos.
Descarga precios históricos de acciones usando yfinance
y los guarda localmente para que la API no dependa de internet.
"""

import yfinance as yf
import pandas as pd
from pathlib import Path

# Carpeta donde vamos a guardar los datos descargados
RAW_DATA_PATH = Path("data/raw")

# Los 3 activos financieros que vamos a usar (mínimo pide 3)
SYMBOLS = ["AAPL", "MSFT", "TSLA"]


def download_data(symbols: list[str] = SYMBOLS, period: str = "2y") -> dict[str, pd.DataFrame]:
    """
    Descarga datos históricos de cada símbolo y los guarda en CSV.
    """
    RAW_DATA_PATH.mkdir(parents=True, exist_ok=True)  # crea la carpeta si no existe

    data = {}
    for symbol in symbols:
        print(f"Descargando datos de {symbol}...")
        ticker = yf.Ticker(symbol)
        df = ticker.history(period=period)

        file_path = RAW_DATA_PATH / f"{symbol}.csv"
        df.to_csv(file_path)
        print(f"Guardado en {file_path}")

        data[symbol] = df

    return data


if __name__ == "__main__":
    download_data()
    