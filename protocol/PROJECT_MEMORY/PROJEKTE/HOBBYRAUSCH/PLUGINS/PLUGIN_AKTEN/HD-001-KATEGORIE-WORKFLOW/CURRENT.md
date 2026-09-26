# HD-001 – KATEGORIE-WORKFLOW – CURRENT

STAND: 2026-09-26
STATUS: V1.8.0 BYTEGENAU GEBUNDEN / V1.8.1 NEUER DOKUMENTIERT / HOBBY-DEPOT-WEITERENTWICKLUNG OFFEN

## Rolle

Einzige aktuelle Pluginwahrheit für HD-001.

## Exakt verfügbare und verifizierte Basis

Affiliate-Portal Kategorie-Workflow V1.8.0 / MASTER016-R10/R11.

Installer:
`AFFILIATE_PORTAL_KATEGORIE_WORKFLOW_V1.8.0_MASTER016_R10_R9_RUNTIME_DEPLOYMENT.zip`
SHA-256:
`4c98847e96b091955436230b721a39b5049132037546367a810d4ed642f40845`

Source:
`QUELLCODE_KATEGORIE_WORKFLOW_V1.8.0_MASTER016_R10_R9_RUNTIME_DEPLOYMENT.zip`
SHA-256:
`1d17566f309f460e48255b78357912cf5e18b1eba2eed7654516e79c8f9fa7fd`

MASTER:
`ALLGEMEINGUELTIGER_KATEGORIE_MASTER_016_R10_R9_RUNTIME_DEPLOYMENT.zip`
SHA-256:
`2e6990847c5bc32176f87c6f4b006ccdd0f3f57891c176ed5a6874edfdff942c`

Frisch geprüft:
- Source 216/216 PASS
- Installer 216/216 PASS
- PHP-Lint 15/15 PASS
- keine Pferde-Atelier-Bindung im Produktionscode / aktiven Schemas

## Neuester belegter Entwicklungsstand

V1.8.1 ist später dokumentiert:
- allgemeines PARENT_TOPIC_GAP-Gate
- 220/220 PASS
- ZIP SHA-256 `1915922977b3d803b25ed9458e5eb40ae7dd30c37f9d3c763720d5e47b25ac6b`

Die exakten V1.8.1-ZIP-Bytes sind derzeit nicht gebunden.

Kein V1.8.2+-Stand gefunden.

## Funktionsstand V1.8.0

Vorhanden:
- DataForSEO-Verbindung/Ideas/Suggestions/Overview
- 14-Stufen-Research-/Kategorie-Workflow
- SEO-Nachfrage, Intent, Ownership, Kannibalisierung, Coverage, Affiliate-Fit
- Baseline-/Delta-Lifecycle
- WordPress category / HivePress hp_listing_category / gebundene Journal-Taxonomie
- Dry-Run / Apply / Readback / Rollback / Idempotenz

Grenze:
- der Initial Tree wird nicht autonom aus einer Rohliste erfunden; er muss als Strukturentwurf vorliegen und wird danach datenbasiert geprüft/korrigiert
- Writer schreibt nur Taxonomie-Terme
- WordPress-Seiten werden gelesen/verglichen, aber V1.8.0 erzeugt keine Seiten
- keine Menüs

## Artefaktablage

Persistente Spiegelung:
`/Campus-Archiv/PROJEKTE/HOBBYRAUSCH/PLUGINS/HD-001-KATEGORIE-WORKFLOW/`

## NEXT ACTION

Auf der byteverifizierten V1.8.0-Basis die Hobby-Depot-Fassung weiterentwickeln:
1. allgemeines PARENT_TOPIC_GAP-Gate aus V1.8.1 übernehmen;
2. transaktionale WordPress-Seitenerzeugung ergänzen;
3. Positiv-/Negativ-/Rollback-/Idempotenztests;
4. neues installierbares ZIP erzeugen;
5. erst danach auf Hobby Depot installieren und DataForSEO/WordPress live testen.
