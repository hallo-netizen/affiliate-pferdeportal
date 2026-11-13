# PFERDE ATELIER – KISS-EINPLUGIN: VERBINDLICHER ARBEITSVERTRAG / CHATÜBERGABE
**Stand:** 13.11.2026 | **Zweck:** Der nächste Chat kann ohne erneute Grundsatzdebatte mit der belegten Inventur und einem gefahrlosen Test-Pilot beginnen.

**Status:** Konzept/Regeln festgelegt; kein neues Plugin erstellt; kein echter WordPress-Ende-zu-Ende-Test durchgeführt; kein Live-Umbau; keine Installationsfreigabe. Das Dokument ist eine **PR-Arbeitsübergabe**, keine zweite Current-Autorität und ersetzt die Campus-Büro-Current nicht. Basis: [Inventur und Empfehlung](2026-11-13_KISS_INVENTUR_EIN_PLUGIN_VERBINDLICHE_EMPFEHLUNG.md), [Regal-Modell](2026-11-13_PRODUKTIONSPLAN_KISS_ERGEBNISOFFEN.md), PR #768.

## 1. Das vereinbarte Ziel in einfachen Worten
**Recherche und redaktionelle Freigabe → Regal aus freigegebenen Themen → externer Titelworker (nur Titel) → chargenweiser Export → unverändertes K0 schreibt nach seinen 81 Regeln → unverändertes Ergebnisformat zurück → WordPress importiert ENTWÜRFE.**

- Kategorieabdeckung ist Teil der **ersten** Redaktion: Wichtige Kategorien dürfen nicht vergessen werden. **Keine künstliche Gleichverteilung**, sondern nach Suchnachfrage und Themenbedarf.
- Kein eigenständiger Produktionsplan/Artikelplatz-Plan nur für einen zweiten Entscheidungsschritt. Ein eindeutig identifizierter Auftrag und ein verlässlicher Bearbeitungsstatus genügen fachlich **grundsätzlich**, müssen technisch aber erst als Ersatz für bestehende PPM-Abhängigkeiten im Echtlauf bewiesen werden.
- **Bevorzugte Lösung:** **EIN** schlankes WordPress-Plugin auf einer **isolierten Testinstallation**, mit klar getrennten Worker-Aufgaben; bestehende funktionierende Bausteine übernehmen, nicht blind alle alten Dateien zusammenkopieren. Live vorerst unverändert.
- Ob später die Live-Seite nur einen kleinen Importer braucht, bleibt ein separater, noch nicht entschiedener Schritt.

