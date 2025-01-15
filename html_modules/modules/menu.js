// Obtener referencias a los elementos del DOM
const menuButton = document.getElementById('menu-button');
const sidebar = document.getElementById('sidebar');
const overlay = document.createElement('div');
const menuItems = document.querySelectorAll('.menu-item'); // Cada elemento debe tener la clase 'menu-item'

// Configuración del overlay
overlay.id = 'menu-overlay';
document.body.appendChild(overlay);

/**
 * Alterna la visibilidad del menú lateral.
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

  // Animar elementos del menú cuando se abra
  if (isOpen) {
    animateMenuItems();
  }
}

/**
 * Cierra el menú si se hace clic fuera de él.
 */
function handleOutsideClick(event) {
  if (!sidebar.contains(event.target) && event.target !== menuButton && sidebar.classList.contains('open')) {
    toggleMenu();
  }
}

// Evento principal para abrir/cerrar el menú
menuButton.addEventListener('click', toggleMenu);

// Evento para cerrar el menú al hacer clic fuera
overlay.addEventListener('click', toggleMenu);
document.addEventListener('click', handleOutsideClick);

/**
 * Configuración inicial y estilos del overlay.
 */
document.addEventListener('DOMContentLoaded', () => {
  // Configurar atributos ARIA iniciales
  menuButton.setAttribute('aria-controls', 'sidebar');
  menuButton.setAttribute('aria-expanded', 'false');
  sidebar.setAttribute('aria-hidden', 'true');

  // Estilo inicial del overlay
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

  overlay.classList.add('hidden');

  overlay.addEventListener('transitionend', () => {
    if (!overlay.classList.contains('visible')) {
      overlay.style.display = 'none';
    }
  });

  // Observar cambios en la clase 'visible' del overlay
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

/**
 * Aplica animaciones suaves a los elementos del menú.
 */
function animateMenuItems() {
  menuItems.forEach((item, index) => {
    item.style.transition = `transform 0.3s ease ${index * 0.1}s, opacity 0.3s ease ${index * 0.1}s`;
    item.style.transform = 'translateX(0)';
    item.style.opacity = '1';
  });
}

/**
 * Inicializa los estilos de los elementos del menú para las animaciones.
 */
menuItems.forEach(item => {
  item.style.transform = 'translateX(-20px)';
  item.style.opacity = '0';
});

/**
 * Expande o colapsa un submenú dentro del menú lateral.
 * @param {string} subMenuId - El ID del submenú a alternar.
 */
function toggleSubMenu(subMenuId) {
  const subMenu = document.getElementById(subMenuId);
  if (subMenu) {
    subMenu.classList.toggle('open');
    subMenu.setAttribute('aria-hidden', !subMenu.classList.contains('open'));
  }
}

/**
 * Maneja el clic en los elementos del menú para garantizar que no se bloquee la navegación predeterminada.
 */
menuItems.forEach(item => {
  item.addEventListener('click', event => {
    const href = item.getAttribute('href');
    if (href) {
      console.log('Clic en enlace:', href);
      if (href.startsWith('/')) {
        // Permitir la redirección predeterminada
        window.location.href = href;
      } else {
        console.warn('Elemento sin enlace válido:', item);
      }
    } else {
      console.error('Este elemento no tiene un enlace asociado:', item);
    }
  });
});
