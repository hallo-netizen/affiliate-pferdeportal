# Affiliate Router 6.72.182 – Banner nach Produktpfad-Prinzip – Full E2E ZIP PASS

Datum: 2026-10-04
Workstream: AFFILIATE_ZENTRALE
Version: 6.72.182
Branch: affiliate-release-current

## Ausgangspunkt

Der vorherige 6.72.181-Stand war NICHT ausreichend belegt. Die isolierte Methoden-Simulation hatte Vorfilter vor dem Ranking nicht abgedeckt.

Der neue vollständige WordPress+MariaDB-Gate reproduzierte deshalb den realen Weg:
gespeicherte Zuweisung -> Kandidatenpool -> Slot-/Formatfilter -> Relevanz -> Verteilung -> Auswahl -> Renderer -> HTML.

## Produktpfad als Vorbild

Der funktionierende eBay/Idealo-Produktpfad folgt dem KISS-Prinzip:
1. Kandidaten bilden;
2. technische Gültigkeit;
3. Ziel/Relevanz;
4. Auswahl;
5. Ausgabe.

Der Bannerpfad ist jetzt auf dasselbe Prinzip zurückgeführt:
- Slot-Aliase werden vor dem technischen Gate eindeutig auf eine vorhandene kanonische Slotregel abgebildet.
- Placement darf einen technischen Bannervertrag niemals umgehen.
- Jeder Banner besteht genau einen zentralen technischen Slot-Gate.
- Danach gilt zentral: exakt -> weiterer Themenkreis -> allgemein -> technisch gültiger Fallback.
- Rassen bleiben themenneutral und verwenden die vorhandene stabile Verteilung.
- Manuelle FIXED/NONE-Ausnahmen bleiben wirksam.
- Produktslots bleiben bannerfrei.

## Belegte Root Causes

Volltest vor Fix:
- REAL category_recommendation technical fallback: FAIL; canonical product_after_category_tiles mit demselben Banner: PASS.
- TRACE canonical_candidates=["tech-wide:5"]
- TRACE real_alias_candidates=[]
- post_inline_banner ließ ein 400x400-Quadrat als exakten Kandidaten vor einen gültigen 1000x100-Banner.
- Rassen-Ranking selbst rotierte bereits korrekt; eine erste Testassertion war falsch und wurde auf exakte gerenderte Ziel-URLs korrigiert.

Fix:
- runtime_contract_slot_rule(): eindeutige bestehende Aliasgruppe -> kanonische technische Slotregel; mehrdeutige Gruppen fail-closed.
- campaign_slot_allowed(): Banner-Placement ist kein Bypass mehr; technische Slotregel gilt immer genau einmal.
- ranked_campaigns_for_slot_uncached(): doppelte Banner-Formatprüfungen entfernt; zentraler campaign_slot_allowed()-Gate ist autoritativ.
- fixed_campaign_selection(): auch feste Bannerzuweisung muss technisch zum realen Slot passen.

## Source Full E2E

GitHub Actions Run: 37216563071
Ergebnis: SUCCESS

- exact 6.72.182 source bound: PASS
- PHP syntax: PASS
- plugin active 6.72.182: PASS
- complete WordPress + MariaDB banner workflow: 21 PASS / 0 FAIL
- real category_recommendation technical fallback: PASS
- page exact > broad > general > technical: PASS
- category exact on real slot: PASS
- post exact: PASS
- post invalid geometry blocked: PASS
- glossary exact: PASS
- breeds visible + stable distribution: PASS (A -> B -> A)
- manual fixed override: PASS
- manual none: PASS
- banner does not fill product slot: PASS
- no remote HTTP calls during render: PASS

## Performance

Geschützte Performancepfade gegen den vollständig gegateten 6.72.176-Stand:
- ranked_campaigns_request_cache_allowed(): IDENTISCH
- ranked_campaign_sanitize_key_request_cached(): IDENTISCH
- ranked_campaign_sanitize_text_request_cached(): IDENTISCH
- ranked_campaigns_request_cache_key(): IDENTISCH
- select_category_product_campaign_fast_v672171(): IDENTISCH
- ranked_campaign_candidate_pool(): IDENTISCH
- ranked_campaigns_for_slot(): IDENTISCH
- category_product_provider_mix_v672133(): IDENTISCH
- render_banner(): IDENTISCH
- banner_distribution_reorder_candidates(): IDENTISCH
- banner_distribution_stable_index(): IDENTISCH
- category_product_shared_rank_base(): IDENTISCH

Neue/angepasste Banner-Gate-Funktionen:
- 0 DB-Aufrufe
- 0 get_post_meta-Aufrufe
- 0 Remote-Aufrufe
- runtime_contract_slot_rule() nutzt bestehenden request-lokalen Cache.

## Installer

Artifact:
release/affiliate-zentrale/artifacts/final/AFFILIATE_ZENTRALE_6.72.182.zip

SHA-256:
a74a4cd2a2831ba31dfbd5485e6a3c1f61792cd47d5b9b2dc9403f13a638593b

Bytes:
1,538,866

Git blob:
2873c726b1e51cc3aeae9b7d8c26a1d88b35d68d

Build commit:
b8e12902640851c4ad275c5e2d5635b596bdf147

## ZIP Full E2E

GitHub Actions Run: 37216941150
Ergebnis: SUCCESS

- ZIP 27/27 manifest byte identity: PASS
- ZIP structure/version: PASS
- Performance hardlock: PASS
- ZIP PHP lint 21/21: PASS
- frische WordPress+MariaDB-Installation aus ZIP: PASS
- ZIP plugin active 6.72.182: PASS
- kompletter Banner-End-to-End-Test: 21 PASS / 0 FAIL
- ZIP_FULL_WORDPRESS_MARIADB_BANNER_E2E_PASS

## Schluss

6.72.182 ist der erste Kandidat dieser Fehlerkette, der sowohl als Source als auch als tatsächlich installiertes ZIP den vollständigen Bannerweg bis zum gerenderten HTML positiv und negativ bestanden hat.

Live-Produktivinstallation auf pferde-atelier.de wurde in diesem Gate nicht durchgeführt.
