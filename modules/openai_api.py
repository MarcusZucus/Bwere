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
    Maneja errores de límites de tokens y problemas de red.
    """
    openai.api_key = get_openai_key()

    # Recuperar el historial completo de la conversación
    conversation_history = get_conversation_history(user_id)

    # Agregar el mensaje actual del usuario al historial
    conversation_history.append({"role": "user", "content": user_input})

    try:
        # Enviar el historial completo a la IA
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=conversation_history,
            max_tokens=1000  # Límite para la respuesta
        )

        # Obtener la respuesta generada por la IA
        assistant_message = response["choices"][0]["message"]["content"]

        # Guardar la respuesta de la IA en Firestore
        save_message(user_id, "assistant", assistant_message)

        return assistant_message

    except openai.error.InvalidRequestError as e:
        # Manejar errores relacionados con límites de tokens
        if "maximum context length" in str(e):
            # Resumir historial si supera los límites
            summarized_history = summarize_history(conversation_history)
            conversation_history = [{"role": "system", "content": "Resumen del contexto previo: " + summarized_history}]
            conversation_history.append({"role": "user", "content": user_input})

            # Reintentar la solicitud con el historial resumido
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=conversation_history,
                max_tokens=1000
            )

            assistant_message = response["choices"][0]["message"]["content"]
            save_message(user_id, "assistant", assistant_message)
            return assistant_message
        else:
            raise e

    except openai.error.OpenAIError as e:
        # Manejar errores generales de OpenAI
        return "Lo siento, hubo un problema al procesar tu solicitud. Por favor, intenta nuevamente."

    except Exception as e:
        # Manejar otros errores
        return f"Ocurrió un error inesperado: {str(e)}"

def summarize_history(conversation_history):
    """
    Resume el historial completo en una breve descripción.
    """
    user_messages = [h["content"] for h in conversation_history if h["role"] == "user"]
    return " ".join(user_messages[-5:])  # Toma las últimas 5 entradas del usuario como resumen
