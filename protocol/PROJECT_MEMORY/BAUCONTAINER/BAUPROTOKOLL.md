# BAUCONTAINER – BAUPROTOKOLL

STAND: 2026-09-07

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


### 2026-09-05 – Startprompt-Protokollpflicht campusweit verankert

AUSLÖSER:
Der Nutzer verlangt eine dauerhafte Gegenmaßnahme dagegen, dass Arbeitschats im langen Verlauf Fehler-, Änderungs-, WHY-, Status- oder NEXT-ACTION-Dokumentation vergessen.

KISS-FIX:
- Campus-`START_HERE.md` verweist vor jedem Abschluss auf die Protokollpflicht;
- `EINGANGSSTANDARD.md` bindet dieselbe Abschlussprüfung für jede Ebene und jeden Raum, einschließlich Archiv/Tresor/Baucontainer;
- Regel lautet ausdrücklich: nur tatsächlich betroffene autoritative Stellen ändern, nichts künstlich protokollieren;
- technische Hardlock-/BLOCKED-Ergebnisse schlagen jede Chatbehauptung.

EXTERNER STARTPROMPT:
Der Nutzer-Startprompt wurde inhaltlich um Single-Writer/Paul-Grenze, Frischeprüfung und technischen Check-Vorrang ergänzt.

BEZUG:
ARCH-048.


### 2026-09-05 – Aktivierungsversuch Security-PR #137

AKTION:
PR #137 aus Draft genommen und normaler Merge gegen den aktiven Ruleset versucht.

ERGEBNIS:
GitHub hat den Merge serverseitig abgewiesen.
`hardlock = PASS`.
`hardlock-base = FAIL` mit dem bestehenden Selbstschutz für Workflow-Security (`IMMUTABLE_SECURITY_PATH_CHANGE_BLOCKED`).

BEWERTUNG:
Kein Bypass vorhanden; genau die beabsichtigte Schutzwirkung des aktuellen Systems.

KONSEQUENZ:
Die Paul-Sperre ist implementiert und reviewbereit, aber **noch nicht aktiv auf main**.
Aktivierung benötigt einmalig den bewussten Repository-Admin-Wartungsweg für eine Änderung an der immutable Security-Schicht. Danach sofort Positiv-/Negativtest und vollständige Wiederherstellung des normalen Rulesets.

KEIN FALSCHER PASS:
Bis zur Aktivierung + Realtest bleibt BAU-024 BLOCKED.


### 2026-09-05 – Nachholprüfung fand eigenen HOBBYRAUM-Statusfehler

AUSLÖSER:
Der Nutzer gab die harte Abschluss-/Nachholprüfung vor: aktuellen Campus/Fachstand frisch lesen, nicht aus Erinnerung antworten, HOBBYRAUM exakt gegen tatsächliche Arbeit prüfen.

BEFUND:
Bei der Paul-Isolationsreparatur war die dauerhafte Rollenregel korrekt, aber ich hatte den TEXT-HOBBYRAUM ohne neue belegte Fachzuweisung auf
`STATUS: AKTIV / TEXT-ARBEITSCHAT FÜHRT`
gesetzt.

Das war unzulässig, weil vor dem Architekturfix eine aktive Paul-Arbeitsbindung belegt war und der Nutzer keine neue Fachzuweisung ausgesprochen hatte.

KISS-KORREKTUR:
- bestehende Paul-Spezialarbeitsbindung wiederhergestellt;
- normaler Arbeitschat wird trotzdem nicht zu Paul geroutet;
- gleicher technischer Bereich bleibt für Parallelwrites gesperrt;
- unabhängige TEXT-Arbeit bleibt möglich;
- HOBBYRAUM_STANDARD um harte Schutzregel gegen Status-/Worker-Erfindung ergänzt.

BEZUG:
ARCH-049; BAU-025.


### 2026-09-05 – Universeller technischer PROTOKOLLCHECK vorbereitet

AUSLÖSER:
Der Nutzer stellte zurecht fest, dass auch der Baucontainer-Chat seine eigenen Anfangs-/Abschlussregeln vergessen kann. Die bisherige „automatische Erinnerung“ war noch keine technische Sperre, sondern nur dokumentierte Pflicht.

KISS-IMPLEMENTIERUNG:
Security-PR #137 erweitert:
- gilt für jeden PR mit `protocol/PROJECT_MEMORY/**`-Diff;
- verlangt maschinenlesbaren `PROTOKOLLCHECK` im PR-Text;
- Pflichtfelder: Fehler, Protokoll, WARUM, CURRENT_STATE, HOBBYRAUM/NEXT ACTION, Zielvertrag, Archiv, Eine Wahrheit, Tests, technische Checks;
- Diff-Konsistenzprüfung gegen tatsächlich geänderte CURRENT_STATE-/HOBBYRAUM-/Ziel-/Archiv-/Fehler-/Protokoll-/WARUM-Dateien;
- Architekturänderungen erzwingen zusätzlich `AENDERUNGSREGISTER.md` + `BAUCONTAINER/BAUPROTOKOLL.md`;
- `EINE_WAHRHEIT` und `TESTS` müssen PASS sein.

ABDECKUNG:
Gesamter `protocol/PROJECT_MEMORY/**`-Baum – ausdrücklich einschließlich Baucontainer selbst.

LOKALER LOGIKTEST:
- gültiger Architektur-PROTOKOLLCHECK → PASS;
- fehlender Block → BLOCK;
- Diff widerspricht `NICHT_BETROFFEN` → BLOCK;
- TESTS = OFFEN → BLOCK;
- Nicht-PROJECT_MEMORY-Diff → NOT_APPLICABLE.

STATUS:
Implementiert im Security-Branch, aber noch nicht serverseitig aktiv auf main.
Grund: derselbe bewusste immutable-Base-Selbstschutz wie BAU-024.

BEZUG:
ARCH-050; BAU-026.


### 2026-09-05 – Automatische Sicherung hart positiv/negativ getestet

ZIEL:
Nicht nur Regeln dokumentieren, sondern die vorbereitete automatische Sicherung gegen erlaubte und verbotene Fälle hart prüfen.

TEST 1 – ERSTER LAUF:
22 Fälle vorgesehen.
ERGEBNIS:
21 PASS / 1 FAIL.

GEFUNDENER ECHTER FEHLER:
Eine Änderung an
`protocol/PROJECT_MEMORY/ZIELVERTRAEGE/REGISTER.md`
wurde noch nicht als Zielvertragsänderung erkannt, weil der Matcher nur `ZIELVERTRAG` prüfte.

KISS-FIX:
Matcher um `ZIELVERTRAEGE` ergänzt.
Security-Commit:
`08b3cd54492623ba621f408969c91445ef474a8d`.

TEST 2 – VOLLSTÄNDIGE WIEDERHOLUNG:
**22/22 PASS.**

PAUL-/PFADSPERRE 5/5:
- NEGATIV: `paul/*` + PROJECT_MEMORY → `PAUL_PROJECT_MEMORY_WRITE_BLOCKED`;
- POSITIV: `paul/*` + rein technischer Pfad → PASS;
- POSITIV: normaler Arbeitsbranch + PROJECT_MEMORY → Paul-Sperre greift nicht fälschlich;
- NEGATIV: immutable Workflow-Pfad → `IMMUTABLE_SECURITY_PATH_CHANGE_BLOCKED`;
- NEGATIV: Paul + gemischter Diff mit PROJECT_MEMORY → BLOCK.

PROTOKOLLCHECK 17/17:
- Nicht-PROJECT_MEMORY → NOT_APPLICABLE;
- gültige Architekturänderung → PASS;
- einfache gültige PROJECT_MEMORY-Änderung → PASS;
- fehlender PROTOKOLLCHECK → BLOCK;
- fehlendes Pflichtfeld → BLOCK;
- Eine Wahrheit != PASS → BLOCK;
- Tests != PASS → BLOCK;
- technische Checks BLOCKED → BLOCK;
- CURRENT_STATE geändert + NICHT_BETROFFEN → BLOCK;
- HOBBYRAUM geändert + NICHT_BETROFFEN → BLOCK;
- Zielregister geändert + NICHT_BETROFFEN → BLOCK;
- Zielvertragsoriginal geändert + NICHT_BETROFFEN → BLOCK;
- Archiv geändert + NICHT_BETROFFEN → BLOCK;
- Fehlerakte/-register geändert + NICHT_BETROFFEN → BLOCK;
- Protokoll geändert + NICHT_BETROFFEN → BLOCK;
- Änderungsregister geändert + WARUM NICHT_BETROFFEN → BLOCK;
- Architektur geändert ohne AENDERUNGSREGISTER + BAUPROTOKOLL → BLOCK.

SELBSTTEST IM WORKFLOW:
Die wichtigsten Positiv-/Negativfälle sind zusätzlich direkt in der Kandidaten-`hardlock-base` eingebaut und laufen nach Aktivierung bei jedem Check mit.

