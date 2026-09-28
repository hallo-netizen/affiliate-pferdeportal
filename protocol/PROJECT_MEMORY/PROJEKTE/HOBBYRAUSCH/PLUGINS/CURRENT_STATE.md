# HOBBYRAUSCH – PLUGINS – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-09-28
STATUS: HD-001 V1.8.7 SIMPLE REVIEW BEREIT / INITIAL-REVIEW SIGNIERT

## Rolle

Einzige aktuelle Zustandsautorität des Scopes `HOBBYRAUSCH_PLUGINS`.

## Aktueller belastbarer Stand

V1.8.6 hat DataForSEO live erfolgreich durchlaufen. Der bereinigte Testlabor-Draft wurde danach live serverseitig als Initial-Review signiert.

Die zuvor unnötig manuell verlangten Felder Review-Scope SHA-256 und Freigabe-Zusammenfassung wurden in V1.8.7 aus allen drei Review-Formularen entfernt.

V1.8.7 erzeugt diese technischen Werte selbst und behält:
- explizite Nutzerbestätigung;
- Admin-/Nonce-Schutz;
- serverseitig signierte Quittung;
- Scope-Bindung;
- Folgevalidierung.

Teststatus:
- 227/227 PASS;
- Fresh-Unpack 227/227 PASS;
- PHP 17/17 Source und 16/16 Runtime;
- Runtime-Parität 21/21.

## NEXT ACTION

V1.8.7 installieren und die bereits signierte Initial-Datei für den kostenlosen Global-Coverage-Preflight verwenden.
