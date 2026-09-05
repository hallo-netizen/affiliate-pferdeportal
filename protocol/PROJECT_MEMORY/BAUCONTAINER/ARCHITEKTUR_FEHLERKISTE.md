# BAUCONTAINER – ARCHITEKTUR-FEHLERKISTE

STAND: 2026-09-05

## Zweck

Fehler des Campus, seiner Struktur und seiner Arbeitsweise werden getrennt von Fachfehlern erfasst.

Fachfehler bleiben im zentralen Fach-`FEHLERREGISTER.md`.

## Felder

- BAU-FEHLER-ID
- STATUS: OPEN / BLOCKED / CLOSED
- KURZ
- AUSWIRKUNG
- URSACHE
- KISS-FIX
- BELEG
- REGRESSIONSSCHUTZ

## BAU-001 – Doppeltes Modulregister

STATUS: CLOSED

KURZ:
Vorübergehend existierten `REGISTER.md` und `MODULREGISTER.md`.

AUSWIRKUNG:
Risiko zweier Wahrheiten.

KISS-FIX:
`REGISTER.md` entfernt; genau ein `MODULREGISTER.md`.

REGRESSIONSSCHUTZ:
Ein Modulregister = eine zentrale Navigationsquelle.

## BAU-002 – Modulklasse mit Masterakte vermischt

STATUS: CLOSED

KURZ:
Die Bildzentrale wurde vorübergehend als Modulklasse „GEMISCHT“ beschrieben.

AUSWIRKUNG:
Allgemeiner Modul-Kern und projektspezifische Masterakte wurden vermischt.

KISS-FIX:
Modulklassen nur ALLGEMEINGÜLTIG / PROJEKTBEZOGEN / UNGEKLÄRT.
„Gemischt“ gilt nur für Masterakten/Artefaktpakete.

BELEG:
ARCH-013.

## BAU-003 – Campus liegt im Pferde-Atelier-Repo

STATUS: OPEN / ARCHITEKTURENTSCHEIDUNG

KURZ:
Campus-Prototyp liegt aktuell im öffentlichen Projekt-Repository des Pferde-Ateliers.

AUSWIRKUNG:
Mehrere künftige Projekte und zentrale geschützte Akten passen logisch nicht dauerhaft unter ein einzelnes Projekt.

KISS-KANDIDAT:
Eigenes privates Campus-Repository nach V1-Freigabe.

REGEL BIS DAHIN:
Keine Secrets in den öffentlichen Prototyp.

## BAU-004 – Hausmeister durfte Fachinhalte verändern

STATUS: CLOSED

KURZ:
Der erste Hausmeisterentwurf erlaubte u. a. CURRENT_STATE zu verkürzen und HOBBYRAUM auf FREI zu setzen.

AUSWIRKUNG:
Eine reine Verwaltungsrolle hätte fachliche Wahrheit verändern können.

URSACHE:
Verwaltung und Fachpflege waren nicht hart genug getrennt.

KISS-FIX:
Hausmeister darf nur unverändert ordnen/verschieben und reine Archiv-/Verwaltungsakten pflegen.

REGRESSIONSSCHUTZ:
**Hausmeister = Verwaltung. Finger weg von Fachinhalten.**

## BAU-005 – Pförtnerrolle und Architekturarbeit vermischt

STATUS: CLOSED

KURZ:
Der Pförtner-Eingang enthielt Architektur-Sonderrecht, ohne den Rollenwechsel hart genug zu trennen.

AUSWIRKUNG:
Ein Pförtner hätte als schreibende Architekturrolle verstanden werden können.

KISS-FIX:
Pförtner = READ/ROUTE ONLY.
Architekturarbeit erst nach ausdrücklich beendetem Pförtner-Modus in der Baucontainer-Rolle.

REGRESSIONSSCHUTZ:
**Rolle bestimmt Rechte. Pförtner schreibt nichts.**

