import os
import openai
import requests
from firebase_admin import credentials, firestore, initialize_app
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Claves de las APIs
GITHUB_API_KEY = os.getenv("GITHUB_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Configurar claves
openai.api_key = OPENAI_API_KEY

if not GITHUB_API_KEY or not OPENAI_API_KEY:
    print("Error: Faltan claves de API en el archivo .env")
    exit()

# Inicializar Firestore
cred = credentials.Certificate("serviceAccountKey.json")
initialize_app(cred)
db = firestore.client()

# URL de la API de GitHub
GITHUB_REPO_URL = "https://api.github.com/repos/MarcusZucus/WerblyAI/contents/"
HEADERS = {
    "Authorization": f"Bearer {GITHUB_API_KEY}",
    "Accept": "application/vnd.github.v3+json"
}

def cargar_prompt():
    """Cargar el prompt inicial desde Firestore."""
    try:
        doc_ref = db.collection("prompts").document("prompt_Loid_developer")
        prompt_data = doc_ref.get().to_dict()
        return prompt_data["content"]
    except Exception as e:
        return f"Error al cargar el prompt desde Firestore: {str(e)}"

def listar_archivos_github():
    """Listar archivos en el repositorio de GitHub."""
    try:
        response = requests.get(GITHUB_REPO_URL, headers=HEADERS)
        if response.status_code == 200:
            return [file['name'] for file in response.json()]
        else:
            return []
    except requests.exceptions.RequestException as e:
        return []

def leer_archivo_github(nombre_archivo):
    """Leer el contenido de un archivo en GitHub."""
    try:
        response = requests.get(f"{GITHUB_REPO_URL}{nombre_archivo}", headers=HEADERS)
        if response.status_code == 200:
            file_data = response.json()
            if "content" in file_data:
                import base64
                return base64.b64decode(file_data["content"]).decode("utf-8")
            else:
                return "Error: No se pudo encontrar el contenido del archivo."
        else:
            return f"Error al acceder al archivo {nombre_archivo}: {response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"Error al realizar la solicitud para leer {nombre_archivo}: {str(e)}"

def interactuar_con_gpt(historial, mensaje_usuario):
    """Enviar un mensaje al modelo GPT-3.5-Turbo manteniendo el contexto."""
    try:
        # Agregar el mensaje del usuario al historial
        historial.append({"role": "user", "content": mensaje_usuario})
        respuesta = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=historial
        )
        # Agregar la respuesta de GPT al historial
        respuesta_content = respuesta["choices"][0]["message"]["content"]
        historial.append({"role": "assistant", "content": respuesta_content})
        return respuesta_content, historial
    except Exception as e:
        return f"Error al interactuar con GPT: {str(e)}", historial

def main():
    """Función principal para interactuar con GPT y acceder a Firestore/GitHub."""
    prompt = cargar_prompt()
    historial = [{"role": "system", "content": prompt}]
    print("¡Loid está listo para ayudarte! Escribe 'salir' para finalizar la conversación.")

    while True:
        mensaje_usuario = input("\nTú: ")
        if mensaje_usuario.lower() == "salir":
            print("Loid: ¡Hasta luego! Aquí estaré para cuando me necesites.")
            break

        # Comandos personalizados
        if mensaje_usuario.lower() == "listar":
            archivos = listar_archivos_github()
            if archivos:
                respuesta = "Aquí tienes los archivos en tu repositorio:\n" + "\n".join(f"- {archivo}" for archivo in archivos)
            else:
                respuesta = "No pude recuperar los archivos del repositorio."
            print(f"Loid: {respuesta}")
            historial.append({"role": "assistant", "content": respuesta})
            continue

        if mensaje_usuario.lower().startswith("leer "):
            nombre_archivo = mensaje_usuario[5:].strip()
            contenido = leer_archivo_github(nombre_archivo)
            print(f"Loid: Contenido de {nombre_archivo}:\n{contenido}")
            historial.append({"role": "assistant", "content": contenido})
            continue

        # Conversación fluida con GPT
        respuesta, historial = interactuar_con_gpt(historial, mensaje_usuario)
        print(f"Loid: {respuesta}")

if __name__ == "__main__":
    main()
