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

NEXT ACTION: `PSTE_0_57_12_DATABASE_PERFORMANCE_FULL_COMPATIBILITY_CHECK`.

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
