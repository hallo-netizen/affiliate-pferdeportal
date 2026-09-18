# PFERDE-ATELIER – BÜRO PLUGINS

<!-- CAMPUS_SINGLE_TRUTH_ENTRY_V1 -->

## HARD RULE – EINE CURRENT-AUTORITÄT

Diese Bürotür ist **nur Navigation**.

Pflichtweg:
`START_HERE → protocol/PROJECT_MEMORY/AUTORITAETSPLAN.json → genau eine Current-Autorität → Frischecheck → deren NEXT ACTION`.

`HOBBYRAUM.md` ist nur eine abgeleitete Ausführungsfläche und niemals Quelle für den aktuellen Status oder die NEXT ACTION.

Bei frischer unveränderter Current-Bindung: **keine Vollrekonstruktion**.
Bei belegter Änderung: **nur Delta prüfen**.


STAND: 2026-09-13
STATUS: AKTIV / ERSTINVENTAR + ARTEFAKT-SYNC IM AUFBAU

## 1-KLICK-ÜBERSICHT

**WAS IST DAS?**  
Das zentrale Plugin-Büro des Pferde-Ateliers. Es hält den Überblick über alle im Pferde-Atelier verwendeten/entwickelten Plugins und deren isolierte aktuelle Ausgabeartefakte.

**HIER BIST DU RICHTIG, WENN …**  
du ein Pferde-Atelier-Plugin finden, den aktuellen isolierten Pluginstand entnehmen oder nach einer echten Pluginentwicklung/-aktualisierung den Ausgabestand synchronisieren willst.

**DU DARFST …**  
die autoritative Fach-/Releasequelle frisch lesen, daraus ein isoliertes Pluginartefakt ableiten, hashen, prüfen und im Ausgabeschrank aktualisieren.

**DU DARFST NICHT …**  
hier Fach-/Release-/LIVE-Wahrheit neu erfinden, aus alten Mastern raten, allgemeingültige Module zu Pferde-spezifischen Modulen umklassifizieren oder Secrets speichern.

**ALS NÄCHSTES …**  
`AUTORITAETSPLAN.json` → Current-Autorität → Frischecheck → NEXT ACTION → ggf. `HOBBYRAUM.md` → `REGISTER.md` → bei Artefaktarbeit `SYNC_VERTRAG.md`.

## Rolle

Das PLUGINS-Büro ist Inventar-, Update- und Ausgabepult.

Autoritative technische/Fach-/Release-/LIVE-Wahrheit bleibt immer im zuständigen Fachbüro bzw. an dessen gebundener technischer Hauptquelle.

Die physischen Plugin-ZIPs liegen persistent im zentralen Ausgabeschrank:
`/Campus-Plugins/PFERDE_ATELIER/<PLUGIN-ID>/CURRENT.zip`

Dazu liegt jeweils:
`/Campus-Plugins/PFERDE_ATELIER/<PLUGIN-ID>/MANIFEST.md`

Diese Dateien sind ausschließlich hashgebundene, abgeleitete Ausgabekopien des autoritativen Stands.

## Klassengrenze

Allgemeingültige Plugin-Kerne bleiben unter `ALLGEMEINGUELTIGE_BAUSTEINE/` autoritativ.
Eine Kopie im Pferde-Atelier-PLUGINS-Büro bedeutet nur: dieses Plugin wird im Pferde-Atelier verwendet. Sie ändert die Modulklasse nicht.

Pferde-spezifische Plugin-Kerne bleiben fachlich im jeweiligen Pferde-Atelier-Büro autoritativ.

## Harte Vorsperre

Vor jeder technischen Aktion:
`protocol/PROJECT_MEMORY/FEHLERREGISTER.md` → relevante autoritative Fehlerquelle frisch lesen.
Treffer = bekannten Fehlerweg nicht wiederholen.

## Zentrale Leitungen

- Handlungsweg: `protocol/PROJECT_MEMORY/HANDLUNGSVERZEICHNIS.md`
- Fehlerwegweiser: `protocol/PROJECT_MEMORY/FEHLERREGISTER.md`
- Warum/Änderungen: `protocol/PROJECT_MEMORY/AENDERUNGSREGISTER.md`
- Zielverträge: `protocol/PROJECT_MEMORY/ZIELVERTRAEGE/REGISTER.md`

## Abschlussregel

Wenn ein Chat tatsächlich ein Plugin entwickelt oder aktualisiert hat, muss vor Abschluss geprüft werden, ob dessen isolierte `CURRENT.zip` + `MANIFEST.md` im zentralen Ausgabeschrank auf den neuen belegten Stand synchronisiert wurden.

Kann der aktuelle Pluginstand nicht vollständig und eindeutig aus der autoritativen Quelle erzeugt/bezogen werden: nicht raten, bisherigen Stand nicht ersetzen, `Plugins: BLOCKED`.