## 2. Verbindliche KISS-/Worker-Regeln
1. **Bewährte Teile übernehmen, nicht neu erfinden.** Vor jeder Wiederverwendung Quellfunktion + Ein-/Ausgabe mit Originaldaten belegen; Code nach Möglichkeit unverändert übernehmen. Nicht auf historische QA-PASS-Zahlen als Livebeweis vertrauen.
2. **Genau eine Aufgabe pro Worker.** Recherche/Redaktion, externer Titel, Entnahme/Export, K0, Rücknahme/Import sind voneinander getrennt. Kein Worker darf Zuständigkeit eines anderen fachlich neu entscheiden.
3. **Genau eine fachliche Entscheidung.** Pferde-Bezug, Keyword-/Suchabsicht, Überschneidungen, Kategorie, Artikelart und Kategorien-Abdeckung ausschließlich bei Recherche/Redaktion. **Keine zweite oder nachgelagerte SEO-/Inhalts-/Titel-/Kategorie-Freigabe** in Export, Redaktionsplan, Import oder PPM.
4. **Kein zweiter Qualitätsprüfer für K0.** Die fachliche und sprachliche Textqualität bleibt vollständig bei K0. Nach K0 nur **technische** Eingangskontrolle auf korrekte Auftragskennung, unveränderte Kategorie/Artikelart, Pflichtfelder, Importziel und Dubletten; das ist keine doppelte Inhaltsbewertung.
5. **Eine einzige Auftragswahrheit.** WordPress erhält pro genehmigtem Thema einen eindeutig wiedererkennbaren Auftrag mit unveränderlicher ID, Keyword, Suchabsicht, Kategorie und Artikelart. Keine zweite konkurrierende Planung oder parallele Speichertabelle, sofern der bestehende WordPress-Datensatz genügt.
6. **Regalmodell und sichere Entnahme.** Viele freigegebene Themen dürfen liegen bleiben. Bei Auswahl einer Charge X ist jedes entnommene Thema **vor der Datei-Ausgabe** eindeutig als in Bearbeitung reserviert. **Nicht physisch löschen**; wiederholter/gleichzeitiger Export darf denselben Auftrag nicht erneut als freien Auftrag entnehmen.
7. **Wiederanlauf ohne Neubewertung.** Bei K0-Abbruch, fehlendem Download oder Teilimport wird derselbe Auftrag gezielt fortgesetzt; nie Keyword/Kategorie neu freigeben. Ein fehlerhafter Auftrag stoppt nicht die unabhängigen anderen Aufträge.
8. **Import nur einmal je Auftrag.** Ein identisches Ergebnis darf nicht mehrfach neue WordPress-Entwürfe erzeugen. WordPress importiert als **Entwurf**, nicht automatisch öffentlich. Bestehende Sicherheits-/Publish-Sperren nicht ohne geprüften Ersatz entfernen.
9. **Titel und K0 bleiben unverändert.** Den vorhandenen externen MINI-/Titelablauf (nur Titel), K0 mit 81 Regeln, die **fünf** bestehenden K0-Felder `title, target_keyword, category, article_type, plan_slot` und das bisherige Rückgabeformat nicht ändern. Der bisherige `plan_slot` ist Pflicht im Altvertrag; seine sichere, akzeptierte Belegung ohne PPM muss vor einer Umstellung belegt werden. Die **sichtbare** Import-Schnittstelle und Entwurfswirkung erhalten; eine nachweislich zwingende interne PPM-Abhängigkeit darf nur minimal und getestet ersetzt werden.
10. **Radikal bereinigen, aber beweisbasiert.** Veraltete Prüfpfade, tote Funktionen, überflüssige Zwischenspeicher, doppelte Freigaben/Verweise/Hooks nur löschen, **wenn** die Nutzlosigkeit im gesamten verbleibenden Export-/Import-/Fehler-/Wiederanlaufpfad belegt ist. Keine pauschale Bereinigung auf Verdacht; keine unterbrochenen WordPress-Aufträge.
11. **Keine unnötige Infrastruktur.** Keine neuen fachlichen Worker, Prüfplugins, Datenbanktabellen, zusätzlichen Redaktionspläne oder WordPress-Core-/Frontend-Umbauten. Ein zentrales Plugin, intern getrennte Verantwortlichkeiten; bestehende WordPress-Möglichkeiten bevorzugen.
12. **Änderungsgrenze und Beweis.** Bestehende Plugins und PPM/Editorial Guard auf Live nicht löschen/deaktivieren. Pilot nur in isolierter Test-WordPress-Kopie; keine zwei Schreibsysteme zugleich auf denselben Themen/Datensätzen. Erst Original-Zustand und Backup sichern, dann minimale Änderung; jedes Ergebnis gegen den gesamten Zielworkflow prüfen; Rückweg/Version dokumentieren.
13. **Keine erfundenen Daten.** Die 61 historisch `FREI`-Entscheidungen nicht stillschweigend nachprüfen, zuordnen, neu betiteln oder mit erfundenen Kategorien/Artikelarten/IDs ergänzen. Echte fehlende Originalfelder als technisch offenen Einzelauftrag melden, nicht semantisch neu entscheiden.
14. **Keine Installationsfreigabe ohne REALTEST.** Tests müssen den echten WordPress-Speicher, Export, Titelrücklauf, K0-Handoff und WordPress-Entwurfsimport einschließlich Wiederanlauf belegen. Mocks/Syntax/CRC beweisen keine echte End-to-End-Produktion.
15. **KISS auch beim Protokoll.** Ein aktueller Handover, Fortschritt/Änderungen nur an der geltenden autoritativen Stelle; kein neuer paralleler Current-Stand. Klare Trennung: **bewiesen / lokal simuliert / offen**.

