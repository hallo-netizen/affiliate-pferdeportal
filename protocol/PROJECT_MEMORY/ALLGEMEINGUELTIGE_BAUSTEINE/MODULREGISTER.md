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
STATUS: Master R10/R9 + WordPress-Plugin V1.8.0 hart inventarisiert; lokaler/fresh Prüfstand PASS; Live-WordPress-Deployment noch nicht PASS
HAUPTORT: `ALLGEMEINGUELTIGE_BAUSTEINE/KATEGORIENMODELL/`
AKTUELL BELEGTER STAND:
- Master 016 R10/R9 Runtime Deployment
- Plugin V1.8.0
ZWECK:
evidenzbasierte, allgemeingültige Kategorie-/Strukturentwicklung für Content, HivePress/Marketplace und explizit gebundene Journal-Taxonomien
ABHÄNGIGKEITEN:
- WordPress >= 6.4
- PHP >= 8.1
- DataForSEO für gebundene Research-Schritte
- HivePress nur wenn Marketplace-Säule genutzt wird
NUTZENDE PROJEKTE:
- historischer Real-/Pilotbeleg Gaumen Atelier im Master; keine fachliche Vererbung
- konkrete neue Projektnutzungen bei Einsatz eintragen
AUTORITATIVE QUELLE:
`ALLGEMEINGUELTIGE_BAUSTEINE/KATEGORIENMODELL/CURRENT_STATE.md`
ARCHIV:
`/Campus-Archiv/ALLGEMEINGUELTIGE_BAUSTEINE/KATEGORIENMODELL/2026-09-05/`
OFFEN:
echter Live-WordPress-Deploymentlauf auf Zielinstallation

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


## MOD-003 – UNIVERSAL PORTAL DESIGN SUITE

MODULKLASSE: ALLGEMEINGÜLTIG
STATUS: V2.2.40 / Contract V104 hart inventarisiert; spätere GitHub-Pferdehistorie bestätigt ausdrücklich „kein Universal-Update erforderlich“
HAUPTORT:
`ALLGEMEINGUELTIGE_BAUSTEINE/DESIGN/`
AKTUELL BELEGTER STAND:
- Plugin 2.2.40
- Designvertrag V104
ABHÄNGIGKEITEN:
- WordPress >= 6.0
- PHP >= 7.4
- HivePress-Funktionen nur bei entsprechender Nutzung
NUTZENDE PROJEKTE:
- PFERDE_ATELIER → eigene Projektlinie unter `PROJEKTE/PFERDE_ATELIER/DESIGN/`
BELEG:
- übergebener Universal Plugin/Master
- GitHub `UNIVERSAL_STATUS.md` auf Commit `f1e074b...`
ARCHIV:
`/Campus-Archiv/ALLGEMEINGUELTIGE_BAUSTEINE/DESIGN/2026-09-05/`

## MOD-004 – HIVEPRESS-ANZEIGENSUCHE

MODULKLASSE: UNGEKLÄRT
STATUS: als separater Plugin-/Source-Baustein in Universal- und Pferde-Designmaster erkannt; eigener Audit noch offen
BELEGE:
- Universal: `UNIVERSAL_HIVEPRESS_ANZEIGENSUCHE_v2.1.5_AJAX_ANZEIGENKATEGORIEN_INSTALLIEREN.zip`
- Pferde: `PFERDE_ATELIER_HIVEPRESS_ANZEIGENSUCHE_v2.1.5_AJAX_ANZEIGENKATEGORIEN_INSTALLIEREN.zip`
REGEL:
Nicht im Designmaster verlieren, aber vor eigenem Audit noch nicht als vollständig allgemeingültiges Modul freigeben.
