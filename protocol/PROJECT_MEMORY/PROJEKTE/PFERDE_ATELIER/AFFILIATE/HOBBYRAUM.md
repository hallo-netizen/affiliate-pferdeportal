# AFFILIATE – HOBBYRAUM

STAND: 2026-09-12
STATUS: BLOCKED AUF AF-063-HASHKORREKTUR + BYTEGENAUE 6.72.9-VERSIONSBINDUNG + DANACH LIVE-E2E

## AKTUELLER AUFTRAG

Zielvertrag `ZV-AFFILIATE-ADCELL-001` erfüllen:

`ADCELL API v2 -> accepted + active -> programId-Allowlist -> CSV/Banner/Deeplink automatisch -> zentrale Relevanz-/Creative-/Output-/Veto-Logik`

Kein manueller CSV-Normalweg. Kein Awin-Fallthrough. Kein paralleler Provider-Arbeitsstrang.

## BELASTBARER STAND

Der fachliche ADCELL-Sourcefix ist fertig und kanonisch auf `affiliate-release-current` committed.

Source-Commit:
`99bcc5796226254f7e190f40397210fca96e7d0b`

Kanonische Version:
`6.72.8`

Kanonisches 26-Dateien-Manifest:
`74a5d0d5e48028a9ddd82bcf7a32628dbeb42d0963c9ae431bfe8dee3e2c00e5`

Nach kanonischer Rückbindung tatsächlich ausgeführt PASS:
- ADCELL Static Gate;
- ADCELL Runtime Positiv/Negativ;
- offizieller Tokenweg / Legacy Basic für ADCELL-v2 blockiert;
- accepted+active+programId-Allowlist positiv;
- Gegenfälle fail-closed;
- kein Awin-Fallthrough;
- Awin/OTTO 18/18 byteidentisch;
- Banner-Regression;
- PHP-Lint 21/21;
- originaler Release-Guard Governance/Source/Tree/Start PASS;
- Fresh-Unpack;
- Source/Unpack-Identity 26/26.

Nachweis:
`release/affiliate-zentrale/evidence/adcell_api_v2_committed_full_gate_20260912.txt`

## AKTUELLER BLOCKER

Nicht mehr der ADCELL-Code.

Vor einem neuen installierbaren Testkandidaten greifen AF-026/AF-027: Der neue ADCELL-Kandidat darf nicht erneut intern `6.72.8` heißen. Der kleinste zulässige Schritt ist `6.72.9`.

Dieser version-only Schritt wurde lokal bereits hart geprüft:
- Plugin-Header 6.72.9;
- `const VERSION` 6.72.9;
- readme Stable tag 6.72.9;
- keine fachliche Sourceänderung;
- exakt verifiziertes lokales Manifest `83c75bf16578e986388d684fbd99b4ffff400a11b34aca1c74fd5eb41e6b2f3e`;
- PHP 21/21, ADCELL Static/Positiv/Negativ, Awin/OTTO 18/18, Banner, Fresh-Unpack und 26/26 Identity PASS.

AF-063: Die zuvor in Status/Evidence transkribierte Zeichenfolge `83c75bf1359...` war falsch. Gegenbeweis ist ausgeführt: gespeichertes Manifest = regeneriertes 26-Dateien-Manifest; Fresh-Unpack 26/26 identisch. Nur `83c75bf16578e986388d684fbd99b4ffff400a11b34aca1c74fd5eb41e6b2f3e` darf weitergebunden werden.

6.72.9 ist noch nicht kanonisch, weil die große Hauptplugin-Datei nur über einen nachgewiesen bytegenauen Transportweg geschrieben werden darf. Kein Base64-Blocktransport, keine Rekonstruktion, kein angenäherter Großinhalt.

Zusätzlich bleibt der echte ADCELL-Kontozugang blockiert. Deshalb ist LIVE-E2E noch nicht möglich.

## NEXT ACTION – GENAU EIN SCHRITT

AF-063 vollständig schließen: Governance/Evidence ausschließlich auf den exakt verifizierten 6.72.9-Manifesthash nachziehen. Danach den bereits lokal geprüften reinen Versionsschritt `6.72.8 -> 6.72.9` bytegenau auf `affiliate-release-current` binden.

Danach ohne fachlichen Sourceumbau:
1. neues 26-Dateien-Manifest + Governance an exakt den committed 6.72.9-Stand binden;
2. ADCELL Positiv/Negativ + Awin/OTTO-Regression + Banner-Regression + PHP 21/21 erneut;
3. originalen Release-Guard erneut;
4. Fresh-Unpack + Source/Unpack-Identity erneut;
5. erst dann 6.72.9-Test-Plugin;
6. LIVE-PASS erst nach wiederhergestelltem ADCELL-Zugang und echtem API/WordPress/MariaDB-E2E.

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
- keine Pluginversionskette außerhalb exakt 6.72.9;
- kein 6.72.18-Scratch;
- keine manuelle CSV-Ersatzlösung.
