# AFFILIATE – HOBBYRAUM

STAND: 2026-09-11
STATUS: BLOCKED

## AKTUELLER AUFTRAG

ADCELL vollautomatisch über API v2 anbinden.

Normalweg:
`accepted + active Programme -> explizite programId-Allowlist -> CSV/Banner/Deeplink automatisch -> zentrale Affiliate-Prüfung/Ausgabe`.

Kein manueller Import/Export als Normalbetrieb.

## BLOCKER

Der exakte technische ADCELL-API-v2-Authentifizierungsvertrag ist noch nicht autoritativ belegt.

Zusätzlich ist der Nutzerzugang zu ADCELL aktuell gesperrt/unerreichbar, weil das Passwort überschrieben wurde und der Passwort-Zurücksetzen-Mailweg nicht funktioniert.

Deshalb:
- keine API-Authentifizierung raten;
- kein kanonischer Source-Fix vor Auth-Beleg;
- kein Live-PASS.

## NEXT ACTION

**GENAU EIN SCHRITT:**
Exakten ADCELL-API-v2-Authentifizierungsvertrag aus autoritativer ADCELL-Dokumentation belegen.

Danach, ohne Parallelweg:
- kanonische Basis 6.72.8 verwenden;
- ADCELL provider-spezifisch routen;
- accepted+active + programId-Allowlist fail-closed;
- CSV/Banner/Deeplink automatisch via API v2;
- POSITIV/NEGATIV/Gesamtworkflow;
- Fresh-Unpack + Source/ZIP-Identity;
- erst danach Test-Plugin.

## ARBEITSWEG

Technische Arbeits-/Rückgabeautorität:
`affiliate-release-current`

Task:
`AFFILIATE_HOBBYRAUM/TASK.current.json`

Scope:
`protocol/AFFILIATE_RELEASE_ADCELL_AUTOMATION_SCOPE_20260911.md`

Fehler:
`AFFILIATE_HOBBYRAUM/FEHLERMATRIX.md`

Side-Branch `hobbyroom/adcell-api-v2-automation-20260911` ist frisch geprüft identisch zum früheren Release-Head und enthält keinen Fix. Für release-scoped Änderungen nicht verwenden.

## NICHT ANFASSEN

- Digistore24: BLOCKED/zurückgestellt, siehe `DIGISTORE24_STATUS.md`;
- OTTO/Awin: ungelöst und pausiert, nicht parallel fortsetzen;
- keine neue Providerarchitektur;
- kein eigenes ADCELL-Plugin;
- keine Pluginversionskette;
- keinen 6.72.18-Scratch übernehmen;
- keine manuelle CSV-URL als Ersatz für Vollautomatik;
- keine Authentifizierung raten.
