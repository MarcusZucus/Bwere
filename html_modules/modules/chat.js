const sendButton = document.getElementById('send-button');
const attachButton = document.getElementById('attach-button'); // Botón de adjuntar archivos
const inputField = document.getElementById('message-input');
const messagesContainer = document.getElementById('messages');

const apiUrl = "http://127.0.0.1:5000/chat"; // URL del endpoint de la API

/**
 * Agrega un mensaje al contenedor de mensajes con soporte para accesibilidad y diseño responsivo.
 * @param {string} role - Rol del mensaje ('user' o 'bot').
 * @param {string} content - Contenido del mensaje a renderizar.
 * @param {boolean} animate - Define si el mensaje debe mostrarse con animación de texto.
 */
function renderMessage(role, content, animate = false) {
  const messageDiv = document.createElement('div');
  messageDiv.className = `message ${role}`;
  const messageContent = document.createElement('div');
  messageContent.className = 'message-content';
  messageContent.style.minHeight = '70px'; // Ajusta la altura mínima para evitar cortes en el contenido

  if (animate) {
    typeText(messageContent, content);
  } else {
    messageContent.textContent = content;
  }

  messageDiv.appendChild(messageContent);
  messagesContainer.appendChild(messageDiv);
  messagesContainer.scrollTop = messagesContainer.scrollHeight; // Scroll automático
}

/**
 * Muestra el contenido del texto carácter por carácter.
 * @param {HTMLElement} element - Elemento donde se mostrará el texto.
 * @param {string} text - Texto a mostrar.
 * @param {number} speed - Velocidad de escritura (en milisegundos por carácter).
 */
function typeText(element, text, speed = 50) {
  let index = 0;
  const interval = setInterval(() => {
    if (index < text.length) {
      element.textContent += text[index];
      index++;
      messagesContainer.scrollTop = messagesContainer.scrollHeight; // Mantener el scroll al final
    } else {
      clearInterval(interval);
    }
  }, speed);
}

/**
 * Muestra la animación de carga desde el archivo Fading_Line_ECG (2).html.
 * La animación se renderiza como un `message-content` para respetar las mismas dimensiones.
 */
function showLoadingAnimation() {
  const messageDiv = document.createElement('div');
  messageDiv.className = 'message bot'; // Asegura que tenga la misma estructura de un mensaje del bot

  const loadingAnimation = document.createElement('div');
  loadingAnimation.className = 'message-content'; // Mantiene las mismas dimensiones y estilos del contenedor de mensajes
  loadingAnimation.style.minHeight = '70px'; // Altura mínima para que el corazón no se corte
  loadingAnimation.style.display = 'flex';
  loadingAnimation.style.justifyContent = 'center';
  loadingAnimation.style.alignItems = 'center';

  const iframe = document.createElement('iframe');
  iframe.src = '/Fading_Line_ECG (2).html'; // Ruta relativa desde la raíz del proyecto
  iframe.style.border = 'none';
  iframe.style.width = '100%';
  iframe.style.height = '100%'; // Se ajusta dinámicamente al contenedor
  iframe.style.overflow = 'hidden';

  loadingAnimation.appendChild(iframe);
  messageDiv.appendChild(loadingAnimation);
  messagesContainer.appendChild(messageDiv);
  messagesContainer.scrollTop = messagesContainer.scrollHeight; // Asegura el scroll al último mensaje
}

/**
 * Elimina la animación de carga (iframe).
 */
function removeLoadingAnimation() {
  const loadingAnimation = document.querySelector('.message.bot .message-content iframe');
  if (loadingAnimation) {
    loadingAnimation.parentElement.parentElement.remove();
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

    // Espera 3 segundos antes de eliminar la animación y mostrar el mensaje
    setTimeout(() => {
      sendMessageToApi({ message })
        .then((response) => {
          removeLoadingAnimation(); // Quita la animación de carga
          renderMessage('bot', response, true); // Renderiza la respuesta del bot con animación
        })
        .catch(() => {
          removeLoadingAnimation(); // Quita la animación de carga
          renderMessage('bot', "Lo siento, ocurrió un error al procesar tu mensaje.", true);
        });
    }, 3000);

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
      showLoadingAnimation(); // Muestra la animación de carga

      // Espera 3 segundos antes de eliminar la animación y mostrar el mensaje
      setTimeout(() => {
        sendFileToApi(file)
          .then((response) => {
            removeLoadingAnimation(); // Quita la animación de carga
            renderMessage('bot', response, true); // Renderiza la respuesta del bot con animación
          })
          .catch(() => {
            removeLoadingAnimation(); // Quita la animación de carga
            renderMessage('bot', "Lo siento, ocurrió un error al procesar tu archivo.", true);
          });
      }, 3000);
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
