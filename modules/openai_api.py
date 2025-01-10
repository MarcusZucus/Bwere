"""
Módulo de Interacción con OpenAI.
Encapsula las llamadas a la API de ChatGPT/GPT.
"""

import openai
from modules.config import get_openai_key
from modules.conversation_manager import save_message, get_conversation_history

def ask_werbly(user_id, user_input):
    """
    Envía la entrada del usuario a la IA de Werbly junto con el historial de conversación y devuelve la respuesta.
    """
    openai.api_key = get_openai_key()

    # Recuperar el historial completo de la conversación
    conversation_history = get_conversation_history(user_id)

    # Agregar el mensaje actual del usuario al historial
    conversation_history.append({"role": "user", "content": user_input})

    # Enviar el historial completo a la IA
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=conversation_history
    )

    # Obtener la respuesta generada por la IA
    assistant_message = response["choices"][0]["message"]["content"]

    # Guardar la respuesta de la IA en Firestore
    save_message(user_id, "assistant", assistant_message)

    return assistant_message
