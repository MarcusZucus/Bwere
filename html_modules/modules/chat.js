const sendButton = document.getElementById('send-button');
const inputField = document.getElementById('message-input');
const messagesContainer = document.getElementById('messages');

sendButton.addEventListener('click', () => {
  const message = inputField.value.trim();
  if (message) {
    renderMessage('user', message);

    // Simulación de respuesta del bot con animación de escritura
    setTimeout(() => {
      typeMessage('bot', `Esto es una respuesta a: "${message}"`);
    }, 1000);

    inputField.value = '';
  }
});

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
