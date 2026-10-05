# ÄNDERUNGS- UND ERKLÄRUNGSREGISTER

STAND: 2026-10-03

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

## ARCH-044 – Pferde-Atelier TECHNIK-Büro
WAS:
`PROJEKTE/PFERDE_ATELIER/TECHNIK/` als eigenes Betriebs-/Diagnosebüro für WordPress-/Hosting-Speicher, Backups und sichere technische Wartung; dazu campusweites Routing und klare Trennung zum PLUGINS-Büro.
WARUM:
Die reale Arbeit an WordPress-Speicher-/Backupzuständen erzeugt eine dauerhafte technische Facharbeit mit eigenem CURRENT_STATE und NEXT ACTION. Das bisherige `WORDPRESS_REGISTER.md` ist bewusst nur Technologieindex und darf diese Betriebswahrheit nicht übernehmen.
KISS:
Kein neues WordPress-Gebäude. Ein zusätzliches Projektbüro reicht. PLUGINS bleibt Inventar-/Artefaktpult; TECHNIK führt Betriebs-/Diagnosezustand.
REGEL:
Bürotür nur Navigation; CURRENT_STATE = eine aktuelle Technikstandwahrheit; HOBBYRAUM = eine aktuelle Arbeitsbindung. Pluginänderungen zusätzlich nach PLUGINS/SYNC_VERTRAG synchronisieren.
BELEG:
`PROJEKTE/PFERDE_ATELIER/TECHNIK/START_HERE.md`

## TEXT-TECH-20260907-CORRIDOR – Anti-Minifix / echte Evidence-Autoritäten
WIEDERHERGESTELLT AUS REGISTERSTAND 2026-09-09; keine neue Entscheidung.

## TEXT-TECH-20260908-FROZEN-RECOVERY – Ein Reparaturalgorithmus, kein Konzeptwechsel
WIEDERHERGESTELLT AUS REGISTERSTAND 2026-09-09; keine neue Entscheidung.
REGEL:
Kein zweites Reparaturkonzept, kein zweiter Kandidat zwischen Realtests, kein Fix auf einen fehlgeschlagenen Fix.

## TEXT-TECH-20260908-HISTORY-MACHINE-PROOF – Eine maschinelle Reparaturstraße statt wiederholter Chat-Prüfung
WIEDERHERGESTELLT AUS REGISTERSTAND 2026-09-09; keine neue Entscheidung.

## ARCH-089 – Campusweit genau eine Current-Autorität pro Arbeitsbereich

WAS:
Der Campus wurde von der bisherigen Zweiteilung `CURRENT_STATE = Stand` plus `HOBBYRAUM = aktuelle Arbeit/NEXT ACTION` auf genau **eine Current-Autorität pro Scope** umgestellt.

ROUTING:
`protocol/PROJECT_MEMORY/AUTORITAETSPLAN.json` benennt ausschließlich, **wo** die eine Current-Autorität liegt. Der Plan enthält selbst keinen Fachstatus.

WARUM:
Neue Chats mussten trotz Übergabe Stand, Hobbyraum, Branches und Protokolle wieder gegeneinander rekonstruieren. Die auf zwei Dateien verteilte dynamische Wahrheit war die strukturelle Ursache.

REGEL:
Die Current-Autorität besitzt Status, aktuellen belastbaren Stand, ersten Blocker und genau eine NEXT ACTION. START_HERE, Hauptpförtner, Gebäude- und sonstige Türen sind Navigation only. HOBBYRAUM ist nur `DERIVED_EXECUTION_SURFACE_V1`.

SPEZIALFALL:
Existiert bereits eine stärkere technische Current-Autorität, wird keine Campus-Kopie gepflegt. Für Pferde-Atelier AFFILIATE ist ausschließlich `control/release-governance/CURRENT_RELEASE.json` Current-Autorität; die frühere Campus-CURRENT_STATE ist nur noch Pointer.

FRISCHE:
`NO_FULL_REDISCOVERY_IF_CURRENT_BINDING_FRESH`.
Bei belegter Änderung gilt `ON_BINDING_CHANGE_INSPECT_DELTA_ONLY`.

SCHUTZ:
`BAUCONTAINER/EINE_WAHRHEIT_STANDARD.md` + `BAUCONTAINER/single_truth_guard.py`.



