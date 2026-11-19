# Pferdeatelier – MINI-Texterstellung: Stand 19.11.2026, Fortsetzung

## Status, verifiziert
- Zuletzt sichtbare WordPress-Version: **Texterstellung 0.4.33 KISS** (Screenshot ca. 15:33 Uhr Europe/Berlin). Eine ältere Diagnose vom selben Tag zeigte 0.4.34; Versionen nicht vermischen.
- Aktiver gespeicherter MINI-Batch: `mini-20261119124823-5320a0031aff`.
- Aktuellster Nutzer-Wiederdownload: `texterstellung-mini-gespeicherter-auftrag(1).json`, 20 Originalthemen.
- **13 DONE (Indizes 0–12), 7 offen mit next=EDITORIAL (Indizes 13–19).** Davor waren 7 DONE, 13 offen.
- WordPress-Auftragsregal laut Screenshot: 67 Aufträge (37 IMPORTIERT, 25 METADATEN_OFFEN, 5 FREI). Zwei Pferdeanhängerartikel sind erfolgreich über K0 importiert, aber falsch kategorisiert.

## Nachweis der Unterbrechung / Ursache
- Diagnose `texterstellung-diagnose-20261119-143340.json`, `last_events`:
  - **14:28:56 UTC**: `txe_seo_import` EDITORIAL gestartet, Importdatei SHA256 `aed0e72dd9a3d74d738a364802157c35c0fb9991b421d862269c2d083cd6e581`.
  - Mehrere `STATE_COMMITTED`, aber vor dem nächsten Import **kein `ACTION_COMPLETED` für EDITORIAL**.
  - **14:29:27 UTC**: Zweiter Import TITLE gestartet, während für EDITORIAL noch keine Abschlussbestätigung protokolliert war.
  - **14:30:35 UTC**: TITLE abgeschlossen, 15 Einzel-HELD: bereits abgeschlossene Indizes 0–6 und 8 `MINI_FINAL_DECISION_ALREADY_COMPLETED`; offene 13–19 `MINI_WORKER_EDITORIAL_NOT_CHECKPOINTED`.
- Original-Code 0.4.33 `texterstellung/texterstellung.php` bei `miniWorkerCheckpoint` (ca. Zeilen 1403–1573): 20 Zeilen werden einzeln dauerhaft verarbeitet; TITLE erfordert zuvor gespeichertes EDITORIAL. Wiederholung desselben Checkpoints ist für noch offene Zeilen zulässig. Abgeschlossene Zeilen werden nicht überschrieben.
- **Sicher nachgewiesen:** EDITORIAL wurde nur teilweise gespeichert, Titelimport kam vor dessen belegtem Abschluss. **Nicht nachgewiesen:** ob Ursache des fehlenden Abschlusses Browserabbruch, Serverlimit oder etwas anderes war. Nicht raten.
- 0.4.33 blendet bei aktivem unvollständigem MINI-Batch neuen MINI-Export aus und bietet den Wiederdownload.

## KISS-Fortsetzung – keine neuen Plugins oder Recherchen
Die zwei bereits vorhandenen Rückgabedateien stimmen bezüglich ursprünglicher 20 Items, Reihenfolge und Source-Hash mit dem aktuellsten Nutzer-Wiederdownload überein; alte Daten werden nicht neu entschieden:
1. `MINI_EDITORIAL_KORREKTUR_2026-11-19.json`, SHA256 `aed0e72dd9a3d74d738a364802157c35c0fb9991b421d862269c2d083cd6e581`
2. `MINI_TITLE_KORREKTUR_2026-11-19.json`, SHA256 `8beb2338c9d0d0a44fd5a1bd083acc8ba064b31e78849dfe32a391b9f32adc62`

