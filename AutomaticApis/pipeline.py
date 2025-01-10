from scripts.download_data import download_data
from scripts.normalize_data import normalize_data
from scripts.sync_firestore import sync_firestore
from scripts.logging_utils import setup_logger

# Configurar logging
logger = setup_logger("pipeline.log")

def main():
    try:
        # Descargar datos
        logger.info("Iniciando descarga de datos...")
        download_data()
        
        # Normalizar datos
        logger.info("Iniciando normalización de datos...")
        normalize_data()
        
        # Sincronizar con Firestore
        logger.info("Iniciando sincronización con Firestore...")
        sync_firestore()
        
        logger.info("¡Pipeline completado con éxito!")
    except Exception as e:
        logger.error(f"Error en el pipeline: {e}")

if __name__ == "__main__":
    main()
