# BAUCONTAINER – BAUPROTOKOLL

STAND: 2026-09-16

## Zweck

Chronologisches Arbeitsprotokoll für den Campus selbst.

Die ausführliche dauerhafte Begründung liegt im `AENDERUNGSREGISTER.md`.

## Pflichtregel

Jeder Chat, der Architektur verändert, protokolliert:
- konkreten Bedarf;
- kleinste Änderung;
- betroffene Architekturakten;
- ARCH-/BAU-Fehler-Bezug;
- Prüfstand.

## Bisherige Bauereignisse

### 2026-09-05 – Campus-Prototyp
Campus → Projektgebäude → Büro → Hobbyraum.
BEZUG: ARCH-001 bis ARCH-006.
PR: #134.

### 2026-09-05 – Organischer Ausbau
BILD, allgemeingültige Bausteine, Modulregister, Masterdateien-Regel.
BEZUG: ARCH-008 bis ARCH-014.

### 2026-09-05 – Zielverträge und Archiv
Zielvertragsraum + Campus-Archiv-Eingang.
BEZUG: ARCH-015 bis ARCH-017.

### 2026-09-05 – Architektur-Selbstpflege
Architektur-Sonderrecht, Bauprotokoll, Architektur-Fehlerkiste, Hausmeister.
BEZUG: ARCH-018 bis ARCH-020.

### 2026-09-05 – Verwaltungsrollen hart getrennt + 1-Klick-Eingänge
BEDARF:
Pförtner/Hausmeister dürfen Inhalte nicht anfassen. Neue Chats müssen an jeder Ebene sofort verstehen, wo sie sind und was gilt.

ERGEBNIS:
- Pförtner = READ/ROUTE ONLY;
- Hausmeister = ORDNEN/VERSCHIEBEN OHNE INHALTSÄNDERUNG;
- `EINGANGSSTANDARD.md`;
- Campus-, Projekt-, Büro- und Paul-Eingänge auf 1-KLICK-ÜBERSICHT vereinheitlicht;
- neue Projektvorlage erzwingt denselben Standard.

BEZUG:
ARCH-021, ARCH-022.

### 2026-09-05 – Entwicklungsprotokoll ergänzt

BEDARF:
Auch der konzeptionelle Austausch und verworfene/offene Architekturgedanken sollen nicht im Chat verloren gehen.

ERGEBNIS:
`ENTWICKLUNGSPROTOKOLL.md` ergänzt.

TRENNUNG:
- Entwicklungsgespräch → ENTWICKLUNGSPROTOKOLL
- tatsächlich gebaut → BAUPROTOKOLL
- dauerhaft gültig + WHY → AENDERUNGSREGISTER

BEZUG:
ARCH-023.

### 2026-09-05 – WordPress-Register

BEDARF:
Zentrale Antwort auf „Welche WordPress-Plugins haben wir bereits?“, ohne ein neues WordPress-Büro oder eine zweite Modulwahrheit zu bauen.

KRITISCHE ENTSCHEIDUNG:
Kein WordPress-Gebäude/Büro. Ein einziges campusweites Technologie-Register reicht aktuell.

ERGEBNIS:
`WORDPRESS_REGISTER.md` mit nachweisbar erhaltenen Plugin-/Installer-Artefakten angelegt.

GRENZE:
Modulklasse bleibt im MODULREGISTER; LIVE-/Release-Status bleibt an der Fach-/Technikquelle.

BEZUG:
ARCH-024.

### 2026-09-05 – Kategoriemodul vollständig eingeordnet + Archiv-Ampel

BEDARF:
Aktuellen allgemeingültigen Kategorieplugin-Bestand vollständig zuordnen und klären, wann lokale Originale entbehrlich werden.

ERGEBNIS:
- MOD-001 auf Master R10/R9 / Plugin V1.8.0 aktualisiert;
- WordPress-Pluginstatus belegt;
- R2/R3 historisch, R10 Hauptakte;
- Pferde-Atelier-Kategoriereparatur separat gehalten;
- persistente Library-Archivkopien erzeugt;
- Archiv-Ampel ROT/GELB/GRÜN eingeführt.

BEZUG:
ARCH-025.

### 2026-09-05 – Design allgemein + Pferde zusammengeführt

BEDARF:
Zwei allgemeine Design-Dateien und zwei Pferde-Dateien mit aktuellem GitHub-System zusammenführen.