## 3. Bereits belegte Ist-Fakten und Fehlerhistorie
- **PSTE 0.57.144.50 QA** (83 PHP-Dateien), **PSERC 0.28.71 QA** (42 PHP-Dateien) sind als vollständige Original-/QA-ZIPs im Files-Library-Büro `/pferdeatelier/PLUGINS/ARBEITSRAUM_PSTE_KISS` zugänglich; QA-Versionen sind keine installierten Liveversionen.
- Vorhandene Funktionen: DataForSEO-/Keyword-Recherche; einmalige SEO-Freigabe; PSTE-Kategorieabdeckung; vorhandene MINI-Titel-Funktionen; PSERC-K0-Manifest mit fünf Feldern; vorhandene PSERC-WordPress-Importfunktion. **Vorhandensein ist kein Beweis eines fehlerfreien Gesamtlaufs.**
- Die ursprünglichen echten SEO-Entscheidungen vom 09.11.2026: **87 Gesamt, 61 FREI, 20 BELEGT, 6 KLÄRUNG**. Im read-only Diagnoseexport 13.11.2026 bei allen 61 alten Freigaben `planning_gate_status=NOT_STORED`; PSERC `planning_topic_count_expected=0` / `PSERC_PLAN_NO_SOURCE_TOPICS_PRESERVE_PRIOR_SNAPSHOT`.
- Ursprungsfehler der alten PSTE .47: vorhandener MINI-Titel unterdrückte Artikelplatzzuordnung (`FREI && !hasTitle`), mit 61 Originalfällen als Null-Aufrufe belegt. Lokale QA .50 korrigierte u. a. Wiedervergabe/Statuskonflikte, ist aber **nicht live abgenommen**.
- PSTE und PSERC sind miteinander gekoppelt; PSTE speichert Freigabe und Vormerkung, PSERC liest seine Planquellen, echter PPM-Plan führt zusätzlich gesonderten Status. Dies erklärt **Teile** der Blocker, aber nicht automatisch alle Altfall-Probleme.
- **PPM 6.7.9 ist nachweislich ein installiertes eigenes WP-Plugin** (Leistungsanalyse 12.11.2026); das zusätzliche Plugin **Editorial Guard 0.1.1-quarantine** ebenfalls. PPM-Original-ZIP liegt auf GitHub `control/startmaster0107/runtime_packages/PORTAL_PRODUCTION_MACHINE_V6.7.9_SIGNED_ARTICLE_TYPE_EXTENSION_ROOTFIX_FINAL.zip`, sein vollständiger Quellinhalt konnte mit verfügbarer GitHub-Dateischnittstelle bisher nicht gelesen werden. Der Guard-Schutz darf nicht ohne Quell-/Laufprüfung abgeschaltet werden.
- Der vorhandene PSERC-System4-Import ruft `PPM679_Editorial_Plan_Runtime_Gate::record_readback` auf. Deshalb würde **ein sofortiges Entfernen von PPM/Produktionsplan nachweislich den Importvertrag gefährden**. Stattdessen erforderliche Identität/Importgrenze erhalten oder gezielt klein ersetzen.
- Ältere Tests mit PPM/K0-Mocks sind keine Echtabnahme. **Keine** komplette neue KISS-Fassung wurde installiert oder live getestet.

## 4. Konkreter STARTPUNKT FÜR NÄCHSTEN CHAT – kein erneutes Grundsatzkonzept
A. Diese Datei und die [Quellinventur](2026-11-13_KISS_INVENTUR_EIN_PLUGIN_VERBINDLICHE_EMPFEHLUNG.md) lesen. Geltenden Campus-`START_HERE`/`AUTORITAETSPLAN` und das Pluginbüro-`CURRENT_STATE` lesen; alte QA-Fassungen nicht als Live-Stand ausgeben.
B. **Read-only Funktionsinventur** der aktuellen PSTE-/PSERC-Originale, besonders reeller 5-Felder-Export, WP-Importer, PPM-Abhängigkeit und externer Titelweg. *Keine* erneute 5.020-Keyword-Recherche, keine Grundsatzdiskussion.
C. Kleinsten Einplugin-Pilot ableiten: intakte Quellfunktionen unverändert, genau **ein** WordPress-Auftrag / Datensatz pro Freigabe und minimaler Status `FREI → RESERVIERT/EXPORTIERT → IMPORTIERT_ENTWURF`, eigener Wiederanlauf `OFFEN`. Redaktionsplanung/Kategorien-Abdeckung bleibt bei Recherche.
D. **Gezielte Trockenübung zuerst**, mit echten bekannten drei Aufträgen und einer 20er-Charge: paralleler Doppel-Export, verlorene Datei, Teilrückgabe 13/20, doppelte Rücklieferung, Kategorie-/Auftrags-ID-Bindung, K0-Fünf-Felder, Entwurf ohne Publish. **Nur echte Fehlstellen reparieren**, nicht funktionierende Teile neu schreiben.
E. Entscheiden anhand Test: Legacy PSERC-Plan und PPM-Planfunktion überflüssig oder für technischen Import erforderlich? Live zunächst nicht verändern. Erst bei bestandener WP-Echtabnahme schrittweise Ablösung vorschlagen.

