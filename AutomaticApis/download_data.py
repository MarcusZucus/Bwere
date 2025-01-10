import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

CONFIG_FILE = "config/apis_config.json"
RAW_DATA_DIR = "raw_data"

def load_config(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

def replace_env_variables(params):
    for key, value in params.items():
        if isinstance(value, str) and value.startswith("${"):
            env_var = value[2:-1]
            params[key] = os.getenv(env_var)
    return params

def download_data():
    os.makedirs(RAW_DATA_DIR, exist_ok=True)
    config = load_config(CONFIG_FILE)

    for api_name, api_config in config.items():
        print(f"Descargando datos de {api_name}...")
        for attempt in range(3):
            try:
                params = replace_env_variables(api_config["params"])
                response = requests.request(
                    method=api_config["method"],
                    url=api_config["url"],
                    headers=api_config["headers"],
                    params=params
                )
                response.raise_for_status()
                
                raw_file = os.path.join(RAW_DATA_DIR, f"{api_name.lower()}.json")
                with open(raw_file, "w") as f:
                    json.dump(response.json(), f, indent=4)
                print(f"Datos guardados: {raw_file}")
                break
            except Exception as e:
                print(f"Intento {attempt + 1} fallido: {e}")
                if attempt == 2:
                    raise
