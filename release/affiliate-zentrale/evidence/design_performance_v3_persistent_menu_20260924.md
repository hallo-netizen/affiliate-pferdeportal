# Design Performance V3 Persistent Menu – 2026-09-24

Status: **HARDTEST PASS / REAL SERVER READBACK NEXT**

## Ziel

Den belegten Template-Kit/WordPress-Menue-Hotspot reduzieren, ohne PPA-013 1.50.559 selbst zu veraendern.

## Kandidat

Plugin:
`pa-affiliate-design-performance`

Version:
**3.0.0**

Branch:
`affiliate-performance-menu-persistent-hardtest-20260924`

Workflow:
`Design Performance V3 Persistent Menu Hardtest`

PASS Run:
**36033879960**

Installierbares ZIP:
`PA_AFFILIATE_DESIGN_PERFORMANCE_3.0.0_PERSISTENT_MENU_HARDTEST.zip`

SHA256:
`2db4a035b83849dbfec048e8821d6990e670d2f145f37d63f5e58ce1717bc1fb`

## Verhalten

- PPA-013 / Template Kit bleibt byte-unveraendert.
- WordPress-Core-Setup der identischen 1550 Menuepunkte wird nach einem kalten Frontend-Aufbau persistent wiederverwendet.
- Die normalen `wp_setup_nav_menu_item`-Filter laufen weiterhin bei jedem Render.
- Desktop/Mobile/Astra-HTML bleibt im Hardtest hash-identisch.
- Cache wird bei Post-, Menue-, Term-, Plugin-, Theme-, Permalink-, Home- oder Site-URL-Aenderungen invalidiert.
- Admin, Cron, REST, WP-CLI und AJAX nutzen den persistenten Cache nicht.

## Hardtest-Messung

1550 Menuepunkte, WordPress 7.1.2 / PHP 8.3 / MariaDB 10.11.

`get_post_metadata` Hook-Aufrufe:
- ohne Helper: **97,650**
- V3 erster kalter Request: **41,850**
- V3 warmer Request: **13,950**

Warm gegen Baseline:
**85.7% weniger Meta-Hook-Arbeit**

Weitere Gates:
- Desktop HTML identisch: PASS
- Mobile HTML identisch: PASS
- Astra HTML identisch: PASS
- Setup-Filter-Hitcount identisch: PASS
- Admin bypass: PASS
- Menueaenderung sichtbar nach Invalidation: PASS
- nach Invalidation erneuter Warm-Cache-Aufbau: PASS

## Naechster Schritt

Bestehenden `pa-affiliate-design-performance` 2.0.0 durch 3.0.0 ersetzen.
Danach einmal eine normale Frontend-Seite aufrufen, damit der persistente Menuecache aufgebaut wird.
Dann genau eine gemeinsame Performance-Diagnose als Server-Zwischenpruefung.

Keine weiteren Performance-Aenderungen vor diesem Readback.