## 5. Was NICHT behaupten / NICHT tun
- Nicht behaupten, die 61 Altaufträge oder ein echter K0→WP-Draft-Lauf seien schon repariert.
- Nicht Titelworker und K0 umgestalten.
- Keine semantische Nachprüfung unter dem Vorwand technischer Qualität.
- Nicht alle vorhandenen PHP-Dateien blind migrieren; keine alten Verweise/Funktionen ohne vollständige Aufrufprüfung entfernen.
- Kein Installations- oder Live-Freigabesiegel ohne echten WordPress-Lauf und Rollback.
- Nicht die bisherige PPM-/Guard-Installation unbesehen ersetzen.

**Verbindliche Pilot-Empfehlung:** **Ja** zu genau **einem** schlanken Plugin mit Worker-Grenzen, **nein** zu Total-Neubau und zusätzlichen Plänen; **keine endgültige Entfernung** der PPM-Abhängigkeit, bis der tatsächliche Import- und Schreibvertrag dafür geprüft und real nachgewiesen wurde.

**Nächster Schritt:** Umsetzungsplan aus konkreten Originalfunktionen mit Quellbeleg und Minimal-Diff erstellen; dann isolierten Pilot bauen und echte Testdatensätze prüfen. Keine Liveänderung.


## 6. Verbindliche Ergänzung – Zuständigkeitssperre, vollständige Code-Inventur und Portalneutralität
**Datum:** 13.11.2026. Diese drei Ergänzungen sind Bestandteil des verbindlichen Pilot-Zielvertrags. Sie ändern nicht die früheren Grenzen: K0, externe Titelerstellung und deren Dateiformate bleiben unverändert; kein Live-Release.

### 16. Technisch erzwungene Einmalzuständigkeit (Anti-Aufblähungs-Vertrag)
**Ziel:** Das System soll neue überflüssige Zuständigkeiten möglichst automatisch bereits beim Einbau verhindern.

- Vor dem Umbau gibt es eine **abgeschlossene, kurze Aufgabentabelle** für genau diese Schritte: `Recherche/Fachfreigabe`, `freigegebenes Regal`, `externer Titel`, `Entnahme/Export`, `K0 extern`, `Rückgabe/Entwurfsimport`, `Wiederaufnahme`. Die Kategorienabdeckung gehört ausschließlich zur **ersten** fachlichen Planung.
- Pro **fachlicher Entscheidung** gibt es **genau einen Eigentümer**. Zu jedem Schritt festhalten: erlaubte Eingaben, erlaubte Ausgaben, zulässige Statusänderung, **verbotene Fachentscheidungen**. Nachgelagerte Schritte transportieren ausschließlich gebundene Fakten.
- **Keine neuen Fachworker, Gremien, Gates, Prüfinstanzen, Tabellen, Zwischenpläne oder Statuskopien ohne vorherigen belegten Bedarf und ausdrückliche Nutzerfreigabe.** Eine neue Prüffunktion darf niemals eine bereits entschiedene Suchintention, Kategorie, Artikelart oder Textqualität nochmals bewerten.
- **Technische Sicherheitskontrollen sind keine zweite fachliche Prüfung:** Auftrags-ID, unveränderliche Übergabefelder, parallelsichere Entnahme, Wiederanlauf, sichere Entwurfsanlage und Duplikatverhinderung sind notwendig und gehören jeweils nur an die technisch zuständige Stelle.
- Eine kleine **automatische Vertragsprüfung** am Pilot-Build und vor Freigabe kontrolliert: nur definierte Rollen; jeder fachliche Entscheidungsaufruf an genau einer Stelle; keine Nachentscheidung in Export/Import; eindeutige Auftragsstatusquelle; K0-Fünf-Felder und Titel-/Rückgabeformat unverändert. Testfälle müssen zusätzliche unerlaubte Freigaben/Worker **negativ** nachweislich blockieren.
- **Kein unprüfbares Versprechen:** Diese Regel verhindert belegbare Rollen- und Vertragserweiterungen, aber nicht jeden denkbaren Programmfehler. Sie ersetzt keine tatsächlichen End-to-End-Tests.

