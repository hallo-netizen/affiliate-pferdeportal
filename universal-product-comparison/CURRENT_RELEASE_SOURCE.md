# UNIVERSAL PRODUCT COMPARISON – CURRENT RELEASE SOURCE STATUS

Stand: 2026-09-11

## HARD RULE

Der aktuell in diesem GitHub-Verzeichnis sichtbare historische Source-Bestand ist **NICHT** die freigegebene Build-/Runner-Quelle für den aktuellen Testkandidaten.

Nicht daraus:
- neue ZIP bauen;
- Version ableiten;
- Regression behaupten;
- Folgefix starten.

GitHub-Akten bleiben Status-/WHY-Wahrheit. Der alte Source-Bestand bleibt historischer technischer Bestand.

## Aktuell freigegebener technischer Testkandidat

`universal-product-comparison-0.8.6-prototype.zip`

SHA-256:
`6ad160d18fb0973463c214de4356447923cbb728e222725e5407868e580c24f6`

Die exakte ZIP enthält:
`tests/HARD_LOCAL_TEST_REPORT_0.8.6.json`

Der Report bindet 73 Source-Datei-SHA256-Werte.

Finale lokale Fresh-ZIP-Prüfung:
- ausführbare Regression **38/38 PASS**;
- PHP-Lint **51/51 PASS**;
- Source↔ZIP **74/74 exakt**;
- Report-Hashbindung **73/73 exakt**;
- 175/175 Portalparität PASS;
- synthetische 1000-Pair-No-Cap-Regel PASS;
- Herstellerfamilien-/Paar-/Dossier-/Kosten-Schutzregeln PASS;
- zwei neue Lifecycle-Rückfallmutationen korrekt ROT;
- kein Writer-/Draft-/Publishweg.

WordPress-Live für 0.8.6 ist **noch offen**.

Dauerbeleg:
`protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/PRODUKTVERGLEICH/AKTENSCHRANK/39_V086_LIFECYCLE_REEVALUATION_HARD_LOCAL_RECEIPT.md`.

## Ableitung / Root Cause

0.8.6 wurde ausschließlich aus der erneut materialisierten exakten 0.8.5-ZIP abgeleitet.

Gebundene 0.8.5-Ausgangs-ZIP:
`universal-product-comparison-0.8.5-prototype.zip`

SHA-256:
`0174051e6584902142f5be5787642426b30aab6c7ba15ef0b07ccbdb4a5844fd`

Bewiesener Fehler:
0.8.5 las das aktuelle Product Knowledge zwar bei jeder Planung neu, ließ aber `DISCONTINUED`, `UNKNOWN` und fehlenden Lifecycle in Paaruniversum/Readiness einfließen.

Sollregression gegen unveränderte 0.8.5 war real ROT: 3 Paare statt 1 gültigem Paar.

0.8.6 schließt ausschließlich diesen Gap:
- `ACTIVE` paarbar;
- `TEMPORARILY_UNAVAILABLE` paarbar;
- `DISCONTINUED` ausgeschlossen;
- `UNKNOWN`/fehlend fail-closed ausgeschlossen;
- kanonische Deduplizierung vor Lifecycle-Gate verhindert Wiederbelebung älterer ACTIVE-Zeilen.

## Product-Knowledge-Bindung

Gegenprüfte aktuelle UPK-ZIP:
`universal-product-knowledge-0.5.1-prototype.zip`

SHA-256:
`17ba686ebbfeac774de5224a042e8ea5fcc472b91774c47271e6b585d74960a1`

Research Candidate Evidence bleibt ausdrücklich **nicht** automatisch Product Knowledge.

## Portalbindung

Autoritative Quelle:
`affiliate-portal-router/assets/portal-structure-v279.json`

SHA-256:
`b86a160e6b8cf720077830422ca6b574203ce171fdc65d357fe9c6bed039c2e0`

Abgeleiteter autoritativer Katalog SHA-256:
`4eecef55a3033a4691f8a832eba5fb1657cdb15826ee47d366dccbaabfbb1fa2`

## Warum keine stille Source-Synchronisierung

Der historische GitHub-Source-Ordner ist nicht automatisch byte-identisch zur geprüften Release-Kandidatenquelle.
Eine teilweise Synchronisierung würde Scheinsicherheit erzeugen.

KISS:
Bis zu einer späteren **exakten byte-identischen Source-Materialisierung** ist ausschließlich die hier hashgebundene 0.8.6-ZIP die technische Release-Kandidaten-Wahrheit.

## Folgearbeit

Der technische Gesamtaudit wird auf Basis der **exakten 0.8.6-Fresh-ZIP** fortgesetzt.

Vor jeder späteren Codeänderung:
1. exakt die aktuelle gebundene ZIP materialisieren;
2. SHA prüfen;
3. daraus isolierten Arbeitsbaum erzeugen;
4. nur den ersten real belegten Gap ändern;
5. wieder komplette positive/negative/Gesamtworkflow-/Fresh-ZIP-Prüfung.

Vor jeder Plugin-Übergabe an den Nutzer muss die **exakt auszugebende ZIP** selbst positiv, negativ/Mutation und gegen den vollständigen aktuellen Produktvergleichsworkflow geprüft sein.

Kein Merge.
Kein Publish.
