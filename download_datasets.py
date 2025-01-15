import os
from kaggle.api.kaggle_api_extended import KaggleApi

# Inicializar Kaggle API
api = KaggleApi()
api.authenticate()

# Lista de palabras clave relevantes
keywords = ["health", "fitness", "nutrition", "activity", "exercise", "sports", "biomechanics", "lifestyle", "wellness"]

# Carpeta base para guardar datasets
base_download_path = "./datasets"

# Crear la carpeta base si no existe
os.makedirs(base_download_path, exist_ok=True)

# Descargar datasets para cada palabra clave
for keyword in keywords:
    print(f"Buscando datasets relacionados con: {keyword}")
    datasets = api.dataset_list(search=keyword)
    
    # Crear carpeta específica para la palabra clave
    keyword_path = os.path.join(base_download_path, keyword)
    os.makedirs(keyword_path, exist_ok=True)
    
    for dataset in datasets:
        dataset_ref = dataset.ref
        dataset_title = dataset.title
        print(f"Descargando: {dataset_title} ({dataset_ref})")
        
        try:
            # Descargar y descomprimir el dataset
            api.dataset_download_files(dataset_ref, path=keyword_path, unzip=True)
        except Exception as e:
            print(f"Error al descargar {dataset_title}: {e}")

print("Descarga completa de todos los datasets relacionados con Bwere.")
