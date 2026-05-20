from __future__ import annotations

import streamlit as st

from src.common.data_utils import METRICS_FILE, load_training_artifacts
from src.predict.predict_service import predict_uploaded_image


def main() -> None:
    st.set_page_config(page_title="Clasificador de gatos", page_icon="🐱", layout="centered")

    st.title("Clasificador de razas de gatos")
    st.write(
        "Esta aplicación compara KNN, Regresión Logística y Regresión Lineal "
        "para clasificar imágenes de gatos."
    )

    try:
        training_data = load_training_artifacts()
    except FileNotFoundError as error:
        st.error(str(error))
        st.info("Primero entrena los modelos con: uv run python main.py train")
        return

    if not METRICS_FILE.exists():
        st.warning("No se encontró el archivo de métricas JSON, pero sí hay modelos entrenados.")

    results = training_data["results"]
    best_model_name = training_data["best_model_name"]

    st.subheader("Accuracy de los modelos")
    for model_name, result in results.items():
        st.write(f"- {model_name}: {result['accuracy']}")

    st.success(f"Mejor modelo entrenado: {best_model_name}")

    selected_model = st.selectbox(
        "Selecciona el modelo para predecir",
        options=list(training_data["models"].keys()),
        index=list(training_data["models"].keys()).index(best_model_name),
    )

    uploaded_file = st.file_uploader(
        "Sube una imagen de gato",
        type=["jpg", "jpeg", "png", "bmp"],
    )

    if uploaded_file is not None:
        st.image(uploaded_file, caption="Imagen subida", use_container_width=True)
        result = predict_uploaded_image(uploaded_file.getvalue(), selected_model)

        st.subheader("Resultado")
        st.write(f"Predicción: **{result['clase_predicha']}**")
        st.write(f"Confianza o similitud aproximada: **{result['confianza']}%**")

        if selected_model == "Regresion Lineal":
            st.info(
                "La Regresión Lineal no entrega probabilidades reales para clases. "
                "Por eso aquí se muestra una similitud aproximada."
            )

    st.subheader("Explicación rápida")
    st.write("KNN compara una imagen nueva con imágenes parecidas del entrenamiento.")
    st.write("La Regresión Logística clasifica usando probabilidades por clase.")
    st.write("La Regresión Lineal se incluyó solo para comparar, pero no es ideal para clasificación.")


if __name__ == "__main__":
    main()
