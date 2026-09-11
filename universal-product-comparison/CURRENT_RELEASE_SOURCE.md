# UNIVERSAL PRODUCT COMPARISON – CURRENT RELEASE SOURCE STATUS

Stand: 2026-09-11

## HARD RULE

Der aktuell in diesem GitHub-Verzeichnis sichtbare historische Source-Bestand ist **NICHT** die freigegebene Build-/Runner-Quelle für 0.8.5.

Nicht daraus:
- neue ZIP bauen;
- Version ableiten;
- Regression behaupten;
- Folgefix starten.

## Aktuell freigegebener Testkandidat

`universal-product-comparison-0.8.5-prototype.zip`

SHA-256:
`0174051e6584902142f5be5787642426b30aab6c7ba15ef0b07ccbdb4a5844fd`

Die exakte ZIP enthält:
`tests/HARD_LOCAL_TEST_REPORT_0.8.5.json`

Der Report bindet 70 Source-Datei-SHA256-Werte.

Finale Prüfung:
- 35/35 ausführbare Tests PASS;
- PHP-Lint 50/50 PASS;
- Source↔ZIP 71/71 exakt;
- Report-Hashbindung 70/70 exakt;
- 175/175 Portalparität PASS;
- 130 zusätzliche echte Cross-Family-Paare aus vorhandenem Product Knowledge fachlich gebunden;
- Herstellerfamilien-Readiness und Paarplaner identisch fail-closed.

## Portalbindung

Autoritative Quelle:
`affiliate-portal-router/assets/portal-structure-v279.json`

SHA-256:
`b86a160e6b8cf720077830422ca6b574203ce171fdc65d357fe9c6bed039c2e0`

Abgeleiteter autoritativer Katalog SHA-256:
`4eecef55a3033a4691f8a832eba5fb1657cdb15826ee47d366dccbaabfbb1fa2`

## Warum keine stille Source-Synchronisierung

0.8.5 wurde aus der exakt geprüften 0.8.4-ZIP abgeleitet und erneut als Fresh-ZIP vollständig geprüft.

Der historische GitHub-Source-Ordner ist nicht automatisch byte-identisch zu dieser Release-Kandidatenquelle.
Eine teilweise Synchronisierung würde Scheinsicherheit erzeugen.

KISS:
Bis zu einer späteren **exakten byte-identischen Source-Materialisierung** ist ausschließlich die gebundene 0.8.5-ZIP die Release-Kandidaten-Wahrheit.

## Folgearbeit

Vor jeder weiteren Codeänderung:
1. exakt die 0.8.5-ZIP materialisieren;
2. SHA prüfen;
3. daraus isolierten Arbeitsbaum erzeugen;
4. erst dann ändern;
5. wieder komplette positive/negative/Gesamtworkflow-/Fresh-ZIP-Prüfung.

GitHub-Akten bleiben Status-/WHY-Wahrheit.
Der alte Source-Bestand bleibt historischer technischer Bestand.
