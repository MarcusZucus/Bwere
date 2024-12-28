"""
Módulo de Configuración (config)
Encargado de cargar variables de entorno y exponerlas de manera segura.
"""

import os
from dotenv import load_dotenv

# Cargamos las variables de .env
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
USDA_API_KEY = os.getenv("USDA_API_KEY")
EDAMAM_API_ID = os.getenv("EDAMAM_API_ID")
EDAMAM_API_KEY = os.getenv("EDAMAM_API_KEY")
OPENFOODFACTS_USER_AGENT = os.getenv("OPENFOODFACTS_USER_AGENT")
SPOONACULAR_API_KEY = os.getenv("SPOONACULAR_API_KEY")
CALORIE_NINJAS_API_KEY = os.getenv("CALORIE_NINJAS_API_KEY")
PUBCHEM_API_BASE_URL = os.getenv("PUBCHEM_API_BASE_URL")

def get_openai_key():
    return OPENAI_API_KEY

def get_usda_key():
    return USDA_API_KEY

def get_edamam_id():
    return EDAMAM_API_ID

def get_edamam_key():
    return EDAMAM_API_KEY

def get_openfoodfacts_user_agent():
    return OPENFOODFACTS_USER_AGENT

def get_spoonacular_key():
    return SPOONACULAR_API_KEY

def get_calorie_ninjas_key():
    return CALORIE_NINJAS_API_KEY

def get_pubchem_base_url():
    return PUBCHEM_API_BASE_URL
