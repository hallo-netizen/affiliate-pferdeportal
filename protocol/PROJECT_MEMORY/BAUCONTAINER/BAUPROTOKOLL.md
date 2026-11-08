## 2026-11-03 – Hab & Bewahr: reiner Nachweis-/Konsistenzabgleich der bestehenden Campus-Büros
<!-- HAB_GEB_AUDIT_20261103 -->
**Bedarf:** Die nachweislich abgeschlossene Ablage von drei Original-Plugin-ZIPs wurde in anderen Büroakten noch als Blocker dargestellt. Neue Chats sollen eindeutig zum richtigen Current gelangen.

**Kleinste Änderung:** Sieben bestehende Büros und ihre einheitliche Routingkette verifiziert (21/21 zentrale Dateien, 8/8 Eingangslinien-Links, 246 Projektdateien und 42 Verzeichnisse ohne leere Datei); überholte historische Ablage-/Fehlerangaben mittels neuer datierter Nachträge in den betroffenen Currents und Fehlerregistern richtiggestellt. Drei Original-`CURRENT.zip` physisch im Campus nachgeprüft; GitHub PR #622/#625/#627. Keine Strukturänderung, keine neuen Büros, keine parallele Current, keine anderen Portale.

**Prüfgrenze:** WordPress-Livebetrieb, redaktionelle Bildarbeit und extern gespeicherte historische Glossar-WIP-Dateien nicht durch Campus-Pfadtest bestätigt. Zentraler `AUTORITAETSPLAN.json` blieb unverändert, technische Projekt-Currents bleiben alleinige Statusquelle. Warum und genaue Belege: `AENDERUNGSREGISTER.md`.

---

## 2026-11-03 – Hab & Bewahr: isoliertes Eigenplugin-Büro als Campus-Routingvorschlag

**WAS:** Für `EIGENTUMSSCHUTZ` ein eigenes `PLUGINS/`-Büro unter bereits bestehendem Projektgebäude mit `START_HERE`, `CURRENT_STATE`, `HOBBYRAUM`, Inventar, drei technischen Plugin-Akten und isolierten künftigen Voll-ZIP-Orten ergänzt. Autoritätsplan erhält exakt einen neuen `EIGENTUMSSCHUTZ_PLUGINS`-Scope; Gebäudeeingang verlinkt ihn. Keine neue selbstständige Projektstruktur, keine Änderung an existierenden Plugin-Quellen.

**WARUM:** Bisher fehlte die projektgebundene, revisionsfeste Eigenpluginablage; Chat-ZIPs und private Library sind kein Campus-current. Das Büro führt nur drei tatsächlich belegte Eigenpluginlinien, keine WordPress-Fremdplugins oder ungeprüften allgemeinen Affiliate-Stamm. Nicht hochladbare Binär-ZIPs werden **nicht** durch leere oder textbasierte CURRENT.zip ersetzt: PLUGINABLAGE BLOCKED.

**Freigabegrenze:** Campus-Änderung über GitHub-PR, nicht direkt auf geschützten Branch übernommen. Der Nachweis einer tatsächlichen ZIP-Ablage einschließlich unabhängigen Fresh-Download und Live-Installation fehlt.

---

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


## 2026-11-08 – Pferdeatelier-Pluginbüro: Testplugin 0.57.144.23 nach echtem MINI-Export abgelegt

**Bedarf:** Für die vereinbarte einmalige externe SEO-Entscheidung muss der vorhandene WordPress-/PSTE-/PSERC-/PPM679-Bestand verlässlich exportiert werden. Der reale Export enthielt neun als „Array“ bezeichnete und 144 ohne Titel dargestellte Planplätze. Der Betreiber will keinen weiteren Gesamtdiagnose-/Rohkeyword-Durchlauf und keine komplexen Pflichtseiten.

