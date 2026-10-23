# HD-003 – EVIDENCE 1.50.716

STAND: 2026-10-23
STATUS: LOCAL HARD PASS / NICHT LIVE

Kandidat:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.716_UPDATE_MAGAZIN_STARTSEITE.zip`

SHA-256:
`072fdbe2fff7b8b4ef32ea3f70f08e1e1de700fb17d784b7e821e2735a1335f1`

Größe:
577,195 Bytes.

## Paket

UPDATE, kein FULL-Paket.

Enthält exakt zwei Dateien unter dem festen Hauptordner `affiliate-portal-template-kit/`:
- `pferde-template-kit.php`
- `includes/class-hobby-depot-profile-v150709.php`

## Magazin-Startseite

Die bestehende Seite `/magazin/` erhält eine eigene Hobby-Depot-Magazin-Root-Darstellung.

Verwendete bestehende 12 Magazin-Ziele, unverändert:
1. Hobbyfinder
2. Alter & Lebensphasen
3. Geschichte & Herkunft
4. Hobby-Porträts
5. Hobby-Ideen & Inspiration
6. Menschen & Geschichten
7. Neue Hobbys & Trends
8. Saison, drinnen & draußen
9. Ungewöhnliche & skurrile Hobbys
10. Vergleiche & Alternativen
11. Wissen & Glossar
12. Zeit, Budget & Platz

Keine neue Kategorie angelegt.

## Design

- Hero in der bestehenden Hobby-Depot-Formsprache;
- separates Magazin-Herobild aus dem vorhandenen Hobby-Depot-Assetbestand;
- 12 Bildkacheln, Desktop 3-spaltig, Tablet 2-spaltig, Mobil 2-spaltig;
- Farben, Typografie, Rundungen und Kartenlogik an HD-003 angelehnt;
- keine Übernahme des alten Pferde-Journal-Layouts.

## Monetarisierung

Vorhandene Slots werden genutzt:
- Banner: `journal_banner`
- Produkte: `journal_product_1`, `journal_product_2`, `journal_product_3`

Zusätzlich:
- Bereich für Affiliate-Artikel / Kaufberatung;
- bestehende Beiträge werden nur dann dort gezeigt, wenn sie per Meta oder vorhandenen Affiliate-Markern als Affiliate-Beitrag erkennbar sind;
- ohne Treffer bleibt der Bereich öffentlich unsichtbar; eingeloggte Nutzer sehen einen Prüfhinweis;
- direkter Werbeplatz über die bestehende Rental-Logik für Placement `journal`.

Keine neue Affiliate-Architektur und keine neuen Parallelslots.

## QA

- PHP-Lint vor Packen: PASS
- ZIP enthält exakt 2 Dateien: PASS
- Fresh-Unpack + PHP-Lint: PASS
- 13/13 verwendete Bildpfade im vorhandenen Assetbestand vorhanden: PASS
- Sonderroute nur für Seite mit Slug `magazin`: PASS
- `journal_banner` eingebunden: PASS
- drei `journal_product_*`-Slots eingebunden: PASS
- Affiliate-Artikel-Renderer eingebunden: PASS
- FAQ-Renderer aus 1.50.715 erhalten: PASS
- PB-one-Link öffnet weiterhin neues Fenster: PASS

Kein Live-PASS behaupten.
