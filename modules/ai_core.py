"""
Módulo Central de Interacciones con IA (ai_core).
Gestiona todas las interacciones con modelos de inteligencia artificial, 
incluyendo OpenAI, modelos entrenados localmente (como LLaMA) u otros backends.

**Propósito**:
- Centraliza todas las interacciones con IA para garantizar un flujo claro y consistente.
- Soporta múltiples backends de IA, adaptándose dinámicamente al modelo configurado.

**Conexión con otros módulos**:
- Es utilizado por módulos como `analysis_engine`, `motivation_tracker`, `nutrition_planner`, etc., 
  para enviar prompts y recibir respuestas de la IA.
"""

import os
import logging
from typing import Dict, Any, Optional
from tenacity import retry, stop_after_attempt, wait_exponential

# Configuración del sistema de logs
logging_level = os.getenv("LOGGING_LEVEL", "INFO").upper()
logging.basicConfig(level=logging_level, format="%(asctime)s - %(levelname)s - %(message)s")

# OpenAI (u otros proveedores externos de IA) importaciones
import openai
import requests

# Configuración global para el módulo
DEFAULT_BACKEND = os.getenv("AI_BACKEND", "openai")  # "openai", "llama", "custom"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LLAMA_API_ENDPOINT = os.getenv("LLAMA_API_ENDPOINT")  # Si usas un modelo local/servidor

class AICore:
    """
    Clase principal para gestionar todas las interacciones con IA.
    """

    def __init__(self):
        self.backend = DEFAULT_BACKEND
        self._validate_configuration()

    def _validate_configuration(self):
        """
        Valida que las configuraciones necesarias para el backend actual estén presentes.
        """
        if self.backend == "openai" and not OPENAI_API_KEY:
            raise ValueError("La clave API de OpenAI no está configurada.")
        elif self.backend == "llama" and not LLAMA_API_ENDPOINT:
            raise ValueError("El endpoint del modelo LLaMA no está configurado.")
        logging.info(f"Backend configurado correctamente: {self.backend}")

    def query_model(self, prompt: str, options: Optional[Dict[str, Any]] = None) -> str:
        """
        Envía un prompt al modelo configurado y devuelve la respuesta generada.

        :param prompt: Texto que se enviará al modelo de IA.
        :param options: Opciones adicionales específicas del backend (como temperatura, tokens, etc.).
        :return: Respuesta generada por la IA.
        """
        try:
            logging.info(f"Enviando prompt al backend {self.backend}: {prompt}")
            if self.backend == "openai":
                return self._query_openai(prompt, self._validate_options(options))
            elif self.backend == "llama":
                return self._query_llama(prompt, self._validate_options(options))
            else:
                raise ValueError(f"Backend de IA desconocido: {self.backend}")
        except Exception as e:
            logging.error(f"Error al procesar el prompt: {str(e)}")
            return f"Error al consultar el modelo {self.backend}: {str(e)}"

    def _validate_options(self, options: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Valida y completa las opciones proporcionadas con valores predeterminados.

        :param options: Opciones adicionales.
        :return: Opciones validadas y completadas.
        """
        default_options = {"temperature": 0.7, "max_tokens": 300, "model": "gpt-3.5-turbo"}
        return {**default_options, **(options or {})}

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def _query_openai(self, prompt: str, options: Dict[str, Any]) -> str:
        """
        Envía un prompt a OpenAI y devuelve la respuesta.

        :param prompt: Texto que se enviará a OpenAI.
        :param options: Opciones adicionales como temperatura, tokens, etc.
        :return: Respuesta generada por OpenAI.
        """
        try:
            openai.api_key = OPENAI_API_KEY
            response = openai.ChatCompletion.create(
                model=options["model"],
                messages=[{"role": "user", "content": prompt}],
                temperature=options["temperature"],
                max_tokens=options["max_tokens"]
            )
            message = response["choices"][0]["message"]["content"].strip()
            logging.info(f"Respuesta de OpenAI: {message}")
            return message
        except openai.error.OpenAIError as e:
            logging.error(f"Error de OpenAI: {str(e)}")
            return f"Error en OpenAI: {str(e)}"
        except (KeyError, IndexError) as e:
            logging.error(f"Respuesta de OpenAI en formato inesperado: {str(e)}")
            return "Error: La respuesta de OpenAI no tiene el formato esperado."

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def _query_llama(self, prompt: str, options: Dict[str, Any]) -> str:
        """
        Envía un prompt al modelo LLaMA (o modelo local) y devuelve la respuesta.

        :param prompt: Texto que se enviará al modelo LLaMA.
        :param options: Opciones adicionales específicas del modelo.
        :return: Respuesta generada por el modelo.
        """
        try:
            payload = {
                "prompt": prompt,
                "temperature": options["temperature"],
                "max_tokens": options["max_tokens"]
            }
            response = requests.post(LLAMA_API_ENDPOINT, json=payload)
            response.raise_for_status()
            generated_text = response.json().get("generated_text", "").strip()
            logging.info(f"Respuesta de LLaMA: {generated_text}")
            return generated_text
        except requests.exceptions.RequestException as e:
            logging.error(f"Error al consultar el modelo LLaMA: {str(e)}")
            return f"Error en LLaMA: {str(e)}"
        except KeyError as e:
            logging.error(f"Respuesta de LLaMA en formato inesperado: {str(e)}")
            return "Error: La respuesta de LLaMA no tiene el formato esperado."

    def get_available_backends(self) -> Dict[str, Any]:
        """
        Devuelve una lista de los backends disponibles y configurados.

        :return: Diccionario con los backends disponibles y su estado.
        """
        backends_status = {
            "openai": bool(OPENAI_API_KEY),
            "llama": bool(LLAMA_API_ENDPOINT)
        }
        logging.info(f"Backends disponibles: {backends_status}")
        return backends_status
