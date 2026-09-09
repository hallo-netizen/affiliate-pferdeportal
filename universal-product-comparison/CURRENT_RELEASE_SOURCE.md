# UNIVERSAL PRODUCT COMPARISON – CURRENT RELEASE SOURCE STATUS

Stand: 2026-09-09

## HARD RULE

Der aktuell in diesem GitHub-Verzeichnis sichtbare historische Source-Bestand ist **NICHT** die freigegebene Build-/Runner-Quelle für 0.8.3.

Nicht daraus:
- neue ZIP bauen;
- Version ableiten;
- Regression behaupten;
- Folgefix starten.

## Aktuell freigegebener Testkandidat

`universal-product-comparison-0.8.3-prototype.zip`

SHA-256:
`4c08ca1df348ab49849ddde8f85980db450694c58010cd0c431575bc6a3cd11e`

Die exakte ZIP enthält:
`tests/HARD_LOCAL_TEST_REPORT_0.8.3.json`

Dieser Report bindet die geprüfte Quelle über 56 Source-Datei-SHA256-Werte.

Finale Prüfung:
- 25/25 ausführbare Tests PASS;
- PHP-Lint 43/43 PASS;
- Source↔ZIP 57/57 exakt;
- Report-Hashbindung 56/56 exakt.

## Warum keine stille Source-Synchronisierung

Der 0.8.x-Kandidat wurde als exakte Fresh-ZIP lokal hart geprüft; der historische GitHub-Ordner stammt aus einer älteren Entwicklungsstufe.

Eine teilweise oder manuell nachgebaute Source-Synchronisierung würde eine neue Scheinsicherheit erzeugen.

KISS:
Bis zu einer späteren **exakten byte-identischen Source-Materialisierung** ist ausschließlich die gebundene 0.8.3-ZIP die Release-Kandidaten-Wahrheit.

## Folgearbeit

Vor jeder weiteren Codeänderung:
1. exakt diese 0.8.3-ZIP materialisieren;
2. SHA prüfen;
3. daraus den isolierten Arbeitsbaum erzeugen;
4. erst dann ändern;
5. wieder Fresh-ZIP + komplette Regression.

GitHub-Akten bleiben aktuelle Status-/WHY-Wahrheit.
Der alte Source-Bestand bleibt nur historischer technischer Bestand.
