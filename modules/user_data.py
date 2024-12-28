"""
Módulo de Datos del Usuario y Wearables.
Recopila y normaliza información biométrica, rutinas, etc.
"""

from modules.firebase_connection import get_firestore_client

def get_user_data(user_id):
    """
    Retorna los datos del usuario desde 'usuarios/{user_id}'.
    """
    db = get_firestore_client()
    doc = db.collection("usuarios").document(user_id).get()
    if doc.exists:
        return doc.to_dict()
    return {}

def update_user_data(user_id, data: dict):
    """
    Actualiza campos del documento 'usuarios/{user_id}' con un dict de datos.
    """
    db = get_firestore_client()
    db.collection("usuarios").document(user_id).set(data, merge=True)
