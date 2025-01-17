import os
from dotenv import load_dotenv
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from huggingface_hub import login
import torch

# Cargar variables de entorno
load_dotenv()

# Obtener el token y la ruta del modelo desde las variables de entorno
HF_TOKEN = os.getenv("HF_TOKEN")
MODEL_NAME = os.getenv("LLAMA_2_MODEL_PATH", "meta-llama/Llama-2-7b-chat-hf")

# Iniciar sesión en Hugging Face utilizando el token
login(token=HF_TOKEN)

# Cargar el tokenizer y el modelo con el token de autenticación
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_auth_token=HF_TOKEN)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, use_auth_token=HF_TOKEN)

# Mover el modelo al dispositivo adecuado (CPU en tu caso)
device = torch.device("cpu")
model.to(device)

# Crear un pipeline de generación de texto
pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, device=0 if torch.cuda.is_available() else -1)

# Función para generar respuesta
def generate_response(prompt, max_length=100):
    outputs = pipe(prompt, max_length=max_length, num_return_sequences=1)
    return outputs[0]['generated_text']

# Ejemplo de uso
if __name__ == "__main__":
    prompt = "Hola, ¿cómo estás?"
    respuesta = generate_response(prompt)
    print(respuesta)
