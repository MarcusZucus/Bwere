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
    collection_ref = db.collection(collection_path)
    docs = collection_ref.stream()
    return [doc.to_dict() for doc in docs]

def get_document_by_id(collection_path, document_id):
    """
    Obtiene un documento específico por su ID.
    :param collection_path: Ruta de la colección.
    :param document_id: ID del documento a buscar.
    :return: Diccionario con los datos del documento, o None si no existe.
    """
    doc_ref = db.collection(collection_path).document(document_id)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    return None

def search_documents_in_subcollection(collection_path, subcollection_name, field, value):
    """
    Busca documentos en una subcolección que coincidan con un valor específico.
    :param collection_path: Ruta de la colección principal.
    :param subcollection_name: Nombre de la subcolección a buscar.
    :param field: Campo a buscar.
    :param value: Valor a buscar en el campo.
    :return: Lista de documentos que coincidan.
    """
    collection_ref = db.collection(collection_path).document(subcollection_name).collections()
    results = []
    for subcollection in collection_ref:
        docs = subcollection.where(field, "==", value).stream()
        for doc in docs:
            results.append(doc.to_dict())
    return results

def get_answer_list():
    """
    Obtiene todos los documentos en la subcolección AnswerList de AccessoryFiles/AnswerFile.
    :return: Lista de documentos en la subcolección AnswerList.
    """
    return get_all_documents_in_collection("AccessoryFiles/AnswerFile/AnswerList")

def get_specific_answer(answer_id):
    """
    Busca un AnswerList específico por su ID.
    :param answer_id: ID del AnswerList a buscar.
    :return: Diccionario con los datos del AnswerList, o None si no existe.
    """
    return get_document_by_id("AccessoryFiles/AnswerFile/AnswerList", answer_id)
