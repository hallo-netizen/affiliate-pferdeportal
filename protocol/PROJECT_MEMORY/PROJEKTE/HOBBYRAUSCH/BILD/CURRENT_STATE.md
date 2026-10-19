# HOBBYRAUSCH – BILD / BILDZENTRALE – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-19
STATUS: **HOBBY DEPOT BILDZENTRALE 1.0.0 LOCAL PASS / INSTALLATIONSKANDIDAT / LIVE OFFEN**

## Aktueller belastbarer Stand

Das vorhandene BILD-Büro bleibt die einzige Hobby-Depot-Bildzentrale. Kein Parallelbüro.

Referenz des früheren allgemeinen Systems:
- Allgemeine Bildzentrale 2.7.6;
- Pferde-Installation 2.7.6 belegt;
- exakte 2.7.6-Pluginbytes im aktuell erreichbaren Arbeitsbestand nicht verfügbar.

Deshalb wurde kein angeblicher 2.7.6-Klon konstruiert, sondern eine **saubere Hobby-Depot-Fassung auf Basis des belegten allgemeinen Funktionsvertrags und der aktuellen Hobby-Depot-Designschnittstellen** gebaut.

## Installationskandidat

Plugin:
**Hobby Depot Bildzentrale 1.0.0**

Artefakt:
`HOBBY_DEPOT_BILDZENTRALE_1.0.0_INSTALLIEREN.zip`

SHA-256:
`bb74d795dffaa6d3ff51d6251d298c04c53ee9a3d75d39c00609afde867c7503`

Persistente Arbeitskopie:
`/Hobby Depot/Bildzentrale/HOBBY_DEPOT_BILDZENTRALE_1.0.0_INSTALLIEREN.zip`

## Übernommener allgemeiner Kern

- Beiträge/Seiten/CPT über WordPress Featured Image;
- WordPress-Kategoriebilder;
- optionale HivePress-Kategoriebilder;
- Pixabay;
- Pexels;
- Magnific;
- Mediathek-Zuweisung;
- URL-Import;
- Readback nach Bildzuweisung;
- Rücksetzung bei fehlgeschlagenem Readback;
- No-Overwrite als Standard;
- Konfigurationsexport ohne API-Schlüssel.

## Exakte Hobby-Depot-Designbindung

Frisch gegen Designstand 1.50.699 geprüft:
- normale WordPress-Kategorien werden über `thumbnail_id` gelesen;
- HivePress liest die von der Bildzentrale bereitgestellte Option `pabz_taxonomy_image_config_v1`;
- Standardbindung der neuen Bildzentrale: `hp_listing_category` + `thumbnail_id`.

Damit wird keine neue Bildschnittstelle erfunden.

## Entfernt / nicht übernommen

- `pa_breed`;
- Pferderassen-Batch;
- Pferderassen-Hero-Sonderlogik;
- Pferde-Prompts/-Framing;
- Pferde-Taxonomien/-IDs/-URLs;
- **Bildertrommel / Random-Rotation**;
- automatische Massenbilderzeugung;
- automatische Überschreibung bestehender Bilder;
- Zugangsdaten.

Magnific läuft nur nach ausdrücklicher Admin-Aktion und ohne Cron.

## Lokale QA

- PHP-Lint: **PASS**;
- ZIP-Integrität: **PASS**;
- `pa_breed` / Horse-Logik: **0**;
- Scheduler/Cron: **0**;
- Design-Kompatibilitätsoption vorhanden;
- WordPress-Kategorie `thumbnail_id`: vorhanden;
- Pixabay/Pexels/Magnific-Wege vorhanden;
- No-Overwrite + Readback/Rollback vorhanden.

## Installation Hobby Depot

Noch nicht installiert.

## ERSTER OFFENER BLOCKER

Echter WordPress-Installations- und Funktionsreadback.

## EXAKT EINE NEXT ACTION

**HOBBY_DEPOT_BILDZENTRALE_1.0.0_INSTALLIEREN.zip im Hobby Depot installieren und zunächst nur einen bestehenden Mediathek-Test sowie je eine leere WordPress-Kategorie-/Seitenzuweisung prüfen; keine Massenbebilderung starten.**
