# ÄNDERUNGS- UND ERKLÄRUNGSREGISTER

STAND: 2026-10-07

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


## HOBBYRAUSCH-HD001-20261005-E – V1.9.8 WordPress-Hierarchieübersetzung lokal bewiesen

WAS:
Die zuvor blockierte WordPress-Abbildung SEITE→SEITE→SEITE→KATEGORIE wurde lokal ohne neue Pluginlinie gelöst. Page-Hierarchie bleibt nativ. Für die technische Page→Taxonomy-Grenze wird ein interner Taxonomie-Bridge genutzt; sichtbare Leafs hängen nativ darunter und bleiben logisch an die Page-concept_id gebunden. Der Bridge selbst ist kein sichtbarer Navigationspunkt.

WARUM:
WordPress kann Page→Page und Term→Term nativ, aber keine Page als nativen Term-Parent. Der alte Pilot speicherte deshalb nur die logische Parent-Bindung und blieb im Frontend leer. Der Bridge verbindet beide nativen Hierarchien ohne falsche object_id und ohne die Fachhierarchie zu verändern.

REGEL:
- Bridge ist rein technisch und frontend-unsichtbar;
- sichtbare Leafs bleiben echte WordPress-Terme;
- Frontend-Ausgabe kommt aus der echten nativen Struktur;
- sichtbarer Frontend-Endzustand ist Teil des Writer-Readbacks;
- gleiche kurze Leaf-Namen sind nur bei verschiedenen Page-Kontexten, verschiedenen technischen Slugs und getrennten Intent-Ownern zulässig;
- gleicher Parent oder technische Slug-/Intent-Kollision bleibt BLOCKED;
- Magazin wird separat über hierarchisches journal_cat geführt;
- HivePress bleibt separat über hp_listing_category.

EVIDENZ:
270/270 lokale Suite PASS. Exakter Zielbaum Fertigen→Buch & Papier→Buchbinden sowie zweites Hobby Nähen geprüft. Zusätzlich echte HOBBY_DEPOT_BUCHBINDEN_READ_ONLY_PREVIEW_V1 lokal migriert: vier bestehende Content-Term-IDs unverändert erhalten, Frontend danach exakt vier Leafs sichtbar, keine Marketplace-/Magazin-/Bridge-Leaks.

OFFEN:
Der alte Concept Builder erzeugt weiterhin nur Root-Seite + max. 4 direkte Kinder. Kein Release vor vollständigem Builder-/DataForSEO-E2E-PASS.


## HOBBYRAUSCH-HD001-20261005-F – Full-Hierarchy Builder und kompletter lokaler E2E HARD PASS

WAS:
Der V1.9.8-Builder wurde auf den bereits bewiesenen WordPress-Zielvertrag erweitert. Der neue Full-Hierarchy-Weg unterstützt variable Page-Ebenen, evidenzbelegte Leaf-Kategorien, getrennte Magazin-/HivePress-Stränge und behält die inkrementelle Delta-Logik.

WARUM:
Der vorherige letzte Blocker war der alte Builder `Root-Seite + max. 4 direkte Kinder`. Dieser konnte den fertigen Fachvertrag `SEITE → SEITE → SEITE → KATEGORIE → BEITRÄGE` nicht automatisch erzeugen.

REGEL:
- Legacy-Weg bleibt regressionstabil;
- Full-Hierarchy-Weg darf 1–3 Page-Ebenen erzeugen;
- keine feste 4-Kinder-Grenze;
- nur evidenzbelegte Leafs;
- nicht belegte optionale Kategorien werden weggelassen;
- gemeinsame Strukturplanung, technisch getrennte Content-/Magazin-/HivePress-Zielstränge;
- bestehende Knoten werden bei Erweiterungen nicht automatisch gelöscht;
- Abnahme endet erst beim sichtbaren Frontend-Readback.

EVIDENZ:
270/270 Regression PASS; Full Builder PASS; Multi-Hobby/Flex PASS; kompletter Positiv-E2E PASS; kompletter Negativ-E2E PASS; Fresh-Unpack erneut PASS; Runtime-Parität 25/25; Installer PHP 19/19.

ARTEFAKTE:
Installer SHA-256 `60ea8d4c235805d66e6795223b1bfbd392cc0109556cfbf5631d9d0109b4585c`.
Source SHA-256 `340af0e4927971c746d97ba2aad8bab1e7efc269c70e12d21319734e7a363c10`.

