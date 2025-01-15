"""
Archivo principal para arrancar Bwere.
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
    print("Firebase initialized. ¡Comencemos una conversación con Bwere!\n")
    print("Bwere: ¡Hola! Soy Bwere, tu asistente de bienestar personalizado. ¿En qué puedo ayudarte hoy?\n")

    user_id = "loki"  # Puedes cambiar este ID según el usuario con el que deseas interactuar.
    while True:
        try:
            user_input = input("Tú: ")
            if user_input.lower() in ["salir", "exit", "quit"]:
                print("Bwere: ¡Hasta luego! Siempre estaré aquí para ayudarte.")
                break

            # Obtener respuesta de Bwere usando GPT
            response = ask_werbly(user_id, user_input)  # Proporcionamos ambos argumentos

            # Mostrar la respuesta al usuario
            print(f"Bwere: {response}\n")

            # Guardar la conversación en Firebase (opcional, si quieres activarlo)
            # save_message(user_id, "user", user_input)
            # save_message(user_id, "werbly", response)

        except Exception as e:
            print("Error durante la conversación:", e)


def run_app():
    """
    Flujo principal de la aplicación.
    """
    # 1. Inicializar Firebase
    init_firebase()
    print("Firebase initialized.")

    # 2. Iniciar conversación interactiva
    start_conversation()

if __name__ == "__main__":
    run_app()