# Pferdeatelier Affiliate 6.72.367 – Prüfnachweis

Stand: 2026-11-21

## Ursache
Live 6.72.365: Pferdesättel 5721,16 ms Wall, 3264,16 ms CPU, 139257 interne Cache-Hits; loop_start→wp_footer 3977,27 ms. Der vorhandene category_product-Postprocess-Plan wurde auf normalen WordPress-Single-Sites blockiert, weil der WordPress-Standardcallback allowed_http_request_hosts auf http_request_host_is_external als Fremdeingriff behandelt wurde.

## Konsolidierter Fix
6.72.367 gibt ausschließlich den Postprocess-Plan im normalen Single-Site-WordPress-Standardfall frei. Multisite, zusätzliche/unklare Host-Callbacks sowie dynamische URL-/Redirect-/Option-/Meta-/Cache-/Sanitizer-/Shortcode-Filter behalten den historischen vollständigen Pfad. Der separate Bildresultat-Cache bleibt exakt auf 6.72.365-Semantik.

## Kausalitätsbeweis
710 Kandidaten, category_product_1/2/3, normaler WordPress-Standardfilter:
- 6.72.365: 3 vollständige Postprocess-Durchläufe
- 6.72.367: 1 vollständiger Durchlauf + 2 Plan-Replays
- Bildprüfungen im Testpfad: 1332 → 444
- identischer Ausgabehash: b775de9f0e950581b56350ff0e374948b3ce16865351cfea8820c765620630b4

## Inhaltlicher Funktionsbeweis
- 353 vorhandene Methoden, 0 entfernt
- 1 neue private Sicherheits-Hilfsmethode
- inhaltlich geändert nur category_product_postprocess_plan_cache_allowed_v672365
- Auswahl, Control/Veto, Health, Fallback, Bildentscheidung, Slot-Auswahl und Kampagnenauswahl unverändert
- 12960 Gate-Kombinationen: 0 unerwartete Abweichungen
- 60000 Alt/Neu-Ausgaben: 0 Ausgabeabweichungen
- 30 dynamische Zustandswechsel-Fälle: 0 Abweichungen

## Struktur-/Schreibschutz
- 66→66 Dateien, 0 entfernt, 0 hinzugefügt
- Actions 176→176, Filter 30→30, Shortcodes 6→6
- Produktions-Schreibprimitive identisch
- 23/23 PHP-Lint PASS
- finales ZIP 66/66 identisch zum geprüften Arbeitsstand

## Paket
PFERDEATELIER_AFFILIATE_6.72.367_KONSOLIDIERT_SEMANTIC_SAFE_PERFORMANCE_ROOTFIX.zip
SHA-256: 88deb31196e7ed3134e5ff11654c4d522c09949cd21189eb44f52c332ee2e14e
Library: /pferdeatelier/PLUGINS/PERFORMANCE/

6.72.366 ist widerrufen / NICHT INSTALLIEREN.
