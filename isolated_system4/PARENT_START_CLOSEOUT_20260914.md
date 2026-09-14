# SYSTEM 4 — PARENT-START LIVE-GAP CLOSEOUT — 2026-09-14

## Anlass

Ein ausdruecklich freigegebener realer Codex-Ein-Artikel-Versuch blockierte vor Root mit:

`SYSTEM4_HARD_BLOCKER:PARENT_MACHINE_POINT0_NOT_PROVIDED`

Der reale Grund war eine Luecke zwischen Chat-/Elternstart und dem bisherigen getesteten Point-0-Einstieg.

## Ursache

Die bisherige als Start-bis-Datei bezeichnete Teststrecke erzeugte Produktionsmetadaten und Quellen bereits ueber Test-Fixtures. Dadurch war nicht bewiesen, dass der reale Elternprozess selbst aus dem gebundenen Startauftrag Quellen beschafft/verifiziert, Produktionssnapshot und Point-0 erzeugt und Root oeffnet.

## Umsetzung

Neu: `isolated_system4/parent_start.py`.

Externer Eingang:

`python3 isolated_system4/parent_start.py start <PARENT_LAUNCH_OUTSIDE_REPO> <RUNTIME_ROOT_OUTSIDE_REPO>`

Der Parent-Start:

- validiert den gebundenen Launch;
- erzwingt `publish_allowed=false`;
- laedt die gebundenen HTTP(S)-Quellen selbst;
- blockiert bei HTTP-/Evidence-Fehlern;
- erzeugt Source-Evidence und SHA256 maschinell;
- baut den Produktionssnapshot;
- erzeugt PREPARED/FINAL Point-0;
- bindet aktuellen Git-Head und kritischen Manifest-Hash;
- oeffnet danach den vorhandenen Root-/Supervisor-/Worker-Dispatch-Weg.

`parent_start.py` ist in `root_entry.py` als kritische Manifest-Datei gebunden.

## Tests

Neue Positiv-/Negativregression: `isolated_system4/test_parent_start.py`.

Nach zwei real gefundenen Integrationsfehlern wurden nur deren Ursachen korrigiert:

1. veraltete Root-Override-Textbindung;
2. falscher erwarteter Supervisor-Artefaktname im neuen Test sowie Erhalt einer bestehenden harten Legacy-Start-Wortlautregression.

Danach vollständiger Workflow auf Head `3a27a7b701b4225527174af09e6cd43c067025df`, Run `34873370940`: **SUCCESS**.

Dort PASS:

- Point-0 lifecycle;
- Root/Supervisor/Worker-Dispatch;
- Maschinenbindung;
- Negativgrenzen;
- komplette System-4-Suite einschliesslich Parent-Start positiv/negativ;
- real LanguageTool 6.8;
- real PPM 6.7.9;
- drei neue Realthemen;
- Ein-/Drei-Artikel-Start-bis-Datei-Korridor.

## Beweisgrenze

Nach dieser Protokolldatei und der README-Aktualisierung entsteht ein neuer Head. Daher gilt fuer den neuen Head erneut: Remote-Workflow und PR-gebundener Immutable-Base-Hardlock muessen auf exakt demselben Head PASS sein, bevor der einmalig freigegebene reale Codex-Artikel gestartet wird.

Kein Merge. Kein Publish. Keine Aenderung an Textmaschine, PPM, LanguageTool, Design, WordPress-Plugin oder STARTMASTER0107-LIVE.
