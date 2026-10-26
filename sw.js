// Launcher-only service worker. Network-first, versioned cache.
// Registered at the site root, so it MUST ignore the game builds (/sinerally/, /sinerally-*/ ...) -> those always go straight to the network.
const VERSION = 'launcher-v1';
const OWN = ['/', '/index.html', '/manifest.webmanifest', '/fonts/bangers.woff2',
  '/icons/apple-touch-icon.png', '/icons/icon-192.png', '/icons/icon-512.png', '/icons/favicon-32.png',
  '/thumbs/sinerally.jpg', '/thumbs/physics.jpg', '/thumbs/terrain.jpg', '/thumbs/enginesim.jpg', '/thumbs/engine.jpg'];
self.addEventListener('install', (e) => { e.waitUntil(caches.open(VERSION).then((c) => c.addAll(OWN)).catch(() => {}).then(() => self.skipWaiting())); });
self.addEventListener('activate', (e) => { e.waitUntil(caches.keys().then((ks) => Promise.all(ks.filter((k) => k !== VERSION).map((k) => caches.delete(k)))).then(() => self.clients.claim())); });
self.addEventListener('fetch', (e) => {
  const u = new URL(e.request.url);
  if (e.request.method !== 'GET' || u.origin !== location.origin || !OWN.includes(u.pathname)) return; // not ours: plain network
  e.respondWith(fetch(e.request).then((r) => { if (r.ok) { const cp = r.clone(); caches.open(VERSION).then((c) => c.put(e.request, cp)); } return r; })
    .catch(() => caches.match(e.request, { ignoreSearch: true }).then((r) => r || caches.match('/index.html'))));
});
