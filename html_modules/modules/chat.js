const sendButton = document.getElementById('send-button');
const attachButton = document.getElementById('attach-button');
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

  // Clase especial para errores del bot
  if (role === 'bot' && content.includes('Lo siento')) {
    messageContent.classList.add('no-bubble');
  }

  messageContent.textContent = content;
  messageDiv.appendChild(messageContent);
  messagesContainer.appendChild(messageDiv);
  messagesContainer.scrollTop = messagesContainer.scrollHeight;
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
 * Muestra la animación ECG antes del mensaje del bot usando un template precargado.
 * @param {string} message - Contenido del mensaje del bot.
 */
function displayECGAnimationAndMessage(message) {
  const template = document.getElementById('ecg-template');
  if (!template) {
    console.error('Plantilla ECG no encontrada.');
    typeMessage('bot', message);
    return;
  }

  const animationContainer = template.content.cloneNode(true).firstElementChild;
  animationContainer.style.transition = 'opacity 1s ease-in-out';
  animationContainer.style.opacity = '1';

  messagesContainer.appendChild(animationContainer);

  setTimeout(() => {
    animationContainer.style.opacity = '0';
    setTimeout(() => {
      animationContainer.remove();
      typeMessage('bot', message);
    }, 1000);
  }, 3000);
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

sendButton.addEventListener('click', () => {
  const message = inputField.value.trim();
  if (message) {
    renderMessage('user', message);

    sendMessageToApi({ message })
      .then((response) => {
        displayECGAnimationAndMessage(response);
      })
      .catch(() => {
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

      sendFileToApi(file)
        .then((response) => {
          displayECGAnimationAndMessage(response);
        })
        .catch(() => {
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

document.addEventListener('DOMContentLoaded', () => {
  inputField.setAttribute('aria-label', 'Escribe tu mensaje');
  sendButton.setAttribute('aria-label', 'Enviar mensaje');
  attachButton.setAttribute('aria-label', 'Adjuntar archivo');
});
