# ZENTRALES MODULREGISTER

STAND: 2026-09-05
ZWECK: Der Nutzer muss sich NICHT merken, welches Modul allgemein oder projektbezogen ist.

## Pflichtregel

Bei:
- jeder neuen Masterdatei,
- jedem neuen Plugin/Modul,
- jedem neuen Projekt,
- jeder geplanten Wiederverwendung

muss dieses Register geprüft und bei neuen Erkenntnissen aktualisiert werden.

## Klassen

### ALLGEMEINGÜLTIG
Der Kern ist projektunabhängig und gehört primär in dieses Gebäude.

### PROJEKTBEZOGEN
Der Baustein gehört ausschließlich zu einem Projekt.

### GEMISCHT
Allgemeiner Kern + projektspezifische Konfiguration/Daten.
Hauptkern hier; Projektbüro enthält nur Nutzung, Konfiguration und Projektgeschichte.

### UNGEKLÄRT
Noch nicht ausreichend belegt.
Nicht automatisch verschieben oder als allgemein behandeln.

## MOD-001 – KATEGORIENMODELL

KLASSE: ALLGEMEINGÜLTIG
STATUS: vom Nutzer ausdrücklich bestätigt
HAUPTORT: ALLGEMEINGUELTIGE_BAUSTEINE/KATEGORIENMODELL
ZWECK: selbstständige Erstellung/Strukturierung von Kategorien
PROJEKTBEZUG: keiner als Grundvoraussetzung
NUTZUNG: Projekte dürfen darauf verweisen und eigene konkrete Kategorien/Parameter führen.
NÄCHSTER BELEG: Masterdateien/Code bei Übergabe vollständig inventarisieren.

## MOD-002 – BILDZENTRALE

KLASSE: GEMISCHT
STATUS: allgemeiner Plugin-Kern bestätigt; LIVE im Pferde-Atelier Version 2.6.9
HAUPTORT KERN: ALLGEMEINGUELTIGE_BAUSTEINE/BILDZENTRALE
PROJEKTNUTZUNG: PROJEKTE/PFERDE_ATELIER/BILD

ALLGEMEINER KERN:
- Beiträge
- WordPress-Taxonomien
- optionale HivePress-Taxonomien
- Pixabay
- Pexels
- Magnific
- sichere Profile
- Export/Import
- Readback-Fallback

PFERDE-ATELIER-SPEZIFISCH:
- Pferde-Prompts
- konkrete Profilwerte
- konkrete Produktionshistorie
- konkrete Post-/Attachment-/Task-Zuordnungen
- konkrete Migrationen und Fehlerhistorie des Projekts

BELEG:
- Nutzerbestätigung LIVE 2.6.9
- BILD-Masterakten-Inventar
- 2.6.6-Konfigurationsbeleg
- 2.4.9-Codebeleg

OFFEN:
vollständiger 2.6.9-Code noch nicht als Datei übergeben; allgemeine Codeprüfung folgt bei Übergabe.

## Keine doppelte Wahrheit

Ein allgemeiner Modul-Kern wird nur hier als Hauptmodul geführt.
Projektgebäude enthalten nur:
- Verweis auf den allgemeinen Kern,
- projektspezifische Konfiguration,
- projektspezifische Historie,
- projektspezifische Fehler/Tests.

## Automatische Entscheidung bei neuen Dateien

1. Datei/Modul vollständig inventarisieren.
2. Auf harte Projektverdrahtung prüfen.
3. Allgemeine Funktion von Projektdaten trennen.
4. Klasse setzen: ALLGEMEINGÜLTIG / PROJEKTBEZOGEN / GEMISCHT / UNGEKLÄRT.
5. Hauptort festlegen.
6. Projektverweise anlegen.
7. Nutzer muss sich die Einordnung nicht merken.
