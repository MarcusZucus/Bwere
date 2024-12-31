/**
 * Aplica un efecto de desvanecimiento a un elemento.
 * @param {HTMLElement} element - El elemento al que se aplicará el efecto.
 * @param {number} duration - Duración de la animación en milisegundos.
 */
export function fadeIn(element, duration = 500) {
  element.style.opacity = 0;
  element.style.transition = `opacity ${duration}ms ease-in-out`;
  setTimeout(() => {
    element.style.opacity = 1;
  }, 10);
}

/**
 * Aplica un efecto de escritura letra por letra a un mensaje.
 * @param {HTMLElement} messageContent - Contenedor del mensaje.
 * @param {string} content - El texto que se va a escribir.
 * @param {number} speed - Velocidad de escritura en milisegundos por carácter.
 */
export function typeMessageEffect(messageContent, content, speed = 24) {
  let index = 0;

  const typingInterval = setInterval(() => {
    if (index < content.length) {
      const span = document.createElement('span');
      span.textContent = content[index];
      span.style.opacity = 0;
      span.style.animation = 'fade-in 0.1s ease forwards'; // Aplicar animación de desvanecimiento
      messageContent.appendChild(span);
      index++;
    } else {
      clearInterval(typingInterval);
    }
  }, speed);
}

/**
 * Aplica un efecto de apertura/cierre animado para un menú lateral.
 * @param {HTMLElement} menuButton - Botón que activa el menú.
 * @param {HTMLElement} sidebar - Menú lateral a mostrar/ocultar.
 */
export function toggleMenuAnimation(menuButton, sidebar) {
  sidebar.classList.toggle('open');
  menuButton.classList.toggle('open');
}
