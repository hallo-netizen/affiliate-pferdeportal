# ZENTRALES MODULREGISTER

STAND: 2026-09-05
ZWECK: Der Nutzer muss sich NICHT merken, welche Grundmodule existieren, wo sie liegen oder ob sie projektübergreifend nutzbar sind.

## Rolle

Das Modulregister ist kein zusätzliches Fachbüro und keine zweite technische Wahrheit.

Es ist der zentrale Karteikasten des Campus:
- Welche Module gibt es?
- Was ist ihr Hauptort?
- Sind sie allgemeingültig oder projektbezogen?
- Welcher Stand ist belegt?
- Welche Projekte nutzen sie?
- Welche Voraussetzungen gelten?

Die technische Wahrheit bleibt beim jeweiligen Modul.

## Pflichtprüfung

Das Modulregister wird automatisch geprüft bei:
- neuem Projekt;
- neuer Masterdatei;
- neuem Plugin/Modul;
- geplanter Wiederverwendung;
- Frage „haben wir dafür schon etwas?“.

Bei normaler Facharbeit ohne Modulbezug muss es nicht jedes Mal vollständig gelesen werden.

## Modulklassen

### ALLGEMEINGÜLTIG
Der Modul-Kern ist projektunabhängig.
Hauptort liegt unter `ALLGEMEINGUELTIGE_BAUSTEINE/`.

### PROJEKTBEZOGEN
Der Modul-Kern ist bewusst nur für ein bestimmtes Projekt bestimmt.
Hauptort liegt im jeweiligen Projektgebäude.

### UNGEKLÄRT
Die Modulklasse ist noch nicht belastbar geklärt.
Default bei Unsicherheit.
Nicht automatisch verschieben oder wiederverwenden.

## Wichtig: GEMISCHT ist KEINE Modulklasse

„Gemischt“ beschreibt eine Datei/Masterakte, die z. B.:
- allgemeinen Plugin-Code
- plus projektspezifische Konfiguration
- plus Projekthistorie

enthält.

Dann wird die Masterakte im Büro inventarisiert und in Bestandteile zerlegt.
Der allgemeine Modul-Kern kann trotzdem eindeutig ALLGEMEINGÜLTIG sein.

## Pflichtfelder je Modul

- MOD-ID
- NAME
- MODULKLASSE
- STATUS / Prüfgrad
- HAUPTORT
- AKTUELL BELEGTER STAND
- ZWECK
- ABHÄNGIGKEITEN
- NUTZENDE PROJEKTE
- AUTORITATIVE QUELLE / BELEG
- OFFENE PUNKTE

## MOD-001 – KATEGORIENMODELL

MODULKLASSE: ALLGEMEINGÜLTIG
STATUS: vom Nutzer ausdrücklich als allgemeingültig bestätigt; Masterakten/Code folgen
HAUPTORT: `ALLGEMEINGUELTIGE_BAUSTEINE/KATEGORIENMODELL/`
AKTUELL BELEGTER STAND: noch aus Masterakten zu ermitteln
ZWECK: selbstständige Erstellung und Strukturierung von Kategorien
ABHÄNGIGKEITEN: noch zu inventarisieren
NUTZENDE PROJEKTE: bei konkreter Nutzung eintragen
BELEG: Nutzerbestätigung 2026-09-05
OFFEN: vollständige technische Inventarisierung nach Übergabe

## MOD-002 – BILDZENTRALE

MODULKLASSE: ALLGEMEINGÜLTIG
STATUS: allgemeingültiger Modul-Kern vom Nutzer bestätigt; LIVE im Pferde-Atelier 2.6.9; Byte-/Codeprüfung 2.6.9 noch offen
HAUPTORT: `ALLGEMEINGUELTIGE_BAUSTEINE/BILDZENTRALE/`
AKTUELL BELEGTER LIVE-STAND: 2.6.9 im Pferde-Atelier
ZWECK:
- Beiträge
- WordPress-Taxonomien
- optionale HivePress-Taxonomien
- Pixabay
- Pexels
- Magnific
- sichere Profile
- Export/Import
- Readback-Fallback
ABHÄNGIGKEITEN: WordPress; optionale HivePress-Nutzung; Providerzugänge
NUTZENDE PROJEKTE:
- PFERDE_ATELIER → `PROJEKTE/PFERDE_ATELIER/BILD/`
BELEG:
- Nutzerbestätigung LIVE 2.6.9
- BILD-Masterakten-Inventar
- 2.6.6-Konfigurationsbeleg
- 2.4.9-Codebeleg
OFFEN:
- vollständiger 2.6.9-Code noch nicht als Datei übergeben;
- technische Portabilitätsprüfung des 2.6.9-Codes folgt nach Übergabe.

## Projektanwendung

Ein Projekt, das ein allgemeingültiges Modul nutzt, speichert NICHT den Modul-Kern ein zweites Mal als Hauptwahrheit.

Im Projekt bleiben nur:
- Verweis auf MOD-ID/Hauptort;
- projektspezifische Konfiguration;
- Projektdaten;
- projektspezifische Historie;
- projektspezifische Fehler und Tests.

## Automatische Klassifizierung neuer Eingänge

1. Masterdatei vollständig inventarisieren.
2. Bestandteile trennen: Code / Konfiguration / Daten / Historie / Tests / Protokolle.
3. Modul-Kern identifizieren.
4. Bei Unsicherheit zunächst MODULKLASSE = UNGEKLÄRT.
5. Auf harte Projektverdrahtung und Konfigurierbarkeit prüfen.
6. Modulklasse festlegen.
7. Genau einen Hauptort festlegen.
8. Projektanwendungen nur verweisen.
9. Modulregister aktualisieren.

Der Nutzer muss diese Einordnung weder erinnern noch manuell vorgeben.
