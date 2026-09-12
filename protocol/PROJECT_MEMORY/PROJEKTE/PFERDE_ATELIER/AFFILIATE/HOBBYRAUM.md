# AFFILIATE – HOBBYRAUM

STAND: 2026-09-12
STATUS: BLOCKED NUR AUF AF-066 READ-ONLY LIVE-API-PREFLIGHT IM ECHTEN WORDPRESS

## AKTUELLER AUFTRAG

Zielvertrag `ZV-AFFILIATE-ADCELL-001` erfüllen:

`ADCELL API v2 -> accepted + active -> programId-Allowlist -> CSV/Banner/Deeplink automatisch -> zentrale Relevanz-/Creative-/Output-/Veto-Logik`

Kein manueller CSV-Normalweg. Kein Awin-Fallthrough. Kein paralleler Provider-Arbeitsstrang.

## BELASTBARER STAND

Der technische/kanonische ADCELL-Teil ist fertig.

- Version: `6.72.19`
- Source-Bind-Commit: `df3e97119fe44ac864701d8de6b946c7c6c3416c`
- technischer Head: `9b5aa4d081ca26e7d89fc55a761b8ad800d723ac`
- Manifest: `694af9869c7aa2b01a51f164173b1c51d9be7c24912c2e129420c3d111346a4b`
- Full Gate: Run `34690118524`, Job `103543774405` → PASS
- kanonischer Artefaktneubau: Run `34692865477`, Job `103551115066` → PASS
- kanonisches Test-ZIP SHA-256: `72f437e5235aaec53631db052e2184b588366c7f8aa7eb72ae1c9e043cdf157f`
- Closeout/Guard-Transition: Run `34693281391`, Job `103552273581` → PASS

Belegt PASS:
- ADCELL Static + Runtime Positiv/Negativ;
- accepted+active+programId-Allowlist;
- Gegenfälle fail-closed;
- kein Awin-Fallthrough;
- Awin/OTTO 18/18;
- Banner Positiv/Negativ;
- PHP 21/21;
- Release-Guard Governance/Source/Tree/Start + PR-Transition;
- Fresh-Unpack/Source-Identity 26/26;
- Versionsmarker 6.72.19.

AF-067 und AF-068 sind geschlossen. Fehlerdetails bleiben ausschließlich in `AFFILIATE_HOBBYRAUM/FEHLERMATRIX.md`.

## AKTUELLER BLOCKER

Nicht Source, Version, Manifest, Governance oder Artefakt.

Einzig offen: **AF-066**.

Der Weblogin/Passwort-Reset ist noch nicht als API-Blocker bewiesen. Im echten WordPress muss zuerst der vorhandene read-only ADCELL-Test **`Token + Programme prüfen`** mit den dort bereits gespeicherten API-Zugangsdaten laufen.

Dieser Chat hat keine verbundene reale WordPress-Laufzeit; daher wurde dieser Live-Preflight **nicht** ausgeführt.

## NEXT ACTION – GENAU EIN SCHRITT

**Im realen WordPress den kanonischen 6.72.19-Stand readbacken und `Token + Programme prüfen` ausführen.**

Danach:
- bei PASS → vorhandenen `accepted` + aktiven `programId` explizit allowlisten und realen ADCELL-/WordPress-/MariaDB-E2E durchführen;
- nur bei fehlenden/ungültigen gespeicherten API-Credentials → Credential-Recovery wird echter Blocker.

Bis zum realen Ergebnis:
- kein Live-PASS;
- `release_allowed=false`;
- keine Sourceänderung;
- kein neuer Kandidat/keine neue Versionsnummer.

## ARBEITSWEG

- technische Autorität: `affiliate-release-current`
- technischer Scope: `protocol/AFFILIATE_RELEASE_ADCELL_AUTOMATION_SCOPE_20260911.md`
- Fehlerautorität: `AFFILIATE_HOBBYRAUM/FEHLERMATRIX.md`
- Task: `AFFILIATE_HOBBYRAUM/TASK.current.json`
- Campus-Stand: `CURRENT_STATE.md`
- Plugin-Kontrollvorgang: `PU-20260912-001`
- kein Codex
- kein Side-Branch als Release-Autorität
- keine historische Rekonstruktion

## NICHT ANFASSEN

- ADCELL-Source bis zum Live-Preflight nicht weiter ändern;
- OTTO/Awin-Arbeit nicht fortsetzen;
- Digistore24 nicht fortsetzen;
- keine neue Providerarchitektur;
- kein separates ADCELL-Plugin;
- keine neue Versionsnummer;
- keine manuelle CSV-Ersatzlösung;
- falsches Vor-Bind-ZIP niemals als Übergabeartefakt verwenden.