## Harte Regel

OPEN/UNGEKLÄRTE Architekturfehler werden nicht durch spontane Großumbauten gelöst.

Erst:
Fehler belegen → kleinste nachhaltige Lösung → protokollieren → prüfen.


## BAU-006 – Sonderräume ohne vollständigen 1-Klick-Eingang

STATUS: CLOSED

KURZ:
Archiv und Zielverträge hatten keinen vollständigen 1-Klick-Block; Baucontainer hatte keinen eigenen START_HERE.

KISS-FIX:
1-Klick-Eingänge ergänzt.

REGRESSIONSSCHUTZ:
EINGANGSSTANDARD gilt auch für Sonderräume.

## BAU-007 – Alltagssprache nicht explizit als Routingauftrag gebunden

STATUS: CLOSED

KURZ:
Der Trigger „Hauptpförtner.“ war definiert, natürliche Formulierungen aber nicht hart beschrieben.

KISS-FIX:
Campus START_HERE + Hauptpförtner akzeptieren eindeutige Alltagssprache als Routingauftrag.

## BAU-008 – Paul TEXT/SEO hatte keine direkte vollständige Quellenkette

STATUS: CLOSED

KURZ:
Paul-Eingang verwies allgemein auf Register, aber nicht direkt auf die sechs aktuellen TEXT-/SEO-Akten.

KISS-FIX:
Wortgleiche aktuelle Quellenkopien + `PAUL/TEXT_SEO/START_HERE.md`.

## BAU-009 – Tresorstatus war implizit statt eindeutig

STATUS: CLOSED

KURZ:
Tresorkonzept verlangte TRESOR_PASS, aber es gab weder START_HERE noch expliziten aktuellen FAIL-Status.

KISS-FIX:
`TRESOR/START_HERE.md` + `TRESOR/STATUS.md`.

WICHTIG:
Architekturlücke geschlossen; operativer TRESOR_PASS bleibt korrekt BLOCKED, bis der Prüfvertrag erfüllt ist.


## BAU-010 – Dauerakten enthielten temporäre Chat-Zustände

STATUS: CLOSED

KURZ:
Gebäude-/Büro-/Hobbyraumtexte enthielten „Sortierchat“ bzw. einen veralteten Parallelchat-Hinweis.

AUSWIRKUNG:
Ein neuer Chat/Paul konnte widersprüchliche Rechte oder veraltete Belegung lesen.

KISS-FIX:
Temporäre Chatbezüge entfernt; dauerhafte Rollen-/Arbeitsweglogik eingesetzt.

REGRESSIONSSCHUTZ:
ARCH-034 + EINGANGSSTANDARD.

## BAU-011 – Paul-Pflichtlektüre mit abgekürzten Pfaden

STATUS: CLOSED

KURZ:
Fünf Paul-Quellen waren als `.../datei.md` angegeben.

AUSWIRKUNG:
Menschlich verständlich, aber kein deterministischer 1-Klick-Weg.

KISS-FIX:
Alle fünf Pfade vollständig ausgeschrieben.

REGRESSIONSSCHUTZ:
Paul-Pfade immer vollständig; keine Ellipsen.

## BAU-012 – Hobbyraum-Zustände/Kennwort nicht zentral normiert

STATUS: CLOSED

KURZ:
„Ein Hobbyraum pro Büro“ war definiert, aber Zustände und Routing-Kennwort nicht.

KISS-FIX:
`HOBBYRAUM_STANDARD.md` mit FREI / AKTIV / BLOCKED und Routing-Kennwort „Hobbyraum“.

SICHERHEIT:
Kein Passwort; echte Rechte bleiben rollen-/branchgebunden.

## BAU-013 – Veraltete Statusduplikate in zentralen Architekturakten

STATUS: CLOSED

KURZ:
Änderungsregister nannte noch alten Tresorblocker und alten Bild-Dateilückenstatus.