BEWERTUNG:
**LOGIKTEST PASS.**
**SERVERSEITIGE AKTIVIERUNG WEITER BLOCKED** bis Admin-Wartung von PR #137; deshalb kein falscher Gesamt-PASS für BAU-024/026.

BEZUG:
ARCH-050/051; BAU-024/026.


### 2026-09-05 – Real-Diff-Abnahme der automatischen Sicherung

Zusätzlich zu den 22 synthetischen Positiv-/Negativfällen wurde die Kandidatenlogik gegen echte vorhandene PR-Diffs ausgewertet.

PR #138 – echter Negativfall:
- Head: `paul/hardlock-negative-selftest-20260905`
- Diff: `protocol/PROJECT_MEMORY/PAUL_WRITE_NEGATIVE_SELFTEST.txt`
- Erwartung: BLOCK
- Ergebnis: `PAUL_PROJECT_MEMORY_WRITE_BLOCKED`
- PASS

PR #139 – echter Positivfall:
- Head: `paul/hardlock-positive-selftest-20260905`
- Diff nur außerhalb PROJECT_MEMORY
- Erwartung: Paul-Sperre darf nicht auslösen
- Ergebnis: PASS / PROTOKOLLCHECK NOT_APPLICABLE
- PASS

PR #134 – echter Campusfall:
- Head: `hobbyroom/project-memory-campus-v1-20260905`
- realer PROJECT_MEMORY-Gesamtdiff
- maschinenlesbarer PROTOKOLLCHECK im PR-Text ergänzt
- Pfadsperre: PASS
- Protokollguard: `PROJECT_MEMORY_PROTOCOLCHECK_PASS`
- PASS

GESAMT LOGIKABNAHME:
- synthetisch: 22/22 PASS nach einem gefundenen und behobenen Zielvertrags-Matcherfehler;
- echte PR-Diffs: 3/3 erwartungsgemäß;
- Kandidatenstruktur/Selbsttestmarker: PASS.

WICHTIGE GRENZE:
Noch kein serverseitiger Required-Check-PASS für die neue Logik, weil Security-PR #137 weiterhin nicht auf main aktiviert ist.


### 2026-09-05 – Paul vollständig auf Campus-Pull statt Promptübergabe umgestellt

AUSLÖSER:
Der Nutzer will Paul ohne wiederkehrende Übergabeprompts nutzen. Alle aktuellen Informationen sollen automatisch aus der einzigen Campuswahrheit kommen.

KRITISCHE PRÜFUNG:
Verworfen wurden:
- 1:1-Livesynchronisation von Campusakten in Pauls Etage;
- eigener dauerhafter Paul-Status;
- separater zweiter Workflow-Bootstrap;
- täglich generierte Paul-Prompts.

GRUND:
Alle vier Varianten erzeugen zusätzliche Wahrheiten, Synchronisationsbedarf oder Konkurrenz zur bestehenden `cloud_entry.py`-Eingangstür.

KISS-LÖSUNG:
- `HOBBYRAUM.md` bleibt einzige aktuelle Auftragswahrheit;
- Paul-Zuweisung nur als kleiner maschinenlesbarer `PAUL_ASSIGNMENT_V1`-Block mit Quellenverweisen;
- campusweit maximal ein aktiver Paul-Auftrag;
- Security-Kandidat erhält `control/paul-scope-gate/paul_scope_gate.py`;
- `AGENTS.md` erzwingt auf `paul/*` nach erfolgreichem Cloud-Start automatisch `paul_scope_gate.py start`;
- vor Cloud-Abschluss automatisch `verify`;
- bestehender `hardlock-base` prüft bei Paul-PRs zusätzlich aktuelle Zuweisung und Write-Scope;
- relevante Quellen werden lokal nur temporär/hashgebunden in `.paul-capsule/` materialisiert;
- relevante Drift → `STALE_ASSIGNMENT_BLOCKED`;
- keine Paul-Zuweisung → `PAUL_NOT_ASSIGNED`.

AKTUELLER REALZUSTAND:
Der TEXT-Hobbyraum weist aktuell den normalen TEXT-Arbeitschat B01 zu und sagt ausdrücklich, dass Paul nicht gebunden ist.
Daher muss Paul im aktuellen Stand automatisch STOP erhalten.

SECURITY-AKTIVIERUNG:
Die Automatik ist im Security-PR #137 vorbereitet, aber bis zur einmaligen bewussten Admin-Wartungsaktivierung nicht auf main wirksam.

BEZUG:
ARCH-052/053; BAU-027.


### 2026-09-05 – Paul-Scope-Gate Volltest + kritische Korrekturen

SELBSTTEST:
`PAUL_SCOPE_GATE_SELFTEST_PASS:11/11`
Python-Syntax/Compile: PASS.

VOLLSTÄNDIGER LOKALER GIT-TEST:
Ein echtes lokales Bare-`origin`, ein offizieller Campus-Branch und echte Paul-Branches wurden aufgebaut.

ERGEBNIS NACH KORREKTUR:
1. gültiger Auftrag / korrekter Branch → `PAUL_BOOTSTRAP_PASS`;
2. Write innerhalb Scope → `PAUL_VERIFY_PASS`;
3. Write außerhalb Scope → `PAUL_WRITE_SCOPE_BLOCKED`;
4. gebundene TASK_SOURCE ändert sich → `STALE_ASSIGNMENT_BLOCKED:SOURCE_CHANGED`;
5. kein aktiver Paul-Auftrag → `PAUL_NOT_ASSIGNED`;
6. zwei aktive Paul-Aufträge → `PAUL_MULTIPLE_ASSIGNMENTS_BLOCKED`;
7. falscher Paul-Branch → `PAUL_BRANCH_MISMATCH_BLOCKED`;
8. READ_ONLY-Auftrag → Start PASS;
9. Write bei READ_ONLY → `PAUL_WRITE_SCOPE_BLOCKED:READ_ONLY`.

GEFUNDENER FEHLER IM ERSTEN VOLLTEST:
Der erste Entwurf fetchte den offiziellen Campus in eine lokale Remote-Tracking-Referenz.
Bei einem bewusst zurückgesetzten Test-Campus wurde der Fetch mit non-fast-forward abgelehnt.

KISS-FIX:
Offizieller Campus wird jetzt direkt gefetcht und über `FETCH_HEAD` ausgewertet.
Security-Commit:
`2c2cecce938da5bc4d124dee7015b850133b47ae`.

WIEDERHOLUNG:
Alle 9 Volltests erwartungsgemäß PASS/BLOCK.

REALER CAMPUSCHECK:
- aktueller Campus-Head zum Prüfzeitpunkt: `1bc3fa72584fb491cd9ff9be0bab70742df7fb5a`;
- 8 reale HOBBYRAUM-Dateien;
- 0 aktive/überhaupt vorhandene `PAUL_ASSIGNMENT_V1`-Marker;
- daher aktueller erwarteter Paul-Start: `PAUL_NOT_ASSIGNED`.
- Campus `hardlock`: PASS;
- Campus `hardlock-base`: PASS.

TECHNISCHE GRENZE:
Repo-/Codex-Worker können über `AGENTS.md` automatisch gezwungen werden.
Ein beliebiger freier Chat kann nicht allein durch GitHub beim Öffnen Code automatisch ausführen; dafür bleibt die serverseitige PR-/Hardlock-Sperre die zweite Schutzschicht.

BEZUG:
ARCH-052 bis ARCH-054; BAU-027.


### 2026-09-05 – Single-Writer-Gegensperre + Branch-Hygiene hart getestet

KRITISCHER BEFUND:
Die erste Paul-Sicherung begrenzte Paul, hätte aber einen normalen Parallel-PR im selben technischen Scope noch nicht technisch verhindert.

KISS-FIX:
`paul_scope_gate.py verify-pr` läuft künftig für **alle** PRs:
- gebundener Paul-Branch → eigener Scope wird geprüft;
- anderer `paul/*`-Branch → Branch-Mismatch BLOCK;
- normaler PR im aktiven Paul-`WRITE_SCOPE` → `PAUL_EXCLUSIVE_SCOPE_LOCKED`;
- normaler PR außerhalb Scope → PASS;
- ohne Paul-Auftrag → für normale PRs NOT_APPLICABLE.

HARTER GIT-TEST AUF FINALER LOGIK:
- Selftest 11/11 PASS;
- Paul Start gültig → PASS;
- Paul allowed write → PASS;
- Paul out-of-scope → BLOCK;
- Paul-PR im Scope → PASS;
- normaler PR im gesperrten Paul-Scope → `PAUL_EXCLUSIVE_SCOPE_LOCKED`;
- normaler PR außerhalb Scope → PASS;
- falscher Paul-Branch → BLOCK;
- relevante Source-Drift → STALE BLOCK;
- Paul ohne Auftrag → BLOCK;
- normaler PR ohne Paul-Auftrag → NOT_APPLICABLE;
- Mehrfachauftrag → BLOCK;
- falsche technische Basis → `PAUL_BASE_MISMATCH_BLOCKED`.

