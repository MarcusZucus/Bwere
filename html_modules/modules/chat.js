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
 * Simula una animación de escritura para mensajes del bot.
 * @param {string} role - Rol del mensaje ('user' o 'bot').
 * @param {string} content - Contenido del mensaje a escribir.
 * @param {number} speed - Velocidad de escritura en milisegundos por carácter (opcional).
 */
function typeMessage(role, content, speed = 50) {
  const messageDiv = document.createElement('div');
  messageDiv.className = `message ${role}`;
  const messageContent = document.createElement('div');
  messageContent.className = 'message-content';

  // Agregar clase no-bubble para mensajes de error del bot
  if (role === 'bot' && content.includes('Lo siento')) {
    messageContent.classList.add('no-bubble');
  }

  messageDiv.appendChild(messageContent);
  messagesContainer.appendChild(messageDiv);

  let index = 0;
  const typingInterval = setInterval(() => {
    if (index < content.length) {
      const span = document.createElement('span');
      span.textContent = content[index];
      span.style.opacity = 0;
      span.style.animation = 'fade-in 0.5s ease forwards';
      messageContent.appendChild(span);

      index++;
      messagesContainer.scrollTop = messagesContainer.scrollHeight;
    } else {
      clearInterval(typingInterval);
    }
  }, speed);
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

/**
 * Llama a la API para enviar un archivo seleccionado por el usuario.
 * @param {File} file - Archivo a enviar a la API.
 * @returns {Promise<string>} Respuesta procesada por la API.
 */
async function sendFileToApi(file) {
  try {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${apiUrl}/upload`, {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data.response;
  } catch (error) {
    console.error("Error al enviar el archivo a la API:", error);
    throw error;
  }
}

// Eventos para manejo de interacciones
sendButton.addEventListener('click', () => {
  const message = inputField.value.trim();
  if (message) {
    renderMessage('user', message);

    // Mostrar el indicador de carga
    showLoadingIndicator();

    sendMessageToApi({ message })
      .then((response) => {
        hideLoadingIndicator();
        typeMessage('bot', response);
      })
      .catch((error) => {
        hideLoadingIndicator();
        typeMessage('bot', "Lo siento, ocurrió un error al procesar tu mensaje.");
      });

    inputField.value = '';
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

      // Mostrar el indicador de carga
      showLoadingIndicator();

      sendFileToApi(file)
        .then((response) => {
          hideLoadingIndicator();
          typeMessage('bot', response);
        })
        .catch((error) => {
          hideLoadingIndicator();
          typeMessage('bot', "Lo siento, ocurrió un error al procesar tu archivo.");
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

  // Funciones para mostrar y ocultar el indicador de carga
  window.showLoadingIndicator = function() {
    const loadingIndicator = document.getElementById('loading-indicator');
    if (loadingIndicator) {
      loadingIndicator.style.display = 'flex';
    }
  };

  window.hideLoadingIndicator = function() {
    const loadingIndicator = document.getElementById('loading-indicator');
    if (loadingIndicator) {
      loadingIndicator.style.display = 'none';
    }
  };
});
