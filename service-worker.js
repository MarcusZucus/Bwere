const CACHE_NAME = "bware-cache-v1";
const urlsToCache = [
  "/index.html",
  "/html_modules/styles.css",
  "/html_modules/modules/animations.js",
  "/html_modules/modules/chat.js",
  "/html_modules/modules/menu.js",
  "/icon-192x192.png",
  "/icon-512x512.png",
  "/manifest.json",
];

// Instalación del Service Worker y almacenamiento en caché
self.addEventListener("install", event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      return cache.addAll(urlsToCache);
    })
  );
});

// Gestión de solicitudes de red
self.addEventListener("fetch", event => {
  event.respondWith(
    caches.match(event.request).then(response => {
      // Si el archivo está en caché, lo devuelve; si no, hace una solicitud de red
      return response || fetch(event.request);
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
          // Elimina las cachés antiguas que no están en la lista blanca
          if (!cacheWhitelist.includes(cacheName)) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});

