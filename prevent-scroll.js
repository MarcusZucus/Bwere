// Previene la recarga por arrastre hacia abajo en móviles
document.addEventListener(
  "touchmove",
  function (event) {
    if (event.touches.length > 1) {
      event.preventDefault();
    }
  },
  { passive: false }
);

// Previene la recarga accidental al navegar fuera de la página
window.addEventListener("beforeunload", (e) => {
  e.preventDefault();
  e.returnValue = "";
});

// Ajusta el comportamiento del encabezado para evitar que desaparezca con el teclado
window.addEventListener("resize", () => {
  const header = document.getElementById("chat-header");
  const chatContainer = document.getElementById("chat-container");
  const messages = document.getElementById("messages");

  // Detecta si el teclado está abierto comparando la altura de la ventana
  if (window.innerHeight < window.outerHeight * 0.8) {
    // El teclado probablemente está abierto
    header.style.position = "absolute";
    header.style.top = `${window.scrollY}px`; // Ajusta la posición según el desplazamiento
    chatContainer.style.height = `${window.innerHeight - 60}px`; // Ajusta el contenedor principal
    messages.style.height = `${window.innerHeight - 120}px`; // Ajusta el área de mensajes
  } else {
    // El teclado probablemente está cerrado
    header.style.position = "fixed";
    header.style.top = "0";
    chatContainer.style.height = "calc(100vh - 60px)"; // Resta la altura del encabezado
    messages.style.height = "auto"; // Restaura el tamaño del área de mensajes
  }
});

// Bloquea el desplazamiento global cuando el teclado está abierto
document.addEventListener("touchstart", (e) => {
  const chatContainer = document.getElementById("chat-container");
  if (!chatContainer.contains(e.target)) {
    e.preventDefault();
  }
}, { passive: false });
