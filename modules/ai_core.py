'''
Módulo Central de Interacciones con IA (ai_core).
Gestiona todas las interacciones con modelos de inteligencia artificial, 
incluyendo OpenAI, modelos entrenados localmente (como LLaMA) u otros backends.

**Propósito**:
- Centraliza todas las interacciones con IA para garantizar un flujo claro y consistente.
- Soporta múltiples backends de IA, adaptándose dinámicamente al modelo configurado.

**Conexión con otros módulos**:
- Es utilizado por módulos como `analysis_engine`, `motivation_tracker`, `nutrition_planner`, etc., 
  para enviar prompts y recibir respuestas de la IA.
'''

import os
import logging
import time
from typing import Dict, Any, Optional
from tenacity import retry, stop_after_attempt, wait_exponential
import openai
import requests

# Configuración del sistema de logs
logging_level = os.getenv("LOGGING_LEVEL", "INFO").upper()
logging.basicConfig(level=logging_level, format="%(asctime)s - %(levelname)s - %(message)s")

# Configuración global para el módulo
DEFAULT_BACKEND = os.getenv("AI_BACKEND", "openai")  # "openai", "llama", "custom"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LLAMA_API_ENDPOINT = os.getenv("LLAMA_API_ENDPOINT")  # Si usas un modelo local/servidor
LLAMA_TIMEOUT = int(os.getenv("LLAMA_TIMEOUT", 10))

class AICore:
    """
    Clase principal para gestionar todas las interacciones con IA.
    """

    def __init__(self):
        self.backend = DEFAULT_BACKEND
        self.custom_backends = {}
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
        self._validate_prompt(prompt)
        start_time = time.time()
        try:
            logging.info(f"Enviando prompt al backend {self.backend}: {prompt}")
            if self.backend == "openai":
                response = self._query_openai(prompt, self._validate_options(options))
            elif self.backend == "llama":
                response = self._query_llama(prompt, self._validate_options(options))
            elif self.backend in self.custom_backends:
                response = self.custom_backends[self.backend](prompt, options)
            else:
                raise ValueError(f"Backend de IA desconocido: {self.backend}")
            elapsed_time = time.time() - start_time
            logging.info(f"Consulta completada en {elapsed_time:.2f} segundos.")
            return response
        except Exception as e:
            logging.error(f"Error al procesar el prompt: {str(e)}")
            return f"Error al consultar el modelo {self.backend}: {str(e)}"

    def _validate_prompt(self, prompt: str):
        """
        Valida que el prompt sea válido.

        :param prompt: Texto que se enviará al modelo.
        """
        if not prompt or not isinstance(prompt, str) or len(prompt) > 5000:
            raise ValueError("El prompt no es válido: debe ser un string no vacío y de menos de 5000 caracteres.")

    def _validate_options(self, options: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Valida y completa las opciones proporcionadas con valores predeterminados.

        :param options: Opciones adicionales.
        :return: Opciones validadas y completadas.
        """
        default_options = {"temperature": 0.7, "max_tokens": 300, "model": "gpt-3.5-turbo"}
        return {**default_options, **(options or {})}

    def _validate_response(self, response: dict, backend: str, key: str = "generated_text") -> str:
        """
        Valida que la respuesta tenga el formato esperado.

        :param response: Respuesta del modelo de IA.
        :param backend: Nombre del backend que generó la respuesta.
        :param key: Clave esperada en la respuesta.
        :return: Texto generado por la IA.
        """
        if not response or key not in response:
            raise ValueError(f"Formato de respuesta inesperado del backend {backend}")
        return response[key].strip()

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
            return self._validate_response(response["choices"][0]["message"], "openai", "content")
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
            response = requests.post(LLAMA_API_ENDPOINT, json=payload, timeout=LLAMA_TIMEOUT)
            response.raise_for_status()
            return self._validate_response(response.json(), "llama")
        except requests.exceptions.RequestException as e:
            logging.error(f"Error al consultar el modelo LLaMA: {str(e)}")
            return f"Error en LLaMA: {str(e)}"

    def register_backend(self, name: str, handler: callable):
        """
        Registra un nuevo backend personalizado.

        :param name: Nombre del backend.
        :param handler: Función que maneja las consultas para este backend.
        """
        self.custom_backends[name] = handler
        logging.info(f"Backend personalizado registrado: {name}")

    def get_available_backends(self) -> Dict[str, Any]:
        """
        Devuelve una lista de los backends disponibles y configurados.

        :return: Diccionario con los backends disponibles y su estado.
        """
        backends_status = {
            "openai": bool(OPENAI_API_KEY),
            "llama": bool(LLAMA_API_ENDPOINT),
            **{name: True for name in self.custom_backends}
        }
        logging.info(f"Backends disponibles: {backends_status}")
        return backends_status

    def test_backend(self, backend: str) -> bool:
        """
        Prueba la disponibilidad de un backend.

        :param backend: Nombre del backend a probar.
        :return: True si el backend está disponible, False en caso contrario.
        """
        try:
            if backend == "openai":
                return bool(OPENAI_API_KEY)
            elif backend == "llama":
                response = requests.get(LLAMA_API_ENDPOINT, timeout=5)
                return response.status_code == 200
            elif backend in self.custom_backends:
                return True  # Los backends personalizados se consideran disponibles por definición
            return False
        except Exception as e:
            logging.error(f"Error al probar el backend {backend}: {str(e)}")
            return False
