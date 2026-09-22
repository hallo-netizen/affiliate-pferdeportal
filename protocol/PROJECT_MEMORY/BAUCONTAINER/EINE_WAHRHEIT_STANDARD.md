# CAMPUS – STANDARD: EINE AKTUELLE WAHRHEIT

STAND: 2026-09-18
STATUS: VERBINDLICH

## Grundsatz

Für jeden abgegrenzten Arbeitsbereich gibt es **genau eine aktuelle Zustandsautorität**.

Nur diese eine Quelle darf gleichzeitig festlegen:
- aktuellen belastbaren Stand;
- aktuellen Status;
- ersten offenen Blocker/Fehler;
- **genau eine NEXT ACTION**;
- dynamische Branch-/Head-/Run-Bindungen, soweit sie für die aktuelle Ausführung nötig sind.

Welche Quelle für einen Bereich zuständig ist, wird ausschließlich in
`protocol/PROJECT_MEMORY/AUTORITAETSPLAN.json`
geroutet.

Der Autoritätsplan enthält **keinen Fachstatus**. Er beantwortet nur die Frage:
**Wo liegt die eine aktuelle Wahrheit?**

## Rollen – strikt getrennt

- `START_HERE.md`, Hauptpförtner, Gebäude-, Flur-, Archiv- und Tresortüren = **Navigation only**.
- Current-Autorität = **einzige aktuelle Stand-/Blocker-/NEXT-ACTION-Wahrheit**.
- `HOBBYRAUM.md` = **DERIVED_EXECUTION_SURFACE**, kein zweiter Current.
- Task-/Jobdatei = ausführbarer Auftrag, kein Current.
- Evidence/Testreport = Nachweis, kein Current.
- Fehlerquelle = Fehlerdetails, kein allgemeiner Current.
- Zielvertrag = Ziel-/Regelautorität, kein allgemeiner Current.
- Protokoll/AENDERUNGSREGISTER = Historie/WAS/WARUM, kein Current.
- Übergabe im Chat = Navigation auf diese Quellen, kein Current.

## Einstieg eines neuen Chats

Pflichtweg:

`START_HERE → AUTORITAETSPLAN → genau eine Current-Autorität → Frischecheck → NEXT ACTION`

Erst **wenn die Current-Autorität selbst** eine Ausführungsfläche bindet:
`→ HOBBYRAUM/Task/Runner`.

Ein neuer Chat darf weder Hobbyraum noch Übergabe noch Protokoll als Ersatz für die Current-Autorität verwenden.

## Frischecheck ohne Vollrekonstruktion

HARD RULE:

`NO_FULL_REDISCOVERY_IF_CURRENT_BINDING_FRESH`

Wenn die in der Current-Autorität gebundene technische Quelle/Generation/Manifest-/Run-Bindung frisch und unverändert ist:
- **kein Repository-Vollscan**;
- keine Historienrekonstruktion;
- keine alten Übergaben neu lesen;
- keine alten Plugins/Branches vergleichen;
- direkt die gebundene NEXT ACTION ausführen.

Bei belegter Änderung:

`ON_BINDING_CHANGE_INSPECT_DELTA_ONLY`

Dann nur die Änderung seit der letzten gebundenen Basis prüfen und Current-Autorität nachziehen. Vollrekonstruktion nur, wenn die Autoritätskette selbst beschädigt oder nicht bestimmbar ist.

## Hobbyraum / Maschinenlocks

Bestehende `PAUL_ASSIGNMENT_V1`- und `HOBBYROOM_WORK_LOCK_V1`-Blöcke dürfen als **abgeleitete technische Sperren** bestehen bleiben.

Sie erzeugen keine Statuswahrheit.

Pflicht:
- sie müssen auf die zuständige Current-Autorität verweisen bzw. an sie hashgebunden sein;
- bei Abweichung: **BLOCKED / STALE EXECUTION BINDING**;
- sie dürfen Current-Status, Blocker oder NEXT ACTION niemals überschreiben;
- ein neuer Chat bestimmt den Stand nie aus dem Lock.

## Spezialfall technische Hauptautorität

Existiert für einen Bereich bereits eine technisch erzwungene Current-Autorität, wird **keine Campus-Kopie** als zweiter Current gepflegt.

Beispiel AFFILIATE:
`control/release-governance/CURRENT_RELEASE.json`
ist die Current-Autorität. Eine Campus-Datei darf dort nur statisch hinweisen.

## Übergaben

Eine Übergabe darf nur enthalten:
- Scope/Büro;
- Pfad zum Autoritätsplan;
- Pfad zur zuständigen Current-Autorität;
- Frischecheck-Methode;
- optional gebundene Ausführungsfläche.

Sie darf **keinen eigenen aktuellen Status, Head, Blocker oder NEXT ACTION** als zweite Wahrheit konservieren.

## Negativregeln

Verboten:
- Status in Current und Hobbyraum parallel pflegen;
- NEXT ACTION in Current und Hobbyraum parallel pflegen;
- aktuelle Branch-/Head-/Run-Werte in START_HERE oder Übergaben kopieren;
- eine `HANDOFF.current.*` als zweite Current-Datei;
- eine abgeleitete Plugin-`CURRENT.zip` zur Fach-/Release-Wahrheit erklären;
- Protokoll oder Archiv als aktuelle Wahrheit verwenden.

## Neue Büros / Projekte

Neue Campusbereiche dürfen nur angelegt werden, wenn der Autoritätsplan genau eine Current-Autorität benennt.
Die Neubauvorlage muss diesen Standard übernehmen.
