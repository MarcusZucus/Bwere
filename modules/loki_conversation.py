from modules.firebase_connection import init_firebase
from modules.conversation_manager import save_message
from modules.openai_api import ask_werbly

def start_loki_conversation(user_id="anon"):
    """
    Inicia una conversación con Werbly. Por defecto, el usuario es "anon".
    """
    init_firebase()
    print(f"Firebase initialized. Ahora estás hablando como {user_id}. Escribe 'salir' para terminar.\n")

    while True:
        user_input = input("Tú: ").strip()
        if user_input.lower() == "salir":
            print("¡Hasta luego!")
            break

        # Guardar el mensaje del usuario
        save_message(user_id, "user", user_input)

        # Obtener respuesta de Werbly
        response = ask_werbly(user_input)
        print(f"Werbly (para {user_id}):", response)

        # Guardar la respuesta de Werbly
        save_message(user_id, "werbly", response)

