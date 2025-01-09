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