READ_ONLY-RANDTEST:
Wiederverwendung eines alten Paul-Branches mit bestehendem Commit wurde korrekt bereits beim Start blockiert.
Auf einem frischen Branch direkt vom Base:
- READ_ONLY Start → PASS;
- anschließender Write → `PAUL_WRITE_SCOPE_BLOCKED:READ_ONLY`.

FOLGERUNG:
Jeder neue Paul-Auftrag = frischer Branch vom exakten Technical Base.

BEZUG:
ARCH-055; BAU-027.


### 2026-09-05 – Altarchiv 0057 + LanguageTool 6.8 einsortiert

EINGANG:
1. `ARBEITSMASTER_0057_NEU_TEIL_A_UNVERAENDERLICHES_HISTORIENARCHIV(1).zip`
2. `ARBEITSMASTER_0043_NEU_TEIL_2_LANGUAGETOOL_ABHAENGIGKEIT(2).zip`

HARTER BEFUND 0057:
- äußere ZIP SHA-256 `25c8a9fa71ff6f1f57137c2afb1e2c03ed8a6e3477f2902fdf003590ea785423`;
- README: unveränderliches Historienarchiv;
- ausschließlich `98_HISTORY_READ_ONLY`;
- Manifest 4.955 Dateien / Liste 4.955;
- innerer tar.zst-Hash real gegen Manifest geprüft → PASS;
- persistent unter TEXT/STARTMASTER/HISTORISCH abgelegt.

HARTER BEFUND LANGUAGETOOL:
- äußere ZIP SHA-256 `187f7c2efe7762049e9f00553dafe686e269bbf62220abe2f2715fe55df8605a`;
- inneres LanguageTool 6.8 SHA-256 `6a7f6b67b779ae9505f7579f0c41453ea8d1bd72ae750bdc2c55ba974281467d`;
- Hash + Größe gegen Originalmanifest PASS;
- 2.051 Einträge im LanguageTool-ZIP;
- README: unveränderte Offline-Abhängigkeit, nicht als Plugin installieren;
- aktuelles `main`: keine LanguageTool-/offline_languagetool-/LANGUAGE_TOOL_PREFLIGHT-Treffer;
- daher aktuelle Nutzung UNGEKLÄRT;
- persistent unter `/Campus-Archiv/PROJEKTE/PFERDE_ATELIER/TEXT_STARTMASTER0107/ABHAENGIGKEITEN/LANGUAGETOOL/6.8/` abgelegt.

KISS-EINORDNUNG:
- **beide Uploads gehören TEXT/SEO**;
- kein neuer aktueller Fachstatus;
- kein allgemeingültiges Modul;
- kein WordPress-Eintrag;
- CURRENT_STATE unverändert;
- HOBBYRAUM unverändert;
- Fehler-/Zielwahrheit unverändert;
- Archivregister + Hausmeisterprotokoll + TEXT-Inventar + WHY aktualisiert.

AMPel:
beide GELB – jeweils eine persistente verifizierte Rohablage, keine zweite unabhängige verifizierte Ablage.

BEZUG:
ARCH-056; HM-001/HM-002.


### 2026-09-05 – Korrektur der LanguageTool-Zuordnung

AUSLÖSER:
Der Nutzer hat klargestellt, dass sowohl das Historienarchiv 0057 als auch LanguageTool fachlich zu TEXT/SEO gehören.

FEHLER:
LanguageTool war zunächst zu breit unter einem campusweiten allgemeinen Abhängigkeitsarchiv eingeordnet.

KORREKTUR:
- LanguageTool-Rohdatei aus dem allgemeinen Abhängigkeitspfad verschoben;
- alter allgemeiner Archivpfad vollständig entfernt;
- neuer eindeutiger Ort:
  `/Campus-Archiv/PROJEKTE/PFERDE_ATELIER/TEXT_STARTMASTER0107/ABHAENGIGKEITEN/LANGUAGETOOL/6.8/`;
- Register, Hausmeisterprotokoll, TEXT-Inventar und WHY entsprechend korrigiert.

WICHTIG:
Fachzugehörigkeit TEXT/SEO ist jetzt eindeutig.
Aktuelle operative Nutzung bleibt weiterhin UNGEKLÄRT, weil dafür kein aktueller main-/Produktionsbeleg vorliegt.


### 2026-09-05 – Tresor-/Archiv-Arbeitsquellenfehler campusweit geschlossen

AUSLÖSER:
Nachbarchat wollte den Campus-Tresor/Git-Mirror als lokalen Repo-Stand verwenden und daraus den vorhandenen Runner direkt ausführen.

BEFUND:
Falsch. Tresor/Archiv sind Restore-/Belegquellen, niemals Arbeitsquelle.

KISS-FIX:
- globale Regel im EINGANGSSTANDARD;
- Hauptpförtner + Handlungsverzeichnis;
- Archiv + Tresor;
- Notfall-Wiederaufbau;
- Hausmeister;
- Neubauvorlage.

TECHNISCH:
Bestehende `cloud_entry.py` im Security-PR #137 erweitert, kein neuer Runner.
Blockiert Backup-/Archiv-Worktree, Bare-Mirror, Sicherungs-Gitdir/Common-Dir und lokalen/nicht offiziellen origin.

BEZUG:
ARCH-057; BAU-028.


### 2026-09-05 – Tresor-/Archiv-Sperre harte Abnahme

FLÄCHENABDECKUNG:
Vier gezielte Campus-Commits gegen den realen Verzeichnisbaum geprüft:
- START_HERE: 22/22;
- HOBBYRAUM: 8/8;
- Gesamt direkte Eingänge/Räume: **30/30**;
- alle verweisen nur auf die eine autoritative Regel im `EINGANGSSTANDARD.md`.

ECHTER SECURITY-PR-TEST:
Security-Head:
`689176ee7c3ef3c6a5b97cb752553ce37a07f134`

GitHub `hardlock`:
**SUCCESS**

Ausgabe des real ausgeführten `cloud_repo_ci_test.py`:
- `CODEX_CLOUD_GATE_CI_PASS`;
- `positive_negative: PASS`;
- `backup_archive_workspace_execution_blocked: PASS`;
- `bare_mirror_execution_blocked: PASS`;
- `local_mirror_origin_execution_blocked: PASS`;
- `backup_common_gitdir_execution_blocked: PASS`.

Damit sind positiv/negativ belegt:
- normaler offizieller Worktree → erlaubt;
- Worktree direkt in Campus-Tresor/Archiv → BLOCK;
- Bare-Mirror → BLOCK;
- lokaler Mirror als origin → BLOCK;
- Worktree außerhalb mit Git-Common-Dir im Tresor → BLOCK.

WICHTIG:
`hardlock-base` des Security-PR bleibt erwartungsgemäß FAIL, weil die bestehende immutable Security-Schicht ihre eigene Änderung blockiert.
Daher:
**LOGIK + KANDIDATENTEST PASS; SERVERSEITIGE AKTIVIERUNG AUF main WEITER BLOCKED bis Admin-Wartung.**

BEZUG:
ARCH-057; BAU-028.


### 2026-09-05 – Paul-Frische hart positiv/negativ im echten GitHub-CI geprüft

FRAGE:
Ist sichergestellt, dass Paul nicht mit veralteten Campusdaten arbeitet, wenn der Fachstand sich weiterentwickelt?

NEUER PERMANENTER CI-TEST:
`control/paul-scope-gate/paul_scope_gate_ci_test.py`

Er wird im normalen `hardlock` des Security-Kandidaten ausgeführt.

ERSTER LAUF:
FAIL.
Befund:
Test erwartete bytegetreuen Quelltext; Paul-`show()` lief über die generische `git()`-Hilfsfunktion mit `.strip()`.
Dadurch wurden Rand-Whitespace/Zeilenumbrüche entfernt.

KISS-FIX:
`show()` liest Git-stdout jetzt unverändert.
Security-Commit:
`9e0340d55ce9c7359fed28e171143a54d4cad5ab`.

WIEDERHOLUNG – ECHTER GITHUB-HARDLOCK:
**SUCCESS**

Paul-CI-Ausgabe:
`PAUL_CURRENT_CAMPUS_CI_PASS`

