# BAUCONTAINER – BAUPROTOKOLL

STAND: 2026-09-05

## Zweck

Chronologisches Arbeitsprotokoll für den Campus selbst.

Die ausführliche dauerhafte Begründung liegt im `AENDERUNGSREGISTER.md`.

## Pflichtregel

Jeder Chat, der Architektur verändert, protokolliert:
- konkreten Bedarf;
- kleinste Änderung;
- betroffene Architekturakten;
- ARCH-/BAU-Fehler-Bezug;
- Prüfstand.

## Bisherige Bauereignisse

### 2026-09-05 – Campus-Prototyp
Campus → Projektgebäude → Büro → Hobbyraum.
BEZUG: ARCH-001 bis ARCH-006.
PR: #134.

### 2026-09-05 – Organischer Ausbau
BILD, allgemeingültige Bausteine, Modulregister, Masterdateien-Regel.
BEZUG: ARCH-008 bis ARCH-014.

### 2026-09-05 – Zielverträge und Archiv
Zielvertragsraum + Campus-Archiv-Eingang.
BEZUG: ARCH-015 bis ARCH-017.

### 2026-09-05 – Architektur-Selbstpflege
Architektur-Sonderrecht, Bauprotokoll, Architektur-Fehlerkiste, Hausmeister.
BEZUG: ARCH-018 bis ARCH-020.

### 2026-09-05 – Verwaltungsrollen hart getrennt + 1-Klick-Eingänge
BEDARF:
Pförtner/Hausmeister dürfen Inhalte nicht anfassen. Neue Chats müssen an jeder Ebene sofort verstehen, wo sie sind und was gilt.

ERGEBNIS:
- Pförtner = READ/ROUTE ONLY;
- Hausmeister = ORDNEN/VERSCHIEBEN OHNE INHALTSÄNDERUNG;
- `EINGANGSSTANDARD.md`;
- Campus-, Projekt-, Büro- und Paul-Eingänge auf 1-KLICK-ÜBERSICHT vereinheitlicht;
- neue Projektvorlage erzwingt denselben Standard.

BEZUG:
ARCH-021, ARCH-022.


### 2026-09-05 – Entwicklungsprotokoll ergänzt

BEDARF:
Auch der konzeptionelle Austausch und verworfene/offene Architekturgedanken sollen nicht im Chat verloren gehen.

ERGEBNIS:
`ENTWICKLUNGSPROTOKOLL.md` ergänzt.

TRENNUNG:
- Entwicklungsgespräch → ENTWICKLUNGSPROTOKOLL
- tatsächlich gebaut → BAUPROTOKOLL
- dauerhaft gültig + WHY → AENDERUNGSREGISTER

BEZUG:
ARCH-023.


### 2026-09-05 – WordPress-Register

BEDARF:
Zentrale Antwort auf „Welche WordPress-Plugins haben wir bereits?“, ohne ein neues WordPress-Büro oder eine zweite Modulwahrheit zu bauen.

KRITISCHE ENTSCHEIDUNG:
Kein WordPress-Gebäude/Büro. Ein einziges campusweites Technologie-Register reicht aktuell.

ERGEBNIS:
`WORDPRESS_REGISTER.md` mit nachweisbar erhaltenen Plugin-/Installer-Artefakten angelegt.

GRENZE:
Modulklasse bleibt im MODULREGISTER; LIVE-/Release-Status bleibt an der Fach-/Technikquelle.

BEZUG:
ARCH-024.


### 2026-09-05 – Kategoriemodul vollständig eingeordnet + Archiv-Ampel

BEDARF:
Aktuellen allgemeingültigen Kategorieplugin-Bestand vollständig zuordnen und klären, wann lokale Originale entbehrlich werden.

ERGEBNIS:
- MOD-001 auf Master R10/R9 / Plugin V1.8.0 aktualisiert;
- WordPress-Pluginstatus belegt;
- R2/R3 historisch, R10 Hauptakte;
- Pferde-Atelier-Kategoriereparatur separat gehalten;
- persistente Library-Archivkopien erzeugt;
- Archiv-Ampel ROT/GELB/GRÜN eingeführt.

BEZUG:
ARCH-025.


### 2026-09-05 – Design allgemein + Pferde zusammengeführt

BEDARF:
Zwei allgemeine Design-Dateien und zwei Pferde-Dateien mit aktuellem GitHub-System zusammenführen.

