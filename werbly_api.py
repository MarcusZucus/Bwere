from flask import Flask, request, jsonify
from modules.openai_api import ask_werbly
from modules.firebase_connection import init_firebase

app = Flask(__name__)

# Inicializar Firebase al arrancar
init_firebase()

@app.route('/')
def index():
    return "¡Bienvenido a la API de Werbly!"

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    
    if not user_message:
        return jsonify({"error": "No se proporcionó ningún mensaje."}), 400

    # Obtener respuesta de Werbly
    response = ask_werbly(user_message)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
