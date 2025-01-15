"""
Módulo de Seguridad y Validaciones de Bwere.
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
from modules.ai_core import query_model


def prepare_validation_context(
    nutrition_plan: Dict[str, Any],
    training_plan: Dict[str, Any],
    user_id: str
) -> Dict[str, Any]:
    """
    Genera un contexto dinámico basado en los planes, datos del usuario y configuraciones adicionales.

    :param nutrition_plan: Diccionario con el plan nutricional generado.
    :param training_plan: Diccionario con el plan de entrenamiento generado.
    :param user_id: Identificador único del usuario.
    :return: Diccionario con el contexto estructurado.
    """
    try:
        db = get_firestore_client()

        # Recuperar datos del usuario desde Firestore
        user_ref = db.collection("usuarios").document(user_id)
        user_data = user_ref.get().to_dict() or {}

        # Recuperar configuraciones de seguridad desde Firestore
        safety_config = db.collection("config").document("safety_limits").get().to_dict() or {}

        # Agregar análisis dinámico si está disponible
        context = {
            "nutrition_plan": nutrition_plan,
            "training_plan": training_plan,
            "user_data": user_data,
            "safety_config": safety_config
        }

        # Incluir campos adicionales dinámicos si están disponibles
        for key, value in user_data.items():
            if key not in context["user_data"]:  # Evita duplicados
                context["user_data"][key] = value

        return context
    except Exception as e:
        raise RuntimeError(f"Error al preparar el contexto dinámico: {str(e)}")


def validate_plans_with_ai(nutrition_plan: Dict[str, Any], training_plan: Dict[str, Any], user_id: str) -> str:
    """
    Envía el contexto dinámico a la IA para que evalúe si los planes son seguros y adecuados.

    :param nutrition_plan: Diccionario con el plan nutricional generado.
    :param training_plan: Diccionario con el plan de entrenamiento generado.
    :param user_id: Identificador único del usuario.
    :return: Respuesta de la IA indicando si los planes son seguros o necesitan ajustes.
    """
    try:
        # Preparar contexto dinámico
        validation_context = prepare_validation_context(nutrition_plan, training_plan, user_id)

        # Crear prompt dinámico para la IA
        prompt = (
            "Eres un asistente avanzado de validación de planes de bienestar. Evalúa si los siguientes planes nutricionales "
            "y de entrenamiento son seguros, adecuados y alineados con el perfil del usuario. Proporciona recomendaciones "
            "detalladas si se requiere algún ajuste.\n\n"
            f"Contexto de validación:\n{validation_context}\n\n"
            "Responde con un análisis claro, incluyendo aspectos positivos, riesgos potenciales y ajustes recomendados."
        )

        # Enviar contexto a la IA para validación
        response = query_model(prompt)
        return response
    except Exception as e:
        return f"Error al validar los planes con IA: {str(e)}"
