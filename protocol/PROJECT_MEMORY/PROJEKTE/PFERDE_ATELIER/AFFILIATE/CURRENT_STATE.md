# AFFILIATE – CURRENT STATE

STAND: 2026-09-12
STATUS: ADCELL API-V2-SOURCEFIX KANONISCH COMMITTED + FULL GATE + FRESH-UNPACK/IDENTITY PASS / 6.72.9-VERSIONSBINDUNG OFFEN / LIVE-E2E BLOCKED

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

Der ADCELL-Sourcefix ist kanonisch auf `affiliate-release-current` committed.

Source-Commit:
`99bcc5796226254f7e190f40397210fca96e7d0b`

Kanonische Version:
`6.72.8`

Kanonisches 26-Dateien-Manifest:
`74a5d0d5e48028a9ddd82bcf7a32628dbeb42d0963c9ae431bfe8dee3e2c00e5`

Geändert wurden ausschließlich:
- `trait-ppar-provider-registry.php`
- `trait-ppar-network-sync.php`
- `trait-ppar-automation-suite.php`

Nach der kanonischen Rückbindung tatsächlich ausgeführt PASS:
- ADCELL API-v2 Static Gate;
- ADCELL Runtime Positiv/Negativ;
- offizieller Tokenweg; kein Legacy-Basic-Auth-Runtimeweg für ADCELL-v2;
- accepted + active + programId-Allowlist positiv;
- non-allowlisted / inactive / not accepted / malformed / falscher Host / mehrdeutige CSV-Lage fail-closed;
- kein Awin-Fallthrough;
- Awin/OTTO-Funktionsblock-Regression 18/18 byteidentisch;
- Banner-Regression;
- PHP-Lint 21/21;
- originaler Release-Guard Governance/Source/Tree/Start PASS;
- Fresh-Unpack PASS;
- Source/Unpack-Byte-Identity 26/26 PASS.

Dauerhafter Nachweis:
`release/affiliate-zentrale/evidence/adcell_api_v2_committed_full_gate_20260912.txt`

Damit sind für den aktuellen kanonischen Stand AF-023, AF-058, AF-059, AF-060 und AF-062 geschlossen. AF-026/AF-027 bleiben als Versionsgrenze aktiv.

## 6.72.9 – NÄCHSTER INSTALLIERBARER TESTKANDIDAT

Ein reiner Versionsschritt wurde lokal bereits vorbereitet und vollständig gegen denselben Fachworkflow geprüft:
- Plugin-Header `6.72.8 -> 6.72.9`;
- `const VERSION` `6.72.8 -> 6.72.9`;
- readme `Stable tag` `6.72.8 -> 6.72.9`;
- keine fachliche Sourceänderung.

Lokales 6.72.9-Manifest:
`83c75bf1359aa989313416c9f9c7d1d4193bfe44a15bef08a83ac45580911bc8`

Auch hier PASS: PHP 21/21, ADCELL Static, ADCELL Positiv/Negativ, Awin/OTTO 18/18, Banner, Fresh-Unpack und 26/26 Identity.

6.72.9 ist **noch nicht kanonisch committed**. Die große Hauptplugin-Datei darf nur über einen nachgewiesen bytegenauen Transferweg geschrieben werden; kein gekürzter oder rekonstruierter Inhalt.

## LIVE-BLOCKER

Der ADCELL-Kontozugang ist weiterhin nicht wiederhergestellt. Deshalb ist echter ADCELL-Live-API-/WordPress-/MariaDB-E2E-PASS noch gesperrt.

## NEXT ACTION

Exakt aus `HOBBYRAUM.md`:

**Nur den bereits lokal geprüften version-only Schritt 6.72.8 -> 6.72.9 bytegenau kanonisieren; danach Manifest/Governance binden und dieselben committed Gates + Fresh-Unpack/Identity erneut ausführen.**

Erst danach Test-Plugin. LIVE-PASS erst nach echtem ADCELL-Zugang und realem API/WordPress/MariaDB-E2E.
