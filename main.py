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

def run_app():
    # 1. Inicializar Firebase
    init_firebase()
    print("Firebase initialized.")

    # 2. Probar llamada a OpenAI (Werbly)
    user_input = "Hola Werbly, ¿cómo me ayudas?"
    response = ask_werbly(user_input)
    print("Werbly responde:", response)

    # 3. Guardar una conversación
    user_id = "andres_123"
    save_message(user_id, "user", user_input)
    save_message(user_id, "werbly", response)

    # 4. Ejemplo de flujo de análisis y planes
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