ERGEBNIS:
- MOD-003 Universal Design 2.2.40/V104 angelegt;
- Universal-Master 298/298 geprüft;
- Pferde-Master 1.50.469 792/792 geprüft;
- Pferde-Dubletten erkannt;
- Roharchive getrennt persistiert;
- GitHub main 1.50.421 als älteren Main-Stand erkannt;
- spätere Design-Fachbranches bis 1.50.472 geprüft;
- 1.50.472/V104 als aktuellen Pferde-LIVE-Stand gebunden;
- Universal 2.2.40/V104 durch spätere GitHub-Historie als unverändert aktuell bestätigt;
- enthaltene HivePress-Anzeigensuche als MOD-004 UNGEKLÄRT separat erfasst.

BEZUG:
ARCH-026.

### 2026-09-05 – Campus-Eingänge + Paul TEXT/SEO + Tresorstatus geschlossen

BEDARF:
Alltagssprache soll als Campus-Routing funktionieren; Archiv/Zielverträge/Baucontainer/Tresor brauchen vollständige 1-Klick-Eingänge; Paul muss TEXT/SEO ohne Kontextverlust finden.

ERGEBNIS:
- Campus-`START_HERE.md`;
- natürliche Sprache als Routingauftrag gebunden;
- Archiv/Zielverträge/Baucontainer/Tresor mit 1-Klick-Eingang;
- sechs aktuelle TEXT-/SEO-Originalakten wortgleich unter `TEXT/QUELLEN_AKTUELL/`;
- aktiver TEXT-Zielvertrag im zentralen Register;
- Paul-Direkteinstieg `PAUL/TEXT_SEO/START_HERE.md`;
- Tresorstatus explizit FAIL statt erfundenem PASS.

BEZUG:
ARCH-027 bis ARCH-030; BAU-006 bis BAU-009.

### 2026-09-05 – Externer Tresor-Git-Mirror V2 erzeugt und Restore-getestet

BEDARF:
Der Tresor durfte nicht nur Konzept sein; Git-Historie/Branches/Tags und GitHub-Metadaten mussten außerhalb des aktiven Repositorys gesichert werden.

ERGEBNIS:
- isolierter Tresor-Branch;
- vollständiger Git-Bundle-Mirror;
- 261 Branches / 1 Tag;
- vollständige paginierte GitHub-Metadaten: 136 Issues, 127 PRs, 1 Release, 1 Ruleset, 59 Workflows;
- Ruleset-Detail separat gesichert;
- Restore-Test + git fsck PASS;
- V2-Artefakt extern in ChatGPT Library gesichert.

STATUS:
Kein vollständiger TRESOR_PASS.
Nächster Blocker: nicht exportierbare Recovery-Abhängigkeiten noch nicht verifiziert.

BEZUG:
ARCH-031.

### 2026-09-05 – Kritische Bauabnahme: erste Mängel direkt geschlossen

BEFUNDE:
- TEXT-/HIVEPRESS-Eingang führte nicht vollständig über CURRENT_STATE → HOBBYRAUM;
- TEXT-Eingang/Hobbyraum waren an den alten Sortierchat gebunden und kollidierten mit Pauls Fachauftrag;
- BILD-Hobbyraum war nach abgeschlossenem Abgleich noch als AKTIV markiert;
- Pferde-Gebäudeeingang enthielt veralteten Parallelchat-Hinweis;
- Paul-TEXT/SEO nutzte fünf abgekürzte `.../`-Pfade;
- zentrale Tresor-/Bild-Metadaten enthielten veraltete Statushinweise;
- Hobbyraum-Kennwort/Zustände waren nicht zentral definiert.

KISS-FIX:
Nur Navigations-/Status-/Architekturmetadaten an bestehenden Adressen korrigiert.
Keine Fachdatei und keine Fachlogik verändert.

ADRESSGARANTIE:
Alle bereits verteilten Campus-/Büro-/Paul-Einstiege bleiben unverändert erreichbar.

BEZUG:
ARCH-032 bis ARCH-034; BAU-010 bis BAU-013.

### 2026-09-05 – Bauabnahme: Büro-Leitungen + Hobbyraum-Direkteinstieg

BEFUND:
Direkter Büro-/Hobbyraumeinstieg war weniger vollständig als der Weg über den Hauptpförtner.