KISS-FIX:
Nur den belegten aktuellen Metadatenstand nachgezogen; keine Fachbewertung ergänzt.


## BAU-014 – Direkter Büroeintritt konnte zentrale Leitungen umgehen

STATUS: CLOSED

KURZ:
Büro-START_HERE führte zwar zu Current/Hobbyraum, aber nicht überall sichtbar zu Fehler-/Änderungs-/Ziel-/Handlungsregistern.

KISS-FIX:
Einheitliche Arbeitsfreigabe an allen sechs Pferde-Atelier-Büroeingängen ergänzt.

## BAU-015 – Hobbyräume waren bei Direktlink nicht selbsterklärend

STATUS: CLOSED

KURZ:
Mehrere HOBBYRAUM-Dateien enthielten nur STATUS/FREI und keine Rechte-/Weiterweg-Erklärung.

KISS-FIX:
Alle sechs Hobbyräume mit derselben 1-Klick-Übersicht ausgestattet.


## BAU-016 – Projekt-Flur ohne Eingang

STATUS: CLOSED

KURZ:
`PROJEKTE/` war ein begehbarer Campus-Flur ohne START_HERE.

KISS-FIX:
`PROJEKTE/START_HERE.md` ergänzt.

## BAU-017 – Affiliate-Bestandsordner suggerierte durch Ablageort Allgemeingültigkeit

STATUS: CLOSED

KURZ:
`ALLGEMEINGUELTIGE_BAUSTEINE/AFFILIATE/` enthielt nur ein Inventar, obwohl Modulklasse UNGEKLÄRT ist.

KISS-FIX:
START_HERE + CURRENT_STATE mit harter UNGEKLÄRT-Kennzeichnung.

## BAU-018 – Tresor übersprang Roharchiv-Redundanz als ersten Blocker

STATUS: CLOSED

KURZ:
Tresorstatus nannte bereits Recovery-Secrets als ersten Blocker, obwohl relevante Archivrohdateien laut Archivregister noch GELB/ROT sind.

KISS-FIX:
Fail-closed auf `TRESOR_FAIL:ARCHIVE_RAW_ARTIFACTS_NOT_REDUNDANT`.


## BAU-019 – TEXT-Quellenraum ohne 1-Klick-Standard

STATUS: CLOSED

KURZ:
`TEXT/QUELLEN_AKTUELL/START_HERE.md` war als einzige von 22 Eingangstüren nicht 1-Klick-konform.

KISS-FIX:
Gleiche Adresse beibehalten und 1-Klick-Übersicht ergänzt.

REGRESSIONSSCHUTZ:
ARCH-040.


## BAU-020 – Neubauvorlage hinkte der realen Bauordnung hinterher

STATUS: CLOSED

KURZ:
NEUES_PROJEKT_VORLAGE enthielt den alten Grundstandard, aber nicht die während der Bauabnahme ergänzten Regeln.

AUSWIRKUNG:
Ein neues Projekt hätte direkte Büro-/Hobbyraum-/Flurfehler reproduzieren können.

KISS-FIX:
Vorlage auf ARCH-032 bis ARCH-040 nachgezogen.

REGRESSIONSSCHUTZ:
ARCH-041.


## BAU-021 – Ausschilderung des aktuellen Arbeitspunkts

STATUS: CLOSED

KURZ:
Die vorhandenen Quellen waren korrekt, aber der Weg zu Stand, aktueller Arbeit, Fehler und Ziel war noch zu verteilt.

KISS-FIX:
Einheitlicher Quellenwegweiser in Gebäude, Büros, Hobbyräumen, Archiv, Fehlerregister und Paul.

REGRESSIONSSCHUTZ:
ARCH-042.

## BAU-022 – Dynamische Angaben in Wegweisern

STATUS: CLOSED

KURZ:
Einzelne Wegweiser enthielten Angaben, die bereits im CURRENT_STATE oder einer Originalquelle geführt wurden.

