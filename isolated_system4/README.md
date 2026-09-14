# SYSTEM 4 — TRUE SINGLE ROOM

Status: **REMOTE-TESTKANDIDAT MIT DIREKT GEBUNDENEM PARENT-START-TOKEN — REALER CODEX-LAUF HAT ZWEITE LIVE-LUECKE AUFGEDECKT UND FAIL-CLOSED GESTOPPT — FIX IST REMOTE VOLLSTAENDIG PASS — SEPARATER LOKALER NACHWEIS FUER GENAU EINEN REALEN CODEX-VERSUCH VOM NUTZER AUSNAHMSWEISE UEBERSPRUNGEN — KEIN MERGE / KEIN PUBLISH.**

Diese Datei ist die **eine aktuelle System-4-Statuswahrheit**. Der offizielle Campus-/Projektstand bleibt getrennt und ausschließlich in `control/startmaster0107/CURRENT_STATE.json`.

## Aktueller Kandidat

Branch: `hobbyroom/system4-point0-supervisor-rebuild-v1`

Kein Merge. Kein Publish. `publish_allowed=false`.

## Geschlossene Live-Startluecken

### 1. Fehlender Parent -> Point-0-Weg

Der erste reale Codex-Versuch blockierte korrekt vor Root mit:

`SYSTEM4_HARD_BLOCKER:PARENT_MACHINE_POINT0_NOT_PROVIDED`

Ursache: Der alte sogenannte Start-bis-Datei-Test begann mit bereits vorbereiteten Metadaten-/Quellen-Fixtures. Die reale Strecke vom Eltern-/Chat-Start bis zur maschinellen Point-0-Erzeugung war nicht bewiesen.

Dafuer wurde `isolated_system4/parent_start.py` eingefuehrt. Die Maschine beschafft/verifiziert gebundene HTTP(S)-Quellen selbst, erzeugt Produktionssnapshot und Point-0 und oeffnet erst danach Root/Supervisor/Worker-Dispatch.

### 2. Freie Launch-Datei vor dem ersten Befehl

Der danach gestartete reale Ein-Artikel-Codex-Lauf auf dem sauberen Produktionskandidaten blockierte erneut korrekt, diesmal bereits im Parent-Start:

`SYSTEM4_PARENT_START_FAIL:PARENT_LAUNCH_ITEMS_INVALID`

Ursache: Obwohl der Parent-Start selbst existierte, durfte Codex vor dem ersten Befehl noch eine Launch-Datei aus dem Chat-Auftrag materialisieren. Genau diese freie Uebergabe erzeugte keine gueltige `items`-Liste. Damit lag weiterhin ein unbeaufsichtigter Uebergabeschritt vor dem eigentlichen Startknopf.

Dieser freie Schritt ist jetzt entfernt. Der Eltern-/Chatprozess bindet das komplette kanonische `SYSTEM4_PARENT_LAUNCH_V1` selbst und uebergibt dessen URL-safe-Base64-Darstellung direkt im ersten System-4-Befehl. Codex baut, interpretiert oder materialisiert davor keine Launch-Datei mehr.

## Einziger externer Produktionsstart

`python3 isolated_system4/parent_start.py start-b64 <BOUND_PARENT_LAUNCH_TOKEN> <RUNTIME_ROOT_OUTSIDE_REPO>`

Der Token muss beim Decodieren exakt kanonische JSON-Bytes ergeben. Nicht-kanonische, defekte oder manipulierte Tokens blockieren vor Runtime-Erzeugung.

Der Parent-Start erhaelt weiterhin keine vorbereitete Point-0-Datei und keine vorbereiteten Source-Evidence-/Hashwerte. Er beschafft und verifiziert die gebundenen HTTP(S)-Quellen selbst, erzeugt Produktionssnapshot und Point-0 und oeffnet erst danach den internen Root-Eingang.

Der interne Root-Eingang bleibt:

`python3 isolated_system4/root_entry.py start-point0 <POINT0_OUTSIDE_REPO> <WORKSPACE_OUTSIDE_REPO>`

`start` und `start-stdin` bleiben dort fail-closed gesperrt.

## Verbindliche Zielarchitektur

Aktueller Zielvertrag:
`ZIELVERTRAG_SYSTEM4_MACHINE_POINT0_CODEX_WRITER_20260914.md`

Kette:

