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

## Tatsächlich ausgeführter GitHub-Liveversuch am 16.11.2026
- Quelle: **GitHub Actions W34**, erfolgreicher Job, neueste Ausführung `43856387658`; gespeicherter Nachweis im GitHub-Workflow-Artefakt `wassertechnik-w34-wp-readonly-inventory`.
- Originaler Nutzerexport **14.11.2026, 12:28:47 UTC** im Repo bytegenau gelesen: **2 WP-Seiten** (Beispielseite `publish`, Datenschutzerklärung `draft`), **1 Standardbeitrag**, **1 Standardkategorie**. **0** W6-Zielpfade/Slugs im damaligen Export belegt; 113 geplante W6-Seiten, 105 geplante Inhaltskategorien und ihre Eltern im Quellenabgleich vollständig.
- Der aktuelle öffentliche HTTP-GET an `/wp-json/wp/v2/pages` antwortet tatsächlich **HTTP 200, `Content-Type: text/html; charset=UTF-8` mit einer HTML-Seite statt der WordPress-REST-JSON-Daten**. Deshalb `PUBLIC_REST_NOT_VERIFIED` und ausdrücklich **kein belastbarer tagesaktueller WP-Gesamtbestand**. Es ist kein Beleg für ein WordPress-Problem oder für die Nichtexistenz veröffentlichter Wassertechnik-Seiten. Auch eine erfolgreiche öffentliche REST-Abfrage könnte Entwürfe und interne Owner-Kennungen nicht vollständig bestätigen.
- **0 WordPress-Schreibzugriffe, 0 kostenpflichtige SEO-/API-Abfragen**, keine Installation, keine Behauptung von aktuell 0 Wassertechnik-Seiten.

## Gebündelte interne Lösung innerhalb des vorhandenen WT001-Probeplugins
- **Eine** schreibfreie Bestandslesung `../PLUGINS/QUELLCODE/W34_class-wassertechnik-inventory-readback.php` im bisherigen W33-Gesamtbauer `../PLUGINS/BUILD/W33_build.py` integriert. Sie liest in einem Vorgang WP-Seiten samt Entwürfen, Beiträge, Kategorien, echte WP-Pfade und vorhandene Owner-Kennungen.
- Die Klasse ordnet dieselben **218 alten Referenz-Owner** aus dem W6-Manifest zu und liefert bestehende/fehlende/fremde oder verschobene Ziele. Kein zweiter SEO-/Produktentscheider; der alte W9-Schreiber bleibt **deaktiviert**.
- **Echter GitHub-Offline-Gesamttest W33** (bei W34-Änderungen automatisch erneut ausgeführt): Original-2/1/1-WordPressdaten im Mock, **0 zugeordnete, 218 fehlende W6-Owner, 0 Konflikte**. Fremder vorhandener Zielpfad, falscher Sitehost und fehlende Adminrechte jeweils **blockiert**. Die W33-218er-SEO-Fortsetzung, die echte W28-81er-Einlesung, das W32-Siebener-Menü und der alte W9-Import-Schutz bestehen unverändert; **0** WordPress-Schreib- und **0** API-Kostenaufrufe.
- GitHub-W33-Gesamtbuild wurde auf **14 Paketdateien** erweitert und vollständig syntax-/ZIP-/Mock-geprüft. Das technische ZIP trägt weiterhin **`NICHT INSTALLIEREN`**, da weder dessen Live-WordPress-Verhalten noch seine vollständige Gleichwertigkeit mit dem fehlenden früheren 0.1.7-Original nachgewiesen wurde.

## Verbindliche KISS-Grenze und konkrete Folgerung
**W34-Bestandsvergleich: ABGESCHLOSSEN für den gesicherten Export und die technische Offline-Abnahme.** Die Live-Inventur bleibt ausdrücklich **NICHT_VERIFIZIERT**, weil die öffentlich erreichbare Website statt WordPress-REST-JSON HTML sendet. Eine spätere komplette Inventur ist bereits als **ein einziger Admin-Leseschritt innerhalb desselben bestehenden Plugin-Workflows** vorbereitet; nicht als neue Nutzervorlage oder separates Zusatzplugin. Vor Freigabe des Imports müssen die alte Neuner-WP-Zielstruktur und die aktuelle W27-Siebener-Zielstruktur in **einem** freigegebenen Migrationsplan zusammengeführt werden. Keine WordPress-Daten vorschnell überschreiben, keine neuen Keywords kostenpflichtig recherchieren.
