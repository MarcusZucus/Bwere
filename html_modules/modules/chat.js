const sendButton = document.getElementById('send-button');
const attachButton = document.getElementById('attach-button'); // Botón de adjuntar archivos
const inputField = document.getElementById('message-input');
const messagesContainer = document.getElementById('messages');

const apiUrl = "http://127.0.0.1:5000/chat"; // URL del endpoint de la API

/**
 * Agrega un mensaje al contenedor de mensajes con soporte para accesibilidad y diseño responsivo.
 * @param {string} role - Rol del mensaje ('user' o 'bot').
 * @param {string} content - Contenido del mensaje a renderizar.
 */
function renderMessage(role, content) {
  const messageDiv = document.createElement('div');
  messageDiv.className = `message ${role}`;
  const messageContent = document.createElement('div');
  messageContent.className = 'message-content';

  // Agregar clase no-bubble para mensajes de error del bot
  if (role === 'bot' && content.includes('Lo siento')) {
    messageContent.classList.add('no-bubble');
  }

  messageContent.textContent = content;
  messageDiv.appendChild(messageContent);
  messagesContainer.appendChild(messageDiv);
  messagesContainer.scrollTop = messagesContainer.scrollHeight; // Scroll automático
}

/**
 * Muestra una animación de carga (ECG) mientras se procesa el mensaje.
 */
function showLoadingAnimation() {
  const animationContainer = document.createElement('div');
  animationContainer.className = 'animation-container';
  animationContainer.innerHTML = `
    <div class="heart"></div>
    <style>
      .animation-container {
        position: relative;
        width: 400px;
        height: 200px;
        margin: 10px auto;
      }
      .heart {
        position: absolute;
        width: 30px;
        height: 30px;
        background-color: #EEEEEE;
        left: 50%;
        top: 50%;
        transform: translate(-50%, -50%) rotate(45deg);
        animation: pulse 1.5s infinite, colorShift 1.5s infinite;
      }
      .heart:before, .heart:after {
        content: '';
        position: absolute;
        width: 30px;
        height: 30px;
        background-color: #EEEEEE;
        border-radius: 50%;
        top: -15px;
        left: 0;
      }
      .heart:after {
        left: 15px;
        top: 0;
      }
      @keyframes pulse {
        0%, 100% {
          transform: translate(-50%, -50%) scale(1);
        }
        50% {
          transform: translate(-50%, -50%) scale(1.2);
        }
      }
      @keyframes colorShift {
        0%, 100% {
          background-color: #EEEEEE;
        }
        50% {
          background-color: #F76E6E;
        }
      }
    </style>
  `;
  messagesContainer.appendChild(animationContainer);
}

/**
 * Elimina la animación de carga (ECG).
 */
function removeLoadingAnimation() {
  const animation = document.querySelector('.animation-container');
  if (animation) {
    messagesContainer.removeChild(animation);
  }
}

/**
 * Llama a la API para obtener una respuesta basada en un mensaje enviado por el usuario.
 * @param {Object} payload - Datos a enviar a la API.
 * @returns {Promise<string>} Respuesta procesada por la API.
 */
async function sendMessageToApi(payload) {
  try {
    const response = await fetch(apiUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data.response;
  } catch (error) {
    console.error("Error al comunicarse con la API:", error);
    throw error;
  }
}

// Eventos para manejo de interacciones
sendButton.addEventListener('click', () => {
  const message = inputField.value.trim();
  if (message) {
    renderMessage('user', message); // Renderiza el mensaje del usuario
    showLoadingAnimation(); // Muestra la animación de carga

    sendMessageToApi({ message })
      .then((response) => {
        removeLoadingAnimation(); // Quita la animación de carga
        renderMessage('bot', response); // Renderiza la respuesta del bot
      })
      .catch(() => {
        removeLoadingAnimation(); // Quita la animación en caso de error
        renderMessage('bot', "Lo siento, ocurrió un error al procesar tu mensaje.");
      });

    inputField.value = ''; // Limpia el campo de entrada
  }
});

attachButton.addEventListener('click', () => {
  const fileInput = document.createElement('input');
  fileInput.type = 'file';
  fileInput.accept = '*';
  fileInput.style.display = 'none';

  fileInput.addEventListener('change', () => {
    const file = fileInput.files[0];
    if (file) {
      renderMessage('user', `Archivo adjuntado: ${file.name}`);

      sendFileToApi(file)
        .then((response) => {
          renderMessage('bot', response);
        })
        .catch(() => {
          renderMessage('bot', "Lo siento, ocurrió un error al procesar tu archivo.");
        });
    }
  });

  fileInput.click();
});

inputField.addEventListener('keypress', (event) => {
  if (event.key === 'Enter') {
    sendButton.click();
  }
});

/**
 * Agrega accesibilidad y seguridad mejorada para eventos globales.
 */
document.addEventListener('DOMContentLoaded', () => {
  inputField.setAttribute('aria-label', 'Escribe tu mensaje');
  sendButton.setAttribute('aria-label', 'Enviar mensaje');
  attachButton.setAttribute('aria-label', 'Adjuntar archivo');
});
