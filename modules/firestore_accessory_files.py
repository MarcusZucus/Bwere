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
    :param collection_path: Ruta de la colección (por ejemplo, 'AccessoryFiles/AnswerFile/AnswerList').
    :return: Lista de documentos (cada documento es un diccionario).
    """
    try:
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
            print(f"El documento con ID {document_id} no existe en {collection_path}.")
            return None
    except Exception as e:
        print(f"Error al obtener el documento {document_id} de {collection_path}: {e}")
        return None

def get_subcollection_documents(document_path, subcollection_name):
    """
    Obtiene los documentos dentro de una subcolección específica.
    :param document_path: Ruta del documento principal (por ejemplo, 'AccessoryFiles/AnswerFile').
    :param subcollection_name: Nombre de la subcolección (por ejemplo, 'AnswerList').
    :return: Lista de documentos en la subcolección.
    """
    try:
        subcollection_ref = db.document(document_path).collection(subcollection_name)
        docs = subcollection_ref.stream()
        return [doc.to_dict() for doc in docs]
    except Exception as e:
        print(f"Error al obtener documentos de la subcolección {subcollection_name} en {document_path}: {e}")
        return []
