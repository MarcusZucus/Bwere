"""
Módulo de Manejo de Prompts.
Se encarga de construir y formatear el prompt que se envía a la IA.
"""

from modules.firebase_connection import get_firestore_client

def get_base_prompt():
    """
    Obtiene el prompt base almacenado en Firestore: colección 'prompts',
    documento 'prompt_usuario', o un texto fijo si no existe.
    """
    db = get_firestore_client()
    doc_ref = db.collection("prompts").document("prompt_usuario").get()
    if doc_ref.exists:
        data = doc_ref.to_dict()
        return data.get("text", "Eres Werbly,...")
    else:
        # Fallback si no existe en Firestore
        return "Eres Werbly,..."

def build_prompt(user_input):
    """
    Construye el prompt final combinando el prompt base con la entrada del usuario.
    """
    base = get_base_prompt()
    return f"{base}\n\nUsuario: {user_input}"
