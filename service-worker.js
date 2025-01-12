import { precacheAndRoute } from 'workbox-precaching';
import { registerRoute } from 'workbox-routing';
import { CacheFirst, NetworkFirst } from 'workbox-strategies';
import { setCacheNameDetails } from 'workbox-core';

// Configurar el nombre del caché personalizado
setCacheNameDetails({
  prefix: 'werbly',
  suffix: 'v1',
  precache: 'precache',
  runtime: 'runtime',
});

// Precacheo automático con Workbox
precacheAndRoute(self.__WB_MANIFEST || []);

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
    caches.open('werbly-runtime-cache-v1').then((cache) => {
      return cache.addAll(urlsToCache);
    })
  );
});

// Rutas personalizadas para manejo de caché
registerRoute(
  ({ request }) => request.destination === 'document',
  new NetworkFirst({
    cacheName: 'werbly-html-cache',
  })
);

registerRoute(
  ({ request }) => request.destination === 'script' || request.destination === 'style',
  new CacheFirst({
    cacheName: 'werbly-static-resources',
  })
);

registerRoute(
  ({ request }) => request.destination === 'image',
  new CacheFirst({
    cacheName: 'werbly-image-cache',
  })
);

// Limpieza de cachés antiguos
self.addEventListener('activate', (event) => {
  const cacheWhitelist = ['werbly-html-cache', 'werbly-static-resources', 'werbly-image-cache', 'werbly-runtime-cache-v1'];
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
