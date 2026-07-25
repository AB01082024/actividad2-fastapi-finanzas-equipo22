
"""
Modulo de entrenamiento del modelo.
Entrena un Random Forest para predecir si el retorno del dia siguiente
sera positivo o negativo, usando las features calculadas.
"""

import json
import pandas as pd
import joblib
from datetime import datetime
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

PROCESSED_DATA_PATH = Path("data/processed")
ARTIFACTS_PATH = Path("artifacts")

# Las columnas que el modelo va a usar para aprender
FEATURE_COLUMNS = ["return", "ma_5", "ma_20", "volatility"]
TARGET_COLUMN = "target"

SYMBOLS = ["AAPL", "MSFT", "TSLA"]


def load_training_data(symbols: list[str] = SYMBOLS) -> pd.DataFrame:
	"""
	Junta los datos procesados de todos los simbolos en una sola tabla.
	"""
	dataframes = []
	for symbol in symbols:
		file_path = PROCESSED_DATA_PATH / f"{symbol}_features.csv"
		df = pd.read_csv(file_path, index_col=0, parse_dates=True)
		dataframes.append(df)
	return pd.concat(dataframes)


def train_model() -> None:
	# 1. Cargar los datos ya procesados
	df = load_training_data()

	X = df[FEATURE_COLUMNS]  # las "pistas" que ve el modelo
	y = df[TARGET_COLUMN]    # lo que queremos predecir (sube=1, baja=0)

	# 2. Separar en datos de entrenamiento (80%) y de prueba (20%)
	X_train, X_test, y_train, y_test = train_test_split(
		X, y, test_size=0.2, random_state=42, shuffle=False
	)

	# 3. Crear y entrenar el modelo
	model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
	model.fit(X_train, y_train)

	# 4. Medir que tan bien predice en datos que NUNCA vio
	predictions = model.predict(X_test)
	accuracy = accuracy_score(y_test, predictions)
	print(f"Precision del modelo (accuracy): {accuracy:.2%}")

	# 5. Guardar el modelo entrenado
	ARTIFACTS_PATH.mkdir(parents=True, exist_ok=True)
	model_path = ARTIFACTS_PATH / "model.joblib"
	joblib.dump(model, model_path)
	print(f"Modelo guardado en {model_path}")

	# 6. Guardar metadatos del modelo (info importante sobre como se entreno)
	metadata = {
		"model_version": "random_forest_v1",
		"trained_at": datetime.now().isoformat(),
		"symbols_used": SYMBOLS,
		"features": FEATURE_COLUMNS,
		"target": TARGET_COLUMN,
		"accuracy": round(accuracy, 4),
		"prediction_horizon": "next_day",
	}
	metadata_path = ARTIFACTS_PATH / "model_metadata.json"
	with open(metadata_path, "w") as f:
		json.dump(metadata, f, indent=2)
	print(f"Metadatos guardados en {metadata_path}")


if __name__ == "__main__":
	train_model()
