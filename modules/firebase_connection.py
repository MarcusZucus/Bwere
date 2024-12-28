"""
Módulo de Conexión a Firebase.
Inicializa el Admin SDK de Firebase y provee instancias de Firestore.
"""

import os
import firebase_admin
from firebase_admin import credentials, firestore

_firebase_app = None
_firestore_client = None

def init_firebase():
    """
    Inicializa la app de Firebase si no está ya inicializada.
    """
    global _firebase_app, _firestore_client
    if not _firebase_app:
        cred_path = os.getenv("FIREBASE_CRED_PATH", "serviceAccountKey.json")
        cred = credentials.Certificate(cred_path)
        _firebase_app = firebase_admin.initialize_app(cred)
        print("Firebase inicializado.")
    else:
        print("Firebase ya estaba inicializado.")

    # Configurar Firestore client si no está configurado
    if _firestore_client is None:
        _firestore_client = firestore.client()
        print("Firestore cliente configurado.")

def get_firestore_client():
    """
    Retorna un cliente de Firestore, iniciando Firebase si fuera necesario.
    """
    global _firestore_client
    if _firestore_client is None:
        init_firebase()
    return _firestore_client
