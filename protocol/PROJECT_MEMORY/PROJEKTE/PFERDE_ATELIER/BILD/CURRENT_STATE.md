# BILD – CURRENT STATE

STAND: 2026-09-05
STATUS: LIVE 2.6.9 / MASTERAKTEN TEILWEISE HISTORISCH

## Aktueller produktiver Stand

LIVE in WordPress:
**Pferde Atelier Bildzentrale 2.6.9**

Vom Nutzer bestätigte Pluginbeschreibung:
Allgemeingültige Bildzentrale für Beiträge, WordPress-Taxonomien und optionale HivePress-Taxonomien mit Pixabay, Pexels und Magnific, sicheren Profilen, Export/Import und Readback-Fallback.

Das ist die aktuelle fachliche LIVE-Wahrheit.

## Beleglage

### Code
Letzter vollständig übergebener Plugin-Code:
**2.4.9**

Plugin-ZIP SHA-256:
`265edaf3cee55b751b5f107e96c50dfcada99450bd94a07339e3234ae0bc47a1`

PHP SHA-256:
`079fe4efc6fa53ffd09c3c7490f1873f249509df17548224ead42ba7389c71c2`

### Konfiguration
Späterer übergebener Einstellungs-Export:
**2.6.6**, Export 2026-08-06.

### LIVE
Aktuell eingesetzte Version:
**2.6.9**.

Der vollständige 2.6.9-Code ist aus den bisher übergebenen Masterdateien noch nicht bytegenau belegbar.

## Belegtes Funktionsbild

Aus 2.4.9-Code + 2.6.6-Konfiguration + LIVE-Beschreibung sind mindestens belegt:

- Beitragsbilder
- WordPress-Taxonomiebilder
- optionale HivePress-Taxonomiebilder
- Pixabay
- Pexels
- Magnific
- Provider-Verbindungstests
- KI-Bildgenerierung
- Einzel- und Batch-Verarbeitung
- Promptanalyse
- Motivcluster
- benutzerdefinierte Motive
- Variationsplanung gegen Wiederholungen
- Variationshistorie
- Medienimport
- Bildzuordnung
- Beitragsbild setzen / Undo
- Inhaltsbild setzen / Undo
- Readback lokaler Bilder
- externer Fallback
- Lizenzregister / Bildnachweise
- Qualitätsdaten / Qualitätsaudit
- Export / Import
- sichere Profile
- Taxonomie-Konfiguration

## Profile aus 2.6.6-Konfigurationsbeleg

### Beitragsbilder
- Ratio 3:2
- 1500 × 1000
- WebP 82
- Zielgröße 350 KB

### WordPress-Kategorien
- gespeicherte Ausgabe: 3:1
- 1200 × 400
- WebP 76
- Zielgröße 120 KB
- Prompttext nennt zugleich 16:9 → UNGEKLÄRTER WIDERSPRUCH

### HivePress-Kategorien
- Ratio 3:2
- 1500 × 1000
- WebP 76
- Zielgröße 120 KB

Taxonomien:
- WordPress: `category` / `thumbnail_id`
- HivePress: `hp_listing_category` / `hp_image`

## Historischer 2.4.9-Fix

Belegter Fehler:
Nach Import/Zuordnung verwendete die Sammelübersicht weiter die temporäre Magnific-Ergebnis-URL. Nach deren Ablauf blieb die Vorschau leer, obwohl das Bild bereits lokal vorhanden war.

Fix:
- lokale Attachment-Suche über `_pabz_asset_id`;
- lokale WordPress-Bild-URL hat Vorrang;
- externe Magnific-URL nur als Fallback;
- globale automatische Verwaisten-Suche bleibt deaktiviert.

Belegte Tests:
- PHP-Syntax PASS
- Version 2.4.9 PASS
- lokale Attachment-Suche PASS
- lokale URL vor externer URL PASS
- externer Fallback PASS
- Verwaisten-Fix aus 2.4.8 erhalten PASS

## Offene Belegpunkte

1. vollständiger 2.6.9-Code noch nicht in den übergebenen Dateien;
2. exakter Änderungsweg 2.4.9 → 2.6.6 → 2.6.9 noch nicht vollständig historisch belegt;
3. WordPress-Kategorie: Prompt 16:9 vs. gespeicherte Ausgabe 3:1 ungeklärt;
4. ein historischer Magnific-Task stand beim Vor-Migrations-Export noch auf `IN_PROGRESS`; späterer Endstatus aus den vorliegenden Akten nicht belegt.

Keine Lücke durch Raten schließen.
