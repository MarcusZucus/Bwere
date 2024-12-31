const sendButton = document.getElementById('send-button');
const inputField = document.getElementById('message-input');
const messagesContainer = document.getElementById('messages');

const apiUrl = "http://127.0.0.1:5000/chat"; // URL del endpoint de la API

sendButton.addEventListener('click', () => {
  const message = inputField.value.trim();
  if (message) {
    renderMessage('user', message);

    // Llamar a la API para obtener la respuesta del bot
    sendMessageToApi(message)
      .then((response) => {
        typeMessage('bot', response); // Mostrar respuesta de la API
      })
      .catch((error) => {
        console.error("Error al comunicarse con la API:", error);
        typeMessage('bot', "Lo siento, ocurrió un error al procesar tu mensaje.");
      });

    inputField.value = '';
  }
});

inputField.addEventListener('keypress', (event) => {
  if (event.key === 'Enter') {
    sendButton.click();
  }
});

// Renderizar mensajes instantáneamente en el chat
function renderMessage(role, content) {
  const messageDiv = document.createElement('div');
  messageDiv.className = `message ${role}`;
  const messageContent = document.createElement('div');
  messageContent.className = 'message-content';
  messageContent.textContent = content;

  messageDiv.appendChild(messageContent);
  messagesContainer.appendChild(messageDiv);
  messagesContainer.scrollTop = messagesContainer.scrollHeight; // Scroll automático
}

// Simular animación de escritura para mensajes del bot
function typeMessage(role, content) {
  const messageDiv = document.createElement('div');
  messageDiv.className = `message ${role}`;
  const messageContent = document.createElement('div');
  messageContent.className = 'message-content';
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
  }, 50);
}

// Función para enviar mensajes a la API
async function sendMessageToApi(message) {
  try {
    const response = await fetch(apiUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message }),
    });

    const data = await response.json();
    return data.response; // Retorna la respuesta del bot desde la API
  } catch (error) {
    console.error("Error al comunicarse con la API:", error);
    throw error; // Lanza el error para que sea manejado en la llamada
  }
}


