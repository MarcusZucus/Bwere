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

// Previene la recarga accidental al navegar fuera
window.addEventListener("beforeunload", (e) => {
  e.preventDefault();
  e.returnValue = "";
});

// Ajusta el comportamiento del encabezado para evitar que desaparezca con el teclado
window.addEventListener("resize", () => {
  const header = document.getElementById("chat-header");
  if (window.innerHeight < window.outerHeight * 0.8) {
    // El teclado probablemente está abierto
    header.style.position = "absolute";
    header.style.top = `${window.scrollY}px`; // Ajusta la posición según el desplazamiento
  } else {
    // El teclado probablemente está cerrado
    header.style.position = "fixed";
    header.style.top = "0";
  }
});
