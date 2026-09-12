# AFFILIATE – HOBBYRAUM

STAND: 2026-09-12
STATUS: BLOCKED NUR AUF ECHTEN ADCELL-LIVE-API- + WORDPRESS/MARIADB-E2E-NACHWEIS

## AKTUELLER AUFTRAG

Zielvertrag `ZV-AFFILIATE-ADCELL-001` erfüllen:

`ADCELL API v2 -> accepted + active -> programId-Allowlist -> CSV/Banner/Deeplink automatisch -> zentrale Relevanz-/Creative-/Output-/Veto-Logik`

Kein manueller CSV-Normalweg. Kein Awin-Fallthrough. Kein paralleler Provider-Arbeitsstrang.

## BELASTBARER STAND

Der technische/kannonische ADCELL-Teil ist fertig.

Kanonische Version:
`6.72.19`

Kanonischer Source-Bind-Commit:
`df3e97119fe44ac864701d8de6b946c7c6c3416c`

Aktueller technischer Branch-Head nach Scope-Cleanup:
`75a2368cfe1efbfb623aa263da16a9ee7ab96462`

Kanonisches 26-Dateien-Manifest:
`694af9869c7aa2b01a51f164173b1c51d9be7c24912c2e129420c3d111346a4b`

Kanonischer Full-Gate-Lauf:
- Run `34690118524`
- Job `103543774405`
- PASS

Belegt PASS:
- ADCELL Static;
- ADCELL Runtime Positiv/Negativ über hash-identische kanonische Dateien;
- accepted+active+programId-Allowlist;
- Gegenfälle fail-closed;
- kein Awin-Fallthrough;
- Awin/OTTO 18/18;
- Banner Positiv/Negativ;
- PHP 21/21;
- Release-Guard Governance/Source/Tree/Start;
- Fresh-Unpack;
- Source/ZIP-Identity 26/26;
- Versionsmarker 6.72.19 konsistent.

Dauerhafter Nachweis:
`release/affiliate-zentrale/evidence/adcell_67219_canonical_full_gate_20260912.txt`

Status-Closeout wurde anschließend ebenfalls gegen denselben Release-Guard geprüft: Run `34690263204`, Job `103544153132` → PASS.

AF-064 und AF-065 sind geschlossen. Temporäre Transport-/Gate-Workflows wurden entfernt.

## AKTUELLER BLOCKER

Nicht mehr Source, Version, Manifest, Governance oder lokaler/kannonischer Test.

Einziger Blocker:
**ADCELL-Kontozugang funktioniert noch nicht; Passwort-Reset-Mail kommt nicht an.**

Damit fehlen noch genau:
1. echter ADCELL API-v2-Lauf mit dem realen Account;
2. echter WordPress/MariaDB-E2E gegen den kanonischen 6.72.19-Stand.

Bis dahin:
- kein Live-PASS;
- `release_allowed=false`;
- keine weitere Sourceänderung;
- kein neuer Plugin-Kandidat;
- keine neue Versionskette.

## NEXT ACTION – GENAU EIN SCHRITT

**Warten, bis der ADCELL-Zugang wiederhergestellt ist. Dann exakt den realen ADCELL-API-v2-Test ausführen und direkt danach den realen WordPress/MariaDB-E2E.**

Nur wenn beide PASS sind, darf der Zielvertrag abgeschlossen bzw. ein Live-PASS ausgesprochen werden.

## ARBEITSWEG

- technische Autorität: `affiliate-release-current`
- technischer Scope: `protocol/AFFILIATE_RELEASE_ADCELL_AUTOMATION_SCOPE_20260911.md`
- Fehlerautorität: `AFFILIATE_HOBBYRAUM/FEHLERMATRIX.md`
- Task: `AFFILIATE_HOBBYRAUM/TASK.current.json`
- Campus-Stand: `CURRENT_STATE.md`
- kein Codex
- kein Side-Branch als Release-Autorität
- keine historische Rekonstruktion

## NICHT ANFASSEN

- ADCELL-Source bis zum Live-Test nicht weiter ändern;
- OTTO/Awin-Arbeit nicht fortsetzen;
- Digistore24 nicht fortsetzen;
- keine neue Providerarchitektur;
- kein separates ADCELL-Plugin;
- keine neue Versionsnummer vor dem realen Live-Test;
- keine manuelle CSV-Ersatzlösung.
