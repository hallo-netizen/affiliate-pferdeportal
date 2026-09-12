# AFFILIATE – HOBBYRAUM

STAND: 2026-09-12
STATUS: BLOCKED AUF KANONISCHE BYTEGENAUE RÜCKBINDUNG

## AKTUELLER AUFTRAG

Zielvertrag `ZV-AFFILIATE-ADCELL-001` erfüllen:

`ADCELL API v2 -> accepted + active -> programId-Allowlist -> CSV/Banner/Deeplink automatisch -> zentrale Relevanz-/Creative-/Output-/Veto-Logik`

Kein manueller CSV-Normalweg. Kein Awin-Fallthrough. Kein paralleler Provider-Arbeitsstrang.

## BELASTBARER STAND

Der ADCELL-Kandidat ist im isolierten Prüfraum aus der kanonischen 6.72.8-Basis fertig gebaut und lokal hart geprüft.

Geänderte Source-Dateien genau:
- `trait-ppar-provider-registry.php`
- `trait-ppar-network-sync.php`
- `trait-ppar-automation-suite.php`

Ausgeführt PASS:
- ADCELL Static Gate;
- ADCELL Runtime Positiv/Negativ;
- AF-062 Legacy-Basic-Auth-Runtimeweg blockiert;
- Awin/OTTO-Funktionsblock-Regression 18/18 byteidentisch;
- Banner-Regression;
- PHP-Lint 21/21;
- originaler Release-Guard Governance/Source/Tree/Start PASS.

Lokales Kandidaten-Manifest:
`74a5d0d5e48028a9ddd82bcf7a32628dbeb42d0963c9ae431bfe8dee3e2c00e5`

Nachweis:
`release/affiliate-zentrale/evidence/adcell_api_v2_local_full_gate_unbound_20260912.txt`

## AKTUELLER BLOCKER

Nicht der ADCELL-Code, sondern ausschließlich die **bytegenaue Rückbindung der drei bereits geprüften Dateien auf den kanonischen Branch**.

Ein GitHub-Blob mit abweichendem Hash darf niemals eingebunden werden. Fehlgeschlagene Transportblobs bleiben unreferenziert und sind keine Source.

Der kanonische Branch bleibt deshalb bis zur exakten Rückbindung die technische Autorität; lokaler PASS ist kein kanonischer PASS.

## NEXT ACTION – GENAU EIN SCHRITT

Die drei lokalen geprüften Source-Dateien bytegenau auf `affiliate-release-current` binden.

Danach ohne neuen Sourceumbau:
1. `CURRENT_SOURCE_SHA256.txt` + `CURRENT_RELEASE.json` atomar an den committed Sourcezustand binden;
2. ADCELL Positiv/Negativ + Awin/OTTO-Regression + Banner-Regression + 21/21 PHP-Lint erneut auf dem committed Stand;
3. originaler Release-Guard erneut;
4. Fresh-Unpack + Source/ZIP-Identity;
5. erst dann Test-Plugin.

Live-PASS zusätzlich erst nach wiederhergestelltem ADCELL-Zugang und echtem WordPress/MariaDB-E2E.

## ARBEITSWEG

- technische Autorität: `affiliate-release-current`
- technischer Scope: `protocol/AFFILIATE_RELEASE_ADCELL_AUTOMATION_SCOPE_20260911.md`
- Fehlerautorität: `AFFILIATE_HOBBYRAUM/FEHLERMATRIX.md`
- Task: `AFFILIATE_HOBBYRAUM/TASK.current.json`
- kein Codex
- kein Side-Branch als Release-Autorität
- keine historische Rekonstruktion

## NICHT ANFASSEN

- OTTO/Awin-Arbeit nicht fortsetzen;
- Digistore24 nicht fortsetzen;
- keine neue Providerarchitektur;
- kein separates ADCELL-Plugin;
- keine Pluginversionskette;
- kein 6.72.18-Scratch;
- keine manuelle CSV-Ersatzlösung.
