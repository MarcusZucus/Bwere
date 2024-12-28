"""
Módulo de Interacción con OpenAI.
Encapsula las llamadas a la API de ChatGPT/GPT.
"""

import openai
from modules.config import get_openai_key
from modules.prompt_manager import build_prompt, get_base_prompt

def ask_werbly(user_input):
    """
    Envía la entrada del usuario a la IA de Werbly y devuelve la respuesta.
    """
    openai.api_key = get_openai_key()
    base_prompt = get_base_prompt()  # Obtiene el prompt base desde Firestore
    final_prompt = build_prompt(user_input)  # Construye el prompt final con la entrada del usuario

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": base_prompt},  # Usa el prompt base dinámico como contexto del sistema
            {"role": "user", "content": user_input}  # La entrada del usuario directamente
        ]
    )
    return response.choices[0].message["content"]
