# UNIVERSAL PRODUCT COMPARISON – CURRENT RELEASE SOURCE STATUS

Stand: 2026-09-11

## HARD RULE

Der aktuell in diesem GitHub-Verzeichnis sichtbare historische Source-Bestand ist **NICHT** die freigegebene Build-/Runner-Quelle für 0.8.4.

Nicht daraus:
- neue ZIP bauen;
- Version ableiten;
- Regression behaupten;
- Folgefix starten.

## Aktuell freigegebener Testkandidat

`universal-product-comparison-0.8.4-prototype.zip`

SHA-256:
`00035ec0e166d9830f97140b6fc0f4f7666504d548bac507b1b206a2173ce856`

Die exakte ZIP enthält:
`tests/HARD_LOCAL_TEST_REPORT_0.8.4.json`

Der Report bindet 66 Source-Datei-SHA256-Werte.

Finale Prüfung:
- 32/32 ausführbare Tests PASS;
- PHP-Lint 48/48 PASS;
- Source↔ZIP 67/67 exakt;
- Report-Hashbindung 66/66 exakt;
- 175/175 Portalparität PASS.

## Portalbindung

Autoritative Quelle:
`affiliate-portal-router/assets/portal-structure-v279.json`

SHA-256:
`b86a160e6b8cf720077830422ca6b574203ce171fdc65d357fe9c6bed039c2e0`

Abgeleiteter autoritativer Katalog SHA-256:
`4eecef55a3033a4691f8a832eba5fb1657cdb15826ee47d366dccbaabfbb1fa2`

## Warum keine stille Source-Synchronisierung

0.8.4 wurde aus der exakt geprüften 0.8.3-ZIP abgeleitet und anschließend erneut als Fresh-ZIP vollständig geprüft.

Der historische GitHub-Source-Ordner ist nicht automatisch byte-identisch zu dieser Release-Kandidatenquelle.
Eine teilweise Synchronisierung würde Scheinsicherheit erzeugen.

KISS:
Bis zu einer späteren **exakten byte-identischen Source-Materialisierung** ist ausschließlich die gebundene 0.8.4-ZIP die Release-Kandidaten-Wahrheit.

## Folgearbeit

Vor jeder weiteren Codeänderung:
1. exakt die 0.8.4-ZIP materialisieren;
2. SHA prüfen;
3. daraus isolierten Arbeitsbaum erzeugen;
4. erst dann ändern;
5. wieder komplette positive/negative/Gesamtworkflow-/Fresh-ZIP-Prüfung.

GitHub-Akten bleiben Status-/WHY-Wahrheit.
Der alte Source-Bestand bleibt historischer technischer Bestand.
