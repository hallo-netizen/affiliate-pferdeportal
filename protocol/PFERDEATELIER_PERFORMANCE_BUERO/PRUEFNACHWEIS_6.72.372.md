# Pferdeatelier Affiliate-Zentrale 6.72.372 – gebündelter Hotpath-Rootfix – Prüfnachweis

Stand: 2026-11-23
Basis: exakt freigegebene/installierte 6.72.371
Paket: `PFERDEATELIER_AFFILIATE_6.72.372_GEBUENDELT_HOTPATH_ROOTFIX.zip`
SHA-256: `745c8fcb4d047794fed37182dcd1881cb35a36e84f83b7aa906b9755dd3ed1fb`

## 1. Gemessene Ursache
Der Ursachenprofil-Lauf `pferdeatelier-performance-gesamtanalyse-20261122-184331.json` lokalisiert die Restlast weiterhin im Affiliate-Produktpfad:
- Pferdesättel: 8.539,76 ms Wall, 3.526,40 ms CPU, 139.475 interne Cache-Hits, 310 Queries.
- `pp_affiliate_slot category_product_1`: über den Lauf 9 Aufrufe, 17.856,88 ms gesamt, 1.984,10 ms je Aufruf, Maximum 7.585,31 ms.
- `category_product_2`: 2.684,18 ms gesamt; `category_product_3`: 3.172,45 ms gesamt.
- Der langsame Artikel `welche-symptome-zeigen-pferde-bei-einem-eiweissueberschuss`: 14.151,54 ms Gesamtzeit; `category_product_1` allein 7.585,31 ms.
- Der alte 6.72.369-Queryfehler ist nicht zurück: Pferdesättel liegt bei 310 Queries.

Damit ist der geänderte Bereich nicht geraten: 6.72.372 verändert ausschließlich wiederholte Arbeit innerhalb dieses bereits gemessenen Affiliate-Hotpaths. Template, Journal, HivePress, Texterstellung und andere Plugins werden nicht geändert.

## 1a. Kausalitätsbeweis je einzelner Änderung
Der Live-Ursachenlauf beweist zuerst den betroffenen Produktionspfad: `pp_affiliate_slot` / `category_product_1..3` ist direkt gemessen langsam. Die folgenden Alt/Neu-Prüfungen verändern jeweils nur eine konkrete Wiederholung innerhalb genau dieses Pfads.

| Änderung | Direkter Ursachenbeweis | Alt -> Neu | Inhaltsbeweis |
|---|---|---:|---|
| A Frühablehnung endgültiger Artikel-Nichttreffer | 2.363 reale Produktkampagnen laufen bei Automation-Nichttreffer im Altweg noch in Vollnormalisierung/Ranking, obwohl der spätere Rank für die reale Struktur nicht mehr gewinnen kann | für diese Nichttreffer: Vollnormalisierung/Ranking entfällt vollständig | 4.726 Real-Hit/Miss-Fälle + 7.000 Legacy-Ausnahmen + 3.000 Sonder-Posttypen: 0 Abweichungen |
| B idealo-Strategie | im realen Kandidatenpool 617 idealo-Kandidaten lesen innerhalb eines synchronen Listenaufrufs denselben unveränderten Strategiewert wiederholt | 617 Reads -> 1 Read je Listenaufruf | products/comparison/hybrid identische IDs/Reihenfolge; 4 Zustandswechsel zwischen Slots + 500 Zufallsfälle: 0 Abweichungen |
| C eBay-Titeldubletten | die bestehende zwingende Längenbedingung wurde als mathematisch äquivalenter Vorindex benutzt | 78.355 -> 34.024 Paarprüfungen; isoliert ca. 88,1 -> 49,0 ms; `similar_text` bleibt 21 -> 21 | Realpool 393 Kandidaten, identischer Ausgabehash; 53.444 Längenfälle + 12.725 Zufallszeilen: 0 Abweichungen |
| D eBay-Source-Prime | bei vorhandener finaler `post:<id>`-Source-Entscheidung konsultiert der spätere Gate-Code den erneut geprimten Row nicht mehr | bis zu 786 redundante Meta-Leseaufrufe pro späterem Prime entfallen | 16 Cache-/Rowzustände: 0 Ergebnisabweichungen; erster noch unentschiedener Aufruf unverändert |
| E doppelte Providerprüfung | `campaign_control_base_allows_delivery()` prüft Provider und `control_partner_gate()` unmittelbar danach denselben Provider nochmals | Matrix Provider-Gate-Aufrufe 288 -> 192; erfolgreicher Pfad 2 -> 1 | 192 Kombinationen + dynamischer Altweg: 0 Ergebnisabweichungen |

