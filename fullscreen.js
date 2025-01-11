/**
 * Inicializa el modo pantalla completa y asegura que la app se comporte correctamente al regresar del fondo.
 */
document.addEventListener("DOMContentLoaded", () => {
  try {
    const isFullscreenAvailable =
      document.documentElement.requestFullscreen ||
      document.documentElement.webkitRequestFullscreen;

    if (isFullscreenAvailable) {
      activateFullScreen();
    } else {
      console.warn("La API de pantalla completa no está disponible en este navegador.");
    }

    // Aplica estilos para ocupar el 100% de la pantalla
    applyFullScreenStyles();
    preventScroll();
  } catch (error) {
    console.error("Error inicializando pantalla completa:", error);
  }
});

/**
 * Activa el modo pantalla completa.
 */
function activateFullScreen() {
  if (document.documentElement.requestFullscreen) {
    document.documentElement.requestFullscreen().catch((err) => {
      console.error("Error al activar pantalla completa:", err);
    });
  } else if (document.documentElement.webkitRequestFullscreen) {
    document.documentElement.webkitRequestFullscreen(); // Para navegadores basados en WebKit
  }
}

/**
 * Evita que el usuario pueda desplazarse accidentalmente.
 */
function preventScroll() {
  document.addEventListener(
    "touchmove",
    (event) => {
      event.preventDefault();
    },
    { passive: false }
  );
}

/**
 * Aplica estilos CSS para asegurar que la app ocupa el 100% del espacio disponible en pantalla.
 */
function applyFullScreenStyles() {
  const style = document.createElement("style");
  style.innerHTML = `
    html, body {
      height: 100%;
      margin: 0;
      padding: 0;
      overflow: hidden;
    }

    body {
      padding: env(safe-area-inset-top) env(safe-area-inset-right) env(safe-area-inset-bottom) env(safe-area-inset-left);
    }

    #app {
      height: 100%;
      display: flex;
      flex-direction: column;
      justify-content: flex-start;
    }
  `;
  document.head.appendChild(style);
}

/**
 * Vuelve a activar el modo pantalla completa cuando la app regresa del fondo.
 */
document.addEventListener("visibilitychange", () => {
  try {
    if (
      document.visibilityState === "visible" &&
      (document.documentElement.requestFullscreen || document.documentElement.webkitRequestFullscreen)
    ) {
      activateFullScreen();
    }
  } catch (error) {
    console.error("Error activando pantalla completa tras volver al frente:", error);
  }
});
