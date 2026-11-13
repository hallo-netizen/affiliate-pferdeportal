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