### 17. Lückenlose, aber verhältnismäßige Codebereinigung
**Annahme bestätigt, Präzisierung:** Alle vorhandenen Quelldateien, Funktionen, Hooks, Schnittstellen, Schreibzugriffe und erreichbaren Entscheidungs-/Abbruchpfade **inventarisieren und beurteilen**. Nicht jede einzelne Anweisung manuell zur neuen fachlichen Abstimmung machen – das wäre selbst ein KISS-Verstoß.

Für jede relevante Funktion eine knappe, belegte Entscheidung: `BEHALTEN`, `UNVERÄNDERT ÜBERNEHMEN`, `VEREINFACHEN`, `ENTFERNEN`, `OFFEN BIS ECHTTEST` – mit tatsächlicher Verwendung, Grund und Risiko.

- Alte Codestücke, toter Code, überholte Verweise, doppelte fachliche Kontrollen, doppelte Daten-/Statushaltung und ungenutzte Abhängigkeiten **nur nach belegtem Nichtgebrauch** entfernen.
- Besonders kritisch: WordPress-Aktionen/Hooks, K0-Export-/Importformat, PPM-Rücklese- und Import-Gates, Titelrücklauf, Entwurfsstatus, Sicherheits-/Publish-Sperren sowie Wiederanlauf und Altdatenmigration.
- **Vorher/Nachher-Gegenprobe** derselben echten Ein- und Ausgaben; keine Löschung nur aufgrund statischer Suchtreffer. Beschränkung auf den bestehenden relevanten Ablauf; kein unnötiger Neuaufbau oder unbegrenzter Audit aller WordPress-/K0-Kerne.
- Das Ergebnis ist eine kurze **Behalten-/Entfernen-Liste plus Minimal-Diff und Negativtests**, nicht ein weiteres umfangreiches Prüfungssystem im Produkt.

### 18. Portalneutraler Kern mit schlankem Portalprofil
**Ja, ausdrückliches Ziel: derselbe Plugin-Code soll auf Pferdeatelier, Hobby Depot und Hab & Bewahr installierbar sein.**

- **EIN allgemeiner, wiederverwendbarer Plugin-Kern pro WordPress-Installation**, mit gleichbleibenden Zuständigkeiten, Auftragsspeicherung, Worker-Grenzen, Export-/Import-Format und Rücklaufkontrolle. **Nicht** drei auseinanderlaufende Quellkopien und kein zentraler Server, der Portaldaten vermischt.
- **Portalabhängiges ausschließlich im lokalen Profil oder vorhandenen WP-Kategoriedaten:** Portalidentität, Themenwortschatz/Ausschlussbegriffe, Kategoriebaum, Suchquellen-/Prompt-Kontext, gültige Artikelarten und eventuelle Redaktionsrichtlinien. Konfiguration möglichst aus vorhandenen WordPress-Daten ableiten; keine unnötige neue Einstellungswelt.
- **Nachgewiesener Ist-Befund aus QA-Originalquellcode:** PSTE enthält fest eingebaute Wörter wie `pferd`/`pferde` in der Kannibalisierungsprüfung und feste Pferde-Kategorien in der Artikelart-Zuordnung; PSERC enthält `PFERDE_ATELIER_...`-Konstanten für Import-/Abschlussverträge. **Unverändertes Kopieren ist deshalb keine geprüfte Portalneutralität.**
- Zur Entkopplung **die vorhandene fachliche Entscheidungslogik bewahren**, nur die harten Pferdeatelier-Annahmen in genau **ein** Portalprofil verschieben; Funktionalität weder auf Hobby Depot noch Hab & Bewahr erraten. Kategorieabdeckung für jedes Portal anhand seines **eigenen** Baums; keine Gleichverteilung erzwingen.
- **Gleicher Quellstand, getrennte Datenbanken/Portalprofile, getrennte Testläufe.** Zuerst Pferdeatelier-Echttest; danach zusätzlicher Negativ-/Positivtest mit je echten Kategorien/Beispielaufträgen aus Hobby Depot und Hab & Bewahr. Keine Freigabe als „universell“ ohne beide realen Portal-Gegenproben.
- **Keine Veränderung von K0:** Die fünf Eingabefelder und das vorhandene Rückgabeformat bleiben Pflicht. Ein eventuell anders benanntes `plan_slot` ist nur nach echtem Vertragsnachweis durch stabile Auftragskennung ersetzbar.
- Portalneutralität darf **nicht** zu neuen Plugins, Worker-Schichten oder doppelten Entscheidungsregeln führen. Sie ist eine **Daten-/Konfigurationsgrenze**, kein Neubau eines Frameworks.