Wichtig: Damit ist die Ursächlichkeit der entfernten Wiederholungsarbeit im gemessenen langsamen Hotpath belegt. Nicht vorweggenommen wird die Höhe des gesamten Live-Seitenspeedups; dafür dient anschließend der eine kontrollierte PASSIV-Lauf.

## 2. Inhaltlicher Funktionsschutz
Exakter PHP-Tokenvergleich 6.72.371 -> 6.72.372:
- benannte PHP-Funktionen: 1.560 -> 1.563
- bestehende Funktionen entfernt: 0
- bestehende Funktionen vollständig weiter vorhanden: 1.560/1.560
- davon funktional geändert: genau 6
- unverändert: 1.554
- neue interne Helfer genau 3:
  - `category_product_raw_nonmatch_final_v672372`
  - `control_partner_gate_after_provider_v672372`
  - `ebay_topic_duplicate_against_seen_v672372`

Funktional geändert wurden ausschließlich:
- `category_product_shared_rank_base`
- `campaign_control_base_allows_delivery`
- `multiprovider_filter_candidates_by_strategy`
- `ebay_topic_titles_duplicate_v672146`
- `ebay_filter_ranked_product_candidates_provider_cohort`
- `ebay_prime_business_campaign_source_row_cache_for_campaigns`

Kritische Fachfunktionen sind körperidentisch, u.a.:
- `render_affiliate_slot_for_context`
- `render_banner`
- `build_click_tracking_url`
- `campaign_slot_allowed`
- `assignment_selection_for_slot`
- `article_plan_apply_to_content`
- `filter_the_content`
- `select_category_product_campaign_fast_v672171`
- `category_product_postprocess_candidates_v672365`
- `campaign_match_rank`
- `product_fill_verified_portal_fallback_v672226`
- `category_product_provider_mix_v672133`
- `campaign_health_allows_delivery`
- `product_campaign_public_image_ready`
- `select_campaign_for_slot`

Struktur-/Integrationsschutz:
- Dateien: 66 -> 66; entfernt 0; hinzugefügt 0; 61/66 byteidentisch
- PHP-Dateien: 23 -> 23
- Actions: 176 -> 176
- Filter: 30 -> 30
- Shortcodes: 6 -> 6
- Klassen-/Trait-Properties: 61 -> 61; entfernt 0; hinzugefügt 0
- Produktions-Schreibprimitive vollständig identisch

Zusatzbeweis „kein anderes Plugin“:
- Beide ZIPs enthalten als einzigen Plugin-Wurzelordner `affiliate-portal-router/`.
- geändert sind nur vier PHP-Dateien innerhalb dieses Ordners plus `readme.txt`.
- keine Datei von Template-Kit, HivePress, Texterstellung, Theme oder WordPress-Core ist Bestandteil des Pakets.

## 3. Paketprüfung
- ZIP-Integrität: PASS
- 66 Dateien im ZIP
- 23 PHP-Dateien im ZIP
- PHP-Lint: 23/23 PASS
- Plugin-Header: 6.72.372
- Klassenkonstante: 6.72.372
- Stable Tag: 6.72.372
- SHA-256: `745c8fcb4d047794fed37182dcd1881cb35a36e84f83b7aa906b9755dd3ed1fb`

## 4. Freigabegrenze
6.72.372 ist inhaltlich und lokal als gebündelter Testkandidat freigegeben. Ein realer Live-Gesamtspeedup wird erst nach genau einem PASSIV-Lauf auf der installierten Version behauptet.