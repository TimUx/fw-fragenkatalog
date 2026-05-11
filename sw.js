// Cache-Version bei jedem inhaltlichen Update hochzählen,
// damit Clients ihren alten Cache verwerfen.
const CACHE_VERSION = 'v3';
const CACHE_NAME = `ffw-fragenkatalog-${CACHE_VERSION}`;

// Nur der App-Shell wird vorab gecacht. Die Fragen-JSONs bewusst NICHT,
// damit Änderungen an data/*.json sofort sichtbar werden.
const PRECACHE_URLS = [
  './',
  './index.html',
  './app.js',
  './style.css',
  './manifest.json',
  './assets/wappen.png'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(PRECACHE_URLS))
  );
  self.skipWaiting();
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys()
      .then(keys => Promise.all(
        keys.filter(key => key !== CACHE_NAME).map(key => caches.delete(key))
      ))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', event => {
  const request = event.request;

  if (request.method !== 'GET') {
    return;
  }

  const url = new URL(request.url);

  if (url.origin !== self.location.origin) {
    return;
  }

  const isData = url.pathname.includes('/data/');
  const isNavigation = request.mode === 'navigate' || request.destination === 'document';
  const isAppShell = /\.(html|js|css|json)$/i.test(url.pathname);

  if (isData || isNavigation || isAppShell) {
    event.respondWith(networkFirst(request));
  } else {
    event.respondWith(cacheFirst(request));
  }
});

async function networkFirst(request) {
  const cache = await caches.open(CACHE_NAME);
  try {
    const fresh = await fetch(request);
    if (fresh && fresh.ok && fresh.type === 'basic') {
      safeCachePut(cache, request, fresh.clone());
    }
    return fresh;
  } catch (err) {
    const cached = await cache.match(request);
    if (cached) {
      return cached;
    }
    throw err;
  }
}

async function cacheFirst(request) {
  const cache = await caches.open(CACHE_NAME);
  const cached = await cache.match(request);
  if (cached) {
    return cached;
  }
  const fresh = await fetch(request);
  if (fresh && fresh.ok && fresh.type === 'basic') {
    safeCachePut(cache, request, fresh.clone());
  }
  return fresh;
}

function safeCachePut(cache, request, response) {
  // cache.put kann bei manchen Responses (opaque, partial, range)
  // synchron oder asynchron werfen. Fehler hier dürfen den Fetch
  // nicht zum Scheitern bringen.
  Promise.resolve()
    .then(() => cache.put(request, response))
    .catch(() => { /* ignore */ });
}