ERGEBNIS:
- MOD-003 Universal Design 2.2.40/V104 angelegt;
- Universal-Master 298/298 geprüft;
- Pferde-Master 1.50.469 792/792 geprüft;
- Pferde-Dubletten erkannt;
- Roharchive getrennt persistiert;
- GitHub main 1.50.421 als älteren Main-Stand erkannt;
- spätere Design-Fachbranches bis 1.50.472 geprüft;
- 1.50.472/V104 als aktuellen Pferde-LIVE-Stand gebunden;
- Universal 2.2.40/V104 durch spätere GitHub-Historie als unverändert aktuell bestätigt;
- enthaltene HivePress-Anzeigensuche als MOD-004 UNGEKLÄRT separat erfasst.

BEZUG:
ARCH-026.


### 2026-09-05 – Campus-Eingänge + Paul TEXT/SEO + Tresorstatus geschlossen

BEDARF:
Alltagssprache soll als Campus-Routing funktionieren; Archiv/Zielverträge/Baucontainer/Tresor brauchen vollständige 1-Klick-Eingänge; Paul muss TEXT/SEO ohne Kontextverlust finden.

ERGEBNIS:
- Campus-`START_HERE.md`;
- natürliche Sprache als Routingauftrag gebunden;
- Archiv/Zielverträge/Baucontainer/Tresor mit 1-Klick-Eingang;
- sechs aktuelle TEXT-/SEO-Originalakten wortgleich unter `TEXT/QUELLEN_AKTUELL/`;
- aktiver TEXT-Zielvertrag im zentralen Register;
- Paul-Direkteinstieg `PAUL/TEXT_SEO/START_HERE.md`;
- Tresorstatus explizit FAIL statt erfundenem PASS.

BEZUG:
ARCH-027 bis ARCH-030; BAU-006 bis BAU-009.


### 2026-09-05 – Externer Tresor-Git-Mirror V2 erzeugt und Restore-getestet

BEDARF:
Der Tresor durfte nicht nur Konzept sein; Git-Historie/Branches/Tags und GitHub-Metadaten mussten außerhalb des aktiven Repositorys gesichert werden.

ERGEBNIS:
- isolierter Tresor-Branch;
- vollständiger Git-Bundle-Mirror;
- 261 Branches / 1 Tag;
- vollständige paginierte GitHub-Metadaten: 136 Issues, 127 PRs, 1 Release, 1 Ruleset, 59 Workflows;
- Ruleset-Detail separat gesichert;
- Restore-Test + git fsck PASS;
- V2-Artefakt extern in ChatGPT Library gesichert.

STATUS:
Kein vollständiger TRESOR_PASS.
Nächster Blocker: nicht exportierbare Recovery-Abhängigkeiten noch nicht verifiziert.

BEZUG:
ARCH-031.


### 2026-09-05 – Kritische Bauabnahme: erste Mängel direkt geschlossen

BEFUNDE:
- TEXT-/HIVEPRESS-Eingang führte nicht vollständig über CURRENT_STATE → HOBBYRAUM;
- TEXT-Eingang/Hobbyraum waren an den alten Sortierchat gebunden und kollidierten mit Pauls Fachauftrag;
- BILD-Hobbyraum war nach abgeschlossenem Abgleich noch als AKTIV markiert;
- Pferde-Gebäudeeingang enthielt veralteten Parallelchat-Hinweis;
- Paul-TEXT/SEO nutzte fünf abgekürzte `.../`-Pfade;
- zentrale Tresor-/Bild-Metadaten enthielten veraltete Statushinweise;
- Hobbyraum-Kennwort/Zustände waren nicht zentral definiert.

KISS-FIX:
Nur Navigations-/Status-/Architekturmetadaten an bestehenden Adressen korrigiert.
Keine Fachdatei und keine Fachlogik verändert.

ADRESSGARANTIE:
Alle bereits verteilten Campus-/Büro-/Paul-Einstiege bleiben unverändert erreichbar.

BEZUG:
ARCH-032 bis ARCH-034; BAU-010 bis BAU-013.


### 2026-09-05 – Bauabnahme: Büro-Leitungen + Hobbyraum-Direkteinstieg

BEFUND:
Direkter Büro-/Hobbyraumeinstieg war weniger vollständig als der Weg über den Hauptpförtner.

KISS-FIX:
- alle sechs Pferde-Büros mit sichtbarer Arbeitsfreigabe zu Handlungs-/Fehler-/Änderungs-/Zielregistern;
- alle sechs Hobbyräume mit 1-Klick-Eingang;
- Gebäudebüroplan auf echte START_HERE-Pfade präzisiert.

