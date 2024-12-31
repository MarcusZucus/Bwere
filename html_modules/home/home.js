// Manejo de la selección del smartwatch
document.getElementById('smartwatchSelect').addEventListener('change', function () {
  const selectedBrand = this.value;

  // Verificar la marca seleccionada
  if (selectedBrand) {
    // Lógica para redirigir a OAuth 2.0 según la marca seleccionada
    switch (selectedBrand) {
      case 'samsung':
        openOAuthPopup('https://oauth.samsung.com/authorize');
        break;
      case 'apple':
        openOAuthPopup('https://appleid.apple.com/auth/authorize');
        break;
      case 'huawei':
        openOAuthPopup('https://oauth.huawei.com/authorize');
        break;
      case 'fitbit':
        openOAuthPopup('https://www.fitbit.com/oauth2/authorize');
        break;
      case 'garmin':
        openOAuthPopup('https://connect.garmin.com/oauth/authorize');
        break;
      default:
        alert('Marca no soportada.');
    }
  }
});

// Función para abrir el popup de OAuth 2.0
function openOAuthPopup(url) {
  const width = 500;
  const height = 600;
  const left = (screen.width / 2) - (width / 2);
  const top = (screen.height / 2) - (height / 2);

  window.open(
    url,
    'OAuthPopup',
    `width=${width},height=${height},top=${top},left=${left},resizable=no,scrollbars=no,status=no`
  );
}
