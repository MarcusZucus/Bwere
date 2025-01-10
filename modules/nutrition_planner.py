"""
Módulo de Planificación Nutricional de Werbly.
Proporciona el contexto necesario para que la IA genere planes de alimentación personalizados.

**Propósito**:
Este módulo actúa como puente entre los datos del usuario y la IA, asegurando que esta reciba toda la información relevante para crear un plan de alimentación dinámico y completamente personalizado.

**Conexión con otros módulos**:
- **Entrada de datos:** Recibe información desde `user_data`, análisis desde `analysis_engine` y datos dinámicos desde Firestore.
- **Salida de contexto:** Proporciona un resumen estructurado al módulo `ai_core` para que la IA diseñe planes de alimentación únicos.
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

        # Recuperar preferencias y restricciones
        dietary_preferences = user_data.get("dietary_preferences", [])
        dietary_restrictions = user_data.get("dietary_restrictions", [])

        # Crear contexto estructurado
        context = {
            "recommended_calories": analysis.get("recommended_calories", 2000),
            "needs_more_protein": analysis.get("needs_more_protein", False),
            "dietary_preferences": dietary_preferences,
            "dietary_restrictions": dietary_restrictions,
            "long_term_goals": user_data.get("long_term_goals", "No definidos"),
            "recent_achievements": user_data.get("recent_achievements", []),
            "current_weight": user_data.get("weight", None),
            "height": user_data.get("height", None),
            "activity_level": user_data.get("activity_level", "unknown")
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

        # Crear prompt para la IA
        prompt = (
            "Eres un asistente nutricional avanzado. Genera un plan de alimentación personalizado basado en el "
            "siguiente contexto:\n"
            f"{context}\n"
            "El plan debe incluir las calorías diarias recomendadas, comidas principales y sugerencias de alimentos. "
            "También debe considerar las preferencias y restricciones alimenticias del usuario."
        )

        # Generar plan usando la IA
        nutrition_plan = ai_core.query_model(prompt)
        return nutrition_plan
    except Exception as e:
        return f"Error al generar el plan nutricional con IA: {str(e)}"
