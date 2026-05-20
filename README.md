# Clasificador de gatos

![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![UV](https://img.shields.io/badge/UV-gesti%C3%B3n%20del%20entorno-green)
![Streamlit](https://img.shields.io/badge/Streamlit-demo-red)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-ML-orange)

Proyecto universitario en Python para clasificar imágenes de gatos por raza usando modelos sencillos de Machine Learning.

## Navegación

- [Instalación](./INSTALACION.md)
- [Problemas comunes](./PROBLEMAS_COMUNES.md)

## Contenido

- [Resumen](#resumen)
- [Qué hace el proyecto](#qué-hace-el-proyecto)
- [Inicio rápido](#inicio-rápido)
- [Cómo ejecutar el proyecto](#cómo-ejecutar-el-proyecto)
- [Dataset esperado](#dataset-esperado)
- [Archivos importantes](#archivos-importantes)

## Resumen

Este proyecto entrena tres modelos de Machine Learning:

- KNN
- Regresión Logística
- Regresión Lineal

Después compara el `accuracy` y muestra cuál funciona mejor.

También incluye una aplicación en Streamlit para subir una imagen y obtener una predicción.

## Qué hace el proyecto

El sistema hace este proceso:

1. Lee las imágenes desde la carpeta `dataset/`.
2. Redimensiona cada imagen a `64x64`.
3. Convierte la imagen a escala de grises.
4. Convierte la imagen en un vector numérico.
5. Divide los datos en entrenamiento y prueba.
6. Entrena los tres modelos.
7. Calcula el `accuracy` de cada uno.
8. Guarda los modelos entrenados.
9. Permite predecir una imagen nueva.

## Inicio rápido

1. Instalar Python 3.11 o superior.
2. Instalar `uv`.
3. Crear el entorno virtual e instalar dependencias.
4. Colocar imágenes en `dataset/`.
5. Ejecutar `uv run gatos organize`.
6. Ejecutar `uv run gatos train`.
7. Ejecutar `uv run gatos demo`.

Para la instalación detallada revisa [INSTALACION.md](./INSTALACION.md).

## Cómo ejecutar el proyecto

La forma más fácil es usar la CLI del proyecto:

```bash
uv run gatos
```

Si ejecutas ese comando sin argumentos, aparece un menú simple en terminal.

### Comandos de la CLI

Entrenar los modelos:

```bash
uv run gatos train
```

Abrir la aplicación web:

```bash
uv run gatos demo
```

Probar una imagen por consola:

```bash
uv run gatos predict ruta/de/la/imagen.jpg
```

También puedes indicar el modelo con nombres más fáciles:

```bash
uv run gatos predict ruta/de/la/imagen.jpg --model knn
uv run gatos predict ruta/de/la/imagen.jpg --model logistica
uv run gatos predict ruta/de/la/imagen.jpg --model lineal
```

Ver información del proyecto y del mejor modelo entrenado:

```bash
uv run gatos info
```

`gatos info` muestra:

- mejor modelo entrenado
- accuracy de cada modelo
- total de imágenes
- cantidad de imágenes por raza

Ordenar y renombrar las imágenes del dataset:

```bash
uv run gatos organize
```

## Dataset esperado

La carpeta `dataset/` debe tener esta estructura:

```text
dataset/
├── persa/
├── siames/
├── bengali/
├── sphynx/
└── maine_coon/
```

Cada carpeta debe contener imágenes de esa raza.

Cantidad recomendada:

- mínimo técnico: `2` imágenes por raza
- recomendado para una demo universitaria: `15 a 30` imágenes por raza
- sugerencia práctica para este proyecto: `20` imágenes por raza

Todas las imágenes se procesan automáticamente a `64x64` dentro del proyecto.

## Archivos importantes

- `main.py`: punto de entrada principal de la CLI.
- `INSTALACION.md`: guía de instalación en Linux y Windows.
- `PROBLEMAS_COMUNES.md`: soluciones rápidas a errores comunes.
- `src/common/data_utils.py`: carga y procesa imágenes.
- `src/train/train_service.py`: entrena y compara modelos.
- `src/predict/predict_service.py`: realiza predicciones.
- `src/interface/app.py`: abre la interfaz en Streamlit.

## Apoyo

Si vas a instalar el proyecto desde cero, empieza por [INSTALACION.md](./INSTALACION.md).

## Nota importante

La Regresión Lineal no es ideal para clasificación porque fue creada para predecir valores numéricos continuos, no categorías. Aquí se usa solo con fines académicos para compararla con modelos de clasificación.
