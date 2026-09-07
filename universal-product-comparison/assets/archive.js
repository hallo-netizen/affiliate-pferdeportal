(function () {
    'use strict';

    function init(root) {
        var filter = 'all';
        var subfilter = 'all';
        var selectedProduct = '';
        var search = '';

        var filterButtons = Array.prototype.slice.call(root.querySelectorAll('[data-upc-filter]'));
        var subfilterButtons = Array.prototype.slice.call(root.querySelectorAll('[data-upc-subfilter]'));
        var productButtons = Array.prototype.slice.call(root.querySelectorAll('[data-upc-product]'));
        var items = Array.prototype.slice.call(root.querySelectorAll('[data-upc-item]'));
        var input = root.querySelector('[data-upc-search]');
        var subfilters = root.querySelector('[data-upc-subfilters]');
        var empty = root.querySelector('[data-upc-empty]');

        function normalize(value) {
            return (value || '').toString().toLowerCase()
                .normalize('NFD').replace(/[\u0300-\u036f]/g, '');
        }

        function setPressed(buttons, active, attr) {
            buttons.forEach(function (button) {
                button.setAttribute('aria-pressed', button.getAttribute(attr) === active ? 'true' : 'false');
            });
        }

        function apply() {
            var visible = 0;

            items.forEach(function (item) {
                var type = item.getAttribute('data-upc-type') || '';
                var comparisonType = item.getAttribute('data-upc-comparison-type') || '';
                var products = (item.getAttribute('data-upc-products') || '').split(/\s+/);
                var haystack = normalize(item.getAttribute('data-upc-search-text') || '');

                var filterOk = filter === 'all' || type === filter;
                var subfilterOk = filter !== 'product_comparison' || subfilter === 'all' || comparisonType === subfilter;
                var productOk = !selectedProduct || products.indexOf(selectedProduct) !== -1;
                var searchOk = !search || haystack.indexOf(search) !== -1;
                var show = filterOk && subfilterOk && productOk && searchOk;

                item.hidden = !show;
                if (show) {
                    visible += 1;
                }
            });

            if (subfilters) {
                subfilters.hidden = filter !== 'product_comparison';
            }
            if (empty) {
                empty.hidden = visible !== 0;
            }
        }

        filterButtons.forEach(function (button) {
            button.addEventListener('click', function () {
                filter = button.getAttribute('data-upc-filter') || 'all';
                if (filter !== 'product_comparison') {
                    subfilter = 'all';
                    setPressed(subfilterButtons, subfilter, 'data-upc-subfilter');
                }
                setPressed(filterButtons, filter, 'data-upc-filter');
                apply();
            });
        });

        subfilterButtons.forEach(function (button) {
            button.addEventListener('click', function () {
                subfilter = button.getAttribute('data-upc-subfilter') || 'all';
                setPressed(subfilterButtons, subfilter, 'data-upc-subfilter');
                apply();
            });
        });

        productButtons.forEach(function (button) {
            button.addEventListener('click', function () {
                var next = button.getAttribute('data-upc-product') || '';
                selectedProduct = selectedProduct === next ? '' : next;
                productButtons.forEach(function (candidate) {
                    candidate.setAttribute(
                        'aria-pressed',
                        selectedProduct && candidate.getAttribute('data-upc-product') === selectedProduct ? 'true' : 'false'
                    );
                });
                apply();
            });
        });

        if (input) {
            input.addEventListener('input', function () {
                search = normalize(input.value);
                apply();
            });
        }

        apply();
    }

    document.addEventListener('DOMContentLoaded', function () {
        Array.prototype.forEach.call(document.querySelectorAll('[data-upc-archive]'), init);
    });
}());
