# GLOSSAR – HOBBYRAUM

STAND: 2026-09-12
STATUS: AKTIV / FRONTEND-PROTOTYP MUSS KORRIGIERT WERDEN

## 1-KLICK-ÜBERSICHT

**WAS IST DAS?**  
Der einzige aktuelle Arbeitsraum des Büros GLOSSAR.

**HIER BIST DU RICHTIG, WENN …**  
die Pferde-Atelier-Anwendung des allgemeinen Glossar-Cores vorbereitet oder geprüft wird.

**DU DARFST …**  
die Pferde-Konfiguration definieren, Fachquellen aus der Wissensdatenbank binden und den allgemeinen Glossar-Core isoliert gegen das Pferde-Atelier testen.

**DU DARFST NICHT …**  
`main` verändern, eine zweite Glossar-Faktendatenbank bauen, normale Beiträge/Seiten pro Begriff erzwingen, Pferde-Fachlogik in den allgemeinen Core schreiben, den verworfenen HTML-Anker-/Alles-auf-einer-Seite-Ansatz weiterverwenden oder vor echtem WordPress-PASS ein Release behaupten.

**ALS NÄCHSTES …**  
den Frontend-Prototyp auf echte Glossar-Kategorieseiten und die bestehende Pferde-Atelier-Designlogik umbauen und danach lokal erneut positiv/negativ prüfen.

## AKTUELLER AUFTRAG

Pferde Atelier als erste reale Anwendung von `MOD-008 – Universal Glossar Engine` auf das korrigierte öffentliche Seitenmodell bringen.

Bestätigter Live-Ausgangspunkt:
- Seite `Glossar` ist angelegt;
- Seite ist verlinkt;
- Nutzer muss aktuell nichts Weiteres manuell anlegen.

Verbindliches Frontendmodell:
- Startseite = begrenzter Einstieg, nicht Gesamtverzeichnis;
- passendes Foto/Hero oben, optisch am Pferde-Atelier orientiert;
- waagerechte Glossar-Navigation auf jeder Glossarseite;
- jede Glossar-Kategorie = eigene öffentliche Seite/URL;
- keine HTML-Anker als Kategorienavigation;
- Kategorien nicht doppelt als große Blöcke auf der Startseite;
- Startseite zeigt stattdessen eine kleine wechselnde Auswahl von Glossarbegriffen analog zur Beitragsvorschau;
- einzelne Begriffe behalten eigene Zieladressen;
- kein Pflichtbild pro Begriff.

## ARBEITSORT

Campus-Basis:
`hobbyroom/project-memory-campus-v1-20260905`

Isolierter Glossar-Hobbyraum-Branch:
`hobbyroom/glossar-office-20260912-v2`

`main` bleibt unangetastet.

## ALLGEMEINER CORE

Autorität:
`../../ALLGEMEINGUELTIGE_BAUSTEINE/GLOSSAR/START_HERE.md`
→ `CURRENT_STATE.md`
→ `HOBBYRAUM.md`

Bisheriger Quellstand:
`../../ALLGEMEINGUELTIGE_BAUSTEINE/GLOSSAR/prototype/0.1.0/universal-glossary-engine/`

Wichtig:
Der bisherige Frontendteil von 0.1.0 ist nicht mehr freigabefähig, weil er Kategorien per HTML-Anker innerhalb der Hauptseite ansteuert und alle veröffentlichten Begriffe gleichzeitig lädt.

## PFERDE-KONFIGURATION

- vorhandene Seite `Glossar` als Hauptseite;
- echte Glossar-Kategorie-URLs unterhalb des Glossars;
- gemeinsame waagerechte Navigation zentral erzeugen;
- URL-Basis `glossar`, Realtest muss Permalink-Kollisionen ausschließen;
- Kategorien nicht im Core fest verdrahten;
- SEO-Schema konfigurierbar, je Begriff überschreibbar;
- Fachimport später aus `../WISSENSDATENBANK/AKTENSCHRAENKE/GLOSSAR/`;
- Import immer als Entwurf, Veröffentlichung manuell.

## DESIGNBINDUNG

Kein eigenes Glossar-Sonderdesign erfinden.

Autoritativer aktueller Pferde-Designstand laut `../DESIGN/CURRENT_STATE.md`:
`Pferde Atelier Design 1.50.472 / Contract V104 + DESIGN-ORDER-SWAP-002`.

Vor Frontend-Code müssen aus dem tatsächlichen Designplugin die relevanten Muster für Hero/Bild, Typografie, Abstände, Karten-/Beitragsvorschau und responsive Verhalten übernommen werden. Nur Farben und Radiuswerte reichen nicht.

## NEXT ACTION – FRONTEND VOR REALTEST KORRIGIEREN

1. aktuellen Frontend-Prototyp isoliert umbauen;
2. `numberposts = -1` auf der Hauptseite entfernen;
3. HTML-Anker-Navigation der Kategorien vollständig entfernen;
4. echte Kategorie-Routen/-seiten erzeugen;
5. dieselbe waagerechte Glossar-Navigation auf Start-, Kategorie- und Begriffsseiten erzeugen;
6. Startseite nur mit begrenzter wechselnder Begriffsauswahl aufbauen;
7. Hero-/Foto-Bereich und Teaserlogik am realen Pferde-Designplugin ausrichten;
8. große Kategorien mit Pagination statt Vollausgabe behandeln;
9. lokal Positiv/Negativ einschließlich großer Begriffsmenge prüfen;
10. erst danach echter WordPress-Smoke-Test.

## PARALLELENTWICKLUNG

Aktuell NICHT erforderlich.

## HARTE REGEL

**Noch kein Plugin an WordPress ausgeben, solange das korrigierte Frontend nicht lokal PASS und anschließend im echten WordPress-Smoke-Test geprüft ist.**

## VERWEISE

- Bürostand: `CURRENT_STATE.md`
- Bürotür: `START_HERE.md`
- Seitenkonzept: `SEITENKONZEPT_V1.md`
- Allgemeiner Core: `../../ALLGEMEINGUELTIGE_BAUSTEINE/GLOSSAR/START_HERE.md`
- Fachdatenbank: `../WISSENSDATENBANK/AKTENSCHRAENKE/GLOSSAR/START_HERE.md`
- DESIGN: `../DESIGN/START_HERE.md`
- TEXT/SEO: `../TEXT/START_HERE.md`
- Fehler: `protocol/PROJECT_MEMORY/FEHLERREGISTER.md`
- Warum: `protocol/PROJECT_MEMORY/AENDERUNGSREGISTER.md`
- Ziel: `protocol/PROJECT_MEMORY/ZIELVERTRAEGE/REGISTER.md`