### Startvorgabe für den nächsten Chat
**Zuerst** Rollen-/Funktionskarte und Quellnutzungsinventur erstellen; dann vorhandene stabile Funktionen in einem neuen Portal-neutralen Pilot **gezielt übernehmen**, PPM-Abhängigkeiten nur nach konkretem Nachweis entfernen; anschließend 3 reale Altaufträge, 20er-Charge und Portalprofile testen. Keine Liveänderung; keine neue Fachprüfung. **Nicht** nochmals eine Grundsatzarchitektur ausdenken.

**Status:** Drei Ergänzungen beschlossen/dokumentiert. Noch kein fertiger Code, kein universeller Test und keine WP-Liveabnahme.

### 19. Sofortartikel / freier Artikelauftrag mit synchronisierter Planung
**Neu verbindlich (13.11.2026, Nutzerkorrektur):** Neben dem normalen Keyword-/Regalweg muss der bestehende **Kurzweg für frei initiierte Artikel** erhalten bleiben.

- Ein Nutzer darf einen Artikel **direkt und kurzfristig anstoßen**, ohne zuerst den vollständigen Keyword-Recherchevorrat abzuarbeiten. Der bereits vorhandene Kurzweg ist zu inventarisieren und möglichst unverändert zu übernehmen; kein neuer Spezial-Worker.
- **Eine zentrale Themen-/Kategorieübersicht:** Ein Sofortartikel erhält vor der Übergabe eine feste Auftragskennung und eine Zuordnung zu der bestehenden Kategorie, Artikelart und dem tatsächlich zugewiesenen Keyword/Suchthema. Damit zählt er als bereits geplant bzw. beauftragt, auch für die Abdeckung der Kategorien und spätere Duplicate-Vermeidung.
- **Keine Parallelwelt:** Sofortartikel dürfen nicht nur im K0-Export erscheinen, während die Themenengine sie weiter als unbesetzt ansieht. Die Eintragung geschieht im selben vorhandenen Auftragsspeicher wie beim normalen Regalweg.
- **Keine doppelte SEO-/K0-Qualitätsentscheidung:** Der freie Start ist keine Erlaubnis zu widersprüchlichen oder fehlenden Pflichtangaben. Nur der zuständige redaktionelle Schritt bindet die notwendige Suchabsicht/Kategorie/Artikelart einmal. Bei völlig fehlenden Angaben wird der konkrete Auftrag zur Klärung gehalten; keine verdeckte automatische neue Recherche in nachgelagerten Workern.
- **Externe Grenzen unverändert:** Externer Titelprozess, unveränderter K0-Fünf-Felder-Vertrag und der WordPress-Entwurfsimport bleiben intakt.
- **Pflicht-Gegenprobe vor Pilotfreigabe:** Sofortauftrag anlegen → erscheint in der einen Themen-/Kategorieübersicht → wird nicht erneut als freies Thema ausgewählt → eindeutiger Export → K0-Rückgabe → genau ein Entwurf; Abbruch und Wiederaufnahme ohne erneute fachliche Entscheidung.

Der Begriff „Redaktionsplan synchronisieren“ bezeichnet im neuen KISS-Zielbild **die eine zentrale Themen-/Kategorie- und Auftragsübersicht** – nicht die unbewiesene Pflicht, einen gesonderten PPM-Produktionsplan wieder einzuführen. Vorhandene Altschnittstellen müssen bis zur tatsächlich bestandenen Migration kompatibel bleiben.


### 20. Integrierte Diagnose als Beweisquelle – nicht als zweiter Prüfer
**Nutzerentscheid vom 13.11.2026: Pluginname im WordPress-Backend ausschließlich `Texterstellung`.** Der frühere Name „Artikelwerkstatt – KISS“ ist nur historisch. **Ein einziges Plugin.** Kein zusätzliches Diagnoseplugin und keine neue fachliche Qualitätsinstanz.

