// Confirmar que el script se ha cargado correctamente
console.log('El script mis_compras.js se ha cargado correctamente.');

// Script exclusivo para manejar "Mis Compras"
document.addEventListener("DOMContentLoaded", () => {
  try {
    // Seleccionar el enlace de "Mis Compras"
    const misComprasLink = document.querySelector('[href="/html_modules/mis_compras/mis_compras.html"]');

    if (!misComprasLink) {
      console.error('El enlace a "Mis Compras" no se encuentra en el DOM.');
      return;
    }

    console.log('Enlace a "Mis Compras" encontrado.');

    // Seleccionar el contenedor donde se insertará el contenido
    const mainContent = document.getElementById("messages");

    if (!mainContent) {
      console.error('El contenedor con id "messages" no existe.');
      return;
    }

    console.log('El contenedor "messages" fue encontrado correctamente.');

    // Función para manejar el clic/toque
    const handleMisComprasClick = async (event) => {
      event.preventDefault(); // Prevenir redirección predeterminada
      console.log('Evento capturado en "Mis Compras".');

      try {
        // Realizar fetch para cargar el contenido de "Mis Compras"
        const response = await fetch("/html_modules/mis_compras/mis_compras.html");

        if (!response.ok) {
          throw new Error(`Error al cargar mis_compras.html: ${response.status}`);
        }

        const html = await response.text();
        console.log('Contenido de "Mis Compras" listo para insertar.');

        // Insertar el contenido en el contenedor principal
        mainContent.innerHTML = html;
      } catch (error) {
        console.error("Error en la solicitud de fetch:", error);
        alert("No se pudo cargar el contenido de 'Mis Compras'. Por favor, inténtalo más tarde.");
      }
    };

    // Escucha de eventos: click y touchstart
    misComprasLink.addEventListener("click", handleMisComprasClick);
    misComprasLink.addEventListener("touchstart", (event) => {
      console.log('Evento táctil detectado en "Mis Compras".');
      handleMisComprasClick(event);
    });

    console.log('Listeners para "Mis Compras" añadidos correctamente.');
  } catch (error) {
    console.error('Error general en el script mis_compras.js:', error);
  }
});
