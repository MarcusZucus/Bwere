if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        navigator.serviceWorker.register('/service-worker.js', { type: 'module' }) // Importante: { type: 'module' }
            .then(function(registration) {
                console.log('Service Worker registrado con éxito:', registration.scope);
            })
            .catch(function(error) {
                console.error('Error al registrar el Service Worker:', error);
            });
    });
}
