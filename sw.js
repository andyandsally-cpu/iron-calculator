const CACHE = 'iron-calc-v1';
const FILES = [
  '/iron-calculator/',
  '/iron-calculator/index.html',
  '/iron-calculator/manifest.json'
];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE).then(c => c.addAll(FILES))
  );
});

self.addEventListener('fetch', e => {
  e.respondWith(
    caches.match(e.request).then(r => r || fetch(e.request))
  );
});
