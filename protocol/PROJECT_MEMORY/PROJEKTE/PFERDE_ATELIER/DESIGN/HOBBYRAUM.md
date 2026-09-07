# DESIGN – HOBBYRAUM

STAND: 2026-09-07
STATUS: FREI / SCRIPT-ONLY-STANDARD

## HARTE OBERREGEL

**Im DESIGN-Hobbyraum werden Miniänderungen nicht mehr manuell gebaut.**

Bei Elementtausch, Verschiebung oder vergleichbaren lokalen Änderungen ist ausschließlich dieser Runner zulässig:

`MINIMAL_PATCH_RUNNER.py`

Aktueller Auftrag:

`MINIMAL_PATCH_JOB_CURRENT.json`

Letzter echter Prüfbeleg:

`MINIMAL_PATCH_LAST_RECEIPT.json`

## WAS DER RUNNER ERZWINGT

Der Runner darf in V1 ausschließlich:

**zwei direkt aufeinanderfolgende vollständige Codebereiche in genau einer Datei vertauschen.**

Er darf ausdrücklich NICHT:
- Artikel zerlegen;
- Markup neu bauen;
- Texte umschreiben;
- CSS ändern;
- weitere Dateien ändern;
- zusätzliche Logik ergänzen;
- selbst eine neue Pluginversion erzeugen;
- einen anderen Ausgangsstand verwenden.

## FAIL-CLOSED

Vor jedem Kandidaten erzwingt das Script:

1. exakter Baseline-SHA;
2. ZIP-Integrität;
3. identische Archivstruktur;
4. genau eine geänderte Paketdatei;
5. exakt nur den definierten Tausch;
6. beide verschobenen Bereiche byte-identisch;
7. beide Bereiche exakt einmal vorhanden;
8. Rücktausch ergibt byte-identisch den Vorgänger.

Danach laufen automatisch Negativtests:

- unveränderte/falsche Reihenfolge → BLOCKED;
- Bereich dupliziert → BLOCKED;
- Bereich verändert → BLOCKED;
- irgendeine andere Datei verändert → BLOCKED.

**Ein Kandidat darf nur bei Gesamt-PASS ausgegeben werden.**

## KEINE PLUGIN-SERIE MEHR

Im Hobbyraum wird immer nur eine Datei erzeugt:

`DESIGN_HOBBYRAUM_CANDIDATE.zip`

Fehlversuch:
Kandidat verwerfen/überschreiben.

**Keine neue Versionsnummer pro Versuch.**

Erst nach echtem Nutzer-LIVE-PASS darf aus dem Kandidaten einmalig ein neuer Release gebaut werden.

## AKTUELLER AUFTRAG

Exakte Basis:
V1.50.472 / Contract V104

SHA-256:
`ae59699c2de750e5ebda14096109e60ddfdac55f32e9ffe848305e4dc2e035b9`

Erlaubte Transformation:
nur

**Affiliate-PRODUKTE / Produktvorschläge (pa266-products) ↔ Beitragsvorschau (pa297-popular)**

Ziel:
**Produktvorschläge stehen direkt über der Beitragsvorschau.**

Der Affiliate-Banner bleibt exakt an seiner bisherigen V1.50.472-Position.
Artikel, Verweise und jeder andere Block bleiben exakt wie V1.50.472.

Kein anderer Block darf bewegt werden.

## LETZTER SCRIPT-LAUF

Aktueller Job **DESIGN-ORDER-SWAP-002** gegen exakte V1.50.472-Basis: **PASS**

Ziel eindeutig:
**Affiliate-Produkte / Produktvorschläge stehen über der Beitragsvorschau.**

Ergebnis:
- Affiliate-Banner bleibt exakt an seiner V1.50.472-Position: PASS;
- Affiliate-Produkte vor Beitragsvorschau: PASS;
- Artikel-/Verweisstruktur unverändert: PASS;
- genau eine Paketdatei verändert: PASS;
- exakter Zwei-Bereich-Tausch: PASS;
- Byteidentität/Reversibilität: PASS;
- vier Negativtests BLOCKED/PASS;
- Kandidaten-SHA: `11b664a10d4ef0ec82f0011436eb92715d9efd14474893fecddcb64e91e6fe0b`.

Der Nutzer hat den Kandidaten am 2026-09-07 real geprüft und mit **PASS** bestätigt. LIVE-Beleg: `LIVE_PASS_DESIGN_ORDER_SWAP_002.md`.

## ABSCHLUSS

Aktueller Auftrag DESIGN-ORDER-SWAP-002: **CLOSED / LIVE PASS**.

Der Hobbyraum ist wieder FREI. Der SCRIPT-ONLY-Standard bleibt für künftige Miniänderungen verbindlich.

## VERBINDLICHER ABLAUF FÜR JEDEN WEITEREN CHAT

1. `CURRENT_STATE.md` lesen.
2. diese `HOBBYRAUM.md` lesen.
3. `MINIMAL_PATCH_JOB_CURRENT.json` lesen.
4. Runner-Selbsttest ausführen.
5. exakte Baseline anhand SHA binden.
6. ausschließlich `MINIMAL_PATCH_RUNNER.py build ...` ausführen.
7. nur bei Gesamt-PASS den einen `DESIGN_HOBBYRAUM_CANDIDATE.zip` verwenden.
8. bei FAIL: STOPP. Keine manuelle Reparatur und kein Ersatzweg.

## HARTE GRENZE

V1.50.473, V1.50.474, V1.50.475 und V1.50.476 sind keine Arbeitsbasis für diesen Auftrag.

Es gibt keinen manuellen Nebenweg.

## VERWEISE

- Bürostand: `CURRENT_STATE.md`
- Fehler: `protocol/PROJECT_MEMORY/FEHLERREGISTER.md`
- Warum: `protocol/PROJECT_MEMORY/AENDERUNGSREGISTER.md`
