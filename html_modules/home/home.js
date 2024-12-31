const brandDropdown = document.getElementById('brand-dropdown');
const connectButton = document.getElementById('connect-button');

// Agrega funcionalidad al botón
connectButton.addEventListener('click', () => {
  const selectedBrand = brandDropdown.value;
  if (selectedBrand) {
    alert(`Has seleccionado ${selectedBrand}. ¡Conectando tu smartwatch!`);
  } else {
    alert('Por favor, selecciona tu smartwatch antes de continuar.');
  }
});
