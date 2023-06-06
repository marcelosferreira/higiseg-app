var staticCacheName = 'djangopwa-v1';

self.addEventListener('install', function (event) {
    event.waitUntil(
        caches.open(staticCacheName).then(function (cache) {
            return cache.addAll([
                '/',
                '/home/',
                '/quemSomos/',
                '/servicos/',
                '/offline/',
            ]);
        })
    );
});

self.addEventListener('fetch', function (event) {
    event.respondWith(
        fetch(event.request).then(function (networkResponse) {
            return networkResponse;
        }).catch(function () {
            return caches.match(event.request).then(function (cachedResponse) {
                if (cachedResponse) {
                    return cachedResponse;
                } else {
                    return caches.match('/offline/'); // Página offline personalizada
                }
            });
        })
    );
});