- Die Diagnose gehört in die bestehende **Texterstellung**. Ihr Zweck ist die **Entwickler-/Assistenten-Fehlersuche anhand tatsächlicher Daten**, nicht die tägliche Bedienung. Ein Admin kann einen maschinenlesbaren JSON-Bericht im Backend herunterladen und im Chat bereitstellen.
- Beim bestehenden Produktionsweg werden nur tatsächliche **Verarbeitungsschritte, Statusänderungen, Fehlercodes, Zuordnungen, Einzelrücklaufprobleme und Speichernachweise** protokolliert; ein begrenzter Verlauf genügt. Keine neue Bewertung von Suchintention, Keyword, Titel, Textqualität, Kategoriebedarf oder K0.
- **Tatsachenkennzeichnung:** Belegte Originaldaten, lokal erzeugte IDs/Artikelplätze und offene/fehlende Felder müssen unterscheidbar bleiben. Kein erfundener PPM-Status und keine Scheinerfolge.
- **Datenschutz/Sicherheit:** Diagnoseabruf nur für Administratoren mit Bestätigung; keine API-Schlüssel, Passwörter, Nonces, vollständigen Artikeltexte oder unsicheren Anbieterfehlermeldungen. Site-Keywords/Titel und echte Fehlerkennungen dürfen für die begrenzte Fehlersuche enthalten sein. Keine automatische Übertragung.
- **Beweisregel:** Bei Problemen zuerst den real heruntergeladenen Bericht lesen, Ursache einem einzigen verantwortlichen Schritt zuordnen und nur dort reparieren. Ein fehlender Bericht begründet keine Vermutung. Ein neuer Reparatur-/Diagnose-Worker ist verboten.
- **Ist-Stand:** `Texterstellung_0.3.0_TEST_INSTALLIEREN.zip` lokal mit **119** Gegenproben geprüft, aber noch **nicht** auf echter WordPress-Testseite installiert/abgenommen. Keine Livefreigabe. Offene automatische PSTE-Semantik und PPM-/K0-Kompatibilität bleiben ausdrücklich offen.
- **Chatübergabe:** `2026-11-13_TEXTERSTELLUNG_0.3.0_DIAGNOSE_ABNAHME.md` im gleichen PR lesen; TEST-Installer verlustfrei als ZIP-Base64 unter `../PILOT_TEXTERSTELLUNG/Texterstellung_0.3.0_TEST_INSTALLIEREN.zip.base64.txt`; Ziel-Testseite und Live unverändert, bis der Nutzer selbst installiert und echte Daten ausliest.


### 21. Vollständige Testoberfläche im linken WordPress-Menü
**Nutzerentscheidung (13.11.2026):** Kein Mini-Pilot unter `Werkzeuge`. **Ein** WordPress-Plugin namens `Texterstellung`, im WordPress-Backend als **eigenständiger linker Hauptmenüpunkt**, mit allen Produktionsstationen als Untermenüs: Übersicht, Recherche, Redaktionsplan, Sofortartikel, Titelerstellung, K0-Export, Rückimport, Entwicklerdiagnose.

Die Installationsdatei darf erst zum Test angeboten werden, wenn jede genannte Station tatsächlich eine aufrufbare und lokal geprüfte Funktion hat, das Plugin ohne aktive PSTE-/PSERC-/PPM-Klassen startet und der gleiche Auftragsbestand über alle Schritte geführt wird. Keine zusätzlichen Plugins und keine Änderung an K0, externen Titel- oder Rückgabedateien.

**Umsetzung:** `Texterstellung_0.4.0_TEST_INSTALLIEREN.zip`, SHA256 `8a5c2faf39081e05d5610bb4757e9d4f6d8eaaa8f52ca0771007be0ab6c8c3c5`, 34.346 Bytes; neuer `add_menu_page`-Hauptmenüpunkt und acht `add_submenu_page`-Stationen. Externe redaktionelle Freigabe zusätzlich als eingefrorene SEO-Dateirunde mit WP-/Auftragsbestand; dadurch ein durchgehender Testlauf. Passwortspeicherung für DataForSEO separat im Testplugin.

**Harter Statusvorbehalt:** Der vollständige **Workflow ist lokal simuliert**, nicht WordPress/K0-echt abgenommen. Die alte automatische semantische PSTE-Entscheidung wurde **nicht** 1:1 übernommen; die eine Freigabe läuft aktuell manuell oder über den externen einmaligen SEO-Redakteur. Nur TEST, kein Liveersatz. Ausführlicher Nachweis `2026-11-13_TEXTERSTELLUNG_0.4.0_ABNAHME_UND_CHATUEBERGABE.md` im gleichen PR.
