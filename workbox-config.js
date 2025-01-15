module.exports = {
  // Directorio base donde Workbox buscará los archivos a cachear
  globDirectory: 'html_modules/',

  // Patrones de archivos a incluir en el precaching
  globPatterns: [
    '**/*.{js,html,css,json,svg,png,jpg}',
  ],

  // Archivo manual existente del Service Worker como base
  swSrc: 'service-worker.js',

  // Archivo destino donde se generará el nuevo Service Worker
  swDest: 'service-worker.js',

  // Configuración avanzada
  dontCacheBustURLsMatching: /\.[0-9a-f]{8}\./, // Evita la busting de URLs con hashes

  // Configuración de Workbox Runtime Caching
  runtimeCaching: [
    {
      // Estrategia para APIs externas (p. ej., datos dinámicos o de backend)
      urlPattern: /^https:\/\/apis\.bwere\.com\/.*$/,
      handler: 'NetworkFirst',
      options: {
        cacheName: 'api-cache',
        expiration: {
          maxEntries: 50, // Máximo de peticiones cacheadas
          maxAgeSeconds: 60 * 60 * 24, // 1 día de vida útil
        },
        networkTimeoutSeconds: 10, // Tiempo límite para esperar a la red antes de usar el caché
      },
    },
    {
      // Estrategia para fuentes (Google Fonts)
      urlPattern: /^https:\/\/fonts\.(?:googleapis|gstatic)\.com\/.*$/,
      handler: 'CacheFirst',
      options: {
        cacheName: 'google-fonts-cache',
        expiration: {
          maxEntries: 30,
          maxAgeSeconds: 60 * 60 * 24 * 365, // 1 año
        },
      },
    },
    {
      // Estrategia para imágenes
      urlPattern: /\.(?:png|jpg|jpeg|svg|gif)$/,
      handler: 'CacheFirst',
      options: {
        cacheName: 'image-cache',
        expiration: {
          maxEntries: 100,
          maxAgeSeconds: 60 * 60 * 24 * 30, // 30 días
        },
      },
    },
    {
      // Estrategia para CSS y JS estáticos
      urlPattern: /\.(?:js|css)$/,
      handler: 'StaleWhileRevalidate',
      options: {
        cacheName: 'static-resources',
        expiration: {
          maxEntries: 50,
        },
      },
    },
    {
      // Estrategia para páginas HTML
      urlPattern: /\/.*\.(html|htm)$/,
      handler: 'NetworkFirst',
      options: {
        cacheName: 'html-cache',
        expiration: {
          maxEntries: 20,
          maxAgeSeconds: 60 * 60 * 24, // 1 día
        },
      },
    },
  ],

  // Opciones adicionales para Workbox
  mode: 'production', // Asegúrate de que esté en modo de producción
  sourcemap: false, // Desactiva mapas de fuente para optimizar
};
