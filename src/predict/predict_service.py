from __future__ import annotations

import numpy as np

from src.common.data_utils import load_image_file, load_training_artifacts, load_uploaded_file


MODEL_NAME_ALIASES = {
    "knn": "KNN",
    "k": "KNN",
    "logistica": "Regresion Logistica",
    "regresion logistica": "Regresion Logistica",
    "regresion_logistica": "Regresion Logistica",
    "lineal": "Regresion Lineal",
    "regresion lineal": "Regresion Lineal",
    "regresion_lineal": "Regresion Lineal",
}


def normalize_model_name(selected_model_name: str | None) -> str | None:
    """Convierte nombres simples del usuario al nombre interno del modelo."""
    if selected_model_name is None:
        return None

    cleaned_name = selected_model_name.strip()
    if not cleaned_name:
        return None

    lowered_name = cleaned_name.lower()
    return MODEL_NAME_ALIASES.get(lowered_name, cleaned_name)


def _build_prediction_result(
    model_name: str,
    model: object,
    class_names: list[str],
    vector: np.ndarray,
) -> dict:
    """Genera una predicción sencilla y una confianza aproximada."""
    if model_name == "Regresion Lineal":
        raw_value = float(model.predict(vector)[0])
        predicted_index = int(np.clip(np.rint(raw_value), 0, len(class_names) - 1))
        confidence = max(0.0, 1.0 - abs(raw_value - predicted_index))
    else:
        predicted_index = int(model.predict(vector)[0])
        probabilities = model.predict_proba(vector)[0]
        confidence = float(probabilities[predicted_index])

    return {
        "modelo": model_name,
        "clase_predicha": class_names[predicted_index],
        "confianza": round(confidence * 100, 2),
    }


def predict_image(image_path: str, selected_model_name: str | None = None) -> dict:
    """Predice la clase de una imagen usando el modelo indicado o el mejor modelo."""
    training_data = load_training_artifacts()
    class_names = training_data["class_names"]
    best_model_name = training_data["best_model_name"]
    model_name = normalize_model_name(selected_model_name) or best_model_name
    if model_name not in training_data["models"]:
        available_models = ", ".join(training_data["models"].keys())
        raise ValueError(f"Modelo no válido. Usa uno de estos: {available_models}")
    model = training_data["models"][model_name]
    vector = load_image_file(image_path).reshape(1, -1)
    return _build_prediction_result(model_name, model, class_names, vector)


def predict_uploaded_image(file_bytes: bytes, selected_model_name: str) -> dict:
    """Predice una imagen subida desde la interfaz."""
    training_data = load_training_artifacts()
    class_names = training_data["class_names"]
    model = training_data["models"][selected_model_name]
    vector = load_uploaded_file(file_bytes).reshape(1, -1)
    return _build_prediction_result(selected_model_name, model, class_names, vector)
