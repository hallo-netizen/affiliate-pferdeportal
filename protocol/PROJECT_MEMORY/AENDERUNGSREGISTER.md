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
AKTUELL: exakter 2.6.9-Dateibeleg vorhanden; eine Fachprüfung wurde im Sortierauftrag bewusst nicht durchgeführt.

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


## ARCH-023 – Entwicklungsprotokoll für den Architektur-Austausch
WAS:
Der Baucontainer erhält `ENTWICKLUNGSPROTOKOLL.md` für Ideen, Einwände, Nutzerkorrekturen, verworfene Varianten und offene Architekturfragen.
WARUM:
Nicht nur fertige Umbauten, sondern auch der nachvollziehbare Gedankenweg soll erhalten bleiben, ohne BAUPLAN oder AENDERUNGSREGISTER aufzublähen.
REGEL:
Nicht als aktuelle Hauptwahrheit verwenden.
TRENNUNG:
Entwicklungsweg = ENTWICKLUNGSPROTOKOLL; gebaut = BAUPROTOKOLL; dauerhaft gültig/WHY = AENDERUNGSREGISTER.


## ARCH-024 – Campusweites WordPress-Register
WAS:
`WORDPRESS_REGISTER.md` als zentraler Technologieindex für bereits vorhandene WordPress-Plugins/Installer.
WARUM:
Der Nutzer soll sofort sehen können, welche WordPress-Werkzeuge bereits vorhanden sind, ohne sich Dateinamen/Projekte merken zu müssen.
KISS:
Kein neues WordPress-Büro, solange keine eigene dauerhafte WordPress-Facharbeit entsteht.
GRENZE:
Modulklasse bleibt ausschließlich im MODULREGISTER; LIVE-/Release-/Fachstatus bleibt ausschließlich an der zuständigen Originalquelle.
REGEL:
Große Masterpakete werden nicht allein wegen ihres Dateinamens als WordPress-Plugin klassifiziert.


## ARCH-025 – Archiv-Ampel für lokale Originale
WAS:
ROT/GELB/GRÜN-Status im Archiv.
WARUM:
Der Nutzer soll nicht selbst beurteilen müssen, ob eine Datei sicher genug archiviert ist, um die lokale Originalkopie zu entfernen.
REGEL:
GRÜN nur bei Hash + mindestens zwei unabhängigen verifizierten Speicherorten.
Nur GRÜN darf `LOKALE_KOPIE_ENTBEHRLICH: JA` setzen.
AKTUELL:
Kategoriemodul = GELB; ChatGPT-Library-Archiv vorhanden, zweite unabhängige Ablage fehlt noch.


## ARCH-026 – Masterakten werden immer gegen aktuelles GitHub zusammengeführt
WAS:
Neue Master-/Pluginakten werden nicht isoliert inventarisiert, sondern gegen aktuellen main, relevante Fachbranches, Release-/Live-Belege und technische Originalquellen abgeglichen.
WARUM:
Masterdateien können älter als spätere GitHub-Arbeit sein; main kann zugleich älter als ein bestätigter Live-Fachbranch sein.
DESIGN-BELEG:
Masterbasis Pferde 1.50.469; main 1.50.421; bestätigter Fachbranch-LIVE 1.50.472.
REGEL:
Widerspruch = sichtbar dokumentieren; Autorität anhand Belegen bestimmen; niemals einfach „neueste Datei gewinnt“.


## ARCH-027 – Alltagssprache als Campus-Einstieg
WAS:
Eindeutige natürliche Sprache ist ein gültiger Routingauftrag.
WARUM:
Der Nutzer soll keine Kommandos oder Dateipfade auswendig lernen.
REGEL:
Bei Eindeutigkeit routen; bei Mehrdeutigkeit STOPP – NICHT RATEN.

## ARCH-028 – Sonderräume folgen dem 1-Klick-Standard
WAS:
Archiv, Zielverträge, Baucontainer und Tresor besitzen eigene START_HERE-Eingänge.
WARUM:
„Ein Klick = alles klar“ muss campusweit gelten, nicht nur für Büros.

## ARCH-029 – Paul TEXT/SEO mit direkter Quellenkette
WAS:
Sechs aktuelle Nutzerakten liegen wortgleich im TEXT-Büro; Paul besitzt einen direkten TEXT/SEO-Einstieg.
WARUM:
Paul soll ohne Chatvorgeschichte Ziel, Status, Protokoll, Fehler und Sperren finden.
GRENZE:
Keine inhaltliche Umschreibung; technische Originalquellen bleiben autoritativ.

## ARCH-030 – Tresor fail-closed
WAS:
Tresor zeigt explizit PASS oder den ersten blockierenden FAIL.
WARUM:
Ein konzeptionell vorhandener Tresor darf nicht mit einem real geprüften Backup verwechselt werden.
AKTUELL:
`TRESOR_FAIL:RECOVERY_DEPENDENCIES_UNVERIFIED`.


