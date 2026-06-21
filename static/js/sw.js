const CACHE_NAME = 'farm-dss-v2';
const urlsToCache = [
  '/',
  '/login/',
  '/static/css/style.css',
  'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css',
  'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css',
  'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        return cache.addAll(urlsToCache);
      })
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME) {
            return caches.delete(cacheName);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        if (response) {
          return response;
        }
        return fetch(event.request).then(response => {
          if (!response || response.status !== 200 || response.type !== 'basic') {
            return response;
          }
          const responseToCache = response.clone();
          caches.open(CACHE_NAME).then(cache => {
            cache.put(event.request, responseToCache);
          });
          return response;
        });
      })
      .catch(() => {
        if (event.request.destination === 'document') {
          return caches.match('/');
        }
      })
  );
});

let deferredPrompt;
const installBanner = `
<div id="pwa-install-banner" style="display:none; position:fixed; bottom:0; left:0; right:0; background:linear-gradient(135deg, #27ae60, #2ecc71); color:white; padding:15px 20px; z-index:9999; box-shadow:0 -2px 10px rgba(0,0,0,0.2);">
  <div style="display:flex; justify-content:space-between; align-items:center;">
    <div style="flex:1;">
      <strong>Install FarmDSS App</strong>
      <p style="margin:5px 0 0 0; font-size:12px;">Get the app for quick offline access</p>
    </div>
    <div style="display:flex; gap:10px;">
      <button id="pwa-install-btn" style="background:#2c3e50; color:white; border:none; padding:8px 16px; border-radius:5px; cursor:pointer;">Install</button>
      <button id="pwa-dismiss-btn" style="background:transparent; color:white; border:1px solid white; padding:8px 16px; border-radius:5px; cursor:pointer;">Later</button>
    </div>
  </div>
</div>
`;

self.addEventListener('message', event => {
  if (event.data === 'skipWaiting') {
    self.skipWaiting();
  }
});

window.addEventListener('beforeinstallprompt', (e) => {
  e.preventDefault();
  deferredPrompt = e;
  document.body.insertAdjacentHTML('beforeend', installBanner);
  const banner = document.getElementById('pwa-install-banner');
  const installBtn = document.getElementById('pwa-install-btn');
  const dismissBtn = document.getElementById('pwa-dismiss-btn');

  banner.style.display = 'block';

  installBtn.addEventListener('click', async () => {
    if (deferredPrompt) {
      deferredPrompt.prompt();
      const { outcome } = await deferredPrompt.userChoice;
      deferredPrompt = null;
      banner.remove();
    }
  });

  dismissBtn.addEventListener('click', () => {
    banner.remove();
  });
});