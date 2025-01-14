import os
from dotenv import load_dotenv
from logging_utils import setup_logger

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Configurar logging
logger = setup_logger("pipeline_simulation.log")

def simulate_pipeline():
    """
    Simulación del pipeline para verificar:
    1. Configuración de variables de entorno.
    2. Existencia de directorios necesarios.
    3. Conexión básica con las APIs configuradas.
    """
    try:
        # 1. Verificar variables de entorno necesarias
        required_env_vars = [
            "USDA_API_KEY", "EDAMAM_API_ID", "EDAMAM_API_KEY",
            "SPOONACULAR_API_KEY", "CALORIE_NINJAS_API_KEY",
            "OPENFOODFACTS_USER_AGENT", "PUBCHEM_API_BASE_URL",
            "GITHUB_API_KEY", "KAGGLE_USERNAME", "KAGGLE_KEY"
        ]
        
        missing_vars = [var for var in required_env_vars if not os.getenv(var)]
        if missing_vars:
            logger.error(f"Faltan las siguientes variables de entorno: {', '.join(missing_vars)}")
            raise EnvironmentError("Configura las variables de entorno faltantes antes de ejecutar la simulación.")

        logger.info("Todas las variables de entorno necesarias están configuradas.")
        
        # 2. Verificar existencia de directorios necesarios
        directories = [
            "./raw_data/opensim", "./structured_data/opensim",
            "./structured_data/acsm", "./structured_data/ninds",
            "./raw_data/kaggle", "./structured_data/kaggle"
        ]
        
        for directory in directories:
            if not os.path.exists(directory):
                logger.warning(f"El directorio no existe: {directory}")
            else:
                logger.info(f"El directorio existe: {directory}")
        
        # 3. Simular conexión con las APIs configuradas
        logger.info("Simulando conexión con APIs configuradas...")
        
        # Simulación de prueba de API
        simulate_api_connections()

        logger.info("¡Simulación completada con éxito!")
    except Exception as e:
        logger.error(f"Error durante la simulación: {e}")
        raise

def simulate_api_connections():
    """
    Simula la conexión con las APIs configuradas.
    """
    import requests
    
    apis_to_test = [
        {
            "name": "USDA",
            "url": "https://api.nal.usda.gov/fdc/v1/foods/list",
            "params": {"api_key": os.getenv("USDA_API_KEY"), "pageSize": 1}
        },
        {
            "name": "Edamam",
            "url": "https://api.edamam.com/api/food-database/v2/parser",
            "params": {
                "app_id": os.getenv("EDAMAM_API_ID"),
                "app_key": os.getenv("EDAMAM_API_KEY"),
                "ingr": "apple"
            }
        },
        {
            "name": "Spoonacular",
            "url": "https://api.spoonacular.com/recipes/complexSearch",
            "params": {"apiKey": os.getenv("SPOONACULAR_API_KEY"), "query": "chicken"}
        },
        {
            "name": "CalorieNinjas",
            "url": "https://api.calorieninjas.com/v1/nutrition",
            "headers": {"X-Api-Key": os.getenv("CALORIE_NINJAS_API_KEY")},
            "params": {"query": "banana"}
        }
    ]
    
    for api in apis_to_test:
        try:
            if "headers" in api:
                response = requests.get(api["url"], headers=api["headers"], params=api["params"])
            else:
                response = requests.get(api["url"], params=api["params"])
            
            if response.status_code == 200:
                logger.info(f"Conexión exitosa con la API {api['name']}.")
            else:
                logger.warning(f"Conexión fallida con la API {api['name']}. Código de estado: {response.status_code}")
        except Exception as e:
            logger.error(f"Error al conectar con la API {api['name']}: {e}")

if __name__ == "__main__":
    logger.info("Iniciando simulación del pipeline...")
    simulate_pipeline()
