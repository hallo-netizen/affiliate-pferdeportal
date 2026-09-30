# PLUGINS – HOBBYRAUM

STAND: 2026-09-30
STATUS: AKTIV / DATENBANK · PERFORMANCE · AUFRÄUMEN

## 1-KLICK-ÜBERSICHT

**WAS IST DAS?**  
Der einzige aktuelle Arbeitsraum des PLUGINS-Büros.

**HIER BIST DU RICHTIG, WENN …**  
ein konkretes Plugin inventarisiert, aktualisiert, deaktiviert, ersetzt, auf Abhängigkeiten geprüft oder als Aufräumkandidat untersucht werden soll.

**DU DARFST …**  
genau einen gebundenen Plugin-Arbeitsauftrag aufnehmen und dessen Inventar-/Update-Nachweis führen.

**DU DARFST NICHT …**  
ohne Fachbürobindung Plugins verändern, mehrere Reparaturwege parallel starten, Bewertung mit Freigabe verwechseln oder Fach-/Releasewahrheit hier duplizieren.

**ALS NÄCHSTES …**  
Bei neuem Auftrag: `CURRENT_STATE.md` → `REGELWERK.md` → `protocol/PROJECT_MEMORY/FEHLERREGISTER.md` → zuständiges Fachbüro → gebundener Arbeitsweg.

## AKTUELLE ARBEIT

Gebundener Nutzerauftrag 30.09.2026:

**Plugin für Plugin Datenbank, Performance und Aufräumen vollständig prüfen; unnötiges Wachstum nachhaltig verhindern; vorhandene Performanceoptimierungen erhalten; keine Plugin-Salami.**

Aktueller reale Betriebsstand der Kernplugins:
- Affiliate-Zentrale 6.72.165 aktiv; Storage-Housekeeping-Ersatz installiert, Performancepfade dürfen nicht verändert werden.
- PSTE 0.57.12 aktiv.
- PSERC 0.28.27 aktiv.
- PPM 6.7.9 aktiv.

Arbeitsreihenfolge:
1. PSTE vollständig gegen aktuelle Fachquelle / installierte Basis prüfen und nur einen gebündelten Datenbank-/Storage-Schritt zulassen.
2. PSERC vollständig prüfen; nur bei belegtem zusätzlichem Speicherproblem ändern.
3. PPM vollständig prüfen; kein Verdachtsfix.
4. Erst danach Altbestände der Datenbank kontrolliert bereinigen.
5. Danach physische DB-Größe und dieselbe Performance-Diagnose vorher/nachher vergleichen.

Harte Grenze:
- Affiliate bleibt während des PSTE-Blocks eingefroren.
- Kein Überschreiben oder Rückbau bereits belegter Performanceoptimierungen.
- Keywords, Topic-Pool, Recovery-/Rollbackautoritäten und aktuelle Produktionsdaten nie blind löschen.
- Kandidaten sind keine LIVE-Stände.

## PSTE-KANDIDAT 0.57.13 – HARD PASS / NOCH NICHT LIVE

Ausgangsbasis: real installiertes PSTE **0.57.12**.

Gebündelter Kandidat:
`PSTE-0.57.13-DATABASE_STORAGE_CLEANUP_PERFORMANCE_SAFE_HARD_PASS.zip`

SHA-256:
`9627705af4d934b6dcde5106476459af2f3959032da9caee2a33cc5621c22345`

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

Wichtig: Ein früherer 0.57.13-Zwischenkandidat wurde vor Installation verworfen, weil er Storage-Klassen global im Frontend lud und noch keine vollständigen Active-Work-Sperren hatte. Nur der oben hashgebundene Kandidat gilt.

## PSERC / PPM – PRÜFRESULTAT 2026-09-30

**PSERC 0.28.27:** vorhandene Generation-Retention ist bereits fail-closed und schützt aktive/Resume-/Lease-Zustände plus zwei Fallbackgenerationen. Eigene Dry-Run-Speicherwartung vorhanden. **Kein Codeupdate erforderlich.**

**PPM 6.7.9:** Datenbankfamilie aktuell klein (ca. 26,6 MB), kein belegtes unkontrolliertes Wachstum. Kritische Produktionslogik. **Kein Codeupdate auf Verdacht.**

NEXT ACTION: `INSTALL_PSTE_0_57_13_DATABASE_STORAGE_CLEANUP_PERFORMANCE_SAFE_HARD_PASS`.

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
