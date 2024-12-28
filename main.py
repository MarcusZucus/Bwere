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

def start_conversation():
    """
    Inicia un bucle interactivo para conversar con Werbly en tiempo real.
    """
    print("Firebase initialized. \u00a1Comencemos una conversaci\u00f3n con Werbly!\n")
    print("Werbly: \u00a1Hola! Soy Werbly, tu asistente de bienestar personalizado. \u00bfEn qu\u00e9 puedo ayudarte hoy?\n")

    user_id = "loki"  # Puedes cambiar este ID seg\u00fan el usuario con el que deseas interactuar.
    while True:
        try:
            user_input = input("T\u00fa: ")
            print("Recibido del usuario:", user_input)  # Depuraci\u00f3n
            if user_input.lower() in ["salir", "exit", "quit"]:
                print("Werbly: \u00a1Hasta luego! Siempre estar\u00e9 aqu\u00ed para ayudarte.")
                break

            # Obtener respuesta de Werbly usando GPT-3.5-turbo
            response = ask_werbly(user_input)
            print("Respuesta generada por Werbly:", response)  # Depuraci\u00f3n
            print(f"Werbly: {response}\n")

            # Guardar la conversaci\u00f3n en Firebase (comentado temporalmente)
            # save_message(user_id, "user", user_input)
            # save_message(user_id, "werbly", response)

        except Exception as e:
            print("Error durante la conversaci\u00f3n:", e)

def run_app():
    """
    Flujo principal de la aplicaci\u00f3n.
    """
    # 1. Inicializar Firebase
    init_firebase()
    print("Firebase initialized.")

    # 2. Iniciar conversaci\u00f3n interactiva
    start_conversation()

if __name__ == "__main__":
    run_app()