## ARCH-031 – Externer Tresor-Git-/Metadaten-PREPASS
WAS:
Vollständiger Git-Bundle-Mirror plus paginierter GitHub-Metadaten-Snapshot wird außerhalb GitHub versioniert gespeichert und real restore-getestet.
WARUM:
Ein Tresor im selben Repository würde bei Repositoryverlust mit verloren gehen.
BELEG:
`/Campus-Tresor/LATEST_PREPASS.txt` → jeweils aktuellster externer manifestgebundener PREPASS
RESTORE:
`GIT_BUNDLE_RESTORE_PASS`
GRENZE:
Noch kein TRESOR_PASS, solange nicht exportierbare Recovery-Abhängigkeiten nicht vollständig verifiziert sind.


## ARCH-032 – Dauerhafte Eingangadressen
WAS:
Bereits verteilte Campus-/Gebäude-/Büro-/Paul-Adressen bleiben stabil.
WARUM:
Ein alter Chat oder Paul-Auftrag darf nicht durch stilles Umbenennen ins Leere laufen.
REGEL:
Bei späterem Umbau bleibt die alte Adresse als Weiterweiser bestehen.

## ARCH-033 – Hobbyraum-Standard + Routing-Kennwort
WAS:
Ein Hobbyraum pro Büro; Zustände FREI / AKTIV / BLOCKED; „Hobbyraum“ ist ein Routing-Kennwort, kein Passwort.
WARUM:
Aktuelle Arbeit muss eindeutig gebunden sein, ohne Scheinsicherheit durch ein Geheimwort im öffentlichen Repository.
BELEG:
`BAUCONTAINER/HOBBYRAUM_STANDARD.md`

## ARCH-034 – Keine temporären Chatrechte in Dauerakten
WAS:
Dauerhafte START_HERE-/HOBBYRAUM-Akten werden nicht an „diesen Chat“, „Sortierchat“ oder veraltete Parallelchat-Hinweise gebunden.
WARUM:
Neue Chats/Paul müssen dieselben Türen widerspruchsfrei verwenden können.


## ARCH-035 – Büro-Kommunikationsleitungen auch bei Direkteinstieg
WAS:
Jedes Pferde-Atelier-Büro verweist bei echter Arbeit sichtbar auf Hobbyraum, Handlungsverzeichnis, Fehlerregister, Änderungsregister und Zielvertragsregister.
WARUM:
Ein direkter Büro-Link darf den Hauptpförtner nicht umgehen und dadurch Sicherheits-/Kontextleitungen verlieren.

## ARCH-036 – Hobbyräume sind selbst erklärende Eingänge
WAS:
Alle sechs Pferde-Atelier-Hobbyräume erfüllen ebenfalls die 1-Klick-Übersicht.
WARUM:
Der Nutzer kann direkt „Büro → Hobbyraum“ adressieren; auch dort müssen Rechte, Status und nächster Schritt sofort klar sein.


## ARCH-037 – Projekt-Flur mit eigenem Eingang
WAS:
`PROJEKTE/START_HERE.md` erklärt den Weg zu registrierten Projektgebäuden.
WARUM:
Auch ein direkter Einstieg eine Ebene oberhalb des Pferde-Ateliers muss selbsterklärend sein.

## ARCH-038 – Ungeklärter Affiliate-Bestand wird sichtbar gekennzeichnet
WAS:
Der bestehende Ordner `ALLGEMEINGUELTIGE_BAUSTEINE/AFFILIATE/` erhält START_HERE + CURRENT_STATE mit MODULKLASSE UNGEKLÄRT.
WARUM:
Der technische Ablageort darf keine falsche Allgemeingültigkeitsfreigabe suggerieren.

## ARCH-039 – Tresor prüft Roharchiv-Redundanz vor Recovery-Secrets
WAS:
Der erste Tresorblocker wird aus dem eigenen Inhaltsvertrag korrekt auf fehlende unabhängige Roharchiv-Redundanz gesetzt.
WARUM:
Git-Mirror und GitHub-Metadaten sichern nicht automatisch die großen Rohmaster in der ChatGPT-Library.
AKTUELL:
`TRESOR_FAIL:ARCHIVE_RAW_ARTIFACTS_NOT_REDUNDANT`


## ARCH-040 – Jedes PROJECT_MEMORY-Verzeichnis hat START_HERE
WAS:
Jede reale Verzeichnisebene im Campus besitzt eine eigene Eingangstafel.
WARUM:
„Egal wo man eintritt“ darf nicht nur für ausgewählte Haupttüren gelten.
ABNAHMEBELEG 2026-09-05:
22/22 PROJECT_MEMORY-Verzeichnisse mit START_HERE; 22/22 Eingänge erfüllen nach Reparatur die 1-Klick-Pflicht.


## ARCH-041 – Neubauvorlage muss aktuellen Campusstandard erzwingen
WAS:
NEUES_PROJEKT_VORLAGE bindet künftig Flur-/START_HERE-Regel, Büro-Kommunikationsleitungen, Hobbyraum-Standard und Positiv-/Negativ-Abnahme.
WARUM:
Die Bauabnahme darf nicht nur den heutigen Bestand reparieren; neue Gebäude dürfen alte Architekturfehler nicht reproduzieren.
