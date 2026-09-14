# SYSTEM 4 — PARENT-START LIVE-GAP CLOSEOUT — 2026-09-14

## Anlass

Zwei ausdruecklich freigegebene reale Codex-Ein-Artikel-Versuche haben nacheinander zwei echte Startluecken sichtbar gemacht und jeweils korrekt fail-closed gestoppt.

### Realversuch 1

`SYSTEM4_HARD_BLOCKER:PARENT_MACHINE_POINT0_NOT_PROVIDED`

Der reale Grund war eine Luecke zwischen Chat-/Elternstart und dem bisher getesteten Point-0-Einstieg.

### Realversuch 2

Nach Einfuehrung von `parent_start.py` blockierte der naechste reale Lauf mit:

`SYSTEM4_PARENT_START_FAIL:PARENT_LAUNCH_ITEMS_INVALID`

Der Parent-Start selbst funktionierte, aber Codex durfte vor dem ersten System-4-Befehl noch eine Launch-Datei aus freiem Text materialisieren. Diese Vorstufe war nicht maschinengebunden und erzeugte keine gueltige `items`-Liste.

## Ursache

Die urspruengliche Start-bis-Datei-Teststrecke begann mit vorbereiteten Metadaten-/Quellen-Fixtures. Nach dem ersten Fix wurde zwar die Parent-Start-Kante getestet, aber die reale Chat->Launch-Datei-Uebergabe lag weiterhin vor dem eigentlichen Startbefehl und damit ausserhalb der Zwangsfuehrung.

## Finale Umsetzung

`isolated_system4/parent_start.py` bleibt die einzige externe System-4-Tuer, erhaelt den Launch jetzt aber direkt als maschinengebundenen kanonischen Token.

Einziger externer Eingang:

`python3 isolated_system4/parent_start.py start-b64 <BOUND_PARENT_LAUNCH_TOKEN> <RUNTIME_ROOT_OUTSIDE_REPO>`

Der Parent-Chat/die Parent-Maschine:

- bindet exakt einen kanonischen `SYSTEM4_PARENT_LAUNCH_V1`;
- setzt `publish_allowed=false`;
- bindet Artikelmetadaten und reale HTTP(S)-Quell-URLs;
- canonicalisiert die JSON-Bytes;
- kodiert exakt diese Bytes URL-safe Base64;
- uebergibt den Token direkt im ersten System-4-Befehl.

Codex darf davor keine Launch-Datei, kein Point-0, keine Source-Evidence und keinen Hash erzeugen oder rekonstruieren.

`parent_start.py`:

- dekodiert den Token fail-closed;
- verlangt bytegenau kanonische JSON-Darstellung;
- validiert den gebundenen Launch;
- erzwingt `publish_allowed=false`;
- laedt die gebundenen HTTP(S)-Quellen selbst;
- blockiert bei HTTP-/Evidence-Fehlern;
- erzeugt Source-Evidence und SHA256 maschinell;
- baut den Produktionssnapshot;
- erzeugt PREPARED/FINAL Point-0;
- bindet aktuellen Git-Head und kritischen Manifest-Hash;
- oeffnet danach den vorhandenen Root-/Supervisor-/Worker-Dispatch-Weg.

Der alte externe Datei-CLI-Weg `parent_start.py start ...` ist gesperrt. Der interne Root-Weg bleibt ausschliesslich `root_entry.py start-point0 ...`.

`parent_start.py` ist in `root_entry.py` als kritische Manifest-Datei gebunden.

## Tests

`isolated_system4/test_parent_start.py` prueft jetzt insbesondere den **exakten ersten CLI-Befehl** mit direkt gebundenem Token.

Positiv:

- kanonischer Launch-Token -> echter HTTP-Quellenabruf -> Produktionssnapshot -> Point-0 -> Root -> Supervisor -> Worker-Dispatch.

Negativ:

- defekter/nicht-kanonischer Token;
- alter Datei-CLI-Einstieg;
- fehlende Quell-URLs;
- HTTP-Fehler;
- `publish_allowed=true`.

Vollstaendiger Workflow auf Head `6c43f09fb69af7dfe284f4dfed9665f353065c21`, Run `34874701598`: **SUCCESS**.

Dort PASS:

- Python-/Boundary-Bestand;
- kompletter System-4-Unittestbestand inkl. direktem Token-Parent-Start positiv/negativ;
- Point-0 lifecycle;
- Root/Supervisor/Worker-Dispatch;
- Maschinenbindung;
- real LanguageTool 6.8;
- real PPM 6.7.9;
- drei neue Realthemen;
- Ein-/Drei-Artikel-Start-bis-Datei-Korridor;
- Batch/V2-Handoff/Inline-Unpack/Bytegleichheit.

## Beweisgrenze / NEXT

README-/Closeout-Bereinigung und das Entfernen des unnoetigen Marker-Files erzeugen danach einen neuen finalen Test-Head. Deshalb wird der komplette Remote-Workflow auf diesem finalen Test-Head erneut ausgefuehrt.

Anschliessend wird wie zuvor ein sauberer Produktionsbranch direkt von `main` gebaut, der exakt den getesteten `isolated_system4`-Tree und `AGENTS.override.md` uebernimmt, aber keine geschuetzten `.github`-/Security-Aenderungen. Auf genau diesem Produktions-Head muss der Immutable-Base-Hardlock PASS sein.

Erst danach darf der Parent-Chat den kanonischen Launch-Token erzeugen und genau den einmalig freigegebenen realen Ein-Artikel-Codex-Lauf starten.

Kein Merge. Kein Publish. Keine Aenderung an Textmaschine, PPM, LanguageTool, Design, WordPress-Plugin oder STARTMASTER0107-LIVE.