**Kleinste Bauänderung:** Vorhandene PSTE-0.57.144.22-Originaltest-ZIP isoliert als PSTE-0.57.144.23-QA-Fassung korrigiert: vier bestehende PHP-Dateien geändert, bestehende Titel-/Planlesung verbessert, 141 von 144 gespeicherten PPM679-Postbezügen korrekt zugeordnet, drei nicht verifizierbare Posts und neun nicht rekonstruierbare Alt-Titel bleiben gesperrt. Alte Diagnosefunktionen nur einklappbar statt neu aufgebaut. PSERC 0.28.55, alle K0-Dateien, Live-System und bestehende gespeicherte Pläne bleiben unverändert. Keine zusätzliche Tabelle, neue Fachautorität, neue Website oder neue Baucontainer-Logik.

**Prüfung:** 121/121 ZIP-CRC, 83/83 PHP-Lint, 36/36 lokale Tests mit dem vorhandenen realen 1.179er-Export, getrennten Negativ- und Positivproben. Drei unbekannte WP-Posttitel wurden nur in der positiven Simulationsvariante ausdrücklich synthetisch belegt; die echte negative Prüfung sperrt sie. Keine echte WP-/MySQL-Ausführung dieser .23-Fassung, daher TEST und Draft-PR, keine Produktionsfreigabe.

**Ein-Wahrheit-Prinzip / Quellen:** `PROJEKTE/PFERDE_ATELIER/PLUGINS/CURRENT_STATE.md`, `PROJEKTE/PFERDE_ATELIER/PLUGINS/EVIDENCE/PSTE_05714423_ECHTER_EXPORT_FIX_36_LOKALE_WORKFLOW_TESTS_20261108.md` und `PROJEKTE/PFERDE_ATELIER/PLUGINS/QA_ONLY/PSTE_05714423_EXPORTFIX/`; physische QA-ZIP in privater Library `/pferdeatelier/PLUGINS/`. Keine Veränderung an Startmaster, Haupt-Hardlock, K0 oder Nachbarportalen.


## 2026-11-08 – Pferdeatelier PSTE 0.57.144.24 nach echtem WP-Fail aus Version .23

**Bedarf:** Der echte .23-WP-Export brach wegen einer beschädigten alten Editorial-Plan-Zeile nach 1025/1179 Einträgen ab. Der ursprüngliche Positivtest hatte den Fehlerfall nicht tatsächlich simuliert.

**Kleinste Korrektur:** Nur vorhandene PSTE-0.57.144.23-Reader in isolierter .24-QA fortentwickelt, damit alle neun ursprünglich „Array“-Einträge lesbar/als unaufgelöst enthalten bleiben und der aktive PSERC-Plan sowie 144 PPM679-Plätze nachfolgend erfasst werden. Weiterhin keine Freigabe ohne echte Titel und vollständige Belegungsdaten; `complete=false` und leerer Freigabe-Fingerprint. Genau drei bestehende PHP-Dateien (inklusive Versionsheader) geändert, keine Tabellen/Worker/Provider/SEO-Zweitentscheider, K0 und PSERC unverändert.

**Prüfung:** Der lokale PHP-Read-only-Nachbau mit realen 1.179 Quellzeilen, echten neun „Array“-Titeln, drei fehlenden Postzuordnungen und 87 JA-Keywords bestand 46/46 Tests. 83/83 PHP-Syntax, 121/121 ZIP-CRC. Positiver kompletter Simulationsbestand hat 9+3 ausdrücklich synthetische Werte; daher kein echter Vollständigkeitsbeleg für WordPress. Ursprüngliche gespeicherte Option weder überschrieben noch gelöscht, kein WordPress/MySQL-Echtlauf mit .24. Sicherheits-Hardlock und andere Portale unverändert.

**Ablage/Autorität:** `PROJEKTE/PFERDE_ATELIER/PLUGINS/CURRENT_STATE.md` bleibt einzige aktuelle Fachautorität; `QA_ONLY/PSTE_05714424_QUELLFIX/` ist Bau- und Prüfnachweis, Binärpakete privat `/pferdeatelier/PLUGINS/`. Draft-PR #682 nicht mergen.


## 2026-11-08 – V24 ECHT-WP-Export-Abnahme aus v24 nach Nutzer-Upload

