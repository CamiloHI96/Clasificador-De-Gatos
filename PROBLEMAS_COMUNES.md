# Problemas comunes

![Soporte](https://img.shields.io/badge/Soporte-b%C3%A1sico-blue)
![UV](https://img.shields.io/badge/UV-errores-green)
![Python](https://img.shields.io/badge/Python-entorno-orange)
![Streamlit](https://img.shields.io/badge/Streamlit-demo-red)

## Navegación

- [Proyecto](./README.md)
- [Instalación](./INSTALACION.md)

## Contenido

- [`uv: command not found`](#uv-command-not-found)
- [`python` o `python3` no existe](#python-o-python3-no-existe)
- [No se puede activar el entorno en Windows PowerShell](#no-se-puede-activar-el-entorno-en-windows-powershell)
- [No hay modelos entrenados](#no-hay-modelos-entrenados)
- [No se encontraron imágenes válidas](#no-se-encontraron-imágenes-válidas)
- [El dataset tiene nombres desordenados](#el-dataset-tiene-nombres-desordenados)
- [Streamlit no abre](#streamlit-no-abre)
- [Apoyo](#apoyo)

## Resumen

Este archivo reúne errores frecuentes y soluciones rápidas para ejecutar el proyecto.

## Objetivo

Resolver fallos comunes de instalación, entrenamiento y ejecución sin cambiar el código del proyecto.

## `uv: command not found`

Significa que `uv` no está instalado o no quedó disponible en la terminal.

Solución:

1. Instalar `uv`.
2. Cerrar y abrir la terminal.
3. Comprobar con:

```bash
uv --version
```

## `python` o `python3` no existe

Significa que Python no está instalado o no está agregado al sistema.

Solución:

1. Instalar Python 3.11 o superior.
2. Verificar con:

```bash
python --version
```

o

```bash
python3 --version
```

## No se puede activar el entorno en Windows PowerShell

A veces PowerShell bloquea la activación.

Prueba este comando:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Luego intenta otra vez:

```powershell
.venv\Scripts\Activate.ps1
```

## No hay modelos entrenados

Si sale un error de que no hay modelos, primero debes entrenar:

```bash
uv run gatos train
```

## No se encontraron imágenes válidas

Eso significa que faltan imágenes en `dataset/` o que no tienen extensiones válidas.

Extensiones aceptadas:

- `.jpg`
- `.jpeg`
- `.png`
- `.bmp`

## El dataset tiene nombres desordenados

Puedes ordenar los nombres con:

```bash
uv run gatos organize
```

## Streamlit no abre

Primero revisa que las dependencias estén instaladas:

```bash
uv sync
```

Luego ejecuta:

```bash
uv run gatos demo
```

## Apoyo

Si necesitas repasar la instalación completa, revisa [INSTALACION.md](./INSTALACION.md).

Si necesitas ver los comandos principales del proyecto, revisa [README.md](./README.md).