`Chat/Parent bindet Launch-Token -> erster start-b64-Befehl -> maschinelle Quellenbeschaffung/-verifikation -> PREPARED Point-0 -> FINAL Point-0 -> Root -> Supervisor -> Worker-Start -> Research -> Facts -> maschinengebundener Context/Authoring-Contract -> Worker-Draft -> echtes LanguageTool 6.8 -> echter PPM 6.7.9 -> Batch -> V2-Handoff -> Inline-Unpack -> bytegleiche Datei`

Codex/Worker besitzt weder Route noch Links noch Kategorie noch Slot noch PASS. Freie Websuche im Worker ist gesperrt; Research darf nur aus dem gebundenen Source-Pool kommen.

## Hart bewiesene Grenzen

Der vollstaendige Workflow Run `34874701598` auf Head `6c43f09fb69af7dfe284f4dfed9665f353065c21` war **SUCCESS** und bewies:

- exakter erster externer `start-b64`-Befehl positiv;
- defekter/nicht-kanonischer Launch-Token blockiert;
- alter Datei-basierter CLI-Einstieg `start` blockiert;
- fehlende Quellen blockieren vor Runtime-Erzeugung;
- HTTP-Fehler blockieren vor Root-Workspace;
- `publish_allowed=true` blockiert vor Runtime-Erzeugung;
- Point-0 PREPARED -> FINAL Quellenbindung;
- Root / Supervisor / Worker-Dispatch / Artikelindex;
- Maschinenbindung von Kategorie, drei internen Links und Quality-Binding;
- komplette bestehende System-4-Suite;
- exakter LanguageTool-6.8-Bestand 43;
- echter LanguageTool-6.8-/PPM-6.7.9-Korridor;
- drei neue Realthemen;
- Ein- und Drei-Artikel-Start-bis-Datei-Korridor;
- Batch / V2-Handoff / Inline-Unpack / SHA- und Bytegleichheit.

Diese README-/Protokollaktualisierung veraendert danach den Head, nicht aber die Runtime-Logik. Vor dem naechsten realen Codex-Lauf muss der vollstaendige Remote-Workflow trotzdem wieder auf exakt dem finalen Test-Head PASS sein. Danach wird wie zuvor ein sauberer Produktionsbranch direkt von `main` mit bytegleichem `isolated_system4`-Tree und `AGENTS.override.md` gebaut und dort der Immutable-Base-Hardlock auf exakt demselben Head verlangt.

## Nutzer-Ausnahme fuer genau einen Realversuch

Der separate lokale Container-/Arbeitsplatzlauf kann in der aktuellen Chat-Containerumgebung wegen fehlendem GitHub-DNS/Netzzugriff nicht ausgefuehrt werden. Der Nutzer hat am 14.09.2026 ausdruecklich freigegeben, diese lokale Zusatzkontrolle fuer **genau einen** realen Codex-Artikel zu ueberspringen.

Diese Ausnahme aendert keine Architektur, keinen Checker und keine Fachregel. Sie erlaubt weder Merge noch Publish.

## HOBBYRAUM / NEXT ACTION

1. Vollstaendigen Remote-Workflow auf dem finalen Test-Head erneut PASS nachweisen.
2. Sauberen Produktionsbranch direkt von `main` mit exakt bytegleichem `isolated_system4`-Tree + `AGENTS.override.md` erzeugen; keine geschuetzten `.github`-/Security-Aenderungen uebernehmen.
3. Immutable-Base-Hardlock auf exakt diesem sauberen Produktions-Head PASS nachweisen.
4. Den gebundenen Launch-Token im Parent-Chat erzeugen und genau **einen** realen Codex-Artikel starten. Codex darf vor dem ersten `start-b64`-Befehl keine Launch-Datei oder andere Startartefakte erzeugen.
5. Bei erstem echten nicht-reparierbaren Fehler fail-closed stoppen. Repair nur innerhalb des vorhandenen Same-Article-Vertrags.
6. Bei PASS Batch Count=1, V2-Handoff, Inline-Unpack und Bytegleichheit nachweisen.
7. Kein Merge. Kein Publish.

NICHT ANFASSEN:
- STARTMASTER0107-LIVE-Wahrheit;
- Textmaschine;
- PPM 6.7.9;
- LanguageTool 6.8;
- Design / WordPress-Plugin / Theme;
- bestehende Portal-/Metadaten-/Linkregeln;
- gesperrte Legacy-Eingaenge.
