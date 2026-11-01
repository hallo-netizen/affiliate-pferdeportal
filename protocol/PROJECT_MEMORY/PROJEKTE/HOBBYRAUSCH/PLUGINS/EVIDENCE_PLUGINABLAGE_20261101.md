# HOBBY DEPOT – Nachholprüfung des gesamten Plugin-Büros
**Datum:** 2026-11-01  
**Rolle:** Prüfbeleg, keine zweite Current- oder Freigabeautorität  
**Gesamtergebnis:** **PLUGINABLAGE: BLOCKED**

## Geprüfte verbindliche Quellen
- `PROJEKTE/HOBBYRAUSCH/START_HERE.md` und `PROJECT_MEMORY/AUTORITAETSPLAN.json`.
- Technischer Plugin-Routing-Current: `PLUGINS/CURRENT_STATE.md`.
- Einzelstände: `PLUGINS/PLUGIN_AKTEN/<PLUGIN-ID>/CURRENT.md`.
- Isolierte Campus-Byte-Ziele: `PLUGINS/ISOLIERTE_PLUGINS/<PLUGIN-ID>/CURRENT.zip`.
- Das separate Library-Büro `/Hobby Depot/Plugin-Büro` wurde geprüft, gilt aber **nicht als Ersatz** für Campus-Pluginablage.

## Vollständiger Inventarabgleich (geprüfte Campus-Current-Akten)
| Akte | Version aus der Einzel-Current / jüngster belegter Kandidat | Exakte Campus-Byte-Lage | Readback in diesem Lauf |
|---|---|---|---|
| HD-001 Kategorie-Workflow | 1.14.16 | Nur MANIFEST; CURRENT.zip fehlt | Nicht durchgeführt |
| HD-002 SEO Themenengine | 0.1.4 | Kein isolierter Zielordner vorhanden | Nicht durchgeführt |
| HD-003 Design | Ältere Campusdeklaration 1.50.744; neuer Library-Dateifund 1.50.785 | Nur MANIFEST; CURRENT.zip fehlt | 1.50.785-Raw-Zugriff verweigert |
| HD-004 Kategorie-Kern | 1.0.0 | Nur MANIFEST; CURRENT.zip fehlt | Nicht durchgeführt |
| HD-005 Glossar Core | 1.0.25 | Nur MANIFEST; CURRENT.zip fehlt | Nicht durchgeführt |
| HD-006 Bildzentrale | 2.7.8 | Nur MANIFEST; CURRENT.zip fehlt | Nicht durchgeführt |
| HD-007 Hobbyregister Core | 1.2.16 | Nur MANIFEST; CURRENT.zip fehlt | Nicht durchgeführt |
| HD-008 SEO-Metadaten | 1.0.0 | Nur MANIFEST; CURRENT.zip fehlt | Nicht durchgeführt |
| HD-009 Affiliate-Zentrale | 0.1.2-dev | CURRENT.zip vorhanden (610.065 Bytes) + MANIFEST | Unabhängiger ZIP-Inhalts-/Hash-Readback nicht durchgeführt |
| Anzeigenfüller (Akte „HD-008-ANZEIGENFUELLER“) | 1.0.0 | Kein zugehöriger isolierter Zielordner | Nicht durchgeführt |

**Inventarkonflikt:** Zwei vorhandene Akten verwenden den Präfix `HD-008` (SEO-Metadaten und Anzeigenfüller). Eine neue ID oder Umnummerierung wurde nicht erfunden. Das zentrale Register war hinsichtlich HD-007/HD-008 SEO zuvor unvollständig und wurde im Prüfzweig ergänzt.

## Favicon – gefundener Stand
- Library-Pfad: `/hobby rausch/HOBBY_DEPOT_HD003_1.50.785_ORIGINALLOGO_VERIFIZIERT_VOLLPLUGIN.zip`.
- Tatsächlicher Dateieintrag mit Größe **63.407.568 Bytes**, nicht als ZIP-Bytes erneut geöffnet.
- Vorversion `HOBBY_DEPOT_HD003_1.50.784_ORIGINALFAVICON_VOLLPLUGIN.zip` ebenfalls als Library-Dateieintrag vorhanden.
- Prüfbericht `HOBBY_DEPOT_HD003_1.50.785_LOGO_PRUEFBERICHT.txt` vorhanden: Originalbogen und ausgeschnittene H-/D-Formen aus Original-Logo statt ersetzter Schrift, historischer lokaler PHP- und ZIP-PASS; kein echter WordPress-Live-PASS.
- Separates Bild `/hobby rausch/HOBBY_DEPOT_FAVICON_ORIGINAL_VORSCHAU.png` visuell gelesen: weißer und dunkler quadratischer Untergrund, türkis-beiger Bogen, H/D.
- Versuch, ZIP-Rohbytes im Prüfungslauf zu erhalten: **fehlgeschlagen** mit `This Project file does not have an authorized raw-byte materialization path.`.
- Textleseversuch derselben ZIP: `No readable content was found in this file for the requested mode.`.
- Kein neuer ZIP-/Unzip-, Größen-/Inhalts-, SHA-, Positiv-/Negativ-, Regressionstest und kein Live-PASS. Die Zahl der Bytes im Library-Dateieintrag ist **kein** unabhängiger Hashnachweis.

## Separate Library-Büroprüfung
Unter `/Hobby Depot/Plugin-Büro` sind u. a. HD-001 1.14.16, Bildzentrale 2.7.8, Design 1.50.704, Glossar 1.0.1, Hobbyregister 1.0.0 und das Designprüfprotokoll 1.50.782 aufgeführt. Ein echtes Design-1.50.785-ZIP wurde dort **nicht** gefunden. Diese Library-Liste darf nicht mit dem Campus-Current verwechselt werden.

## Harter Abschluss
- Kein binäres Plugin-Paket wurde in diesem Prüflauf erstellt, ersetzt, als Campus-CURRENT ausgegeben oder live installiert.
- Es gibt keinen bestätigten Campus-Gesamt-PASS. Kein früheres alteres Vollplugin darf ersatzweise als neuester Stand ausgegeben werden.
- Erste nächste Aktion nach Einzel-Current HD-003: **1.50.785 als echte Roh-ZIP unabhängig erneut öffnen und prüfen; dann erst die vollständige geprüfte ZIP in der vorgesehenen Campus-Akte synchronisieren.** Weitere fehlende ZIPs danach aus ihren tatsächlichen Einzel-Currents nachholen.
