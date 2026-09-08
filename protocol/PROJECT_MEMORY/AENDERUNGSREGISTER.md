# ÄNDERUNGS- UND ERKLÄRUNGSREGISTER

STAND: 2026-09-08

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
Draft-PR #140, Head `7990029428399e8ba01d88a6543ce068812e9218`: aktiver interner Call-Graph bis 107007 ohne ED25519-/Signer-/Key-/`SIGNED`-Pflicht; gebundenes H8-Paket `WORKFLOW_SUPERVISOR_RELEASE_V2_HASH_BOUND` ohne Signaturfelder; `hardlock` + `hardlock-base` PASS. Erst `finalize_after_107008` erzeugt den externen signierten Release; ENDSTEMPEL-/WordPress-Signierung bleibt unangetastet.
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


## ARCH-057 – Tresor/Archiv/Mirror sind campusweit keine Arbeitsquelle
WAS:
Backup-, Archiv- und Mirrorbestände werden von jeder normalen Arbeitsausführung getrennt.
WARUM:
Ein Nachbarchat wollte den vorhandenen Campus-Tresor/Git-Mirror als „kürzesten sauberen Weg“ verwenden, um einen Runner direkt auszuführen. Das hätte einen Sicherungsstand zur Arbeitsquelle gemacht und die Workflowbindung umgangen.
REGEL:
READ/VERIFY/RESTORE ONLY. Keine Runner, Tests, Reparaturen, Produktion oder Releases aus Tresor/Archiv/Mirror. Restore erst in frischen Arbeits-Worktree außerhalb der Sicherungsbereiche; danach offizielles GitHub-origin + normale Eingangstür.
TECHNIK:
Vorbereitet in Security-PR #137 durch die bestehende `cloud_entry.py`: Backup-Pfad, Bare-Mirror, Tresor-/Archiv-Gitdir und lokaler Mirror-origin werden fail-closed blockiert.


## ARCH-058 – Paul-Frische ist Start + Driftblock + Refresh, keine Live-Synchronisation
WAS:
Paul liest bei jedem Start den frisch geholten offiziellen Campus und materialisiert daraus nur einen temporären hashgebundenen Snapshot. Vor Rückgabe/Integration wird der Campus erneut frisch gelesen.
WARUM:
Unabhängige Branches/Chats können nicht zuverlässig live synchronisiert werden. Entscheidend ist deshalb nicht „sekündlich dieselbe Kopie“, sondern dass Paul nie gültig auf einem veralteten relevanten Stand abschließen kann.
REGEL:
- alte PROJECT_MEMORY-Kopie auf Pauls Branch wird ignoriert;
- Start nimmt den neuesten offiziellen Campus;
- Änderung an zuständigem CURRENT_STATE, HOBBYRAUM oder gebundener TASK-/TARGET-/RULES-Quelle → `STALE_ASSIGNMENT_BLOCKED`;
- neuer Start lädt den neuen Campusstand automatisch;
- irrelevante Campusänderungen blockieren Paul nicht.
BELEG:
Security-Head `9e0340d55ce9c7359fed28e171143a54d4cad5ab`, echter GitHub-`hardlock` SUCCESS mit `PAUL_CURRENT_CAMPUS_CI_PASS`.

## ARCH-059 – Paul-Snapshots bewahren Quelltext byte-näher ohne strip
WAS:
`git show` für Paul-Quellen wird nicht mehr über eine globale `.strip()`-Rückgabe gelesen.
WARUM:
Der harte Frischetest zeigte, dass führende/abschließende Whitespace-Änderungen sonst aus dem Snapshot verschwinden und damit theoretisch nicht als Drift erkannt werden könnten.
KISS:
Nur `show()` liest stdout unverändert; Ref-/Branch-Kommandos behalten die bestehende getrimmte Ausgabe.


## ARCH-060 – Lokaler Tresor wird als unabhängiger versionierter Snapshot gebaut
WAS:
Git/GitHub, Campus-Archiv und Recovery-Unterlagen werden in einem versionierten lokalen Snapshot zusammengeführt. Jeder Snapshot prüft Git-Restore und Rohdatei-Hashes.
WARUM:
Der vorhandene Git-/GitHub-PREPASS bewies die Wiederherstellbarkeit des Git-Teils, deckte aber die großen Library-Roharchive und nicht exportierbare Secrets nicht ab. Außerdem veraltet ein alter PREPASS nach weiterer Campusarbeit.
REGEL:
Alter PREPASS = Restore-Beweis, nicht automatisch aktueller Backupstand. Jeder 1:1-Snapshot wird frisch erzeugt.

## ARCH-061 – LOCAL_BACKUP_PASS und TRESOR_PASS bleiben getrennt
WAS:
Das lokale Werkzeug darf nur `LOCAL_BACKUP_PASS` melden.
WARUM:
Eine technisch perfekte Kopie eines bereits unvollständigen Rohbestands ist noch kein vollständiger Katastrophen-Tresor.
REGEL:
`TRESOR_PASS` erst nach zusätzlicher Prüfung aller erforderlichen Originalartefakte und Recovery-Abhängigkeiten.

## ARCH-062 – ENDSTEMPEL_PRIVATE_KEY ist bestätigte Recovery-Abhängigkeit
WAS:
Der Workflow nutzt `secrets.ENDSTEMPEL_PRIVATE_KEY`.
WARUM:
GitHub Actions Secrets sind nicht als Originalwert wieder auslesbar. Ein 1:1-Wiederaufbau ohne unabhängige Recovery-Quelle wäre nicht möglich.
REGEL:
Secret niemals in Campus/Git/Chat kopieren; nur sichere externe Recovery-Quelle + praktischer Recovery-Test dürfen PASS begründen.


## ARCH-063 – Paul-Frische wird von der einzigen Cloud-Eingangstür automatisch erzwungen
WAS:
`cloud_entry.py` ruft auf jedem `paul/*`-Branch den Paul-Scope-Gate selbst auf: bei `start` mit Startprüfung, bei `verify` erneut mit Frischeprüfung und bei `complete` zwingend vor jeder Zustandsfortschreibung mit `verify`.
WARUM:
Die vorherige Lösung war logisch verpflichtend, hing aber noch daran, dass der Worker die zweite Paul-Anweisung aus `AGENTS.md` tatsächlich ausführte. Für „Paul muss zwingend automatisch sein“ war das eine vermeidbare Erinnerungsstelle.
KISS:
Kein neuer Runner und keine zweite Eingangstür. Nur die bestehende `cloud_entry.py` ruft die vorhandene Paul-Sicherung automatisch auf.
LOKAL:
Frischematrix 10/10 PASS; Auto-Bridge 6/6 PASS.
GITHUB:
Security-Head `d9bb690f677a34d09540338ca2a4c32494b42079`; `Paul automatic cloud-entry bridge CI` SUCCESS; `Paul current-Campus positive-negative CI` SUCCESS; gesamter `hardlock` SUCCESS.
GRENZE:
Auf `main` weiterhin nicht produktiv aktiv, bis Security-PR #137 kontrolliert aktiviert ist.


## ARCH-064 – Eigenes Büro PRODUKTVERGLEICH
WAS:
Das Pferde-Atelier erhält ein siebtes Fachbüro `PRODUKTVERGLEICH/` mit `START_HERE.md`, `CURRENT_STATE.md` und genau einem `HOBBYRAUM.md`.
WARUM:
Produktvergleichs-Konzept, konkrete Vergleichsdefinition, Vergleichseigenschaften, harte Faktengrundlagen und Quellenbindung sind ein eigener wiederkehrender Fachbereich. Diese Arbeit soll auffindbar bleiben, ohne den aktuellen TEXT-/STARTMASTER-Produktionsstand oder andere Büros zu vermischen.
FACHGRENZE:
PRODUKTVERGLEICH = Vergleichsdefinition/Faktendossier/Quellenbindung/Übergabe.
TEXT = eigentliche Textproduktion und technische Textmaschine.
EINE WAHRHEIT:
Das neue Büro führt keine zweite Textmaschine, Fehlerliste oder Zielwahrheit.
STARTSTATUS:
HOBBYRAUM FREI; frühere Produktvergleichsarbeit wird nicht aus Erinnerung als CURRENT übernommen.

## ARCH-065 – Fehlerliste ist technische Vorsperre an jeder Bürotür
WAS:
Projektbüro-Eingänge müssen vor jeder technischen Aktion zwingend zuerst über das zentrale Fehlerregister zur relevanten autoritativen Fehlerquelle führen und die geplante Aktion gegen bekannte Fehler, Wiederholungsfehler und Test-/Umgebungsgrenzen abgleichen.

WARUM:
Im TEXT-Hobbyraum wurde ein bereits als B06 dokumentierter Sachverhalt erneut praktisch ausprobiert: ein Live-/7/7-Start aus einem PR-/Hobbyraum-Head, obwohl der Production Preflight current `main` verlangt. Die Information war vorhanden; sie wurde nur nicht vor der Aktion verpflichtend gelesen.

REGEL:
Treffer in der autoritativen Fehlerquelle = Aktion nicht wiederholen. Bestehende Lösung/Arbeitsgrenze übernehmen. Erst bei belegtem KEIN-TREFFER weiterarbeiten.

GRENZE:
Diese Architekturregel betrifft Bürotüren und neue Projektbüros. Der Campus-Eingang selbst wird dadurch nicht verändert.

UMSETZUNG:
- TEXT-`START_HERE.md`;
- `BAUCONTAINER/EINGANGSSTANDARD.md`;
- `BAUCONTAINER/NEUES_PROJEKT_VORLAGE.md`.



## PV-PLAN-001 – Eigenes Produktvergleichs-Fachmodul, aber keine zweite Textmaschine

STAND:
2026-09-06 / reversible Planungsentscheidung.

WAS:
Produktvergleiche werden als eigener fachlicher Workflow entwickelt:
Vergleichsauswahl → Vergleichsebene → Merkmale → Recherche → Herstellerfakten → Quellen → Lücken/Konflikte → fachliches neutrales Vergleichsergebnis → strukturiertes Dossier.

Danach übernimmt die bestehende TEXT-/SEO-Maschine die eigentliche Artikelproduktion.

WARUM:
Die bereitgestellten Produktvergleichs-Arbeitsstände besitzen bereits eine saubere Daten-/Recherchetrennung und einen expliziten Übergabevertrag zur Textproduktion. Ein zweites vollständiges TEXT-/SEO-System würde Recherche-, SEO-, Qualitäts-, WordPress- und Produktionslogik doppeln und damit zusätzliche Fehler- und Synchronisationsquellen erzeugen.

