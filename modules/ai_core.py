import requests
from google.cloud import secretmanager
from typing import Dict, Any

# Configuración para el modelo actual
MODEL_BACKEND = "llama2"  # Opciones: "llama2", "openai"

# URLs para interactuar con los modelos
ENDPOINTS = {
    "llama2": "http://localhost:8000/api/v1/query",  # Servidor local para LLaMA 2
    "openai": "https://api.openai.com/v1/completions"
}


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
        raise RuntimeError(f"Error al obtener el secreto {secret_name}: {str(e)}")


def query_model(prompt: str, options: Dict[str, Any] = None) -> str:
    """
    Interactúa con el modelo configurado y devuelve la respuesta generada.
    
    :param prompt: El texto o instrucción a enviar al modelo.
    :param options: Opciones adicionales para personalizar la solicitud.
    :return: La respuesta generada por el modelo.
    """
    options = options or {}
    
    if MODEL_BACKEND == "llama2":
        return _query_llama2(prompt, options)
    elif MODEL_BACKEND == "openai":
        return _query_openai(prompt, options)
    else:
        raise ValueError(f"Modelo backend no soportado: {MODEL_BACKEND}")


def _query_llama2(prompt: str, options: Dict[str, Any]) -> str:
    """
    Consulta el modelo LLaMA 2 a través de su API REST.
    
    :param prompt: El texto o instrucción a enviar.
    :param options: Opciones adicionales para la consulta.
    :return: Respuesta generada por LLaMA 2.
    """
    try:
        api_key = get_secret("llama2-api-key")  # Nombre del secreto en Google Secret Manager
        payload = {"prompt": prompt, **options}
        headers = {"Authorization": f"Bearer {api_key}"}
        response = requests.post(ENDPOINTS["llama2"], json=payload, headers=headers)
        response.raise_for_status()
        return response.json().get("response", "Sin respuesta.")
    except requests.RequestException as e:
        return f"Error al consultar LLaMA 2: {str(e)}"


def _query_openai(prompt: str, options: Dict[str, Any]) -> str:
    """
    Consulta el modelo OpenAI GPT a través de su API.
    
    :param prompt: El texto o instrucción a enviar.
    :param options: Opciones adicionales para la consulta.
    :return: Respuesta generada por OpenAI GPT.
    """
    try:
        api_key = get_secret("openai-api-key")  # Nombre del secreto en Google Secret Manager
        headers = {"Authorization": f"Bearer {api_key}"}
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": prompt}],
            **options
        }
        response = requests.post(ENDPOINTS["openai"], json=payload, headers=headers)
        response.raise_for_status()
        return response.json().get("choices", [{}])[0].get("message", {}).get("content", "Sin respuesta.")
    except requests.RequestException as e:
        return f"Error al consultar OpenAI GPT: {str(e)}"
