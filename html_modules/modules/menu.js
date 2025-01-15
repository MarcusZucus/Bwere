// Obtener referencias a los elementos del DOM
const menuButton = document.getElementById('menu-button');
const sidebar = document.getElementById('sidebar');
const overlay = document.createElement('div');
const menuItems = document.querySelectorAll('.menu-item'); // Asegúrate de que cada item tenga la clase 'menu-item'

// Configuración del overlay (pantalla oscura que aparece cuando el menú está abierto)
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

  // Alternar la clase 'open' para los elementos del menú
  menuItems.forEach((item) => item.classList.toggle('open', isOpen));
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
  // Asegurar la configuración de los atributos ARIA en el botón del menú
  menuButton.setAttribute('aria-controls', 'sidebar');
  menuButton.setAttribute('aria-expanded', 'false');
  sidebar.setAttribute('aria-hidden', 'true');

  // Estilos iniciales del overlay
  Object.assign(overlay.style, {
    position: 'fixed',
    top: '0',
    left: '0',
    width: '100%',
    height: '100%',
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    zIndex: '999',
    display: 'none',
    opacity: '0',
    transition: 'opacity 0.3s ease',
  });

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

  // Configuración inicial del sidebar (abre desde la derecha y ocupa más espacio)
  Object.assign(sidebar.style, {
    position: 'fixed',
    top: '0',
    right: '-80%', // Oculto inicialmente
    width: '80%', // Ocupa el 80% de la pantalla
    height: '100%',
    backgroundColor: '#fff',
    boxShadow: '-4px 0 10px rgba(0, 0, 0, 0.2)',
    zIndex: '1000',
    transition: 'right 0.3s ease',
  });

  // Estilo para el menú cuando está abierto
  sidebar.classList.add('closed');
});

/**
 * Función para aplicar animaciones al abrir/cerrar el menú.
 * Este puede ser útil para la transición suave de los elementos dentro del menú.
 */
function animateMenuItems() {
  menuItems.forEach((item, index) => {
    item.style.transition = `transform 0.3s ease ${index * 0.1}s`;
    item.style.transform = 'translateX(0)';
  });
}

// Llamar a la función de animación solo cuando el menú se abra
sidebar.addEventListener('transitionend', () => {
  if (sidebar.classList.contains('open')) {
    animateMenuItems();
  }
});

/**
 * Función para activar/desactivar un menú secundario (por ejemplo, para sub-opciones dentro de las categorías).
 * Esto puede ser utilizado si decides expandir las opciones dentro del menú (por ejemplo, opciones dentro de "Mi Plan de Bienestar").
 */
function toggleSubMenu(subMenuId) {
  const subMenu = document.getElementById(subMenuId);
  if (subMenu) {
    subMenu.classList.toggle('open');
  }
}

// Estilo para las clases dinámicas
const style = document.createElement('style');
style.innerHTML = `
  #sidebar.open {
    right: 0;
  }

  #menu-overlay.visible {
    display: block;
  }

  .menu-item {
    transform: translateX(-100%);
  }
`;
document.head.appendChild(style);
