const brandDropdown = document.getElementById('brand-dropdown');
const connectButton = document.getElementById('connect-button');

// Mostrar el botón solo cuando el usuario seleccione una marca
brandDropdown.addEventListener('change', () => {
  if (brandDropdown.value) {
    connectButton.classList.remove('hidden');
  } else {
    connectButton.classList.add('hidden');
  }
});

// Acción del botón de conectar
connectButton.addEventListener('click', () => {
  const selectedBrand = brandDropdown.options[brandDropdown.selectedIndex].text;
  alert(`Has seleccionado ${selectedBrand}. Redirigiendo al chat...`);
  // Redirige al chat (ajusta la ruta si es necesario)
  window.location.href = '../index.html';
});
