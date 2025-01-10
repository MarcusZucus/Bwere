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
from typing import Dict, Any, Optional

# OpenAI (u otros proveedores externos de IA) importaciones
import openai

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

    def query_model(self, prompt: str, options: Optional[Dict[str, Any]] = None) -> str:
        """
        Envia un prompt al modelo configurado y devuelve la respuesta generada.

        :param prompt: Texto que se enviará al modelo de IA.
        :param options: Opciones adicionales específicas del backend (como temperatura, tokens, etc.).
        :return: Respuesta generada por la IA.
        """
        if self.backend == "openai":
            return self._query_openai(prompt, options)
        elif self.backend == "llama":
            return self._query_llama(prompt, options)
        else:
            raise ValueError(f"Backend de IA desconocido: {self.backend}")

    def _query_openai(self, prompt: str, options: Optional[Dict[str, Any]] = None) -> str:
        """
        Envía un prompt a OpenAI y devuelve la respuesta.

        :param prompt: Texto que se enviará a OpenAI.
        :param options: Opciones adicionales como temperatura, tokens, etc.
        :return: Respuesta generada por OpenAI.
        """
        try:
            openai.api_key = OPENAI_API_KEY
            response = openai.ChatCompletion.create(
                model=options.get("model", "gpt-3.5-turbo"),
                messages=[{"role": "user", "content": prompt}],
                temperature=options.get("temperature", 0.7),
                max_tokens=options.get("max_tokens", 300)
            )
            return response["choices"][0]["message"]["content"].strip()
        except Exception as e:
            return f"Error al consultar OpenAI: {str(e)}"

    def _query_llama(self, prompt: str, options: Optional[Dict[str, Any]] = None) -> str:
        """
        Envía un prompt al modelo LLaMA (o modelo local) y devuelve la respuesta.

        :param prompt: Texto que se enviará al modelo LLaMA.
        :param options: Opciones adicionales específicas del modelo.
        :return: Respuesta generada por el modelo.
        """
        try:
            import requests  # Solo se usa para LLaMA/locales
            payload = {
                "prompt": prompt,
                "temperature": options.get("temperature", 0.7),
                "max_tokens": options.get("max_tokens", 300)
            }
            response = requests.post(LLAMA_API_ENDPOINT, json=payload)
            response.raise_for_status()
            return response.json().get("generated_text", "").strip()
        except Exception as e:
            return f"Error al consultar el modelo LLaMA: {str(e)}"

    def get_available_backends(self) -> Dict[str, Any]:
        """
        Devuelve una lista de los backends disponibles y configurados.

        :return: Diccionario con los backends disponibles y su estado.
        """
        return {
            "openai": bool(OPENAI_API_KEY),
            "llama": bool(LLAMA_API_ENDPOINT)
        }