KISS-FIX:
Wegweiser auf reine Navigation reduziert.

REGRESSIONSSCHUTZ:
ARCH-043.


## BAU-023 – Normaler TEXT-Chat wurde automatisch zu Paul geroutet

STATUS: CLOSED

KURZ:
Der TEXT-Hobbyraum führte jeden Arbeitschat direkt in den Paul-TEXT/SEO-Eingang.

AUSWIRKUNG:
Arbeitschat und Paul konnten als zwei gleichzeitige Bearbeiter desselben Problems verstanden werden. Das hätte parallele Writes, veraltete Zustände und Integrationskonflikte begünstigt.

URSACHE:
Bei der letzten Ausschilderungsvereinheitlichung wurde „Paul als gebundener Spezialworker“ fälschlich zu „Paul als normaler NEXT ACTION“ verkürzt.

KISS-FIX:
Paul aus der normalen TEXT-Navigation entfernt; Paul-Eingänge WORKER_ONLY; PROJECT_MEMORY für Paul READ ONLY; technischer Schreibbereich explizit; Integration nur durch Arbeitschat.

REGRESSIONSSCHUTZ:
ARCH-044 + ARCH-045 + EINGANGSSTANDARD + NEUES_PROJEKT_VORLAGE.


## BAU-024 – Paul-Schreibgrenze noch nicht serverseitig erzwungen

STATUS: BLOCKED / SECURITY-MAINTENANCE

KURZ:
Campus und Paul-Eingänge verbieten Paul Änderungen an `protocol/PROJECT_MEMORY/**`, aber der aktuelle main-`hardlock-base` prüft diese Worker-Grenze noch nicht technisch.

AUSWIRKUNG:
Ein fehlgeleiteter Paul-Worker könnte auf seinem Branch weiterhin PROJECT_MEMORY-Dateien committen. Die dokumentierte Regel verhindert das logisch, aber noch nicht serverseitig beim Integrationsweg.

KISS-FIX:
Eine einzige trusted-base-Diffregel in `.github/workflows/pferde-atelier-immutable-base-hardlock.yml`:
`paul/*` + `protocol/PROJECT_MEMORY/**` = `PAUL_PROJECT_MEMORY_WRITE_BLOCKED`.

BELEG:
Security-PR #137, Commit `68aaced0cb8629577c3b82f02da298b4b74fff93`.

BLOCKER:
Der bestehende immutable Base-Hardlock blockiert absichtlich jede Änderung seiner eigenen Workflow-Security mit `IMMUTABLE_SECURITY_PATH_CHANGE_BLOCKED`.
Der verfügbare GitHub-Zugriff besitzt keinen Ruleset-Admin-Write/BYPASS.

REGRESSIONSSCHUTZ NACH ADMIN-AKTIVIERUNG:
echter Positiv-/Negativtest auf main; erst danach CLOSED.


## BAU-025 – Architekturfix änderte unbelegt den aktuellen Worker

STATUS: CLOSED

KURZ:
Im Zuge der Paul-Isolation wurde der TEXT-HOBBYRAUM von einer belegten Paul-Arbeitsbindung auf `TEXT-ARBEITSCHAT FÜHRT` umgestellt, obwohl keine neue Fachzuweisung belegt war.

AUSWIRKUNG:
Die Architektur hätte selbst eine neue aktuelle Arbeitswahrheit erzeugt – genau entgegen dem Eine-Wahrheit-Prinzip.

URSACHE:
Rollen-/Routingkorrektur und dynamische Arbeitszuweisung wurden vermischt.

KISS-FIX:
Paul-Bindung als aktuellen Arbeitsstatus wiederhergestellt; nur Routing/Schreibgrenzen geändert. HOBBYRAUM_STANDARD verbietet künftig unbelegte Status-/Worker-/Branch-Umschreibungen durch Architekturarbeit.

