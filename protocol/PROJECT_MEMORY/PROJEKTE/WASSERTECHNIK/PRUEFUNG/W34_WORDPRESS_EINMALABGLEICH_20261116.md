# W34 – ein einziger echter WordPress-Abgleich aus vorhandenen Quellen
**16.11.2026 – keine Nutzerdateien nötig, keine WordPress-Schreibaktionen.**

## Beweissicherung
- **Original-WordPress-Export 14.11.2026, 12:28:47 UTC:** 2 Seiten, 1 Beitrag, 1 Beitragskategorie, 0 Wassertechnik-Produktseiten. Im Export: 1 veröffentlichte Beispielseite, 1 Datenschutzerklärungs-Entwurf, veröffentlichter Standardbeitrag „Hallo Welt!“, Beitragskategorie „Allgemein“.
- **Historischer W6-Plan:** 218 SEO-Owner = 113 WP-Seiten und 105 Beitragskategorien. Gegen **genau diesen Snapshot** 0 Namens-/Slug-Kollisionen; dies erlaubt keine Aussage über später angelegte Inhalte.
- **W27-Fachmaster / W32:** 7 sichtbare Zielbereiche, 79 unverändert geplante W4-Produktseiten (71 kaufnah, 8 industrielle Fachseiten) – kein neuer Produktowner durch den Navigationsplan.
- **W28:** 81 weitere kanonische Kandidaten und 90 Rubriken, aber 0 SEO-/WP-Freigaben. Keine automatisch zu importierenden neuen Seiten.
- **Altes W6-Neuner-Importmanifest darf nicht durch WT001 0.1.8 W33 aktiviert werden**: für die W27-Siebener-Zielstruktur veraltet. Kein doppeltes Entscheidungssystem, keine neue Version wegen einer Teilprüfung.

## Ein einziger zusätzlicher technischer Test
Die GitHub-Action `wassertechnik-w34-wp-inventory.yml` startet `PRUEFUNG/W34_public_wordpress_readonly.py`. Sie prüft den Archivbestand gegen alle aktuellen Quelldateien und versucht **nur über öffentliche HTTP-GET-Abfragen** die wirklich veröffentlichten Seiten, Beiträge und Rubriken der gebundenen Testseite zu zählen. Das darf keine Zugangsdaten oder Änderungen in WordPress erfordern. Ein Fehler bei der öffentlichen Website wird als **NICHT_VERIFIZIERT** markiert; niemand deutet den 14.11.-Export als tagesaktuellen Stand um.

Die öffentliche WordPress-Schnittstelle kann keine Entwürfe, privaten Inhalte oder internen Owner-Metadaten bestätigen. Auch bei Erfolg bleibt ein vollständiger schreibfreier Admin-Readback unmittelbar vor dem einen schreibenden Import erforderlich; dieser kann in demselben freigegebenen WP-Workflow stattfinden.

**KISS / Status:** W34 macht nur Bestandsprüfung und Quellenabgleich, keine neue Fachentscheidung, kein Plugin zur Installation, kein API-Bezahlaufruf, 0 WP-Schreibaktionen.
