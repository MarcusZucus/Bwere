import os
from scripts.download_data import download_data
from scripts.normalize_data import normalize_data
from scripts.sync_firestore import sync_firestore
from scripts.process_opensim import process_opensim_data
from scripts.process_acsm import process_acsm_data
from scripts.process_ninds import process_ninds_data
from scripts.logging_utils import setup_logger

# Configurar logging
logger = setup_logger("pipeline.log")

def main():
    """
    Pipeline principal para:
    1. Descargar datos desde APIs configuradas y Kaggle.
    2. Procesar datos específicos (OpenSim, ACSM, NINDS).
    3. Normalizar los datos descargados.
    4. Sincronizar los datos procesados con Firestore.
    """
    try:
        # Descargar datos desde las APIs configuradas y Kaggle
        logger.info("Iniciando descarga de datos desde las APIs y Kaggle...")
        download_data()
        
        # Procesar datos de OpenSim
        logger.info("Iniciando procesamiento de datos de OpenSim...")
        process_opensim_data(
            input_dir="./raw_data/opensim",
            output_dir="./structured_data/opensim",
            supported_formats=[".sto", ".mot", ".osim"]
        )
        
        # Procesar datos de ACSM
        logger.info("Iniciando procesamiento de datos de ACSM...")
        process_acsm_data(
            data_source="https://www.acsm.org/",
            output_dir="./structured_data/acsm"
        )
        
        # Procesar datos de NINDS
        logger.info("Iniciando procesamiento de datos de NINDS...")
        process_ninds_data(
            data_source="https://www.ninds.nih.gov/",
            output_dir="./structured_data/ninds"
        )
        
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
    
    # Validar directorios necesarios
    directories = [
        "./raw_data/opensim", "./structured_data/opensim",
        "./structured_data/acsm", "./structured_data/ninds",
        "./raw_data/kaggle", "./structured_data/kaggle"
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            logger.info(f"Creando directorio: {directory}")
            os.makedirs(directory, exist_ok=True)
    
    logger.info("Todas las variables de entorno y directorios necesarios están configurados.")
    
    # Ejecutar el pipeline principal
    main()