## ARCH-090 – Hobbyraum immer nur temporär genutzt
WAS:
Hobbyraum-Nutzung ausdrücklich als temporär klargestellt.
WARUM:
Ein Hobbyraum ist nur Arbeitsfläche für einen konkreten Auftrag und darf keine dauerhafte Status- oder Fachwahrheit werden.
REGEL:
Nach Abschluss/Rückgabe endet die Arbeitsbindung; dauerhafte Wahrheit bleibt in Current-/Protokoll-/Fachquellen.
BELEG:
`BAUCONTAINER/HOBBYRAUM_STANDARD.md`


## ARCH-091 – Neues Projektgebäude HOBBYRAUSCH mit Plugin-Einzelwahrheit

WAS:
Neues Projektgebäude `PROJEKTE/HOBBYRAUSCH/` startet leer auf Basis der bewährten Campusregeln.

WARUM:
Hobbyrausch soll von Anfang an ohne historische Mischzustände aufgebaut werden. Insbesondere darf sich das Pferde-Atelier-Problem mehrerer konkurrierender Pluginstände nicht wiederholen.

REGEL:
- zentrale Campusdienste Hauptpförtner, Hausmeister, Archiv und Tresor bleiben einmalig zentral;
- jedes Hobbyrausch-Büro besitzt genau eine Current-Autorität;
- jedes einzelne Plugin erhält später genau eine Akte `PLUGINS/PLUGIN_AKTEN/<PLUGIN-ID>/CURRENT.md`;
- unveränderte Originalplugin-Dateien liegen separat unter `.../<PLUGIN-ID>/ORIGINAL/`;
- Register, Originalablage, Historie und Hobbyraum sind niemals zweite Current-Wahrheiten;
- Pferde-Atelier ist nur Struktur-/Erfahrungsreferenz, kein automatisch übernommener Bestand.

BELEG:
`PROJEKTE/HOBBYRAUSCH/START_HERE.md`


## ARCH-092 – Neues Projektgebäude MENSCH mit eigenem Konzeptbüro

WAS:
Neues Projektgebäude `PROJEKTE/MENSCH/` mit zunächst genau einem Büro `KONZEPT/`.

WARUM:
Die bereits zusammengetragenen menschbezogenen Portal-, Affiliate-, Abo-, Weiterbildungs- und E-Learning-Ideen sollen getrennt von allen nicht-menschlichen Projekten dauerhaft konsolidiert werden. Bislang gab es dafür kein eigenes Campus-Projektgebäude.

REGEL:
- ausschließlich Themenfeld Mensch;
- keine Nicht-Mensch-Themen;
- zunächst nur das tatsächlich benötigte Büro `KONZEPT`;
- genau eine Current-Autorität über Scope `MENSCH_KONZEPT`;
- `KONZEPT_MASTER.md` enthält dauerhaften Konzeptinhalt, aber keinen dynamischen Current-Status;
- `HOBBYRAUM.md` bleibt nur temporäre Ausführungsfläche;
- weitere Büros erst bei echtem Bedarf.

BELEG:
`PROJEKTE/MENSCH/START_HERE.md`


## ARCH-093 – LANDINGPAGES-Büro im Pferde-Atelier

WAS:
Neues Projektbüro `PROJEKTE/PFERDE_ATELIER/LANDINGPAGES/` für eigenständige Vergleichs-, Rechner-, Such- und Angebots-Landingpages.

WARUM:
Landingpages sollen im Frontend in vorhandene Portalstrukturen eingebunden werden können, ohne als Fake-Kategorien in KATEGORIEN.tsv, PSTE, PSERC oder normale TEXT-Produktion zu geraten.

REGEL:
- Landingpage = normale WordPress-Seite, keine Kategorie;
- optisch darf sie als zusätzliche Themenkachel erscheinen;
- technische Darstellung bleibt DESIGN-Verantwortung;
- Provider/Rechner/Banner bleiben AFFILIATE-Verantwortung;
- erster Pilot ausschließlich `Pferdehaftpflicht vergleichen`;
- keine allgemeine Automatik vor Pilot-PASS.

BELEG:
`PROJEKTE/PFERDE_ATELIER/LANDINGPAGES/START_HERE.md`


## HOBBYRAUSCH-HD001-20261003 – Kategorie-Ziel vom Pilot zum vollautomatischen Gesamtweg erweitert

