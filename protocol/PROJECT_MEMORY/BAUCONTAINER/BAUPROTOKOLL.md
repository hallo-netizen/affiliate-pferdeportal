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
