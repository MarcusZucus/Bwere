"""
Módulo de Conexión a Firebase.
Inicializa el Admin SDK de Firebase y provee instancias de Firestore.
"""

import os
import firebase_admin
from firebase_admin import credentials, firestore

# Variable global para el cliente de Firestore
_firestore_client = None

def init_firebase():
    """
    Inicializa la app de Firebase si no está ya inicializada.
    """
    if not firebase_admin._DEFAULT_APP_NAME in firebase_admin._apps:
        cred_path = os.getenv("FIREBASE_CRED_PATH", "serviceAccountKey.json")
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)

def get_firestore_client():
    """
    Retorna un cliente de Firestore, iniciando Firebase si fuera necesario.
    """
    global _firestore_client
    if _firestore_client is None:
        init_firebase()
        _firestore_client = firestore.client()
    return _firestore_client
