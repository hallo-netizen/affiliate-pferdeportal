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
        if (image.complete && image.naturalWidth > 0) {
            callback(image);
        } else {
            image.addEventListener('load', function () { callback(image); }, { once: true });
        }
    }

    /* V6.72.37: reale Kategorie-Querbanner-Toleranz auf allen Kategorieebenen.
       Downscale bleibt erste Wahl. Nur wenn die Mindestfuellung sonst knapp
       verfehlt wird, darf bis zum gebundenen Maximum (derzeit 1.10) skaliert
       werden. Darueber bleibt der Platz fail-closed unsichtbar. */
    function normalizeLargeCategoryBannerHost(slot) {
        var host = slot ? slot.closest('.pa356-partner, .pa359-partner, .pa255-network, .pa266-network') : null;
        if (!host) {
            return;
        }
        Array.prototype.forEach.call(host.children || [], function (child) {
            var hide = child.tagName === 'HEADER'
                || (child.classList && child.classList.contains('pa356-ad-label'));
            if (hide) {
                child.style.setProperty('display', 'none', 'important');
                child.setAttribute('aria-hidden', 'true');
            }
        });
    }

    function validateLargeCategoryBanner(image) {
        var link = image.closest('[data-ppar-large-banner="1"]');
        var slot = image.closest('.ppar-category-large-banner-slot');
        if (!link || !slot) {
            return;
        }
        normalizeLargeCategoryBannerHost(slot);
        var minFill = parseFloat(link.getAttribute('data-ppar-min-fill') || '0.60');
        if (!isFinite(minFill) || minFill <= 0 || minFill > 1) {
            minFill = 0.60;
        }
        var upscaleMax = parseFloat(link.getAttribute('data-ppar-upscale-max') || '1.00');
        if (!isFinite(upscaleMax) || upscaleMax < 1 || upscaleMax > 1.10) {
            upscaleMax = 1.00;
        }
        var available = slot.clientWidth || (slot.parentElement ? slot.parentElement.clientWidth : 0) || 0;
        var natural = image.naturalWidth || 0;
        var threshold = available * minFill;
        var valid = natural > 0 && available > 0 && (natural * upscaleMax) + 0.5 >= threshold;
        slot.setAttribute('data-ppar-large-banner-checked', '1');
        image.style.removeProperty('width');
        link.style.removeProperty('width');
        if (valid) {
            if (natural + 0.5 < threshold) {
                var scaled = Math.min(available, threshold, natural * upscaleMax);
                image.style.setProperty('width', Math.ceil(scaled) + 'px', 'important');
                link.style.setProperty('width', Math.ceil(scaled) + 'px', 'important');
            }
            slot.removeAttribute('data-ppar-large-banner-invalid');
        } else {
            slot.setAttribute('data-ppar-large-banner-invalid', '1');
        }
    }

    function categoryProductCards(grid) {
        return Array.prototype.filter.call(grid.children || [], function (card) {
            if (!card.classList || !card.classList.contains('is-real')) {
                return false;
            }
            if (card.getAttribute('data-pftk-affiliate-card-v150414') === '1') {
                return true;
            }
            var slot266 = card.getAttribute('data-pa266-slot') || '';
            var slot255 = card.getAttribute('data-pa255-slot') || '';
            if (slot266.indexOf('category_product_') === 0 || slot255.indexOf('category_product_') === 0) {
                return true;
            }
            return !!card.querySelector('.ppar-affiliate-slot[data-ppar-slot^="category_product_"]');
        });
    }

    function setImportantHeight(node, value) {
        if (node && node.style) {
            node.style.setProperty('height', value, 'important');
        }
    }

    /* Bereits historisch vorhandene Invariante wiederherstellen:
       sichtbare category_product-Karten derselben realen Rasterzeile bekommen
       nach dem finalen DOM-/Bild-/Font-Layout exakt dieselbe Aussenhoehe. */
    function equalizeCategoryProductGrid(grid) {
        var cards = categoryProductCards(grid);
        if (cards.length < 2) {
            return;
        }

        cards.forEach(function (card) {
            setImportantHeight(card, 'auto');
        });

        var rows = [];
        cards.forEach(function (card) {
            var rect = card.getBoundingClientRect();
            var top = Math.round(rect.top);
            var row = rows.find(function (candidate) { return Math.abs(candidate.top - top) <= 2; });
            if (!row) {
                row = { top: top, cards: [], max: 0 };
                rows.push(row);
            }
            var height = Math.max(rect.height, card.scrollHeight || 0, card.offsetHeight || 0);
            row.cards.push(card);
            row.max = Math.max(row.max, Math.ceil(height));
        });

        rows.forEach(function (row) {
            if (row.cards.length < 2 || row.max <= 0) {
                return;
            }
            row.cards.forEach(function (card) {
                setImportantHeight(card, row.max + 'px');
                var shell = card.querySelector(':scope > [data-pftk-affiliate-clean-shell-v150414="1"]');
                if (shell) {
                    shell.style.setProperty('height', '100%', 'important');
                }
                var directSlot = card.querySelector(':scope > .ppar-affiliate-slot[data-ppar-slot^="category_product_"]');
                if (directSlot) {
                    directSlot.style.setProperty('height', '100%', 'important');
                }
            });
        });
    }

    function runOnce() {
        document.querySelectorAll('.ppar-banner-image, .ppar-category-large-banner-image').forEach(function (image) {
            inspect(image, function (loaded) {
                classify(loaded);
                if (loaded.classList.contains('ppar-category-large-banner-image')) {
                    validateLargeCategoryBanner(loaded);
                }
            });
        });

        // Produktkarten sind kein Banner-Nachladeweg. Ein einmaliger Layoutabgleich
        // nach dem normalen Seitenaufbau bleibt erhalten; keine Observer/Timer-Schleife.
        document.querySelectorAll('.pa255-product-grid, .pa266-product-grid, .pa272-product-grid, .pa273-product-grid').forEach(equalizeCategoryProductGrid);
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', runOnce, { once: true });
    } else {
        runOnce();
    }
    window.addEventListener('load', runOnce, { once: true });
}());

