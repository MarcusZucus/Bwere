"""
Módulo de Motivación y Seguimiento de Werbly.
Proporciona el contexto necesario a la IA para que genere mensajes motivacionales adaptados al estado actual del usuario.

**Propósito**:
Este módulo actúa como puente entre los datos de progreso del usuario y la IA, asegurándose de que esta reciba toda la información relevante para generar mensajes únicos, personalizados y dinámicos en cada situación.

**Conexión con otros módulos**:
- **Entrada de datos:** Integra información de `user_data`, `analysis_engine` y Firestore (a través de `firebase_connection`).
- **Salida de contexto:** Proporciona un resumen estructurado al módulo `ai_core`, que luego utiliza la IA para crear mensajes motivacionales.
- **Uso en lógica central:** Sirve como enlace para convertir datos en contexto claro y comprensible para la IA, sin imponer limitaciones en las respuestas.
"""

from typing import Dict, Any
from modules.analysis_engine import analyze_user_data
from modules.firebase_connection import get_firestore_client


def prepare_motivation_context(user_id: str) -> Dict[str, Any]:
    """
    Genera un contexto estructurado basado en los datos del usuario y su progreso.
    Este contexto será enviado a la IA para que genere mensajes motivacionales personalizados.

    :param user_id: Identificador único del usuario.
    :return: Diccionario con contexto relevante para la motivación.
    """
    try:
        db = get_firestore_client()
        user_ref = db.collection("usuarios").document(user_id)
        user_data = user_ref.get().to_dict()

        if not user_data:
            raise ValueError(f"No se encontraron datos para el usuario {user_id}.")

        # Analizar datos del usuario
        analysis = analyze_user_data(user_data)

        # Obtener progreso desde Firestore
        progress_percentage = user_data.get("progress_percentage", 0)

        # Crear contexto estructurado
        context = {
            "progress_percentage": progress_percentage,
            "fatigue_level": analysis.get("fatigue_level", "unknown"),
            "bmi": analysis.get("bmi", None),
            "calories_goal": user_data.get("calories_goal", None),
            "calories_consumed": user_data.get("calories_consumed", None),
            "recent_achievements": user_data.get("recent_achievements", []),
            "long_term_goals": user_data.get("long_term_goals", "No definidos")
        }

        return context
    except Exception as e:
        raise RuntimeError(f"Error al preparar el contexto de motivación para el usuario {user_id}: {str(e)}")


def generate_motivational_message(user_id: str, ai_core) -> str:
    """
    Envía el contexto de motivación a la IA y obtiene un mensaje motivacional único.

    :param user_id: Identificador único del usuario.
    :param ai_core: Referencia al módulo `ai_core` para generar mensajes con la IA.
    :return: Mensaje motivacional generado por la IA.
    """
    try:
        # Preparar contexto
        context = prepare_motivation_context(user_id)

        # Crear prompt para la IA
        prompt = (
            "Eres un asistente motivacional avanzado. Genera un mensaje motivador para el usuario "
            "basado en el siguiente contexto:\n"
            f"{context}\n"
            "Tu mensaje debe ser motivador, personalizado y único, basado en el progreso y el estado del usuario."
        )

        # Generar mensaje usando la IA
        message = ai_core.query_model(prompt)
        return message
    except Exception as e:
        return f"Error al generar mensaje motivacional: {str(e)}"