KISS-FIX:
- alle sechs Pferde-Büros mit sichtbarer Arbeitsfreigabe zu Handlungs-/Fehler-/Änderungs-/Zielregistern;
- alle sechs Hobbyräume mit 1-Klick-Eingang;
- Gebäudebüroplan auf echte START_HERE-Pfade präzisiert.

BEZUG:
ARCH-035/036; BAU-014/015.

### 2026-09-05 – Bauabnahme: Flur/ungeklärter Bestand/Tresor-Reihenfolge

BEFUNDE:
- Projektflur ohne START_HERE;
- Affiliate-Bestandsraum unter allgemeingültiger Ablage ohne sichtbare UNGEKLÄRT-Warnung;
- Tresorstatus übersprang die fehlende unabhängige Roharchiv-Redundanz.

KISS-FIX:
- Projektflur-Eingang ergänzt;
- Affiliate-Bestandsraum selbsterklärend gemacht, ohne Modulfreigabe;
- MOD-004-Registerpflichtfelder vervollständigt, ohne eigenen Modulraum vor Audit;
- Tresor auf ersten realen Blocker zurückgesetzt.

BEZUG:
ARCH-037 bis ARCH-039; BAU-016 bis BAU-018.

### 2026-09-05 – Formale Bauabnahme nach Reparaturen

POSITIV:
- 22/22 PROJECT_MEMORY-Verzeichnisse besitzen START_HERE;
- 22/22 START_HERE-Eingänge erfüllen 1-Klick-Standard;
- 6/6 Pferde-Büros besitzen START_HERE + CURRENT_STATE + genau einen HOBBYRAUM;
- 6/6 Hobbyräume besitzen 1-Klick-Übersicht und gültigen Status;
- 6/6 Büros führen bei echter Arbeit über Handlungs-/Fehler-/Änderungs-/Zielregister;
- Pförtner READ/ROUTE ONLY;
- Hausmeister reine Verwaltung;
- Paul-Pfade vollständig, keine Ellipsen;
- bestehende Adressen unverändert;
- Campus-Hardlocks auf den vorausgehenden Abnahmeständen PASS.

NEGATIV / BEWUSST OFFEN:
- BAU-003: Campus-Prototyp noch im öffentlichen Pferde-Atelier-Repo/Branch;
- TRESOR: kein vollständiger PASS, erster Blocker fehlende unabhängige Roharchiv-Redundanz;
- danach weiterhin Recovery-Abhängigkeiten/Secrets zu prüfen;
- Archivbestände mit ROT/GELB bleiben lokal nicht entbehrlich.

GESAMT:
Architektur/Navigations-/Rollenabnahme PASS.
Vollständiger Sicherheits-/Katastrophen-PASS BLOCKED.

### 2026-09-05 – Bauabnahme: Neubauvorlage gegen aktuellen Standard gehärtet

BEFUND:
Die bestehende Projektvorlage kannte den ursprünglichen 1-Klick-Standard, aber noch nicht alle späteren Regeln aus ARCH-032 bis ARCH-040.

KISS-FIX:
Vorlage ergänzt um:
- START_HERE für jedes neue Verzeichnis;
- stabile Adressen;
- zentrale Büro-Leitungen;
- Hobbyraum-Standard;
- Positiv-/Negativ-Abnahme.

BEZUG:
ARCH-041 / BAU-020.

### 2026-09-16 – TECHNIK-Büro für WordPress-Betrieb / Speicher / Backups

BEDARF:
Die reale Speicher-/Backupdiagnose des Pferde-Ateliers braucht eine dauerhafte eigene Betriebswahrheit. Das campusweite `WORDPRESS_REGISTER.md` ist nur Technologieindex und darf keinen dynamischen Technikstatus übernehmen.

KLEINSTE ÄNDERUNG:
- neues Büro `PROJEKTE/PFERDE_ATELIER/TECHNIK/` mit Bürotür, CURRENT_STATE, genau einem HOBBYRAUM, Regelwerk, Handlungsverzeichnis und Updateprotokoll;
- bestehende Campus-/Hauptpförtner-/Gebäude-/Handlungswegweiser um TECHNIK ergänzt;
- PLUGINS bleibt getrenntes Inventar-/Artefaktpult;
- `PPA-014` dort nur als Plugin referenziert/synchronisiert.

