if ('serviceWorker' in navigator) {
    window.addEventListener('load', function () {
        navigator.serviceWorker.register('/service-worker.js')
            .then(function (registration) {
                console.log('Service Worker registrado con éxito en el scope:', registration.scope);

                // Manejo de actualizaciones del Service Worker
                registration.onupdatefound = function () {
                    const installingWorker = registration.installing;
                    if (installingWorker) {
                        installingWorker.onstatechange = function () {
                            if (installingWorker.state === 'installed') {
                                if (navigator.serviceWorker.controller) {
                                    console.log('Nueva versión disponible. Por favor, recarga la página.');
                                    // Opcional: notificar al usuario que hay una nueva versión disponible
                                } else {
                                    console.log('El contenido está listo para usarse sin conexión.');
                                }
                            }
                        };
                    }
                };
            })
            .catch(function (error) {
                console.error('Error al registrar el Service Worker:', error);
            });
    });

    // Verificar si el SW está controlando la página actual
    navigator.serviceWorker.ready.then(function (registration) {
        console.log('Service Worker está activo y controlando la página:', registration.scope);
    });
}
