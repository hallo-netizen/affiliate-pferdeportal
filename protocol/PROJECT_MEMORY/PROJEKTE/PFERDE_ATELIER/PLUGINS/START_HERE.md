# BÜRO PLUGINS – PFERDE-ATELIER

STAND: 2026-09-14
STATUS: AKTIV

## 1-KLICK-ÜBERSICHT

**WAS IST DAS?**  
Inventar-, Update- und Ausgabepult für tatsächlich im Pferde-Atelier entwickelte oder aktualisierte Plugins.

**HIER BIST DU RICHTIG, WENN …**  
ein Plugin technisch geändert/aktualisiert wurde und der belastbare Pluginstand nachvollziehbar inventarisiert bzw. – nur bei erfüllter Artefaktpflicht – als isolierte Ausgabekopie synchronisiert werden muss.

**DU DARFST …**  
Pluginvorgänge dokumentieren, auf das zuständige Fachbüro verweisen und nach vollständig bestandenen Prüfungen eine hashgebundene `CURRENT.zip`-Ausgabekopie führen.

**DU DARFST NICHT …**  
eine zweite Fach-/Release-/LIVE-Wahrheit erzeugen, ungeprüfte ZIPs als CURRENT ausgeben, Versionsstände raten oder Secrets speichern.

**ALS NÄCHSTES …**  
`REGISTER.md` → `UPDATEPROTOKOLL.md` → bei Artefakten `ISOLIERTE_PLUGINS/<PLUGIN-ID>/`.

## Autoritätsgrenze

- Fach-/Release-/LIVE-Wahrheit bleibt im zuständigen Fachbüro.
- `REGISTER.md` ist Inventar/Wegweiser, kein CURRENT_STATE.
- `UPDATEPROTOKOLL.md` führt genau einen zentralen Vorgang je realer Entwicklung/Update.
- `CURRENT.zip` ist nur eine abgeleitete Ausgabekopie.
- Unterschiedliche Paketbytes benötigen unterschiedliche Pluginversionen bzw. einen eindeutig gebundenen Buildstand.
- Kein `CURRENT.zip` aus Erinnerungsstand, altem Master oder ungebundenem Nebenbau.

## Artefaktpfad

`ISOLIERTE_PLUGINS/<PLUGIN-ID>/CURRENT.zip`

Zu jedem real vorhandenen `CURRENT.zip` gehört ein `MANIFEST.md` mit Plugin-ID, Name, Version, SHA-256, autoritativer Quelle, Quell-Ref/Commit, Erstellzeit und Prüfstatus.

## Artefakt-Gate

`CURRENT.zip` darf nur angelegt/ersetzt werden, wenn gleichzeitig belegt sind:
- exakte autoritative Quelle / Quell-Ref / Releasequelle;
- ZIP-Lesetest und Strukturprüfung;
- Versionsprüfung;
- SHA-256-Prüfung;
- erforderliche Positivprüfung;
- erforderliche Negativ-/Mutationprüfung;
- Fach-/Regressionstest;
- kein aktuell bekannter blockierender LIVE-/Releasefehler, soweit für den Stand erforderlich.

Fehlt einer dieser Belege, bleibt die bestehende Ausgabekopie unverändert und der Vorgang wird `BLOCKED` dokumentiert.

## Eine Wahrheit

Dynamische Pluginstände stehen ausschließlich in `REGISTER.md`/`UPDATEPROTOKOLL.md` und den dort verlinkten Fachquellen. Diese Eingangstür kopiert bewusst keine aktuelle Version, keinen aktuellen Head und keinen aktuellen Blocker.