WAS:
Für Hobbyrausch/HD-001 wurde ein eigener aktiver Zielvertrag angelegt. Der erfolgreiche V1.9.4-Buchbinden-Pilot bleibt produktive Basis, ist aber nicht mehr das Endziel der Kategoriearbeit.

WARUM:
Der Nutzer hat den Zielrahmen ausdrücklich erweitert: DataForSEO soll die konkreten sichtbaren Bezeichnungen und die Hierarchie bestimmen; Hauptportal, Magazin und HivePress müssen gemeinsam bis WordPress-Publish, sichtbarer Frontend-Navigation und Readback geführt werden.

REGEL:
- Konzept bestimmt Geschäftslogik und Strukturprinzip;
- DataForSEO bestimmt innerhalb dieser Grenzen konkrete Namen und Parent-/Child-Hierarchie;
- keine feste Root+4-Kinder-Grenze als Zielarchitektur;
- Hobbyfinder bleibt vom SEO-Baum getrennt;
- Vollautomatik ist Normalweg;
- keine Abnahme ohne lokale Positiv-/Negativ-E2E-Simulation bis Frontend plus realen Endzustands-Readback;
- V1.9.4 bleibt live und darf nicht zurückgerollt oder aus alten Dateien rekonstruiert werden;
- technische Weiterentwicklung erst nach bytegenauer Bindung der echten V1.9.4-Source.


## HOBBYRAUSCH-HD001-20261005 – V1.9.5 Direct Publish auf echter V1.9.4-Basis

WAS:
Die zuvor nur in GitHub fehlenden exakten V1.9.4-Source-/Installer-Bytes wurden im Library-Campus-Archiv wiedergefunden und gegen die dokumentierten SHA-256 verifiziert. Darauf wurde V1.9.5 als kleinster KISS-Nachfolger gebaut.

WARUM:
Der produktive Buchbinden-Pilot war technisch readback-geprüft, WordPress-Seiten wurden aber noch als Draft erzeugt und der Normalweg enthielt unnötige menschliche Review-/Deploy-Freigabeschleifen. Für die gewünschte Sichtprüfung auf der noch nicht öffentlich zugänglichen Site müssen gebundene Seiten direkt veröffentlicht werden.

REGEL:
- V1.9.4-Livebestand bleibt Ausgangsbasis;
- keine neue Pluginlinie;
- Research-/Ownership-Gates bleiben erhalten;
- serverseitige signierte Receipts bleiben erhalten, werden im Normalweg aber automatisch nach Hard-PASS erzeugt;
- WordPress-Seiten-Zielstatus = publish;
- Status gehört zu Preflight/Fingerprint/Readback;
- V1.9.4-Draft-Baseline darf einmalig sicher auf Publish migrieren;
- danach Statusdrift fail-closed;
- keine Live-Abnahme ohne realen WordPress-Publish + Readback.

LOKALE EVIDENZ:
251/251 V1.9.4-Baseline PASS; V1.9.5 256/256 PASS; Fresh-Source 256/256 PASS; Runtime-Parität 22/22 PASS.


## HOBBYRAUSCH-HD001-20261005-B – Kategorien müssen inkrementell erweiterbar bleiben

WAS:
HD-001 erhält mit V1.9.6 einen echten Sparse-Extension-Vertrag. Eine spätere Ergänzung muss nur neue oder geänderte Knoten liefern; der vorhandene produktive Baum wird serverseitig aus der Lifecycle-Baseline erhalten und ergänzt.

WARUM:
Der Nutzer verlangt ausdrücklich einen dauerhaft flexiblen Kategorienbaum. Neue Hobbys, Unterseiten, Leaf-Kategorien, Magazin- oder HivePress-Zweige dürfen keinen kompletten System- oder Kategorienbaum-Neuaufbau erfordern.

REGEL:
- stable identity = concept_id;
- sparse extension merge gegen aktuelle Baseline;
- nicht genannte Alt-Knoten = behalten;
- keine automatische Löschung;
- Löschung/Retirement im Extension-Pfad = BLOCKED;
- falsche project_id / Baseline-Hash / Parent = BLOCKED;
- nach Merge laufen die bestehenden Hard-Gates weiter;
- Deployment schreibt nur das tatsächliche Delta.

