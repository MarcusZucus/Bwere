const sendButton = document.getElementById('send-button');
const attachButton = document.getElementById('attach-button'); // Botón de adjuntar archivos
const inputField = document.getElementById('message-input');
const messagesContainer = document.getElementById('messages');

const apiUrl = "http://127.0.0.1:5000/chat"; // URL del endpoint de la API

// Evento para enviar mensajes al hacer clic en el botón de enviar
sendButton.addEventListener('click', () => {
  const message = inputField.value.trim();
  if (message) {
    renderMessage('user', message);

    // Llamar a la API para obtener la respuesta del bot
    sendMessageToApi({ message })
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

// Evento para manejar el botón de adjuntar archivos
attachButton.addEventListener('click', () => {
  const fileInput = document.createElement('input');
  fileInput.type = 'file';
  fileInput.accept = '*'; // Puedes limitar los tipos de archivos, por ejemplo: 'image/*'
  fileInput.style.display = 'none';

  // Evento para manejar la selección de archivos
  fileInput.addEventListener('change', () => {
    const file = fileInput.files[0];
    if (file) {
      renderMessage('user', `Archivo adjuntado: ${file.name}`);

      // Llamar a la API para enviar el archivo
      sendFileToApi(file)
        .then((response) => {
          typeMessage('bot', response); // Mostrar respuesta de la API
        })
        .catch((error) => {
          console.error("Error al enviar el archivo a la API:", error);
          typeMessage('bot', "Lo siento, ocurrió un error al procesar tu archivo.");
        });
    }
  });

  fileInput.click();
});

// Evento para enviar mensajes al presionar Enter
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
async function sendMessageToApi(payload) {
  try {
    const response = await fetch(apiUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    const data = await response.json();
    return data.response; // Retorna la respuesta del bot desde la API
  } catch (error) {
    console.error("Error al comunicarse con la API:", error);
    throw error; // Lanza el error para que sea manejado en la llamada
  }
}

// Función para enviar archivos a la API
async function sendFileToApi(file) {
  try {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${apiUrl}/upload`, {
      method: "POST",
      body: formData,
    });

    const data = await response.json();
    return data.response; // Retorna la respuesta del bot desde la API
  } catch (error) {
    console.error("Error al enviar el archivo a la API:", error);
    throw error; // Lanza el error para que sea manejado en la llamada
  }
}
