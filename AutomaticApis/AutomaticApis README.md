# AutomaticApis

## **Descripción General**
AutomaticApis es un sistema modular diseñado para gestionar de manera integral la extracción, normalización y sincronización de datos provenientes de diversas fuentes, incluyendo APIs, scraping web y plataformas de almacenamiento de datos. El objetivo principal es automatizar la integración de información estructurada en bases de datos como Firestore, asegurando un flujo coherente y sinérgico entre sus componentes.

## **Estructura del Proyecto**
El sistema está dividido en múltiples módulos que cumplen roles específicos dentro del flujo de datos. A continuación, se describe cada archivo en la carpeta `AutomaticApis` y su propósito dentro del sistema:

### **1. Extractores de Datos**
Estos scripts se encargan de extraer datos desde fuentes específicas mediante técnicas de scraping o APIs. Son responsables de convertir datos no estructurados en formatos manejables para las etapas posteriores.

- **`acsm_data_extractor.py`**:
  - Extrae información de la American College of Sports Medicine (ACSM).
  - Utiliza `scrapy` y `selenium` para navegar por el sitio web y recolectar contenido estructurado.
  - Guarda temporalmente los datos en SQLite o en formato JSON.

- **`exrx_data_extractor.py`**:
  - Recopila datos relacionados con ejercicios físicos desde ExRx.net.
  - Similar al extractor de ACSM, usa `scrapy` y `selenium` para estructurar los datos antes de almacenarlos.

- **`musclewiki_data_extractor.py`**:
  - Extrae información sobre músculos y ejercicios desde MuscleWiki.
  - Su diseño permite que los datos se procesen directamente hacia Firestore tras la extracción.

- **`ninds_data_extractor.py`**:
  - Maneja la extracción de datos médicos sobre trastornos neurológicos desde el sitio oficial de NINDS.
  - Está optimizado para procesar tanto contenido HTML como documentos PDF.

### **2. Normalización de Datos**
La normalización asegura que los datos provenientes de diferentes fuentes compartan una estructura común y uniforme:

- **`normalize_data.py`**:
  - Transforma los datos extraídos en estructuras estandarizadas definidas por `mappings.json`.
  - Verifica la integridad de los datos y maneja valores ausentes o inconsistentes.

### **3. Descarga de Datos desde APIs**
Las fuentes de datos que proporcionan información mediante APIs son manejadas por este módulo:

- **`download_data.py`**:
  - Descarga datos desde las APIs configuradas en `apis_config.json`.
  - Reemplaza dinámicamente las variables de entorno para manejar claves de API de manera segura.
  - Almacena los datos descargados en la carpeta `raw_data` para ser procesados posteriormente.

### **4. Sincronización con Firestore**
El sistema integra los datos estructurados en una base de datos Firestore siguiendo reglas estrictas:

- **`sync_firestore.py`**:
  - Lee las reglas definidas en `firestore_rules.json` para determinar cómo y dónde deben almacenarse los datos.
  - Valida que los datos cumplan con los criterios mínimos antes de sincronizarlos.

### **5. Configuraciones y Mapeos**
Estos archivos definen las configuraciones necesarias para que los módulos trabajen de manera sincronizada:

- **`apis_config.json`**:
  - Contiene la configuración para cada API, incluyendo URLs, métodos HTTP, headers y parámetros requeridos.
  - Define los detalles de fuentes como USDA, Edamam, Spoonacular, Kaggle, entre otros.

- **`firestore_rules.json`**:
  - Establece las reglas de cómo deben sincronizarse los datos con Firestore, mapeando cada conjunto de datos a su colección correspondiente.

- **`mappings.json`**:
  - Proporciona las reglas para transformar datos crudos en estructuras normalizadas, asegurando coherencia en campos clave como nombres, calorías y otros atributos.

### **6. Pipeline Principal**
El archivo `pipeline.py` coordina todas las etapas del flujo de trabajo, desde la extracción hasta la sincronización:

1. **Descarga de Datos**:
   - Llama a `download_data.py` para recopilar datos crudos desde APIs y Kaggle.

2. **Procesamiento Específico**:
   - Invoca los extractores de datos (`acsm_data_extractor.py`, `ninds_data_extractor.py`, `musclewiki_data_extractor.py`, `exrx_data_extractor.py`) para procesar información especializada.
   - También llama a `process_opensim.py` para manejar datos biomecánicos en formatos específicos (.sto, .mot, .osim).

3. **Normalización**:
   - Ejecuta `normalize_data.py` para estructurar y validar los datos extraídos.

4. **Sincronización**:
   - Utiliza `sync_firestore.py` para cargar los datos normalizados en Firestore.

5. **Manejo de Logs**:
   - Centraliza todos los eventos y errores en `pipeline.log` mediante `logging_utils.py`.

### **7. Utilidades**

- **`logging_utils.py`**:
  - Configura el manejo de logs para registrar eventos críticos, errores y actividades generales.

### **8. Otros Archivos**
- **`pipeline_simulation.log`**:
  - Contiene logs generados durante simulaciones del pipeline.

- **`pipelinetry.py`**:
  - Prototipo para probar y validar las etapas del pipeline antes de su integración final.

---

## **Flujo Detallado**
El pipeline comienza desde la ejecución de `pipeline.py`, que orquesta todas las etapas del flujo de trabajo. El proceso detallado es el siguiente:

1. **Preparación**:
   - Carga de variables de entorno y validación de directorios necesarios.

2. **Ejecución del Pipeline**:
   - Descarga datos desde APIs mediante `download_data.py`.
   - Procesa datos específicos llamando a los extractores.
   - Normaliza los datos descargados con `normalize_data.py`.
   - Sincroniza los datos estructurados a Firestore con `sync_firestore.py`.

3. **Validación y Logs**:
   - Los logs generados en `pipeline.log` permiten rastrear el estado de cada etapa y diagnosticar problemas.

---

## **Propósito del Proyecto**
AutomaticApis facilita la integración de datos provenientes de múltiples fuentes mediante un flujo automatizado que garantiza precisión, consistencia y sincronización eficiente con Firestore. Esto lo hace ideal para aplicaciones que requieren manejar grandes volúmenes de información estructurada y dinámica.

