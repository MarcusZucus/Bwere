const sendButton = document.getElementById('send-button');
const attachButton = document.getElementById('attach-button'); // Botón de adjuntar archivos
const inputField = document.getElementById('message-input');
const messagesContainer = document.getElementById('messages');

const apiUrl = "http://127.0.0.1:5000/chat"; // URL del endpoint de la API
const fadingLineUrl = "/Fading_Line_ECG.html"; // Ruta al archivo HTML de la animación

/**
 * Carga el contenido HTML desde una URL y lo inserta en el DOM.
 * @param {string} url - URL del archivo HTML.
 * @returns {Promise<string>} - Contenido del archivo HTML.
 */
async function loadHtmlFromUrl(url) {
  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`Error al cargar el archivo HTML: ${response.status}`);
    }
    return await response.text();
  } catch (error) {
    console.error("Error al cargar el HTML:", error);
    return "<div>Error al cargar el indicador de carga</div>"; // Mensaje de fallback
  }
}

/**
 * Muestra el indicador de carga en el contenedor de mensajes.
 */
async function showLoadingIndicator() {
  const loadingIndicator = document.createElement("div");
  loadingIndicator.className = "message bot"; // Clase de mensaje del bot
  loadingIndicator.id = "loading-indicator"; // ID para identificarlo

  const htmlContent = await loadHtmlFromUrl(fadingLineUrl); // Cargar el HTML de la animación
  loadingIndicator.innerHTML = htmlContent;

  messagesContainer.appendChild(loadingIndicator);
  messagesContainer.scrollTop = messagesContainer.scrollHeight; // Asegura el scroll hacia abajo
}

/**
 * Oculta el indicador de carga eliminándolo del DOM.
 */
function hideLoadingIndicator() {
  const loadingIndicator = document.getElementById("loading-indicator");
  if (loadingIndicator) {
    loadingIndicator.remove();
  }
}

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
sendButton.addEventListener('click', async () => {
  const message = inputField.value.trim();
  if (message) {
    renderMessage('user', message);

    // Mostrar el indicador de carga
    await showLoadingIndicator();

    sendMessageToApi({ message })
      .then((response) => {
        hideLoadingIndicator();
        typeMessage('bot', response);
      })
      .catch(() => {
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
        .catch(() => {
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
});