WICHTIGER ZUSATZ:
Dass die Produktvergleichskategorien noch neu entstehen, ändert diese Entscheidung nicht. Kategorien und Vergleichslogik dürfen im Produktvergleichsmodul frisch und eigenständig entwickelt werden; nur die bereits vorhandene allgemeine Text-/SEO-Produktionsfunktion wird nicht dupliziert.

ALLGEMEINGÜLTIGKEIT:
Der geplante Kern muss projektunabhängig sein. Pferde-Atelier wird erste Konfiguration/Profil, nicht Bestandteil des Kerncodes.
Technische Allgemeingültigkeit ist noch nicht bewiesen und bleibt bis zum Prototyp UNGEKLÄRT.

VERWORFENE VARIANTE V0:
Zweites komplettes Produktvergleichs-Text-/SEO-System parallel zu STARTMASTER.
Nicht grundsätzlich unmöglich, aber aktuell schlechteres Verhältnis von zusätzlicher Komplexität zu Nutzen.

REVISIONSREGEL:
Wenn die spätere Schnittstellenanalyse zeigt, dass TEXT wesentliche Produktvergleichsanforderungen nicht ohne invasive Sonderlogik aufnehmen kann, darf diese Entscheidung neu geprüft werden.


## PV-PLAN-002 – Kaufquellen gehören zur Affiliate-Zentrale, nicht zur Produktfakten-Engine

STAND:
2026-09-06 / reversible Planungsentscheidung.

WAS:
Das Produktvergleichsmodul übergibt für jedes verglichene Produkt eine möglichst eindeutige Produktidentität.
Die bestehende Affiliate-Zentrale bleibt zuständig für aktuelle Kaufangebote, Provider, Preise, Verfügbarkeit, Tracking, Disclosure und Rendering.

WARUM:
Preise und Verfügbarkeit sind dynamisch und dürfen nicht mit langlebigen Herstellerfakten vermischt werden. Außerdem besitzt die Affiliate-Zentrale bereits Artikel-Produktkarten, Qualitätsprüfung, Deduplizierung, Tracking und Multi-Provider-Ausgabe. Eine zweite Kaufquellen-/Produktkartenlogik wäre unnötige Doppelarchitektur.

KISS-SCHNITTSTELLE:
Produktvergleich → Produktidentität A/B.
TEXT → fertiger Artikel + unveränderte strukturierte Produktidentitäten.
AFFILIATE → exakte Kaufquellenauflösung und Rendering.

HARD RULE:
Für einen Produktvergleich darf die Affiliate-Zentrale nicht automatisch ein nur ähnliches Produkt als Ersatz für Produkt A oder B ausgeben.
Exact Match zuerst; kein belastbarer Exact Match = keine Karte für dieses Produkt.

FAIL-SOFT:
Fehlende Kaufquelle blockiert den fachlich korrekten Artikel nicht.
Sie darf nur die kommerzielle Ausgabe reduzieren, niemals Fakten oder Fazit verändern.


## PV-PLAN-003 – STARTMASTER nicht anbinden; eigenständige vertikale Produktvergleichsstraße

STAND:
2026-09-06 / revidierte bevorzugte Architektur nach erneuter Prüfung des realen Text-/SEO-Gesamtworkflows.

ERSETZT ALS BEVORZUGTE V1-RICHTUNG:
PV-PLAN-001, soweit dort eine Laufzeitübergabe des Produktvergleichsdossiers an die bestehende TEXT-/SEO-Produktion vorgesehen war.
PV-PLAN-001 bleibt als dokumentierte frühere Planungsvariante erhalten.

BEFUND:
Der heutige Textproduktionsweg ist stark gebunden und fehlerempfindlich. Die nominelle Textmaschine ist nur ein Teil einer Kette aus SEO-Metadaten, Plan-Slot-Bindung, Fachworkflow, Research/Fact-Pack, PPM 6.7.9, PSERC, PSTE, Duplicate-/Cannibalization-, SEO-, Design-, Signer-/Release- und Publish-Safety-Schritten.
Die aktuelle offizielle SEO→Text-Schnittstelle ist bewusst exakt fünf Felder breit. Produktvergleichsdossiers dort einzuschleusen würde die bestehende Architekturgrenze erneut verletzen oder eine neue Artikeltyp-/Plan-Slot-Erweiterung erzwingen.

KISS-ENTSCHEIDUNG:
Produktvergleich als eigenständige vertikale Straße entwickeln:
Discovery → Pair Validation → Research → Dossier → Product-Compare-Writer → Qualitätsprüfung → WordPress-DRAFT.

STARTMASTER/TEXT:
keine Laufzeit-Abhängigkeit in V1.

WIEDERVERWENDUNG:
Nur bewährte Schreib-/Struktur-/Formatregeln bzw. technisch wirklich isolierbare kleine Writer-Bestandteile übernehmen.
Kein Klon des kompletten STARTMASTER-/PSERC-/PPM-/PSTE-Stacks.

WARUM:
- isoliert reparierbar;
- keine Synchronisationspflicht mit einem noch instabilen System;
- keine Plan-Slot-/Signer-/Gate-Kette als Voraussetzung;
- Produktvergleich kann unabhängig getestet und versioniert werden;
- spätere Integration bleibt möglich, wenn beide Systeme stabil sind.

EINZIGE ZWINGENDE EXTERNE V1-SCHNITTSTELLE:
AFFILIATE Exact-Product-Auflösung über stabile Produktidentitäten in WordPress-Post-Metadaten.

KATEGORIEN:
Kein allgemeines Kategoriemodul. Produktvergleich verwaltet nur seine eigene minimale, projektkonfigurierbare Kategoriezuordnung.

SEO:
optional zur Priorisierung/Keyword-/Dublettenprüfung; keine Pflichtabhängigkeit für Recherche oder Produktion.


## PV-PLAN-004 – Journal/Wissen-Beleg öffnet die Extension-Option erneut

STAND:
2026-09-06 / Architekturentscheidung erneut geöffnet.

ERSETZT ALS AKTUELL BEVORZUGTE ENTSCHEIDUNGSLOGIK:
PV-PLAN-003 ist nicht verworfen, aber nicht mehr automatisch bevorzugt.

NEUER BEFUND:
Nach den damaligen Problemen mit Wissen/Journal wurde eine allgemeine additive Beitragsart-Erweiterung gebaut.
PSERC 0.28.2 trennt Core-Release und Extension-Release allgemein.
Journal wird signiert/versioniert als Erweiterung angebunden; die Textmaschine selbst bleibt unverändert.
Ein zusätzlicher SyntheticProbe-Extension-Test wurde positiv dokumentiert.
Aktuelle Snapshots belegen, dass Extension-Registry und signierte Extension-Manifeste weiterhin Teil von PPM 6.7.9 sind.

KISS-FOLGERUNG:
Nicht theoretisch zwischen Vollintegration und Vollkopie entscheiden.
Zuerst ein winziger isolierter Machbarkeitstest:
`Produktvergleich_TEST` ausschließlich über die vorhandene Extension-Tür.

PASS-BEDINGUNGEN:
- Core-Textmaschine unverändert;
- 5-Felder-Handoff unverändert;
- keine neue Workflow-/Runner-/Gate-/Signer-Architektur;
- keine Änderung bestehender Beitragsarten;
- bestehende Regressionen unverändert PASS;
- Produktvergleich kann eigenen Titel-/Strukturvertrag besitzen;
- keine externe Artikeltext-/HTML-/Fact-Pack-Einspeisung.

ENTSCHEIDUNGSREGEL:
Kleiner isolierter PASS → gemeinsame bestehende Textproduktion wird bevorzugte KISS-Variante.
Core-Umbau / sechstes Feld / breite Kopplung nötig → Extension verwerfen und eigenständige Produktvergleichsstraße nach PV-PLAN-003 verwenden.

OFFEN:
Wie exakte Produktidentitäten A/B und belastbare Herstellerfakten die bestehende Research-Stufe erreichen, ohne die alte externe Fact-Pack-/Content-Grenze zu verletzen.


## PV-PLAN-005 – Fachkonzept im PRODUKTVERGLEICH, technische Integration im betroffenen Fachbüro

STAND:
2026-09-06.

WAS:
Das vollständige fachliche Produktvergleichskonzept wird ausschließlich im Büro PRODUKTVERGLEICH entwickelt.
Dazu gehören Beitragsart, eigene Textregeln, Kategorieanforderungen, Produktfindung/Pairing, Recherche, Fakten-/Quellenregeln und Abnahmekriterien.

Wenn das Konzept eine Änderung des bestehenden TEXT-/SEO-Systems benötigt, wird daraus ein begrenzter technischer Integrationsauftrag.
Die Umsetzung dieser Änderung findet ausschließlich im TEXT/SEO-Büro und nach dessen eigener Arbeitsfreigabe statt.
Affiliate-Änderungen entsprechend ausschließlich im AFFILIATE-Büro.

WARUM:
Fachliche Verantwortung und technische Besitzgrenzen bleiben eindeutig. So entsteht kein paralleles Schreiben am selben System und kein Zuständigkeitsstreit.

KISS:
PRODUKTVERGLEICH definiert **WAS** benötigt wird.
TEXT/SEO entscheidet und implementiert **WIE** es innerhalb seines Systems sicher angebunden wird.
AFFILIATE implementiert nur seine Kaufquellen-Schnittstelle.

AKTUELL:
Keine TEXT/SEO-Änderung aus diesem Planungschat. Der aktuelle TEXT-Hobbyraum ist anderweitig gebunden und sperrt Fach-/Textmaschinenregeländerungen.


## ARCH-066 – Externe Prüfer bekommen eine allgemeingültige READ-ONLY-Außentür
WAS:
`PAUL/READ_ONLY_REVIEW.md` stellt externen Prüfern ohne Git-Werkzeuge einen einzigen öffentlichen Einstieg für **alle Projekte/Büros/Fachthemen** bereit.
WARUM:
Ein eigener Claude-Bereich würde Pauls vollständige Lesesicht duplizieren und neue Zuständigkeits-/Synchronisationsprobleme schaffen. Externe Prüfer brauchen nur eine sichere Lesetür und einen klar begrenzten Prüfgegenstand.
KISS:
Keine Claude-Etage, kein eigener Status, keine Fachkopien. Prüfgegenstand = exakt Nutzerauftrag. Standard = FACH-/INHALTSPRÜFUNG. System-/Architekturprüfung nur bei ausdrücklichem Auftrag.
ZUSAMMENSPIEL:
Claude = READ-ONLY-Zweitprüfer; Paul kann Befunde verwenden, bleibt aber alleiniger Paul-Worker.
FALLBACK:
Wenn auch HTTPS/Webzugriff fehlt, genau eine automatisch erzeugte READ-ONLY-Prüfkapsel für den genannten Prüfgegenstand.


