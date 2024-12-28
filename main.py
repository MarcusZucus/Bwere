"""
Archivo principal para arrancar Werbly.
"""

from modules.firebase_connection import init_firebase
from modules.openai_api import ask_werbly
from modules.conversation_manager import save_message
from modules.user_data import get_user_data, update_user_data
from modules.analysis_engine import analyze_user_data
from modules.nutrition_planner import generate_nutrition_plan
from modules.training_planner import generate_training_plan
from modules.security_guard import validate_plans
from modules.firestore_accessory_files import get_all_documents_in_collection


def fetch_accessory_files():
    """
    Recupera y muestra datos de la colección AccessoryFiles para usar con Werbly.
    """
    print("Obteniendo datos de AccessoryFiles...")
    collection_path = "AccessoryFiles/AnswerFile"  # Cambia a otra subcolección si es necesario.
    documents = get_all_documents_in_collection(collection_path)

    if documents:
        print(f"Se encontraron {len(documents)} documentos en {collection_path}:")
        for doc in documents:
            print(doc)
    else:
        print(f"No se encontraron documentos en {collection_path}.")


def start_conversation():
    """
    Inicia un bucle interactivo para conversar con Werbly en tiempo real.
    """
    print("Firebase initialized. ¡Comencemos una conversación con Werbly!\n")
    print("Werbly: ¡Hola! Soy Werbly, tu asistente de bienestar personalizado. ¿En qué puedo ayudarte hoy?\n")

    user_id = "loki"  # Puedes cambiar este ID según el usuario con el que deseas interactuar.
    while True:
        user_input = input("Tú: ")
        if user_input.lower() in ["salir", "exit", "quit"]:
            print("Werbly: ¡Hasta luego! Siempre estaré aquí para ayudarte.")
            break

        # Obtener respuesta de Werbly usando GPT-3.5-turbo
        response = ask_werbly(user_input)
        print(f"Werbly: {response}\n")

        # Guardar la conversación en Firebase
        save_message(user_id, "user", user_input)
        save_message(user_id, "werbly", response)


def run_app():
    """
    Flujo principal de la aplicación.
    """
    # 1. Inicializar Firebase
    init_firebase()
    print("Firebase initialized.")

    # 2. Recuperar datos de AccessoryFiles
    fetch_accessory_files()

    # 3. Iniciar conversación interactiva
    start_conversation()

    # 4. Ejemplo de flujo de análisis y planes
    user_id = "andres_123"
    user_data = get_user_data(user_id)
    analysis = analyze_user_data(user_data)
    nutrition_plan = generate_nutrition_plan(user_data, analysis)
    training_plan = generate_training_plan(user_data, analysis)

    # 5. Validar los planes
    if validate_plans(nutrition_plan, training_plan):
        print("Planes válidos. Listo para mostrar al usuario.")
    else:
        print("Planes peligrosos. Ajustar recomendaciones.")


if __name__ == "__main__":
    run_app()
