from __future__ import annotations

import argparse
import subprocess
import sys

def build_parser() -> argparse.ArgumentParser:
    """Crea el parser principal para usar el proyecto desde consola."""
    parser = argparse.ArgumentParser(
        description="Clasificador de gatos con KNN, Regresión Logística y Regresión Lineal."
    )
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("train", help="Entrena los modelos con las imágenes del dataset.")

    predict_parser = subparsers.add_parser("predict", help="Predice la raza de una imagen.")
    predict_parser.add_argument("image_path", help="Ruta de la imagen que se quiere predecir.")
    predict_parser.add_argument(
        "--model",
        dest="model_name",
        default=None,
        help="Modelo opcional: KNN, Regresion Logistica o Regresion Lineal.",
    )

    subparsers.add_parser("info", help="Muestra información general del proyecto y del dataset.")
    subparsers.add_parser("demo", help="Abre la aplicación Streamlit.")
    subparsers.add_parser("organize", help="Renombra imágenes del dataset como 1.jpg, 2.jpg, etc.")

    return parser


def show_info() -> None:
    """Muestra información simple del proyecto."""
    from src.common.data_utils import DATASET_DIR, load_training_artifacts

    print("Clasificador de gatos")
    print(f"Carpeta del dataset: {DATASET_DIR}")

    try:
        training_data = load_training_artifacts()
    except FileNotFoundError:
        print("Estado: todavía no hay modelos entrenados.")
        print("Para entrenar usa: uv run gatos train")
        return

    print("Estado: modelos entrenados encontrados.")
    print(f"Mejor modelo: {training_data['best_model_name']}")
    print(f"Total de imágenes: {training_data['dataset_info']['total_images']}")
    print("Imágenes por raza:")
    for class_name, image_count in training_data["dataset_info"]["classes"].items():
        print(f"- {class_name}: {image_count}")
    print("Accuracy por modelo:")
    for model_name, result in training_data["results"].items():
        print(f"- {model_name}: {result['accuracy']}")


def launch_demo() -> None:
    """Abre la aplicación web con Streamlit."""
    subprocess.run([sys.executable, "-m", "streamlit", "run", "src/interface/app.py"], check=True)


def organize_dataset() -> None:
    """Renombra las imágenes del dataset para dejar nombres simples."""
    from src.common.data_utils import rename_dataset_images

    renamed_counts = rename_dataset_images()
    print("Renombrado completado.")
    for class_name, image_count in renamed_counts.items():
        print(f"- {class_name}: {image_count} imágenes renombradas")


def interactive_menu() -> None:
    """Muestra un menú simple si el usuario ejecuta la CLI sin argumentos."""
    while True:
        print("\nClasificador de gatos")
        print("1. Entrenar modelos")
        print("2. Predecir imagen")
        print("3. Ver información")
        print("4. Organizar nombres del dataset")
        print("5. Abrir demo web")
        print("6. Salir")

        try:
            option = input("Elige una opción: ").strip()
        except EOFError:
            print("No se recibió entrada. Usa: uv run gatos --help")
            return

        try:
            if option == "1":
                from src.train.train_service import run_training

                run_training()
                continue

            if option == "2":
                from src.predict.predict_service import predict_image

                image_path = input("Escribe la ruta de la imagen: ").strip()
                model_name = input(
                    "Modelo opcional (knn, logistica, lineal). "
                    "Si no quieres elegir uno, presiona Enter: "
                ).strip()
                selected_model = model_name or None
                result = predict_image(image_path, selected_model)
                print(f"Modelo usado: {result['modelo']}")
                print(f"Clase predicha: {result['clase_predicha']}")
                print(f"Confianza aproximada: {result['confianza']}%")
                continue

            if option == "3":
                show_info()
                continue

            if option == "4":
                organize_dataset()
                continue

            if option == "5":
                launch_demo()
                continue

            if option == "6":
                print("Saliendo.")
                return

            print("Opción no válida. Elige un número del 1 al 6.")
        except (FileNotFoundError, ValueError) as error:
            print(f"Error: {error}")
        except KeyboardInterrupt:
            print("\nOperación cancelada.")


def main() -> None:
    """Punto de entrada principal del proyecto."""
    parser = build_parser()
    args = parser.parse_args()

    if args.command is None:
        interactive_menu()
        return

    if args.command == "train":
        from src.train.train_service import run_training

        run_training()
        return

    if args.command == "predict":
        from src.predict.predict_service import predict_image

        result = predict_image(args.image_path, args.model_name)
        print(f"Modelo usado: {result['modelo']}")
        print(f"Clase predicha: {result['clase_predicha']}")
        print(f"Confianza aproximada: {result['confianza']}%")
        return

    if args.command == "info":
        show_info()
        return

    if args.command == "demo":
        launch_demo()
        return

    if args.command == "organize":
        organize_dataset()
        return

    parser.print_help()


if __name__ == "__main__":
    main()
