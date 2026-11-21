# Pferdeatelier Affiliate-Zentrale 6.72.371 – konsolidierter Root-Cause-Performance-Nachweis

Stand: 2026-11-21

## Ausgangspunkt
6.72.369 ist widerlegt und widerrufen. Der Live-PASSIV-Lauf zeigte gegenüber 6.72.367:
- Pferdesättel 320 -> 1421 Queries
- Ausrüstung/Sattel 298 -> 838
- Trensen & Gebisse 296 -> 828
- Satteldecken 311 -> 734

6.72.370 nahm den Narrow-Meta-Fehler vollständig zurück. 6.72.371 baut ausschließlich auf diesem query-sicheren Stand auf.

Der Ursachenprofil-Lauf lokalisiert die feste Rechenlast im Affiliate-Ausgabepfad:
- the_content gesamt 17.951,59 ms
- Priorität 20 / Pferdeportal_Affiliate_Router::filter_the_content 14.139,88 ms
- category_product_1 bis 1.684,42 ms
- hub_after_cards bis 582,41 ms
- start_after_topics bis 575,70 ms
- product_after_category_tiles ca. 450,94 ms
- journal_product_1 ca. 658,73 ms
Diese Werte sind Attributionswerte, keine Live-Walltime-Prognose.

## Rootfix A – automatische Banner vor Vollnormalisierung sicher aussortieren
Der allgemeine Kandidatenpfad normalisierte automatische Banner vollständig, bevor zwei bereits bindende Ausschlussregeln geprüft wurden:
1. automatische Banner müssen source=output_object_v4 besitzen;
2. der bestehende technische Slotvertrag muss erfüllt sein.

6.72.371 verschiebt nur diese identische sichere Ablehnung vor die Vollnormalisierung. Forced/fixed campaigns sind ausgenommen.

Alt/Neu:
- 300.000 Einzelkampagnen: 0 Abweichungen
- 5.000 Listen × 213 Banner: 0 Ergebnislisten-Abweichungen
- 500.000 Source+Format-Fälle inkl. forced path: 0 Abweichungen
- synthetische Vollnormalisierungen im erweiterten Harness 500.000 -> 26.597 (-94,68 %)
Die Prozentzahl gilt nur für den Testmix.

## Rootfix B – Control/Health derselben Kampagne nicht slotweise wiederholen
Der allgemeine öffentliche Rankingpfad führte dieselbe Basis-Control- und Health-Prüfung bei jedem Slot erneut aus. Nur das Slot-Veto ist slotbezogen.

6.72.371 im stabilen normalen Frontend:
- Control-Basis einmal je Kampagne
- Health einmal je Kampagne
- Slot-Veto einmal je Slot
Dynamische Filter/Meta/Option/Cache/Sanitizer/Shortcode/URL/Redirect/Host-Zustände verwenden den historischen Pfad.

Breite Simulation:
- 100.000 stabile Fälle: 0 Ausgabeabweichungen
- Base-Control -77,31 %
- Health -76,39 %
- Slot-Veto -95,64 %
- 50.000 dynamische Fälle: 0 Ausgabe-/Aufruffolgeabweichungen

Im eingebetteten historischen Pferdeatelier-Snapshot:
- 2.012 Produktkampagnen, 1.518 aktiv
- 1.985 gleichzeitig auf hub_product_1..3
- 895 gleichzeitig auf journal_product_1..3
- 608 reale Zielschlüssel

5.000 echte Zielkontexte:
- Hub: 0 Ergebnisabweichungen; Base -66,67 %, Health -65,67 %, Slot-Veto -94,11 %
- Journal: 0 Ergebnisabweichungen; Base -66,67 %, Health -65,76 %, Slot-Veto -80,20 %
Der Snapshot dient nur als Struktur-/Wiederholungsbeleg.

## Beibehaltener Bildcache
Der getestete 6.72.370-Bildcache ist in 6.72.371 unverändert. Exakte relevante Methodenhashes sind identisch.

## Query-Regression ausgeschlossen
Die drei Metadatenfunktionen sind 6.72.370 -> 6.72.371 identisch:
- ranked_campaign_posts_snapshot()
- ranked_campaign_raw_records_snapshot()
- campaign_from_post()
Kein update_post_meta_cache=false und keine Narrow-Meta-Helfer.

## Inhaltlicher Funktionsschutz
- PHP-Dateien 23 -> 23
- Dateien entfernt 0, neu 0
- vorhandene benannte Funktionen entfernt 0
- neu nur 2 interne Performance-/Sicherheitshelfer
- bestehende Funktionskörper geändert nur ranked_campaign_candidate_pool() und ranked_campaigns_for_slot_uncached()
- Actions 176 -> 176
- Filter 30 -> 30
- Shortcodes 6 -> 6
- alle geprüften Produktions-Schreibwege identisch
- Auswahl, Ranking, Provider, Placement, Fallback, Veto/Control, Health, Tracking, Inhalt, Rendering unverändert
- Design 1.50.616 und Diagnose 7.0.0 unangetastet

## Paket
PFERDEATELIER_AFFILIATE_6.72.371_KONSOLIDIERT_ROOTCAUSE_PERFORMANCE.zip
SHA-256: 832b7b82f1b190e06250cab922b4e9ab6ee0abb7661097991ae7eca7ce87a456
- 66/66 Dateien identisch zum geprüften Arbeitsstand
- 23/23 PHP-Lint PASS
- Version/Stable Tag 6.72.371

## Live-Freigabe
6.72.371 ist lokaler Testkandidat, kein behaupteter Live-Gesamtspeedup.
Nach Installation genau ein PASSIV-Gesamtlauf. Zuerst Queries, CPU, Cache-Hits und Inhaltsphasen vergleichen; Wall-Time wegen schwankender Serverlast nicht allein bewerten.