## PV-PLAN-006 – Campus-Queraudit vor Architekturfestlegung

STAND:
2026-09-06.

BEFUND:
Historische Campus-Quellen wurden gezielt auf Integrationsmuster geprüft.

- stabile Organisationsmuster: allgemeiner Kern + Projektkonfiguration + klare Fachgrenzen;
- problematisch: Cross-Core-Hartverdrahtung neuer Fachlogik;
- Journal/Wissen belegt diese Gefahr konkret;
- additive Extension ist der reparierte Weg, aber weiterhin an PSTE + PSERC + PPM + signed Kategorie-/Plan-Slot-Verträge gekoppelt;
- Extension erzeugt reale WordPress-Kategorien nicht selbst, sondern verlangt bereits vorhandene eindeutig auflösbare Terms;
- Kategoriemodell ist ein eigener umfangreicher Workflow und für eine einzelne Produktvergleichs-Kategorie nicht automatisch die KISS-Lösung;
- aktuelle TEXT-Fehlerhistorie zeigt Übergabe-/Kategorie-/Plan-Slot-/Context-Kopplungen als wiederkehrende Risikozone.

FOLGE:
Noch keine Endarchitektur einfrieren.
Eigenständige Universal-Engine und additive TEXT-Extension werden anhand derselben festen KISS-/Fehlerrisiko-/Wartungs-/Allgemeingültigkeitskriterien verglichen.

KORREKTUR:
Ein stiller Bridge-Shortcut `Produktvergleich -> bestehender Vergleich` wird nicht bevorzugt. Produktvergleich benötigt eigene Text-/Fakten-/Quellenregeln.

## TECH-TEXT-ALT-001 – Rückbau nur mit Mikro-, Abhängigkeits-, Historien- und Makrobeweis
BEREICH: TEXT / STARTMASTER0107
STATUS: VERBINDLICH / 2026-09-06
WAS:
Altlasten werden nicht aufgrund von Alter, Größe oder Ähnlichkeit zum letzten funktionierenden Stand entfernt. Jeder einzelne Rückbaukandidat muss vor Änderung positiv/negativ, auf direkte/indirekte Abhängigkeiten und gegen die vollständige autoritative Fehlerhistorie geprüft werden. Danach ist der bestehende Gesamtregressionslauf Pflicht.
WARUM:
Lokale KISS-Fixes können indirekt alte Fehler wieder öffnen oder nachträglich ergänzte, notwendige Funktionen beschädigen. Das bisherige Fehlerprotokoll enthält genau diese historischen Gründe und muss deshalb als Gegenprüfung Teil jeder Rückbauentscheidung sein.
SCHUTZLISTE:
Textmaschine/Fachregeln, externe-Link-Regel, Tabellenstufe, LanguageTool, echter PPM 6.7.9, PSERC/PSTE, Dubletten/Kannibalisierung, SEO, Design, Publish-Sperre, Hash-/Herkunftsbindung sowie externe Signierung ab 107008 bleiben erhalten.
FAIL-CLOSED:
Ungeklärter Zweck, ungeklärte Abhängigkeit oder ungeklärter historischer Fehlerbezug = NICHT ENTFERNEN.
TESTGRENZE:
Regression-PASS ist kein Live-/7/7-PASS.



## PV-PLAN-007 – Produktvergleichs-Beitragsbilder werden neutral und deterministisch selbst erzeugt

STAND:
2026-09-06 / VERBINDLICHER KONZEPTSTAND.

WAS:
Produktvergleich verwendet für Beitrags-/Teaserbilder keine manuell kopierten echten Produktfotos. Stattdessen wird pro Vergleich eine eigene neutrale Vergleichsgrafik automatisch erzeugt und über eine stabile `comparison_id` eindeutig gebunden.

DESIGN-REFERENZ:
Aus dem bestehenden Designplugin wird ausschließlich das technische Produktionsprinzip übernommen: zentraler Katalog, eigener Asset-Ordner, deterministische Zuordnung und Fail-closed bei fehlender/ungültiger Bindung. Die geprüfte Designquelle besitzt dafür 329 strukturgebundene Icon-Zuordnungen.

NICHT ÜBERNEHMEN:
Keine bestehenden Pferde-Icons, SVG-Geometrien, Motive oder inhaltlichen Zuordnungen werden kopiert.

ECHTE PRODUKTBILDER:
Bleiben ausschließlich Teil der vorgesehenen AFFILIATE-Produktdarstellung, sofern die jeweilige Affiliate-/Produktquelle ihre Nutzung trägt. Produktvergleich baut keinen zweiten fremden Produktbildbestand.

FAIL-CLOSED:
Falsche oder nur ähnliche Vergleichsgrafik ist verboten. Fehlt die korrekte Grafik, lieber kein Beitragsbild als eine falsche Zuordnung.

ALLGEMEINGÜLTIGKEIT:
Der Grafikgenerator soll als kleiner wiederverwendbarer Baustein mit Projekt-/Stilkonfiguration entwickelt werden; Pferde-Atelier ist nur die erste Konfiguration.

WARUM:
Weniger Copyright-Risiko, reproduzierbare Optik, automatische Skalierung auf viele Vergleiche, keine Abhängigkeit vom Fortbestand fremder Produktbilder und geringere Fehleranfälligkeit durch eindeutige Schlüsselbindung.


## PV-PLAN-008 – Eine Vergleichskategorie pro Produktgruppe mit eigenem Vergleichs-Archiv

STAND:
2026-09-06 / VERBINDLICHER KONZEPTSTAND.

ENTSCHEIDUNG:
Konzept 1 wird eingefroren: Produktgruppenvergleich, Produktvergleich und Variantenvergleich werden nicht in getrennte WordPress-Kategorieäste aufgeteilt, sondern unter einer einzigen sichtbaren Kategorie `Vergleich` der jeweiligen Produktgruppe gebündelt.

DARSTELLUNG:
Eigenes Vergleichs-Archivtemplate statt normaler WordPress-Listenansicht. Oben prominente Filter `Alle | Produktgruppenvergleiche | Produktvergleiche`; Variantenvergleiche werden innerhalb der konkreten Produktvergleichswelt klar gekennzeichnet bzw. über `Produkte | Varianten` unterfilterbar.

PRODUKTNAVIGATION:
Desktop shopartig seitlich; nur Produkte mit vorhandenen Vergleichsinhalten. Bei größerem Bestand `Weitere anzeigen` und/oder AJAX-Produktsuche. Mobil kompakt über Suchfeld plus aufklappbare Produktliste/Drawer statt langer Sidebar.

SUCHE:
Produktsuche liefert alle passenden eigenen Beiträge aus Produktvergleich und Variantenvergleich und kennzeichnet deren Typ sichtbar.

HARD RULE VERLINKUNG:
Vorhandener Variantenvergleich muss aus dem passenden Produktvergleich ausdrücklich im Text genannt und intern verlinkt werden. Variantenvergleich verlinkt zurück zum passenden Produktvergleich, sofern vorhanden.

TECHNISCHE GRENZE:
Eine Kategorie bedeutet keine fachliche Vermischung. Produktgruppenvergleich, Produktvergleich und Variantenvergleich bleiben intern eindeutige Vergleichstypen mit getrennten Regeln.

WARUM:
Ein zentraler Ort für die Nutzerfrage „vergleichen“, bessere Auffindbarkeit und interne Navigation, weniger künstliche Kategorieebenen und geringere Gefahr dünner Parallelkategorien. Die zusätzliche Komplexität wird einmalig kontrolliert im Vergleichs-Archivtemplate gebündelt.


## PV-PLAN-009 – Produktrecherche wird gemeinsame Faktenbasis; Affiliate bleibt Commerce-Schicht

STAND:
2026-09-06 / VERBINDLICHER KONZEPTSTAND.

WAS:
Die Produktrecherche des Produktvergleichssystems wird nicht ausschließlich für Produktvergleichsartikel gedacht. Ihre quellengebundenen Produktfakten dürfen auch Beratungsbeiträge und Variantenvergleiche versorgen.

BERATUNG:
Bedarfsorientiert, z. B. `Reitstiefel für breite Waden`. Sie kann anhand verifizierter Produktmerkmale passende konkrete Modelle nennen oder auswählen.

AFFILIATE:
Bleibt zuständig für aktuelle Kaufangebote, Verfügbarkeit, Tracking und Produktkarten. Affiliate darf fachliche Eignung nicht aus Händler-/Commerce-Daten selbst ableiten, sondern erhält nur bereits fachlich begründete Produktidentitäten bzw. Bedarfszuordnungen.

KISS-GRUNDSATZ:
Einmal recherchieren, mehrfach verwenden. Keine zweite parallele Produktrecherche in Beratung oder Affiliate.

WARUM:
Vermeidet doppelte Herstellerrecherche, widersprüchliche Produktfakten und die Vermischung von fachlicher Eignung mit kommerzieller Verfügbarkeit.


## PV-PLAN-010 – Produktregal ist fachliche Hauptquelle; Affiliate entdeckt und monetarisiert

STAND:
2026-09-06 / VERBINDLICHER KONZEPTSTAND.

ENTSCHEIDUNG:
Die fachliche Produktauswahl beginnt nicht im Affiliate-Pool. Zentrale Quelle ist ein Produktregal mit eindeutig identifizierten und quellengebunden recherchierten Produkten/Varianten.

HAUPTRICHTUNG:
`Produktregal/Faktenbasis -> Beratung/Produktvergleich/Variantenvergleich -> Affiliate-Exact-Match -> Kaufangebot`.

AFFILIATE-ROLLE:
Affiliate prüft nachgelagert, ob die fachlich ausgewählten Produkte exakt bei Amazon, eBay, idealo, Awin oder anderen angebundenen Quellen verfügbar sind. Kein Exact Match = kein Ersatzprodukt und keine Veränderung des fachlichen Artikels.

ENTDECKUNG:
Affiliate darf neue Commerce-Produkte als Kandidaten an die Produktrecherche melden. Diese Kandidaten werden erst nach Identitäts- und Quellenprüfung in das fachliche Produktregal aufgenommen und dürfen erst danach für Inhalte genutzt werden.

