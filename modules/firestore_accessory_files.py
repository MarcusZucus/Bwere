"""
Módulo para interactuar con la colección AccessoryFiles en Firestore.
Proporciona funciones para consultar datos relevantes para Werbly, como listas de respuestas, configuraciones y otros datos accesorios.

**Propósito**:
Este módulo actúa como una interfaz para acceder a datos auxiliares almacenados en Firestore, necesarios para el funcionamiento de diferentes funcionalidades de Werbly. Específicamente, facilita la recuperación de documentos, subcolecciones y datos estructurados de la colección `AccessoryFiles`.

**Conexión con otros módulos**:
- **Entrada de datos:** Utiliza `firebase_connection` para conectarse a Firestore y consultar la colección `AccessoryFiles`.
- **Salida de datos:** Proporciona datos estructurados que pueden ser utilizados por módulos como `ai_core`, `recommendation_engine` y `analysis_engine` para enriquecer sus operaciones.
- **Uso en lógica central:** Este módulo sirve como fuente de datos para listas de respuestas predeterminadas, configuraciones dinámicas y valores auxiliares requeridos en tiempo de ejecución.
"""

from typing import List, Dict, Any
from modules.firebase_connection import get_firestore_client


def get_all_documents_in_collection(collection_path: str) -> List[Dict[str, Any]]:
    """
    Obtiene todos los documentos en una colección específica de Firestore.
    
    :param collection_path: Ruta de la colección (por ejemplo, 'AccessoryFiles/AnswerFile/AnswerList').
    :return: Lista de documentos (cada documento es un diccionario).
    """
    try:
        db = get_firestore_client()
        collection_ref = db.collection(collection_path)
        docs = collection_ref.stream()
        return [doc.to_dict() for doc in docs]
    except Exception as e:
        raise RuntimeError(f"Error al obtener documentos de {collection_path}: {str(e)}")


def get_document_by_id(collection_path: str, document_id: str) -> Dict[str, Any]:
    """
    Obtiene un documento específico por su ID.
    
    :param collection_path: Ruta de la colección.
    :param document_id: ID del documento a buscar.
    :return: Diccionario con los datos del documento, o None si no existe.
    """
    try:
        db = get_firestore_client()
        doc_ref = db.collection(collection_path).document(document_id)
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        else:
            return None
    except Exception as e:
        raise RuntimeError(f"Error al obtener el documento {document_id} de {collection_path}: {str(e)}")


def get_subcollection_documents(document_path: str, subcollection_name: str) -> List[Dict[str, Any]]:
    """
    Obtiene los documentos dentro de una subcolección específica.
    
    :param document_path: Ruta del documento principal (por ejemplo, 'AccessoryFiles/AnswerFile').
    :param subcollection_name: Nombre de la subcolección (por ejemplo, 'AnswerList').
    :return: Lista de documentos en la subcolección.
    """
    try:
        db = get_firestore_client()
        subcollection_ref = db.document(document_path).collection(subcollection_name)
        docs = subcollection_ref.stream()
        return [doc.to_dict() for doc in docs]
    except Exception as e:
        raise RuntimeError(f"Error al obtener documentos de la subcolección {subcollection_name} en {document_path}: {str(e)}")


def search_documents_by_field(collection_path: str, field_name: str, value: Any) -> List[Dict[str, Any]]:
    """
    Busca documentos en una colección filtrando por un campo específico y su valor.
    
    :param collection_path: Ruta de la colección donde buscar.
    :param field_name: Nombre del campo por el que filtrar.
    :param value: Valor del campo a buscar.
    :return: Lista de documentos que cumplen con el criterio de búsqueda.
    """
    try:
        db = get_firestore_client()
        collection_ref = db.collection(collection_path)
        query = collection_ref.where(field_name, "==", value)
        docs = query.stream()
        return [doc.to_dict() for doc in docs]
    except Exception as e:
        raise RuntimeError(f"Error al buscar documentos por {field_name}={value} en {collection_path}: {str(e)}")