/* V6.72.100 PASS-RESTORE – Glossar Desktop order from confirmed 6.72.60/57. */
(function(){
  'use strict';
  var raf=0;
  function position(){
    raf=0;
    var grid=document.querySelector('.pftk-gsingle-grid-v150490');
    var aside=document.querySelector('.pftk-gsingle-aside-v150490');
    var related=aside?aside.querySelector('.pftk-gsingle-related-v150548, .pftk-gsingle-related-v150547'):null;
    var more=aside?aside.querySelector('.pftk-gsingle-topic-v150490'):null;
    var ad=document.querySelector('.ppar-glossary-banner-desktop-v67244');
    var footer=document.querySelector('.pftk-gsingle-footer-v150490');
    if(!grid||!aside||!related||!more||!ad)return;
    if(window.matchMedia('(max-width:840px)').matches){
      ad.style.removeProperty('top');more.style.removeProperty('transform');if(footer)footer.style.removeProperty('margin-top');return;
    }
    more.style.removeProperty('transform');if(footer)footer.style.removeProperty('margin-top');
    var gr=grid.getBoundingClientRect(), rr=related.getBoundingClientRect();
    var top=Math.round(rr.bottom-gr.top+40);ad.style.setProperty('top',top+'px','important');
    var ar=ad.getBoundingClientRect(), shift=Math.ceil(ar.height+40);
    more.style.setProperty('transform','translateY('+shift+'px)','important');
    if(footer){var fr=footer.getBoundingClientRect(), mr=more.getBoundingClientRect(), bottom=Math.max(ar.bottom,mr.bottom), overlap=Math.ceil(bottom+30-fr.top);if(overlap>0)footer.style.setProperty('margin-top',(30+overlap)+'px','important');}
  }
  function schedule(){if(raf)return;raf=window.requestAnimationFrame(position);}
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',schedule,{once:true});else schedule();
  window.addEventListener('load',schedule);window.addEventListener('resize',schedule,{passive:true});
  document.addEventListener('load',function(e){if(e.target&&e.target.closest&&e.target.closest('.ppar-glossary-banner-desktop-v67244'))schedule();},true);
})();