HARD RULE:
Provision, Angebotsdichte oder kurzfristige Händlerverfügbarkeit dürfen niemals die fachliche Eignung, Vergleichspaarung oder Herstellerfakten bestimmen.

LEITSATZ:
**Affiliate darf entdecken. Produktrecherche entscheidet. Affiliate monetarisiert.**


## ARCH-067 – PB ONE ist das zentrale nicht-technische Agenturgebäude
WAS:
`protocol/PROJECT_MEMORY/PB_ONE/` wird als zentraler Agenturknoten des Campus eingerichtet.
WARUM:
Die Agentur PB ONE ist der organisatorische Mittelpunkt hinter mehreren Projekten. Ideen, Angebote und Unterlagen sollen projektübergreifend auffindbar sein, ohne Pferde-Atelier zum Mittelpunkt des gesamten Campus zu machen.
GRENZE:
Keine Programmierung in PB ONE. Operative Fach-/Technikarbeit wird an Projekt-/Fachbüros übergeben.
START:
Zwei Bereiche: `ANGEBOTE_FLYER` und `IDEENWERKSTATT`.

## ARCH-068 – PB ONE ist gemeinsamer gleichberechtigter Agenturraum von Nutzer und Paul
WAS:
Innerhalb `PB_ONE/**` haben Nutzer und Paul dieselben redaktionellen Rechte: lesen, schreiben, Ideen/Konzepte verändern, Register pflegen, Unterlagen erstellen und Entscheidungen dokumentieren.
WARUM:
PB ONE ist die gemeinsame Agentur, nicht Pauls technischer Spezialworkerraum.
AUSNAHME:
Die sonstige Paul-Regel `protocol/PROJECT_MEMORY/** = READ ONLY` gilt für `PB_ONE/**` redaktionell nicht.
GRENZE:
Keine Programmierung in PB ONE; kein technischer `paul/*`-Branch und kein WRITE_SCOPE.
ÜBERGABE:
Technische/projektspezifische Umsetzung geht bewusst an ein Projekt-/Fachbüro; dort gelten wieder die normalen Paul-Regeln.


## ARCH-069 – PB ONE erhält Zentralregister und Entwicklungsraum
WAS:
PB ONE bekommt `ZENTRALREGISTER.md` sowie `ENTWICKLUNGSRAUM/` mit CURRENT_STATE, HOBBYRAUM und KONZEPTREGISTER.
WARUM:
Rohideen, weiterentwickelte Konzepte und fertige Unterlagen brauchen unterschiedliche Reifegrade, aber einen gemeinsamen Agenturknoten.
KISS:
Idee → Entwicklung → Angebot/Flyer oder Projektübergabe.
Keine zusätzliche technische Schicht.


## ARCH-070 – PB ONE Arbeitsdokumente als eigene Akten
WAS:
`PB_ONE/ARBEITSDOKUMENTE/` wird als gemeinsamer Ablage- und Entwicklungsort für laufende Präsentationen, Flyer, Konzeptpapiere und andere Unterlagen eingerichtet.
WARUM:
Punkte, Entscheidungen und Entwurfsstände sollen nicht in Chats verschwinden und nicht in Zentral-/Unterlagenregister hineinkopiert werden.
KISS:
Eine laufende Unterlage = eine eigene Akte. `REGISTER.md` verweist nur auf die Akte; `VORLAGE.md` gibt ein minimales Schema vor.
RECHTE:
Nutzer und Paul gleichberechtigt redaktionell.
GRENZE:
Keine Programmierung in PB ONE.


## ARCH-071 – PB ONE erhält einen Aktenschrank für dauerhafte Referenzakten
WAS:
`PB_ONE/AKTENSCHRANK/` wird als dauerhafter Ablageort für belastbare PB-ONE-Referenzunterlagen eingerichtet.
WARUM:
Quellen wie die eigene Website sollen chatübergreifend verfügbar sein, ohne Rohdaten oder Inhalte in Arbeitsregister zu duplizieren.
KISS:
START_HERE + REGISTER + konkrete Akten.
ERSTE AKTE:
`WEBSITE_PB_ONE_20260907.md` – strukturierte Inhaltszusammenfassung aus dem WordPress-Export vom 07.09.2026.
GRENZE:
Die Akte dokumentiert Website-Aussagen; sie ist keine externe Tatsachenprüfung und kein vollständiges WordPress-Backup.


## ARCH-072 – Sicherungsarchitektur: Baucontainer definiert, Tresor führt aus
WAS:
Die Zuständigkeit für Sicherung wird getrennt:
Baucontainer definiert Sicherungsregeln und Architektur; der Tresorraum erzeugt und prüft die tatsächlichen Backup-/Download-/Restorestände.
WARUM:
Sicherungsarchitektur ist Campus-Regel, die konkrete Sicherung ist operative Tresorarbeit. Vermischung würde Baucontainer zur Backup-Werkbank machen.
KISS:
Regeln im Baucontainer; Ausführung ausschließlich im Tresor.
HAUPTQUELLE AUSFÜHRUNG:
`TRESOR/LOKALES_BACKUP_KONZEPT.md`.

## ARCH-073 – PB ONE Aktenschrank erhält Plugin-Fach für Eigenentwicklungen
WAS:
`PB_ONE/AKTENSCHRANK/PLUGINS/` wird als Agentur-/IP-Katalog für bestätigte selbstentwickelte Plugins und digitale Eigenentwicklungen eingerichtet.
WARUM:
PB ONE benötigt einen geschäftlichen Überblick über eigene Produkte/Bausteine, ohne technische Wahrheiten zu duplizieren.
REGEL:
Pluginfach speichert Beschreibung, Zweck, Eigentums-/Agenturstatus und Verweis auf technische Hauptquelle.
Version, Release, LIVE, Code und Modulklasse bleiben ausschließlich in den bestehenden autoritativen technischen Quellen.

## ARCH-074 – PB ONE Aktenschrank erhält TODO-Fach
WAS:
`PB_ONE/AKTENSCHRANK/TODO/` wird als zentrale Ablage für offene operative PB-ONE-Aufgaben eingerichtet.
WARUM:
Offene Entscheidungen und fehlende Vertriebs-/Betriebsgrundlagen sollen chatübergreifend auffindbar bleiben, ohne Fachwahrheiten in Arbeitslisten zu duplizieren.
KISS:
Ein Fach, ein START_HERE, konkrete TODO-Akten.
REGEL:
Das TODO-Fach hält nur offene Punkte und Verweise. Sobald Preise, Verträge, Prozesse oder technische Stände entschieden sind, liegt die autoritative Wahrheit an der jeweils zuständigen Hauptquelle.
ERSTE AKTE:
`TODO/VERTRIEB_STARTKLAR_20260907.md`.

## ARCH-075 – PB ONE erhält Preis-Fach
WAS:
`PB_ONE/AKTENSCHRANK/PREISE/` wird als dauerhafter Ort für Preis-, Paket- und Baukastenkonzepte eingerichtet.
WARUM:
Preise sind ein wiederkehrender geschäftlicher Kernbereich und dürfen nicht dauerhaft nur in einer TODO-Liste liegen.
REGEL:
Entwurf und verbindlicher Preis müssen klar getrennt sein.

## ARCH-076 – Präsentation & Werbung nutzt bestehenden Angebote/Flyer-Raum
WAS:
Der bestehende Bereich `PB_ONE/ANGEBOTE_FLYER/` wird funktional und an der Tür zu „Präsentation & Werbung / Angebote & Flyer“ erweitert.
WARUM:
Präsentationen, Pitch, Musterseiten, Werbung, Flyer und Angebotsunterlagen gehören fachlich zusammen. Ein zweiter paralleler Raum würde dieselben Unterlagen doppelt verwalten.
KISS:
Pfad bleibt stabil; Funktion und Beschilderung werden erweitert.

## ARCH-077 – Vertriebs-Fach bündelt Abläufe und Lead-Management
WAS:
`PB_ONE/AKTENSCHRANK/VERTRIEB/` wird als dauerhafter Ort für Vertriebsprozesse, Kundendaten-Schnittstellen, Angebotsablauf, Sonderfälle, Onboarding und Lead-Management eingerichtet.
WARUM:
Diese Themen greifen operativ ineinander. Eigene Fächer nur für „Lead Management“ oder „Onboarding“ wären zu kleinteilig und würden Zusammenhänge zerreißen.
GRENZE:
LeadScout selbst bleibt im Plugin-Fach; Preise bleiben im Preis-Fach; Verkaufsunterlagen bleiben im Bereich Präsentation & Werbung.

## ARCH-078 – OTTO wird nach Programmzusage vor Digistore24 priorisiert
WAS:
Der Nutzer meldet am 07.09.2026 die Zusage für das OTTO-Partnerprogramm. OTTO wird damit zum aktuellen gebundenen Affiliate-Auftrag; Digistore24 wird vorerst zurückgestellt.
WARUM:
Das bestehende Konzept priorisiert Awin als Kernnetzwerk und möglichst wenige stabile Datenquellen. Die Affiliate-Source führt OTTO bereits als vorbereitete Produktquelle mit dem Weg `Awin → fachlich OTTO`.
KISS:
Kein eigener OTTO-Gesamtworkflow und kein neuer Paralleladapter. OTTO wird in den bestehenden Awin-/Produktquellenweg integriert.
SICHERHEIT:
Die Nutzerzusage priorisiert die Arbeit, ersetzt aber nicht den technischen Nachweis von Produktfeed, Tracking-/Deeplinkdaten und Pflichtfeldern. Öffentliche Aktivierung erst nach realer Positiv-/Negativprüfung; bis dahin `prepared / integration pending`.
GRENZE:
Der dokumentierte Digistore24-Fehlerstand bleibt erhalten, wird während des OTTO-Auftrags aber nicht weiterbearbeitet.

## AFFILIATE-OTTO-001 – OTTO als Awin-Breitenquelle mit Productwissen-Exact-Match

STAND: 2026-09-07.

WAS:
OTTO wird im AFFILIATE-System über den bestehenden Awin-Transport automatisiert für reale Produktkarten und reale Bannerwerbemittel genutzt.
Kanonische OTTO-Identität ist Awin Advertiser-ID `14336`.

EBENEN:
- Startseite: reales passendes Banner;
- Hub Ebene 1/2: Banner + bis zu drei Produkte;
- Kategorie/Leaf: Banner + bis zu drei Produkte;
- normale Beiträge: Banner + bis zu drei Produkte;
- Produktvergleich/Variantenvergleich/fachlich gebundene Beratung: Exact Product Match.

