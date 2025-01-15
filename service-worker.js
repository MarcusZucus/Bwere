import { precacheAndRoute } from 'https://storage.googleapis.com/workbox-cdn/releases/6.5.4/workbox-precaching.mjs';
import { registerRoute } from 'https://storage.googleapis.com/workbox-cdn/releases/6.5.4/workbox-routing.mjs';
import { CacheFirst, NetworkFirst } from 'https://storage.googleapis.com/workbox-cdn/releases/6.5.4/workbox-strategies.mjs';
import { setCacheNameDetails } from 'https://storage.googleapis.com/workbox-cdn/releases/6.5.4/workbox-core.mjs';

// Configurar el nombre del caché personalizado
setCacheNameDetails({
  prefix: 'Bwere',
  suffix: 'v1',
  precache: 'precache',
  runtime: 'runtime',
});

// Precacheo automático con Workbox
precacheAndRoute([{"revision":"6da9b85404e5654454c49b6e802b3802","url":"home/exchangeToken.js"},{"revision":"3777c9ecad59e4ca0d7d5e8f745d7ca6","url":"home/home.html"},{"revision":"8aeb73e69a3fbc84bf948f241cc8cac8","url":"home/responsive.css"},{"revision":"e7e0797046e52b2eb763ee8f493baf5c","url":"modules/animations.js"},{"revision":"0d4e80fed94561a3728a55616d8ad3fe","url":"modules/chat.js"},{"revision":"23e23e9fca7a07856022ac061ad571af","url":"modules/gpt.js"},{"revision":"06cbd0ce2a8bc8c28e27ee645fcd073a","url":"modules/menu.js"},{"revision":"e64f64b2be8e88db509525aaf82221c8","url":"styles.css"}] || []);

// URLs adicionales para precache manual
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

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open('Bwere-runtime-cache-v1').then((cache) => {
      return cache.addAll(urlsToCache);
    })
  );
});

// Rutas personalizadas para manejo de caché
registerRoute(
  ({ request }) => request.destination === 'document',
  new NetworkFirst({
    cacheName: 'Bwere-html-cache',
  })
);

registerRoute(
  ({ request }) => request.destination === 'script' || request.destination === 'style',
  new CacheFirst({
    cacheName: 'Bwere-static-resources',
  })
);

registerRoute(
  ({ request }) => request.destination === 'image',
  new CacheFirst({
    cacheName: 'Bwere-image-cache',
  })
);

// Limpieza de cachés antiguos
self.addEventListener('activate', (event) => {
  const cacheWhitelist = ['Bwere-html-cache', 'Bwere-static-resources', 'Bwere-image-cache', 'Bwere-runtime-cache-v1'];
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (!cacheWhitelist.includes(cacheName)) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});

// Gestión de solicitudes de red
self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request).then((response) => {
      return response || fetch(event.request);
    })
  );
});
