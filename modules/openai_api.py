"""
Módulo de Interacción con OpenAI.
Encapsula las llamadas a la API de ChatGPT/GPT.
"""

import openai
from modules.config import get_openai_key
from modules.prompt_manager import build_prompt

def ask_werbly(user_input):
    """
    Envía la entrada del usuario a la IA de Werbly y devuelve la respuesta.
    """
    openai.api_key = get_openai_key()
    final_prompt = build_prompt(user_input)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Eres Werbly, la IA infalible..."},
            {"role": "user", "content": final_prompt}
        ]
    )
    return response.choices[0].message["content"]
