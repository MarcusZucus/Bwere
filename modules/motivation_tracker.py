"""
Módulo de Motivación y Seguimiento de Werbly.
Proporciona el contexto necesario a la IA para que genere mensajes motivacionales adaptados al estado actual del usuario.

**Propósito**:
Este módulo recopila y organiza datos dinámicamente para que la IA genere mensajes motivacionales únicos y personalizados en cada situación, sin imponer limitaciones ni reglas predefinidas.

**Conexión con otros módulos**:
- **Entrada de datos:** Integra información de `user_data`, `analysis_engine` y Firestore.
- **Salida de contexto:** Proporciona un resumen dinámico al módulo `ai_core`.
"""
from typing import Dict, Any
from modules.firebase_connection import get_firestore_client
from modules.analysis_engine import prepare_analysis_context
from modules.ai_core import query_model


def prepare_motivation_context(user_id: str) -> Dict[str, Any]:
    """
    Genera un contexto dinámico basado en todos los datos disponibles del usuario.

    :param user_id: Identificador único del usuario.
    :return: Diccionario con el contexto dinámico para la motivación.
    """
    try:
        # Conexión con Firestore para obtener datos del usuario
        db = get_firestore_client()
        user_ref = db.collection("usuarios").document(user_id)
        user_data = user_ref.get().to_dict()

        if not user_data:
            raise ValueError(f"No se encontraron datos para el usuario {user_id}.")

        # Incorporar análisis dinámico desde analysis_engine
        analysis = prepare_analysis_context(user_id)

        # Combinar datos del usuario y análisis dinámico en un único contexto
        context = {**user_data, **analysis}

        # Agregar datos adicionales si están disponibles
        context["recent_achievements"] = user_data.get("recent_achievements", [])
        context["long_term_goals"] = user_data.get("long_term_goals", "No definidos")

        return context
    except Exception as e:
        raise RuntimeError(f"Error al preparar el contexto de motivación para el usuario {user_id}: {str(e)}")


def generate_motivational_message(user_id: str) -> str:
    """
    Envía el contexto dinámico de motivación a la IA y obtiene un mensaje motivacional único.

    :param user_id: Identificador único del usuario.
    :return: Mensaje motivacional generado por la IA.
    """
    try:
        # Preparar contexto dinámico
        context = prepare_motivation_context(user_id)

        # Crear un prompt dinámico basado en el estado del usuario
        prompt = (
            "Eres un asistente motivacional avanzado. Con base en los siguientes datos del usuario:\n"
            f"{context}\n"
            "Por favor, genera un mensaje motivador que sea único, personalizado y adaptado a su progreso, logros y metas."
        )

        # Generar mensaje usando la IA
        message = query_model(prompt)
        return message
    except Exception as e:
        return f"Error al generar mensaje motivacional: {str(e)}"
