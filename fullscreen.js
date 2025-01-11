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
    requestImmersiveMode();
  } catch (error) {
    console.error("Error inicializando pantalla completa:", error);
  }
});

/**
 * Activa el modo pantalla completa.
 */
function activateFullScreen() {
  if (document.fullscreenElement || document.webkitFullscreenElement) {
    console.log("La aplicación ya está en modo de pantalla completa.");
    return;
  }

  if (document.documentElement.requestFullscreen) {
    document.documentElement.requestFullscreen().catch((err) => {
      console.error("Error al activar pantalla completa:", err);
    });
  } else if (document.documentElement.webkitRequestFullscreen) {
    document.documentElement.webkitRequestFullscreen(); // Para navegadores basados en WebKit
  }
}

/**
 * Solicita el modo inmersivo para ocultar el notch, la barra inferior y otros elementos del sistema.
 */
function requestImmersiveMode() {
  if ("screen" in window && "orientation" in screen) {
    try {
      screen.orientation.lock("portrait-primary").catch((err) => {
        console.warn("No se pudo bloquear la orientación de pantalla:", err);
      });
    } catch (error) {
      console.warn("La API de orientación de pantalla no está disponible.");
    }
  }

  // Intenta activar el modo inmersivo
  const metaViewport = document.querySelector("meta[name=viewport]");
  if (!metaViewport) {
    const meta = document.createElement("meta");
    meta.name = "viewport";
    meta.content =
      "width=device-width, height=device-height, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover";
    document.head.appendChild(meta);
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
 * Aplica estilos CSS para asegurar que la app ocupa el 100% del espacio disponible en pantalla,
 * incluyendo áreas seguras y eliminación de overflow.
 */
function applyFullScreenStyles() {
  const style = document.createElement("style");
  style.innerHTML = `
    html, body {
      height: 100%;
      margin: 0;
      padding: 0;
      overflow: hidden;
      touch-action: none; /* Evita gestos de scroll o zoom accidental */
    }

    body {
      padding: env(safe-area-inset-top) env(safe-area-inset-right) env(safe-area-inset-bottom) env(safe-area-inset-left);
      background-color: #000; /* Fondo negro para máxima inmersión */
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

/**
 * Salir del modo pantalla completa (opcional).
 */
function exitFullScreen() {
  if (document.fullscreenElement || document.webkitFullscreenElement) {
    if (document.exitFullscreen) {
      document.exitFullscreen().catch((err) => {
        console.error("Error al salir de pantalla completa:", err);
      });
    } else if (document.webkitExitFullscreen) {
      document.webkitExitFullscreen(); // Para navegadores basados en WebKit
    }
  } else {
    console.log("No hay elementos en pantalla completa para desactivar.");
  }
}

// Opcional: Asignar salida de pantalla completa a un botón
// document.getElementById("exitButton").addEventListener("click", exitFullScreen);