PRODUCTWISSEN:
Die parallel entwickelte Produktwissen-Datenbank ist die fachliche Produkt-/Variantenwahrheit.
Affiliate liest sie nur über eine stabile Consumer-Schnittstelle und schreibt keine Produktfakten.
`ppar_affiliate_exact_product_requirements`
liefert exakte Kennungen.
Kein identisches Affiliate-Angebot = keine Karte; kein Ersatzmodell.

AFFILIATE:
Bleibt zuständig für aktuelles Angebot, Preis, Bestand, Verkäufer, Tracking und reale Werbemittel.

BANNER:
Automatische Zuordnung/Activation realer importierter Awin-Banner ist Teil der bestehenden Affiliate-Zentrale.
Die automatische Beschaffung eines OTTO/Awin-Creative-Katalogs wird nicht erfunden und bleibt bis zu einem real belegten Publisher-Zugang/Export/API offen.
Produktbilder werden niemals als Ersatzbanner verwendet.

WARUM:
OTTO besitzt eine hohe Sortimentsbreite und kann viele Portalbereiche versorgen. Die Trennung verhindert zugleich, dass Handelsverfügbarkeit oder Provision fachliche Produktentscheidungen übernimmt.

KISS:
Kein eigenes OTTO-Plugin, kein zweiter Feedmotor, keine direkte Productwissen-Tabellenkopplung, keine neue Bannerarchitektur.

BELEG:
`protocol/AFFILIATE_RELEASE_OTTO_AUTOMATION_CONCEPT_20260907.md`
`release/affiliate-zentrale/evidence/otto_awin_productwissen_banner_contract_20260907.txt`



## PV-PLAN-011 – Produktwissen und Vergleichskern werden über reales Dossier gehärtet

STAND: 2026-09-07.

WAS:
Der V1-Kern wird nicht nur mit synthetischen Daten, sondern vor dem Writer mit einem realen freigegebenen Forschungsdossier geprüft. `PV-REG-001` besteht den WordPress+MySQL-Lauf mit 14 Pflichtmerkmalen, SOURCE_CONFLICT und NOT_IN_SOURCE.

KISS-FOLGE:
Vergleiche speichern keine Produktfaktenkopie. Zusätzlich zu den Produkt-/Varianten-IDs wird nur die geordnete Liste der verbindlichen Vergleichsmerkmale gespeichert. Daraus wird ein deterministisches Writer-Dossier gebaut.

FAIL-CLOSED:
Fehlt ein erforderlicher Fakt vollständig, entsteht kein Writer-Dossier. NOT_IN_SOURCE und SOURCE_CONFLICT sind dagegen explizite belegte Zustände und bleiben als Warnungen sichtbar.

ALTSTAND:
Ältere `TIER_SAME_BRAND`-Dossiers aus dem Forschungsbestand werden wegen der späteren Zwei-Hersteller-Regel nicht automatisch importiert.
## AFFILIATE-OTTO-002 – Bannerautomatik arbeitet relevance-first mit Zielanteilen und manueller Reparaturinstanz

STAND: 2026-09-07.

WAS:
Alle realen Affiliate-Bannerplätze werden nach erfolgreicher Sicherheits-, Format- und Relevanzprüfung automatisch zwischen den aktuell gleich relevanten Bannerquellen verteilt.

STARTANTEILE:
- OTTO 40
- andere Awin-Programme 25
- ADCELL 20
- Direktpartner 15
- Digistore24 0
- Sonstige 0

REGEL:
Die Quote darf niemals Relevanz schlagen.
Nur Quellen der besten aktuell vorhandenen Relevanzstufe nehmen an der Anteilsauswahl teil.

FEHLENDE QUELLEN:
Nicht vorhandene/ungeeignete Quellen erzeugen keine künstlichen Leerplätze.
Die verbleibenden Anteile werden unter den verfügbaren gleich relevanten Quellen automatisch normalisiert.

STABILITÄT:
V1 verteilt Bannerplätze deterministisch nach Kalenderwoche + Seite/Kontext + Slot.
Keine request-zufällige Rotation und keine neue Realtime-Impression-Counter-Architektur.

REPARATUR:
Die vorhandene interne „Zuordnungen“-Instanz wird ausdrücklich als Reparaturschicht genutzt:
Automatik / fest auswählen / nicht anzeigen / Vererbung.
Zusätzlich bleiben Provider-, Partner-, Creative-, Target-, Slot-, Output-Veto und globale Notabschaltung erhalten.
Manuelle Reparatur gewinnt immer vor automatischer Anteilsauswahl.

WARUM:
Der Normalbetrieb soll ohne manuelle Einzelpflege skalieren. Gleichzeitig muss ein falscher oder geschäftlich unerwünschter Einzelfall sofort korrigierbar bleiben, ohne die Automatik insgesamt abzuschalten.

KISS:
Kein eigener Banner-Router, keine zweite Datenbank, kein Impression-Tracking-System und kein neuer OTTO-Sonderworkflow.
Bestehende Relevanz-, Slot-, Campaign- und Control-Logik wird nur um eine kleine Anteilsschicht ergänzt.

BELEG:
`protocol/AFFILIATE_RELEASE_OTTO_AUTOMATION_CONCEPT_20260907.md`
`release/affiliate-zentrale/evidence/otto_awin_banner_distribution_contract_20260907.txt`



## PV-PLAN-012 – Writer übernimmt Zwangsjacken-Grundidee ohne STARTMASTER-Komplexität

STAND: 2026-09-07.

WAS:
Das bestehende TEXT-/STARTMASTER-Konzept wurde gezielt auf seine Grundidee geprüft. Die starke Grundidee „keine freie Entscheidung ab Produktionsstart; Prompt allein reicht nicht“ wird verbindlich übernommen. Die komplexe technische Altarchitektur wird nicht kopiert.

OBERSTE REGEL:
Der Produktvergleichs-Writer hat **NULL Freiheit**. Gleiche gebundene Inputs bei gleicher Vertrags-/Renderer-Version müssen byte-identischen Output erzeugen.

ÜBERNOMMEN:
Single Door, gebundene Inputs, Hashes, Fail-closed, keine Fallbackroute, Output-Quarantäne, Validator vor Sichtbarkeit, Receipt, kein Auto-Publish, Regression aus realen Fehlern.

NICHT ÜBERNOMMEN:
STARTMASTER-Raumkette, PPM/PSERC/PSTE, Signer/Capsule, mehrere Gate-/Executor-Schichten und freie Worker.

V1-KETTE:
`BOUND_INPUT -> QUARANTINED_RENDERED -> VALIDATED -> DRAFT_READY_FOR_REVIEW`.

RULEBOOK:
Keine Callbacks/Promptregeln in Produktion. Ausschließlich manifest- und SHA-256-gebundene, versionierte Datenregeln. Regeln sind an exakte Fakten-Signaturen gebunden.

BELEG:
PR #142 / Run 34111825722 SUCCESS; Zero-Freedom Static Guard PASS; 100/100 byte-identisch; Golden Output PV-REG-001 `994d20136cebd169daa8a09f38248ee315552f8f63ea5f25c14995a01344828f`; manipuliertes Rulebook und geänderte Fakten korrekt BLOCKED.

LEITSATZ:
**Nicht der Writer schreibt den Artikel. Der Vertrag schreibt den Artikel.**


## PV-PLAN-013 – WordPress-Draft bleibt reine Materialisierung des gebundenen Outputs

STAND: 2026-09-07.

REGEL:
WordPress erhält keinen freien Titel, Body oder Kategorieparameter. Die Draft-Schicht akzeptiert nur Vergleichs-ID + gebundenes Projekt + gebundene Ruleset-ID und ruft intern den Zero-Freedom-Single-Door-Prozess auf.

PASS:
Run 34112287717 SUCCESS; Draft-Body byte-identisch zum validierten Renderer-HTML; Golden Output erhalten; kein Publish; keine Dublette bei Wiederholung; manipulierte Publishing-Konfiguration BLOCKED; Faktenänderung kann die Draft-Schicht nicht umgehen.

KISS:
Keine zweite Textlogik in WordPress. WordPress materialisiert nur bereits vollständig validierten Output.
## AFFILIATE-OTTO-003 – Bannerautomatik ist direkt prüfbar und besitzt realen Awin-Creative-Anschluss

STAND: 2026-09-07.

WAS:
Die OTTO/Awin-Bannerautomatik wurde bis zur konkreten technischen Anschluss- und Prüfschicht gehärtet.

REAL-SOURCE:
`ppar_affiliate_awin_static_creatives` nimmt nur reale Awin-Creative-Daten entgegen.
Keine Awin-API wird erfunden.
Fremde Advertiser-ID, fehlendes Bild oder fehlendes Tracking werden blockiert.
Eine real gebundene, aktuell leere Quelle wird mit `bound=true, rows=[]` von einer ungebundenen Quelle unterschieden.

ANTEILE:
`0` bedeutet automatische Sperre.
Mehrere Bannerplätze derselben Seite erhalten getrennte deterministische Entscheidungen; Creative-Dubletten zwischen Platz 1 und 2 werden verhindert.

REPARATUR:
Seitenreparaturen benötigen Begründung und speichern Benutzer/Zeitpunkt.
Kategorien und andere Portalziele werden über die bestehende feste Creative→Ziel/Slot-Entscheidung mit Begründung repariert.

PRÜFUNG:
Direkter read-only Test ohne Docker:
`bash AFFILIATE_HOBBYRAUM/run_otto_checks.sh`
Zusätzlich bleibt der isolierte Container-Hobbyraum bestehen.

WARUM:
Der Normalbetrieb soll vollautomatisch skalieren, aber reale Datenquellen, technische Fehler und einzelne Fehlzuordnungen müssen ohne Architekturumbau sicher prüf- und reparierbar bleiben.


## AFFILIATE-OTTO-004 – Awin-Kataloge aktualisieren sich selbst und freigegebene Programme starten ohne Snapshot-Voraussetzung

STAND: 2026-09-07.

WAS:
- Zu Beginn eines neuen Awin-Automationszyklus werden Joined-Programmliste und offizielle Produktfeedliste neu gelesen.
- Schlägt der Refresh fehl, bleibt Last-Known-Good erhalten; es wird nichts leer überschrieben.
- Scheduled Sources entstehen aus explizit `allow_local` + aktuell `joined` Programmen.
- Ein vorhandener Partner-Intake-Snapshot ist keine Startvoraussetzung mehr; der Job erzeugt ihn selbst.

