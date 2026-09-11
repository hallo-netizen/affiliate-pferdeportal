# UNIVERSAL PRODUCT COMPARISON – CURRENT RELEASE SOURCE STATUS

Stand: 2026-09-11

## HARD RULE

Der aktuell in diesem GitHub-Verzeichnis sichtbare historische Source-Bestand ist **NICHT** die freigegebene Build-/Runner-Quelle für 0.8.5.

Nicht daraus:
- neue ZIP bauen;
- Version ableiten;
- Regression behaupten;
- Folgefix starten.

## Aktuell freigegebener technischer Testkandidat

`universal-product-comparison-0.8.5-prototype.zip`

SHA-256:
`0174051e6584902142f5be5787642426b30aab6c7ba15ef0b07ccbdb4a5844fd`

Die exakte ZIP enthält:
`tests/HARD_LOCAL_TEST_REPORT_0.8.5.json`

Der Report bindet 70 Source-Datei-SHA256-Werte.

Finale lokale Prüfung:
- 35/35 ausführbare Tests PASS;
- PHP-Lint 50/50 PASS;
- Source↔ZIP 71/71 exakt;
- Report-Hashbindung 70/70 exakt;
- 175/175 Portalparität PASS;
- Herstellerfamilien-Readiness und Paarplaner identisch fail-closed.

## Interpretationskorrektur zu den 130 Paaren

Der 0.8.5-Lokaltest bewies für fünf zusätzliche Fachprofile insgesamt **130 katalogseitige Cross-Family-Paarpotentiale**, wenn die freigegebenen Recherchekandidaten erfolgreich als Product Knowledge materialisiert vorliegen.

Er bewies **nicht**, dass diese 130 Paare bereits auf WordPress als reales Product-Knowledge-Inventar vorhanden waren.

Der echte WordPress-Vorcheck zeigte diese Grenze korrekt fail-closed und führte zu:
`AKTENSCHRANK/12_V085_LIVE_INVENTORY_GAP_UPK051_HARD_LOCAL_RECEIPT.md`.

Danach wurde Universal Product Knowledge 0.5.1 über den vorhandenen kanonischen Importweg real ausgeführt. Der Live-Batch materialisierte die kleine Alt-Recherchebasis von 17 Gruppen; eine neue globale reale Paarzahl wurde nach diesem Batch noch nicht separat im Produktvergleich abgelesen und wird hier nicht behauptet.

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
Bis zu einer späteren **exakten byte-identischen Source-Materialisierung** ist ausschließlich die gebundene 0.8.5-ZIP die technische Release-Kandidaten-Wahrheit.

## Folgearbeit

Aktueller Arbeitsblock ist Marktrecherche, nicht Code.

Vor jeder späteren Codeänderung:
1. exakt die 0.8.5-ZIP materialisieren;
2. SHA prüfen;
3. daraus isolierten Arbeitsbaum erzeugen;
4. erst dann ändern;
5. wieder komplette positive/negative/Gesamtworkflow-/Fresh-ZIP-Prüfung.

Vor jeder Plugin-Übergabe an den Nutzer muss die **exakt auszugebende ZIP** selbst positiv, negativ/Mutation und gegen den vollständigen aktuellen Produktvergleichsworkflow geprüft sein.

GitHub-Akten bleiben Status-/WHY-Wahrheit.
Der alte Source-Bestand bleibt historischer technischer Bestand.
