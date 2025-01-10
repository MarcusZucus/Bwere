"""
Módulo de Planificación Nutricional de Werbly.
Proporciona el contexto necesario para que la IA genere planes de alimentación personalizados y dinámicos.

**Propósito**:
Este módulo recopila y organiza toda la información relevante del usuario para que la IA pueda tomar decisiones informadas y generar planes personalizados sin restricciones predefinidas.

**Conexión con otros módulos**:
- **Entrada de datos:** Recibe información desde `user_data`, análisis desde `analysis_engine` y datos dinámicos desde Firestore.
- **Salida de contexto:** Proporciona un resumen estructurado al módulo `ai_core` para que la IA diseñe planes únicos.
"""
from typing import Dict, Any
from modules.analysis_engine import analyze_user_data
from modules.firebase_connection import get_firestore_client


def prepare_nutrition_context(user_id: str) -> Dict[str, Any]:
    """
    Genera un contexto estructurado basado en los datos del usuario y su análisis nutricional.
    Este contexto será enviado a la IA para que genere un plan de alimentación dinámico.

    :param user_id: Identificador único del usuario.
    :return: Diccionario con contexto relevante para la planificación nutricional.
    """
    try:
        db = get_firestore_client()
        user_ref = db.collection("usuarios").document(user_id)
        user_data = user_ref.get().to_dict()

        if not user_data:
            raise ValueError(f"No se encontraron datos para el usuario {user_id}.")

        # Analizar datos del usuario
        analysis = analyze_user_data(user_data)

        # Recuperar preferencias, restricciones y datos adicionales
        dietary_preferences = user_data.get("dietary_preferences", [])
        dietary_restrictions = user_data.get("dietary_restrictions", [])
        previous_plans = user_data.get("previous_plans", [])
        local_availability = user_data.get("local_availability", "unknown")

        # Crear contexto estructurado con datos ampliados
        context = {
            "recommended_calories": analysis.get("recommended_calories", 2000),
            "needs_more_protein": analysis.get("needs_more_protein", False),
            "dietary_preferences": dietary_preferences,
            "dietary_restrictions": dietary_restrictions,
            "previous_plans": previous_plans,
            "long_term_goals": user_data.get("long_term_goals", "No definidos"),
            "recent_achievements": user_data.get("recent_achievements", []),
            "current_weight": user_data.get("weight", None),
            "height": user_data.get("height", None),
            "activity_level": user_data.get("activity_level", "unknown"),
            "local_availability": local_availability
        }

        return context
    except Exception as e:
        raise RuntimeError(f"Error al preparar el contexto nutricional para el usuario {user_id}: {str(e)}")


def generate_nutrition_plan_with_ai(user_id: str, ai_core) -> str:
    """
    Envía el contexto nutricional a la IA y obtiene un plan de alimentación dinámico.

    :param user_id: Identificador único del usuario.
    :param ai_core: Referencia al módulo `ai_core` para generar planes con la IA.
    :return: Plan de alimentación generado por la IA.
    """
    try:
        # Preparar contexto
        context = prepare_nutrition_context(user_id)

        # Crear prompt dinámico para la IA
        prompt = (
            "Eres un asistente nutricional avanzado. Tu objetivo es generar un plan de alimentación completamente "
            "personalizado basado en el siguiente contexto:\n"
            f"{context}\n"
            "Si necesitas más información para generar el plan, indica qué datos faltan."
        )

        # Generar plan usando la IA
        response = ai_core.query_model(prompt)
        return response
    except Exception as e:
        return f"Error al generar el plan nutricional con IA: {str(e)}"