GRENZE:
Noch kein V1.9.8-Live-PASS. Nächste Aktion ist ausschließlich Installation plus realer WordPress-/Frontend-Readback.


## HOBBYRAUSCH-HD001-20261005-G – Pferdeatelier-Taxonomie statt technischer Bridge

WAS:
Nach erneuter harter Prüfung der real funktionierenden Pferdeatelier-Struktur wurde das V1.9.8-Bridge-Modell verworfen. V1.9.9 bildet die WordPress-Übersetzung nach dem bewährten Pferdeatelier-Prinzip ab.

WARUM:
Im Pferdeatelier sind Level-4-Themenkategorien echte Root-Terms der WordPress-Taxonomie category (`parent_slug=""` / technisch parent=0). Ihre Zugehörigkeit zur Level-3-Seite wird über Produkt-/Kontextschlüssel und den Renderer hergestellt. V1.9.8 hatte fälschlich zusätzliche technische Bridge-Terme eingeführt.

REGEL:
- Level 1–3 = native WordPress-Seiten;
- Level 4 = echte Root-category-Terme;
- kein technischer Bridge;
- logische Seitenbindung bleibt stabil;
- Speichername/Slug müssen kontextuell eindeutig sein;
- sichtbares Frontend-Label darf kurz bleiben;
- Magazin und HivePress bleiben technisch getrennt;
- bestehende IDs dürfen bei Migration nicht unnötig ersetzt werden.

EVIDENZ:
270/270 Regression PASS; Full Builder PASS; echter Buchbinden-Altbestand PASS; kompletter Positiv-E2E PASS; kompletter Negativ-E2E PASS; Fresh-Unpack erneut PASS; Runtime-Parität 19/19; Installer PHP 19/19 PASS.

WICHTIG:
Der zuvor behauptete einzelne `full-e2e-positive.php`-PASS war nicht belastbar; standalone fiel er auch in der unveränderten alten V1.9.8-Quelle an der DataForSEO-Evidenzbindung durch. Dieser Scheintest wurde im V1.9.9-Abschlusslauf korrigiert und durch einen standalone grün laufenden Gesamt-E2E ersetzt.


## HOBBYRAUSCH-HD001-20261005-H – V1.10.0 portalweite Discovery statt Einzelhobby

WAS:
HD-001 wurde lokal auf einen portalweiten Discovery-/Builder-Weg erweitert. Die Maschine kann große Rohlisten gegen DataForSEO Overview prüfen, Synonyme/Core-Keywords gruppieren, canonical Seeds bilden, die acht Konzeptwelten anhand pro-Hobby Suggestions evidenzbasiert routen und Content/Magazin/HivePress in Concept-Batches weitergeben.

WARUM:
Buchbinden war nur technischer Pilot. Das eigentliche Ziel ist der vollständige Hobby-Depot-Kategorienbaum. Die sichtbaren Namen und Hierarchien dürfen nicht aus einer statischen Hobbyliste geraten werden, sondern müssen aus Konzeptleitplanken + DataForSEO-Evidenz entstehen.

REGEL:
- Rohkandidatenliste != Taxonomie;
- Konzept setzt Leitplanken;
- DataForSEO entscheidet Nachfrage, Synonyme, canonical Seeds, Weltzuordnung und unterstützte Unterintentionen;
- ambige Zuordnung bleibt BLOCKED;
- kein Publish in der Discovery;
- bereits erfasster realer HD-002-Gesamtbestand darf nicht durch eine neu erfundene Liste ersetzt werden.

EVIDENZ:
270/270 Regression PASS plus V1.10.0 Portal Discovery, World Routing, 8 Worlds E2E, Scale, Negative, Admin und Resume PASS. 844er Lauf ist nur Skalierungsbeweis.

OFFEN:
Realer HD-002-Gesamtbestand ist laut HD-002 Current erfasst, aber im verfügbaren Archiv derzeit nicht als vollständiger Export/Source gebunden. Echter Gesamtbaum daher noch nicht erzeugt.

## HOBBYRAUSCH-HD001-20261007-I – Hobby-Master V2 integriert Breite, Monetarisierung und Portalgrenze

WAS:
Das Hobby-Depot-Konzept wurde nach V1.12 um eine vorgeschaltete Größen-/Rollen- und Portfolioebene erweitert.

WARUM:
Der bisherige Bestand war wirtschaftlich zu stark auf Nischen ausgerichtet; gleichzeitig würde das bloße Hinzufügen aller bekannten Hobbys Navigation und SEO-Architektur explodieren lassen.

