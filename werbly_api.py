from flask import Flask, request, jsonify
from modules.openai_api import ask_Bwere
from modules.firebase_connection import init_firebase
from flask_cors import CORS
import logging
import re

# Configurar logging
logging.basicConfig(
    filename='Bwere_api.log',
    level=logging.DEBUG,  # Cambiado a DEBUG para registrar más detalles
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)

# Habilitar CORS
CORS(app)

# Inicializar Firebase al arrancar
init_firebase()

def is_valid_user_id(user_id):
    """
    Verifica que el user_id sea válido.
    - Debe ser alfanumérico.
    - No debe contener caracteres especiales.
    """
    return bool(re.match(r"^[a-zA-Z0-9_-]+$", user_id))

@app.route('/')
def index():
    return "¡Bienvenido a la API de Bwere!"

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        if not data:
            logging.warning("Solicitud sin datos proporcionados.")
            return jsonify({"error": "No se proporcionaron datos en la solicitud."}), 400

        user_id = data.get("user_id", "")
        user_message = data.get("message", "")

        if not user_id or not user_message:
            logging.warning(f"Datos incompletos: user_id={user_id}, message={user_message}")
            return jsonify({"error": "No se proporcionó el ID de usuario o el mensaje."}), 400

        if not is_valid_user_id(user_id):
            logging.warning(f"Intento de uso con ID de usuario inválido: {user_id}")
            return jsonify({"error": "El ID de usuario no es válido."}), 400

        # Obtener respuesta de Bwere con historial
        response = ask_Bwere(user_id, user_message)

        logging.info(f"Respuesta generada para user_id={user_id}: {response}")
        return jsonify({"response": response})

    except ValueError as ve:
        logging.error(f"Error de valor: {ve}", exc_info=True)
        return jsonify({"error": "Datos inválidos enviados."}), 400
    except Exception as e:
        logging.critical(f"Error inesperado en la ruta /chat: {e}", exc_info=True)
        return jsonify({"error": "Ocurrió un error interno al procesar tu mensaje."}), 500

if __name__ == '__main__':
    # Ejecutar el servidor Flask
    app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == '__main__':
    # Ejecutar el servidor Flask
    app.run(debug=True, host='0.0.0.0', port=5000)
