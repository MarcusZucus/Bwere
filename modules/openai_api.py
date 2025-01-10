import openai
from modules.config import get_openai_key
from modules.conversation_manager import save_message, get_conversation_history
from modules.firebase_connection import get_firestore_client

def get_base_prompt():
    """
    Recupera el prompt base desde Firestore para usarlo como contexto del sistema.
    """
    db = get_firestore_client()
    doc_ref = db.collection("prompts").document("prompt_usuario")
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict().get("contenido", "No se encontró el prompt base.")
    else:
        return "No se encontró el prompt base."

def ask_werbly(user_id, user_input):
    """
    Envía la entrada del usuario a la IA de Werbly junto con el historial de conversación y devuelve la respuesta.
    Maneja errores de límites de tokens y problemas de red.
    """
    openai.api_key = get_openai_key()

    # Recuperar el prompt base desde Firestore
    base_prompt = get_base_prompt()

    # Recuperar el historial completo de la conversación
    conversation_history = get_conversation_history(user_id)

    # Agregar el mensaje actual del usuario al historial
    conversation_history.append({"role": "user", "content": user_input})

    # Construir el contexto completo para la IA
    messages = [{"role": "system", "content": base_prompt}] + conversation_history

    try:
        # Enviar el historial completo a la IA
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
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
            messages = [
                {"role": "system", "content": base_prompt},
                {"role": "system", "content": "Resumen del contexto previo: " + summarized_history},
                {"role": "user", "content": user_input}
            ]

            # Reintentar la solicitud con el historial resumido
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
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
