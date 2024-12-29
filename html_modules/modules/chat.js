export function renderMessage(role, content, messagesContainer) {
  const messageDiv = document.createElement('div');
  messageDiv.className = `message ${role}`;
  const messageContent = document.createElement('div');
  messageContent.className = 'message-content';
  messageContent.textContent = content;

  messageDiv.appendChild(messageContent);
  messagesContainer.appendChild(messageDiv);
  messagesContainer.scrollTop = messagesContainer.scrollHeight; // Auto-scroll
}

export function typeMessage(role, content, messagesContainer) {
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
      messagesContainer.scrollTop = messagesContainer.scrollHeight; // Auto-scroll
    } else {
      clearInterval(typingInterval);
    }
  }, 50);
}
