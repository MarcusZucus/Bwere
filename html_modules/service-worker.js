const CACHE_NAME = "werbly-cache-v1";
const urlsToCache = [
    "/html_modules/index.html",
    "/html_modules/styles.css",
    "/html_modules/modules/animations.js",
    "/html_modules/icon-192x192.png",
    "/html_modules/icon-512x512.png",
    "/html_modules/manifest.json",
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
      return response || fetch(event.request);
    })
  );
});

// Activación del Service Worker y limpieza de cachés antiguas
self.addEventListener("activate", event => {
  const cacheWhitelist = [CACHE_NAME];
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (!cacheWhitelist.includes(cacheName)) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});
