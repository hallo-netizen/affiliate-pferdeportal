# SYSTEM 4 — TRUE SINGLE ROOM

Status: **REMOTE-TESTKANDIDAT MIT REALER PARENT-START-KANTE PASS — SEPARATER LOKALER NACHWEIS FUER GENAU EINEN REALEN CODEX-VERSUCH VOM NUTZER AUSNAHMSWEISE UEBERSPRUNGEN — REALER CODEX-LAUF AUF DIESEM KANDIDATEN NOCH NICHT AUSGEFUEHRT — KEIN MERGE / KEIN PUBLISH.**

Diese Datei ist die **eine aktuelle System-4-Statuswahrheit**. Der offizielle Campus-/Projektstand bleibt getrennt und ausschließlich in `control/startmaster0107/CURRENT_STATE.json`.

## Aktueller Kandidat

Branch: `hobbyroom/system4-point0-supervisor-rebuild-v1`

Kein Merge. Kein Publish. `publish_allowed=false`.

## Real geschlossene Startluecke

Der erste reale Codex-Versuch nach dem bisherigen Remote-PASS blockierte korrekt noch vor Root mit:

`SYSTEM4_HARD_BLOCKER:PARENT_MACHINE_POINT0_NOT_PROVIDED`

Die Ursache war eine echte Testluecke: der bisher als Start-bis-Datei bezeichnete Test startete mit bereits vorbereiteten Metadaten-/Quellen-Fixtures und bewies die Strecke vom Eltern-/Chat-Start bis zur maschinellen Point-0-Erzeugung nicht.

Diese Luecke ist jetzt technisch geschlossen. Der einzige externe Produktionsstart ist:

`python3 isolated_system4/parent_start.py start <PARENT_LAUNCH_OUTSIDE_REPO> <RUNTIME_ROOT_OUTSIDE_REPO>`

Der Parent-Start erhaelt keine vorbereitete Point-0-Datei und keine vorbereiteten Source-Evidence-/Hashwerte. Er beschafft und verifiziert die gebundenen HTTP(S)-Quellen selbst, erzeugt Produktionssnapshot und Point-0 und oeffnet erst danach den internen Root-Eingang.

Der interne Root-Eingang bleibt:

`python3 isolated_system4/root_entry.py start-point0 <POINT0_OUTSIDE_REPO> <WORKSPACE_OUTSIDE_REPO>`

`start` und `start-stdin` bleiben dort fail-closed gesperrt.

## Verbindliche Zielarchitektur

Aktueller Zielvertrag:
`ZIELVERTRAG_SYSTEM4_MACHINE_POINT0_CODEX_WRITER_20260914.md`

Kette:

`ein Parent-Startknopf -> maschinelle Quellenbeschaffung/-verifikation -> PREPARED Point-0 -> FINAL Point-0 -> Root -> Supervisor -> Worker-Start -> Research -> Facts -> maschinengebundener Context/Authoring-Contract -> Worker-Draft -> echtes LanguageTool 6.8 -> echter PPM 6.7.9 -> Batch -> V2-Handoff -> Inline-Unpack -> bytegleiche Datei`

Codex/Worker besitzt weder Route noch Links noch Kategorie noch Slot noch PASS. Freie Websuche im Worker ist gesperrt; Research darf nur aus dem gebundenen Source-Pool kommen.

## Hart bewiesene Grenzen

Auf dem Parent-Start-Kandidaten wurden remote tatsaechlich ausgefuehrt und bestanden:

- Parent-Start positiv: externer Launch -> Quellenabruf -> Produktionssnapshot -> Point-0 -> Root/Supervisor/Worker-Dispatch;
- Parent-Start negativ: fehlende Quellen, HTTP-Fehler und `publish_allowed=true` blockieren vor Worker-Produktion;
- Point-0 PREPARED -> FINAL Quellenbindung;
- Root / Supervisor / Worker-Dispatch / Artikelindex;
- Maschinenbindung von Kategorie, drei internen Links und Quality-Binding;
- Single-Button Positiv-/Negativstrecke;
- Hard-Block verbotener Provider-Abhaengigkeiten;
- komplette bestehende System-4-Suite;
- exakter LanguageTool-6.8-Bestand 43;
- echter LanguageTool-6.8-/PPM-6.7.9-Korridor;
- drei neue Realthemen;
- Ein- und Drei-Artikel-Start-bis-Datei-Korridor;
- Batch / V2-Handoff / Inline-Unpack / SHA- und Bytegleichheit.

Der letzte vollstaendige Remote-Workflow vor dieser reinen Statusaktualisierung war Run `34873370940` auf Head `3a27a7b701b4225527174af09e6cd43c067025df` mit `conclusion=success`. Da diese README-Aktualisierung den Head veraendert, muss der gleiche Workflow auf dem neuen Head erneut PASS sein, bevor der neue Head als Produktionskandidat gilt.

## Nutzer-Ausnahme fuer genau einen Realversuch

Der separate lokale Container-/Arbeitsplatzlauf kann in der aktuellen Chat-Containerumgebung wegen fehlendem GitHub-DNS/Netzzugriff nicht ausgefuehrt werden. Der Nutzer hat am 14.09.2026 ausdruecklich freigegeben, diese lokale Zusatzkontrolle fuer **genau einen** realen Codex-Artikel zu ueberspringen.

Diese Ausnahme aendert keine Architektur, keinen Checker und keine Fachregel. Sie erlaubt weder Merge noch Publish und gilt nicht automatisch fuer weitere Produktionslaeufe.

## HOBBYRAUM / NEXT ACTION

1. Vollstaendigen Remote-Workflow auf dem durch diese Statusaktualisierung entstandenen neuen Head erneut PASS nachweisen.
2. Draft-PR fuer exakt `hobbyroom/system4-point0-supervisor-rebuild-v1` verwenden; PR #238 zeigt auf einen anderen Branch und ist kein gueltiger Codex-/Hardlock-Einstieg fuer diesen Kandidaten.
3. Immutable-Base-Hardlock auf exakt demselben Head nachweisen.
4. Danach genau **einen** neuen real gebundenen Codex-Artikel ueber `parent_start.py` starten.
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
