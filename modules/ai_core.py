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
- Integra `backend_manager` para gestionar backends personalizados dinámicamente.
'''

import os
import logging
import time
import uuid
from typing import Dict, Any, Optional
from tenacity import retry, stop_after_attempt, wait_exponential
import openai
import requests
from backend_manager import BackendManager

# Configuración del sistema de logs
logging_level = os.getenv("LOGGING_LEVEL", "INFO").upper()
logging.basicConfig(level=logging_level, format="%(asctime)s - %(levelname)s - %(message)s")

# Configuración global para el módulo
DEFAULT_BACKEND = os.getenv("AI_BACKEND", "openai")  # "openai", "llama", "custom"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LLAMA_API_ENDPOINT = os.getenv("LLAMA_API_ENDPOINT")  # Si usas un modelo local/servidor
LLAMA_TIMEOUT = int(os.getenv("LLAMA_TIMEOUT", 10))
RETRY_ATTEMPTS = int(os.getenv("RETRY_ATTEMPTS", 3))
WAIT_MULTIPLIER = float(os.getenv("WAIT_MULTIPLIER", 1.0))

class AICore:
    """
    Clase principal para gestionar todas las interacciones con IA.
    """

    def __init__(self):
        self.backend = DEFAULT_BACKEND
        self.backend_manager = BackendManager()
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
        query_id = uuid.uuid4()
        self._validate_prompt(prompt)
        start_time = time.time()
        try:
            logging.info(f"[{query_id}] Enviando prompt al backend {self.backend}: {prompt}")
            if self.backend == "openai":
                response = self._query_openai(prompt, self._validate_options(options, "openai"))
            elif self.backend == "llama":
                response = self._query_llama(prompt, self._validate_options(options, "llama"))
            elif self.backend in self.backend_manager.list_backends():
                response = self.backend_manager.query_backend(self.backend, prompt, options)
            else:
                raise ValueError(f"[{query_id}] Backend de IA desconocido: {self.backend}")
            elapsed_time = time.time() - start_time
            self.log_performance(self.backend, elapsed_time)
            return response
        except Exception as e:
            self.log_error(self.backend, e)
            return f"Error al consultar el modelo {self.backend}: {str(e)}"
    def _validate_prompt(self, prompt: str):
        """
        Valida que el prompt sea válido.

        :param prompt: Texto que se enviará al modelo.
        """
        if not prompt or not isinstance(prompt, str) or len(prompt) > 5000:
            raise ValueError("El prompt no es válido: debe ser un string no vacío y de menos de 5000 caracteres.")

    def _validate_options(self, options: Optional[Dict[str, Any]], backend: str) -> Dict[str, Any]:
        """
        Valida y completa las opciones proporcionadas con valores predeterminados específicos del backend.

        :param options: Opciones adicionales.
        :param backend: Nombre del backend para el cual se validan las opciones.
        :return: Opciones validadas y completadas.
        """
        default_options = {
            "openai": {"temperature": 0.7, "max_tokens": 300, "model": "gpt-3.5-turbo"},
            "llama": {"temperature": 0.7, "max_tokens": 300}
        }
        return {**default_options.get(backend, {}), **(options or {})}

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

    @retry(stop=stop_after_attempt(RETRY_ATTEMPTS), wait=wait_exponential(multiplier=WAIT_MULTIPLIER, min=4, max=10))
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

    @retry(stop=stop_after_attempt(RETRY_ATTEMPTS), wait=wait_exponential(multiplier=WAIT_MULTIPLIER, min=4, max=10))
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
        self.backend_manager.register_backend(name, handler)
        logging.info(f"Backend personalizado registrado: {name}")

    def remove_backend(self, name: str):
        """
        Elimina un backend personalizado registrado.

        :param name: Nombre del backend a eliminar.
        """
        self.backend_manager.remove_backend(name)
        logging.info(f"Backend personalizado eliminado: {name}")

    def get_available_backends(self) -> Dict[str, Any]:
        """
        Devuelve una lista de los backends disponibles y configurados.

        :return: Diccionario con los backends disponibles y su estado.
        """
        backends_status = {
            "openai": bool(OPENAI_API_KEY),
            "llama": bool(LLAMA_API_ENDPOINT),
            **{name: True for name in self.backend_manager.list_backends()}
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
            elif backend in self.backend_manager.list_backends():
                return self.backend_manager.test_backend(backend)
            return False
        except Exception as e:
            logging.error(f"Error al probar el backend {backend}: {str(e)}")
            return False

    def test_all_backends(self) -> Dict[str, bool]:
        """
        Prueba la disponibilidad de todos los backends configurados.

        :return: Diccionario con el estado de cada backend (True si está disponible, False si no lo está).
        """
        results = {}
        for backend in ["openai", "llama", *self.backend_manager.list_backends()]:
            results[backend] = self.test_backend(backend)
        logging.info(f"Resultados de las pruebas de backends: {results}")
        return results

    def log_performance(self, backend: str, elapsed_time: float):
        """
        Registra el tiempo de ejecución de una consulta al backend.

        :param backend: Nombre del backend utilizado.
        :param elapsed_time: Tiempo transcurrido en segundos.
        """
        logging.info(f"Tiempo de ejecución para el backend '{backend}': {elapsed_time:.2f} segundos.")

    def log_error(self, backend: str, error: Exception):
        """
        Registra un error asociado a un backend específico.

        :param backend: Nombre del backend en el que ocurrió el error.
        :param error: Objeto de la excepción capturada.
        """
        logging.error(f"Error en el backend '{backend}': {str(error)}")

    def integration_test(self) -> Dict[str, Any]:
        """
        Realiza una prueba de integración para todos los backends configurados
        enviando un prompt genérico y verificando la respuesta.

        :return: Diccionario con los resultados de la prueba para cada backend.
        """
        prompt = "Este es un prompt de prueba para la integración del backend."
        results = {}
        for backend in ["openai", "llama", *self.backend_manager.list_backends()]:
            try:
                logging.info(f"Realizando prueba de integración para el backend: {backend}")
                self.backend = backend  # Cambiar dinámicamente el backend
                results[backend] = self.query_model(prompt, options={})
            except Exception as e:
                results[backend] = f"Error: {str(e)}"
                self.log_error(backend, e)
        return results