VERBINDLICHE REGEL:
- drei Säulen bleiben: CORE / EDITORIAL / DIRECTORY;
- acht Welten bleiben geschützt und bilden die oberste fachliche CORE-Ebene;
- `Hobbywelten` ist nur Übersicht/View, nicht Parent der acht Welten;
- große bekannte Hobbys dienen als wirtschaftliche Anker;
- mittlere Hobbys bilden das Rückgrat;
- Nischen bleiben als SEO-/Longtail-Stärke erhalten;
- diese Klassen sind Eigenschaften/Präsentationsrollen, keine Parallel-Taxonomie;
- großer interner Hobbybestand ist erlaubt, sichtbare Navigation bleibt klein;
- vor dem Zielbaum entscheidet der HOBBY_MASTER V2 über Scope, Identität/Alias, Größe, Content Capacity und Publikationsrolle;
- mögliche Rollen: ORIENTATION_UNIVERSE / HOBBY_HUB / EDITORIAL_TOPIC / ARTICLE_ONLY / FINDER_ONLY / OUT_OF_SCOPE;
- Leaf-Ziel 5–12 Beiträge, Hobby-Hub-Ziel 3–6 tragfähige Leafs;
- Monetarisierung beeinflusst CORE-Priorität, aber löscht keine validen Themen;
- DataForSEO liefert Keyword-/Nachfrage-/Longtail-Evidenz, bestimmt aber weder Hauptwelt noch Parent noch structural_role;
- alle drei Säulen, Hobbyfinder, Suche und kuratierte Views referenzieren dieselben kanonischen Identitäten;
- pro Primärintent genau ein SEO-Owner.

INTEGRATION:
Der vorhandene V1.12-Zielbaum bleibt technische Baseline. Er wird nicht komplett neu erfunden, sondern nach abgeschlossener Masterbewertung per Delta fortgeschrieben.

KORREKTUR:
Die V1.12-Beziehung `Hobbywelten → acht Welten` ist als fachliche Hierarchie verworfen. Im nächsten Zielbaum-Delta stehen die acht Welten auf CORE-Ebene 1.

BELEG:
`PROJEKTE/HOBBYRAUSCH/KONZEPT/HOBBY_GROESSEN_ROLLENMODELL_20261007.md`
`PROJEKTE/HOBBYRAUSCH/SEO_KATEGORIEN/HOBBY_MASTER_V2_INTEGRATION_20261007.md`
`PROJEKTE/HOBBYRAUSCH/SEO_KATEGORIEN/HOBBY_MASTER_V2_PILOT_20261007.md`


## HOBBYRAUSCH-HD001-20261007-J – Maschinenlesbarer V2-Bewertungsvertrag + kontrollierter Batch 001

WAS:
Die bislang nur konzeptionell beschriebenen V2-Gates wurden als eindeutiger maschinenlesbarer Bewertungsvertrag gebunden. Zusätzlich wurde ein reproduzierbarer 16er-Masterbatch definiert und ausgeführt sowie die 19er-Research-Queue über ein eigenes Intake-Gate getrennt.

WARUM:
Die frühere NEXT ACTION verlangte eine maschinelle Batch-Bewertung, obwohl Auswahl, Fail-closed-Verhalten, Rollenentscheidung und Research-Queue-Aufnahme noch nicht eindeutig genug definiert waren. Dadurch hätte ein Folgechat erneut Ermessensentscheidungen erfinden müssen.

REGEL:
- fehlende Evidenz = EVIDENCE_REQUIRED, niemals Schätzung;
- DIRECT/ASSISTED erzeugt keine Strukturrolle;
- Batch 001 wird deterministisch gewählt;
- Research Queue gehört nicht automatisch zu den 841 Master-Identitäten;
- neue Research-Identität erst nach Scope + Identitätsgate;
- nur ASSESSED darf später Zielbaum schreiben.

ERGEBNIS:
- Batch 001 = 16 Identitäten;
- 16/16 ID-Eindeutigkeit PASS;
- 4 aktuelle Alias-/Kanonikbindungen bestätigt;
- 12 semantische Identitäts-/Unterformprüfungen offen;
- 0 Zielbaum-Writes zulässig;
- Buchbinden bleibt HOBBY_HUB aus vorhandener Pilotevidenz;
- Treibholz sammeln bleibt EDITORIAL erhalten, Unterrolle noch evidenzabhängig;
- 19 Research-Kandidaten ohne aktuelle Namens-/Alias-Kollision;
- Fotografie als erstes provisorisches Master-Intake-Delta vorbereitet.

