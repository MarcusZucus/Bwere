module.exports = {
  globDirectory: 'html_modules/',
  globPatterns: [
    '**/*.{js,html,css}'
  ],
  swSrc: 'service-worker.js', // Archivo manual existente
  swDest: 'service-worker.js', // Sobreescribe el mismo archivo
  dontCacheBustURLsMatching: /[\?&](utm_|fbclid)/, // Patrón como expresión regular directamente
};