HART POSITIV/NEGATIV BELEGT:
1. Paul-Branch enthält alte CURRENT_STATE-Kopie → wird ignoriert: PASS;
2. Start liest neuesten offiziellen Campus → PASS;
3. unveränderte relevante Quellen → VERIFY PASS;
4. TASK/Problem entwickelt sich weiter → `STALE_ASSIGNMENT_BLOCKED`: PASS;
5. erneuter Start lädt automatisch neuen Campusstand → PASS;
6. irrelevante Änderung im AENDERUNGSREGISTER → kein Fehlblock: PASS;
7. CURRENT_STATE ändert sich → STALE BLOCK: PASS;
8. Assignment-ID/HOBBYRAUM-Bindung ändert sich → STALE BLOCK: PASS;
9. Paul-Zuweisung entfernt → `PAUL_NOT_ASSIGNED`: PASS;
10. zwei aktive Paul-Zuweisungen → `PAUL_MULTIPLE_ASSIGNMENTS_BLOCKED`: PASS.

WICHTIGE DEFINITION:
Das ist **keine Live-Synchronisation während jeder Sekunde**.
Die Garantie lautet:
**frisch beim Start + fail-closed bei relevanter Drift vor gültiger Rückgabe + automatischer Refresh beim Neustart.**

SERVERSTATUS:
Security-Kandidat Logik = PASS.
Aktivierung auf `main` weiterhin durch bestehenden immutable `hardlock-base` BLOCKED; deshalb noch keine Behauptung „produktiv serverseitig aktiv“.

BEZUG:
ARCH-058/059; BAU-029.


### 2026-09-05 – Tresor hart geprüft und lokales 1:1-Backup gebaut

AUSGANG:
Bestehender V4-PREPASS in der Library gefunden und geprüft.
Belegt:
- Git-Bundle-Restore PASS;
- 261 Branches;
- 1 Tag;
- 136 Issues;
- 127 PRs;
- 1 Release;
- 1 Ruleset.

KRITISCH:
Dieser PREPASS bindet ältere Campus-/Paul-SHAs und ist nach weiterer Campusarbeit kein aktueller 1:1-Snapshot mehr.

ROHARCHIV:
Aktuelles `/Campus-Archiv`:
38 Dateien / 985.708.251 Bytes.

Umgesetzt:
- alle 38 Dateien materialisiert;
- SHA-256 je Datei;
- fünfteiliger lokaler Export;
- Wiederherstellungswerkzeug;
- realer Restore: 38/38 PASS;
- Negativtest: absichtlich manipulierter Teil → Hash FAIL.

LOKALER BACKUP-RUNNER:
`CAMPUS_LOCAL_TRESOR.command`

Positivtest:
- synthetischer Git-Origin mit mehreren Refs;
- Mirror;
- Bundle;
- Restore;
- Refvergleich;
- Archivkopie;
- bestätigte Recovery;
→ `LOCAL_BACKUP_PASS`.

Negativtests:
- Recovery nicht bestätigt → `LOCAL_BACKUP_BLOCKED:RECOVERY_NOT_CONFIRMED`;
- Campus-Archiv fehlt → BLOCK;
- manipulierter Exportteil → BLOCK.

RECOVERY:
Workflowprüfung findet als echten Secret:
`ENDSTEMPEL_PRIVATE_KEY`.

STATUS:
Werkzeug/Logik PASS.
Vollständiger `TRESOR_PASS` weiterhin BLOCKED durch:
1. zweite lokale Rohablage noch nicht vom Nutzer bestätigt;
2. fehlende finale Design-1.50.472-Rohartefakte;
3. Recovery-Secrets noch nicht vollständig praktisch bestätigt.

BEZUG:
ARCH-060 bis ARCH-062; BAU-030.


### 2026-09-05 – Paul-Eingang auf echte Ein-Tür-Automatik gehärtet

KRITISCHE NACHPRÜFUNG:
Die Frischelogik selbst war bereits hart getestet, aber `AGENTS.md` verlangte noch einen separaten Paul-Gate-Aufruf nach `cloud_entry.py start`.

BEFUND:
Das war für die Forderung „Paul muss zwingend automatisch sein“ zu weich: ein Worker konnte theoretisch die zweite Anweisung vergessen.

LOKALER HARTTEST VOR GITHUB-ÄNDERUNG:
Paul-Frische mit echtem lokalem Bare-origin/Campus-/Paul-Branch:
**10/10 PASS**
- alte Branch-Campus-Kopie wird ignoriert;
- Start liest neuesten Campus;
- TASK-/CURRENT_STATE-/Assignment-Drift blockiert;
- Neustart lädt neuen Stand;
- irrelevante Campusänderung blockiert nicht;
- ohne Auftrag / Mehrfachauftrag blockiert.

Vorgeschlagene Auto-Bridge separat positiv/negativ:
**6/6 PASS**
- normaler Branch → kein Paul-Gate;
- Paul start → auto;
- Paul verify → auto;
- complete → auto-preverify;
- Gate FAIL → Eingang BLOCK;
- Gate fehlt → Eingang BLOCK.

KISS-FIX:
Bestehende `cloud_entry.py` ruft den vorhandenen Paul-Scope-Gate jetzt selbst auf.
`AGENTS.md` verlangt keinen zweiten Paul-Befehl mehr.

ECHTER GITHUB-RUN:
Security-Head:
`d9bb690f677a34d09540338ca2a4c32494b42079`

GitHub Actions:
- `Paul automatic cloud-entry bridge CI` → SUCCESS;
- `Paul current-Campus positive-negative CI` → SUCCESS;
- gesamter `hardlock` → SUCCESS.

AUTOMATISCHE GARANTIE NACH AKTIVIERUNG:
Ein einziger `cloud_entry.py start` auf `paul/*` lädt automatisch den aktuellen Campus.
Ein gültiger Paul-Abschluss kann relevante Drift nicht überspringen, weil `complete` vorher automatisch Paul-`verify` ausführt.

STATUS:
Logik/Kandidat PASS.
Produktive Aktivierung auf main bleibt bis Admin-Aktivierung von PR #137 BLOCKED.

BEZUG:
ARCH-063; BAU-031.


### 2026-09-06 – Büro PRODUKTVERGLEICH eingerichtet

AUFTRAG:
Neues Büro „Produktvergleich“ im Pferde-Atelier mit Campus-/Gebäudeverweisen einrichten.

KISS-UMSETZUNG:
- neues Verzeichnis `PRODUKTVERGLEICH/`;
- `START_HERE.md`;
- `CURRENT_STATE.md`;
- genau ein `HOBBYRAUM.md`;
- Campus-START_HERE um natürliche Route ergänzt;
- Hauptpförtner um eindeutiges Produktvergleich-vs-TEXT-Routing ergänzt;
- Pferde-Atelier-Büroplan ergänzt;
- Handlungsverzeichnis ergänzt;
- keine neue Fehlerliste, kein neuer Zielvertrag, kein neuer Runner.

FACHGRENZE:
Produktvergleich bereitet Vergleichsdefinition, Vergleichseigenschaften, Faktendossier und Quellenbindung vor.
TEXT bleibt alleinige eigentliche Text-/STARTMASTER-Produktion.

DYNAMISCHE WAHRHEIT:
Neuer Hobbyraum = FREI.
Keine frühere Produktvergleichsarbeit aus Erinnerung zu CURRENT erklärt.

ABNAHME:
nach Commit:
- 7/7 Pferde-Atelier-Büros müssen `START_HERE + CURRENT_STATE + HOBBYRAUM` besitzen;
- neues Verzeichnis muss 1-Klick-Eingang besitzen;
- Campus/Pförtner/Gebäude/Handlungsverzeichnis müssen auf das Büro routen;
- Produktvergleichs-START_HERE darf keine dynamische Arbeitsbindung duplizieren;
- beide bestehenden Campus-Hardlocks müssen PASS sein.

BEZUG:
ARCH-064.


### 2026-09-06 – PRODUKTVERGLEICH Büro-Abnahme

REALER GIT-BAUM:
- Pferde-Atelier-Büros geprüft: **7/7**;
- jedes der sieben Büros besitzt `START_HERE.md + CURRENT_STATE.md + HOBBYRAUM.md`;
- neues Büro `PRODUKTVERGLEICH/`: 3/3 Pflichtdateien vorhanden.

POSITIV:
- Produktvergleich-`START_HERE` routet zu `CURRENT_STATE → HOBBYRAUM`;
- Gebäude-Büroplan routet zu PRODUKTVERGLEICH;
- Campus-START_HERE enthält natürliche Produktvergleichsroute;
- Hauptpförtner trennt Produktvergleichsvorbereitung eindeutig von TEXT-Produktion;
- Handlungsverzeichnis besitzt Produktvergleichsweg;
- CURRENT_STATE ist einzige Bürostand-Zusammenfassung;
- Hobbyraum ist `FREI`.

NEGATIV:
- kein `PAUL_ASSIGNMENT_V1` im neuen Hobbyraum;
- kein Worker/Branch durch reine Büroeinrichtung erfunden;
- keine zweite Textmaschine;
- keine neue Fehlerliste;
- kein neuer Zielvertrag;
- keine frühere Produktvergleichsarbeit aus Erinnerung als CURRENT kopiert.

