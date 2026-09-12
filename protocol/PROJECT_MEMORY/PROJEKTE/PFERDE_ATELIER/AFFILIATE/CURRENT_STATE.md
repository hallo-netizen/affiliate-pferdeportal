# AFFILIATE – CURRENT STATE

STAND: 2026-09-12
STATUS: ADCELL 6.72.19 KANONISCH + FULL GATE + KANONISCHER ARTEFAKT-26/26-PASS / AF-066 LIVE-PREFLIGHT BLOCKED

## AUTORITÄT

Diese Datei ist die einzige aktuelle Campus-Standzusammenfassung des Büros AFFILIATE.

- aktuelle Arbeit / NEXT ACTION → `HOBBYRAUM.md`
- Fehlerdetails → `AFFILIATE_HOBBYRAUM/FEHLERMATRIX.md` auf `affiliate-release-current`
- Zielvertrag → `ZV-AFFILIATE-ADCELL-001`
- technische Release-Autorität → Branch `affiliate-release-current`
- technischer Scope → `protocol/AFFILIATE_RELEASE_ADCELL_AUTOMATION_SCOPE_20260911.md`
- Plugin-Kontrollvorgang → `PU-20260912-001` im PB-ONE-PLUGINS-Updateprotokoll

## VERBINDLICHES ZIEL

ADCELL vollautomatisch über API v2:

`accepted + active Programme -> explizite programId-Allowlist -> CSV/Banner/Deeplink automatisch -> bestehende zentrale Relevanz-/Creative-/Output-/Veto-Logik`

Kein Awin-Fallthrough. Kein manueller CSV-Import/Export als Normalbetrieb. Nicht freigegebene oder inaktive Programme fail-closed.

OTTO/Awin bleibt pausiert und ungelöst. Digistore24 bleibt zurückgestellt. Kein paralleler Provider-Arbeitsstrang.

Der Zielvertrag bleibt **AKTIV**: technische/kanonische Gates sind grün, der reale ADCELL-/WordPress-/MariaDB-Live-Nachweis fehlt.

## BELASTBARER TECHNISCHER STAND

Pluginbüro-Stand 6.72.17 und der geprüfte ADCELL-API-v2-Fix wurden konfliktfrei als **6.72.19** zusammengeführt.

- kanonischer Source-Bind-Commit: `df3e97119fe44ac864701d8de6b946c7c6c3416c`
- aktueller technischer Head nach Abschluss-/Nachholprüfung: `9b5aa4d081ca26e7d89fc55a761b8ad800d723ac`
- Version: `6.72.19`
- 26-Dateien-Manifest: `694af9869c7aa2b01a51f164173b1c51d9be7c24912c2e129420c3d111346a4b`

Kanonischer Full-Gate-Lauf `34690118524`, Job `103543774405` → PASS:
- ADCELL API-v2 Static + Runtime Positiv/Negativ;
- offizieller Tokenweg; kein Legacy-Basic-Auth-Runtimeweg;
- accepted + active + programId-Allowlist positiv;
- Gegenfälle fail-closed;
- kein Awin-Fallthrough;
- Awin/OTTO 18/18;
- Banner Positiv/Negativ;
- PHP 21/21;
- Release-Guard Governance/Source/Tree/Start;
- Fresh-Unpack + Source/ZIP-Identity 26/26;
- Versionsmarker 6.72.19.

Dauerhafter Full-Gate-Nachweis:
`release/affiliate-zentrale/evidence/adcell_67219_canonical_full_gate_20260912.txt`

## ABSCHLUSS-/NACHHOLPRÜFUNG

AF-067 ist geschlossen: ein neues Testartefakt wurde **direkt aus der kanonischen 6.72.19-Source** gebaut.

Run `34692865477`, Job `103551115066` → PASS:
- Manifest 26/26;
- PHP 21/21;
- Versionsmarker 6.72.19;
- Fresh-Unpack/Source-Identität 26/26;
- Test-ZIP SHA-256 `72f437e5235aaec53631db052e2184b588366c7f8aa7eb72ae1c9e043cdf157f`.

AF-068 ist geschlossen: der zunächst ungültige temporäre Closeout-Workflow wurde als Fehler gebunden, vor Wiederholung mit YAML-Parser geprüft und anschließend erfolgreich ausgeführt. Run `34693281391`, Job `103552273581` → SUCCESS; Governance/Source/Tree/Start und PR-Transition PASS. Temporärer Workflow ist wieder entfernt.

## EINZIG OFFEN: AF-066

Der fehlende ADCELL-Weblogin ist **nicht** als technischer API-Blocker bewiesen.

Nächster echter Gate ist im realen WordPress read-only:
**`Token + Programme prüfen`** mit den bereits dort gespeicherten ADCELL-API-Zugangsdaten.

Bei PASS: vorhandenen `accepted` + aktiven `programId` explizit allowlisten und direkt realen ADCELL-/WordPress-/MariaDB-E2E ausführen.

Nur wenn gespeicherte API-Zugangsdaten fehlen/ungültig sind, wird Credential-Recovery zum echten Blocker.

Bis dahin:
- kein Live-PASS;
- `release_allowed=false`;
- keine weitere Sourcearbeit;
- keine neue Versionskette.

## NEXT ACTION

**Im realen WordPress den kanonischen 6.72.19-Stand readbacken und read-only `Token + Programme prüfen` ausführen. Danach ausschließlich nach diesem Ergebnis weiter.**