**Genauer Nutzer-Klickpfad:**
1. WordPress → Texterstellung → **MINI-Import** → Datei 1 **erneut importieren**. **Nicht zu Datei 2 wechseln, bevor WordPress die Abschlussmeldung „MINI-Arbeitsschritt EDITORIAL gesichert“ zeigt.** Bei nicht erscheinender Bestätigung oder Fehler: keine weiteren Importe, Bildschirm/Diagnose vorlegen.
2. Erst danach unter MINI-Import Datei 2 erneut importieren und deren Abschlussmeldung „MINI-Arbeitsschritt TITLE gesichert“ prüfen.
3. MINI-Export prüfen: neuer normaler Export sollte wieder verfügbar sein, wenn der alte Batch komplett DONE ist; sonst aktuellsten Wiederdownload ohne erneuten Eingriff hochladen.

**Besonderheit:** Die Importdateien müssen alle 20 ursprünglichen Zeilen enthalten. Das Originalplugin meldet bei Wiederimport bereits fertige Zeilen irreführend als Einzel-HELD/`MINI_FINAL_DECISION_ALREADY_COMPLETED`. Das ändert abgeschlossene Entscheidungen nicht. Relevant ist, dass Indizes **13–19** korrekt weiterlaufen. Die früher durchgeführte lokale Simulation mit Original 0.4.33 zeigte 20/20 DONE beim vollständigen Ablauf, ist aber keine Bestätigung auf Live.

## Sieben offene Themen und bereits vorbereitete Entscheidungen
13 „Soll man Pferde jeden Tag reiten?“ → FREI + Titel.
14 „Häufige Fehler bei der Fütterung“ → FREI + Titel.
15 „Ist Gurke gut für Pferde?“ → FREI + Titel.
16 „Leckstein für Pferde selbst machen“ (zweites ähnliches Thema) → KLAERUNG/Überschneidung mit Thema 10, kein neuer Titel.
17 „salzleckstein mineralleckstein pferd“ → BELEGT, bestehende Referenz WORDPRESS:973183, kein neuer Titel.
18 „mineralleckstein pferd krämer“ → FREI + Titel.
19 „Sind Minerallecksteine sinnvoll?“ → FREI + Titel.

Erwartetes Ergebnis bei komplettem Ablauf: 5 neue FREI-Aufträge, ein BELEGT, ein KLAERUNG; alle sieben im MINI abgeschlossen (KLAERUNG erzeugt bewusst keinen Artikel).

## Separater Fehler: Pferdeanhänger-Kategorien
- „Leergewicht und Zuladung beim Pferdeanhänger verstehen“, Beitrag 974848.
- „Was sollte ich beachten, wenn ich einen Pferdeanhänger miete?“, Beitrag 974849.
- Beide durch frühere Chat-Kategoriewahl in `recht-finanzen-organisation` eingeordnet; diese Entscheidung ist fachlich zu korrigieren. **Nichts in den Papierkorb verschieben oder rein manuell die Kategorie ändern**, weil WordPress-Beitrag, K0-Auftrag und gespeicherte Metadaten auseinanderlaufen können. Gesondert sicher prüfen, keine Doppelproduktion.

**Verbindliche Grenzen:** Kein Pluginwechsel, keine neuen Plugins, K0 nicht verändern, keine neue SEO-Recherche, aktiven Batch nicht löschen/zurücksetzen. Erfolg nur nach echten WordPress-Abschlussmeldungen/neuester Diagnose behaupten.


## Nutzer-Fortsetzung (19.11.2026, nach MINI-Import)
- Nutzer bestätigt: **beide empfohlenen Dateien erneut importiert („erledigt“) **.
- **Wichtig:** Es liegt noch **kein** neuer WordPress-Nachweis über vollständige Annahme oder 0 offene Themen vor; daher Status „20/20 DONE“ **nicht** behaupten.
- Angeordneter nächster Schritt: WordPress → Texterstellung → MINI-Export; prüfen, ob „MINI-Gesamtauftrag herunterladen“ wieder sichtbar ist. Falls weiterhin nur Wiederdownload: aktuellen gespeicherten MINI-Auftrag herunterladen und als JSON hier vorlegen.
- Kein erneuter Import oder Pluginwechsel bis zur Prüfung. Pferdeanhänger-Kategorien bleiben separat offen.