BELEG:
`PROJEKTE/HOBBYRAUSCH/SEO_KATEGORIEN/HOBBY_MASTER_V2_ASSESSMENT_RULES_20261007.json`
`PROJEKTE/HOBBYRAUSCH/SEO_KATEGORIEN/HOBBY_MASTER_V2_BATCH_001_RESULTS_20261007.json`
`PROJEKTE/HOBBYRAUSCH/SEO_KATEGORIEN/HOBBY_MASTER_V2_RESEARCH_INTAKE_20261007.json`
`PROJEKTE/HOBBYRAUSCH/SEO_KATEGORIEN/HOBBY_MASTER_V2_INTAKE_DELTA_001_20261007.json`


## HOBBYRAUSCH-HD001-20261007-K – V2 pro Leaf prüfen + kleine Themen zusammenfassen

WAS:
Das vollständige überarbeitete Hobby-Depot-Konzept wurde erneut gegen den aktuellen Arbeitsstand geprüft. Zwei Punkte wurden im maschinenlesbaren Bewertungsweg nachgezogen:
1. Content Capacity wird pro unterster Kategorie geprüft, nicht nur als Gesamtzahl eines Hobbys.
2. Kleine valide Hobbys dürfen gemeinsam dargestellt werden, ohne ihre kanonische Identität zu verlieren.

WARUM:
Das Konzept verlangt 5–12 eigenständige Beiträge pro unterster Kategorie. Außerdem sollen Nischen erhalten bleiben, ohne hunderte dünne Kategorien zu erzeugen.

REGEL:
- 0–3 distinct Artikelintents = keine eigene Leaf-Kategorie;
- 4 = Ausnahmeprüfung;
- 5–12 = Zielbereich;
- 13–15 = Split-Prüfung;
- 16+ = Split erforderlich;
- ein Hobby-Hub benötigt typischerweise 3–6 tragfähige Leafs;
- Synonyme/Formulierungsvarianten zählen nicht mehrfach;
- kleine valide Hobbys können über Übersichten, gemeinsame Leafs oder redaktionelle Cluster zusammen sichtbar werden;
- hobby_id/Identität bleibt dabei getrennt;
- DataForSEO validiert Nachfrage/Intenttiefe, erzeugt aber keine Struktur.

KORREKTUR ZU VORGANG J:
Die Aussage „Buchbinden bleibt HOBBY_HUB“ war als bestehende Baseline richtig, aber als neuer V2-PASS zu stark.
Vorhandene reale DataForSEO-Evidence belegt aktuell:
Einstieg 4 / Ausrüstung 5 / Material 3 / Techniken-Praxis 4 distinct Gruppen.
Damit bleibt der bestehende Pilot erhalten, der endgültige V2-Hub-PASS ist aber offen.

BELEG:
`PROJEKTE/HOBBYRAUSCH/SEO_KATEGORIEN/HOBBY_MASTER_V2_CONCEPT_AUDIT_20261007.md`
`PROJEKTE/HOBBYRAUSCH/SEO_KATEGORIEN/HOBBY_MASTER_V2_ASSESSMENT_RULES_20261007.json`
`PROJEKTE/HOBBYRAUSCH/SEO_KATEGORIEN/HOBBY_MASTER_V2_BATCH_001_SUBJECT_PREFLIGHT_20261007.json`
`PROJEKTE/HOBBYRAUSCH/SEO_KATEGORIEN/HOBBY_MASTER_V2_BATCH_001_DATAFORSEO_REQUEST_20261007.json`

NÄCHSTER FACHLICHER SCHRITT:
Den vorbereiteten Batch-001-DataForSEO-Request real ausführen und danach Leaf-Zählung, Ownership und Aggregation neu berechnen.


## HOBBYRAUSCH-HD001-20261007-L – Konzeptgrenzen exakt korrigiert + V1.12.1 WordPress-Bewertung

WAS:
Die komplette V2-Umsetzung wurde erneut gegen den ursprünglichen Konzepttext geprüft. Dabei wurde die in Vorgang K zu streng formulierte Split-Regel korrigiert und der V2-Bewertungslauf direkt in HD-001/WordPress umgesetzt.

