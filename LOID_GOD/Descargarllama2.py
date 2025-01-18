from transformers import AutoModelForCausalLM, AutoTokenizer

# Nombre del modelo
model_name = "meta-llama/Llama-2-7b-chat-hf"

# Descarga del modelo y el tokenizer
print("Descargando el modelo y tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(model_name, use_auth_token=True)
model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto", use_auth_token=True)

print("¡Modelo y tokenizer descargados exitosamente!")
