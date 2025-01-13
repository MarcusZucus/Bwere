import os
from scripts.download_data import download_data
from scripts.normalize_data import normalize_data
from scripts.sync_firestore import sync_firestore
from scripts.logging_utils import setup_logger

# Configurar logging
logger = setup_logger("pipeline.log")

def main():
    """
    Pipeline principal para:
    1. Descargar datos desde APIs configuradas y Kaggle.
    2. Normalizar los datos descargados.
    3. Sincronizar los datos procesados con Firestore.
    """
    try:
        # Descargar datos desde las APIs configuradas
        logger.info("Iniciando descarga de datos desde las APIs...")
        download_data()
        
        # Normalizar datos descargados
        logger.info("Iniciando normalización de datos descargados...")
        normalize_data()
        
        # Sincronizar datos con Firestore
        logger.info("Iniciando sincronización de datos con Firestore...")
        sync_firestore()
        
        logger.info("¡Pipeline completado con éxito!")
    except Exception as e:
        logger.error(f"Error en el pipeline: {e}")
        raise  # Elevar el error para depuración adicional si es necesario

if __name__ == "__main__":
    # Verifica que todas las configuraciones necesarias están presentes
    required_env_vars = [
        "USDA_API_KEY", "EDAMAM_API_ID", "EDAMAM_API_KEY",
        "SPOONACULAR_API_KEY", "CALORIE_NINJAS_API_KEY",
        "OPENFOODFACTS_USER_AGENT", "PUBCHEM_API_BASE_URL",
        "GITHUB_API_KEY", "KAGGLE_USERNAME", "KAGGLE_KEY"
    ]
    
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    
    if missing_vars:
        logger.error(f"Faltan las siguientes variables de entorno: {', '.join(missing_vars)}")
        raise EnvironmentError("Configura las variables de entorno faltantes antes de ejecutar el pipeline.")
    
    logger.info("Todas las variables de entorno necesarias están configuradas.")
    
    # Ejecutar el pipeline principal
    main()
