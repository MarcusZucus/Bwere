# modules/config.py
"""Módulo de Configuración.
   Encargado de cargar variables de entorno y exponerlas de manera segura.
"""

import os
from dotenv import load_dotenv

# Cargamos el .env
# (Si .env está en la misma carpeta que main.py, y "config.py" se llama desde main, bastará con load_dotenv() a secas)
load_dotenv()

# Ahora leemos cada variable
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

# y así sucesivamente para cada variable que quieras exponer...