REGRESSIONSSCHUTZ:
ARCH-049 + HOBBYRAUM_STANDARD.


## BAU-026 – Protokollpflicht war dokumentiert, aber nicht technisch erzwungen

STATUS: BLOCKED / SECURITY-MAINTENANCE

KURZ:
Campus-START_HERE und EINGANGSSTANDARD verlangen die Nachhol-/Protokollprüfung, aber ein Chat konnte trotzdem einen PR ohne diese Prüfung erzeugen.

AUSWIRKUNG:
Auch der Baucontainer selbst konnte seine eigene Dokumentationspflicht vergessen. Die Regel hing weiterhin teilweise am Chatgedächtnis.

URSACHE:
Es existierte noch kein Required-Check, der PROJECT_MEMORY-Diffs mit einer expliziten Abschlussentscheidung koppelt.

KISS-FIX:
Security-PR #137 um universellen `PROJECT_MEMORY_PROTOCOLCHECK` im bestehenden `hardlock-base` erweitert.

REGRESSIONSSCHUTZ NACH AKTIVIERUNG:
- fehlender/inkonsistenter PROTOKOLLCHECK blockiert;
- Architekturänderung ohne AENDERUNGSREGISTER + BAUPROTOKOLL blockiert;
- Tests oder Eine Wahrheit ohne PASS blockieren;
- gilt auch für Baucontainer-/Archiv-/Tresor-/Paul-/Büroänderungen.

BLOCKER:
Aktivierung benötigt denselben einmaligen Admin-Wartungsweg wie BAU-024.


### BAU-026 – TESTNACHTRAG 2026-09-05

ERSTER HARTER POSITIV-/NEGATIVLAUF:
21/22 PASS.

GEFUNDENE LÜCKE:
`ZIELVERTRAEGE/REGISTER.md` wurde nicht als Zielvertragsänderung erkannt.

FIX:
Singular- und Pluralpfad werden jetzt erkannt.

WIEDERHOLUNG:
22/22 PASS.

STATUS BLEIBT:
BLOCKED / SECURITY-MAINTENANCE – nicht wegen Logikfehler, sondern ausschließlich weil der neue trusted Check noch nicht auf main aktiviert werden kann.

NACH AKTIVIERUNG:
echte GitHub-PR-Positiv-/Negativtests bleiben Pflicht.


### BAU-026 – REAL-DIFF-NACHTRAG

Echte vorhandene PR-Diffs gegen Kandidatenlogik:
- #138 Paul + PROJECT_MEMORY → korrekt BLOCK;
- #139 Paul ohne PROJECT_MEMORY → korrekt PASS;
- #134 Campus + vollständiger PROTOKOLLCHECK → korrekt PASS.

LOGIK:
PASS.

SERVERSEITIGE ERZWINGUNG:
weiterhin BLOCKED bis Admin-Aktivierung von Security-PR #137.


## BAU-027 – Paul brauchte noch manuelle Übergabedisziplin statt automatischem Campus-Pull

STATUS: BLOCKED / SECURITY-MAINTENANCE

KURZ:
Pauls Eingang verlangte bereits frisches Lesen des Campus, aber kein technischer Mechanismus zwang ihn bei jedem Start automatisch dazu und band Branch/Scope/Frische maschinenlesbar.

AUSWIRKUNG:
Ein langer Worker-Chat hätte die Frischepflicht vergessen oder eine veraltete Branch-Kopie als Kontext verwenden können. Wiederkehrende Übergabeprompts wären als Ersatz ebenfalls fehleranfällig.

KISS-FIX:
- einzige Zuweisung = `PAUL_ASSIGNMENT_V1` im zuständigen HOBBYRAUM;
- trusted `paul_scope_gate.py start/verify`;
- automatische Verankerung in Root-`AGENTS.md` für `paul/*`;
- hardlock-base prüft aktuelle Paul-Zuweisung und Write-Scope bei Paul-PRs;
- temporäre Hash-Kapsel statt synchronisierter Zweitkopie.