GITHUB-CHECKS AUF HEAD
`c5d00b645980d26c6664e399547ca4afddaac3d5`:
- `hardlock` = SUCCESS;
- `hardlock-base` = SUCCESS.

ERGEBNIS:
**BÜROARCHITEKTUR PASS.**
Facharbeit bleibt bis ausdrücklichem Auftrag ungebunden.

### 2026-09-06 – Harte Fehlerabgleich-Sperre an Bürotüren

BEDARF:
Im TEXT-Prüfprozess wurde B06 erneut praktisch ausprobiert, obwohl der Fehler bereits in der autoritativen Fehlerliste dokumentiert war. Die Bürotür verlinkte das Fehlerregister, erzwang den Abgleich aber nicht vor jeder technischen Aktion.

KISS-FIX:
- TEXT-`START_HERE.md`: harte Fehlerabgleich-Sperre vor Test/Live/Branch-/Code-/Merge-/Release-Aktion;
- `EINGANGSSTANDARD.md`: gleiche Pflicht als Bürostandard;
- `NEUES_PROJEKT_VORLAGE.md`: neue Projektbüros erben die Pflicht automatisch.

HARD RULE:
Bekannter Treffer = nicht erneut praktisch ausprobieren. Vorhandene Lösung/Arbeitsgrenze übernehmen.

NICHT VERÄNDERT:
Campus-Eingang und Campus-Routing.

ABNAHME POSITIV/NEGATIV:
- TEXT-Bürotür enthält Fehlerabgleich-Sperre + STOP bei Treffer → PASS;
- EINGANGSSTANDARD enthält die Regel ausschließlich als Bürotür-Regel → PASS;
- NEUES_PROJEKT_VORLAGE vererbt die Pflicht → PASS;
- Campus-`START_HERE.md` enthält die neue Bürotür-Sperre **nicht** → NEGATIV-PASS;
- Campus-Dokumentationshead nach Nachholung: `hardlock-base` SUCCESS.

BEZUG:
ARCH-065 / BAU-032.



### 2026-09-06 – Externe READ-ONLY-Außentür für Paul

AUSLÖSER:
Claude meldete, dass seine aktuelle Umgebung keine Git-/Repository-Werkzeuge besitzt und daher `PAUL/TEXT_SEO/START_HERE.md` nicht direkt erreichen könne.

BEFUND:
Die Paul-Etage selbst ist korrekt. Das Problem ist die Zugriffsschicht der externen Chatumgebung, nicht die Campusstruktur.

KISS-LÖSUNG:
- keine neue Claude-Etage;
- `PAUL/READ_ONLY_REVIEW.md` als eine Außentür;
- nur absolute GitHub-Web-/Raw-Links auf den offiziellen Campus-Branch;
- READ/REVIEW ONLY;
- keine Fach-/Statuskopien;
- bei komplett fehlendem Webzugriff genau eine automatisch erzeugte Prüfkapsel als Fallback.

NEGATIV:
Kein Schreibrecht, kein Merge, kein neuer Paul-Auftrag, keine zweite Wahrheit.

BEZUG:
ARCH-066.


### 2026-09-06 – Außentür von TEXT/SEO auf allgemeingültige Zweitprüfung korrigiert

AUSLÖSER:
Claude nutzte die erste READ-ONLY-Außentür und prüfte ungefragt Paul-/Branch-/Campusarchitektur statt primär den vom Nutzer gewünschten Fachinhalt.

URSACHE:
Die Außentür war zu eng auf TEXT/SEO verdrahtet und erlaubte ausdrücklich „Architektur und Konsistenz prüfen“. Damit war die Scope-Ausweitung durch Claude durch unsere eigene Anweisung gedeckt.

KISS-KORREKTUR:
- keine neue Claude-Etage;
- bestehende `PAUL/READ_ONLY_REVIEW.md` bleibt die **eine Außentür**;
- jetzt allgemeingültig für alle Projekte, Büros und Themen;
- Prüfgegenstand = exakt Nutzerauftrag;
- Standard = FACH-/INHALTSPRÜFUNG;
- Paul-/Campus-/Branch-/Routingarchitektur nur bei ausdrücklich verlangter SYSTEM-/ARCHITEKTURPRÜFUNG;
- Claude bleibt READ-ONLY-Zweitprüfer;
- Paul darf Befunde anschließend verwenden.

NEBENBEFUND:
Doppelte ID `ARCH-065` erkannt.
Die bereits bestehende Fehlerabgleich-Regel behält `ARCH-065`.
Die externe Außentür wird eindeutig auf `ARCH-066` korrigiert.

NEGATIV:
kein eigener Claude-Bereich, keine zweite Wahrheit, keine automatische Auftragsübernahme.

BEZUG:
ARCH-066.


### 2026-09-07 – PB ONE als Agenturzentrale eingerichtet

AUFTRAG:
Zentrales Gebäude für die Agentur PB ONE schaffen.
Kein Programmierraum, sondern Unterlagen-/Angebots-/Ideen-Knotenpunkt.

KISS-UMSETZUNG:
- `PB_ONE/START_HERE.md`;
- `ANGEBOTE_FLYER/` mit START_HERE, CURRENT_STATE, HOBBYRAUM, UNTERLAGENREGISTER;
- `IDEENWERKSTATT/` mit START_HERE, CURRENT_STATE, HOBBYRAUM, IDEENREGISTER;
- Campus/Pförtner/Handlungsverzeichnis ergänzt;
- Nutzer und Paul arbeiten in PB ONE mit denselben redaktionellen Rechten.

HARTE GRENZE:
Keine Programmierung in PB ONE.
Keine zweite Projekt-/Fachwahrheit.
Übergabe an bestehendes/neues Projektbüro erst nach bewusster Entscheidung.

STARTSTATUS:
beide Hobbyräume FREI.
Keine alten Angebote/Ideen aus Erinnerung zu CURRENT erklärt.

BEZUG:
ARCH-067/068.


### 2026-09-07 – PB ONE auf gleichberechtigte gemeinsame Agentur korrigiert

NUTZERKORREKTUR:
PB ONE ist nicht ein Paul-Sparringsraum mit eingeschränkten Paul-Rechten.
PB ONE ist die gemeinsame Agentur von Nutzer und Paul.

KORREKTUR:
- Nutzer und Paul haben in `PB_ONE/**` dieselben redaktionellen Rechte;
- Paul darf dort Inhalte/Register/Ideen/Konzepte/Unterlagen lesen und schreiben;
- die allgemeine PROJECT_MEMORY-READ-ONLY-Regel für Paul erhält für `PB_ONE/**` eine redaktionelle Ausnahme;
- keine technische Paul-Workerrolle innerhalb PB ONE;
- weiterhin keine Programmierung;
- zusätzlich `ZENTRALREGISTER.md`;
- zusätzlich `ENTWICKLUNGSRAUM/` mit Konzeptregister.

ARBEITSLOGIK:
Ideenschmiede → Entwicklungsraum → Angebot/Flyer oder bewusste Projektübergabe.

NEGATIV:
kein `paul/*`-Branch, kein WRITE_SCOPE, keine technische Projektarbeit innerhalb PB ONE.

BEZUG:
ARCH-068/069.


### 2026-09-07 – PB ONE Arbeitsdokumente ergänzt

BEDARF:
Laufende Präsentationen, Flyer und Konzeptpapiere brauchen eine eigene Akte, damit Punktesammlung, Entscheidungen und Entwürfe chatübergreifend erhalten bleiben.

KISS-UMSETZUNG:
- `PB_ONE/ARBEITSDOKUMENTE/START_HERE.md`;
- `REGISTER.md` als Index;
- `VORLAGE.md` als minimale Aktenvorlage;
- Verweise aus PB ONE, Zentralregister, Angebote/Flyer und Handlungsverzeichnis.

ARBEITSLOGIK:
Punkte sammeln → eigene Akte fortschreiben → Entwurf entwickeln → freigeben → finales Ergebnis im zuständigen Register referenzieren.

NEGATIV:
Keine zweite CURRENT-Wahrheit, kein zusätzlicher Hobbyraum, keine Programmierung.

BEZUG:
ARCH-070.


### 2026-09-07 – PB ONE Aktenschrank und Website-Akte angelegt

AUFTRAG:
Die aktuelle PB-ONE-Website aus dem bereitgestellten WordPress-Export dauerhaft im PB-ONE-Aktenschrank verfügbar machen.

KISS-UMSETZUNG:
- `PB_ONE/AKTENSCHRANK/START_HERE.md`;
- `PB_ONE/AKTENSCHRANK/REGISTER.md`;
- `PB_ONE/AKTENSCHRANK/WEBSITE_PB_ONE_20260907.md`;
- PB-ONE-Eingang und Zentralregister verlinkt.

QUELLE:
`codetrifftcreativitt.WordPress.2026-09-07.xml`
WordPress-Export der Website `https://p-b.one`, erzeugt 2026-09-07.

