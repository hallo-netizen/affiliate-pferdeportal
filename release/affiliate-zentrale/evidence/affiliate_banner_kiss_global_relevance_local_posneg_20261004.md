# Affiliate Banner KISS – globale Relevanz + Rassenverteilung – lokaler Positiv/Negativ-Nachweis

Datum: 2026-10-04
Workstream: AFFILIATE_ZENTRALE
Branch: affiliate-release-current
Source functional commit: 95454463ddd5058eaa699875d349a39c598fc4d6
Source manifest SHA-256: 62bb2ff2b22c97fbfef6b9d64bccfa1d06e41fdecd3ca8b33c4a764bc40415f8
Pluginversion unverändert: 6.72.180
Release: NICHT freigegeben

## Nutzerentscheidung

Einheitliche Bannerreihenfolge auf allen fachlichen Ebenen:
1. exaktes Thema;
2. weiterer Themenkreis;
3. allgemeiner Fallback;
4. danach jeder aktive, technisch/slotseitig gültige Banner – Thema egal.

Gilt für:
- Seiten;
- Kategorien;
- Beiträge;
- Glossar.

Pferderassen:
- kein künstlicher Themenvorrang;
- alle technisch gültigen Rassenbanner liegen in derselben Relevanzstufe;
- die bereits vorhandene stabile Partner-/Creative-Verteilung entscheidet;
- keine zweite Verteilungsmaschine.

## Belegter Root Cause

Im zentralen Runtime-Ranking konnten frühe URL-/Runtime-Returns einen später vorhandenen exakten gespeicherten Zieltreffer abschneiden. Zusätzlich war die Banner-Slot-Typisierung nicht vollständig deckungsgleich mit der Banner-Distributionsliste; insbesondere category_recommendation konnte dadurch den letzten technischen Bannerfallback nicht über denselben zentralen Bannerpfad erhalten.

## Minimaler Fix

Nur:
- release/affiliate-zentrale/current/affiliate-portal-router/pferdeportal-affiliate-router.php

Geändert:
- campaign_match_rank(): exakte gespeicherte Zielkante wird vor breiteren URL-/Texttreffern gezogen;
- Rassen-Single + Rassen-Overview werden themenneutral auf specificity=5 gelegt und dadurch von der bestehenden stabilen Distribution verteilt;
- slot_required_creative_type(): alle vorhandenen Banner-Slot-Aliase sind zentral als Banner typisiert.

Nicht geändert:
- Providerlogik;
- Awin/eBay/Idealo;
- GTIN;
- Housekeeping;
- Renderer;
- Output-Objects;
- Automation-Suite;
- Datenbank-/Remote-Calls;
- Designplugin.

## Lokaler exakter Methodentest

Die beiden geänderten Methoden wurden aus dem aktuellen Source extrahiert und als identischer PHP-Methodencode mit Stub-Umgebung ausgeführt.

Ergebnis:
- PHP Syntax der geänderten Methoden: PASS.
- Seite: exakte Zielkante 520 schlägt breiteren URL-Treffer 440: PASS.
- Kategorie: exakte Zielkante 520 schlägt breiteren URL-Treffer 440: PASS.
- Beitrag: exakte Zielkante 520 schlägt breiteren URL-Treffer 440: PASS.
- Glossar: exakte Zielkante 520 schlägt breiteren URL-Treffer 440: PASS.
- breiter Themenmatch 440 schlägt themenfreien Fallback: PASS.
- category_recommendation ohne Themenmatch -> technischer Bannerfallback 5: PASS.
- product_after_category_tiles ohne Themenmatch -> technischer Bannerfallback 5: PASS.
- post_inline_banner ohne Themenmatch -> technischer Bannerfallback 5: PASS.
- glossary_single_mobile_banner ohne Themenmatch -> technischer Bannerfallback 5: PASS.
- template_mid_banner ohne Themenmatch -> technischer Bannerfallback 5: PASS.
- expliziter allgemeiner Fallback 100 schlägt technischen Fallback 5: PASS.
- breed_single_desktop_banner -> themenneutrale Stufe 5: PASS.
- breed_single_mobile_banner -> themenneutrale Stufe 5: PASS.
- breed_overview_banner -> themenneutrale Stufe 5: PASS.
- category_product_1 bleibt Produkt-Slot: PASS.
- Produkt ohne Zielmatch bleibt fail-closed: PASS.

Gesamt: 16/16 PASS.

## Slot-Abdeckung

Vergleich der zentralen Banner-Distributionsslots mit slot_required_creative_type():
- fehlende Distributionsslots: 0.
- zentrale Banner-Slot-Typisierung: 35 Slot-/Aliasnamen.

## Performance-Hardlock

