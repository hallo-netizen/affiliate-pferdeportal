# PRODUKTVERGLEICH – ARBEITSPROTOKOLL 2026-09-07

ROLLE: chronologischer Ausführungs-/Testbeleg. Nicht CURRENT, nicht Zielvertrag, nicht Fehlerregister.

## Ausgeführt

- eigenständigen Universal Product Knowledge V1-Prototyp mit vier DB-Tabellen gebaut und real in WordPress/MySQL getestet;
- Universal Product Comparison V1 gebaut;
- Produkt-/Variantenvergleichsregeln und Fail-closed-Sperren implementiert;
- reales Dossier `PV-REG-001` gebunden;
- Zero-Freedom-Writer zu deterministischem Renderer verschärft;
- deklaratives, versioniertes und SHA-gebundenes Rulebook eingeführt;
- unabhängigen Validator und Single-Door-Produktionsweg gebaut;
- Golden Output für `PV-REG-001` gebunden;
- 100/100 byte-identische Renderer-Wiederholungen geprüft;
- WordPress-DRAFT-Materialisierung gebaut und Readback geprüft;
- Affiliate-Schnittstelle auf GTIN/EAN/echte MPN begrenzt;
- SEO auf read-only Signale begrenzt;
- Vergleichsarchiv, Link-Manifest, Link-Finalisierung und neutrale SVG-Grafik gebaut;
- 20/20 byte-identische Grafiken geprüft;
- finalen Draft mit Link-/Grafikbindung und Endhash geprüft;
- echte ZIP-Installation/Aktivierung geprüft;
- reale Pferde-Atelier-Kategorie `Vergleich Regendecken` auf Term-ID 11 / Parent 0 gebunden;
- gebundenen Erstimport und `PV-REG-001`-Admin-Drafttest gebaut;
- Hauptnavigation von `Werkzeuge` auf Top-Level `Produktvergleich` verschoben.

## Wichtige Fehler/Befunde

- falsche Taxonomie-Parent-Annahme entdeckt und in 0.2.1 korrigiert;
- Erst-Draft übersprang zunächst die Draft-Materialisierung und blockierte mit `UPC_LINK_FINALIZER_SOURCE_NOT_UNIQUE`; Reihenfolge korrigiert;
- 0.2.3-Menütest als falscher Positivtest erkannt, nachdem der Nutzer real keinen Menüpunkt sah;
- Testmethode daraufhin auf echten WordPress-HTTP-Admin-Lifecycle umgestellt.

Details:
`FEHLERQUELLEN.md`.

## Relevante PASS-Belege

- Product Knowledge real WordPress/MySQL: Run `34108014923` PASS.
- Comparison Core real WordPress/MySQL: Run `34108369648` PASS.
- Realdossier `PV-REG-001`: Run `34109035504` PASS.
- Zero-Freedom Writer: Run `34111825722` PASS.
- WordPress-Draft: Run `34112287717` PASS.
- Link-Finalisierung nach Testzustandskorrektur: PASS.
- Kategoriebindung 0.2.1: Run `34141063395` PASS.
- Clean 0.2.2 Erst-Draft: Run `34144140088` PASS.
- 0.2.3 Menütest: Run `34153930934` technisch PASS, später als methodisch unzureichend verworfen.
- 0.2.4 echter WP-Admin-Lifecycle: Run `34154550626` PASS.

## Nicht ausgeführt / weiterhin offen

- 0.2.4 wurde auf der echten Nutzer-WordPress-Seite noch nicht bestätigt;
- damit kein LIVE-PASS für den Hauptmenüpunkt;
- der reale `PV-REG-001`-Draft auf der Nutzerseite wurde mit 0.2.4 noch nicht erzeugt und visuell/fachlich geprüft;
- kein Publish ausgeführt;
- kein Merge nach main ausgeführt.

## Aktueller technischer Codebeleg

Plugin-Code 0.2.4:
- Menü-Hook-Fix: Commit `3295653c19aed3a4af47aad73dc2226e0d7a9b78`;
- Versions-/Bootstrap-Fix: Commit `47666ef1a0f1dbe36c5c8744382b52e178d734e9`.

Realtest-Head mit temporärem Workflow:
`4fe4d9a64a20be776a97605f9213033760eb612f`.
Der temporäre Workflow wurde danach entfernt.

Bereinigter Branch vor dieser Abschluss-Nachholprüfung:
`d9460e19f30f9bbaff5e9d5c63e134f8d9a38333`;
Immutable Base Hardlock Run `34154765043` PASS.


## Abschluss-/Nachholprüfung

Frisch aus autoritativen Quellen geprüft und nachgeholt:

- `FEHLERQUELLEN.md` als einzige detaillierte Produktvergleichs-Fehlerquelle angelegt;
- `FEHLERREGISTER.md` nur mit einem Zeiger auf diese Quelle ergänzt;
- `ZIELVERTRAG_V1.md` als aktiver Produktvergleichs-Zielvertrag angelegt;
- `ZIELVERTRAEGE/REGISTER.md` nur mit einem Zeiger ergänzt;
- alte Bürotür-Aussage `Produktvergleich -> TEXT-Produktion` entfernt;
- gleiche alte Route aus `HANDLUNGSVERZEICHNIS.md`, `HAUPTPFOERTNER.md` und Pferde-Atelier-`START_HERE.md` entfernt;
- `CURRENT_STATE.md` auf `0.2.4 technisch PASS / Nutzer-Live-Verify OFFEN` bereinigt;
- `HOBBYRAUM.md` auf genau einen aktuellen 0.2.4-Live-Verifikationsweg gekürzt;
- veraltete MOD-006/MOD-007-Stände im Modulregister auf technisch belegten V1-Prototyp aktualisiert;
- Universal Product Knowledge und Universal Product Comparison im WordPress-Register als Artefakte aufgenommen;
- dynamischen Projekt-Livestatus aus WordPress-/Modulregister bewusst **nicht** dupliziert;
- allgemeine Regel `Funktions-PASS ≠ Lifecycle-PASS` in den Hobbyraum-Standard übernommen und im Bauprotokoll dokumentiert;
- PR #142 auf aktuellen Produktwissen+Produktvergleich-Scope umbenannt; PR-Text verweist für dynamischen Stand ausschließlich auf CURRENT/HOBBYRAUM.

Negativ geprüft:
- genau eine Produktvergleichs-`CURRENT_STATE.md`;
- genau eine Produktvergleichs-Fehlerhauptquelle;
- genau ein Produktvergleichs-Zielvertrag;
- keine temporären Produktvergleichs-Testworkflows im Branch;
- kein aktiver Paul-Auftrag;
- kein Auto-Publish;
- kein Merge nach main.

Weiter offen:
0.2.4 muss auf der echten Nutzer-WordPress-Seite installiert und dort Hauptmenü + erster Draft bestätigt werden.
