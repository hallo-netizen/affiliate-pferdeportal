# PFERDE-ATELIER / TECHNIK – REGELWERK

STAND: 2026-09-16
STATUS: VERBINDLICH

## Harte Regeln

1. **Nicht raten.** Vor Bereinigung immer aktuellen technischen Ist-Stand messen.
2. **Erst Analyse, dann Löschung.** Keine pauschalen Cleanup-Aktionen.
3. **Inhalt und Struktur bleiben unangetastet**, solange der Auftrag nur technischen Ballast betrifft.
4. **Backup-Dateien sind nicht Website-Inhalte.** Trotzdem nur nach eindeutiger Identifikation und bewusster Auswahl entfernen.
5. **Kein rekursives Freilöschen** durch ein Wartungsplugin, wenn der Auftrag nur einzelne Backup-Dateien betrifft.
6. **Pfad-Hardlock:** Löschwerkzeuge dürfen ausschließlich den ausdrücklich freigegebenen Ordner und Dateityp/-scope bearbeiten.
7. **Keine Symlinks, keine Pfadtraversal-Pfade, keine Unterordner** ohne eigenen Auftrag.
8. **Kein Auto-Delete.** Löschen benötigt bewusste Auswahl + Bestätigung.
9. **Nach jeder Bereinigung neu messen** und Vorher/Nachher dokumentieren.
10. **Pluginänderung = PLUGINS-Pflicht.** `../PLUGINS/START_HERE.md` + `SYNC_VERTRAG.md` beachten; isolierte `CURRENT.zip` nur mit Version, Hash und Testnachweis.
11. Lokale Tests dürfen einen erforderlichen WordPress-LIVE-Readback nicht ersetzen.
12. Keine Secrets in Campus-/Pluginartefakten.

## PPA-014-spezifische Löschgrenze

`WordPress Speicheranalyse 1.1.0` darf nur reguläre Dateien direkt unter:

`wp-content/wpvividbackups/`

löschen.

Verboten:
- Pfade außerhalb dieses Verzeichnisses;
- Unterordner;
- Symlinks;
- automatische Löschung;
- Uploads, WordPress-Core, Plugins, Themes oder Datenbankeinträge über diese Funktion.
