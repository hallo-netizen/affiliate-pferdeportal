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

## TECH-KEYFLOW-001 – Signier-/Schlüsselgrenze
Bereich: TEXT
STATUS: GEKLÄRT / 2026-09-05.
WAS:
Innerhalb der Produktionsstraße keine kryptografische Raum-/Worker-Signierung. Interne Sicherheit erfolgt über Single-Door/Wächter, Hash-/Herkunftsbindung, reale Fachprüfungen und PASS/Receipt. Kryptografische Versiegelung beginnt erst nach abgeschlossener Produktion außerhalb des Workers.
WARUM:
Das frühere Raum-zu-Raum-Signiermodell erzeugte Signer-/Key-/Übergabeabhängigkeiten und widersprach der später bewusst vereinfachten Ein-Tür-Architektur. Die kryptografische Funktion wird intern nicht benötigt, solange der gebundene Weg und die unveränderten Fachprüfungen fail-closed erzwungen werden; sie bleibt an der externen Manipulationsgrenze notwendig.
BELEG:
Draft-PR #140, Head `c3244d5bf838817078a3821c045fb52e86f3db46`: interne ED25519-/Signer-Pflichten aus aktivem 107007-Vorlauf entfernt; `hardlock` + `hardlock-base` PASS. Externe 107008-/ENDSTEMPEL-/WordPress-Signierung unangetastet.
REGEL:
Keine interne Signierpflicht wiedereinführen. Externe Signierstufen nur nach separater Positiv-/Negativprüfung vereinfachen.


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
`TRESOR_FAIL:ARCHIVE_RAW_ARTIFACTS_NOT_REDUNDANT`.


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


## ARCH-042 – Eine Wahrheit besser ausgeschildert
WAS:
Gebäude, alle sechs Büros, Hobbyräume, Archiv, Fehlerregister und Paul zeigen jetzt einheitlich auf die jeweils eine zuständige Quelle.
WARUM:
Der Fremdnutzer-Test zeigte: Informationen waren vorhanden, aber der aktuelle Arbeitspunkt musste noch zu stark zusammengesetzt werden.
REGEL:
START_HERE = Wegweiser; CURRENT_STATE = Bürostand; HOBBYRAUM = aktuelle Arbeit; Register = Index zur Hauptquelle.
KEINE NEUE WAHRHEIT:
Kein neues TextSEO-Büro, keine zweite Fehlerliste, kein zweiter Zielvertrag, kein paralleler Kurzstatus.

## ARCH-043 – Dynamische Fakten nicht in Wegweisern doppeln
WAS:
Dynamische Versions-/Historienangaben werden aus Wegweisern entfernt, wenn sie bereits im CURRENT_STATE oder einer Originalquelle geführt werden.
WARUM:
Wegweiser dürfen nicht veralten und dadurch zur konkurrierenden Wahrheit werden.


## ARCH-044 – Paul ist isolierter Spezialworker, kein normaler Arbeitsweg
WAS:
Paul ist ausschließlich ein ausdrücklich beauftragter Spezialworker. Normale Arbeitschats werden nicht automatisch zu Paul geroutet.
WARUM:
Der ursprüngliche Zweck von Paul war freie Analyse/Tests auf eigenem Branch ohne Einfluss auf offizielle Stände. Eine normale Weiterleitung aus dem TEXT-Hobbyraum vermischte Arbeitschat und Spezialworker und erzeugte unnötiges Parallelitäts-/Synchronisationsrisiko.
REGEL:
Paul darf alle Campus-/Büro-/Fachquellen lesen, aber keine Datei unter `protocol/PROJECT_MEMORY/**` verändern. Technische Writes nur im ausdrücklich gebundenen Schreibbereich auf eigenem `paul/*`-Branch. Integration/Merge ausschließlich durch zuständigen Arbeitschat.

## ARCH-045 – Single Writer, Multi Reader
WAS:
Für jede offizielle Büro-/Campuswahrheit und jeden konkreten technischen Schreibbereich gibt es gleichzeitig genau einen Schreiber.
WARUM:
Unabhängige Chats besitzen keine verlässliche Echtzeit-Synchronisation. Gleichzeitige Writes am selben Bereich erzeugen Konflikte, veraltete Annahmen und doppelte Wahrheiten.
REGEL:
Mehrere dürfen lesen. Parallel gearbeitet wird nur an klar unabhängigen Bereichen. Spezialworker liefern Lösungspakete; der zuständige Arbeitschat integriert.


## ARCH-046 – Worker-Branches sind keine Statusquelle
WAS:
Pauls eigener Branch ist ausschließlich technische Werkbank. Büro-/Campusstand wird vor Start und vor Rückgabe frisch aus dem offiziellen Campus-Ref gelesen.
WARUM:
Branches synchronisieren sich nicht in Echtzeit. Eine PROJECT_MEMORY-Kopie auf einem Worker-Branch kann während paralleler Arbeit veralten.
REGEL:
Bei relevantem Drift `STALE_ASSIGNMENT` und stoppen; keine Lösung auf veralteter Annahme integrieren.


