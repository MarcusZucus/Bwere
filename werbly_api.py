from flask import Flask, request, jsonify
from modules.openai_api import ask_werbly
from modules.firebase_connection import init_firebase
from flask_cors import CORS

app = Flask(__name__)

# Habilitar CORS
CORS(app)

# Inicializar Firebase al arrancar
init_firebase()

@app.route('/')
def index():
    return "¡Bienvenido a la API de Werbly!"

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No se proporcionaron datos en la solicitud."}), 400
        
        user_message = data.get("message", "")
        if not user_message:
            return jsonify({"error": "No se proporcionó ningún mensaje."}), 400

        # Obtener respuesta de Werbly
        response = ask_werbly(user_message)

        return jsonify({"response": response})

    except Exception as e:
        # Registrar el error y devolver un mensaje de error al cliente
        print(f"Error en la ruta /chat: {e}")
        return jsonify({"error": "Ocurrió un error al procesar tu mensaje."}), 500

if __name__ == '__main__':
    # Ejecutar el servidor Flask
    app.run(debug=True, host='0.0.0.0', port=5000)