REALTEST:
Echte Buchbinden-Preview mit 7 Knoten + 1 synthetischer Extension-Knoten → 7 UNCHANGED + 1 ADDED, 0 RETIRED, automatic_delete=false.

LOKALE EVIDENZ:
V1.9.6 263/263 PASS; Fresh Source 263/263 PASS; Runtime Source↔Installer 23/23 byteidentisch; Installer PHP 17/17 PASS.


## HOBBYRAUSCH-HD001-20261005-C – Sichtbarer Frontend-Endzustand ist zwingender Teil der Abnahme

WAS:
Beim realen Buchbinden-Pilot wurde ein bisher übersehener Endzustandsfehler gefunden: `Buchbinden` war als WordPress-Seite sichtbar, die vier fachlich gebundenen Content-Unterkategorien aber nicht. Der alte Writer speicherte die Cross-Adapter-Beziehung nur als Metadaten und der alte Readback prüfte ausschließlich technische WordPress-Objekte.

WARUM:
Ein WordPress-Seitenobjekt und Taxonomie-Terme können technisch korrekt existieren, ohne dass die Beziehung auf der Seite sichtbar wird. Genau dieser Zustand war live vorhanden und wurde lokal reproduziert: Write PASS + technischer Readback PASS + publish PASS, aber Frontend FAIL.

REGEL:
- technischer WordPress-Readback allein ist niemals End-PASS;
- Seiten mit direkten Content-Kindern müssen diese Kinder persistent im sichtbaren Seiteninhalt verlinken;
- hierfür wird ein klar markierter, vom Workflow verwalteter Block im `post_content` verwendet;
- kein zweites Plugin, kein Theme-Hack und kein Laufzeit-`the_content`-Filter;
- Magazin/HivePress dürfen nicht in den Content-Kinderblock leaken;
- vorhandener redaktioneller Inhalt außerhalb des Managed Blocks bleibt unberührt;
- Sparse-Erweiterungen ändern nur den notwendigen Block;
- fehlender/manipulierter sichtbarer Endzustand blockiert bzw. löst Rollback aus;
- Abnahme erst nach realem Frontend-Readback.

LOKALE EVIDENZ:
Vor Fix wurde der Live-Fehler hart reproduziert. Nach Fix: 275/275 PASS; Fresh Source 275/275 PASS; Source↔Installer 23/23 byteidentisch; Source-PHP 17/17 PASS; Installer-PHP 17/17 PASS; echte Buchbinden-Topologie mit exakt vier Content-Kindern geprüft.


## HOBBYRAUSCH-HD001-20261005-D – WordPress-Hierarchieübersetzung vor Frontend-Fix

WAS:
Der zuvor gebaute V1.9.7-Frontend-Linkblock wurde vor Live-Installation verworfen. Eine nachgelagerte harte Prüfung zeigte, dass der eigentliche Fehler tiefer liegt: Der Buchbinden-Pilot übersetzt den fachlichen Baum nicht in die vorgesehene WordPress-Tiefe.

WARUM:
Der Fachvertrag lautet SEITE → SEITE → SEITE → KATEGORIE → BEITRÄGE. Der Pilot erzeugt technisch nur Buchbinden als Seite und die vier Leafs als Core-Kategorien. WordPress kann eine Taxonomie-Kategorie nicht nativ als Kind einer Seite führen; der aktuelle Writer setzt bei diesem Adapterwechsel den nativen Term-Parent auf 0 und speichert nur eine logische Meta-Beziehung. Ein sichtbarer Linkblock würde dies nur kaschieren.

ZUSÄTZLICHE BEFUNDE:
- Validator erlaubt Level 1..20, Builder erzeugt jedoch nur Root-Seite + maximal vier direkte Kategorie-Kinder;
- wiederkehrende sichtbare Leafs wie „Einstieg“ werden APKW-seitig global blockiert;
- Content und Magazin teilen aktuell die Core-Taxonomie category;
- native Term-Hierarchie funktioniert nur innerhalb derselben hierarchischen Taxonomie;
- HivePress listing_category ist upstream hierarchisch definiert;
- WordPress-Core-Escaping von „&“ ist separat korrekt behandelt und nicht die Ursache.

REGEL:
Kein weiterer Live-Installer, bis ein exakter WordPress-Übersetzungsvertrag für die vollständige Fachhierarchie lokal positiv und negativ bis zum Frontend bewiesen ist.
