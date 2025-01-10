"""
Módulo de Manejo de Prompts.
Su propósito es construir el prompt base que ayuda a la IA a interpretar su rol y propósito en las interacciones.
Confía en que la IA tiene acceso directo a Firestore y al historial de datos dinámicos del usuario.

**Propósito**:
- Este módulo se centra en proporcionar un prompt base consistente y adaptado al propósito de la IA.
- Deja la interpretación del historial, contexto y datos dinámicos a la IA entrenada, ya que está integrada directamente con Firestore.

**Conexión con otros módulos**:
- **Entrada de datos:** Recupera el prompt base desde Firestore o utiliza un fallback predeterminado.
- **Salida de datos:** Devuelve un prompt base listo para enviar a la IA junto con la entrada del usuario.
"""
from modules.firebase_connection import get_firestore_client


def get_base_prompt() -> str:
    """
    Obtiene el prompt base almacenado en Firestore o utiliza un texto fijo como fallback.

    :return: Prompt base como texto.
    """
    try:
        db = get_firestore_client()
        doc_ref = db.collection("prompts").document("prompt_usuario").get()
        if doc_ref.exists:
            data = doc_ref.to_dict()
            prompt_base = data.get("contenido", "").strip()
            if not prompt_base:
                raise ValueError("El prompt base está vacío.")
            return prompt_base
        else:
            # Fallback si no existe el documento en Firestore
            return (
                "Eres Werbly, una innovadora plataforma diseñada para mejorar el bienestar personal de los usuarios. "
                "Ayuda de manera proactiva y personalizada, utilizando el historial y datos en Firestore para entender "
                "a cada usuario y proporcionar recomendaciones útiles."
            )
    except Exception as e:
        return f"Error al obtener el prompt base: {str(e)}"


def build_prompt(user_input: str) -> str:
    """
    Construye el prompt final combinando el prompt base con la entrada del usuario.

    :param user_input: Entrada del usuario.
    :return: Prompt final construido como texto.
    """
    try:
        # Obtener el prompt base
        base = get_base_prompt()

        # Construir el prompt final
        prompt = f"{base}\n\nUsuario: {user_input}"
        return prompt.strip()
    except Exception as e:
        return f"Error al construir el prompt: {str(e)}"
