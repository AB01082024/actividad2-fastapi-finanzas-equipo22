"""
Módulo de features (variables) para el modelo.
Toma los datos crudos y calcula indicadores simples de mercado.
"""

import pandas as pd
from pathlib import Path

RAW_DATA_PATH = Path("data/raw")
PROCESSED_DATA_PATH = Path("data/processed")


def build_features(symbol: str) -> pd.DataFrame:
    """
    Lee el CSV crudo de un símbolo y calcula las variables (features).
    """
    file_path = RAW_DATA_PATH / f"{symbol}.csv"
    df = pd.read_csv(file_path, index_col=0, parse_dates=True)

    # Retorno diario: % de cambio del precio de cierre respecto al día anterior
    df["return"] = df["Close"].pct_change()

    # Medias móviles: promedio de los últimos 5 y 20 días
    df["ma_5"] = df["Close"].rolling(window=5).mean()
    df["ma_20"] = df["Close"].rolling(window=20).mean()

    # Volatilidad: qué tanto varían los retornos en una ventana de 5 días
    df["volatility"] = df["return"].rolling(window=5).std()

    # Variable objetivo: ¿el retorno de MAÑANA será positivo (1) o negativo (0)?
    df["target"] = (df["return"].shift(-1) > 0).astype(int)

    # Quitar filas con datos faltantes (los primeros días no tienen medias móviles completas)
    df = df.dropna()

    PROCESSED_DATA_PATH.mkdir(parents=True, exist_ok=True)
    output_path = PROCESSED_DATA_PATH / f"{symbol}_features.csv"
    df.to_csv(output_path)
    print(f"Features guardadas en {output_path}")

    return df


def build_all_features(symbols: list[str] = ["AAPL", "MSFT", "TSLA"]) -> None:
    for symbol in symbols:
        build_features(symbol)


if __name__ == "__main__":
    build_all_features()
