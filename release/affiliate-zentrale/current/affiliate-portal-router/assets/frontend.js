(function () {
    'use strict';

    function classify(image) {
        var width = image.naturalWidth || 0;
        var height = image.naturalHeight || 0;
        if (!width || !height) {
            return;
        }
        var ratio = width / height;
        var slot = image.closest('.ppar-affiliate-slot, .ppar-article-product-card');
        if (slot) {
            var format = ratio >= 2 ? 'wide' : (ratio <= 0.8 ? 'portrait' : (ratio >= 0.9 && ratio <= 1.1 ? 'square' : 'landscape'));
            slot.classList.add('ppar-banner-format-' + format);
            slot.dataset.pparBannerWidth = String(width);
            slot.dataset.pparBannerHeight = String(height);
            slot.dataset.pparBannerRatio = ratio.toFixed(3);
        }
    }

    function inspect(image, callback) {
        if (image.complete) {
            callback(image);
        } else {
            image.addEventListener('load', function () { callback(image); }, { once: true });
        }
    }

    document.addEventListener('DOMContentLoaded', function () {
        document.querySelectorAll('.ppar-banner-image').forEach(function (image) {
            inspect(image, classify);
        });
    });
}());
