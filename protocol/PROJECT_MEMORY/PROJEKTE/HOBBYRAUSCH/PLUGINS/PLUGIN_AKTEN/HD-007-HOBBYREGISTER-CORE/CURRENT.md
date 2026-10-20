# HD-007 – HOBBYREGISTER CORE – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-20
STATUS: **1.0.0 READ-ONLY LOCAL HARD PASS / ISOLIERTE CURRENT.ZIP-SYNC OFFEN / LIVE-INSTALLATION DANACH**

Plugin-ID:
HD-007-HOBBYREGISTER-CORE

Artefakt:
`HOBBY_DEPOT_HOBBYREGISTER_CORE_HD007_V1.0.0_READONLY_LOCALPASS.zip`

SHA-256:
`3887c914b5193f35e1ac5297fa96e2917d0d70effaae51de59501de0d3dcb8ba`

Library:
`/Hobby Depot/Plugin-Büro/HOBBY_DEPOT_HOBBYREGISTER_CORE_HD007_V1.0.0_READONLY_LOCALPASS.zip`

## Zweck

Schlanker read-only WordPress-Laufzeitkern für das **eine zentrale Hobbyregister**.

Er stellt anderen Hobby-Depot-Komponenten ausschließlich Lesezugriff bereit. Er führt keine zweite fachliche Hobby-Wahrheit: fachliche Datenautorität bleibt
`../../../WISSENSDATENBANK/CURRENT_STATE.md`
mit dem zentralen Register unter
`/Hobby Depot/Hobby-Klassifikation/HOBBY_KLASSIFIKATIONSREGISTER_V1.json`.

Die im Plugin enthaltene JSON-Datei ist eine hashgebundene Laufzeitprojektion exakt dieses geprüften Registerstands.

## Datenstand

- 862 kanonische Hobbyidentitäten;
- 54 Traits je Hobby;
- 4 Kurzprofilfelder je Hobby;
- Register-SHA-256:
  `4deb4be2b235db450d58f02485ec40e780fc2671f9dfc6edf8cbbba0f738af78`.

## Read-only API

- `hd_hobbyregister_ready()`
- `hd_hobbyregister_records()`
- `hd_hobbyregister_get($registry_id)`
- `hd_hobbyregister_get_by_name($name)`
- `hd_hobbyregister_finder_rows()`

## Harte Grenzen

- keine WordPress-DB-Writes;
- keine eigenen Tabellen;
- keine Cronjobs;
- keine Netzwerkaufrufe;
- keine Kategorie-/SEO-Strukturänderungen;
- keine Auto-Produktion;
- Design/Frontend darf nur lesen.

## Lokale QA

- PHP-Lint: **2/2 PASS**;
- Runtime-Readback: **862/862 PASS**;
- ZIP-Integrität: **PASS**;
- statischer Write-Audit: **0** Treffer für Post-/Option-/SQL-Writes;
- Scheduler/Cron: **0**;
- Netzwerkpfad: **0**.

## Integrationsbindung

Geprüfter Designkandidat:
`HD-003 1.50.704`

HD-003 liest die Finder-Daten ausschließlich über diese API. Das Design enthält keine persistente 862er-Hobbykopie.

## ISOLIERTE CAMPUS-ABLAGE

Die vorgeschriebene Ausgabekopie
`../../ISOLIERTE_PLUGINS/HD-007-HOBBYREGISTER-CORE/CURRENT.zip`
ist im Campus noch nicht vorhanden.

Der lokal vorhandene Release-ZIP wurde in der Abschlussprüfung 2026-10-20 erneut gegen den autoritativen SHA-256 geprüft und ist identisch:
`3887c914b5193f35e1ac5297fa96e2917d0d70effaae51de59501de0d3dcb8ba`.

Keine Ersatz-/Pointerdatei darf als `CURRENT.zip` ausgegeben werden.

## ERSTER OFFENER BLOCKER

**Isolierte Campus-Ausgabekopie `CURRENT.zip` + MANIFEST fehlt.**

## EXAKT EINE NEXT ACTION

**Die hash-identische HD-007-1.0.0-ZIP als `PLUGINS/ISOLIERTE_PLUGINS/HD-007-HOBBYREGISTER-CORE/CURRENT.zip` synchronisieren und das MANIFEST mit Version, SHA, Quelle und LOCAL-HARD-PASS anlegen. Erst danach WordPress-Installation/Aktivierung.**
