"""
Módulo de Conexión a Firebase de Bwere.
Gestiona la inicialización del Admin SDK de Firebase y proporciona un cliente de Firestore.

**Propósito**:
Este módulo es responsable de conectar Bwere con Firebase, gestionando la autenticación mediante un archivo de claves seguras. Proporciona acceso centralizado a Firestore, permitiendo a otros módulos realizar operaciones de lectura, escritura y eliminación en la base de datos.

**Conexión con otros módulos**:
- **Entrada de datos:** Utiliza un archivo de credenciales JSON, cuya ubicación está definida por una variable de entorno (`FIREBASE_CRED_PATH`).
- **Salida de servicios:** Proporciona una instancia de Firestore para que módulos como `conversation_manager`, `user_data` y `analysis_engine` interactúen con la base de datos.
- **Integración con Google Secret Manager:** Compatible con configuraciones que almacenan las claves en servicios externos para mayor seguridad.
"""

import os
import logging
import firebase_admin
from firebase_admin import credentials, firestore

# Configuración de logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Variable global para el cliente de Firestore
_firestore_client = None

def init_firebase():
    """
    Inicializa la app de Firebase si no está ya inicializada.
    Utiliza un archivo de credenciales cuya ubicación se especifica en la variable de entorno FIREBASE_CRED_PATH.
    Si la variable de entorno no está configurada, usa 'serviceAccountKey.json' como valor predeterminado.

    Maneja errores comunes relacionados con la inicialización.
    """
    try:
        if not firebase_admin._DEFAULT_APP_NAME in firebase_admin._apps:
            cred_path = os.getenv("FIREBASE_CRED_PATH", "serviceAccountKey.json")
            if not os.path.exists(cred_path):
                logging.error(f"Archivo de credenciales '{cred_path}' no encontrado.")
                raise FileNotFoundError(f"El archivo de credenciales '{cred_path}' no fue encontrado.")

            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
            logging.info("Firebase inicializado correctamente.")
    except FileNotFoundError as fnf_error:
        logging.critical("Error: Archivo de credenciales no encontrado.")
        raise fnf_error
    except Exception as e:
        logging.exception("Error inesperado al inicializar Firebase.")
        raise RuntimeError(f"Error al inicializar Firebase: {str(e)}")

def get_firestore_client():
    """
    Retorna un cliente de Firestore, iniciando Firebase si fuera necesario.
    Implementa un patrón singleton para evitar inicializaciones múltiples.

    :return: Instancia del cliente de Firestore.
    """
    global _firestore_client
    if _firestore_client is None:
        init_firebase()
        _firestore_client = firestore.client()
        logging.info("Cliente de Firestore inicializado y listo para su uso.")
    return _firestore_client

def test_connection():
    """
    Prueba la conexión con Firestore realizando una operación básica.
    Útil para verificar que Firebase está correctamente configurado.

    :return: Mensaje indicando el estado de la conexión.
    """
    try:
        client = get_firestore_client()
        client.collection("test").document("connection_check").set({"status": "ok"})
        logging.info("Prueba de conexión con Firestore completada exitosamente.")
        return "Conexión con Firestore exitosa."
    except Exception as e:
        logging.error(f"Error al probar la conexión con Firestore: {str(e)}")
        return f"Error al probar la conexión con Firestore: {str(e)}"
