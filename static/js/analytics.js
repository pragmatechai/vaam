// Loads GA4, Meta Pixel and TikTok Pixel only after cookie consent.
(function () {
    var config = document.getElementById('vaam-analytics').dataset;
    var loaded = false;

    function addScript(src) {
        var script = document.createElement('script');
        script.async = true;
        script.src = src;
        document.head.appendChild(script);
    }

    function loadGoogle(id) {
        window.dataLayer = window.dataLayer || [];
        window.gtag = function () { window.dataLayer.push(arguments); };
        window.gtag('js', new Date());
        window.gtag('config', id);
        addScript('https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(id));
    }

    function loadMeta(id) {
        var fbq = function () {
            fbq.callMethod ? fbq.callMethod.apply(fbq, arguments) : fbq.queue.push(arguments);
        };
        fbq.push = fbq;
        fbq.loaded = true;
        fbq.version = '2.0';
        fbq.queue = [];
        window.fbq = window._fbq = fbq;
        addScript('https://connect.facebook.net/en_US/fbevents.js');
        fbq('init', id);
        fbq('track', 'PageView');
    }

    function loadTikTok(id) {
        var url = 'https://analytics.tiktok.com/i18n/pixel/events.js';
        var ttq = window.ttq = window.ttq || [];
        window.TiktokAnalyticsObject = 'ttq';
        ['page', 'track', 'identify', 'grantConsent', 'revokeConsent'].forEach(function (method) {
            ttq[method] = function () {
                ttq.push([method].concat([].slice.call(arguments)));
            };
        });
        ttq._i = ttq._i || {};
        ttq._i[id] = [];
        ttq._i[id]._u = url;
        ttq._t = ttq._t || {};
        ttq._t[id] = Date.now();
        ttq._o = ttq._o || {};
        ttq._o[id] = {};
        addScript(url + '?sdkid=' + encodeURIComponent(id) + '&lib=ttq');
        ttq.page();
    }

    function track(googleEvent, metaEvent, tiktokEvent) {
        if (!loaded) return;
        if (window.gtag) window.gtag('event', googleEvent);
        if (window.fbq) window.fbq('track', metaEvent);
        if (window.ttq) window.ttq.track(tiktokEvent);
    }

    function start() {
        if (loaded) return;
        loaded = true;
        if (config.ga) loadGoogle(config.ga);
        if (config.meta) loadMeta(config.meta);
        if (config.tiktok) loadTikTok(config.tiktok);

        // The inquiry view redirects here with one of these flags after a saved submission.
        var params = new URLSearchParams(window.location.search);
        if (params.get('sent') === '1' || params.get('inquiry_sent') === '1') {
            track('generate_lead', 'Lead', 'SubmitForm');
        }
    }

    window.vaamConsentGranted = start;

    document.addEventListener('click', function (event) {
        if (event.target.closest && event.target.closest('a[href*="wa.me"]')) {
            track('whatsapp_click', 'Contact', 'Contact');
        }
    });

    try {
        if (localStorage.getItem('cookie_consent') === 'accepted') start();
    } catch (error) {
        // Storage blocked: treat as no consent.
    }
})();