BETROFFENE ARCHITEKTURAKTEN:
`START_HERE.md`, `HAUPTPFOERTNER.md`, `HANDLUNGSVERZEICHNIS.md`, `PROJEKTE/PFERDE_ATELIER/START_HERE.md`, `WORDPRESS_REGISTER.md`, `AENDERUNGSREGISTER.md`, dieses Bauprotokoll.

BEZUG:
ARCH-044 / BAU-021.

PRÜFSTAND:
- Bürotür enthält 1-Klick-Übersicht und nur Navigation;
- CURRENT_STATE führt die einzige aktuelle Technikstandwahrheit;
- HOBBYRAUM enthält Status BLOCKED + eindeutige NEXT ACTION;
- Pluginartefakt PPA-014 persistent mit Manifest/Testnachweis und Hash-Readback vorhanden;
- lokale Plugin-Positiv-/Negativprüfung PASS;
- WordPress-LIVE-Retest ausdrücklich offen, daher kein erfundener LIVE-PASS.

### 2026-09-18 – Campusweite Ein-Wahrheit-Migration

BEDARF:
Ein neuer Chat darf nicht erneut stundenlang den Stand des Vorgängerchats rekonstruieren, obwohl eine Übergabe existiert. Gleichzeitig darf keine zusätzliche Handoff-/Current-Datei eine zweite Wahrheit erzeugen.

KISS-FIX:
- `AUTORITAETSPLAN.json` als reine Routingautorität angelegt;
- `EINE_WAHRHEIT_STANDARD.md` campusweit gebunden;
- Current-Autoritäten führen jetzt selbst die eine NEXT ACTION;
- Hobbyräume als `DERIVED_EXECUTION_SURFACE_V1` gekennzeichnet;
- Pferde-Atelier-Bürotüren, PB-ONE-Arbeitsräume und registrierte allgemeingültige Module migriert;
- Pferde-Atelier AFFILIATE auf die bereits technisch autoritative `control/release-governance/CURRENT_RELEASE.json` geroutet; alte Campus-Current nur noch Pointer;
- Neubauvorlage und Handlungsverzeichnis nachgezogen;
- maschinenlesbarer `single_truth_guard.py` ergänzt.

NEGATIVPRÜFUNG:
- 18/18 registrierte START_HERE-Pfade besitzen den Single-Truth-Marker und keine alte CURRENT→HOBBY-NEXT-ACTION-Kette;
- 17/17 eindeutige Current-Autoritäten besitzen eine direkte NEXT ACTION bzw. maschinenlesbare `authorized_next_action`;
- 15/15 registrierte Ausführungsflächen besitzen `DERIVED_EXECUTION_SURFACE_V1` und beanspruchen nicht mehr exklusiv die aktuelle NEXT-ACTION-Autorität.

GRENZE:
Maschinenlocks in Hobbyräumen bleiben als abgeleitete, hashgebundene technische Sperren erhalten. Sie sind keine Current-Wahrheit.

BEZUG:
ARCH-089 / BAU-042.



### 2026-09-18 – Hobbyraum temporär klargestellt

KISS-FIX:
Keine Architekturänderung. Nur die bestehende Hobbyraum-Regel präzisiert: Hobbyraum wird ausschließlich während einer konkreten Arbeit genutzt; dauerhafte Wahrheit bleibt in Current-/Protokoll-/Fachquellen.

BEZUG:
ARCH-090.


### 2026-09-25 – Projektgebäude HOBBYRAUSCH neu angelegt

BEDARF:
Hobbyrausch startet vollständig bei null und soll dieselben Ordnungs- und Sicherheitsprinzipien des Campus nutzen, ohne Pferde-Atelier-Bestand zu kopieren.

KISS-FIX:
- neues Gebäude `PROJEKTE/HOBBYRAUSCH/`;
- 14 leere Fachbüros mit START_HERE + genau einer CURRENT_STATE + genau einem Hobbyraum;
- zentraler Hauptpförtner und Projektflur um Hobbyrausch ergänzt;
- Autoritätsplan um Hobbyrausch-Scopes ergänzt;
- Hausmeister, Archiv und Tresor bleiben unverändert campusweit zentral;
- Pluginbüro mit `PLUGIN_AKTEN/<PLUGIN-ID>/CURRENT.md` als Einzelwahrheit und separater `ORIGINAL/`-Ablage vorbereitet.

