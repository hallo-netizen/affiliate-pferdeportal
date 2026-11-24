# Pferdeatelier Affiliate-Zentrale 6.72.375 – gebündelter Meta-/Options-Read-Rootfix

Stand: 24.11.2026
Basis: exakt 6.72.374
Paket: PFERDEATELIER_AFFILIATE_6.72.375_GEBUENDELT_META_READ_ROOTFIX.zip
SHA-256: f0c813dc1b5d0de01e45f15b6a3f0bdf725ff721f6f7e3f71da10754e80c86a4

## Live-Ausgangslage 6.72.374
PASSIV 20261124-100752:
- Pferdesättel 3.495,84 ms Wall / 1.296,52 ms CPU / 135.828 Cache-Hits / 310 Queries.
- Gegen 6.72.373: CPU ca. -7,4 %, Cache-Hits praktisch unverändert, Queries unverändert.
- Schluss: 6.72.374 wirkt klein auf CPU, Hauptrest der Wiederholungsarbeit bleibt.

## Vier gemeinsam behobene, reproduzierte Restursachen
Realbestand Pferdesättel: 1.010 aktive relevante Produktkampagnen, 617 idealo + 393 eBay.

1. Doppelte Kampagnendaten-Lesung:
- 1.091 zusätzliche ppar_campaign_data-Metalesungen -> 0.
- Shared Base bleibt 1.010/1.010 identisch.

2. Incident-Evidence:
- 81 Kandidaten x 8 globale Optionen = 648 Lesungen -> 8.
- Bei dynamischem Incident-Optionfilter historischer Pfad: 648 -> 648.

3. Einzel-Metalesungen im ersten vollständigen Produktdurchlauf:
- 7.983 get_post_meta-Aufrufe -> 1.010 vollständige Kandidaten-Snapshots.
- nur innerhalb stabilem category_product_1..3-Scope.
- außerhalb Scope sowie bei dynamischen Metadata-Hooks/external object cache historischer Einzelpfad.
- registrierte Defaults, serialisierte und Multi-Metawerte inhaltlich erhalten.

4. eBay Public Checkpoint:
- 393 Checkpoint-Optionslesungen -> 1 im stabilen Kategoriepfad.
- bei checkpoint-spezifischem Optionfilter 393 -> 393.
- außerhalb Kategorie-Scope 3 Direktaufrufe Alt 3 / Neu 3.

## Reproduzierte Gesamtwirkung im exakten Realbestands-Harness
6.72.374:
- Shared Base 1.091 Meta + 648 Option.
- voller Auswahlpfad 7.983 Meta + 407 Option.
- zusammen 10.129 Meta-/Optionslesungen.

6.72.375:
- Shared Base 0 Meta + 8 Option.
- voller Auswahlpfad 1.010 Meta + 15 Option.
- zusammen 1.033 Meta-/Optionslesungen.

Reduktion:
- Meta 9.074 -> 1.010 = ca. -88,9 %.
- Option 1.055 -> 23 = ca. -97,8 %.
- zusammen 10.129 -> 1.033 = ca. -89,8 %.

Dies sind exakte lokale Funktionsaufrufe im Realbestands-Harness, nicht behauptete Live-Cache-Hits. Live-Speedup erst nach PASSIV.

## Inhaltlicher Funktionsbeweis
- 2.721/2.721 Kampagnennormalisierungen identisch; derselbe SHA-256.
- direkte stored-Normalisierung 2.721/2.721 ebenfalls derselbe Hash.
- Pferdesättel Shared Base 1.010/1.010, Reihenfolge/Inhalt identisch.
- Standard-Postprocessing 315/315, kompletter geordneter Output identisch.
- finale Slots 1/2/3 Standardfall identisch.
- 30/30 Kombinationen Provider-Modus x Linkstrategie x Amazon aus/an: kompletter Postprocessing-Output Alt=Neu.
- 10 repräsentative Randkombinationen mit finaler Slotauswahl: 0 Abweichungen.
- 1.010 Control-/Health-Entscheidungen außerhalb Snapshot-Scope: identischer Hash und identische historische Einzelaufrufzahlen.
- synthetisches AWIN/Otto-Auto, DFS-Amazon-ASIN und eBay Public Source Row außerhalb Scope: Alt=Neu.

## Meta-Härtetest und dynamische Zustände
- 10.000 Fälle: Strings, serialisierte Integer/Booleans/Arrays, Multi-Werte, fehlende Keys, registrierte Defaults, b:0; -> 0 Abweichungen.
- dynamischer Metadata-Zustandswechsel A->B bei get_post_metadata-Filter wird weiterhin als B gelesen.
- external object cache, get_post_metadata und global pre_option: vollständiger historischer Pfad, Alt/Neu-Aufrufzahlen identisch.
- default_post_metadata: historischer Meta-Einzelweg.
- checkpoint-spezifischer Optionfilter: 393 -> 393.
- incident-spezifischer Optionfilter: 81 -> 81.

## Vollständiger Plugin-Funktionsschutz
PHP-Tokenvergleich:
- Funktionen/Methoden 1.570 -> 1.581.
- entfernt 0.
- alle 1.570 alten weiterhin vorhanden.
- 1.555 bestehende token-inhaltlich unverändert.
- 15 gezielt geänderte bestehende Funktionen, ausschließlich in bewiesenen Lesewegen.
- 11 neue interne Schutz-/Cachehelfer.

Unverändert sind u.a.:
render_affiliate_slot_for_context, render_banner, build_click_tracking_url, campaign_slot_allowed, assignment_selection_for_slot, article_plan_apply_to_content, filter_the_content, campaign_match_rank, product_fill_verified_portal_fallback_v672226, product_campaign_public_image_ready, select_campaign_for_slot, control_provider_gate, control_partner_gate, category_product_postprocess_candidates_v672365.

## Hooks / Schreibwege / Paket
- Actions 176 -> 176; Filter 30 -> 30; Shortcodes 6 -> 6.
- alle geprüften Produktions-Schreibprimitive identisch.
- Dateien 66 -> 66; entfernt 0; hinzugefügt 0.
- geändert nur Hauptdatei, eBay, eBay-Run, idealo, DFS-Amazon, readme.
- keine Datei anderer Plugins/Themes/Core.
- PHP 23/23 PASS im Arbeitsstand und finalen ZIP.
- finales ZIP 66/66, 0 Hashabweichungen zum geprüften Arbeitsstand.
- Paketwurzel ausschließlich affiliate-portal-router/.
- Header/Klassenkonstante/Stable Tag 6.72.375.
- ZIP-Integrität PASS.

## Freigabegrenze
6.72.375 ist ein einziger gebündelter lokaler Rootfix-Kandidat mit vier belegten Änderungen. Kein Live-Speedup wird vor dem kontrollierten PASSIV-Lauf behauptet.
