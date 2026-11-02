# PFERDE-ATELIER – BÜRO PLUGINS

<!-- CAMPUS_SINGLE_TRUTH_ENTRY_V1 -->

## ERSTER SCHRITT BEI JEDEM CHATWECHSEL: ORIGINAL TATSÄCHLICH LESEN

**Nicht bei GitHub nach einer externen Binärdatei suchen:** Laut verbindlichem `SYNC_VERTRAG.md` liegt `/Campus-Plugins/PFERDE_ATELIER/PPA-005/CURRENT.zip` im **separaten persistenten Plugin-Schrank**, während GitHub nur Steuerung und Inventar enthält.

Vor Aussagen wie „Original vorhanden“, „ich kann das Plugin lesen“, „Original aktuell geprüft“ oder vor Paketbau: die **echte vollständige ZIP im physisch verbundenen Plugin-Schrank** öffnen, alle Einträge prüfen und den SHA256 der tatsächlichen Datei gegen die geltende Current-Bindung abgleichen. Ein in GitHub eingetragener Pfad, eine SHA-Zeichenfolge, ein alter QA-Bericht oder ein erfolgreiches `--metadata-only` beweisen ausdrücklich **keinen Zugriff auf die Binärdatei**.

**Zugriffsdiagnose 02.11.2026:** In der hier verbundenen Files-Library ergab das direkte Öffnen von `/Campus-Plugins/PFERDE_ATELIER/PPA-005` die Meldung `Library path not found`. Das ist eine **fehlende Verbindung zu diesem Ablageort in diesem Arbeitskontext**, **kein** Beweis für gelöschte oder nicht existierende Originaldateien. GitHub-404 ist für diesen separaten Schrank kein Gegenbeweis. Den Standort nicht neu erfinden, keine alten ZIPs als Ersatz und keine zusätzlichen Prüfer-Plugins bauen. **Nur tatsächlichen externen Schrankzugang klären; bis zum physischen Readback kein Installer.** Bei neuem Zugriff erneut prüfen; diesen zeitbezogenen Fehler niemals als dauerhafte Aussage behandeln.

## HARD RULE – EINE CURRENT-AUTORITÄT

Diese Bürotür ist **nur Navigation**.

Pflichtweg:
`START_HERE → protocol/PROJECT_MEMORY/AUTORITAETSPLAN.json → genau eine Current-Autorität → Frischecheck → deren NEXT ACTION`.

`HOBBYRAUM.md` ist nur eine abgeleitete Ausführungsfläche und niemals Quelle für den aktuellen Status oder die NEXT ACTION.

Bei frischer unveränderter Current-Bindung: **keine Vollrekonstruktion**.
Bei belegter Änderung: **nur Delta prüfen**.



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
