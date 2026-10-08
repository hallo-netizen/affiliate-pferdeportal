# Affiliate Zentrale 6.72.207 – Glossar Standardregel / Pferderassen freie Wahl

Datum: 2026-10-08

## Nutzerregel
- Glossar: dieselben Bannerregeln wie überall – thematisch passend zuerst; wenn kein passender Treffer vorhanden ist, freie technisch/formatlich gültige Bannerwahl.
- Pferderassen-Singles: grundsätzlich freie Bannerwahl; kein Themenzwang und kein Themenrangvorteil.
- Alles andere unverändert.

## Root Cause
Creative-Library-Banner wurden im Glossar bei fehlendem exaktem gespeicherten Zieltreffer zu früh mit `return null` ausgeschlossen. Dadurch konnten manche Glossarbeiträge Banner zeigen und andere trotz technisch gültigem Bestand leer bleiben.
Der historische freie Rassenpfad griff für moderne `output_object_v4`-Banner nicht, weil deren Library-Branch vorher beendet wurde.

## KISS-Fix
- Glossar-Singles: Library-Banner ohne exakten Zieltreffer laufen weiter durch die normale Themenrangfolge; ohne Themenbezug greift der bereits vorhandene globale technische Banner-Fallback.
- Pferderassen-Singles: nach Active/Technik/Format/Placement sofort neutraler Rang `specificity=5`; Themenzuordnung beeinflusst die Auswahl nicht.
- Keine Änderung an Rechner, Artikeln, Hubs, Kategorien, Providern, DB oder HTTP.

## Harter Positiv-/Negativnachweis
Fresh WordPress + MariaDB:
- Run: 37768292261
- Ergebnis: SUCCESS
- Assertions: 34 PASS / 0 FAIL

Entscheidende Assertions:
- glossary_thematic_match_first: PASS
- glossary_unrelated_mapped_free_fallback_article1: PASS
- glossary_unrelated_mapped_free_fallback_article2: PASS
- glossary_topic_outweighs_free: PASS
- glossary_second_unrelated_topic_desktop_visible: PASS
- glossary_second_unrelated_topic_mobile_visible: PASS
- breed_unrelated_is_free: PASS
- breed_thematic_is_same_free_rank: PASS
- breed_has_no_topic_preference: PASS
- glossary/breed format positive and negative: PASS
- no duplicate: PASS
- calculator live-pass guard preserved: PASS

## Installer
- AFFILIATE_ZENTRALE_6.72.207.zip
- SHA256: b2e88dc663a6f14b00071aa1a4c709afc73a113a49d631c9a5f6dcf38d6c9ad4
- Bytes: 821428
- ZIP/source identity: 28/28 PASS
- Workflow artifact: 11545587566

Status: HARD_GATE_PASS / LIVE_READBACK_OPEN
