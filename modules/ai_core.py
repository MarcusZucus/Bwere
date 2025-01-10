"""
Módulo Central de IA para Werbly.
Proporciona una interfaz flexible y extensible para interactuar con diferentes modelos de IA (LLaMA 2, OpenAI, etc.).

**Propósito**:
- Generalizar la interacción con modelos de IA.
- Facilitar la incorporación de nuevos modelos sin modificar la lógica principal.
- Asegurar que las solicitudes sean seguras y adaptables.

**Conexión con otros módulos**:
- Se utiliza como núcleo en todos los módulos que necesitan interactuar con modelos de IA.
"""

import requests
import logging
from google.cloud import secretmanager
from typing import Dict, Any

# Configuración para el modelo actual
MODEL_BACKEND = "llama2"  # Opciones: "llama2", "openai"

# URLs para interactuar con los modelos
ENDPOINTS = {
    "llama2": "http://localhost:8000/api/v1/query",  # Servidor local para LLaMA 2
    "openai": "https://api.openai.com/v1/completions"
}

# Configuración de formatos específicos por modelo
MODEL_CONFIG = {
    "llama2": {
        "headers": {"Content-Type": "application/json"},
        "format_request": lambda prompt, options: {"prompt": prompt, **options}
    },
    "openai": {
        "headers": lambda api_key: {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        "format_request": lambda prompt, options: {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": prompt}],
            **options
        }
    }
}

# Configuración de logs
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def get_secret(secret_name: str) -> str:
    """
    Recupera un secreto almacenado en Google Secret Manager.

    :param secret_name: Nombre del secreto a recuperar.
    :return: Valor del secreto.
    """
    try:
        client = secretmanager.SecretManagerServiceClient()
        project_id = "tu-id-de-proyecto"  # Reemplaza con el ID de tu proyecto
        name = f"projects/{project_id}/secrets/{secret_name}/versions/latest"
        response = client.access_secret_version(request={"name": name})
        return response.payload.data.decode("UTF-8")
    except Exception as e:
        logging.error(f"Error al obtener el secreto {secret_name}: {str(e)}")
        raise RuntimeError(f"No se pudo obtener el secreto {secret_name}.")


def query_model(prompt: str, options: Dict[str, Any] = None) -> str:
    """
    Interactúa con el modelo configurado y devuelve la respuesta generada.

    :param prompt: El texto o instrucción a enviar al modelo.
    :param options: Opciones adicionales para personalizar la solicitud.
    :return: La respuesta generada por el modelo.
    """
    options = options or {}
    backend_config = MODEL_CONFIG.get(MODEL_BACKEND)
    if not backend_config:
        raise ValueError(f"Modelo backend no soportado: {MODEL_BACKEND}")

    try:
        # Configurar endpoint y encabezados
        endpoint = ENDPOINTS[MODEL_BACKEND]
        api_key = get_secret(f"{MODEL_BACKEND}_api_key") if MODEL_BACKEND == "openai" else None
        headers = backend_config["headers"](api_key) if callable(backend_config["headers"]) else backend_config["headers"]

        # Formatear solicitud
        request_payload = backend_config["format_request"](prompt, options)
        logging.info(f"Solicitud enviada al modelo {MODEL_BACKEND}: {request_payload}")

        # Enviar solicitud con reintentos
        for attempt in range(3):
            try:
                response = requests.post(endpoint, json=request_payload, headers=headers, timeout=10)
                response.raise_for_status()
                break
            except requests.exceptions.RequestException as e:
                logging.warning(f"Error en el intento {attempt + 1} para el modelo {MODEL_BACKEND}: {str(e)}")
                if attempt == 2:  # Último intento fallido
                    raise RuntimeError(f"No se pudo obtener respuesta del modelo {MODEL_BACKEND} tras 3 intentos.")

        # Procesar respuesta
        response_json = response.json()
        logging.info(f"Respuesta recibida del modelo {MODEL_BACKEND}: {response_json}")

        return (
            response_json.get("choices", [{}])[0].get("text", "").strip()
            if MODEL_BACKEND == "openai"
            else response_json.get("response", "")
        )
    except Exception as e:
        logging.error(f"Error al consultar el modelo {MODEL_BACKEND}: {str(e)}")
        return f"Error: {str(e)}"


# Función asíncrona (opcional para flujos concurrentes)
async def async_query_model(prompt: str, options: Dict[str, Any] = None) -> str:
    """
    Interactúa de manera asíncrona con el modelo configurado.

    :param prompt: El texto o instrucción a enviar al modelo.
    :param options: Opciones adicionales para personalizar la solicitud.
    :return: La respuesta generada por el modelo.
    """
    import aiohttp
    options = options or {}
    backend_config = MODEL_CONFIG.get(MODEL_BACKEND)
    if not backend_config:
        raise ValueError(f"Modelo backend no soportado: {MODEL_BACKEND}")

    try:
        endpoint = ENDPOINTS[MODEL_BACKEND]
        api_key = get_secret(f"{MODEL_BACKEND}_api_key") if MODEL_BACKEND == "openai" else None
        headers = backend_config["headers"](api_key) if callable(backend_config["headers"]) else backend_config["headers"]
        request_payload = backend_config["format_request"](prompt, options)

        async with aiohttp.ClientSession() as session:
            for attempt in range(3):
                try:
                    async with session.post(endpoint, json=request_payload, headers=headers) as response:
                        response.raise_for_status()
                        response_json = await response.json()
                        logging.info(f"Respuesta recibida (async) del modelo {MODEL_BACKEND}: {response_json}")
                        return (
                            response_json.get("choices", [{}])[0].get("text", "").strip()
                            if MODEL_BACKEND == "openai"
                            else response_json.get("response", "")
                        )
                except aiohttp.ClientError as e:
                    logging.warning(f"Error en intento {attempt + 1} (async) para el modelo {MODEL_BACKEND}: {str(e)}")
                    if attempt == 2:
                        raise RuntimeError(f"No se pudo obtener respuesta del modelo {MODEL_BACKEND} tras 3 intentos (async).")
    except Exception as e:
        logging.error(f"Error (async) al consultar el modelo {MODEL_BACKEND}: {str(e)}")
        return f"Error: {str(e)}"
