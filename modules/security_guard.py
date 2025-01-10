"""
Módulo de Seguridad y Validaciones de Werbly.
Proporciona el contexto necesario para que la IA evalúe si los planes nutricionales y de entrenamiento 
son seguros y adecuados para el usuario.

**Propósito**:
- Este módulo recopila datos dinámicos relevantes según el contexto del usuario y los organiza en un formato 
  flexible para que la IA pueda tomar decisiones informadas.

**Conexión con otros módulos**:
- **Entrada de datos:** Recibe planes generados desde `nutrition_planner` y `training_planner`.
- **Salida de contexto:** Proporciona un resumen estructurado al módulo `ai_core` para que la IA valide o ajuste los planes.
- **Integración con Firestore:** Recupera configuraciones y datos adicionales según el perfil del usuario.
"""

from typing import Dict, Any
from modules.firebase_connection import get_firestore_client


def prepare_dynamic_validation_context(
    nutrition_plan: Dict[str, Any],
    training_plan: Dict[str, Any],
    user_id: str
) -> Dict[str, Any]:
    """
    Genera un contexto dinámico basado en los planes, datos del usuario, y configuraciones adicionales.

    :param nutrition_plan: Diccionario con el plan nutricional generado.
    :param training_plan: Diccionario con el plan de entrenamiento generado.
    :param user_id: Identificador único del usuario.
    :return: Diccionario con el contexto estructurado.
    """
    try:
        db = get_firestore_client()

        # Recuperar datos básicos del usuario desde Firestore
        user_data = db.collection("usuarios").document(user_id).get().to_dict() or {}

        # Recuperar configuraciones adicionales desde Firestore
        safety_config = db.collection("config").document("safety_limits").get().to_dict() or {}

        # Construir contexto dinámico
        context = {
            "nutrition_plan": nutrition_plan,
            "training_plan": training_plan,
            "user_data": {
                "weight": user_data.get("weight"),
                "height": user_data.get("height"),
                "activity_level": user_data.get("activity_level"),
                "dietary_restrictions": user_data.get("dietary_restrictions", []),
                "goals": user_data.get("goals", []),
                "medical_conditions": user_data.get("medical_conditions", []),
                "previous_plans": user_data.get("previous_plans", [])
            },
            "safety_config": safety_config
        }

        return context
    except Exception as e:
        raise RuntimeError(f"Error al preparar el contexto dinámico: {str(e)}")


def validate_with_ai(validation_context: Dict[str, Any], ai_core) -> str:
    """
    Envía el contexto dinámico a la IA para que evalúe si los planes son seguros y adecuados.

    :param validation_context: Diccionario con el contexto estructurado de los planes y el usuario.
    :param ai_core: Referencia al módulo `ai_core` para que la IA realice la validación.
    :return: Respuesta de la IA indicando si los planes son seguros o necesitan ajustes.
    """
    try:
        # Crear prompt para la IA
        prompt = (
            "Eres un sistema avanzado de validación de planes de bienestar. Evalúa si los siguientes planes nutricionales "
            "y de entrenamiento son seguros y adecuados para el usuario, y proporciona recomendaciones si es necesario.\n\n"
            f"Contexto de validación:\n{validation_context}"
        )

        # Enviar el contexto a la IA para validación
        response = ai_core.query_model(prompt)
        return response
    except Exception as e:
        return f"Error al validar los planes con IA: {str(e)}"
