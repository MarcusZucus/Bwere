"""
Módulo de Gestión de Conversaciones.
Registra cada turno de conversación y recupera historiales.
"""

import datetime
from modules.firebase_connection import get_firestore_client


def save_message(user_id, role, content):
    """
    Guarda un turno de conversación en 'usuarios/{user_id}/conversaciones'.
    Verifica que los datos no estén vacíos antes de guardarlos.
    """
    if not user_id or not role or not content:
        raise ValueError("Todos los campos (user_id, role, content) son obligatorios.")

    db = get_firestore_client()
    db.collection("usuarios").document(user_id)\
      .collection("conversaciones").add({
          "role": role,
          "content": content,
          "timestamp": datetime.datetime.utcnow()
      })


def get_conversation_history(user_id):
    """
    Recupera el historial completo de la conversación desde Firestore.
    Retorna una lista del historial en orden cronológico.
    Maneja el caso donde no hay historial disponible.
    """
    if not user_id:
        raise ValueError("El user_id es obligatorio para recuperar el historial.")

    db = get_firestore_client()
    conversations = db.collection("usuarios").document(user_id)\
                      .collection("conversaciones").order_by("timestamp").stream()

    history = [{"role": c.get("role"), "content": c.get("content")} for c in conversations]

    if not history:
        # Mensaje inicial predeterminado si no hay historial
        history.append({"role": "system", "content": "Hola, soy Werbly. ¿En qué puedo ayudarte hoy?"})

    return history
