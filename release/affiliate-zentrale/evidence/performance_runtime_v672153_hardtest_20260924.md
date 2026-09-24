# Affiliate Performance Block A – Runtime Reuse 6.72.153 – 2026-09-24

Status: **HARDTEST PASS / REAL SERVER READBACK REQUIRED**

## Basis

Messquelle: `performance-diagnose-safe-20260924-121142.json`

Belegte Hotspots:
- sehr hohe request-lokale `sanitize_key`-Last im Affiliate Router;
- wiederholte Normalisierung identischer Kampagnenwerte;
- identische Runtime-Slotregel wurde innerhalb desselben Frontend-Requests erneut aufgebaut.

## Kandidat

Version: **6.72.153**

Installierbares ZIP:
`AFFILIATE_ZENTRALE_V6.72.153_PERFORMANCE_RUNTIME_HARDTEST.zip`

SHA256:
`209c70886fcd7b17ead16efb0440a877fb7cafb28a91460bd9cf7baeba703600`

Aenderungsgrenze:
- exakt **eine** Plugin-Datei geaendert: `pferdeportal-affiliate-router.php`;
- Kategorie-/Struktur-JSONs und alle 30 weiteren Dateien bleiben byteidentisch;
- keine Inhalts-, Design-, Ranking-, Provider-, Slot-, Veto-, Publish- oder Kategorienregel geaendert.

## Performance-Aenderungen

1. `campaign_from_post()` behaelt bereits normalisierte request-lokale Kampagnenwerte.
2. Ranking nutzt diese Werte erneut statt identische Scalars je Slot erneut zu sanitizen.
3. `campaign_is_complete()` nutzt den vorhandenen normalisierten Assignment-Wert.
4. Runtime-Slotregel wird im normalen Frontend request-lokal je Slot wiederverwendet.
5. Admin/Cron/REST/WP-CLI/AJAX bleiben auf der bisherigen ungecachten Semantik.

## Hardtest

Workflow:
`Affiliate Performance Runtime V672153 Hardtest`

Finaler Run:
`36023528874`

Result:
**SUCCESS**

Geprueft:
- isolierte exakte 6.72.152 Quelle -> 6.72.153 Patch;
- Ein-Datei-Delta;
- PHP-Lint aller Kandidatendateien;
- bestehende Affiliate-Performance-Marker erhalten;
- Bannerregression PASS;
- WordPress 7.1.2 + PHP 8.3 + MariaDB 10.11;
- fachliche Gleichheit der betroffenen Campaign-/Slot-Pruefungen;
- Normalisierungstest: 500 Durchlaeufe alt = 3000 zusaetzliche `sanitize_key`, neu = 0;
- Frontend-Slotregelcache greift;
- Admin bleibt absichtlich ungecached.

## Naechster Schritt

Exakt dieses ZIP als Server-Teststand installieren und mit demselben Performance-Diagnoseplugin dieselben Seiten erneut messen.

Bis zu diesem echten Server-Readback:
- **kein Block B**;
- keine Cache-/Kubio-/Astra-/HivePress-Aenderung;
- 6.72.153 ist **HARDTEST PASS**, noch kein finaler Performance-Live-PASS.