BEZUG:
ARCH-035/036; BAU-014/015.


### 2026-09-05 – Bauabnahme: Flur/ungeklärter Bestand/Tresor-Reihenfolge

BEFUNDE:
- Projektflur ohne START_HERE;
- Affiliate-Bestandsraum unter allgemeingültiger Ablage ohne sichtbare UNGEKLÄRT-Warnung;
- Tresorstatus übersprang die fehlende unabhängige Roharchiv-Redundanz.

KISS-FIX:
- Projektflur-Eingang ergänzt;
- Affiliate-Bestandsraum selbsterklärend gemacht, ohne Modulfreigabe;
- MOD-004-Registerpflichtfelder vervollständigt, ohne eigenen Modulraum vor Audit;
- Tresor auf ersten realen Blocker zurückgesetzt.

BEZUG:
ARCH-037 bis ARCH-039; BAU-016 bis BAU-018.


### 2026-09-05 – Formale Bauabnahme nach Reparaturen

POSITIV:
- 22/22 PROJECT_MEMORY-Verzeichnisse besitzen START_HERE;
- 22/22 START_HERE-Eingänge erfüllen 1-Klick-Standard;
- 6/6 Pferde-Büros besitzen START_HERE + CURRENT_STATE + genau einen HOBBYRAUM;
- 6/6 Hobbyräume besitzen 1-Klick-Übersicht und gültigen Status;
- 6/6 Büros führen bei echter Arbeit über Handlungs-/Fehler-/Änderungs-/Zielregister;
- Pförtner READ/ROUTE ONLY;
- Hausmeister reine Verwaltung;
- Paul-Pfade vollständig, keine Ellipsen;
- bestehende Adressen unverändert;
- Campus-Hardlocks auf den vorausgehenden Abnahmeständen PASS.

NEGATIV / BEWUSST OFFEN:
- BAU-003: Campus-Prototyp noch im öffentlichen Pferde-Atelier-Repo/Branch;
- TRESOR: kein vollständiger PASS, erster Blocker fehlende unabhängige Roharchiv-Redundanz;
- danach weiterhin Recovery-Abhängigkeiten/Secrets zu prüfen;
- Archivbestände mit ROT/GELB bleiben lokal nicht entbehrlich.

GESAMT:
Architektur/Navigations-/Rollenabnahme PASS.
Vollständiger Sicherheits-/Katastrophen-PASS BLOCKED.


### 2026-09-05 – Bauabnahme: Neubauvorlage gegen aktuellen Standard gehärtet

BEFUND:
Die bestehende Projektvorlage kannte den ursprünglichen 1-Klick-Standard, aber noch nicht alle späteren Regeln aus ARCH-032 bis ARCH-040.

KISS-FIX:
Vorlage ergänzt um:
- START_HERE für jedes neue Verzeichnis;
- stabile Adressen;
- zentrale Büro-Leitungen;
- Hobbyraum-Standard;
- Positiv-/Negativ-Abnahme.

BEZUG:
ARCH-041 / BAU-020.


### 2026-09-05 – Fremdnutzer-Test: eine Wahrheit besser ausgeschildert

AUSLÖSER:
Ein neuer Chat fand den Campus, musste aber aktuellen Stand, aktuelle Arbeit, Fehler und Ziel noch unnötig zusammensetzen.

KISS-FIX:
- alle sechs Bürotüren mit einheitlichem Quellenwegweiser;
- CURRENT_STATE als einzige Büro-Standzusammenfassung markiert;
- Hobbyraum als einzige aktuelle Arbeitsbindung markiert;
- Fehlerregister auf reinen Index reduziert;
- Archiv ausdrücklich nie CURRENT;
- Paul führt keine zweite Fach-/Statuswahrheit;
- Neubau- und Eingangsstandard entsprechend nachgezogen.

NICHT GEBAUT:
kein neues Büro, kein zusätzlicher Statusspeicher, keine zweite Fehler-/Zielwahrheit.

BEZUG:
ARCH-042/043; BAU-021/022.


### 2026-09-05 – Paul-Isolation gegen Fremdchat-Test wiederhergestellt

AUSLÖSER:
Ein normaler Nachbarchat wollte TEXT/SEO weiterbearbeiten und wurde durch den TEXT-Hobbyraum direkt zu Paul geroutet.

