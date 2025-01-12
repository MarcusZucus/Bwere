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
 * Muestra la animación de carga desde el archivo Fading_Line_ECG (2).html.
 */
function showLoadingAnimation() {
  const iframe = document.createElement('iframe');
  iframe.src = '/Fading_Line_ECG (2).html'; // Ruta relativa desde la raíz del proyecto
  iframe.className = 'loading-animation';
  iframe.style.border = 'none';
  iframe.style.width = '100%';
  iframe.style.height = '200px';
  iframe.style.overflow = 'hidden';

  messagesContainer.appendChild(iframe);

  // Elimina la animación automáticamente después de 3 segundos
  setTimeout(() => {
    removeLoadingAnimation();
  }, 3000);
}

/**
 * Elimina la animación de carga (iframe).
 */
function removeLoadingAnimation() {
  const iframe = document.querySelector('.loading-animation');
  if (iframe) {
    messagesContainer.removeChild(iframe);
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
        renderMessage('bot', response); // Renderiza la respuesta del bot
      })
      .catch(() => {
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
