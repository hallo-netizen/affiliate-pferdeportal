# Pferdeatelier Affiliate-Zentrale 6.72.374 – Provider-Control-Rootfix – Prüfnachweis

Stand: 24.11.2026
Basis: exakt installierte 6.72.373
Paket: PFERDEATELIER_AFFILIATE_6.72.374_PROVIDER_CONTROL_ROOTFIX.zip
SHA-256: 377683dd1e65ae586188e51f16e35e3a8f49d3257ea0cbfa516536c824dbe68b

## Live-Restproblem
PASSIV 6.72.373, Datei pferdeatelier-performance-gesamtanalyse-20261124-090340.json:
- Pferdesättel: 3.486,00 ms Wall / 1.400,20 ms CPU / 135.789 Cache-Hits / 310 Queries.
- Sattel-Elternseite: 1.886,62 / 1.050,89 / 81.262 / 288.
- Satteldecken: 1.779,48 / 876,98 / 84.833 / 301.
- Sattelgurte: 1.566,94 / 808,91 / 86.605 / 308.
6.72.373 hat den vorherigen DNS/Bild-Engpass klar beseitigt, aber Pferdesättel behält ca. 50.000 zusätzliche interne Cachezugriffe bei ähnlicher Queryzahl.

## Direkte Restursache
Echter WXR-Bestand:
- 1.010 aktive Produktkampagnen in derselben Pferdesättel-Fallback-Relevanzstufe.
- 617 idealo, 393 eBay.
- alle 1.010 mit Partner-/Advertiser-ID.

6.72.373 führt in campaign_control_base_allows_delivery() je Kandidat aus:
1. Notstopp lesen.
2. Portal-ID bestimmen.
3. control_provider_gate(provider, portal).
4. control_partner_gate(); dieser ruft control_provider_gate(provider, portal) nochmals auf.
Der schon vorhandene Doppelprüfungs-Schutz blieb live aus, weil die Affiliate-Zentrale selbst Provider-Registry-/Access-Filter registriert.

Die aktuell eingebauten Filter sind ausschließlich:
- PPAR_Affiliate_Source_Plan::extend_provider_registry
- digistore24_provider_registry
- idealo_provider_access_snapshot
- digistore24_provider_access_snapshot
Sie arbeiten auf Provider-/globalem Zustand und erhalten keine Produktkampagne. Jeder unbekannte zusätzliche Callback schaltet 6.72.374 automatisch auf den historischen Einzelpfad zurück.

## Kausalitätsbeweis am echten 1.010er-Pool
Mit den exakten 6.72.373-/6.72.374-Methoden:
- Provider-Channel-/Provider-Gate-Auswertungen: 2.020 -> 2.
- Provider-Access-Auswertungen: 2.020 -> 2.
- Notstopp-Leseweg: 1.010 -> 1.
- Portalbestimmung: 1.010 -> 1.
- Partnerentscheidungen: 2.020 -> 2.020.
- Creative-Entscheidungen: 393 -> 393.
- Output-Entscheidungen: 393 -> 393.
- Einzelziel-Vetos: 2 -> 2.
- Ergebnisabweichungen: 0 / 1.010.

Der unveränderte 6.72.373-Callgraph verursacht in diesem globalen Provider-/Control-Teil mindestens 10.548 wiederholte get_option-/home_url-Lesevorgänge. 6.72.374 reduziert genau diesen globalen Teil auf 10. Zusätzliche Sanitizer-/Registry-/Control-Zugriffe sind darin nicht enthalten.

Damit ist die Ursache der entfernten Wiederholungsarbeit bewiesen. Die Höhe des Live-Seitenspeedups wird erst nach PASSIV behauptet.

