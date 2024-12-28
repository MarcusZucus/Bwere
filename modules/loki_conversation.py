"""
Módulo independiente para probar la interacción como 'loki' (u otro user) 
sin tocar el flujo general de Werbly.
"""

import openai
from modules.config import get_openai_key
from modules.firebase_connection import init_firebase
from modules.conversation_manager import save_message
from modules.user_data import get_user_data

def talk_as_werbly_for_user(user_id, user_input):
    """
    Llama a OpenAI con un 'system message' que indica que Werbly
    está hablando a un usuario concreto (user_id) en 2da persona.
    Carga datos de 'user_id' en Firebase para personalizar el contexto.
    """
    openai.api_key = get_openai_key()

    # Cargar la info del usuario desde Firestore
    user_info = get_user_data(user_id)  # dict con 'prompt', 'realtime_data', etc.

    # Construir la instrucción para ChatGPT
    system_content = f"""
    Eres Werbly, un asistente infalible y preciso.
    El usuario se llama '{user_id}' y estos son sus datos: {user_info}.
    Debes hablarle en 2da persona, refiriéndote a él como '{user_id}' cuando convenga,
    usando la información anterior para dar respuestas personalizadas.
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_input}
        ]
    )

    return response.choices[0].message["content"]


def start_loki_conversation():
    """
    Bucle interactivo que, si detecta 'loki' al inicio, usará user_id='loki'.
    Si no, usará otro user_id (p.ej. 'anon') o lo que desees para otras pruebas.
    """
    init_firebase()
    print("Firebase initialized. Ahora puedes hablar directamente como Loki o cualquier otro usuario. Escribe 'salir' para terminar.\n")

    while True:
        user_input = input("Tú: ")
        if user_input.lower() in ["salir", "exit", "quit"]:
            print("¡Hasta luego!")
            break

        # Identificar el usuario según el prefijo
        if user_input.lower().startswith("loki:"):
            user_id = "loki"
            clean_input = user_input[5:].strip()
        else:
            user_id = "anon"
            clean_input = user_input

        # Obtener respuesta personalizada de Werbly
        werbly_response = talk_as_werbly_for_user(user_id, clean_input)
        print(f"Werbly (para {user_id}):", werbly_response)

        # Guardar la conversación en Firestore
        save_message(user_id, "user", clean_input)
        save_message(user_id, "werbly", werbly_response)

        save_message(user_id, "user", clean_input)
        save_message(user_id, "werbly", werbly_response)
