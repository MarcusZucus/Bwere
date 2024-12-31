// script.js
document.addEventListener("DOMContentLoaded", function () {
    const selectElement = document.querySelector("select");

    // Escuchar el cambio de selección
    selectElement.addEventListener("change", function (event) {
        const selectedValue = event.target.value;

        // Redirigir si el valor seleccionado es "fitbit"
        if (selectedValue === "fitbit") {
            window.location.href = "index.html";
        }
    });
});
