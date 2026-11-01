# HD-003 – HOBBY DEPOT DESIGN / TEMPLATE KIT – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-11-01
STATUS: **NEUER 1.50.785-DATEIEINTRAG GEFUNDEN / ZIP-BYTES NICHT WIEDERÖFFNET / CAMPUS-CURRENT BLOCKED / LIVE OFFEN**

Plugin-ID:
`HD-003-DESIGN-TEMPLATE-KIT`

Fach-Current:
`../../../DESIGN/CURRENT_STATE.md`

Fehlerautorität:
`../../../DESIGN/FEHLERQUELLEN.md` → `HRD-078`

Historie / WAS+WARUM:
`../../UPDATEPROTOKOLL.md` → `PU-20261024-001`

## AKTUELLER BELASTBARER STAND
- letzte ältere Campus-Deklaration vom 24.10.: **1.50.744**, nicht als neue aktuelle Installationsbasis zu verwenden;
- Root-only-Ziel der Anzeigenmarkt-Startseite ist dokumentiert: Breadcrumb → Banner → eigener Anzeigenmarkt-Hero → reine Anzeigen-Suche → 8 Fotokacheln → „Aktuelle Anzeigen“ → nativer HivePress-Anzeigenbestand;
- Kategorie-/zweite Ebene bleibt vorerst nativ;
- Live-PASS für 1.50.744 liegt nicht vor.

Dokumentiertes 1.50.744-Artefakt:
`HOBBY_DEPOT_HD003_CYBERDUCK_1.50.744_ANZEIGENMARKT_STARTSEITE_HARDPASS.zip`

Dokumentierter SHA-256:
`72b048db7516640e19f4432aaf98f5d4fa6ca9cc2fd26964a421e2ac1eece6b8`

## ERSTER OFFENER BLOCKER
Die exakten 1.50.744-ZIP-Bytes sind im Abschluss-Frischecheck nicht materialisierbar. Dadurch können SHA/Fresh-Unpack nicht erneut geprüft und `ISOLIERTE_PLUGINS/HD-003-DESIGN-TEMPLATE-KIT/CURRENT.zip` nicht synchronisiert werden.

## ARBEITSBINDUNG
- keine neue HD-003-Designänderung oder Deploymentausgabe aus 1.50.744, solange das exakte Artefakt nicht wiederhergestellt ist;
- 1.50.743 ist nur letzter aktuell materialisierter ZIP-Stand, **nicht** neue Current-Autorität;
- keine Rekonstruktion auf Verdacht;
- Header/Footer-1440 und zentrale Body-Achse 1200 nicht nebenbei verändern.


## NEUER FUND / FRISCHECHECK 01.11.2026

In der vorhandenen Projekt-Dateiablage ist der tatsächliche **Dateieintrag** `/hobby rausch/HOBBY_DEPOT_HD003_1.50.785_ORIGINALLOGO_VERIFIZIERT_VOLLPLUGIN.zip` mit **63.407.568 Bytes** vorhanden. Ebenso vorhanden: die Vorversion 1.50.784 und `HOBBY_DEPOT_HD003_1.50.785_LOGO_PRUEFBERICHT.txt`. Der Bericht dokumentiert ein Favicon aus dem Originalpinselbogen und ausgeschnittenem H/D, 11/11 PHP-Lints und ZIP-Integritätsprüfung im Vorlauf, aber **keinen WordPress-Live-PASS**.

**Harte Prüfgrenze:** Die Datei wurde diesmal nicht als echte ZIP gelesen. Die Rohdatei-Bereitstellung verweigerte mit `This Project file does not have an authorized raw-byte materialization path.`; Textleseversuch meldete `No readable content was found in this file for the requested mode.`. Daher **kein neuer SHA-/ZIP-/Dateibestand-/Funktionsvergleich, keine vollständige neue Simulation**. Auch 1.50.782 wurde lediglich als GitHub-Prüfbeleg vorgefunden; dort steht ausdrücklich „Campus-ZIP noch nicht eingespielt“.

**Keine Herabstufung auf 1.50.744 oder 1.50.782, kein unechtes CURRENT.zip.** Der neueste aufgefundene Kandidat 1.50.785 bleibt bis zum echten Wiederöffnungs-/Prüf-PASS lediglich **Dateifund, nicht freigegebene Campus-Binärversion**.

## EXAKT EINE NEXT ACTION

**Die echte vollständige ZIP 1.50.785 aus einer autorisierten Rohdateiquelle wiederöffnen, ZIP-Inhalt, Version und Hash unabhängig prüfen.** Erst dann unverändert in die vorgesehene isolierte Campus-Ablage überführen und eine separate Rückfallkopie prüfen. Keine weiteren Designänderungen und keine Live-Freigabe vor diesem Nachweis.