## ARCH-047 – Paul-PROJECT_MEMORY-Sperre gehört in den vertrauenswürdigen Base-Hardlock
WAS:
Ein `paul/*`-PR, der `protocol/PROJECT_MEMORY/**` verändert, soll technisch mit `PAUL_PROJECT_MEMORY_WRITE_BLOCKED` scheitern.
WARUM:
Die reine Rollenregel schützt gegen versehentliche Parallelwrites, aber nur der vertrauenswürdige Base-Hardlock kann verhindern, dass ein Worker seine eigene Sperre im PR umgeht.
KISS:
Eine einzige zusätzliche Diff-Prüfung im bestehenden `hardlock-base`; kein neuer Runner, kein neuer Statusspeicher.
AKTUELL:
Security-PR #137 vorbereitet. Aktivierung auf `main` ist noch BLOCKED durch den absichtlichen Selbstschutz `IMMUTABLE_SECURITY_PATH_CHANGE_BLOCKED` und erfordert den bestehenden bewussten Admin-Wartungsweg.


## ARCH-048 – Universelle Protokollpflicht an jedem Abschluss
WAS:
Vor `fertig`, `PASS` oder Übergabe muss jeder Arbeitschat – unabhängig von Ebene oder Raum – frisch prüfen, ob Fehlerquelle, Arbeits-/Bauprotokoll, dauerhaftes WARUM, CURRENT_STATE, HOBBYRAUM/NEXT ACTION oder Zielvertrag tatsächlich betroffen sind.
WARUM:
Eine einmal am Chatbeginn gelesene Anweisung kann im langen Verlauf vergessen werden. Die Pflicht muss deshalb dauerhaft am Campus-Einstieg und im Eingangsstandard sichtbar bleiben und bei jedem Abschluss erneut greifen.
REGEL:
Nicht pauschal Dateien anfassen. Nur tatsächlich betroffene autoritative Stellen aktualisieren; keine zweite Wahrheit erzeugen; technische FAIL/BLOCKED-Zustände niemals durch Chat-PASS ersetzen.


## ARCH-049 – Architektur darf dynamische Arbeitsbindung nicht erfinden
WAS:
STATUS, Worker, Branch und NEXT ACTION im HOBBYRAUM dürfen bei Architektur-/Routingarbeiten nur geändert werden, wenn eine neue Arbeitszuweisung frisch belegt oder ausdrücklich vom Nutzer erteilt ist.
WARUM:
Bei der Paul-Isolationsreparatur wurde die Rollenarchitektur korrekt geändert, aber der TEXT-Hobbyraum fälschlich von einer bestehenden Paul-Bindung auf `TEXT-ARBEITSCHAT FÜHRT` umgedeutet.
REGEL:
Architektur ändert die Regeln um eine bestehende Arbeitsbindung herum; sie ersetzt die dynamische Bindung nicht aus eigener Annahme.


## ARCH-050 – PROJECT_MEMORY-Protokollpflicht wird technisch fail-closed
WAS:
Jeder PR mit Änderungen unter `protocol/PROJECT_MEMORY/**` muss einen maschinenlesbaren `PROTOKOLLCHECK` im PR-Text enthalten. Der trusted `hardlock-base` vergleicht diesen Block mit dem tatsächlichen Diff.
WARUM:
Die bisherige Protokollpflicht war nur dokumentiert. Ein langer Chat – auch der Baucontainer-Chat selbst – kann sie vergessen. Die Erinnerung muss deshalb außerhalb des Chatgedächtnisses liegen und vor Integration technisch blockieren.
KISS:
Kein neuer Runner und keine zweite Statusdatei. Eine einzige zusätzliche Prüfung im bestehenden trusted Base-Hardlock.
GRENZE:
Der Check kann bewusste Falschangaben nicht vollständig beweisen; er erzwingt aber Vollständigkeit, offensichtliche Diff-Widersprüche, PASS für Eine Wahrheit/Tests und die Architektur-Protokollkopplung.
AKTUELL:
Im Security-PR #137 implementiert; Aktivierung auf main weiterhin durch die bestehende immutable-Security-Wartungsgrenze BLOCKED.


## ARCH-051 – Sicherungslogik besitzt eingebaute Positiv-/Negativ-Selbsttests
WAS:
Die vorbereitete trusted `hardlock-base`-Erweiterung testet bei jedem Lauf ihre Paul-Pfadgrenze und den PROJECT_MEMORY-PROTOKOLLCHECK selbst mit positiven und negativen Fällen.
WARUM:
Eine Sicherung darf nicht nur existieren; spätere Änderungen müssen auch beweisen, dass erlaubte Fälle erlaubt und verbotene Fälle weiterhin blockiert werden.
BEFUND:
Der erste externe Logiktest fand eine reale Lücke bei `ZIELVERTRAEGE/REGISTER.md`. Nach KISS-Fix wurde der vollständige Testblock erneut ausgeführt.
ERGEBNIS:
Pfad-/Paul-Regel 5/5 PASS; PROTOKOLLCHECK 17/17 PASS; gesamt 22/22 PASS.
GRENZE:
Das ist ein harter Logiktest des exakten Kandidatenverhaltens. Der echte serverseitige Required-Check kann erst nach der einmaligen Admin-Aktivierung von Security-PR #137 bewiesen werden.


