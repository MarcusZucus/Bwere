const menuButton = document.getElementById('menu-button');
const sidebar = document.getElementById('sidebar');
const overlay = document.createElement('div'); // Fondo oscuro para resaltar el menú
overlay.id = 'menu-overlay';
document.body.appendChild(overlay);

/**
 * Alterna la visibilidad del menú lateral con accesibilidad y transiciones avanzadas.
 */
function toggleMenu() {
  const isOpen = sidebar.classList.toggle('open');
  menuButton.classList.toggle('open');
  overlay.classList.toggle('visible', isOpen);

  // Actualizar atributos ARIA para accesibilidad
  menuButton.setAttribute('aria-expanded', isOpen);
  sidebar.setAttribute('aria-hidden', !isOpen);

  // Bloquear desplazamiento del fondo cuando el menú está abierto
  document.body.style.overflow = isOpen ? 'hidden' : '';
}

/**
 * Cierra el menú lateral si se hace clic fuera de él.
 * @param {Event} event - Evento de clic.
 */
function handleOutsideClick(event) {
  if (!sidebar.contains(event.target) && event.target !== menuButton && sidebar.classList.contains('open')) {
    toggleMenu();
  }
}

// Evento principal para abrir/cerrar el menú
menuButton.addEventListener('click', toggleMenu);

// Evento para cerrar el menú al hacer clic fuera de él
overlay.addEventListener('click', toggleMenu);

document.addEventListener('click', handleOutsideClick);

/**
 * Configuración inicial de accesibilidad y atributos del menú.
 */
document.addEventListener('DOMContentLoaded', () => {
  menuButton.setAttribute('aria-controls', 'sidebar');
  menuButton.setAttribute('aria-expanded', 'false');
  sidebar.setAttribute('aria-hidden', 'true');

  // Estilos iniciales del overlay
  overlay.style.position = 'fixed';
  overlay.style.top = '0';
  overlay.style.left = '0';
  overlay.style.width = '100%';
  overlay.style.height = '100%';
  overlay.style.backgroundColor = 'rgba(0, 0, 0, 0.5)';
  overlay.style.zIndex = '999';
  overlay.style.display = 'none';
  overlay.style.transition = 'opacity 0.3s ease';

  // Clase visible para el overlay
  overlay.classList.add('hidden');

  // Añadir estilo dinámico al mostrar el overlay
  overlay.addEventListener('transitionend', () => {
    if (!overlay.classList.contains('visible')) {
      overlay.style.display = 'none';
    }
  });

  // Mostrar overlay cuando es visible
  const observer = new MutationObserver(() => {
    if (overlay.classList.contains('visible')) {
      overlay.style.display = 'block';
      requestAnimationFrame(() => {
        overlay.style.opacity = '1';
      });
    } else {
      overlay.style.opacity = '0';
    }
  });

  observer.observe(overlay, { attributes: true, attributeFilter: ['class'] });
});
