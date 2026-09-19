# Affiliate – Übergabe neuer Chat – 19.09.2026 19:34

Diese Datei ist nur Wegweiser. Keine zweite CURRENT-Wahrheit.

## Einstieg
1. Repo `hallo-netizen/affiliate-pferdeportal`
2. Branch `affiliate-release-current`
3. `release/affiliate-zentrale/AGENTS.md`
4. genau eine Current-Autorität: `control/release-governance/CURRENT_RELEASE.json`
5. Frischecheck gegen Branch-HEAD + `release/affiliate-zentrale/CURRENT_SOURCE_SHA256.txt` + direkten Source-Tree
6. bei unverändertem Stand exakt die dortige NEXT ACTION ausführen.

## Zielvertrag
`protocol/AFFILIATE_RELEASE_AUTOMATIC_CREATIVE_LIFECYCLE_SCOPE_20260918.md`
Vollautomatischer providerneutraler Creative-Lifecycle. Für Awin zusätzlich: kein Einzel-`Code kopieren` als Normalweg; bewiesene Bulk-/maschinenlesbare reale Quelle erforderlich.

## Belastbarer Stand
- Live/tested: 6.72.108.
- Awin Programmliste live: 7 verbundene Programme PASS.
- Awin Partnerdropdown live: `Awin · Ahipos Horses DE · 120341` PASS.
- Lokal 6.72.108: 25/25 Partner, 21/21 Awin-Transport, 82/82 Gesamtregression, PHP 21/21, Fresh-Unpack 26/26 PASS.
- Protected output base: 6.72.104/106; Journal/Glossar/Pferderassen/Kategorien dürfen nicht zurückgebaut werden.
- Canonical repo is still 6.72.105. Therefore no release PASS.

## Erster Blocker
`AFF-ERR-035`: exact 6.72.108 tree is not canonical; 14/26 files differ from canonical 6.72.105.

## Genau eine NEXT ACTION
Reconcile exact tested/live 6.72.108 against canonical 6.72.105 without blind overwrite, preserving the 6.72.104 live-pass base; run governance + full positive/negative/regression/fresh-unpack gates. Erst danach `AFF-ERR-038` fortsetzen: realen Cleos-Bulkweg beweisen oder dokumentierte maschinenlesbare Awin-Publisherquelle binden.

## Nicht anfassen
- kein STARTMASTER für Affiliate;
- keine Awin-Codeänderung auf 6.72.105 vor Drift-Reconciliation;
- kein 6.72.102 Breadcrumb-/Spacer-Guard;
- keine Journal-/Glossar-/Pferderassen-/Kategorie-/Design-Nebenfixes;
- kein einzelnes manuelles Code-Kopieren als Zielworkflow;
- keine DevTools/private Endpoint-Raterei;
- PPA-001 CURRENT.zip nicht ersetzen, solange kanonische Source-/Release-Bindung offen ist.
