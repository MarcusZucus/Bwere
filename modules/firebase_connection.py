"""
Módulo de Conexión a Firebase.
Inicializa el Admin SDK de Firebase y provee instancias de Firestore.
"""

import os
import firebase_admin
from firebase_admin import credentials, firestore

_firebase_app = None

def init_firebase():
    """
    Inicializa la app de Firebase si no está ya inicializada.
    """
    global _firebase_app
    if not _firebase_app:
        cred_path = os.getenv("FIREBASE_CRED_PATH", "serviceAccountKey.json")
        cred = credentials.Certificate(cred_path)
        _firebase_app = firebase_admin.initialize_app(cred)

def get_firestore_client():
    """
    Retorna un cliente de Firestore, iniciando Firebase si fuera necesario.
    """
    if not firebase_admin._DEFAULT_APP_NAME in firebase_admin._apps:
        init_firebase()
    return firestore.client()
