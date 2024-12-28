"""
Módulo para interactuar con la colección AccessoryFiles en Firestore.
Proporciona funciones para consultar datos relevantes para Werbly.
"""

import firebase_admin
from firebase_admin import credentials, firestore

# Inicialización de Firebase (solo si no está ya inicializado)
if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

def get_all_documents_in_collection(collection_path):
    """
    Obtiene todos los documentos en una colección específica de Firestore.
    :param collection_path: Ruta de la colección (por ejemplo, 'AccessoryFiles/AnswerFile').
    :return: Lista de documentos (cada documento es un diccionario).
    """
    try:
        # Verifica si collection_path se refiere a una subcolección
        path_parts = collection_path.split("/")
        if len(path_parts) % 2 == 0:
            raise ValueError(f"La ruta {collection_path} apunta a un documento, no a una colección.")

        collection_ref = db.collection(collection_path)
        docs = collection_ref.stream()
        return [doc.to_dict() for doc in docs]

    except Exception as e:
        print(f"Error al obtener documentos de {collection_path}: {e}")
        return []

def get_document_by_id(collection_path, document_id):
    """
    Obtiene un documento específico por su ID.
    :param collection_path: Ruta de la colección.
    :param document_id: ID del documento a buscar.
    :return: Diccionario con los datos del documento, o None si no existe.
    """
    try:
        doc_ref = db.collection(collection_path).document(document_id)
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        else:
            print(f"Documento con ID {document_id} no encontrado en {collection_path}.")
            return None
    except Exception as e:
        print(f"Error al obtener el documento {document_id} en {collection_path}: {e}")
        return None
