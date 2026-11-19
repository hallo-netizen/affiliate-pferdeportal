# Pferdeatelier – Performance Zwischenstand
Stand: 2026-11-19 16:38 Europe/Berlin

## Installierter und geprüfter Stand
- Affiliate-Zentrale: 6.72.361
- Template Kit: 1.50.616
- Performance Diagnose Safe: 6.0.0
- 6.72.360 ist ausdrücklich widerrufen / NICHT INSTALLIEREN.

## Was 6.72.361 bewiesen behebt
- Nur die verlorene request-lokale Wiederverwendung innerhalb `ebay_filter_ranked_product_candidates_provider_cohort()` für `category_product_1..3`.
- Finaler lokaler Paketbeweis: 10.894 Fälle / 26.630 Aufrufe / 0 Output-Abweichungen; eBay 35/35 PASS; Amazon/Idealo 15/15 PASS.
- Isolierter Funktionspfad: 33,551 ms -> 13,832 ms (-58,77 %), gleicher Ausgabe-Hash.
- Dieser Fix ist korrekt, aber live zu klein, um das Hauptproblem zu erklären.

## Live-Befund nach Installation 6.72.361
Pferdesättel: Ø 12.661,78 ms Gesamt, Ø 4.368,68 ms CPU, Ø 1.216,76 ms DB, 320 Queries, 138.150 Cache-Hits, 0 ms externe HTTP-Aufrufe.
Vorher 6.72.359: Ø 7.373,52 ms Gesamt, Ø 4.170,49 ms CPU, Ø 728,92 ms DB, 320 Queries, 138.129 Cache-Hits, 0 ms externe HTTP-Aufrufe.

Zusätzlicher Beleg im selben 6.72.361-Lauf, Seite ausruestung-sattel:
- 10.432,05 ms / CPU 2.740,28 / 298 Queries
- 3.768,06 ms / CPU 2.596,08 / 298 Queries
=> zusätzliche variable Warte-/Blockierzeit bei nahezu gleicher Programmarbeit; konkrete Ressource noch nicht bewiesen, daher kein Produktionsfix auf Verdacht.

## Feste Rechenlast – Fokus
- Pferdesättel ca. 4,37 s CPU
- ca. 138.150 interne Cachezugriffe
- `the_content` dominanter Inhaltsweg.
- Gemeinsamer Kandidatenbestand `category_product_shared_rank_base` wird bereits request-lokal nur einmal gebaut.

Spätere notwendige Facharbeit im Kategoriepfad:
1. `multiprovider_prefer_shared_offer_cards()`
2. mehrere Relevanzbänder
3. `product_fill_verified_portal_fallback_v672226()`
4. erweiterte Provider-/Relevanzmischung

## Nächster Prüfblock
- 6.72.361 gegen 6.72.211 und historischen Produktsnapshot.
- Mehranbieter-/GTIN-/Metadatenarbeit in category_product_1..3 isolieren.
- Nur bei bewiesener identischer Doppelarbeit + messbarem Effekt + identischer Ausgabe neuer Testkandidat.
- Kein Verlust von Fallback, Providerwahl, Reihenfolge, Veto, Health, Bild, Tracking oder Fachverhalten.

## Sperren
- Kein neues Diagnoseplugin.
- Kein weiterer Live-Seitenlade-Test als Voraussetzung.
- Kein Rollback Template 1.50.616.
- Kein Rückbau der Fachfunktionen ab 6.72.226 / 6.72.237.
- Kein Produktionsfix ohne Kausal- und Semantikbeweis.
