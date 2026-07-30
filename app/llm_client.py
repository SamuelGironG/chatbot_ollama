"""Cliente HTTP aislado para la API de generación de Ollama."""

from dataclasses import dataclass
from time import perf_counter

import requests


OLLAMA_GENERATE_URL = "http://localhost:11434/api/generate"


class OllamaClientError(RuntimeError):
    """Error controlado durante una petición a Ollama."""


@dataclass(frozen=True)
class GenerationResult:
    text: str
    elapsed_seconds: float


class OllamaClient:
    """Envía prompts a Ollama sin conocer detalles de la interfaz gráfica."""

    def __init__(self, endpoint: str = OLLAMA_GENERATE_URL, timeout: float = 120.0) -> None:
        self._endpoint = endpoint
        self._timeout = timeout

    def generate(self, model: str, prompt: str) -> GenerationResult:
        started_at = perf_counter()
        try:
            response = requests.post(
                self._endpoint,
                json={"model": model, "prompt": prompt, "stream": False},
                timeout=self._timeout,
            )
            response.raise_for_status()
            payload = response.json()
        except requests.RequestException as error:
            raise OllamaClientError(f"No fue posible conectar con Ollama: {error}") from error
        except ValueError as error:
            raise OllamaClientError("Ollama devolvió JSON no válido.") from error

        if not isinstance(payload, dict) or not isinstance(payload.get("response"), str):
            raise OllamaClientError("Ollama devolvió una respuesta inesperada.")

        return GenerationResult(
            text=payload["response"].strip(),
            elapsed_seconds=perf_counter() - started_at,
        )
