"""
Módulo de Suplementación de Bwere.
Identifica deficiencias y proporciona recomendaciones personalizadas de suplementos en función de los datos del usuario.

**Propósito**:
- Este módulo organiza dinámicamente los datos del usuario y delega a la IA la tarea de recomendar suplementos adaptados a las necesidades individuales.

**Conexión con otros módulos**:
- **Entrada de datos:** Recibe datos del usuario desde `user_data`, análisis desde `analysis_engine` y configuraciones desde Firestore.
- **Salida de contexto:** Proporciona un resumen estructurado al módulo `ai_core` para que la IA genere recomendaciones precisas.
"""
from typing import Dict, Any
from modules.firebase_connection import get_firestore_client
from modules.analysis_engine import prepare_analysis_context
from modules.ai_core import query_model


def prepare_supplement_context(user_id: str) -> Dict[str, Any]:
    """
    Genera un contexto dinámico basado en los datos del usuario y su análisis.

    :param user_id: Identificador único del usuario.
    :return: Diccionario con el contexto estructurado para recomendaciones de suplementos.
    """
    try:
        db = get_firestore_client()

        # Obtener datos del usuario desde Firestore
        user_ref = db.collection("usuarios").document(user_id)
        user_data = user_ref.get().to_dict()

        if not user_data:
            raise ValueError(f"No se encontraron datos para el usuario {user_id}.")

        # Incluir análisis dinámico desde analysis_engine
        analysis = prepare_analysis_context(user_id)

        # Combinar datos del usuario y análisis en un único contexto
        context = {**user_data, **analysis}

        # Incluir configuraciones relacionadas con suplementación (si están disponibles)
        supplement_config = db.collection("config").document("supplementation_guidelines").get().to_dict() or {}
        context["supplement_config"] = supplement_config

        return context
    except Exception as e:
        raise RuntimeError(f"Error al preparar el contexto de suplementación para el usuario {user_id}: {str(e)}")


def recommend_supplements_with_ai(user_id: str) -> str:
    """
    Envía el contexto dinámico a la IA para generar recomendaciones personalizadas de suplementos.

    :param user_id: Identificador único del usuario.
    :return: Respuesta de la IA con las recomendaciones de suplementos.
    """
    try:
        # Preparar contexto dinámico
        supplement_context = prepare_supplement_context(user_id)

        # Crear un prompt dinámico para la IA
        prompt = (
            "Eres un asistente especializado en suplementación. Basándote en los siguientes datos del usuario:\n"
            f"{supplement_context}\n"
            "Proporciona una lista personalizada de suplementos, incluyendo dosis, horarios y cualquier advertencia relevante. "
            "Asegúrate de que las recomendaciones sean seguras, basadas en las condiciones de salud y objetivos del usuario."
        )

        # Generar recomendaciones usando la IA
        recommendations = query_model(prompt)
        return recommendations
    except Exception as e:
        return f"Error al generar recomendaciones de suplementos: {str(e)}"
