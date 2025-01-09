document.addEventListener("DOMContentLoaded", () => {
  try {
    const isFullscreenAvailable =
      document.documentElement.requestFullscreen ||
      document.documentElement.webkitRequestFullscreen;

    if (isFullscreenAvailable) {
      if (document.documentElement.requestFullscreen) {
        document.documentElement.requestFullscreen().catch((err) => {
          console.error("Error al activar pantalla completa:", err);
        });
      } else if (document.documentElement.webkitRequestFullscreen) {
        document.documentElement.webkitRequestFullscreen(); // Para navegadores basados en WebKit
      }
    } else {
      console.warn("La API de pantalla completa no está disponible en este navegador.");
    }
  } catch (error) {
    console.error("Error inicializando pantalla completa:", error);
  }
});

// Opcional: vuelve a pantalla completa al regresar a la app desde el fondo
document.addEventListener("visibilitychange", () => {
  try {
    if (
      document.visibilityState === "visible" &&
      (document.documentElement.requestFullscreen || document.documentElement.webkitRequestFullscreen)
    ) {
      if (document.documentElement.requestFullscreen) {
        document.documentElement.requestFullscreen().catch((err) => {
          console.error("Error al activar pantalla completa tras volver al frente:", err);
        });
      } else if (document.documentElement.webkitRequestFullscreen) {
        document.documentElement.webkitRequestFullscreen(); // Para navegadores basados en WebKit
      }
    }
  } catch (error) {
    console.error("Error activando pantalla completa tras volver al frente:", error);
  }
});