WARUM:
Das Konzept sagt nicht `13–15 zwingend splitten / 16+ splitten`.
Es sagt: unter 4 zusammenlegen, ideal etwa 5–12, ab etwa 15 prüfen, ob eine echte Teilung sinnvoll ist.
Eine automatische Teilung hätte wieder Struktur erfunden.

VERBINDLICH:
- unter 4 = zusammenlegen / keine eigene Leaf-Kategorie;
- 4 = Grenzfall;
- 5–12 = ideal;
- 13–14 = oberhalb ideal, keine automatische Teilung;
- ab etwa 15 = Teilung prüfen, nur bei echter fachlicher Trennlinie;
- Hobby-Hub typischerweise 3–6 Leafs;
- 7–9 = oberhalb typisch, prüfen;
- ab etwa 10 eigenständigen Unterbereichen = Macro-/Split-Prüfung.

TECHNISCHE UMSETZUNG:
HD-001 V1.12.1 führt Batch 001 read-only im WordPress-Backend aus und benutzt den vorhandenen DataForSEO-Zugang.
Der alte V1.12-Zielbaum darf dabei nicht geschrieben werden.

BELEG:
- Artefakt SHA-256 `959bc80217aac9b90ac107e6b315908b084704d09777ae9be990c2825245d33d`;
- Prüfbericht SHA-256 `3f34f58d0d7d35d0ac290e2926ac706f5fd6ff84e5a314d6ecde554204c89ac2`;
- PHP 59/59;
- Legacy 270/270;
- V1.12 POS/NEG;
- realer 908/844/841-Test;
- V1.12.1 V2-Grenz-/Negativtests;
- 0 Strukturwrites.

OFFEN:
Nur der reale Batch-001-DataForSEO-Lauf in Hobby Depot.


## HOBBYRAUSCH-HD001-20261007-M – Reales Batch-001-Ergebnis ausgewertet / fehlende DataForSEO-Tiefenstufe geschlossen

WAS:
Der echte V1.12.1-WordPress/DataForSEO-Lauf wurde ausgewertet.
263 exakte Artikel-Seeds wurden angefragt, DataForSEO lieferte 106 Overview-Zeilen zurück; 157 blieben offen.

WARUM:
Der Zwischenbefund `0 Hub-Kandidaten` war dadurch nicht belastbar.
Regelvertrag 1.2 verlangt nach der fachlichen Leaf-/Artikelkandidatenbildung zusätzliche Suggestions/Ideas zur Tiefenprüfung.
V1.12.1 hatte diese zweite Stufe noch nicht umgesetzt.

KORREKTUR:
HD-001 V1.12.2:
- verwendet das vorhandene Resultat weiter;
- 37 offene fachlich definierte Cluster;
- 37 Keyword Ideas;
- 1 finaler Overview;
- 38 zusätzliche Calls;
- max. 15 distinct Intentgruppen je Cluster;
- erneute Dedupe/Ownership;
- 0 Strukturwrites.

WICHTIG:
Die 157 fehlenden exakten Overview-Zeilen werden weder positiv noch negativ erfunden.
DataForSEO bleibt Evidenz und erzeugt keine Taxonomie.

BELEG:
`PROJEKTE/HOBBYRAUSCH/SEO_KATEGORIEN/HOBBY_MASTER_V2_BATCH_001_REAL_RESULT_20261007.md`
`PROJEKTE/HOBBYRAUSCH/SEO_KATEGORIEN/HOBBY_MASTER_V2_BATCH_001_DEPTH_PLAN_20261007.json`

ARTEFAKT:
`HD001_V1.12.2_V2_DATAFORSEO_DEPTH_READONLY_HARDPASS.zip`
SHA-256 `233f3b5a71f6080d98e8748795cedb0b684c5e1a16407ec509919fa3d1f7e17f`.

OFFEN:
Nur der reale 38-Call-Tiefenlauf in Hobby Depot.


## HOBBYRAUSCH-HD001-20261007-N – DataForSEO-Rohzeilen sind Evidenz, keine neuen Artikel

WAS:
Nach dem realen V1.12.3-Lauf wurde die Zähllogik korrigiert.

WARUM:
Fachfremde Keyword-Ideas-Treffer wurden als zusätzliche Artikel gezählt. Das widersprach der V2-Regel, dass Fachlogik die Artikelintents vorgibt und DataForSEO nur validiert/dedupliziert.

VERBINDLICH:
Provider-Rohzeilen erhöhen niemals selbst die Artikelanzahl.
Sie dürfen nur einen bereits vorhandenen fachlich definierten Artikelintent bestätigen oder mit anderen per Core-Keyword zusammenführen.

