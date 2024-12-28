"""
Módulo de Gestión de Conversaciones.
Registra cada turno de conversación y recupera historiales.
"""

import datetime
from modules.firebase_connection import get_firestore_client

def save_message(user_id, role, content):
    """
    Guarda un turno de conversación en 'usuarios/{user_id}/conversaciones'.
    """
    db = get_firestore_client()
    db.collection("usuarios").document(user_id)\
      .collection("conversaciones").add({
          "role": role,
          "content": content,
          "time": datetime.datetime.utcnow()
      })

def get_conversation_history(user_id):
    """
    Retorna una lista del historial en orden cronológico.
    """
    db = get_firestore_client()
    docs = db.collection("usuarios").document(user_id)\
             .collection("conversaciones").order_by("time").get()
    return [doc.to_dict() for doc in docs]
