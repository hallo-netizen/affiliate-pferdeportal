# PLUGINS – HOBBYRAUM

STAND: 2026-09-30
STATUS: AKTIV / DATENBANK · PERFORMANCE · AUFRÄUMEN

## 1-KLICK-ÜBERSICHT

**WAS IST DAS?**  
Temporäre Ausführungsfläche des PLUGINS-Büros. `CURRENT_STATE.md` bleibt alleinige Current-/NEXT-ACTION-Autorität.

**HIER BIST DU RICHTIG, WENN …**  
ein konkretes Plugin inventarisiert, aktualisiert, deaktiviert, ersetzt, auf Abhängigkeiten geprüft oder als Aufräumkandidat untersucht werden soll.

**DU DARFST …**  
genau einen gebundenen Plugin-Arbeitsauftrag aufnehmen und dessen Inventar-/Update-Nachweis führen.

**DU DARFST NICHT …**  
ohne Fachbürobindung Plugins verändern, mehrere Reparaturwege parallel starten, Bewertung mit Freigabe verwechseln oder Fach-/Releasewahrheit hier duplizieren.

**ALS NÄCHSTES …**  
Bei neuem Auftrag: `CURRENT_STATE.md` → `REGELWERK.md` → `protocol/PROJECT_MEMORY/FEHLERREGISTER.md` → zuständiges Fachbüro → gebundener Arbeitsweg.

## TEMPORÄRE AUSFÜHRUNGSBINDUNG

Zielvertrag:
`protocol/PROJECT_MEMORY/ZIELVERTRAEGE/ZV-PLUGINS-CLEANUP-001.md`

Current-/NEXT-ACTION-Autorität:
`CURRENT_STATE.md`

Dieser Hobbyraum enthält nur die für die aktuell gebundene Ausführung nötigen technischen Hinweise. Ziel, Status und NEXT ACTION werden hier nicht eigenständig bestimmt.

## PSTE-KANDIDAT 0.57.13 – HARD PASS / NOCH NICHT LIVE

Ausgangsbasis: real installiertes PSTE **0.57.12**.

Gebündelter Kandidat:
`PSTE-0.57.13-DATABASE_STORAGE_CLEANUP_PERFORMANCE_SAFE_HARD_PASS.zip`

SHA-256:
`bb5f3cc84dc00fa85e2c0ddf48c8994a4788c2595c6d98f0d440780377060248`

Scope:
- verlustfreie Verdichtung von Run-Snapshots, Candidate-Payloads, Parkarchiven und record-lokalen Sandbox-Daten;
- alte unkomprimierte Daten bleiben lesbar;
- Topic-Pool und Legacy-Sandbox-Rollbackautorität bleiben unangetastet;
- kein neuer Frontend-Hook/-Filter und kein zusätzliches globales Frontend-Include;
- Storagepflege nur adminseitig, bounded, mit Active-Work-Sperren und atomarem Lock;
- separater Legacy-Restore stellt vor einem Rückfall auf 0.57.12 die alte Speicherform wieder her.

Hardtests:
- PHP-Lint **78/78 PASS**;
- Storage-Core **22/22 PASS**;
- Maintenance/Active-Work-Guards **10/10 PASS**;
- Public Storage API **8/8 PASS**;
- Rollback-Restore **17/17 PASS**;
- Restore-Mode **7/7 PASS**;
- Atomic Lock **3/3 PASS**;
- PSERC-0.28.27-Bindung PASS;
- Fresh-Unpack/Dateistruktur PASS.

Wichtig:
- Ein früherer 0.57.13-Zwischenkandidat wurde vor Installation verworfen, weil er Storage-Klassen global im Frontend lud und noch keine vollständigen Active-Work-Sperren hatte.
- Die Abschlussprüfung fand in einem weiteren vorinstallativen Paket zusätzlich eine ungewollte `.orig`-Backup-Datei. Auch dieses Paket wurde verworfen.
- Nur der oben hashgebundene Kandidat `bb5f3c...` gilt.

## PSERC / PPM – PRÜFRESULTAT 2026-09-30

**PSERC 0.28.27:** vorhandene Generation-Retention ist bereits fail-closed und schützt aktive/Resume-/Lease-Zustände plus zwei Fallbackgenerationen. Eigene Dry-Run-Speicherwartung vorhanden. **Kein Codeupdate erforderlich.**

**PPM 6.7.9:** Datenbankfamilie aktuell klein (ca. 26,6 MB), kein belegtes unkontrolliertes Wachstum. Kritische Produktionslogik. **Kein Codeupdate auf Verdacht.**

Ausführungsbindung: ausschließlich die in `CURRENT_STATE.md` aktuell gebundene NEXT ACTION ausführen. Dieser Hobbyraum erzeugt keine eigene NEXT ACTION.

## WENN EIN UPDATE BEAUFTRAGT WIRD

Der Hobbyraum bindet genau:

- Plugin-ID aus `PLUGINREGISTER.md`;
- zuständiges Fachbüro;
- beobachtete Ausgangsversion;
- Zielversion/Updatequelle;
- betroffene Abhängigkeiten;
- Test-/Rollbackweg;
- vorgesehene `PU-YYYYMMDD-NNN`-Update-ID.

Nach Abschluss wird das Update genau einmal im `UPDATEPROTOKOLL.md` protokolliert; das Fachbüro erhält nur den Rückverweis auf die PU-ID.

## STOP

Bei unklarer Zuständigkeit, unklarer Abhängigkeit, fehlendem Rollback, bekanntem Fehler-Treffer oder widersprüchlichem Versions-/Releasebeleg: **STOP / PRÜFEN**, nicht raten.