NEGATIVPRÜFUNG:
- keine Pferde-Atelier-Fachinhalte übernommen;
- keine zweite Tresor-/Archiv-/Hausmeister-Struktur erzeugt;
- keine Plugin-Current-Wahrheit im Register oder in ORIGINAL abgelegt;
- keine bestehenden Pferde-Atelier-Scopes geändert.

BEZUG:
ARCH-091.


### 2026-09-28 – LANDINGPAGES-Büro Pferde-Atelier

BEDARF:
Vergleichs-/Rechnerseiten sollen sichtbar in bestehende Themenkacheln integrierbar sein, intern aber nicht als Produktionskategorien oder Journalartikel geführt werden.

KISS-FIX:
- neues Büro `PROJEKTE/PFERDE_ATELIER/LANDINGPAGES/`;
- genau eine Current-Autorität im Autoritätsplan;
- dauerhafter Konzeptmaster getrennt vom dynamischen Current;
- erster Pilot ausschließlich `Pferdehaftpflicht vergleichen`;
- technische Source-Änderungen bleiben in DESIGN/AFFILIATE und werden vom Landingpage-Büro nicht selbst ausgeführt.

NEGATIVPRÜFUNG:
- keine neue Kategorie erzeugt;
- keine Kategorienwahrheit verändert;
- keine Affiliate-/Design-Source verändert;
- keine zweite technische Autorität angelegt.

BEZUG:
ARCH-093.


### 2026-10-13 – HAB UND BEWAHR Bürotür/Current-Routing berichtigt

BEDARF: Die Projekt-Bürotür sagte noch, die KONZEPT-Current sei nicht unabhängig verifiziert; der zentrale Autoritätsplan routet seitdem jedoch belegbar genau eine existierende Konzept-Current. Der Hobbyraum zeigte einen älteren R3-Datenpfad. Das erzeugte unnötige Rekonstruktions- und Zwei-Wahrheiten-Risiken bei der nächsten Chatübergabe.

KISS-KORREKTUR:
- `PROJEKTE/EIGENTUMSSCHUTZ/START_HERE.md` verweist ohne widersprüchlichen Vorbehalt auf `AUTORITAETSPLAN.json` → `KONZEPT/CURRENT_STATE.md`.
- `PROJEKTE/EIGENTUMSSCHUTZ/KONZEPT/HOBBYRAUM.md` bindet künftig Arbeitsdaten ausschließlich über die gerade aktuelle Current; keine zweite aktuelle Version/Blocker/NEXT ACTION.
- Existierendes Campus-Routing und Fach-/Plugin-/WordPressarchitektur bleiben unverändert.
- Verbindliche 3–10-Regel in eigener Zielvertragsakte und Zielregister, dauerhaftes WAS/WARUM in `AENDERUNGSREGISTER.md` festgehalten.

NEGATIVREGEL: Weder Bürotür noch Zielvertrag/Hobbyraum dürfen den dynamischen V8-Status, aktuellen SEO-Blocker oder die eine NEXT ACTION parallel zur Current führen. Keine R3-Synchronisierung, kein neues Plugin, keine WordPress-Schreibarbeit.



## HAB-KAT-ZENTRAL-20261014 – Büro Kategorien (14.10.2026)
Anlass: ausdrücklich verlangte zentrale Kategorienverwaltung für alle Plugins; Änderungen ohne Umbau.
KISS-Eingriff: neues eigenständiges Kategorienbüro samt einer Current-Autorität, neutralem Anschlussvertrag und Register; Routing/Gebäudeeingang sowie fachlicher Verweis im Konzept angepasst. WordPress-Kategorien, Zielprofil, URLs, Plugins, Design und produktiver Sync unverändert.
Negativgrenze: Dokumentierter Zielvertrag ist kein Beleg einer bereits vorhandenen/abgenommenen neutralen PHP-API oder CRUD-End-to-End-Tests. Sicherer Änderungsweg bleibt Delta → Dry-Run → genau ein Sync → Readback.
Autorität: `PROJEKTE/EIGENTUMSSCHUTZ/KATEGORIEN/CURRENT_STATE.md`.


### 2026-10-16 – Textsystem-Keller, K0-Aktivroute und Gebäudetrennung

BEDARF:
Historische Textsysteme und alte Querverweise erzeugten bei neuer Arbeit unnötige Fehlwege. Gleichzeitig müssen Pferdeatelier, Hobby Depot und Hab & Bewahr fachlich getrennt bleiben.