## ARCH-052 – Paul holt seinen Auftrag automatisch aus der einzigen Hobbyraum-Wahrheit
WAS:
Pauls aktuelle Zuweisung wird ausschließlich als maschinenlesbarer `PAUL_ASSIGNMENT_V1` direkt im zuständigen `HOBBYRAUM.md` geführt. Paul erzeugt/erhält keinen täglich neu geschriebenen Übergabeprompt.
WARUM:
Eine separate Paul-Auftragsakte oder synchronisierte Kopie würde eine zweite Wahrheit und zusätzlichen Pflegebedarf erzeugen. Der Campus soll alleinige aktuelle Wahrheit bleiben.
REGEL:
Null aktive Paul-Blöcke = `PAUL_NOT_ASSIGNED`; mehr als einer = `PAUL_MULTIPLE_ASSIGNMENTS_BLOCKED`. Problem/Ziel/Regeln nur als Verweis auf autoritative Quellen.

## ARCH-053 – Paul-Scope-Gate ergänzt, aber ersetzt nicht die bestehende Cloud-Eingangstür
WAS:
Auf `paul/*` bleibt `cloud_entry.py start` zwingend erster Schritt. Danach prüft ein trusted `paul_scope_gate.py start` automatisch aktuelle Campuszuweisung, Branch, technische Basis und Write-Scope; vor Rückgabe folgt `verify`.
WARUM:
Ein unabhängiger zweiter Bootstrap hätte die vorhandene deterministische Eingangstür konkurriert. Die neue Schicht darf nur Worker-Berechtigung/Frische begrenzen, nicht den Workflow auswählen.
KAPSEL:
`.paul-capsule/` ist temporär, nicht eingecheckt, hashgebunden und keine Wahrheit.
DRIFT:
Nur HOBBYRAUM, zuständiger CURRENT_STATE sowie gebundene TASK-/TARGET-/RULES-Originalquellen blockieren bei Änderung; fremde Campusänderungen nicht.


## ARCH-054 – Paul-Automatik ist Worker-Automatik, keine behauptete Chat-Autostart-Funktion
WAS:
Die technische Startautomatik wird über repositoryweites `AGENTS.md` + trusted Paul-Scope-Gate für Repo-/Codex-Worker erzwungen; GitHub-Hardlock erzwingt die Zuweisungs-/Scopegrenze am Integrationsweg.
WARUM:
Ein gewöhnlicher freier Chat kann nicht allein durch eine Repository-Datei beim Öffnen automatisch Code ausführen. Diese Produktgrenze darf nicht als gelöste Technik behauptet werden.
REGEL:
Kein neuer Übergabeprompt nötig. Für Worker automatisch; für beliebige Chats bleibt der Campus die Wahrheit und GitHub blockiert unautorisierte Paul-Integration fail-closed.


## ARCH-055 – Pauls technischer Scope ist exklusiv und jeder Auftrag startet auf frischem Branch
WAS:
Während eines aktiven Paul-Auftrags ist dessen `WRITE_SCOPE` für andere PRs gesperrt. Jeder neue Paul-Auftrag startet auf einem frischen `paul/*`-Branch direkt vom `TECHNICAL_BASE_SHA`.
WARUM:
Nur Paul einzuschränken reicht nicht; sonst könnte der normale Arbeitschat denselben technischen Bereich parallel verändern. Wiederverwendete Paul-Branches tragen außerdem Altcommits in neue Aufträge.
REGEL:
Kollidierender Fremd-PR → `PAUL_EXCLUSIVE_SCOPE_LOCKED`. Alter/inkonsistenter Paul-Branch → Scope-/Base-Block.


## ARCH-056 – TEXT/SEO-Historienarchive und TEXT/SEO-Dependencies werden nicht zu CURRENT hochgestuft
WAS:
Master 0057 Teil A wird ausschließlich als unveränderliches TEXT/SEO-Historienarchiv geführt. LanguageTool 6.8 wird als **TEXT/SEO-spezifische Offline-Abhängigkeit** archiviert, nicht als Plugin oder allgemeingültiges Modul.
WARUM:
Beide Uploads stammen aus älteren Produktionsmaster-Zusammenhängen. Der 0057-README bindet seinen Inhalt ausdrücklich an `98_HISTORY_READ_ONLY`; der 0043-README bezeichnet LanguageTool ausdrücklich als unveränderte Offline-Abhängigkeit. Auf aktuellem `main` wurde kein LanguageTool-Pfad/-Code gefunden.
REGEL:
Beide Bestände gehören fachlich zu TEXT/SEO. Historischer Nachweis darf Auffindbarkeit ermöglichen, aber ohne neuen aktuellen Beleg weder CURRENT_STATE noch aktive Nutzung verändern.
