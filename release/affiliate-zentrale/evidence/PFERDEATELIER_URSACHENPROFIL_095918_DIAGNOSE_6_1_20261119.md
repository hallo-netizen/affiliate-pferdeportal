# Pferdeatelier – Ursachenprofil 09:59 / Performance Diagnose Safe 6.1.0

Stand: 2026-11-19

## Gemessener Stand
- Diagnose: 6.0.0, Modus URSACHENPROFIL
- Affiliate-Zentrale: 6.72.359
- Template-Kit: 1.50.616

## Harte Messbeweise
- /ausruestung/: Ø 3120,78 ms gesamt; the_content Ø 958,92 ms.
- /ausruestung/ausruestung-sattel/: Ø 5365,90 ms; the_content Ø 2326,70 ms.
- /ausruestung/ausruestung-sattel/pferdesaettel/: Ø 7373,51 ms; the_content Ø 5394,83 ms = 73,1 %.
- Pferdesättel DB Ø 728,91 ms; damit erklärt DB allein den zusätzlichen Mehrsekundenblock nicht.
- OPcache Ende 99,11 %, max. zwei parallele Requests.

## Quellbeweis des noch blinden Unterpfads
Template 1.50.616 rendert die Page-Kategorie über:
auto_append_category_tiles_to_content -> render_category_level_v150269 -> category_affiliate_layout_v150341.

Dort:
- Banner: render_design_affiliate_slot -> do_shortcode(pp_affiliate_slot)
- Produkte: category_real_affiliate_products_only_v150341 -> drei direkte pp_affiliate_slot-Shortcodes für category_product_1..3.

Affiliate 6.72.359:
pp_affiliate_slot -> shortcode_affiliate_slot -> render_affiliate_slot -> render_affiliate_slot_for_context -> select_campaign_for_slot -> bei category_product_1..3 select_category_product_campaign_fast_v672171.

6.0 maß the_content und PFTK-Leaf-Hooks, aber nicht die direkte Shortcode-Ausführungszeit. Deshalb war der Gesamtblock bewiesen, nicht der Anteil jedes einzelnen Slots.

## Diagnose 6.1.0
Paket: PERFORMANCE_DIAGNOSE_SAFE_6.1.0_ALL_IN_ONE.zip
SHA-256: 58effb9f9ec7eb2d9bd1f3f0eba2cd9a0785b404bc64c6169e5e9688b346fd09
Source SHA-256: f5a065ed3ecf60164248b81afd9640a34cb691bc1edb1fed396ecb758ae3052c

Funktionsschutz 6.0 -> 6.1:
- benannte Diagnosefunktionen: 134 -> 147
- entfernt: 0
- neu: 13
- geänderte bestehende Diagnosefunktionen: bootstrap, shutdown, build_findings, coverage, build_export, diagnostic_interference_proof_v50
- Affiliate-Zentrale: unverändert
- Template-Kit: unverändert
- keine neuen Post-/Term-/Meta-Writes
- keine Cron-Änderung
- kein Cache-Flush
- kein direkter DB-Write
- PHP-Lint PASS
- ZIP-Integrität PASS

Neu dauerhaft:
- echte Shortcode-Callback-Zeit für alle Shortcodes, pp_affiliate_slot mit type/intent getrennt
- the_content-Prioritätsblöcke
- the_content-Callback-Inventar
- alle bisherigen 6.0-Modi und Messungen bleiben erhalten

Lokale Pass-through-Simulation:
- Shortcode pre-filter unverändert
- Shortcode output identisch
- vorab beantworteter Shortcode unverändert
- the_content identisch

## Nächster Test
6.1.0 installieren -> URSACHENPROFIL -> Pferdesättel zweimal laden -> Export.
Erst danach Produktionsänderung.
