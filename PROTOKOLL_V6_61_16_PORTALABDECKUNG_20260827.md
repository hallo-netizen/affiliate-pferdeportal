# Affiliate-Zentrale V6.61.16 – Portalabdeckung

Stand: 27.08.2026
Status: LOCAL HARD PASS / LIVE COVERAGE DATA AWAITING EXPORT

## Ziel
Nach Live-PASS von V6.61.15 wird das Layout eingefroren. V6.61.16 dient ausschließlich der belastbaren Erfassung der tatsächlichen Produktabdeckung über den echten Live-Router und der textlichen Providerbezeichnung.

## Abdeckungsvertrag
- 329 Produktzielseiten im kanonischen Katalog.
- 311 verpflichtende physische Produktkonzepte.
- 13 Konzepte besitzen jeweils zwei Zielseiten; dadurch 324 physische Zielseiten mit Produktpflicht.
- 5 Grundlagen-/Informationsseiten sind bewusst ohne automatische Produktpflicht.

## Änderungen gegen V6.61.15
Exakt zwei Plugin-Dateien geändert:
- pferdeportal-affiliate-router.php
- readme.txt

17/19 Dateien byteidentisch, darunter frontend.css, frontend.js, eBay-Katalog, Portalstruktur, eBay-/idealo-Runtime, Provider-Registry und Output-Objects.

## Neuer read-only Audit
Backend: Affiliate-Zentrale -> Portalabdeckung.

Je physischem Produktziel werden category_product_1..3 über den echten Live-Router geprüft. Status: covered_3, partial, not_materialized, inactive_only, gated, page_missing, router_disabled oder excluded. Zusätzlich werden aktuell gebundene aktive/inaktive eBay-/idealo-Kampagnen ausgewiesen. JSON-Export verfügbar.

Der Snapshot enthält keine Schreib-, Feed-, Materialisierungs- oder Providerlauf-Aufrufe. Kein eBay-/idealo-Lauf wird durch Öffnen oder Exportieren gestartet.

## CTA-Vertrag
- idealo: Bei idealo vergleichen
- eBay: Bei eBay ansehen
- sonstige Provider: Zum Angebot

Die Korrektur greift nach der späten Design-DOM-Transformation nur auf den CTA-Text.

## Lokale Gates
- PHP-Lint 14/14 PASS.
- Abdeckungsvertrag 329 / 311 / 324 / 5 PASS.
- Read-only statisch: 0 Mutationsaufrufe innerhalb portal_coverage_snapshot() PASS.
- V6.61.15 Layout-CSS/JS byteidentisch PASS.
- Gespeicherte echte Live-HTML: 10 Breiten, Geometrie vor/nach CTA-Normalisierung identisch; idealo/eBay-Bezeichnungen korrekt PASS.
- Fresh-Unpack 19/19 hashidentisch PASS.

Installer: affiliate-zentrale_v6.61.16_PORTALABDECKUNG_READONLY_HARD_VERIFIED.zip
SHA-256: 98c6faf6c8d49c57bc68f1031a7dea036fa137f4492ebbceb9b71973d5e2887c

MASTER: MASTER_AFFILIATE_ZENTRALE_V6_61_16_PORTALABDECKUNG_20260827.zip
SHA-256: be6361b1cbc21c6f9c93b635dde9177f73836c75259051fa1ee2d3bb4172e7ae

## Nächster Live-Schritt
V6.61.16 installieren, Portalabdeckung öffnen und genau einen JSON-Prüfbericht exportieren. Dieser Bericht ist der Nullpunkt für die globale Reparatur der Versorgungslücken. Erst danach werden gezielt Provider-/Matching-Ursachen behoben. Anschließend folgt Digistore24.
