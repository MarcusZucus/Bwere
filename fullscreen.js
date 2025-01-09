document.addEventListener("DOMContentLoaded", () => {
  if (document.documentElement.requestFullscreen) {
    document.documentElement.requestFullscreen();
  } else if (document.documentElement.webkitRequestFullscreen) {
    document.documentElement.webkitRequestFullscreen(); // Para navegadores basados en WebKit
  }
});

// Opcional: vuelve a pantalla completa al regresar a la app desde el fondo
document.addEventListener("visibilitychange", () => {
  if (document.visibilityState === "visible" && document.documentElement.requestFullscreen) {
    document.documentElement.requestFullscreen();
  }
});
