# ÄNDERUNGS- UND ERKLÄRUNGSREGISTER

STAND: 2026-09-05

Zweck: **Was wurde geändert – und warum?**

Wenn WARUM nicht belastbar geklärt ist:
`WARUM: UNGEKLÄRT`
`ENTFERNBAR: NEIN, BIS GEKLÄRT`

## ARCH-001 – Campus/Bürogebäude-Modell
WARUM: neue Chats sollen ohne Vorwissen Stand, Regeln, Fehler und Arbeitswege finden.

## ARCH-002 – Hauptpförtner als Resetpunkt
WARUM: bei Kontextverlust neu lesen statt raten.

## ARCH-003 – Ein Hobbyraum pro Büro
WARUM: Seitensprünge und Parallelreparaturen verhindern.

## ARCH-004 – Paul isoliert über eigenen Branch
WARUM: freie Analyse/Tests ohne Einfluss auf offizielle Stände.

## ARCH-005 – Modulares Gebäude
WARUM: Räume/Büros/Projekte ohne Gesamtumbau ergänzen können.

## ARCH-006 – PROJECT_MEMORY unter protocol/
WARUM: bestehender hardlock deckt `protocol/**` bereits ab.
BELEG: Draft-PR #134.

## ARCH-007 – Notfall-Tresor
WARUM: Wiederaufbau aus geprüftem Gesamtstand.

## ARCH-008 – Organischer Campus
WARUM: Struktur soll mit der realen Arbeit wachsen statt vorab starr festgelegt zu werden.

## ARCH-009 – Allgemeingültige Bausteine
WARUM: geprüfte universelle Module projektübergreifend wiederverwenden.

## ARCH-010 – Vollständige Masterdatei-Verwertung
WARUM: auch Altstände, Tests, Fehlergründe und Produktionshistorie erhalten.

## ARCH-011 – BILD-Büro
WARUM: Pferde-Atelier-spezifische Bildnutzung braucht eigenes Fachgedächtnis.

## ARCH-012 – Zentrales Modulregister
WAS: ein einziger Campus-Karteikasten für vorhandene Module und deren Hauptorte.
WARUM: der Nutzer soll nicht erinnern müssen, was bereits allgemeingültig existiert.
REGEL: keine zweite technische Wahrheit; Modulregister verweist auf die Hauptquelle.

## ARCH-013 – Modulklasse und Masterakte getrennt
WAS: Modulklasse = ALLGEMEINGÜLTIG / PROJEKTBEZOGEN / UNGEKLÄRT. GEMISCHT gilt nur für Masterakten/Artefaktpakete.
WARUM: ein allgemeiner Plugin-Kern kann in einer projektspezifischen Masterakte stecken. Vermischung würde allgemeine Module fälschlich projektgebunden machen.
BEISPIEL: MOD-002 Bildzentrale ist ALLGEMEINGÜLTIG; Pferde-Atelier-Bildakten enthalten Projektdaten/Config/History.
ENTFERNBAR: nein.

## ARCH-014 – Oberwachtmeister als Ablauf, nicht als Agent
WAS: „Oberwachtmeister“ bezeichnet nur den Projektstart-Prozess.
WARUM: kein neues Büro/Agent/Controller nötig; KISS.
REGEL: Modulregister prüfen, nur relevante Module lesen, minimales Projektgebäude anlegen.

## BILD-001 – Lokaler Magnific-Readback 2.4.9
WARUM: temporäre externe Magnific-URLs liefen ab; lokale WordPress-URL muss Vorrang haben.
BELEG: BILD-Masterdatei 049.

## BILD-002 – Allgemeingültige Bildzentrale 2.6.9
WAS: allgemeiner Modul-Kern für Beiträge, WP-Taxonomien, optional HivePress, Pixabay/Pexels/Magnific, Profile, Export/Import, Readback-Fallback.
BELEG: Nutzerbestätigung 2026-09-05.
OFFEN: 2.6.9-Codeprüfung nach Dateiauslieferung.

## TECH-KEYFLOW-001 – Schlüsselübergabe
Bereich: TEXT
WARUM: UNGEKLÄRT.
ENTFERNBAR: NEIN, BIS GEKLÄRT.