BEFUND:
Das widersprach dem bereits bestehenden Grundkonzept ARCH-004:
Paul sollte isoliert analysieren/testen und seine Lösung an das Fachbüro zurückgeben. Die spätere Ausschilderung hatte Paul fälschlich zum normalen nächsten Arbeitsschritt gemacht.

KISS-FIX:
- normaler TEXT-Arbeitschat bleibt im TEXT-Hobbyraum;
- Paul-Eingänge auf WORKER_ONLY gesetzt;
- Paul darf alle Campus-/Büroakten lesen, aber `protocol/PROJECT_MEMORY/**` nicht verändern;
- technische Writes nur auf eigenem Paul-Branch und nur im ausdrücklich gebundenen Schreibbereich;
- ohne Schreibbereich READ ONLY;
- kein Merge/keine Integration durch Paul;
- derselbe technische Schreibbereich nie gleichzeitig durch Paul und Arbeitschat;
- Regel in Handlungsverzeichnis, Eingangsstandard und Neubauvorlage verankert.

LEITSATZ:
**Single Writer, Multi Reader. Keine Echtzeit-Synchronisation zwischen Chats als Voraussetzung.**

BEZUG:
ARCH-004, ARCH-044, ARCH-045; BAU-023.


### 2026-09-05 – Paul-Frischeprüfung gegen Branch-Drift

BEDARF:
Auch bei sauberer Schreibtrennung kann Pauls eigener Branch eine ältere Kopie von CURRENT_STATE/HOBBYRAUM enthalten.

KISS-FIX:
- Paul-Branch ausdrücklich nur als technische Werkbank definiert;
- offizieller Campus-Ref ist Quelle für Büro-/Statuswahrheit;
- Frischeprüfung vor Start und vor Rückgabe;
- relevanter Drift führt zu STALE_ASSIGNMENT statt Weiterarbeit auf altem Stand.

BEZUG:
ARCH-046.


### 2026-09-05 – Technische Paul-Sperre vorbereitet, Aktivierung fail-closed

BEDARF:
Die bereits wiederhergestellte Paul-Regel sollte nicht nur dokumentiert, sondern technisch erzwungen werden:
Paul darf `protocol/PROJECT_MEMORY/**` lesen, aber niemals über seinen `paul/*`-Branch verändern/integrationsfähig machen.

KISS-IMPLEMENTIERUNG:
Security-Branch:
`security/paul-project-memory-hardlock-20260905`

Commit:
`68aaced0cb8629577c3b82f02da298b4b74fff93`

Draft-PR:
#137 – `SECURITY: block Paul writes to PROJECT_MEMORY`

Geplante trusted-base-Regel:
- PR-Head `paul/*`;
- Diff berührt `protocol/PROJECT_MEMORY/**`;
- Ergebnis: `PAUL_PROJECT_MEMORY_WRITE_BLOCKED`.

ABDECKUNG:
Damit sind ohne Einzellisten automatisch geschützt:
Campus, Projektgebäude, alle Büros, CURRENT_STATE, HOBBYRAUM, Paul-Akten, Fehler-/Ziel-/Änderungsregister, Archiv, Tresor und Baucontainer.

PRÜFUNG:
- normaler `hardlock` auf Security-Kandidat: PASS;
- bestehender `hardlock-base`: erwartetes FAIL `IMMUTABLE_SECURITY_PATH_CHANGE_BLOCKED`, weil Workflow-Security selbst geändert wird;
- Test-PRs #138/#139 wurden angelegt und wieder geschlossen;
- Befund: `pull_request_target` verwendet weiterhin die Default-Branch-Version des vertrauenswürdigen Workflows; Kandidatenregel kann daher vor Aktivierung auf main nicht live über diesen Mechanismus getestet werden.

STATUS:
**BLOCKED – ADMIN-WARTUNGSAKTIVIERUNG ERFORDERLICH.**
Kein technischer PASS behauptet.

NACH AKTIVIERUNG ZWINGEND:
1. realer Negativtest: `paul/*` + `protocol/PROJECT_MEMORY/**` → `PAUL_PROJECT_MEMORY_WRITE_BLOCKED`;
2. realer Positivtest: `paul/*` ohne PROJECT_MEMORY-Write → diese Sperre darf nicht auslösen;
3. Ruleset sofort wieder im normalen Hardlock-Zustand;
4. erst danach TECHNISCHE PAUL-SPERRE = PASS.

BEZUG:
ARCH-044 bis ARCH-047; BAU-024.
