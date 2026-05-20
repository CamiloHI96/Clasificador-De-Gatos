# Instalación

![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![UV](https://img.shields.io/badge/UV-instalaci%C3%B3n-green)
![Linux](https://img.shields.io/badge/Linux-compatible-success)
![Windows](https://img.shields.io/badge/Windows-compatible-success)

## Navegación

- [Proyecto](./README.md)
- [Problemas comunes](./PROBLEMAS_COMUNES.md)

## Contenido

- [Resumen](#resumen)
- [Objetivo](#objetivo)
- [Requisitos previos](#requisitos-previos)
- [Instalación de UV](#instalación-de-uv)
- [Instalación principal con pyprojecttoml](#instalación-principal-con-pyprojecttoml)
- [Instalación alternativa con requirementstxt](#instalación-alternativa-con-requirementstxt)
- [Compatibilidad](#compatibilidad)
- [Apoyo](#apoyo)

## Resumen

Este archivo explica cómo preparar el entorno del proyecto en Linux y Windows.

## Objetivo

Dejar el proyecto listo para usar la CLI, entrenar modelos y abrir la demo web.

## Requisitos previos

Antes de ejecutar el proyecto, la computadora debe tener instalado:

- Python 3.11 o superior
- UV

Sin `uv` no funcionarán comandos como:

- `uv sync`
- `uv run gatos`

## Instalación de UV

En Linux o macOS:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

En Windows PowerShell:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Verificar instalación:

```bash
uv --version
```

## Instalación principal con pyproject.toml

Esta es la forma recomendada.

### Linux o macOS

```bash
uv venv
source .venv/bin/activate
uv sync
uv run gatos
```

### Windows PowerShell

```powershell
uv venv
.venv\Scripts\Activate.ps1
uv sync
uv run gatos
```

### Windows CMD

```bat
uv venv
.venv\Scripts\activate.bat
uv sync
uv run gatos
```

Comando principal para iniciar el proyecto:

```bash
uv run gatos
```

## Instalación alternativa con requirements.txt

### Linux o macOS

```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
uv run gatos
```

### Windows PowerShell

```powershell
uv venv
.venv\Scripts\Activate.ps1
uv pip install -r requirements.txt
uv run gatos
```

### Windows CMD

```bat
uv venv
.venv\Scripts\activate.bat
uv pip install -r requirements.txt
uv run gatos
```

## Compatibilidad

El proyecto funciona igual en Linux y Windows.

Lo que cambia normalmente es:

- la activación del entorno virtual
- la forma de escribir algunas rutas en la terminal

Los comandos de la CLI son los mismos en ambos sistemas:

- `uv run gatos`
- `uv run gatos train`
- `uv run gatos predict ruta/de/la/imagen.jpg`
- `uv run gatos info`
- `uv run gatos demo`
- `uv run gatos organize`

## Apoyo

Si aparece un error durante la instalación, revisa [PROBLEMAS_COMUNES.md](./PROBLEMAS_COMUNES.md).