## ARCH-015 – Zentraler Zielvertragsraum
WAS: `ZIELVERTRAEGE/` mit einem zentralen Register.
WARUM: verbindliche Endziele dürfen nicht nur in Chats/Übergaben leben oder mit CURRENT_STATE vermischt werden.
REGEL: aktive Verträge referenzieren; Änderungen versionieren, nicht still überschreiben.

## ARCH-016 – Campus-Archiv mit automatischer Zuordnung
WAS: `ARCHIV/` als historischer Aktenraum.
WARUM: der Nutzer soll Dateien nur bereitstellen müssen, nicht selbst archivieren/sortieren.
REGEL: bereits erreichbare Dateien benötigen keinen erneuten Upload; lokale-only Dateien müssen einmal bereitgestellt werden.

## ARCH-017 – Zugriffsschutz des Campus
STATUS: OFFENE ARCHITEKTURENTSCHEIDUNG
EMPFEHLUNG: eigener privater Campus-Repository statt Passwortdateien im öffentlichen Projekt-Repository.
WARUM: der Campus soll mehrere Projekte umfassen und zentrale Projektakten schützen; Verschlüsselung/Passwortdateien würden Suche, Pförtner und Automatisierung erschweren.
BIS ZUR ENTSCHEIDUNG: keine Secrets in den öffentlichen Campus-Prototyp.


## ARCH-018 – Architektur-Sonderrecht für jeden Chat
WAS:
Jeder Chat darf bei einem konkret in der täglichen Arbeit erkannten Optimierungsbedarf die Campus-Architektur selbst verbessern.
WARUM:
Architektur soll aus realer Nutzung lernen; Verbesserungen dürfen nicht an einen speziellen Architekten-Chat oder spätere Erinnerung gebunden sein.
GRENZE:
Nur Architektur-Ebene; keine fremde Facharbeit, kein Maschinenraum-Umbau ohne Fachauftrag.
PFLICHT:
KISS + Bauprotokoll + ggf. Architektur-Fehlerkiste + dauerhaftes WHY.

## ARCH-019 – Bauprotokoll und Architektur-Fehlerkiste
WAS:
Der Baucontainer erhält eigenes Arbeitsprotokoll und eigenes Fehlerregister.
WARUM:
Die Architektur und der „Architekt“ müssen denselben Lern- und Fehlerregeln unterliegen wie Fachsysteme.
BELEG:
`BAUCONTAINER/BAUPROTOKOLL.md`
`BAUCONTAINER/ARCHITEKTUR_FEHLERKISTE.md`

## ARCH-020 – Campus-Hausmeister
WAS:
Wiederholbarer Wartungsprozess zum Schlankhalten produktiver Räume.
WARUM:
Historischer Ballast soll erhalten, aber aus aktiven Arbeitsräumen herausgehalten werden.
REGEL:
Nur eindeutig HISTORISCH/ABGELÖST nach Referenzprüfung archivieren; AKTIV/UNGEKLÄRT tabu; keine Löschung.
BELEG:
`BAUCONTAINER/HAUSMEISTER.md`
`ARCHIV/HAUSMEISTER_PROTOKOLL.md`


## ARCH-021 – Pförtner und Hausmeister sind reine Verwaltung
WAS:
Hauptpförtner und Hausmeister dürfen keinerlei Fachinhalt verändern.
WARUM:
Navigation und Ordnung dürfen niemals unbemerkt fachliche Wahrheit erzeugen oder verändern.
PFÖRTNER:
READ/ROUTE ONLY.
HAUSMEISTER:
unverändert ordnen/archivieren + Verwaltungsprotokoll; keine Fachdatei editieren.
REGEL:
Ein Chat muss die Verwaltungsrolle ausdrücklich verlassen, bevor er Fach- oder Architekturarbeit beginnt.

## ARCH-022 – 1-Klick-Eingangsstandard
WAS:
Campus-, Gebäude-, Büro- und Paul-Eingänge beginnen mit derselben kurzen 1-KLICK-ÜBERSICHT.
WARUM:
Ein völlig neuer Chat soll ohne Vorwissen auf dem ersten Bildschirm verstehen: Zweck, Zuständigkeit, Rechte, Verbote und nächsten Schritt.
REGEL:
Neue Gebäude/Büros nur mit `BAUCONTAINER/EINGANGSSTANDARD.md`.
LEITSATZ:
**Ein Klick = alles klar.**