INHALT:
Positionierung, Leistungen, Arbeitsweise, Werte, Gründerprofil, KI-Angebot, importly/BMEcat, Zusammenarbeit/FAQ und wichtige Nutzungsgrenzen.

NEGATIV:
Kein XML-Rohdump in der aktiven PB-ONE-Struktur.
Keine Behauptung, dass der Export ein vollständiges Backup oder eine externe Verifikation der Website-Aussagen ist.

BEZUG:
ARCH-071.


### 2026-09-07 – Abschluss-/Nachholprüfung Architekturbüro

AUSLÖSER:
Universelle Abschluss-/Nachholprüfung vor dem bewussten Campus-Cut.

FRISCH GEPRÜFT:
aktueller Campus-Head, Baucontainer, Hauptpförtner, Bauplan, Bauänderungsindex, Entwicklungsprotokoll, Architektur-Fehlerkiste und PB-ONE-Architektur.

GEFUNDEN:
1. Hauptpförtner nannte Paul in PB ONE noch veraltet nur als Sparringspartner.
2. Bauplan enthielt PB ONE noch nicht.
3. Bauänderungsindex endete bei ARCH-043 und war gegenüber ARCH-044 bis ARCH-071 stale.
4. Technische PB-ONE-Schreibausnahme für Paul ist weiterhin nicht implementiert.

NACHGEHOLT:
- Hauptpförtner korrigiert;
- Bauplan PB ONE ergänzt;
- BAUAENDERUNGEN bis ARCH-071 nachgezogen;
- Entwicklungsprotokoll um PB-ONE-Entstehung + Campus-Cut ergänzt;
- BAU-033 CLOSED dokumentiert;
- BAU-034 als BLOCKED dokumentiert.

CUT:
Kein weiterer Architektur-Ausbau auf Vorrat.
Campus ab jetzt real nutzen; nur konkrete Nutzungslücken führen zu neuen Umbauten.


### 2026-09-07 – Tresor-Zuständigkeit und PB-ONE-Pluginfach geklärt

ANLASS:
Vor dem Campus-Cut sollte eindeutig sein, wo Download-/lokale Sicherung konzipiert und praktisch ausgeführt wird und wo PB ONE eigene Plugin-Entwicklungen dauerhaft findet.

ENTSCHEIDUNG TRESOR:
- Baucontainer definiert Sicherungsarchitektur, Regeln und Anforderungen.
- Tresorraum führt Backup, Download, lokale Kopie, Hashprüfung, Recovery und Restore-Test aus.
- bestehendes `TRESOR/LOKALES_BACKUP_KONZEPT.md` bleibt die operative Hauptquelle.

AKTUELLER TRESORBEFUND:
Konzept + Werkzeuge V1 vorhanden und positiv/negativ getestet.
Kein TRESOR_PASS, solange zweite unabhängige lokale Kopie, fehlende Rohartefakte und Recovery-Abhängigkeiten nicht vollständig bestätigt sind.

ENTSCHEIDUNG PB ONE:
Im bestehenden `PB_ONE/AKTENSCHRANK/` wird kein zweiter Aktenschrank gebaut.
Stattdessen entsteht `PLUGINS/` als eigenes Fach für bestätigte selbstentwickelte Plugins/Eigenentwicklungen.

EINE-WAHRHEIT-REGEL:
Pluginfach = Agentur-/IP-Katalog.
Technische Version/Release/LIVE-Wahrheit bleibt im WORDPRESS_REGISTER, MODULREGISTER bzw. zuständiger Fachquelle.

BEZUG:
ARCH-072/073.

### 2026-09-07 – PB-ONE-TODO-Fach für Vertriebsbereitschaft ergänzt

ANLASS:
Der Nutzer benötigt eine dauerhaft auffindbare Liste der noch fehlenden Grundlagen, damit der PB-ONE-Vertrieb direkt arbeitsfähig wird.

UMSETZUNG:
- `PB_ONE/AKTENSCHRANK/TODO/START_HERE.md` angelegt;
- `VERTRIEB_STARTKLAR_20260907.md` mit offenen Punkten zu Produkten/Preisen, operativen Abläufen, Lead Management und Verkaufsunterlagen angelegt;
- PB-ONE-Aktenschrank und Register auf das neue Fach ausgeschildert;
- keine Preis-, Vertrags-, Prozess- oder technische Wahrheit im TODO-Fach erfunden.

EINE-WAHRHEIT-REGEL:
TODO = offene Punkte / Entscheidungsübersicht.
Entschiedene Inhalte werden später an ihren autoritativen Hauptquellen gepflegt.

BEZUG:
ARCH-074.


### 2026-09-07 – Tresor-Mac-Kit aktualisiert und erneut hart getestet

AUFTRAG:
Nach Campus-Architekturabschluss den praktischen lokalen Sicherungsweg bis zur Nutzergrenze vorbereiten.

BESTAND:
Vorhandenes V1-Kit nicht neu erfunden, sondern geprüft und um praktische Mac-/Download-Unterlagen ergänzt.

NEUES KIT:
`CAMPUS_LOCAL_TRESOR_KIT_20260907.zip`
SHA-256:
`74ebe867ddcb3920fe333f3d2bb31a9d7332bc03e0cd6c7a72a99f0a1bf033c6`

DAUERHAFTE ABLAGE:
`/Campus-Archiv/TRESOR_TOOLS/2026-09-07/`

TEST:
- positiver Test → LOCAL_BACKUP_PASS;
- Recovery negativ → korrekt BLOCKED;
- Archiv fehlt → korrekt BLOCK.

ERGEBNIS:
Werkzeug/Downloadkonzept PASS.
Echter Nutzer-Lokalbackup weiterhin OFFEN, weil die unabhängige physische/local Kopie nur auf dem Nutzer-Datenträger entstehen kann.

TRESOR_PASS:
weiterhin BLOCKED durch Redundanz-/Rohartefakt-/Recovery-Restpunkte.

### 2026-09-07 – PB ONE Vertriebsstruktur aus TODO abgeleitet

ANLASS:
Die Vertriebs-TODO-Liste sollte auf dauerhafte sinnvolle Bereiche geprüft werden; zusätzlich wurde ein Bereich für Präsentation & Werbung gewünscht.

ERGEBNIS:
- PREISE = eigenes dauerhaftes Fach;
- VERTRIEB = eigenes dauerhaftes Fach für Abläufe + Lead-Management + Onboarding;
- PRÄSENTATION & WERBUNG = kein neuer Doppelraum, sondern Erweiterung des vorhandenen `ANGEBOTE_FLYER`-Bereichs;
- kein separates Lead-Management-Fach;
- kein separates Onboarding-Fach.

ROUTING:
- Preise/Konditionen/Zahlungsmodell → `PB_ONE/AKTENSCHRANK/PREISE/`;
- Kundendaten/Angebotsablauf/Sonderfälle/Onboarding/Leads → `PB_ONE/AKTENSCHRANK/VERTRIEB/`;
- Pitch/Musterseiten/Präsentation/Werbung/Angebote/Leistungsbeschreibung → `PB_ONE/ANGEBOTE_FLYER/`;
- offene Restpunkte → `PB_ONE/AKTENSCHRANK/TODO/`.

BESCHILDERUNG:
PB-ONE-Türschild, Zentralregister, Aktenschrank-START_HERE und Aktenschrank-Register wurden entsprechend nachgezogen.

BEZUG:
ARCH-075/076/077.


### 2026-09-07 – Tresor V2 Ein-Klick-Automatisierung

ZIEL:
GitHub + Campus-Tresor möglichst automatisiert als einen Sicherungsweg betreiben.

UMSETZUNG:
- `START_CAMPUS_TRESOR.command` als einheitlicher Ein-Klick-Starter;
- automatische Archivprüfung/-wiederherstellung;
- vollständiger bestehender Git-/GitHub-/Campus-/Recovery-Runner wird danach automatisch aufgerufen;
- GitHub-Metadaten um Environments, Actions-Secret-Namen, Actions-Variablen und Actions-Berechtigungen erweitert;
- `AUTOMATIK_EINRICHTEN.command` für täglich/wöchentlich planbare macOS-Sicherung.

KIT:
`CAMPUS_LOCAL_TRESOR_KIT_20260907_V2.zip`
SHA-256:
`bb5f28d26885fd8b58fd86bea3548375c97782f58581277daddd651b2151ca54`

TEST:
Syntax PASS; positiver Lauf PASS; Recovery-Negativ korrekt BLOCKED; fehlendes Archiv korrekt BLOCK.

GRENZE:
Ein echter unabhängiger lokaler PASS kann nur auf dem Nutzer-Datenträger entstehen.
Library-Roharchive werden nicht automatisch vom Mac aus ChatGPT nachgeladen.


