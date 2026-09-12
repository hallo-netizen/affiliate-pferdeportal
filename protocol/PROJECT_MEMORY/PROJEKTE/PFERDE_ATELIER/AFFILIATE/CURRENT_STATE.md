# AFFILIATE – CURRENT STATE

STAND: 2026-09-12
STATUS: ADCELL API-V2-KANDIDAT LOKAL GEPRÜFT / KANONISCHE RÜCKBINDUNG OFFEN

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

## BELASTBARER TECHNISCHER STAND

`AF-023` wurde geschlossen: der damalige partielle Source-Stand wurde wieder korrekt an Manifest/Governance gebunden und der originale Release-Guard real mit Governance/Source/Tree/Start PASS ausgeführt.

Darauf wurde im isolierten lokalen Prüfraum der kleinste ADCELL-Kandidat aus der kanonischen 6.72.8-Basis gebaut. Geändert sind ausschließlich:
- `trait-ppar-provider-registry.php`
- `trait-ppar-network-sync.php`
- `trait-ppar-automation-suite.php`

Ausgeführt und bestanden:
- ADCELL API-v2 Static Gate;
- ADCELL Runtime Positiv/Negativ inkl. Token, accepted+active+Allowlist, Host-/CSV-Fail-closed, Banner/Deeplink;
- AF-062 Legacy-Basic-Auth-Runtimeweg blockiert;
- aktuelle Awin/OTTO-Funktionsblock-Regression 18/18 byteidentisch;
- Banner-Regressionsgate;
- PHP-Lint 21/21;
- finaler lokaler originaler Release-Guard Governance/Source/Tree/Start PASS.

Lokales Kandidaten-Manifest:
`74a5d0d5e48028a9ddd82bcf7a32628dbeb42d0963c9ae431bfe8dee3e2c00e5`

Dauerhafter technischer Nachweis:
`release/affiliate-zentrale/evidence/adcell_api_v2_local_full_gate_unbound_20260912.txt`

## WICHTIGE GRENZE

Der lokal geprüfte Kandidat ist **noch nicht die kanonische Source**, weil die drei geprüften Source-Dateien noch nicht bytegenau auf `affiliate-release-current` zurückgebunden wurden.

Deshalb weiterhin:
- kein kanonischer ADCELL-Gesamt-PASS;
- kein Plugin/ZIP;
- kein Release-PASS.

Der kanonische Branch enthält weiterhin den davor gebundenen partiellen ADCELL-Stand plus Test-/Evidence-/Task-Protokollierung.

## LIVE-BLOCKER

Der ADCELL-Kontozugang ist weiterhin nicht wiederhergestellt. Deshalb ist echter ADCELL-Live-API-/WordPress-/MariaDB-E2E-PASS noch gesperrt.

## NEXT ACTION

Exakt aus `HOBBYRAUM.md`:

**Die drei lokal bereits geprüften ADCELL-Source-Dateien bytegenau auf `affiliate-release-current` zurückbinden, Manifest/Governance atomar an diesen committed Sourcezustand binden und dieselben Gates auf dem committed Stand erneut ausführen.**

Erst danach Fresh-Unpack + Source/ZIP-Identity und Test-Plugin. Live-PASS erst nach echtem ADCELL-Zugang.
