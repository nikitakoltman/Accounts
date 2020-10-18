const CACHE = 'cache-and-update-v11';

const cache_files = [
    '/',
    '/offline/'
];

// При установке воркера мы должны закешировать часть данных (статику).
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches
        .open(CACHE)
        .then((cache) => cache.addAll(cache_files))
        // `skipWaiting()` необходим, потому что мы хотим активировать SW
        // и контролировать его сразу, а не после перезагрузки.
        .then(() => self.skipWaiting())
    );
});

self.addEventListener('activate', (event) => {
    // `self.clients.claim()` позволяет SW начать перехватывать запросы с самого начала,
    // это работает вместе с `skipWaiting()`, позволяя использовать `fallback` с самых первых запросов.
    event.waitUntil(self.clients.claim());
});

self.addEventListener('fetch', function(event) {
    // Можете использовать любую стратегию описанную выше.
    // Если она не отработает корректно, то используейте `Embedded fallback`.
    if ((event.request.cache === 'only-if-cached' && event.request.mode !== 'same-origin') ||
        (event.request.referrerPolicy === 'same-origin' && event.request.cache === 'no-cache')) {
        return;
    }
    event.respondWith(networkOrCache(event.request)
        .catch(() => useFallback()));

    // `waitUntil()` нужен, чтобы предотвратить прекращение работы worker'a до того как кэш обновиться.
    event.waitUntil(update(event.request));
});

function fromCache(request) {
    return caches.open(CACHE).then((cache) =>
        cache.match(request).then((matching) =>
            matching || Promise.reject('no-match')
        ));
}

function update(request) {
    return caches.open(CACHE).then((cache) =>
        fetch(request/*.clone()*/).then((response) =>
            cache.put(request, response)
        )
    );
}

function networkOrCache(request) {
    return fetch(request)
        .then((response) => response.ok ? response : fromCache(request))
        .catch(() => fromCache(request));
}

// Он никогда не упадет, т.к мы всегда отдаем заранее подготовленные данные.
function useFallback() {
    console.log('useFallback');
    //return Promise.resolve(fetch('/offline/'));
    return caches.match('/offline/');
}

function fromCache(request) {
    return caches.open(CACHE).then((cache) =>
        cache.match(request, { cacheName: CACHE, ignoreVary: true }).then((matching) =>
            matching || Promise.reject('no-match')
        ));
}