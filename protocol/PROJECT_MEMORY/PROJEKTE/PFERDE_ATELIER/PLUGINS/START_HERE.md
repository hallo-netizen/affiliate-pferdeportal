# BÜRO PLUGINS – PFERDE-ATELIER

STAND: 2026-09-13
STATUS: AKTIV

## 1-KLICK-ÜBERSICHT

**WAS IST DAS?**  
Inventar-, Update- und Ausgabepult für tatsächlich im Pferde-Atelier entwickelte oder aktualisierte Plugins.

**HIER BIST DU RICHTIG, WENN …**  
ein Plugin technisch geändert/aktualisiert wurde und der belastbare aktuelle Pluginstand für das Pferde-Atelier nachvollziehbar inventarisiert bzw. als isolierte Ausgabekopie synchronisiert werden muss.

**DU DARFST …**  
Pluginvorgänge dokumentieren, auf das zuständige Fachbüro verweisen und nach vollständig bestandenen Prüfungen eine hashgebundene `CURRENT.zip`-Ausgabekopie führen.

**DU DARFST NICHT …**  
eine zweite Fach-/Release-/LIVE-Wahrheit erzeugen, ungeprüfte ZIPs als CURRENT ausgeben, Versionsstände raten oder Secrets speichern.

**ALS NÄCHSTES …**  
`REGISTER.md` → `UPDATEPROTOKOLL.md` → bei Artefakten `ISOLIERTE_PLUGINS/<PLUGIN-ID>/`.

## Autoritätsgrenze

- Fach-/Release-/LIVE-Wahrheit bleibt im zuständigen Fachbüro.
- Dieses Büro führt nur Inventar, genau einen zentralen Pluginvorgang je Entwicklung/Update und die daraus abgeleitete isolierte Ausgabekopie.
- `CURRENT.zip` darf nur nach ZIP-Lesetest, Struktur-, Versions- und SHA-256-Prüfung sowie den fachlich erforderlichen Positiv-/Negativ-/Regressionstests ersetzt oder angelegt werden.
- Unterschiedliche Paketbytes benötigen unterschiedliche Pluginversionen.
- Kein `CURRENT.zip` aus Erinnerungsstand, altem Master oder ungebundenem Nebenbau.

## Artefaktpfad

`ISOLIERTE_PLUGINS/<PLUGIN-ID>/CURRENT.zip`

Zu jedem real vorhandenen `CURRENT.zip` gehört ein `MANIFEST.md` mit Plugin-ID, Name, Version, SHA-256, autoritativer Quelle, Quell-Ref/Commit, Erstellzeit und Prüfstatus.

## Aktueller erster Vorgang

Universal Glossary Engine / `MOD-008` → Fachbüro `../GLOSSAR/`.

Aktuell ist der Artefaktexport BLOCKED, weil der technisch grüne 0.2.10-rc7-Hardtest ausdrücklich **kein Paket** erzeugt hat. Siehe `UPDATEPROTOKOLL.md` → `PU-20260913-001`.
