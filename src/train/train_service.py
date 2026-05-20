from __future__ import annotations

from pathlib import Path

import numpy as np
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

from src.common.data_utils import (
    DATASET_DIR,
    IMAGE_SIZE,
    ensure_project_dirs,
    load_dataset,
    save_metrics,
    save_training_artifacts,
)


def train_models() -> dict:
    """Entrena los tres modelos y devuelve resultados listos para guardar."""
    ensure_project_dirs()
    X, y, class_names, class_counts = load_dataset(DATASET_DIR)

    unique_classes, class_frequencies = np.unique(y, return_counts=True)
    if len(unique_classes) < 2:
        raise ValueError("Se necesitan al menos 2 clases diferentes para entrenar.")
    if np.min(class_frequencies) < 2:
        raise ValueError(
            "Cada clase necesita al menos 2 imágenes para poder dividir entrenamiento y prueba."
        )

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.25,
        random_state=42,
        stratify=y,
    )

    models = {
        "KNN": KNeighborsClassifier(n_neighbors=3),
        "Regresion Logistica": LogisticRegression(max_iter=2000),
        "Regresion Lineal": LinearRegression(),
    }

    trained_models: dict[str, object] = {}
    results: dict[str, dict] = {}

    for model_name, model in models.items():
        model.fit(X_train, y_train)

        if model_name == "Regresion Lineal":
            raw_predictions = model.predict(X_test)
            predictions = np.rint(raw_predictions).astype(int)
            predictions = np.clip(predictions, 0, len(class_names) - 1)
        else:
            predictions = model.predict(X_test)

        accuracy = accuracy_score(y_test, predictions)
        trained_models[model_name] = model
        results[model_name] = {"accuracy": round(float(accuracy), 4)}

    best_model_name = max(results, key=lambda name: results[name]["accuracy"])

    return {
        "models": trained_models,
        "results": results,
        "best_model_name": best_model_name,
        "class_names": class_names,
        "image_size": IMAGE_SIZE,
        "dataset_info": {
            "dataset_dir": str(DATASET_DIR),
            "total_images": int(len(X)),
            "classes": class_counts,
            "train_size": int(len(X_train)),
            "test_size": int(len(X_test)),
        },
    }


def build_metrics_for_json(training_data: dict) -> dict:
    """Arma un resumen sencillo para el archivo JSON."""
    return {
        "mejor_modelo": training_data["best_model_name"],
        "accuracy_modelos": training_data["results"],
        "explicacion_regresion_lineal": (
            "La regresión lineal predice valores continuos. "
            "Como las clases de gatos son categorías, este modelo no es ideal "
            "para clasificación y por eso se usa aquí solo para comparar."
        ),
        "dataset_info": training_data["dataset_info"],
    }


def update_results_document(training_data: dict) -> None:
    """Genera un documento simple con los resultados del entrenamiento."""
    document_path = Path("documentos/resultados_modelo.md")
    results = training_data["results"]
    best_model_name = training_data["best_model_name"]
    dataset_info = training_data["dataset_info"]

    content = f"""# Resultados del modelo

## Resumen general

- Total de imágenes: {dataset_info["total_images"]}
- Tamaño de entrenamiento: {dataset_info["train_size"]}
- Tamaño de prueba: {dataset_info["test_size"]}
- Mejor modelo: {best_model_name}

## Accuracy por modelo

- KNN: {results["KNN"]["accuracy"]}
- Regresión Logística: {results["Regresion Logistica"]["accuracy"]}
- Regresión Lineal: {results["Regresion Lineal"]["accuracy"]}

## Interpretación sencilla

- KNN compara la imagen nueva con imágenes parecidas del entrenamiento.
- Regresión Logística intenta separar las clases usando fronteras de decisión.
- Regresión Lineal no fue diseñada para clases, sino para valores numéricos continuos.

## Conclusión académica

El mejor modelo en este entrenamiento fue **{best_model_name}**.

La Regresión Lineal se incluye para comparación, pero no es ideal para clasificación de imágenes porque produce salidas continuas y luego toca convertirlas a clases.
"""
    document_path.write_text(content, encoding="utf-8")


def run_training() -> None:
    """Ejecuta el entrenamiento completo y muestra un resumen en consola."""
    training_data = train_models()
    save_training_artifacts(training_data)
    save_metrics(build_metrics_for_json(training_data))
    update_results_document(training_data)

    print("Entrenamiento completado.")
    print(f"Mejor modelo: {training_data['best_model_name']}")
    print("Accuracy por modelo:")
    for model_name, data in training_data["results"].items():
        print(f"- {model_name}: {data['accuracy']}")