POSITIVER ARCHITEKTURFALL:
Ein korrekt gebundener Auftrag mit passendem Paul-Branch/Basis/Scope darf starten.

NEGATIVE FÄLLE:
- kein aktiver Auftrag → `PAUL_NOT_ASSIGNED`;
- mehrere aktive Aufträge → `PAUL_MULTIPLE_ASSIGNMENTS_BLOCKED`;
- falscher Branch → `PAUL_BRANCH_MISMATCH_BLOCKED`;
- falsche Basis → `PAUL_BASE_MISMATCH_BLOCKED`;
- Write außerhalb Scope → `PAUL_WRITE_SCOPE_BLOCKED`;
- relevante Quellenänderung → `STALE_ASSIGNMENT_BLOCKED`.

AKTUELL:
Implementierung im Security-PR #137 vorbereitet.
Serverseitige/agentenseitige Vollaktivierung bleibt bis einmaliger Admin-Wartung BLOCKED.


### BAU-027 – TESTNACHTRAG

SELBSTTEST:
11/11 PASS.

VOLL-GIT-TEST:
9/9 erwartete Positiv-/Negativergebnisse nach einem gefundenen und behobenen Fetch-Fehler.

GEFUNDENER FEHLER:
lokaler Remote-Tracking-Ref konnte bei non-fast-forward den Frischecheck mit falscher Ursache blockieren.

FIX:
offizieller Campus wird über frisches `FETCH_HEAD` gelesen.

REALER AKTUELLER CAMPUS:
8 Hobbyräume, 0 Paul-Assignment-Marker.
Erwartetes Ergebnis für Paul aktuell:
`PAUL_NOT_ASSIGNED`.

STATUS BLEIBT:
BLOCKED / SECURITY-MAINTENANCE – ausschließlich bis Security-PR #137 kontrolliert auf main aktiviert und dort real serverseitig positiv/negativ geprüft wurde.


### BAU-027 – EXKLUSIVSCOPE-/BRANCH-NACHTRAG

Gefundene Lücke:
Nur Pauls eigenen Write-Scope zu kontrollieren verhinderte noch keinen kollidierenden normalen PR.

Fix:
Aktiver Paul-`WRITE_SCOPE` wird für alle anderen PRs technisch gesperrt.

Belege:
- Fremd-PR im Scope → `PAUL_EXCLUSIVE_SCOPE_LOCKED`;
- Fremd-PR außerhalb Scope → PASS;
- alter Paul-Branch mit Altcommit bei READ_ONLY → korrekt BLOCK;
- frischer READ_ONLY-Branch vom Base → START PASS, Write BLOCK.

Zusatzregel:
Jeder Auftrag erhält einen frischen Paul-Branch.


## BAU-028 – Tresor/Git-Mirror konnte als Arbeitsquelle missverstanden werden

STATUS: BLOCKED / SECURITY-MAINTENANCE

KURZ:
Ein Nachbarchat wollte den Campus-Tresor/Git-Mirror als lokalen Arbeitsstand nehmen und dort den Runner direkt ausführen.

AUSWIRKUNG:
Backup/Archiv hätte die offizielle aktuelle Arbeitsquelle und den gebundenen Workflow umgehen können.

URSACHE:
„nicht CURRENT“ war dokumentiert; „niemals Werkbank/Runner-Quelle“ war noch nicht explizit und technisch fail-closed.

KISS-FIX:
Campusweit READ/VERIFY/RESTORE ONLY + Arbeitsortprüfung direkt in bestehender `cloud_entry.py`.

POSITIV:
frischer normaler Git-Worktree außerhalb Tresor/Archiv mit offiziellem GitHub-origin → erlaubt.

NEGATIV:
- Worktree unter Campus-Tresor/Archiv → BLOCK;
- Bare-Mirror → BLOCK;
- außerhalb liegender Worktree mit Git-Common-Dir im Tresor → BLOCK;
- lokaler Mirror als origin → BLOCK.