## Inhaltliche Gleichheit
500 unabhängige Request-Zustände, insgesamt 17.426 Kandidaten:
- eBay, idealo, AWIN, Digistore24, manual
- Provider Pause/Prepared/Access off/missing credentials/Chef-Veto
- Partner-Veto/Review
- Creative-Veto
- Output-Veto
- Einzelziel-Veto
- AWIN-Block
- globaler Notstopp
Ergebnis: 0 / 17.426 Abweichungen.

Dynamische/unsichere Fälle:
- externer Registry-Callback
- externer Access-Callback
- Partneradapter-Filter mit Block
- Control-Optionfilter
- während der Kandidatenfolge wechselnde Providerzustände
Ergebnis jeweils: 0 Abweichungen und identische Alt/Neu-Aufrufzahlen. Der historische Einzelprüfpfad bleibt vollständig aktiv.

## Funktionsschutz 6.72.373 -> 6.72.374
Exakter PHP-Tokenvergleich über alle 23 PHP-Dateien:
- benannte Funktionen/Methoden 1.564 -> 1.570
- entfernt 0
- 1.564 / 1.564 bestehende weiter vorhanden
- 1.563 bestehende token-inhaltlich unverändert
- geändert genau 1: campaign_control_base_allows_delivery()
- neu genau 6 interne Schutz-/Cachehelfer
- Properties 33 -> 37; entfernt 0; neu nur vier requestlokale Cache-/Sicherheitszustände.

Token-inhaltlich unverändert sind u.a.:
render_affiliate_slot_for_context, render_banner, build_click_tracking_url, campaign_slot_allowed, assignment_selection_for_slot, article_plan_apply_to_content, filter_the_content, campaign_match_rank, product_fill_verified_portal_fallback_v672226, category_product_provider_mix_v672133, campaign_health_allows_delivery, product_campaign_public_image_ready, select_campaign_for_slot, control_provider_gate, control_partner_gate, control_partner_gate_after_provider_v672372, category_product_shared_rank_base, select_category_product_campaign_fast_v672171, category_product_postprocess_candidates_v672365.

Damit bleiben Providerregeln, Partnerregeln, Ranking, Placement, Fallback, Veto, Health, Bilder, Tracking, Rendering und Artikelausgabe erhalten.

## Integration/Schreibschutz
- Actions 176 -> 176
- Filter 30 -> 30
- Shortcodes 6 -> 6
- update_option 290 -> 290
- add_option 7 -> 7
- delete_option 37 -> 37
- update_post_meta 85 -> 85
- add_post_meta 2 -> 2
- delete_post_meta 10 -> 10
- wp_insert_post 3 -> 3
- wp_update_post 12 -> 12
- wp_delete_post 1 -> 1
- set_transient 11 -> 11
- delete_transient 12 -> 12
- wp_schedule_event 9 -> 9
- wp_schedule_single_event 36 -> 36
- wp_clear_scheduled_hook 34 -> 34
- $wpdb->insert 13 -> 13
- $wpdb->update 76 -> 76
- $wpdb->delete 2 -> 2
- $wpdb->query 16 -> 16

## Andere Plugins / Paket
Paketwurzel ausschließlich affiliate-portal-router/.
- Dateien 66 -> 66; entfernt 0; neu 0; 64/66 unverändert.
- geändert ausschließlich pferdeportal-affiliate-router.php und readme.txt (Stable Tag).
- keine Datei anderer Plugins, Themes oder WordPress-Core enthalten.
- finales ZIP erneut entpackt: 66/66 Dateien, 0 Hashabweichungen.
- PHP 23/23 PASS im Arbeitsbaum und im finalen ZIP.
- Header/Klassenkonstante/Stable Tag: 6.72.374.
- SHA-256: 377683dd1e65ae586188e51f16e35e3a8f49d3257ea0cbfa516536c824dbe68b

## Freigabegrenze
6.72.374 ist lokal als gebündelter Rootfix-Kandidat freigegeben. Kein Live-Gesamtspeedup wird vor dem einen kontrollierten PASSIV-Lauf behauptet.