# Pferdeatelier Affiliate-Zentrale 6.72.372 – gebündelter Hotpath-Rootfix

Stand: 2026-11-23
Basis: exakt freigegebene/installierte 6.72.371

## Gemessene Ursache
Ursachenprofil 2026-11-22 18:43:
- Pferdesättel: 8.539,76 ms Wall / 3.526,40 ms CPU / 139.475 Cache-Hits / 310 Queries.
- pp_affiliate_slot category_product_1: 17.856,88 ms gesamt bei 9 Aufrufen, Ø 1.984,10 ms, max. 7.585,31 ms.
- langsamer Artikel Eiweißüberschuss: 14.151,54 ms; category_product_1 allein 7.585,31 ms.
Der 6.72.369-Queryfehler bleibt behoben. Geändert wird ausschließlich der gemessene Affiliate-Produkthotpath.

## Gebündelte, kausal belegte Änderungen
1. Normale Artikel-Posts: endgültige Automation-Nichttreffer kanonischer Produktkampagnen werden vor Vollnormalisierung verworfen. Realbestand 2.363 Produktkampagnen; alle page_tree, page_id=0, ohne Term-/Slug-/Keyword-Alternativbindung, mit automation_target_keys. 4.726 Hit/Miss-Fälle: 0 Abweichungen. 7.000 Legacy-Ausnahmen + 3.000 Sonder-Posttypen bleiben historisch: 0 Fehlablehnungen.
2. idealo-Strategie: pro synchronem Kandidatenlisten-Aufruf einmal statt je idealo-Kandidat lesen. Realpool 1.010 aktive Kandidaten / 617 idealo. products/comparison/hybrid jeweils 0 Ausgabeabweichungen, Reads 617 -> 1. Vier Zustandswechsel zwischen Slot-Aufrufen: 0 Abweichungen; jeder neue Aufruf liest erneut. Dynamischer Pfad bleibt historisch.
3. eBay-Titeldubletten: vorhandene mathematische Längen-Vorbedingung als exakter Index. Realpool 393 eBay-Kandidaten: Alt/Neu 315 Ausgaben, identischer Ausgabe-Hash; Paarprüfungen 78.355 -> 34.024 (-56,58 %), similar_text 21 -> 21. 53.444 Längenfälle und 250 randomisierte Listen / 12.725 Zeilen: 0 Abweichungen.
4. eBay-Source-Prime: bereits final gecachte post:<id>-Entscheidungen werden nicht erneut vorgeprimt. Realpool 393 eBay: bis 786 redundante Meta-Leseaufrufe pro späterem Prime entfallen. 16 Cache-/Rowzustände: 0 Ergebnisabweichungen.
5. Control: unmittelbar doppelte Providerprüfung nur im streng stabilen Frontend einmal ausführen. 192 Zustandskombinationen: 0 Ausgabeabweichungen; dynamischer/unsicherer Pfad bleibt exakt historisch.

## Inhaltlicher Funktionsschutz 6.72.371 -> 6.72.372
- Dateien 66 -> 66; entfernt 0; hinzugefügt 0; 61 unverändert.
- PHP-Dateien 23 -> 23.
- benannte Funktionen 1.564 -> 1.567; entfernt 0; neu nur 3 private Performance-Helfer.
- Properties 61 -> 61; entfernt 0; hinzugefügt 0.
- Actions 176 -> 176; Filter 30 -> 30; Shortcodes 6 -> 6.
- Produktions-Schreibprimitive vollständig identisch.
- Kritische Fachfunktionen körperidentisch: render_affiliate_slot_for_context, render_banner, build_click_tracking_url, campaign_slot_allowed, assignment_selection_for_slot, article_plan_apply_to_content, filter_the_content, select_category_product_campaign_fast_v672171, category_product_postprocess_candidates_v672365, campaign_match_rank, product_fill_verified_portal_fallback_v672226, category_product_provider_mix_v672133, campaign_health_allows_delivery, product_campaign_public_image_ready, select_campaign_for_slot.
- Keine Ranking-, Provider-, Placement-, Fallback-, Veto-, Health-, Bild-, Tracking-, Rendering-, Artikel- oder Schreibfunktion entfernt.
- Andere Plugins sind nicht Bestandteil des Pakets.

## Paket
PFERDEATELIER_AFFILIATE_6.72.372_GEBUENDELT_HOTPATH_ROOTFIX.zip
SHA-256: 745c8fcb4d047794fed37182dcd1881cb35a36e84f83b7aa906b9755dd3ed1fb
ZIP-Integrität PASS; 23/23 PHP-Lint PASS; Header/Klassenkonstante/Stable Tag 6.72.372.

## Freigabegrenze
Lokaler, inhaltlich geprüfter Testkandidat. Nach Installation nur einen PASSIV-Gesamtlauf; Live-Gesamtspeedup wird vorher nicht behauptet.