const CACHE_NAME = 'teck_cheff_v1';
const urlsToCache = [
  '/',
  // '/static/css/main.css',
  // '/static/js/main.js',
  // Agrega aquí las URL de otros recursos estáticos que deseas cachear
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(urlsToCache))
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => response || fetch(event.request))
  );
});