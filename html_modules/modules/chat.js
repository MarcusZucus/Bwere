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
 * Muestra la animación de Fading_Line_ECG_2.html antes del mensaje del bot.
 * Ocupa el mismo espacio que message-content-no-bubble.
 * @param {string} message - Contenido del mensaje del bot.
 */
function displayECGAnimationAndMessage(message) {
  // Crear un contenedor para la animación
  const animationContainer = document.createElement('div');
  animationContainer.id = 'ecg-animation-container';
  animationContainer.className = 'message-content'; // Alinea con el estilo de message-content
  animationContainer.style.display = 'flex';
  animationContainer.style.alignItems = 'center';
  animationContainer.style.justifyContent = 'center';
  animationContainer.style.height = 'auto';
  animationContainer.style.overflow = 'hidden';
  animationContainer.style.transition = 'opacity 1s ease-in-out';
  animationContainer.style.opacity = '1'; // Visible inicialmente

  // Cargar el contenido de Fading_Line_ECG_2.html
  fetch('Fading_Line_ECG_2.html')
    .then(response => {
      if (!response.ok) {
        throw new Error(`Error al cargar la animación: ${response.statusText}`);
      }
      return response.text();
    })
    .then(html => {
      animationContainer.innerHTML = html;
      messagesContainer.appendChild(animationContainer);

      // Desvanecer la animación después de 3 segundos
      setTimeout(() => {
        animationContainer.style.opacity = '0';
        setTimeout(() => {
          animationContainer.remove(); // Eliminar la animación
          typeMessage('bot', message); // Mostrar el mensaje del bot
        }, 1000); // Tiempo para el efecto fade-out
      }, 3000);
    })
    .catch(error => console.error('Error al cargar la animación:', error));
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

    sendMessageToApi({ message })
      .then((response) => {
        displayECGAnimationAndMessage(response);
      })
      .catch((error) => {
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
        .catch((error) => {
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
});