### 2026-09-07 – Tresorziel auf geschlossene Ein-Datei-Recovery verschärft

NUTZERZIEL:
Nach vollständigem Verlust soll eine einzige lokal gespeicherte Tresordatei genügen, um den kompletten GitHub-Campus mit allen recovery-relevanten Informationen wiederherzustellen; zusätzlich bleibt der zuvor definierte Gesamtanspruch inklusive WordPress bestehen.

KRITISCHE PRÜFUNG:
- KISS: PASS – eine Einheit statt mehrerer Pflichtdownloads;
- nachhaltig: PASS – versionierte Kapseln + automatisierte Erzeugung + realer Restore;
- sicher: PASS nur mit starker Verschlüsselung und ohne Klartext-Secrets;
- vollständig: nur PASS, wenn externe Roharchive und WordPress wirklich in die Kapsel eingezogen werden.

HARTE KORREKTUR:
Das bisherige V2-Kit ist ein guter Backup-Runner, aber noch **keine** geschlossene Ein-Datei-Disaster-Recovery.
Es darf deshalb nicht als TRESOR_PASS ausgegeben werden.

UMGESETZT:
- TRESOR/KONZEPT auf Ein-Datei-Ziel verschärft;
- INHALTSVERTRAG um geschlossene Kapsel, Campus-Referenzschluss, GitHub-Kollaborationshistorie und WordPress-Vollstand ergänzt;
- PRUEFVERTRAG um echten Ein-Datei-Restore ergänzt;
- NOTFALL_WIEDERAUFBAU auf „eine Datei + Masterpasswort“ als Katastrophen-Ausgangslage erweitert;
- STATUS um neue Restpunkte ergänzt.

PROVIDERGRENZE:
Nach vollständiger GitHub-Löschung können interne GitHub-Objekt-IDs beim Neuaufbau neu vergeben werden.
Original-IDs/Zeitstempel müssen im Recovery-Metadatenarchiv erhalten bleiben.

BEZUG:
ARCH-080.


### 2026-09-07 – Ein-Datei-Tresor V3 technisch vorbereitet

ZIEL:
ARCH-080 praktisch bis zur Nutzer-/WordPress-Grenze umsetzen.

KISS:
Keine neue Backup-Engine.
V3 kapselt den bereits getesteten V2-Snapshot in genau eine verschlüsselte Recovery-Datei.

KIT:
`CAMPUS_LOCAL_TRESOR_ONEFILE_KIT_20260907_V3.zip`
SHA-256:
`cab73e13c12a10e807146291521601221d05a3094660c373c95afd33e4881489`

ENTHALTEN:
- Masterpasswort-Keychain-Setup;
- privater GitHub-Tresor-Repo-Setup;
- Ein-Datei-Builder;
- GitHub-Release-Uploader;
- kombinierter Starter;
- Restore-Verifikation.

TESTGRENZE:
Shell-Syntax aller neuen Starter PASS.
Der echte AES-7z-Lauf kann erst in einer Umgebung mit installiertem 7-Zip durchgeführt werden.
Daher keine Behauptung eines kryptographischen V3-End-to-End-PASS.

BLOCKER:
- V3 auf Nutzer-Mac real ausführen;
- WordPress-Vollbackup anbinden;
- geschlossene Kapsel real erzeugen;
- isolierten Vollrestore genau dieser Datei durchführen.

TRESOR_STATUS:
weiterhin FAIL/BLOCKED.


### 2026-09-07 – Ein-Datei-Tresor V4 vollständig zum Realtest vorbereitet

AUFTRAG:
Alle nicht-destruktiven Vorbereitungen für den echten Katastrophen-/Restore-Test abschließen.

GEFUNDENE V3-LÜCKEN:
- Automatik stoppte praktisch nach dem V2-Snapshot;
- GitHub-Informationsarchiv war für Kommentare/Reviews/Release-Artefakte noch zu schmal;
- kein einheitlicher isolierter Kapsel-Restore-Test;
- WordPress-`COMPLETE.flag` war als Vollständigkeitsbeweis zu schwach.

KISS-FIX:
Keine neue Backup-Engine.
Bestehende V2/V3-Kette nur vervollständigt und härter geprüft.

V4:
- Vollautomatik: Build → isolierter Restore → erst dann Upload;
- Source-Refs dauerhaft im Snapshot;
- Git-FSCK;
- zusätzliche GitHub-Metadaten;
- Release-Artefakte;
- WordPress-Hashvertrag;
- Preflight;
- isolierter Ein-Datei-Restore;
- separates privates GitHub-Restore-Testskript.

KIT:
`CAMPUS_LOCAL_TRESOR_ONEFILE_TESTKIT_20260907_V4.zip`
SHA-256:
`83b80a7108c13d17af9d88b03c6da942e8191432106e786bc06af247cd5bae1d`

INTERN GETESTET:
- Syntax PASS;
- synthetischer Multi-Ref-Git-Restore PASS;
- WordPress positiv PASS;
- WordPress manipuliert korrekt BLOCK;
- Ein-Datei-Kontrollfluss positiv PASS;
- WordPress fehlt korrekt BLOCKED;
- beschädigte Kapsel korrekt BLOCK.

NICHT VORGETÄUSCHT:
Echter 7-Zip-AES-Lauf und echter GitHub-/WordPress-Neuaufbau brauchen die reale Nutzer-/Providerumgebung.

BEZUG:
ARCH-080; BAU-036.


### 2026-09-07 – Tresor-Bedienweg auf einen Download reduziert

NUTZERKORREKTUR:
Der Nutzer will keine Backup-Kits, Terminal-Kommandos oder Einzelarchive bedienen.
Ziel ist ausschließlich eine regelmäßig bereitgestellte Komplettsicherungsdatei.

KISS-ENTSCHEIDUNG:
- bestehender GitHub-Releases-Bereich = fester Download-Ort;
- genau eine verschlüsselte Datei je gültigem Stand;
- alte V1–V4-Kits = interne Technik, nicht Nutzerweg;
- Nutzerhandlung = nur Download + lokale Ablage.

NICHT ALS GELÖST GEMELDET:
Die automatische serverseitige Erzeugung und der vollständige WordPress-/Recovery-End-to-End-Restore sind noch nicht produktiv abgenommen.

BEZUG:
ARCH-081.


### 2026-09-07 – Serverseitigen Ein-Datei-Tresor bis zu externen Quellen vorbereitet

ZIEL:
Regelmäßige Komplettsicherung ohne Nutzerkommandos.

UMGESETZT:
- serverseitiger Builder;
- inaktiver Wochen-Workflow-Kandidat;
- Git-Mirror + Bundle + Refs;
- GitHub-Metadaten + PR-Reviews + Release-Artefakte;
- WordPress-Hashvertrag;
- opaque Recovery-Bundle;
- Roharchiv-Pflicht;
- AES256-GPG-Ein-Datei-Verschlüsselung;
- exakter Wiederentschlüsselungs-/Restore-Test;
- Release erst nach PASS;
- keine rekursive Einbettung alter Tresor-Releases.

HARD TEST:
Positiv: Multi-Ref-Git + WordPress-Testbackup + Roharchiv + Recovery-Testbundle -> Build/Decrypt/Hash/Git-Restore PASS.
Negativ: falsches Passwort BLOCK; manipulierte WordPress-Datenbank BLOCK; fehlendes Roharchiv BLOCK.

OFFEN:
echte WordPress-/Hostingquelle, serverseitige Roharchivquelle, Recovery-Bundle, Masterpasswort und Workflow-Aktivierung.

BEZUG:
ARCH-082.


### 2026-09-07 – Abschluss-/Nachholprüfung Tresor nach Nutzerweg-Korrektur

AUSLÖSER:
Universelle Abschluss-/Nachholprüfung nach Umstellung auf „eine Datei herunterladen“.

FRISCH GEPRÜFT:
- TRESOR START_HERE/STATUS/KONZEPT/INHALTSVERTRAG/PRUEFVERTRAG/LOKALES_BACKUP/NOTFALL/REALTEST;
- Archivregister;
- Fehlerregister;
- Zielvertragsregister;
- Änderungsregister + Bauänderungsindex;
- Architektur-Fehlerkiste;
- serverseitiger Builder + inaktiver Workflow-Kandidat.

GEFUNDEN UND NACHGEHOLT:
1. `BAUAENDERUNGEN.md` fehlte ARCH-081 → ergänzt.
2. Ein-Datei-Tresorziel fehlte im Zielvertragsregister → ZV-TRESOR-001 ergänzt.
3. Alter Status `ARCHIVE_RAW_ARTIFACTS_NOT_REDUNDANT` war gegenüber dem ROT-Befund zu schwach/stale → korrigiert auf `ARCHIVE_RAW_ARTIFACTS_INCOMPLETE`.
4. Nutzerweg-Fehler aus diesem Chat war noch nicht in der Architektur-Fehlerkiste → BAU-037 CLOSED ergänzt.
5. Zentraler Fehlerwegweiser um TRESOR-AUTOMATIK ergänzt, ohne Blocker zu duplizieren.
6. Aktuelles Asset-Schema auf `.tar.gz.gpg` vereinheitlicht; alte 7z-Angaben bleiben nur in historischen V3-Befunden.
7. aktuelle NEXT ACTION im TRESOR/STATUS eindeutig nachgezogen.