KISS-FIX:
- Pferdeatelier TEXT auf genau eine aktive Produktionsbasis K0 geroutet;
- K1 bis K9 aus der aktiven Campus-Textfläche entfernt und ausschließlich als Archiv-/Recherchebestand gebunden;
- TEXTSYSTEM_4A als aktive Bürotür entfernt;
- Projektflur, Campus-Eingang und Hauptpförtner auf klare Gebäudetrennung nachgezogen;
- Affiliate-Current explizit an Branch `affiliate-release-current` gebunden, damit keine veraltete Main-Kopie als Current gelesen wird;
- keine Fachlogik, Pluginquelle oder WordPress-Installation geändert.

SICHERUNG:
Vor Umbau existieren GitHub-Snapshotbranches für Main, Campus, K0 und K9 sowie ein frisches vollständiges lokales GitHub-Backup des Nutzers.

PRÜFUNG:
- Pferdeatelier TEXT aktiv nur noch drei Navigationsdateien;
- keine aktive TEXTSYSTEM_4A-Route;
- zentrale Text-Current zeigt ausschließlich auf K0;
- geprüfte aktive Routingdateien enthalten keinen STARTMASTER-/System4-/K7-/K8-Currentverweis;
- andere Projektgebäude fachlich unverändert.

BEZUG:
ARCH-094 / HM-005.


### Main-Hardlock-Grenze 2026-10-16

PRÜFUNG:
Das aktive GitHub-Ruleset `Pferde Atelier Main Hardlock` verlangt auf dem Default-Branch die Statuschecks `hardlock` und `hardlock-base`. Der vertrauenswürdige `hardlock-base` sperrt Änderungen an den alten Workflow-/Control-Sicherheitsdateien ausdrücklich.

FOLGE:
Der alte technische K1–K8-Unterbau auf `main` wird **nicht blind physisch entfernt**, solange diese Schutzschicht darauf gebunden ist. Ein Test-Cleanup wurde nicht auf `main` übernommen und der temporäre Cleanup-Branch wieder auf `main` zurückgesetzt.

SICHERE LÖSUNG:
Aktive Campus- und Textnavigation ignoriert diesen Legacy-Unterbau vollständig und routet ausschließlich auf K0. Der alte Main-Bestand bleibt bis zu einer separat beweisbaren Hardlock-Migration nur technischer Legacy-/Schutzbestand, nicht Current oder Fallback.


### 2026-10-17 – BAU-043: Repository-/Branch-Cleanup an eine Current-Autorität gebunden

BEDARF:
Der Branch-Cleanup hatte trotz campusweiter Ein-Wahrheit-Regel keinen eigenen Scope und keine Current-Autorität.

KISS-FIX:
- genau einen Scope `CAMPUS_REPOSITORY_CLEANUP` im bestehenden `AUTORITAETSPLAN.json` ergänzt;
- genau eine Current-Autorität `protocol/PROJECT_MEMORY/REPOSITORY_CLEANUP_CURRENT_STATE.md` angelegt;
- bestehende Campus-START_HERE-Tür als Einstieg weiterverwendet;
- kein neues Büro, kein neuer Runner, keine Fachlogik und keine Änderung an K0/Affiliate/Plugins.

NEGATIVPRÜFUNG:
Hausmeisterprotokoll, Archivcheckpoint und ACTIVE_BRANCHES bleiben Nachweis/Registry und wurden nicht zu Current-Autoritäten gemacht. PR #518 und Main-Hardlock-Legacy bleiben geschützt.

BEZUG:
ARCH-095 / BAU-043 / HM-007.

### 2026-10-21 – Pinterest-Büros

BEDARF: Pinterest für drei eigenständige Marken, ohne dreifachen Automatikbau oder neues Zentralgebäude.

KLEINSTE ÄNDERUNG: Drei projektlokale PINTEREST-Büros (je START_HERE, CURRENT_STATE, HOBBYRAUM, KONZEPT); AUTORITAETSPLAN, drei Gebäudeeingänge und AENDERUNGSREGISTER angepasst.

BEZUG: BAU-001 Ein-Wahrheit-Prinzip; BAU-003: keine Zugangsdaten im öffentlichen Campus.

PRÜFUNG: Eigenständige Current pro Büro, keine Fremdbüroänderung in Fach-/Plugin-Systemen, keine Online-Veröffentlichung und keine aktive Linkprüfung.
