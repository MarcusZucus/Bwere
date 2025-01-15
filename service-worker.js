const CACHE_NAME = "bware-cache-v2";
const urlsToCache = [
  "/index.html",
  "/html_modules/styles.css",
  "/html_modules/modules/animations.js",
  "/html_modules/modules/chat.js",
  "/html_modules/modules/menu.js",
  "/icon-192x192.png",
  "/icon-512x512.png",
  "/manifest.json",
  "/offline.html" // Página de respaldo para modo offline
];

// Instalación del Service Worker y almacenamiento en caché
self.addEventListener("install", event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      console.log("Archivos precacheados correctamente");
      return cache.addAll(urlsToCache);
    })
  );
  self.skipWaiting(); // Activa el SW inmediatamente
});

// Gestión de solicitudes de red
self.addEventListener("fetch", event => {
  if (event.request.method !== "GET") {
    return; // Ignora solicitudes que no sean GET
  }

  event.respondWith(
    caches.match(event.request).then(cachedResponse => {
      if (cachedResponse) {
        return cachedResponse; // Devuelve respuesta desde caché si existe
      }

      return fetch(event.request)
        .then(networkResponse => {
          if (!networkResponse || networkResponse.status !== 200 || networkResponse.type !== "basic") {
            return networkResponse;
          }

          // Clona la respuesta para agregarla al caché
          const responseToCache = networkResponse.clone();

          caches.open(CACHE_NAME).then(cache => {
            cache.put(event.request, responseToCache);
          });

          return networkResponse;
        })
        .catch(() => {
          // Respuesta alternativa en caso de error de red
          return caches.match("/offline.html");
        });
    })
  );
});

// Activación del Service Worker y limpieza de cachés antiguos
self.addEventListener("activate", event => {
  const cacheWhitelist = [CACHE_NAME];
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (!cacheWhitelist.includes(cacheName)) {
            console.log(`Eliminando caché antigua: ${cacheName}`);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
  self.clients.claim(); // Toma el control de las pestañas sin recargar
});

// Notificaciones push (opcional, si usas Firebase o un servidor propio)
self.addEventListener("push", event => {
  const data = event.data ? event.data.json() : {};
  const title = data.title || "Nueva notificación";
  const options = {
    body: data.body || "Haz clic para obtener más información.",
    icon: data.icon || "/icon-192x192.png",
    badge: data.badge || "/icon-192x192.png",
    data: data.url || "/"
  };

  event.waitUntil(self.registration.showNotification(title, options));
});

// Gestión de eventos de clic en notificaciones
self.addEventListener("notificationclick", event => {
  event.notification.close();
  const url = event.notification.data;

  event.waitUntil(
    clients.matchAll({ type: "window" }).then(clientList => {
      for (const client of clientList) {
        if (client.url === url && "focus" in client) {
          return client.focus();
        }
      }

      if (clients.openWindow) {
        return clients.openWindow(url);
      }
    })
  );
});
