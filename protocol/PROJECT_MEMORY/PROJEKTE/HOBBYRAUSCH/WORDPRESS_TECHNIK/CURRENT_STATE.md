# HOBBYRAUSCH – WORDPRESS_TECHNIK – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-11-01
STATUS: 15 aktive WordPress-Plugins laut Betreiberliste / Server-Funktionsprüfung offen / keine Installation in diesem Abgleich

## Quelle und Zuständigkeit
Einzige Current-Autorität für den WordPress-Betriebsstand. Quelle: vom Betreiber am 01.11.2026 gelieferte vollständige Pluginliste, alle Einträge zeigen „Deaktivieren“. Kein eigener authentifizierter WordPress-Readback durchgeführt. Für einzelne Eigenplugins bleibt die jeweilige Plugin-Akte die technische Current-Autorität.

## Aktive Plugins laut WordPress-Ansicht
| WordPress-Pluginname | Installierte Version | Zuordnung |
|---|---|---|
| Affiliate Portal Template Kit | 1.50.783 | HD-003 |
| Affiliate-Portal Kategorie-Workflow | 1.14.17 | HD-001 |
| Footer-Umzug – Portale | 1.1.1 | Werkzeug |
| HivePress | 1.7.31 | Drittanbieter |
| Hobby Depot Bildzentrale | 2.7.8 | HD-006 |
| Hobby Depot Glossar Core | 1.0.25 | HD-005 |
| Hobby Depot Hobbyregister Core | 1.2.16 | HD-007 |
| Hobby Depot Kategorie-Kern | 1.0.0 | HD-004 |
| Hobby Depot – Affiliate-Zentrale | 0.1.7-dev | HD-009 |
| Hobby Depot – FAQ Frontend Fix | 1.0.2 | ohne HD-ID |
| Hobby Depot – Performance Diagnose | 1.1.0 | ohne HD-ID |
| Minimal Coming Soon & Maintenance Mode | 2.45 | Drittanbieter |
| WPForms Lite | 2.0.3.1 | Drittanbieter |
| WPvivid Backup Plugin | 0.9.136 | Drittanbieter |
| Yoast SEO | 28.7 | Drittanbieter |

Verfügbare, nicht installierte Updates: HivePress 1.8.1 (aktiv 1.7.31), WPvivid 0.9.139 (aktiv 0.9.136), Yoast SEO 28.8 (aktiv 28.7).

## Abweichungen und Arbeitsgrenzen
- HD-003 Design 1.50.783 aktiv; 1.50.785 ist ein nicht unabhängig wiedergeöffneter Vollplugin-Dateifund, nicht installiert.
- HD-001 Kategorie-Workflow 1.14.17 aktiv; ältere Akte hat nur 1.14.16 geprüft. Keinen Downgrade vornehmen.
- HD-009 Affiliate-Zentrale 0.1.7-dev aktiv; archivierter Campus-Kandidat 0.1.2-dev ist älter. Nicht überinstallieren.
- HD-004 1.0.0, HD-005 1.0.25, HD-006 2.7.8, HD-007 1.2.16 bereits aktiv; lokale Tests sind kein funktionaler WordPress-Live-PASS.
- FAQ Frontend Fix 1.0.2 und Performance Diagnose 1.1.0 aktiv; noch ohne verifizierte Voll-ZIP im Campus und ohne geklärte HD-ID.
- HD-002 Themenengine, HD-008 SEO-Metadaten und Anzeigenfüller nicht in den gelieferten 15 Pluginzeilen; keine Behauptung einer Deinstallation. Yoast SEO ist aktiv; parallelen HD-008-Ausgabeweg erst auf Überschneidungen prüfen.
- Bestandskollision HD-008-SEO versus HD-008-Anzeigenfüller bleibt unverändert und offen.

Beleg: ../PLUGINS/EVIDENCE_WP_PLUGINLISTE_20261101.md (Nachweis, keine zweite Current-Autorität).

## Historischer lokaler Test (20.10.2026, nicht mehr als aktueller Installationsstand)
HD-007 1.0.0 und HD-003 1.50.704 waren frühe lokale Hobbyfinder-Tests. Die aktuelle WordPress-Liste zeigt HD-007 1.2.16 und HD-003 1.50.783. Das zentrale Hobbyregister bleibt fachliche Quelle; HD-004 bleibt read-only. Keine neue Architektur.

## HD-003 Updatekandidat 01.11.2026

Die Betreiberliste enthält weiter HD-003 **1.50.783 aktiv**. Eine neue vollständige **1.50.786-ZIP** enthält das freigegebene Favicon und den zwischen Suche und Kategorie-Kacheln verschobenen Banner der Anzeigenmarkt-Root-Seite. ZIP lokal 1.281/1.281 und 11/11 PHP PASS; beide persistierten Library-Kopien nach Upload erneut komplett geöffnet, Größe/SHA identisch. **Nicht live installiert**. Technische Wahrheit und Bezugswege: `../PLUGINS/PLUGIN_AKTEN/HD-003-DESIGN-TEMPLATE-KIT/CURRENT.md`. Keine neue WordPress-Installation behaupten.

## ERSTER OFFENER BLOCKER
Die echten vollständigen aktuellen Plugin-Dateien wurden nicht unabhängig mit dem WordPress-Bestand verglichen. Die 1.50.785-Datei konnte im Nachholcheck nicht als Roh-ZIP geöffnet werden. Die vollständige Campus-Ablage ist BLOCKED.

## EXAKT EINE NEXT ACTION

**HD-003 1.50.786 als vollständiges Plugin über die vorhandene WordPress-Installation 1.50.783 einspielen und anschließend Favicon und Banner-Reihenfolge live ablesen.** Live-Readback nicht vorwegnehmen.
