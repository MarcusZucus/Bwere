/**
 * Inicializa el modo pantalla completa y asegura que la app se comporte correctamente al regresar del fondo.
 */
document.addEventListener("DOMContentLoaded", () => {
  try {
    const fullscreenButton = document.getElementById("fullscreen-button");
    if (!fullscreenButton) {
      console.error("No se encontró el botón de pantalla completa.");
      return;
    }

    // Detectar clic en el botón para activar pantalla completa
    fullscreenButton.addEventListener("click", () => {
      activateFullScreen();
    });

    // Detectar cuando el usuario sale del modo pantalla completa
    document.addEventListener("fullscreenchange", () => {
      if (!document.fullscreenElement) {
        console.log("El usuario salió del modo pantalla completa.");
      }
    });

    // Intentar bloquear la orientación si es compatible
    if ('orientation' in screen && 'lock' in screen.orientation) {
      screen.orientation.lock("portrait-primary")
        .then(() => {
          console.log("La orientación de pantalla se bloqueó con éxito en portrait-primary.");
        })
        .catch((err) => {
          console.warn("No se pudo bloquear la orientación de pantalla:", err.message);
        });
    } else {
      console.warn("El bloqueo de orientación no es compatible con este dispositivo o navegador.");
    }

    // Aplicar estilos y prevenir scroll
    applyFullScreenStyles();
    preventScroll();
  } catch (error) {
    console.error("Error inicializando pantalla completa:", error);
    alert("Ocurrió un error al activar el modo inmersivo.");
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

  const elem = document.documentElement;
  if (elem.requestFullscreen) {
    elem.requestFullscreen().catch((err) => {
      console.error("Error al activar pantalla completa:", err);
    });
  } else if (elem.webkitRequestFullscreen) {
    elem.webkitRequestFullscreen().catch((err) => {
      console.error("Error al activar pantalla completa (webkit):", err);
    });
  } else if (elem.msRequestFullscreen) {
    elem.msRequestFullscreen().catch((err) => {
      console.error("Error al activar pantalla completa (ms):", err);
    });
  } else {
    console.warn("El modo de pantalla completa no está disponible en este navegador.");
  }
}

/**
 * Solicita el modo inmersivo para ocultar el notch, la barra inferior y otros elementos del sistema.
 */
function requestImmersiveMode() {
  if ('orientation' in screen && 'lock' in screen.orientation) {
    screen.orientation.lock("portrait-primary")
      .then(() => {
        console.log("La orientación de pantalla se bloqueó con éxito en portrait-primary.");
      })
      .catch((err) => {
        console.warn("No se pudo bloquear la orientación de pantalla:", err.message);
      });
  } else {
    console.warn("El bloqueo de orientación no es compatible con este dispositivo o navegador.");
  }

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
  const appContainer = document.getElementById("app") || document.documentElement;
  appContainer.addEventListener(
    "touchmove",
    (event) => {
      event.preventDefault();
    },
    { passive: false }
  );
  appContainer.addEventListener(
    "wheel",
    (event) => {
      event.preventDefault();
    },
    { passive: false }
  );
  appContainer.addEventListener(
    "keydown",
    (event) => {
      if (["ArrowUp", "ArrowDown", "PageUp", "PageDown"].includes(event.key)) {
        event.preventDefault();
      }
    }
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

    @media (max-width: 480px) {
      #app {
        font-size: 90%; /* Escala el contenido para dispositivos más pequeños */
      }
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
      document.webkitExitFullscreen().catch((err) => {
        console.error("Error al salir de pantalla completa (webkit):", err);
      });
    } else if (document.msExitFullscreen) {
      document.msExitFullscreen().catch((err) => {
        console.error("Error al salir de pantalla completa (ms):", err);
      });
    }
  } else {
    console.log("No hay elementos en pantalla completa para desactivar.");
  }
}