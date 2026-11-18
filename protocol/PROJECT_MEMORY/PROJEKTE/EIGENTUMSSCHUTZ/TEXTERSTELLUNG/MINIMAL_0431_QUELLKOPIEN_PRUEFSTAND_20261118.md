# Hab & Bewahr / Universal – exakte Minimal-Kopie aus Texterstellung 0.4.31

**Stand: 18.11.2026. Status: INTERNE ARBEITSKOPIEN, KEIN INSTALLATIONS-RELEASE.**

## Auftrag und Kurskorrektur
Der Nutzer hat die universelle Neuentwicklung ausdrücklich verworfen: keine neuen Klassen, keine Adapter, keine Architekturumstellung, keine Fixes. Ziel ist ausschließlich die vorhandene originale Pferdeatelier-Texterstellung als leere unabhängige Kopie für (a) Hab & Bewahr und (b) universelle Neuinstallationen, indem pferdespezifische Daten und Sonderfälle auskommentiert oder entfernt werden. Im Chat nur echte vollständig freigegebene WordPress-Plugins zum Download.

## Beleg des Ausgangsstands
Original: `/pferdeatelier/PLUGINS/ARBEITSRAUM_PSTE_KISS/Texterstellung-0.4.31-KISS-DURCHGAENGIGER-MINI-ABLAUF-PFERDEATELIER.zip`, 88 Dateien (78 PHP, 8 JSON, README und Signatur). SHA256 `07b99fa549e87d28db53f0fac0b107c92a9f0de4a3de80ad5f31fb3b7b399f7d`. Original bytegleich bewahrt, K0 unverändert. *Die 0.5.x-Entwürfe sind keine Quellbasis mehr.*

## Exakter Arbeitsvorgang
Es wurden zwei vollständige technische Kopien der Originalquelle erstellt, keine Neuentwicklung.
1. Pluginname/Anleitung/Diagnosekennung auf Hab & Bewahr bzw. Blanko angepasst; technischer PSTE- und PSERC-Originalkern erhalten.
2. Pferde-Kategoriekarte mit 1165 alten Einträgen entfernt, bewusst leer. Kein erfundener Hab-Kategorien- oder Artikeltypeneintrag.
3. 26 Pferde-Familien-Overrides, feste Pferde-Suchbegriffe/Seeds, Pferde-Journal-Kategorien und pferdespezifische Beispieltexte aus JSON gelöscht; Pferde-Journal-Autozuordnung deaktiviert.
4. Verändertes altes Journal-Manifest nicht mit unpassender Originalsignatur weitergegeben; `.sig` entfernt und Erweiterung bewusst nicht freigegeben.
5. Pferdebezogene PHP-Sonderfälle an ihrer jeweiligen Originalstelle deaktiviert (zwei Pferde-Familiennamen, Pferde-Medizinwörter, Pferde-Phrase, alter Pferde-Haftpflicht-Kurzweg, Pferde-Kontext). Allgemeine bestehende Sicherheitsregeln, andere Recherchepfade, MINI, K0 und Entwurfsimport bleiben stehen.
6. Originale technische K0-Vertragskennung `PFERDE_ATELIER_WORDPRESS_IMPORT_V1` ist noch in Hauptdatei und PSERC-Original. Das sind kompatibilitätsrelevante technische Namen, keine verbliebene Pferde-Themenzuordnung. Kommentare und deaktivierter Journal-Altkode enthalten weiterhin Pferde-Beispiele. Nicht fälschlich komplette Null-Treffer behaupten.
7. Ausschließlich bestehende Dateien geändert: **68/88 unverändert, 20/88 geändert oder entfernt** (darunter eine Signaturdatei entfernt), **0 neue Laufzeitdateien, 0 Klassen/Adapter/Tabellen hinzugefügt**. Beide ZIPs haben je 87 Einträge und differieren nur in README, Pluginname/Hauptdatei und Diagnoseanzeige.

## Verifizierte Prüfungen
- Beide ZIP CRC PASS, je 78/78 PHP Syntax und 8/8 JSON Parser PASS.
- Isolierte Ausführung Original-Kategorie-Map liefert `PSTE_PORTAL_CATEGORY_MAP_COUNT_INVALID` (korrekte eindeutige Sperre statt Übernahme alter Pferde-Kategorien); Journal ohne Originalsignatur liefert `PSTE_EXTENSION_MANIFEST_MISSING`; Pferde-Journal-Autoroute ist inaktiv. Allgemeiner Notfall-Risikoweg weiter aktiv.
- Keine reale WordPress-Installation, kein echter DataForSEO- oder K0-WP-Rundlauf vorgenommen. Kein Live-Daten-Write.

## Tatsächliche Büroablagen – erfolgreiche Uploads
- Hab: `/hab-und-bewahr/TEXTERSTELLUNG/ARBEITSKOPIEN/MINIMAL_ORIGINAL_0431/Texterstellung_HAB_0.4.31.1_MINIMAL_NICHT_FREIGEGEBEN.zip`, SHA256 `3f74e5c47f79ed36571dfc9a2adb63f639bdb9aafa294c19722ad2394fbe48d4`.
- Universal: `/texterstellung-universal/ENTWICKLUNG_20261118/MINIMAL_ORIGINAL_0431/Texterstellung_BLANKO_0.4.31.1_MINIMAL_NICHT_FREIGEGEBEN.zip`, SHA256 `cbbca4c2a2f1122198cb3cda927ab739ad94e9df87bf9ace28c9201a4f16dc4d`.
- An beiden Orten: `MINIMAL_KOPIEN_0431_ENTWICKLUNGSPROTOKOLL.md`, `MINIMAL_KOPIEN_0431_PRUEFBERICHT.json`, vollständiges reproduzierbares Bau-/Vergleichsskript und isolierter Originalfunktionstest. Uploads bestätigt.

## Eine unvermeidbare Original-Grenze – nicht behaupten, fertig zu sein
Original-PSTE setzt eine nichtleere, eindeutig zu Artikelart und Produkt-/Themenseite gebundene Kategoriekarte voraus. Hab benutzt R3-Seiten mit flachen eigenständigen WordPress-Kategorien, deren Namen im historischen 285er Stand keine Artikelart-Vorsilben tragen. Ohne belegtes kompatibles Hab-Zuordnungsformat wird die originale Recherche korrekt blockiert. Eine bloße Löschung der Pferdevorgaben kann dieses Original-Datenmodell nicht füllen. Der Nutzer hat neue Architektur/Fixes untersagt; also keine Zuordnungen raten und keine neue Kategorieautomatik bauen. Aktive K0-Registrierung für Hab ist ebenfalls nicht belegt.

**Nächste zulässige Arbeit:** Ausschließlich prüfen, ob vorhandene reale Hab-Kategorien samt Artikelart und Seitenbindung ohne zusätzliche Logik in die Original-Kategorie-Map passen. Falls nicht, die nachgewiesene Grenze als solche respektieren. Beide Minimal-ZIPs bleiben intern und NICHT zum Herunterladen oder Installieren freigegeben; die Ausgaberegel bleibt gültig.