WARUM:
Die gewünschte Vollautomatik darf weder von einem manuellen Verbindungstest noch von einem bereits vorhandenen Snapshot abhängen. Gleichzeitig dürfen Feed-/Programmdaten bei einem Refreshfehler nicht verschwinden.

KISS:
Kein zweiter Scheduler und kein OTTO-Sondermotor. Der bestehende Awin-Automationszyklus wurde nur an seiner realen Quelle gehärtet.

FEHLERBEZUG:
`AFFILIATE_HOBBYRAUM/FEHLERMATRIX.md` → AF-051 / AF-052.


## DESIGN-ORDER-001 – Kategorieebene: Orientierung vor Vertiefung

STAND:
2026-09-07 / V1.50.473 REJECTED NACH REALER NUTZERPRÜFUNG.

WAS:
Auf der zentral gesteuerten Pferde-Atelier-Kategorieebene wird die Ausgabereihenfolge geändert zu:
`Unterkategorie-/Beitragsart-Verweise -> Kategorienartikel -> Beitragsvorschau -> kommerzielle Blöcke`.
H1 bleibt am Seitenkopf.

WARUM:
Der Besucher soll zuerst die vorhandenen Wege im Thema erkennen, danach den redaktionellen Hauptinhalt lesen und erst anschließend weitere Beiträge entdecken. Banner und Produkte sollen diesen redaktionellen Weg nicht unterbrechen.

KISS:
Nur die zentrale Renderer-Reihenfolge wird verändert. Keine Einzelpflege pro Kategorie.

GRENZE:
V104, Kategorietexte, Karten-/Linklogik, Beitragsauswahl und Affiliate-Auswahl bleiben unverändert. `main` bleibt unverändert. LIVE-Stand bleibt bis zur Nutzerprüfung V1.50.472.

BELEG:
`fix/category-content-order-v150473-20260907`
`design-baseline/2026-09-07/v150473-category-content-order/`

## AFFILIATE-OTTO-005 – Productwissen→Affiliate Exact-Bridge wird isoliert gebaut, nicht in parallele Produktvergleich-Arbeit geschrieben

STAND: 2026-09-07.

WAS:
Affiliate besitzt den Exact-Consumer, der offizielle Produktwissen-Prototyp aber noch keinen Producer.
Ein isolierter Kandidat wurde deshalb auf Basis des aktuellen Produktwissen-Heads erstellt:
`hobbyroom/productwissen-affiliate-exact-bridge-20260907`.

Der Kandidat liefert Vergleichsprodukte read-only über `ppar_affiliate_exact_product_requirements`, bindet WordPress-Drafts an `_upc_comparison_id` und nutzt ausschließlich Productwissen-Identifier.

WARUM:
Produktwissen soll die fachliche Produktidentität bestimmen, Affiliate nur monetarisieren. Gleichzeitig darf der Affiliate-Arbeitsweg die parallel laufende Produktvergleich-Entwicklung nicht überschreiben.

REGEL:
Affiliate darf den Brückenkandidaten nicht selbst in den offiziellen Produktwissen-Branch mergen. Prüfung/Übernahme liegt beim Produktvergleich-Büro.

STATUS:
STATIC CONTRACT PASS / PRODUKTVERGLEICH-INTEGRATION + E2E OFFEN.


## DESIGN-ORDER-002 – Korrigierter Kandidat direkt aus V1.50.472

STAND:
2026-09-07 / **V1.50.474 REJECTED NACH REALER NUTZERPRÜFUNG**.

WAS:
Nach dem Fehlversuch V1.50.473 wurde nicht weitergepatcht. V1.50.474 wurde frisch aus dem exakten archivierten V1.50.472-Vorgänger gebaut.

REIHENFOLGE:
`H1 + kurzer Lead -> Unterkategorie-/Beitragsart-Verweise -> bestehende Artikel-Fortsetzung -> Beitragsvorschau -> Banner -> Produkte -> Direktwerbeplatz`.

KISS:
Nur `pferde-template-kit.php` ist verändert. Alle übrigen 497 Paketdateien bleiben byte-identisch.

HARD LOCAL:
Positiv-/Negativprüfung, PHP-Lint, V104-Parität, CSS-Parität und 498/498 ZIP-Readback PASS.

WARUM:
V1.50.473 hatte den bestehenden Introblock zu grob umgebaut. V1.50.474 trennt nur den bereits vorhandenen kurzen Lead von der vorhandenen Fortsetzung und sortiert ausschließlich die gewünschten Blöcke.

BELEG:
`fix/category-content-order-v150474-20260907`
`design-baseline/2026-09-07/v150474-category-content-order/`


## ARCH-079 – Masterdateien-Inventare dürfen keine zweite aktuelle Wahrheit führen

STAND: 2026-09-07.

WAS:
Masterdateien-Inventare werden campusweit auf ihre eigentliche Rolle begrenzt: Herkunft, Hash, Klassifizierung, historische/technische Belege und Referenzorte.

Sie dürfen keine eigenen dynamischen Aussagen über aktuellen Head, aktuelles Manifest, aktuellen Blocker, NEXT ACTION oder „aktuellen Statusbeleg“ führen.

WARUM:
Die Abschluss-/Nachholprüfung fand im Affiliate-Inventar einen alten Head/Manifest und eine 05.09.-Statusakte, die als aktuell bezeichnet war. Das erzeugte neben `CURRENT_STATE.md` und Release-Governance eine zweite Standwahrheit.

KISS:
Keine neue Datei und kein neues Register.
Nur:
- betroffenes Affiliate-Inventar bereinigt;
- `MASTERDATEIEN_REGEL.md` gehärtet;
- `NEUES_PROJEKT_VORLAGE.md` um dieselbe Negativprüfung ergänzt.

FEHLERBEZUG:
`BAUCONTAINER/ARCHITEKTUR_FEHLERKISTE.md` → BAU-035.

LEITSATZ:
**Inventar sagt, was vorhanden/belegt ist. CURRENT_STATE/Governance sagen, was jetzt gilt.**


## ARCH-080 – Tresor wird zur geschlossenen Ein-Datei-Disaster-Recovery
WAS:
Der Tresor-Zielzustand wird von mehreren Sicherungsbestandteilen auf **eine einzige verschlüsselte, geschlossene Recovery-Datei** verschärft.
WARUM:
Der Nutzer will nach theoretischem Totalverlust den kompletten GitHub-Campus einschließlich aller benötigten Informationen ohne zusätzliche Projektdateien wiederherstellen können.
KISS:
Eine Download-Einheit, ein Restore-Einstieg, ein Manifest, ein PASS/BLOCKED-Ergebnis.
SICHERHEIT:
Keine Klartext-Secrets im Repository. Recovery-Geheimnisse nur verschlüsselt innerhalb der Kapsel.
VOLLSTÄNDIGKEIT:
Git + Campus + recovery-relevante Roharchive + persistente GitHub-Projektdaten + WordPress-Vollstand + Recovery + Restore-Werkzeuge.
GRENZE:
Providerinterne GitHub-IDs können beim Neuaufbau neu vergeben werden; Original-IDs/Zeitstempel bleiben als archivierte Information erhalten.
PASS-REGEL:
`TRESOR_PASS` erst nach echtem isoliertem Wiederaufbau ausschließlich aus genau einer Recovery-Datei + Masterpasswort.


## PV-PLAN-014 – Affiliate liest Exact-IDs, SEO bleibt bis Vertragsprüfung upstream

STAND: 2026-09-07.

AFFILIATE:
Read-only Bridge ist real gegen WordPress/MySQL geprüft. Produktwissen liefert nur stabile Exact-Identifier; Affiliate darf keinen Ersatz erzeugen und schreibt keine Produktwahrheit zurück.

PASS:
Run 34131779064 SUCCESS; EAN/MPN PASS; fehlender Identifier erzeugt keine Anforderung; keine direkte Tabellenkopplung.

SEO:
Keine spekulative Integration. Der aktuelle SEO-Installerbestand ist dokumentiert, aber seine Fachregeln sind im Campus ausdrücklich noch nicht geprüft. Produktvergleich bleibt V1 ohne SEO-Laufzeitabhängigkeit. Später darf SEO ausschließlich upstream priorisieren/Metadaten liefern.

KISS:
Keine neue SEO-API auf Verdacht, keine Rückkopplung in Writer oder Produktwissen.


## DESIGN-SCRIPT-001 – Miniänderungen im DESIGN-Hobbyraum nur noch per Fail-Closed-Runner

STAND:
2026-09-07 / VERBINDLICH / MIT DESIGN-ORDER-SWAP-002 LIVE BEWÄHRT.

WAS:
Für lokale DESIGN-Miniänderungen wird der manuelle Patchweg gesperrt.
`MINIMAL_PATCH_RUNNER.py` ist der einzige Arbeitsweg.

WARUM:
Mehrere Fehlversuche zeigten, dass eine einfache Verschiebung durch Interpretation, zusätzliche Umbauten und unzureichend zielgenaue Prüfungen unnötig vergrößert wurde.

ZWANG:
- exakte Baseline per SHA;
- genau eine Paketdatei;
- nur zwei vollständige benachbarte Bereiche tauschen;
- keine Inhalts-/CSS-/Markup-/Versionsänderung;
- automatische Positiv-/Negativprüfung;
- Reversibilität zum byte-identischen Vorgänger;
- FAIL = kein Artefakt.

PLUGINHYGIENE:
Im Hobbyraum nur ein überschreibbarer Kandidat.
Keine neue Pluginversion pro Fehlversuch.
Releaseversion erst nach bestätigtem LIVE-PASS.

BELEG:
`PROJEKTE/PFERDE_ATELIER/DESIGN/MINIMAL_PATCH_RUNNER.py`
`PROJEKTE/PFERDE_ATELIER/DESIGN/MINIMAL_PATCH_JOB_CURRENT.json`
`PROJEKTE/PFERDE_ATELIER/DESIGN/MINIMAL_PATCH_LAST_RECEIPT.json`


## ARCH-081 – Tresor-Nutzerweg ist exakt ein Download

WAS:
Der Nutzerweg des Tresors wird auf genau eine Handlung reduziert:
`GitHub Releases -> neueste TRESOR_PASS-Komplettsicherung herunterladen -> lokal speichern`.

WARUM:
Die bisherigen Mac-Kits und Einzelkommandos verlagerten interne Sicherungstechnik auf den Nutzer und verletzten damit das KISS-Ziel.

KISS:
Kein separates Tresor-Repository erforderlich.
Der bestehende GitHub-Releases-Bereich wird als fester Download-Ort genutzt.

