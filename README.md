# Chat para Ollama con Tkinter

Aplicación de escritorio para conversar con modelos Ollama locales. Usa Tkinter, incluido con Python, y `requests` como única dependencia externa.

## Requisitos

- Python 3.10 o superior.
- Ollama instalado y ejecutándose localmente.
- Uno o más de estos modelos: `gemma2:2b`, `llama3.2:3b`, `llama3.1:8b`.

## Instalación

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Preparar Ollama

```powershell
ollama pull gemma2:2b
ollama pull llama3.2:3b
ollama pull llama3.1:8b
ollama serve
```

Ollama atiende por defecto en `http://localhost:11434`.

## Ejecutar

```powershell
python main.py
```

Elige un modelo, escribe el mensaje y pulsa **Enviar** o `Enter`. La aplicación conserva el contexto del chat durante la sesión, muestra el tiempo total de cada respuesta y permite borrar el historial.

## Estructura

```text
.
├── app/
│   ├── __init__.py
│   ├── llm_client.py
│   └── ui.py
├── main.py
├── requirements.txt
└── README.md
```
clonar repositorio