Direkter Funktionsvergleich vor/nach dem Source-Fix:
- render_banner(): UNCHANGED
- ranked_campaigns_request_cache_allowed(): UNCHANGED
- ranked_campaign_sanitize_key_request_cached(): UNCHANGED
- ranked_campaign_sanitize_text_request_cached(): UNCHANGED
- ranked_campaigns_request_cache_key(): UNCHANGED
- select_category_product_campaign_fast_v672171(): UNCHANGED
- ranked_campaign_candidate_pool(): UNCHANGED
- ranked_campaigns_for_slot(): UNCHANGED
- category_product_provider_mix_v672133(): UNCHANGED
- banner_distribution_reorder_candidates(): UNCHANGED
- banner_distribution_stable_index(): UNCHANGED

Source-Delta des Fix-Commits:
- exakt eine Plugin-Datei geändert: pferdeportal-affiliate-router.php.

Damit werden die 6.72.171 Request-/Ranking-Performancepfade nicht zurückgebaut.

## Alte automatische Workflows

Die automatisch gestarteten Workflows 37209864921, 37209864936 und 37209864980 sind für 6.72.170/6.72.171 hart codiert und brachen an ihren Versions-Greps ab. Sie sind deshalb weder Positiv- noch Negativbeleg für 6.72.180 und werden nicht als Gate gewertet.

## Offener Gate

Noch offen:
- aktueller versionneutraler WordPress/MariaDB Gesamtgate auf genau diesem Manifest;
- erst danach Release-Check/Installer/Live-Readback.

Kein Versionssprung, kein ZIP, keine Liveinstallation in diesem Schritt.


## Performance-Nachprüfung 04.10.2026

Zusätzlicher Review nach Nutzerhinweis auf möglichen Performance-Rückbau:

- 6.72.171-Performancefunktionen gegen den belegten 6.72.171-Stand direkt verglichen:
  - ranked_campaigns_request_cache_allowed(): IDENTISCH
  - ranked_campaign_sanitize_key_request_cached(): IDENTISCH
  - ranked_campaign_sanitize_text_request_cached(): IDENTISCH
  - ranked_campaigns_request_cache_key(): IDENTISCH
  - select_category_product_campaign_fast_v672171(): IDENTISCH
  - ranked_campaign_candidate_pool(): IDENTISCH
  - ranked_campaigns_for_slot(): IDENTISCH
  - category_product_provider_mix_v672133(): IDENTISCH
  - category_product_shared_rank_base(): IDENTISCH
  - automation_campaign_exact_target_rank(): IDENTISCH
  - automation_campaign_exact_target_rank_uncached(): IDENTISCH
- render_banner() ist gegenüber 6.72.171 später verändert worden, aber gegenüber dem belegten 6.72.176-Stand IDENTISCH. Damit stammt diese Änderung nicht aus dem aktuellen KISS-Fix; sie ist der bereits belegte eBay-BUSINESS-Payload-Fix.
- Gegen 6.72.176 sind zusätzlich IDENTISCH:
  - render_banner()
  - ranked_campaigns_request_cache_allowed()
  - ranked_campaigns_request_cache_key()
  - select_category_product_campaign_fast_v672171()
  - ranked_campaign_candidate_pool()
  - ranked_campaigns_for_slot()
  - category_product_provider_mix_v672133()
  - banner_distribution_reorder_candidates()
  - banner_distribution_stable_index()
- Die beiden aktuell geänderten Funktionen enthalten keine DB-Abfrage und keinen Remote-Request.
- Im ersten KISS-Stand war bei einem Nichttreffer ein zweiter Aufruf von automation_campaign_exact_target_rank() möglich. Dieser unnötige Doppelaufruf wurde in Commit 95454463ddd5058eaa699875d349a39c598fc4d6 entfernt.
- Nach Cleanup gibt es im zentralen Rankingpfad nur noch einen Aufrufpunkt für die gespeicherte Zielkante.
- Rassenbanner verlassen campaign_match_rank() vor URL-/Glossar-/Rassensemantik und verursachen dadurch weniger Rankingarbeit als vorher.
- slot_required_creative_type() bleibt statisch request-lokal gecacht; die erweiterte Aliasliste erzeugt keine DB-/Remote-Arbeit.

Ergebnis: KEIN belegter Rückbau oder Überschreiben der 6.72.171/6.72.176-Performanceverbesserungen durch den aktuellen Banner-KISS-Fix.

Offen bleibt weiterhin ein aktueller WordPress/MariaDB-Gesamtgate. Die vorhandenen automatisch gestarteten 6.72.170/6.72.171-Workflows sind versionshart codiert und brechen vor ihren eigentlichen Tests am Versions-Grep ab; sie dürfen nicht als Funktions-Fail gewertet werden. Eine Workflowänderung ist nach aktuellem Scope ausdrücklich verboten.