STATUSGRUND:
Dokumentation umgesetzt; technische Aktivierung bleibt bis kontrollierter Aktivierung von Security-PR #137 BLOCKED.


### BAU-028 – TESTNACHTRAG

DOKUMENTATIONSABDECKUNG:
30/30 direkte Campus-Eingänge/Räume tragen den Verweis auf die globale Arbeitsort-Sperre.

SECURITY-KANDIDAT:
`hardlock` SUCCESS.

Harte Fälle im echten GitHub-Run:
- offizieller normaler Worktree → PASS;
- Campus-Tresor/Archiv-Worktree → BLOCK;
- Bare-Mirror → BLOCK;
- lokaler Mirror-origin → BLOCK;
- externer Worktree mit Tresor-Common-Gitdir → BLOCK.

LOGIK:
PASS.

STATUS BLEIBT:
BLOCKED / SECURITY-MAINTENANCE ausschließlich bis PR #137 kontrolliert auf main aktiviert und danach derselbe reale Servercheck erneut bestätigt wurde.


## BAU-029 – Paul-Quellsnapshot entfernte Rand-Whitespace

STATUS: CLOSED IM SECURITY-KANDIDAT / AKTIVIERUNG BLOCKED

KURZ:
Der neue harte Paul-Frischetest zeigte, dass `show()` über die generische Git-Hilfsfunktion Quelltext mit `.strip()` zurückgab.

AUSWIRKUNG:
Der richtige aktuelle Campus-Commit wurde zwar gelesen, aber Rand-Whitespace/Zeilenumbrüche wurden im Snapshot verändert. Eine reine Whitespace-Änderung hätte theoretisch nicht zuverlässig als relevante Drift gezählt.

KISS-FIX:
Nur `show()` auf unveränderte stdout-Rückgabe umgestellt.

NEGATIV/POSITIV:
Der erste neue GitHub-Paul-CI-Lauf FAILte.
Nach Fix kompletter Wiederholungslauf:
`PAUL_CURRENT_CAMPUS_CI_PASS` + gesamter `hardlock` SUCCESS.

REGRESSIONSSCHUTZ:
Der Paul-Frischetest ist dauerhaft Teil des Security-`hardlock`-Workflows.

STATUSGRENZE:
Fix im Security-PR #137 getestet; produktive Aktivierung auf main bleibt bis Admin-Wartung BLOCKED.


## BAU-030 – Tresor hatte Restore-Beweis, aber noch keinen vollständigen aktuellen lokalen 1:1-Snapshot

STATUS: BLOCKED / INHALTLICHE RESTPUNKTE

KURZ:
Git/GitHub-PREPASS war restore-geprüft, aber Roharchive lagen nur in der Library und der PREPASS wurde durch spätere Campusarbeit zeitlich überholt.

KISS-FIX:
- lokales Snapshotkonzept;
- kompletter aktueller Library-Export;
- Hashmanifest;
- Restorewerkzeug;
- lokaler Ein-Klick-Runner mit Git-Mirror/Bundle/Restore, Metadaten, Archivkopie und Recoveryprüfung.

HARD TEST:
- Archivexport 38/38 Restore PASS;
- korrupter Teil → BLOCK;
- lokaler Backup-Positivfall → PASS;
- fehlendes Archiv → BLOCK;
- Recovery ungeprüft → BLOCK.

OFFENE BLOCKER FÜR TRESOR_PASS:
- Nutzer muss zweite unabhängige lokale Ablage real speichern + Hash-PASS bestätigen;
- finale Design-1.50.472-Rohartefakte fehlen;
- `ENDSTEMPEL_PRIVATE_KEY`-Recovery und weitere notwendige externe Recovery-Abhängigkeiten müssen vollständig/praktisch geprüft werden.
