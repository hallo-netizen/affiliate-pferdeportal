# Hobbydepot 0.4.24.11 – überprüfte Gesamtkette gegenüber Pferdeatelier 0.4.34 (19.11.2026)

**Status: BLOCKED; kein installationsreifer Nachfolger.** Vollständige WordPress-Live-Ausführung nicht behaupten.

## Original-Quellprüfungen
- Hobby-ZIP SHA256: `f7e5a5e03100af5dc7c7921886716c584b429fd303202fc9112869323b9e0280`; 87 Einträge, CRC PASS, 78/78 PHP-Syntax PASS.
- Pferde-ZIP SHA256: `14a3976702fa782e110184c3abc8eba82a0225f28384b4d540488c96f65dfb6b`; 89 Einträge, CRC PASS, 79/79 PHP-Syntax PASS.
- Hobby 19.11. 13:46:47 UTC Diagnose: 223 Rohkeywords, 180 Kandidaten, 0 PASS, 164 SANDBOX_REQUIRED, 16 REVIEW_REQUIRED, 75 family MATCH, 105 NO_MATCH, K0-Typstatus BLOCKED.
- Original-PHP-Methode `PSTE_Portal_Relevance_Gate::evaluate` ohne kostenpflichtige API: `3D-Bogenschießen Regeln` und `3D-Bogenschießen Parcours` -> EXTERNAL_REVIEW_REQUIRED. Off-topic `Modellpark Berlin-Brandenburg` -> nicht PROVEN. Rein `3D-Bogenschießen` -> PASS FAMILY_ONLY_OR_EDITORIAL_INTENT, aber noch keine Titelquittung/Produktionsfreigabe.
- Hobby `contracts/k0-article-type-capabilities-v1.json` enthält `K0_PORTAL_ADAPTER_PENDING`; originaler PHP-Aufruf `TXE_K0_Article_Types::snapshot()` wirft exakt `K0_ARTICLE_TYPE_AUTHORITY_UNAVAILABLE`. Pferde-Original nimmt `K0_RULE_VALUES_JSON` und liefert genau Beratung, FAQ, Pflege, Vergleich, Anleitung.
- Hobby `original/pste/contracts/portal-domain-seeds-v1.json` hat noch leere Bindungen: `THEMENREGISTER_NOCH_ZU_VERBINDEN`. `appendOriginalProvenResearch()` lässt original gesperrte Rohkeywordkandidaten nicht nach MINI.
- K0-Original-Branch `konzept0-portal-neutral-20261002`, `K0_PORTAL_REGISTRY.json` + `engine/k0_portal_resolver.py`: Hobby nur `discgolf-beratung`, keine übrige Hobby-Kategorie. Andere Slugs erhalten keine eindeutige Portalzuordnung; Eingangsidentität bleibt strikt bei fünf Feldern.
- Echte Pferde-Referenz: MINI-Gesamtauftrag (10 Items), CATEGORY-Checkpoint (20 Items); davon unabhängig echtes 2er-K0-Paket `WP_K0_UPLOAD_PACKAGE_V1` mit exakt fünf Feldern, Batch-Hash PASS, WordPress-Receipt-Hash PASS, beide resultierenden Artikelidentitäten in gleicher Reihenfolge im echten `SYSTEM4_WORDPRESS_HANDOFF_V1`, Test-Suite PASS. Dies sind nicht notwendigerweise dieselben MINI- und K0-Batches.
- Es wurde weder eine neue DataForSEO-Recherche ausgelöst noch WordPress verändert.

## Freigabekriterium vor nur EINEM neuen Plugin
1. Bindung Hobby-Themenrelevanz an verifizierte tatsächliche WordPress-Kategorien, unter Beibehaltung Fremdkeyword-Sperre und bestehender Entscheidungsverantwortung.
2. K0-Beitragsarten aus tatsächlich bestehender K0-Regelautorität übernehmen; kein eigener Fachentscheid.
3. Eindeutige bestehende K0-Portalzuordnung für reale Hobby-Kategorie-Slugs, ohne K0-Fünf-Feld-Vertrag zu verbiegen.
4. Die 223 gespeicherten Keywords kostenfrei reanalysieren, validierten MINI-Titel- und CATEGORY-Checkpoint prüfen, echtes Hobby-K0-Input / Ausgabe inklusive sämtlicher Originalprüfungen erfolgreich nachweisen.

Nur Source- und isolierte PHP-Tests = KEIN vollständiger Integrationsnachweis. Das bloße Beseitigen eines einzelnen Fehlers ist **kein Grund für eine Installations-ZIP**.