REGEL:
Pro gültigem Sicherungsstand genau eine verschlüsselte Datei.
Keine Nutzerkommandos, keine manuellen Teilarchive, keine zusätzlichen Projektdateien.

PASS-GRENZE:
Eine Datei erscheint erst als gültige `TRESOR_PASS`-Sicherung, nachdem der vollständige Restore aus genau dieser Datei bewiesen ist.


## ARCH-082 – Tresor läuft serverseitig, Nutzer bleibt reiner Downloader

WAS:
Die regelmäßige Ein-Datei-Sicherung wird serverseitig in GitHub vorbereitet.
Der Nutzer-Mac ist weder Backup-Runner noch Voraussetzung für die Erzeugung.

KISS:
Ein interner Builder + ein Workflow.
Für den Nutzer unverändert genau ein Weg:
`GitHub Releases -> TRESOR_PASS-Datei herunterladen`.

PRÜFREIHENFOLGE:
Build -> Verschlüsselung -> Wiederentschlüsselung -> Hash-/Git-Restore-Prüfung -> erst danach Release.

WACHSTUMSSCHUTZ:
Frühere `tresor-*`-Backups werden nicht in neue Backups eingebettet.

GRENZE:
Produktiv erst nach Bindung von WordPress-Vollbackup, serverseitigem Roharchiv, Recovery-Bundle und Masterpasswort sowie kontrollierter Workflow-Aktivierung.


## DESIGN-ORDER-003 – Affiliate-Produkte vor Beitragsvorschau LIVE

STAND:
2026-09-07 / LIVE PASS.

WAS:
Auf der zentralen Kategorieebene wurden ausschließlich die vollständigen Blöcke
`pa266-products` und `pa297-popular` gegeneinander getauscht.

ERGEBNIS:
Affiliate-Produkte / Produktvorschläge stehen über der Beitragsvorschau.
Affiliate-Banner, Artikel, Verweise, CSS, Texte, V104 und alle übrigen Bereiche bleiben unverändert.

UMSETZUNG:
Ausschließlich über den fail-closed `MINIMAL_PATCH_RUNNER.py`.
Keine manuelle Reparatur.

LIVE-BELEG:
`PROJEKTE/PFERDE_ATELIER/DESIGN/LIVE_PASS_DESIGN_ORDER_SWAP_002.md`

LIVE-SHA:
`11b664a10d4ef0ec82f0011436eb92715d9efd14474893fecddcb64e91e6fe0b`


## DESIGN-ORDER-003 – Affiliate-Produkte stehen vor der Beitragsvorschau

STAND:
2026-09-07 / **LIVE PASS**.

WAS:
Auf der zentralen Pferde-Atelier-Kategorieebene stehen die **Affiliate-Produkte / Produktvorschläge** vor der **Beitragsvorschau / Meistgelesen**.

UNVERÄNDERT:
Affiliate-Banner, Artikel-/Verweisstruktur, Texte, CSS, Karten/Links, Beitragsauswahl, Affiliate-Auswahl, Produktlogik und V104.

WARUM:
Gewünscht war ausschließlich, die Produktvorschläge früher sichtbar zu machen. Frühere Fehlversuche veränderten versehentlich andere Blöcke.

TECHNISCH:
Finaler Job `DESIGN-ORDER-SWAP-002`, ausgeführt ausschließlich über `MINIMAL_PATCH_RUNNER.py` gegen die exakte V1.50.472-Baseline.

PASS:
HARD LOCAL Positiv/Negativ + Reversibilität PASS; Nutzer-LIVE-PASS auf „Gebisse“ am 2026-09-07.

BELEG:
`PROJEKTE/PFERDE_ATELIER/DESIGN/LIVE_PASS_DESIGN_ORDER_SWAP_002.md`
`PROJEKTE/PFERDE_ATELIER/DESIGN/MINIMAL_PATCH_LAST_RECEIPT.json`


## ARCH-083 – ABGELÖST: falsche Erweiterung des GitHub-Backupauftrags

STATUS:
ABGELÖST durch ARCH-086.

HISTORISCHER FEHLER:
Der GitHub-Backupauftrag wurde fälschlich auf WordPress + Projektarchiv erweitert.

REGEL:
Nicht als aktuelle Sicherungsarchitektur verwenden.


## ARCH-084 – Hobbyraum-Arbeitsauftrag wird maschinenlesbar und serverseitig sperrbar

STAND:
2026-09-07 / vorbereitet, noch nicht auf main aktiviert.

WAS:
Der bestehende Hobbyraum erhält für technische Arbeiten einen maschinenlesbaren `HOBBYROOM_WORK_LOCK_V1`.

Der bereits vorhandene Security-PR #137 wurde KISS erweitert:
Sein ohnehin auf jeder PR laufender `verify-pr`-Schritt prüft zusätzlich den aktuellen Hobbyraum-Lock.

WIRKUNG NACH AKTIVIERUNG:
- `FIX_FORBIDDEN` → technische PR im gebundenen Scope BLOCK;
- fehlender 7-Punkte-PASS → BLOCK;
- falscher Branch/Head/main-Basis → BLOCK;
- Pfad außerhalb des freigegebenen Kandidatenscopes → BLOCK;
- `INTEGRATION_ALLOWED=false` → BLOCK;
- nur exakt gebundener Kandidat → PASS.

WARUM:
Reine Text-/Promptregeln verhindern nicht zuverlässig, dass ein Arbeitschat neue Prüfpfade oder Minifixes beginnt.
Der Hobbyraum soll deshalb nicht nur erinnern, sondern die Integrationsgrenze technisch fail-closed binden.

KISS:
- keine neue Campus-Ebene;
- kein neuer Workflow;
- keine zweite Tür;
- vorhandener Hobbyraum;
- vorhandener #137-Scope-Gate;
- vorhandener hardlock-base.

UNVERÄNDERT:
Produktionsarchitektur, Single Door, dumme Wächter, Fachlogik, Qualität, Inhalt, Design, PPM/PSERC/PSTE, LanguageTool und Publish-Sperre.

AKTIVIERUNGSGRENZE:
Security-PR #137 ist weiterhin nicht gemergt.
Current immutable-base-Hardlock blockiert Security-Wartung absichtlich.
Kontrollierte Admin-Aktivierung bleibt erforderlich.

BELEG:
- `BAUCONTAINER/HOBBYRAUM_STANDARD.md`
- `PROJEKTE/PFERDE_ATELIER/TEXT/HOBBYRAUM.md`
- Security-PR #137 / Head `5e0547c999a544d57e1891776f2f417e836eb605`
- GitHub normaler hardlock auf diesem Head: PASS.


## TEXT-TECH-20260907-PLANAB – Plan A und Plan B strikt getrennt

WAS:
Plan A (bestehender Produktionsweg) und Plan B (Slimline-Shadow) werden unabhängig gebaut, geprüft und gelagert.
Plan B = Draft-PR #143 / `plan-b/text-slimline-shadow-v1-20260907`; keine Produktionsverdrahtung, kein Merge.

WARUM:
A/B-Vergleich soll jederzeit möglich bleiben, ohne dass Fixes, Tests oder Zustände zwischen den Linien vermischt werden.

REGEL:
Keine automatische Fixübernahme, kein Cherry-Pick/Teilmischen während der Vergleichsphase. Gemeinsame Basis dürfen nur dieselben Testdaten und unveränderten Qualitäts-/Sicherheitsregeln sein.


## TEXT-TECH-20260907-LIVE-LT – B01 integriert, erster neuer Liveblocker LanguageTool

WAS:
B01-only PR #141 wurde integriert; current main = `f14ccf187b94c4beab9a86d0c69144f792ba2f64`.
Der reale Plan-A-Codex-Lauf stoppte bei `BOUND_LANGUAGETOOL_EXECUTION_PATH_MISSING` vor Abschluss von 107007.

WARUM:
#141 war der kleinste kausal isolierte Kandidat für den vorherigen B01-Liveblocker. Der anschließende Lauf sollte ausschließlich den nächsten realen technischen Zustand sichtbar machen.

REGEL:
B01 nicht als erneut live bestanden behaupten; neuer Lauf erreichte B01 nicht. LanguageTool-Einzelbranch bleibt Parkplatz.


## TEXT-TECH-20260907-CORRIDOR – Anti-Minifix / echte Evidence-Autoritäten

WAS:
Pauls direkte Pipeline-Befunde, B01–B15/M01–M33, letzter echter 7/7-Stand und neuer LT-Livebefund wurden in einer technischen Corridor-Matrix zusammengeführt.

WARUM:
Wiederkehrende Fehler sind überwiegend dieselbe Klasse: geforderte Ausführung/Evidence ist nicht eindeutig gebunden oder angrenzende Gates beziehen sich auf unterschiedliche Artefaktzustände. Weitere isolierte Minifixes würden die Fehlerkette fortsetzen.

REGEL:
Kein Worker-selbstgeschriebenes PASS/Stage-Proof darf allein echte Prüfung beweisen. Keine neue Facharchitektur; vorhandene echte Prüfer/Evidence-Quellen müssen in der bestehenden einen Straße mechanisch eindeutig gebunden sein.


## ARCH-085 – Verbindlicher A–F-Pre-Fix-Ablauf für technische Hobbyräume

WAS:
Der allgemeine Hobbyraum-Standard erhält denselben verbindlichen Ablauf wie der TEXT-Hobbyraum:
Ausgangspunkt → 7 Pflichtchecks → Anti-Minifix → genau ein KISS-Kandidat → Positiv/Negativ/Invarianten → erst dann Realtest.

WARUM:
Ein bloßer Prompt oder Chat-Hinweis verhindert wiederholte Minifix-Schleifen nicht zuverlässig. Der Arbeitsraum muss die Reihenfolge und Fix-Sperre dauerhaft vorgeben.

GRENZE:
Keine Fachlogik im Hobbyraum. Eine Tür, dumme Wächter und fachliche Autoritäten bleiben unverändert.


## ARCH-086 – GitHub-Backup-Scope hart wiederhergestellt

STAND: 2026-09-07.

WAS:
Der Notfall-Tresor für diesen Auftrag sichert ausschließlich GitHub für
`hallo-netizen/affiliate-pferdeportal`.

WARUM:
Der vorhandene GitHub-only-Tresorweg war bereits real gebaut und restore-geprüft.
Die spätere Erweiterung um WordPress/Projektarchiv verletzte Nutzerauftrag und BAU-032.

KISS:
Bestehenden GitHub-Tresorworkflow weiterverwenden und härten; keine neue Backup-Engine.

