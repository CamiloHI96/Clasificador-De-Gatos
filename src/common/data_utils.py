from __future__ import annotations

import json
import pickle
from pathlib import Path

import cv2
import numpy as np


IMAGE_SIZE = (64, 64)
VALID_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp"}
DATASET_DIR = Path("dataset")
MODELS_DIR = Path("modelos")
MODELS_FILE = MODELS_DIR / "modelos.pkl"
METRICS_FILE = MODELS_DIR / "metricas.json"
DEFAULT_CLASSES = ["persa", "siames", "bengali", "sphynx", "maine_coon"]


def ensure_project_dirs() -> None:
    """Crea carpetas básicas del proyecto si no existen."""
    MODELS_DIR.mkdir(exist_ok=True)
    DATASET_DIR.mkdir(exist_ok=True)
    for class_name in DEFAULT_CLASSES:
        (DATASET_DIR / class_name).mkdir(exist_ok=True)


def list_class_names(dataset_dir: Path = DATASET_DIR) -> list[str]:
    """Devuelve las clases usando los nombres de carpetas del dataset."""
    if not dataset_dir.exists():
        return []
    return sorted(item.name for item in dataset_dir.iterdir() if item.is_dir())


def image_to_vector(image: np.ndarray, image_size: tuple[int, int] = IMAGE_SIZE) -> np.ndarray:
    """Convierte una imagen a vector simple en escala de grises."""
    resized = cv2.resize(image, image_size)
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    normalized = gray.astype(np.float32) / 255.0
    return normalized.flatten()


def load_image_file(image_path: str | Path, image_size: tuple[int, int] = IMAGE_SIZE) -> np.ndarray:
    """Lee una imagen desde disco y la convierte a vector numérico."""
    image = cv2.imread(str(image_path))
    if image is None:
        raise ValueError(f"No se pudo leer la imagen: {image_path}")
    return image_to_vector(image, image_size=image_size)


def load_uploaded_file(file_bytes: bytes, image_size: tuple[int, int] = IMAGE_SIZE) -> np.ndarray:
    """Convierte la imagen subida en Streamlit a vector numérico."""
    array = np.frombuffer(file_bytes, dtype=np.uint8)
    image = cv2.imdecode(array, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError("No se pudo procesar la imagen subida.")
    return image_to_vector(image, image_size=image_size)


def load_dataset(
    dataset_dir: Path = DATASET_DIR,
) -> tuple[np.ndarray, np.ndarray, list[str], dict[str, int]]:
    """Carga todas las imágenes del dataset y crea X, y y estadísticas simples."""
    class_names = list_class_names(dataset_dir)
    features: list[np.ndarray] = []
    labels: list[int] = []
    class_counts: dict[str, int] = {}

    for class_index, class_name in enumerate(class_names):
        class_dir = dataset_dir / class_name
        image_count = 0

        for image_path in sorted(class_dir.iterdir()):
            if image_path.suffix.lower() not in VALID_EXTENSIONS:
                continue
            try:
                vector = load_image_file(image_path)
            except ValueError:
                continue
            features.append(vector)
            labels.append(class_index)
            image_count += 1

        class_counts[class_name] = image_count

    if not features:
        raise ValueError(
            "No se encontraron imágenes válidas en el dataset. "
            "Agrega imágenes dentro de las carpetas de cada raza."
        )

    return np.array(features), np.array(labels), class_names, class_counts


def save_training_artifacts(data: dict) -> None:
    """Guarda modelos y métricas del entrenamiento."""
    ensure_project_dirs()
    with MODELS_FILE.open("wb") as file:
        pickle.dump(data, file)


def load_training_artifacts() -> dict:
    """Carga los modelos y resultados guardados."""
    if not MODELS_FILE.exists():
        raise FileNotFoundError(
            "No se encontraron modelos entrenados. Ejecuta primero: uv run python main.py train"
        )
    with MODELS_FILE.open("rb") as file:
        return pickle.load(file)


def save_metrics(metrics: dict) -> None:
    """Guarda métricas en JSON para consultarlas fácilmente."""
    ensure_project_dirs()
    with METRICS_FILE.open("w", encoding="utf-8") as file:
        json.dump(metrics, file, indent=4, ensure_ascii=False)


def rename_dataset_images(dataset_dir: Path = DATASET_DIR) -> dict[str, int]:
    """Renombra imágenes por carpeta usando números simples."""
    ensure_project_dirs()
    renamed_counts: dict[str, int] = {}

    for class_name in list_class_names(dataset_dir):
        class_dir = dataset_dir / class_name
        valid_files = [
            image_path
            for image_path in sorted(class_dir.iterdir())
            if image_path.is_file() and image_path.suffix.lower() in VALID_EXTENSIONS
        ]

        temp_files: list[Path] = []
        for index, image_path in enumerate(valid_files, start=1):
            temp_path = class_dir / f"__temp_{index}{image_path.suffix.lower()}"
            image_path.rename(temp_path)
            temp_files.append(temp_path)

        for index, temp_path in enumerate(temp_files, start=1):
            final_path = class_dir / f"{index}{temp_path.suffix.lower()}"
            temp_path.rename(final_path)

        renamed_counts[class_name] = len(temp_files)

    return renamed_counts
