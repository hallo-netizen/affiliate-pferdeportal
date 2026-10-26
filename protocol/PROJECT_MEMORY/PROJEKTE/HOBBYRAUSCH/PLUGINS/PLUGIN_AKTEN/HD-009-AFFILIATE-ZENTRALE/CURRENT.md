# HD-009 – HOBBY DEPOT AFFILIATE-ZENTRALE – CURRENT

<!-- PLUGIN_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-26
STATUS: PORTIERUNG AKTIV / KEIN INSTALLATIONSKANDIDAT

## Rolle

Einzige technische Plugin-Wahrheit für die neue Hobby-Depot-Affiliate-Zentrale.

Fach-Current:
`../../../AFFILIATE/CURRENT_STATE.md`

## Technische Basis

Referenz:
Pferdeatelier Affiliate-Zentrale 6.72.211, Generation 313.

Referenzbranch:
`affiliate-release-current`

Referenz-Head:
`7375bc46a57ac4c2ff2a74a6dd4919113defd009`

Referenz-Source-Manifest:
`f11687daa1f11d8ff98a3c0d62a720dac170dd95edddf39eba04530e858c44cf`

Diese Referenz ist keine Hobby-Depot-Current-Wahrheit.

## Hobby-Depot-Workbench

Branch:
`hobbyrausch-affiliate-current`

Commit:
`be76ac860272628b3f2ecf66cb8c95ffcc92d29f`

Pfad:
`work/hobbyrausch-affiliate/porting/hobby-depot-affiliate-router/`

24 Engine-/Provider-Dateien übernommen.

Nicht übernommen:
- `assets/ebay-portal-catalog-v2.json` aus Pferdeatelier;
- `assets/portal-structure-v279.json` aus Pferdeatelier;
- `recovery/aff043-historical-product-state-20260915.json`;
- Pferde-spezifisches `readme.txt`.

Die beiden erwarteten Katalogpfade enthalten nur fail-closed Portierungsplatzhalter.

## Harte Regeln

- Keine Pferde-Banner/-Produkte/-Artikel/-Taxonomien/-Kataloge.
- Keine Secrets in Git/Campus/Evidence.
- Bestehende Credential-Schnittstellen nur kontrolliert migrieren, nicht blind umbenennen.
- eBay, idealo und Amazon müssen jeweils positiv und negativ getestet werden.
- Kein ZIP/CURRENT.zip, solange Pferdebezüge im Code verbleiben oder Providerpfade nicht vollständig geprüft sind.

## Erster Blocker

Noch vorhandene Pferdeatelier-spezifische Fachlogik in Hauptplugin, eBay, idealo und Automation.

## NEXT ACTION

Diese Fachlogik neutralisieren und an Hobby-Depot-Kategorie-/Hobbyverträge binden, ohne Provider-/Credential-/Output-Kern umzubauen.
