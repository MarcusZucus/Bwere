/**
 * Aplica un efecto de desvanecimiento a un elemento.
 * @param {HTMLElement} element - El elemento al que se aplicará el efecto.
 * @param {number} duration - Duración de la animación en milisegundos.
 * @param {Function} [callback] - Función opcional a ejecutar tras completar la animación.
 */
export function fadeIn(element, duration = 500, callback = null) {
  if (!element) return;

  element.style.opacity = 0;
  element.style.transition = `opacity ${duration}ms ease-in-out`;
  requestAnimationFrame(() => {
    element.style.opacity = 1;
    setTimeout(() => {
      if (typeof callback === 'function') callback();
    }, duration);
  });
}

/**
 * Aplica un efecto de escritura letra por letra a un mensaje con soporte para animación.
 * @param {HTMLElement} messageContent - Contenedor del mensaje.
 * @param {string} content - El texto que se va a escribir.
 * @param {number} speed - Velocidad de escritura en milisegundos por carácter.
 * @param {Function} [callback] - Función opcional a ejecutar tras completar la escritura.
 */
export function typeMessageEffect(messageContent, content, speed = 24, callback = null) {
  if (!messageContent || typeof content !== 'string') return;

  let index = 0;
  const typingInterval = setInterval(() => {
    if (index < content.length) {
      const span = document.createElement('span');
      span.textContent = content[index];
      span.style.opacity = 0;
      span.style.animation = 'fade-in 0.1s ease forwards';
      messageContent.appendChild(span);
      index++;
    } else {
      clearInterval(typingInterval);
      if (typeof callback === 'function') callback();
    }
  }, speed);
}

/**
 * Aplica un efecto de apertura/cierre animado para un menú lateral con accesibilidad.
 * @param {HTMLElement} menuButton - Botón que activa el menú.
 * @param {HTMLElement} sidebar - Menú lateral a mostrar/ocultar.
 */
export function toggleMenuAnimation(menuButton, sidebar) {
  if (!menuButton || !sidebar) return;

  const isOpen = sidebar.classList.toggle('open');
  menuButton.classList.toggle('open');

  // Actualiza atributos ARIA para accesibilidad
  menuButton.setAttribute('aria-expanded', isOpen);
  sidebar.setAttribute('aria-hidden', !isOpen);

  // Agregar transición suave con transformaciones CSS para un mejor rendimiento
  if (isOpen) {
    sidebar.style.transform = 'translateX(0)';
  } else {
    sidebar.style.transform = 'translateX(-100%)';
  }
}

/**
 * Agrega eventos globales para cerrar el menú si se hace clic fuera de él.
 * @param {HTMLElement} menuButton - Botón que activa el menú.
 * @param {HTMLElement} sidebar - Menú lateral a gestionar.
 */
export function setupOutsideClickHandler(menuButton, sidebar) {
  if (!menuButton || !sidebar) return;

  document.addEventListener('click', (event) => {
    const target = event.target;
    if (!sidebar.contains(target) && target !== menuButton && sidebar.classList.contains('open')) {
      toggleMenuAnimation(menuButton, sidebar);
    }
  });
}