NICHT ERLEDIGT / KORREKT BLOCKED:
- finale Design-1.50.472-Rohartefakte fehlen;
- WordPress-Vollbackup-Provider nicht gebunden;
- serverseitige Roharchivquelle nicht gebunden;
- Recovery-Bundle/Masterpasswort nicht gebunden;
- Workflow-Kandidat nicht produktiv aktiviert;
- kein realer Gesamt-Restore der final veröffentlichten Sicherungsdatei.

EINE WAHRHEIT:
Aktueller Stand ausschließlich in `TRESOR/STATUS.md`; Register bleiben Wegweiser/Index.

BEZUG:
ARCH-080/081; BAU-036/037; ZV-TRESOR-001.


### 2026-09-07 – Backupkonzept auf einen KISS-Weg reduziert

BEDARF:
Die Tresorentwicklung war für die einfache Aufgabe „Pferde-Atelier komplett sichern“ zu komplex geworden und erzeugte mehrere technische Varianten.

ERGEBNIS:
- genau ein Backupweg;
- GitHub komplett + WordPress komplett + Projektarchiv komplett;
- ein datiertes Sicherungspaket;
- zwei unabhängige Kopien;
- wöchentlich + vor größeren Umbauten;
- BACKUP_PASS/BACKUP_FAIL;
- alte V1/V2/V3/V4-Tresorvarianten nur noch historische Entwicklungsbelege.

KISS:
Keine neue Backup-Engine. Vorhandene Git-, WordPress- und Archivtechnik wird wiederverwendet.

BEZUG:
ARCH-083.


### 2026-09-07 – Hobbyraum von Erinnerung zu technischer Integrationssperre vorbereitet

AUSLÖSER:
Der normale TEXT-Arbeitschat wich trotz dokumentierter Hobbyraumregeln wiederholt vom festgelegten Arbeitsplan ab und begann neue Prüfpfade/Minifix-Überlegungen.

HARTER BEFUND:
- `HOBBYROOM_WORK_LOCK_V1` war bereits im TEXT-Hobbyraum vorhanden;
- im technischen Security-Pfad wurde dieser Lock bisher nirgends ausgewertet;
- dadurch war er faktisch nur Dokumentation.

KISS-UMSETZUNG:
- vorhandenen `HOBBYROOM_WORK_LOCK_V1` um `TECHNICAL_SCOPE_PREFIXES` ergänzt;
- bestehenden Hobbyraum-Standard um das maschinenlesbare Schema ergänzt;
- bestehenden #137-`verify-pr`-Gate erweitert, sodass derselbe serverseitige Hardlock den Lock prüft;
- kein neuer Workflow, keine zweite Tür, kein neuer Fachprüfer.

SERVERREGEL:
Nur exakt gebundener Branch + Head + main-Basis + erlaubte Pfade + vollständige 7-Punkte-PASSes + `INTEGRATION_ALLOWED=true` kann im gebundenen technischen Scope PASS erhalten.

HARD TEST:
- Security-Head `5e0547c999a544d57e1891776f2f417e836eb605`;
- `Pferde Atelier Deterministic Entrance Gate`: SUCCESS;
- `hardlock-base`: weiterhin erwarteter FAIL an der bestehenden `IMMUTABLE_SECURITY_PATH_CHANGE_BLOCKED`-Selbstschutzgrenze.

EINE-WAHRHEIT-KORREKTUR:
TEXT-`CURRENT_STATE.md` und `HOBBYRAUM.md` enthielten noch stale Angaben `main c8a96e7…` / PR #141 nicht gemergt.
Beide wurden auf den frisch geprüften Stand `main f14ccf1…`, PR #141 MERGED und aktuellen LanguageTool-Liveblocker bereinigt.

NICHT ALS AKTIV GEMELDET:
Die neue serverseitige Hobbyraum-Sperre ist erst nach kontrollierter Aktivierung von Security-PR #137 auf main produktiv erzwungen.

BEZUG:
ARCH-084.


### 2026-09-07 – Hobbyraum-Ablauf gegen wiederholte Minifix-Schleifen gehärtet

AUSLÖSER:
Im TEXT-Arbeitschat wurden trotz vorhandener Regeln wiederholt neue Prüfpfade und Einzel-Fix-Spuren begonnen.

BEFUND:
Der maschinenlesbare Lock schützt die spätere Integration, aber der allgemeine Hobbyraum-Standard enthielt die verbindliche A–F-Arbeitsreihenfolge noch nicht ausdrücklich.

KISS-FIX:
- A–F-Pre-Fix-Ablauf in `HOBBYRAUM_STANDARD.md` verankert;
- Anti-Minifix-Regel campusweit;
- `NEUES_PROJEKT_VORLAGE.md` verweist darauf;
- keine Fachregel, Produktionsarchitektur, Tür oder Wächterlogik verändert.

BEZUG:
ARCH-085.


### 2026-09-07 – GitHub-only Backup real erneut restore-geprüft

AUSLÖSER:
Korrektur der falschen WordPress-/Projektarchiv-Erweiterung.

REALER LAUF:
GitHub Actions Run `34160894135` = SUCCESS.

EXAKTER DOWNLOAD-NACHTEST:
- Außenhash PASS;
- Innenhash PASS;
- TAR PASS;
- Bundle verify PASS;
- Mirror-Clone PASS;
- `git fsck --full --strict` PASS.

ERGEBNIS:
`GITHUB_REPOSITORY_RESTORE_PASS`.

BESTAND:
291 Branches, 1 Tag, 173 PR-Refs sowie GitHub-Kollaborations-/Release-Metadaten.

OFFEN:
Actions Variables/Permissions/Secret-Namen und Webhooks liefern mit der Workflow-Identität HTTP 403.
Der Workflow referenziert `ENDSTEMPEL_PRIVATE_KEY`; der Secret-Wert selbst ist über GitHub nicht exportierbar.

DARUM:
`GITHUB_BACKUP_PREPASS`, kein erfundener `GITHUB_KOMPLETT_PASS`.

BEZUG:
BAU-038 / ARCH-086.


### 2026-09-07 – Finaler GitHub-Snapshot extern gesichert

FINALER LAUF:
Run `34160894135`, Attempt 2 = SUCCESS.

ARTEFAKT:
`GITHUB_KOMPLETTBACKUP_2026-09-07_FINAL.zip`
SHA-256 `b885d46a9ad7f9b521677da2cc4c0abcf6d9ecbf6356b83055fc18a6c1259a25`.

REALER NACHTEST:
`GITHUB_REPOSITORY_RESTORE_PASS`.

EXTERNE KOPIE:
`/Campus-Tresor/GITHUB_KOMPLETTBACKUP_2026-09-07_FINAL.zip`.

AUTOMATIK:
wöchentlich Sonntag 03:17 Europe/Berlin; derselbe GitHub-only-Weg; bei FAIL keine Ersetzung des letzten funktionierenden Backups.

PROVIDERGRENZE BLEIBT:
Actions-Adminendpunkte 403; Secret-Werte nicht exportierbar.

DARUM:
`GITHUB_BACKUP_PREPASS`, nicht `GITHUB_KOMPLETT_PASS`.


### 2026-09-08 – Unabhängige Tresor-Automatik real eingerichtet

AUFTRAG:
Tresor soll auch dann aktuell bleiben, wenn längere Zeit kein lokales Mac-Backup ausgelöst wird.

KISS-UMSETZUNG:
- bestehender GitHub-only Tresorworkflow wiederverwendet;
- neuer Trigger nur über `control/tresor/AUTO_TRIGGER.txt`;
- wöchentlicher Scheduler Sonntag 03:17 Europe/Berlin;
- nach PASS Download des neuen Workflow-Artefakts;
- externe persistente Ablage unter `/Campus-Tresor/`;
- Pointer erst nach erfolgreichem externen Upload aktualisieren;
- alter gültiger Stand bleibt bei jedem FAIL erhalten.

REALTEST:
Trigger-Commit `25e4c462b2a93447a8ca3be68e6ae2942b4dd4b6`
→ Run `34198674940` SUCCESS
→ Artifact `10044960646`
→ äußerer/innerer Hash PASS
→ Bundle verify PASS
→ Mirror-Clone PASS
→ git fsck --full --strict PASS
→ externe Ablage PASS.

ERGEBNIS:
`TRESOR_AUTO_BACKUP_REALTEST_PASS`.

BEZUG:
ARCH-087.