REGRESSIONSSCHUTZ:
- TRESOR/START_HERE enthält GITHUB-ONLY-SCOPE-LOCK;
- HANDLUNGSVERZEICHNIS verbietet WordPress/Projektarchiv ohne neuen ausdrücklichen Auftrag;
- BAU-038 dokumentiert den Wiederholungsfehler;
- falsche WordPress-Backuptechnik wird aus `control/tresor` entfernt.

PASS-GRENZE:
Git-Restore real PASS; vollständiges GitHub-PASS erst nach Abdeckung bzw. belegter Nichtrelevanz nicht lesbarer Admin-Einstellungen.


## TEXT-TECH-20260908-FROZEN-RECOVERY – Ein Reparaturalgorithmus, kein Konzeptwechsel

WAS:
Der TEXT-Wiederaufbau ist fest gebunden an:
`de21f6…` → erster realer Blocker → vier Pflichtquellen prüfen → genau ein Delta → Positiv/Negativ → echter 7/7-Realtest → PASS einfrieren oder Regression vollständig zurückbauen.

WARUM:
Mehrfaches Wechseln zwischen Minifixes, Security-Umbauten und parallelen Ansätzen erzeugte neue Fehler und machte den funktionierenden Stand schlechter reproduzierbar.

REGEL:
Kein zweites Reparaturkonzept, kein zweiter Kandidat zwischen Realtests, kein Fix auf einen fehlgeschlagenen Fix.

HAUPTQUELLE:
`PROJEKTE/PFERDE_ATELIER/TEXT/HOBBYRAUM.md`.

## TEXT-TECH-20260908-B02-SEMANTIC – Historische Semantik statt alter Hash-Snapshot

WAS:
Der vollständige historische B02-Dateisnapshot wurde nach `INPUT_HASH_MISMATCH` verworfen.
Nur die historisch bewiesene Worker-Bindungssemantik wurde auf die aktuelle Hashkette übertragen.

WARUM:
Hashgebundene alte Gesamtdateien sind nicht sicher auf einen späteren Zwischenstand übertragbar; die fachlich/technisch notwendige Semantik kann trotzdem exakt isoliert werden.

BELEG:
B02-Kandidat `562b71c7…`: `hardlock` PASS + `hardlock-base` PASS.
Merge `36d1ecb5…`.
Realer Lauf kam über B02 hinaus und stoppte erst bei B07/M32.

REGEL:
Historische Fixquelle ist Beleg für die Semantik, nicht automatische Cherry-Pick-/Dateisnapshot-Freigabe.

## ARCH-084 – STATUSKORREKTUR 2026-09-08

Der zuvor als vorbereitet dokumentierte `HOBBYROOM_WORK_LOCK_V1` / `hardlock-base`-Weg ist inzwischen auf main aktiviert und im Ruleset `Pferde Atelier Main Hardlock` wieder als Required Check gebunden.

Die frühere Formulierung „noch nicht auf main aktiviert“ ist damit historisch überholt.

Der allgemeine Hobbyraum-Standard bleibt die zuständige campusweite Regel; keine zweite Architektur wurde geschaffen.


## ARCH-087 – Regelmäßiger GitHub-Doppelklick-Backupweg

STAND: 2026-09-08.

WAS:
Der Nutzerweg ist ein wiederverwendbares lokales Werkzeug:
`GITHUB_BACKUP_STARTEN.command`.

WARUM:
Gefordert ist regelmäßiges GitHub-Backup, nicht die einmalige Bereitstellung einer Snapshot-Datei.

HARD GATES:
- frische Refs am Anfang;
- kompletter Git-/Campus-Restore aus finaler ZIP;
- frische Refs am Ende;
- Änderung während Lauf = BLOCK;
- fester `GITHUB_BACKUP_AKTUELL.zip`-Stand wird nur nach PASS ersetzt.

PASS:
`GITHUB_DATEIEN_CAMPUS_1ZU1_RESTORE_PASS`
+
`AKTUELLITAET_PASS`.

GRENZE:
GitHub-Secret-Werte und providerinterne IDs sind nicht als 1:1-Export behauptbar.


## ARCH-088 – Tresor und lokales Backup unabhängig

STAND: 2026-09-08.

WAS:
Der Tresor ist wieder eine echte eigenständige Sicherungsinstanz.
Er läuft automatisch wöchentlich und speichert außerhalb GitHubs.
Das lokale Mac-Backup bleibt als zweite unabhängige Sicherung per Doppelklick bestehen.

WARUM:
Auch bei längerer Zeit ohne lokalen Backup-Lauf muss eine aktuelle Notfallsicherung existieren.

KISS:
Eine GitHub-Backupfachlogik, aber zwei unabhängige Auslöser/Speicherorte:
- Tresor automatisch;
- Mac manuell.

REGRESSIONSSCHUTZ:
Keiner der beiden Wege darf den anderen als Voraussetzung haben.

## TEXT-TECH-20260908-HISTORY-MACHINE-PROOF – Eine maschinelle Reparaturstraße statt wiederholter Chat-Prüfung

WAS:
Der TEXT-Reparaturweg wird serverseitig auf eine einzige, maschinengebundene Evidenzkette reduziert:
- current main;
- erster realer Blocker;
- letzter real funktionierender Stand (`RECOVERY_BASE_SHA`);
- exakter Kandidatenscope;
- autoritative Fach-Fehlerquelle;
- zuständige CURRENT_STATE;
- Paul-Pipeline-Audit;
- fortlaufende historische Fehlermatrix;
- vertrauenswürdiger historischer Regression-Runner vom aktuellen PR-Base/main;
- Änderungs-/Erklärungsregister;
- campusweiter Hobbyraum-Standard;
- vollständiges Ausführungs-/Testprotokoll.

Der Runner-Bootstrap PR #159 ist auf main `2f3678aa…` integriert.
Die stale Regressionen M26/M28/M31 wurden korrigiert; M28 besitzt einen Negativ-Mutanten-Selbsttest.

WARUM:
M28 war bereits schriftlich bekannt und wurde trotzdem erneut eingeführt.
Die Ursache war nicht Informationsmangel, sondern fehlende technische Kopplung:
Chat/Hobbyraum konnte `CHECK_HISTORY: PASS` behaupten, obwohl ausführbarer Regressionstest und historische Definition auseinanderliefen.

DAUERHAFTER ZWANGSWEG NACH AKTIVIERUNG VON PR #160:
1. Branch, Head, Base und erlaubter Dateiscope müssen exakt zum offiziellen Hobbyraum passen.
2. Manuelle `CHECK_*`-Felder sind keine Integrationsautorität.
3. Alle Evidenzquellen werden per Git-Blob an exakt den geprüften Stand gebunden.
3a. Das Ausführungsprotokoll muss aktuellen Blocker, current main und `RECOVERY_BASE_SHA` real enthalten; sonst BLOCK.
4. Historische Fehler müssen ab M01 lückenlos sein; mindestens M01–M33 bleiben Pflicht.
5. Matrix, Runner und autoritative Fehlerquelle müssen dieselbe akzeptierte Fehlerhistorie tragen.
6. `ACTIVE_BLOCKER` muss real in Fehlerquelle und CURRENT_STATE stehen.
7. `MAIN_SHA` und `RECOVERY_BASE_SHA` müssen real in CURRENT_STATE stehen.
8. Pauls Kernregeln werden semantisch geprüft: kein Sammelfix, historische Fehlerquelle, bestehende Regression, echter 7/7-Produktionsbeweis, Vertragskollision, Artefaktzustands-Parität, Hash-Semantik, Pre-/Post-Transformation.
9. Frozen-Recovery, kausaler Corridor und Maschinenbeweis-Entscheidung müssen im Änderungsregister stehen.
10. Historienprüfung, letzter funktionierender Stand, direkte Nachbarn, Wiederholungsfehlerklasse, Positiv/Negativ und STOP ohne Reparatur im Realtest müssen im Hobbyraum-Standard stehen.
11. Jeder Produktionskandidat muss den kompletten vertrauenswürdigen historischen Runner vom PR-Base/main GESAMT PASS machen.
12. Produktionscode darf Matrix/Runner nicht im selben PR ändern.

NEUER FEHLER = ZUERST MASCHINELLE ERINNERUNG:
- Ein neu real auftretender Fehler wird als nächstes Mxx in Fehlerquelle, Matrix und Runner aufgenommen.
- Dafür ausschließlich separater Plan `HISTORY_AUTHORITY_MAINTENANCE`.
- `HISTORY_EXPECTED_FAIL` bindet exakt diesen neuen/zu korrigierenden historischen Fehler.
- Der Base-Runner muss alle bisher akzeptierten Fehler weiter PASS halten.
- Der Kandidaten-Runner muss auf dem **noch unreparierten** Stand exakt bei `HISTORY_EXPECTED_FAIL` als erstem Fehler FAIL liefern.
- Bestehende Historie darf nicht verkürzt oder übersprungen werden.
- Erst nach dieser FAIL-Reproduktion darf der Produktionsfix entstehen.
- Der spätere Produktionsfix muss die komplette erweiterte Historie PASS machen.
- Dadurch können M34, M35, ... ohne erneute Security-Gate-Änderung aufgenommen werden.

SELBSTSCHUTZ:
- Gate-Arbeitslock- und Evidenz-Selbsttests laufen bei jedem serverseitigen `verify-pr` automatisch.
- Negativfälle prüfen fehlende Historienabdeckung, Lücken, Paul-Regeln, Entscheidungsregeln, Standardregeln und fehlenden letzten guten Stand.
- Eine künstliche Erweiterung um M34 ist als Positivfall eingebaut.
- `CHECK_*` darf auf PENDING stehen und kann den Maschinenbeweis weder ersetzen noch erzeugen.

STATUS:
- PR #159: integriert.
- PR #160: exakt eine Security-Datei.
- aktueller PR-Head: `3059c907be76477e44e2396430551c4bec35feb6`.
- PR #160 bleibt nur durch `IMMUTABLE_SECURITY_PATH_CHANGE_BLOCKED` blockiert, weil der bestehende Hardlock seine eigene Gate-Datei schützt.
- Ein direkter Mergeversuch wurde von GitHub mit Repository-Rule-Verstoß abgewiesen; kein Chat-seitiger Admin-/Ruleset-Schreibweg existiert.
- Historischer PR #137 belegt denselben kontrollierten Einmal-Admin-Wartungsweg.
- M28-Produktionsfix bleibt bis zur Aktivierung eingefroren.
