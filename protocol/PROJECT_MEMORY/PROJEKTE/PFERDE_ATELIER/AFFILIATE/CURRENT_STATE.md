# AFFILIATE – CURRENT STATE

STAND: 2026-09-12
STATUS: ADCELL 6.72.19 KANONISCH GEBUNDEN + VOLLE KANONISCHE GATES/FRESH-UNPACK PASS / LIVE-E2E BLOCKED

## AUTORITÄT

Diese Datei ist die einzige aktuelle Campus-Standzusammenfassung des Büros AFFILIATE.

- aktuelle Arbeit / NEXT ACTION → `HOBBYRAUM.md`
- Fehlerdetails → `AFFILIATE_HOBBYRAUM/FEHLERMATRIX.md` auf `affiliate-release-current`
- Zielvertrag → `ZV-AFFILIATE-ADCELL-001`
- technische Release-Autorität → Branch `affiliate-release-current`
- technischer Scope → `protocol/AFFILIATE_RELEASE_ADCELL_AUTOMATION_SCOPE_20260911.md`

## VERBINDLICHES ZIEL

ADCELL vollautomatisch über API v2:

`accepted + active Programme -> explizite programId-Allowlist -> CSV/Banner/Deeplink automatisch -> bestehende zentrale Relevanz-/Creative-/Output-/Veto-Logik`

Kein Awin-Fallthrough. Kein manueller CSV-Import/Export als Normalbetrieb. Nicht freigegebene oder inaktive Programme fail-closed.

OTTO/Awin bleibt pausiert und ungelöst. Digistore24 bleibt zurückgestellt. Kein paralleler Provider-Arbeitsstrang.

Der Zielvertrag bleibt **AKTIV**: der technische/kannonische Teil ist grün, der reale ADCELL-Live-API- und WordPress/MariaDB-E2E-Nachweis fehlt noch.

## BELASTBARER TECHNISCHER STAND

Pluginbüro-Stand 6.72.17 und der geprüfte ADCELL-API-v2-Fix wurden konfliktfrei zusammengeführt und als **6.72.19** kanonisch gebunden.

Kanonischer Source-Bind-Commit:
`df3e97119fe44ac864701d8de6b946c7c6c3416c`

Aktueller technischer Branch-Head nach Scope-Cleanup:
`75a2368cfe1efbfb623aa263da16a9ee7ab96462`

Kanonische Version:
`6.72.19`

Kanonisches 26-Dateien-Manifest:
`694af9869c7aa2b01a51f164173b1c51d9be7c24912c2e129420c3d111346a4b`

Kanonischer Full-Gate-Lauf:
- Run `34690118524`
- Job `103543774405`
- Ergebnis: PASS

Tatsächlich belegt PASS:
- ADCELL API-v2 Static Gate;
- ADCELL Runtime Positiv/Negativ über exakt hash-identische kanonische ADCELL-Dateien;
- offizieller Tokenweg; kein Legacy-Basic-Auth-Runtimeweg;
- accepted + active + programId-Allowlist positiv;
- non-allowlisted / inactive / not accepted / falscher Host / mehrdeutige CSV-Lage fail-closed;
- kein Awin-Fallthrough;
- Awin/OTTO-Funktionsblock-Regression 18/18 PASS;
- Banner Positiv/Negativ PASS;
- PHP-Lint 21/21 PASS;
- originaler Release-Guard Governance/Source/Tree/Start PASS;
- Fresh-Unpack PASS;
- Source/ZIP-Byte-Identity 26/26 PASS;
- Plugin-Header / const VERSION / Stable tag = 6.72.19 PASS.

Dauerhafter Nachweis:
`release/affiliate-zentrale/evidence/adcell_67219_canonical_full_gate_20260912.txt`

Status-Closeout wurde danach erneut durch den Release-Guard geprüft: Run `34690263204`, Job `103544153132` → Governance/Source/Tree/Start PASS.

AF-064 ist geschlossen: vor Versionswahl wird der echte Pluginbüro-Stand geprüft; 6.72.17 war die richtige Integrationsbasis.
AF-065 ist geschlossen: der unveränderliche Governance-Wert `new_version_policy` wurde wieder exakt auf den Guard-Vertragswert gesetzt und derselbe Gate-Lauf danach erfolgreich wiederholt.

Temporäre ADCELL-Transport-/Gate-Workflows wurden nach dem PASS wieder entfernt. Kein zusätzlicher dauerhafter Runner bleibt zurück.

## LIVE-BLOCKER

Der ADCELL-Kontozugang ist weiterhin nicht wiederhergestellt; Passwort-Reset-Mail kommt nicht an.

Deshalb weiterhin **kein Live-PASS** und `release_allowed=false`:
- echter ADCELL API-v2-Lauf fehlt;
- echter WordPress/MariaDB-E2E fehlt.

## NEXT ACTION

Exakt aus `HOBBYRAUM.md`:

**Keine weitere Sourcearbeit. Sobald der ADCELL-Kontozugang wieder funktioniert: genau den echten ADCELL-API-v2-Lauf ausführen und danach den echten WordPress/MariaDB-E2E. Erst bei deren PASS darf der ADCELL-Zielvertrag als erfüllt/LIVE-PASS behandelt werden.**