UMSETZUNG:
HD-001 V1.12.4, automatische Zero-Cost-Neuauswertung des gespeicherten V1.12.3-Ergebnisses.

OFFEN:
Nur reale Neuauswertung in Hobby Depot; keine weitere DataForSEO-Recherche.


## HOBBYRAUSCH-HD001-20261007-O – Root Cause geschlossen: Content Capacity ≠ Provider-Zeilen

WAS:
Die gesamte Batch-001-Fehlerkette wurde gegen Konzept und echtes V1.12.3-Ergebnis erneut durchgeprüft.

ROOT CAUSE:
Die fachliche Frage „Wie viele eigenständige Beiträge trägt die unterste Kategorie?“ war schrittweise mit DataForSEO-Zeilen verwechselt worden.

VERBINDLICHE KISS-REGEL:
- Fachlogik zählt eigenständige Artikelintents.
- DataForSEO prüft Nachfrage, Synonyme, Core Keywords und Intent-Überschneidung.
- DataForSEO darf fachliche Dubletten zusammenführen.
- Fehlende exakte Longtail-Zeile entfernt keinen fachlich eigenständigen Intent.
- Provider-Rohzeilen erzeugen keine neuen Artikel.
- automatische Keyword-Ideas-Tiefenrecherche ist im Normalweg nicht erforderlich.

UMSETZUNG:
Regelvertrag 1.4 + HD-001 V1.12.5.

BELEG:
`PROJEKTE/HOBBYRAUSCH/SEO_KATEGORIEN/HOBBY_MASTER_V2_BATCH_001_V125_KISS_REPLAY_20261007.md`

ERGEBNIS:
Der echte gespeicherte Batch wurde ohne neue Calls/Kosten/Writes lokal bis zum Endergebnis neu gerechnet und hart getestet.

OFFEN:
Nur noch ein einmaliger realer WordPress-Readback desselben V1.12.5-Endstands.


## HOBBYRAUSCH-HD001-20261007-P – stale Export als letzter technischer Restfehler geschlossen

WAS:
Der reale nach V1.12.5 heruntergeladene JSON-Readback war nachweislich weiterhin das alte V1.12.3-Ergebnis.

WARUM:
Die KISS-Neuberechnung hing am Rendern der Bewertungsseite. Der Download selbst war nicht fail-closed.

ÄNDERUNG:
HD-001 V1.12.6 macht den Download zum finalen Recalc-Gate:
Altstand wird vor Export kostenlos neu berechnet und gespeichert; bei Fehler wird blockiert.

NICHT GEÄNDERT:
Regeln 1.4, DataForSEO-Fachrolle, Zielbaum, Taxonomie, WordPress-/HivePress-Struktur.

BELEG:
`PROJEKTE/HOBBYRAUSCH/SEO_KATEGORIEN/HOBBY_MASTER_V2_BATCH_001_V126_STALE_EXPORT_READBACK_20261007.md`

NEXT:
Einmal real mit V1.12.6 exportieren und JSON readback-prüfen.

## HOBBYRAUSCH-HD001-20261008-Q – Produktionsweg auf einen praktischen Final-Sync reduziert

WAS:
Die manuelle 16er-Batchschleife endet nach Batch 003. HD-001 V1.13.1 führt den finalen Zielbaum als einen manual-only Dry-Run-/Sync-Weg zusammen.

URSACHE:
Der 841er Master wurde im Zwischenweg fälschlich wie 841 einzeln zu beweisende CORE-Strukturobjekte behandelt. Gleichzeitig enthielt der erste praktische Zielentwurf noch die alte falsche Parent-Beziehung Hobbywelten → acht Welten.

KORREKTUR:
- Master = Inventar;
- 340 CORE / 501 Finder-Editorial;
- acht Welten physisch Root;
- Hobbywelten nur View;
- 431 physische Zielobjekte;
- keine weitere DataForSEO-Batchserie;
- genau ein realer Delta-Dry-Run;
- danach bei PASS ein kontrollierter Sync.

BELEG:
`PROJEKTE/HOBBYRAUSCH/SEO_KATEGORIEN/HOBBY_MASTER_V2_PRACTICAL_FINAL_TARGET_AUDIT_20261008.json`

NÄCHSTER SCHRITT:
V1.13.1 real installieren und nur den read-only finalen Delta-Dry-Run ausführen.