**Bedarf:** Die Testsite-Lesefunktion .24 muss an wirklich vorhandenen WordPress-Daten nachgewiesen werden, nicht nur künstlichem neunfach gültigen Redaktionsplan. **Aktion:** Originalexport 16:29 UTC, alle sechs Quellen und 1.179 Zeilen ausgewertet; strenge Negativprobe der neun identischen `Array`-Platzhalter und drei weiterhin belegten unlesbaren PPM679-Referenzen. 55/55 lokale PHP-Tests mit echter Exportdatei erfolgreich. Vollständiger gespeicherter Wert jeder der neun Editorial-Zeilen anhand SHA256-Beweis rekonstruiert; keinerlei ursprüngliche Namen vorhanden. **Grenze:** Test belegt Export-/Sperrlogik, nicht 87 fachliche SEO-FREI-Entscheidungen; künstliche Titel ausschließlich in expliziter Positivprobe. Herkunft der neun Zeilen (externer Filter oder Importoption) nicht im bisherigen JSON unterscheidbar. Kein produktives Freigabe-Hash, keine Änderung von WordPress-Optionen, WordPress-Artikeln, K0 oder Live.

**Ablage:** `PROJEKTE/PFERDE_ATELIER/PLUGINS/EVIDENCE/PSTE_V24_ECHTER_WP_EXPORT_162920_REPLAY_55PASS_20261108.md` plus `QA_ONLY/PSTE_05714424_QUELLFIX/LIVE_WP_20261108_162920/`; Roh-JSON privat. Keine neuen Plugin-Binaries. Sicherheits-Hardlocks unverändert, Draft PR #682.


## 2026-11-08 – Systemische PSTE v0.57.144.25-Quellenreconciliation im isolierten Pferdeatelier-Zweig

**Bedarf:** WordPress-Testexport v24 enthält 1.179 Einträge; bisheriger Parkhaus-Reader sperrt komplette SEO-Fachentscheidung wegen neun bereits vollständig wertloser historischer `Array`-Import-Ruinen und drei älteren nicht mehr vorhandenen WP-Posts, obwohl PPM679 144 echte technische Reservierungen hat. Zusätzliche reale Metadatenkollision zweier WP-Posts unter einer Canonical-ID wurde bei vollständiger Prüfung entdeckt.

**Kleinste Änderung:** Ursprüngliches v24-Test-ZIP unverändert belassen; exakt **zwei vorhandene Leserdateien** plus Plugin-Version auf .25 isoliert anpassen. Inhalte ohne Identität/Artikelabsicht von aktiver Semantik trennen, Originale samt Rohhash exportieren, technische PPM-Reservierungen unabhängig erhalten, WP-Post-IDs bei Migration nur anhand exakter Canonical+Slot-Paarung zuordnen, echte Canonical-Kollisionen protokollieren, widersprechende Filter/Optionquellen und unklare Datensätze fail-closed sperren. WP-Metadaten bleiben unangetastet, kein neuer Worker/Tabellenbau/Owner, PSERC und K0 unverändert.

**Harte Tests:** 85/85 Einzelchecks mit originalem 1.179er-Export, 83 PHP-Syntaxchecks, 121 ZIP-Pfade/CRC, Rebuild der 121 Quelldateien aus originalem v24-ZIP + einem Patch erneut 121 bytegleich, finale ZIP/Paar-ZIP in zwei Läufen exakt gleiche SHA256. Negative Fälle: Quellkonflikte, nichtleere defekte Altzeilen, doppelte Reservierungen, falsche Migrationen, gefälschte BELEGT-Referenzen und fehlender SEO-Owner. PSERC-Reader aus dem unveränderten Plugin .55 verbunden. Kein echter v25-WordPress-/MySQL-Lauf und keine fachliche Freigabe/K0-Produktion, also nur QA.

**Ablage/Autorität:** `PROJEKTE/PFERDE_ATELIER/PLUGINS/CURRENT_STATE.md`, `EVIDENCE/PSTE_05714425_URSACHENFIX_85_ECHTDATEN_LOKALTESTS_20261108.md`, Quellnachweise `QA_ONLY/PSTE_05714425_ROOT_CAUSE_RECONCILIATION/`. Binär-ZIP und Paar in privatem Pluginbüro `/pferdeatelier/PLUGINS/`. GitHub QA-Branch/Draft-PR #682 **nicht mergen**; harte Gebäude-/K0-Grenzen unverändert.
