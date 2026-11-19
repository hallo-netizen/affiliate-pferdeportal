# Pferdeatelier – Performance – aktueller Stand

Stand: 2026-11-19 15:04 Europe/Berlin

## Installierter und geprüfter Stand
- Affiliate-Zentrale 6.72.361 ist live installiert.
- Affiliate Portal Template Kit 1.50.616 ist installiert und bleibt geschützt.
- Performance Diagnose Safe 6.0.0 ist installiert; 6.1 wird nicht verwendet.
- 6.72.360 ist widerrufen und darf nicht installiert werden.

## Bewiesener 6.72.361-Fix
6.72.361 behebt ausschließlich die nachgewiesene verlorene request-lokale Wiederverwendung in `ebay_filter_ranked_product_candidates_provider_cohort()` für `category_product_1..3`.
- 10.894 lokale Matrixfälle / 26.630 Aufrufe: 0 Output-Abweichungen.
- eBay-Fachtest 35/35 PASS, Amazon/idealo 15/15 PASS.
- isolierter 710-Kandidaten-Pfad: 33,551 ms -> 13,832 ms, gleicher Output-Hash.
- Der Fix ist real, erklärt aber nicht die mehrsekündige Hauptlast der Live-Seite.

## Live-Beweis nach Installation 6.72.361
Bericht: `pferdeatelier-performance-gesamtanalyse-20261119-112110.json`.
- Pferdesättel: 2 Frontend-Aufrufe, Ø 12.661,78 ms, Ø CPU 4.368,68 ms, 320 Queries, Ø DB 1.216,76 ms, Ø interne Cache-Hits 138.150, externe HTTP 0 ms.
- Vorheriger 6.72.359-Vergleich: Ø 7.373,52 ms, Ø CPU 4.170,49 ms, 320 Queries, Ø DB 728,92 ms, Ø Cache-Hits 138.129, externe HTTP 0 ms.
- Damit bleibt die Arbeitsmenge nahezu gleich; der zusätzliche Wall-Time-Anteil ist nicht durch zusätzliche Affiliate-Rechenarbeit bewiesen.
- Derselbe Lauf zeigt `/ausruestung/ausruestung-sattel/` einmal mit 10.432,05 ms und kurz danach mit 3.768,06 ms bei jeweils 298 Queries und nahezu gleicher CPU-Zeit. Das beweist zusätzliche variable Wartezeit bei nahezu gleicher Arbeit.

## Harte Ausschlüsse
- Kein externer Provider-HTTP-Aufruf erklärt die Zielseiten: 0 ms.
- Footer ist nicht dominant.
- DB-Abfragezahl erklärt die Schwankung nicht: sie bleibt je Vergleichsseite gleich.
- 6.72.361 führt keine neue Gesamtbestands-Schleife oder neue Netzwerk-/DB-Schreibarbeit ein; der Mehrsekundenanstieg ist dadurch nicht belegt.
- Template 1.50.616 wird nicht zurückgebaut: der frühere Child-Page-N+1-Block ist nachweislich beseitigt und der aktuelle Template-Persistent-Cache ist gültig.

## Feste Restlast im Kategorie-Produktpfad
Der Kategorie-Renderer erzeugt im `the_content`-Pfad Banner + `category_product_1`, `_2`, `_3`.
Der gemeinsame Kandidatenaufbau `category_product_shared_rank_base()` wird bereits request-lokal einmal ausgeführt.
Nach diesem Shared-Base bleiben spätere Fachschritte, die seit 6.72.211 hinzugekommen/erweitert wurden:
1. eBay Provider-Cohort – dessen bewiesene Dreifacharbeit ist mit 6.72.361 korrigiert.
2. `multiprovider_prefer_shared_offer_cards()` – GTIN-/Provider-/Amazon-Identitätsbewertung.
3. Verarbeitung mehrerer Relevanzbänder statt früher Rückgabe am ersten geeigneten Band.
4. `product_fill_verified_portal_fallback_v672226()` bei weniger als drei Treffern.
5. erweiterter Provider-Mix.
Diese Funktionen sind fachlich gewollt und dürfen nicht zurückgebaut werden.

## Aktueller Arbeitsauftrag / nächste Prüfung
Ohne weiteren Live-Test und ohne neues Diagnoseplugin wird lokal auf dem exakten 6.72.361-Paket geprüft:
- welche der späteren Fachschritte mit identischen Eingaben mehrfach ausgeführt werden;
- wie groß deren isolierter Zeit-/Aufrufanteil ist;
- ob sichere request-lokale Wiederverwendung möglich ist;
- nur bei vollständigem Kausal- und Semantikbeweis darf eine Änderung entstehen.
`product_fill_verified_portal_fallback_v672226()` wird nicht pauschal über Slots gecacht, weil Placement/Control/Health/Bildprüfungen slotabhängig sind.