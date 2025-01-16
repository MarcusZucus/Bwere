// Script exclusivo para cargar "Mis Compras"
document.addEventListener("DOMContentLoaded", () => {
  const misComprasLink = document.querySelector('[href="/html_modules/mis_compras/mis_compras.html"]');

  if (!misComprasLink) {
    console.error('El enlace a "Mis Compras" no se encuentra en el DOM.');
    return;
  }

  console.log('Enlace a "Mis Compras" encontrado.');

  // Capturar clic en el enlace
  misComprasLink.addEventListener("click", (event) => {
    event.preventDefault(); // Prevenir redirección predeterminada
    console.log('Clic en "Mis Compras" capturado.');

    // Hacer el fetch
    fetch("/html_modules/mis_compras/mis_compras.html")
      .then(response => {
        if (!response.ok) {
          throw new Error("Error al cargar mis_compras.html: " + response.status);
        }
        return response.text();
      })
      .then(html => {
        const mainContent = document.getElementById("messages");
        if (!mainContent) {
          console.error('El contenedor con id "messages" no existe.');
          return;
        }
        console.log('Contenido de "Mis Compras" cargado correctamente.');
        mainContent.innerHTML = html;
      })
      .catch(error => {
        console.error("Error en la solicitud de fetch:", error);
      });
  });
});
