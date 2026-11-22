# Hab & Bewahr – Gefahr & Schutz: praktischer K-Multi-Teststand

## Fortschreibung 22.11.2026 – NUR Workflow-Sicherheit, Ausgabe und Plugin-Speicher (Vorrang)

**Auftrag strikt eingegrenzt:** Keine Beitrags-, Link-, Tabellen- oder Textregeln aus Pferdeatelier übernehmen. Original-K0 und alle alten K0-Workflows **unangetastet**, keine K-Multi-Architektur geändert.

### Originalquellen und gesicherte Tatsachen
- Neueste im Pferdeatelier-Pluginbüro entdeckte Original-ZIP: **0.4.47 KISS-SAMMELREPARATUR** (nicht die zuvor als neueste angenommene 0.4.46). Der Bürobericht belegt die lokale Fehlerreparatur an Diagnose-Download und MINI-Dublettenbezug; **Live-Installation nicht nachgewiesen**.
- Original Hab-Plugin 0.4.31.20 mit Archiv-SHA-256 `404090884e80ade8d963859395ebaa5271f062199889d0a955cbfb0f6adc49e7`, 87 Dateien, 78 PHP; ursprünglicher gespeicherter WordPress-Auftragsweg mit wiederholten Option-Leseoperationen und optionalem gigantischen Diagnose-JSON für Log-Hash.
- **Neue einzelne, lokal getestete Hab-Update-Testfassung 0.4.31.21:** ausschließlich zwei vorhandene PHP-Dateien und README geändert, **84/87 Dateien byteidentisch**; WP-Optionsname, DB-Mutation-Lock, `update_option`/Original-WordPress-Hooks, Entwurfsschutz, gespeicherte Aufträge, MINI-Export/-Import, Wiederdownload und Abbruchzuständigkeit **unverändert**. WordPress-Artikelimport wurde **nicht** umgestellt; Pferdeatelier-MySQL-Streaming oder AJAX-Einzelimport **nicht** vorsorglich kopiert.
- **Nachgewiesene lokale Testfälle:** 78/78 PHP-Syntaxdateien PASS; altes Diagnosemodul bei 64-MiB-Test mit einem synthetischen großen Auftragsbestand `PHP_MEMORY_EXHAUSTED`, Testfassung bei identischem Eingang PASS; bei 256 MiB weiterhin vollständiger bisheriger Diagnose-Hash, bei weniger Speicher explizit markierter Verzicht auf nur den großen *zusätzlichen* Log-Hash; Diagnoseansicht öffnet ohne großes Auftrags-Option-Lesen und zeigt Button; Speichern/Unverändert/Writes-fehlgeschlagen/Dateninhalt/Lock/Gespeichert-Zustände in PHP-Stubs geprüft. Kein echter Hab-Live-Erfolg, keine behauptete Behebung *aller* 512-MiB-Fälle.
- Archiviert **nur als nicht freigegebener Update-Kandidat** im EXISTIERENDEN Ordner: `/hab-und-bewahr/TEXTERSTELLUNG/PLUGIN_FREIGABEKANDIDATEN/Hab-Textplugin-0.4.31.21-KISS-SPEICHER-UND-DIAGNOSE-NUR-TEST.zip`; mit `HAB_TEXTPLUGIN_043121_SICHERHEIT_PERFORMANCE_NUR_TEST_20261122.md`, ZIP-SHA-256 `6cf25af769ebbf6b2e164a1106e1128ecdecd5c08f1aa05b01e6f2d1d5814aca`. **Nicht** in `PLUGIN_FREIGABEN`, nicht auf Live installiert.
- **K-Multi finaler Ausgabe-Owner unverändert**: `offline_writer_dev/hobby_trial/kmulti_safe_delivery.py` und `kmulti_single_release.py`. Der aktuelle Hab-Auftrag kann nicht versehentlich über die Hobbydepot-Freigabe laufen. Zusätzlicher **echter Negativtest** am bereits bestehenden Testfile `test_kmulti_safe_delivery.py` mit originalem Hab-Upload, unfreigegebenem Hab-QA-Kontext, echtem Hab-Binding-Manifest und gefälschtem Zertifikat: **keine finale Datei, alte Datei entfernt, keine unautorisierte Veröffentlichung**. Beide Original-GitHub-Workflows nach dem neuen Test **SUCCESS**: [Hobby Sicherheitstestlauf 45041674058](https://github.com/hallo-netizen/k0-multiportal/actions/runs/45041674058), [Hab Gesamt-QA-Lauf 45041674065](https://github.com/hallo-netizen/k0-multiportal/actions/runs/45041674065). **Kein** neuer Freigabeweg, keine K0-Änderung.
- **Reale offene Hab-Endanbindung:** bestehender sicherer K-Multi-Endausgang bleibt derzeit Hobbydepot-spezifisch; der Hab-Freigabebeleg darf erst beim Vorliegen **vollständiger echter Hab-QA** und vertrauenswürdig signiertem Freigabebeleg an genau diese Ausgabe gebunden werden. Aktuell 57/110 Original-Hab-HARD-Regeln mit echtem Beleg pro Artikel, 53 weiterhin nicht ausgeführt. Eine verifizierte WordPress-Importdatei existiert deshalb **nicht**.

**Nächste konkrete sichere Arbeit:** 0.4.31.21 als Update **nur im Hab-Testsystem** mit großen echten gespeicherten Aufträgen testen und Rückimport/Abbruch/Wiederaufnahme/Diagnose gegen alte Funktionsliste kontrollieren, bevor eine Liveempfehlung ausgesprochen wird. Hab-K-Multi-Endsignatur erst nach vollständiger echter QA anbinden; kein K0-Aufruf und keine Regelübernahme.

---


## Korrigierter Vergleich: ausschließlich K-Multi-Verfahrenssicherheit, Dateiausgabe, WordPress-Plugin-Performance – 22.11.2026

**GELTUNGSBEREICH:** KEINE Übernahme von Pferdeatelier-K0-Text-/Beitrags-/Link-/Tabellenregeln. KEINE Änderungen an K0. KEIN Umbau von K-Multi, keine neue Station, kein neues Plugin; ausschließlich Quellvergleich und Anschlussbewertung.

**Tatsächlich geprüfte Quellen:**
- Pferdeatelier Original-K0 `hallo-netizen/affiliate-pferdeportal`, Branch `konzept0-portal-neutral-20261002`: `K0_CURRENT_STATE.json`, `K0_START_HERE.md`, `engine/k0_wp_upload.py`, `engine/k0_wordpress_export.py`, `engine/wordpress_batch_export.py`, `.github/workflows/k0-writer-accept.yml`. Letzter bestätigter Single-Writer-Lauf [45008261702](https://github.com/hallo-netizen/affiliate-pferdeportal/actions/runs/45008261702) SUCCESS.
- Echte ZIP-Pakete im jeweiligen vorhandenen Library-Pluginbüro bytegeprüft: Pferdeatelier `Texterstellung-0.4.45-KISS-GESAMTWORKFLOW-SPEICHERFIX.zip` und `Texterstellung-0.4.46-MINI-UND-K0-SPEICHERWEG.zip` (SHA256 `2358975027ecb5b30bcd923014a4c24c086688f6d220f07c648cc4b0d3991fd2`), Hab `Texterstellung_HAB_UND_BEWAHR_0.4.31.20_MINI_EINMALREIMPORT_PFERDEATELIER.zip` (SHA256 `404090884e80ade8d963859395ebaa5271f062199889d0a955cbfb0f6adc49e7`). ZIP-Dateien lokal entpackt und echte Klassen/Funktionen direkt verglichen, nicht nur Dokumentation.
- Original-K-Multi `hallo-netizen/k0-multiportal`, Branch `k0-offline-rule-bindings-20261027`: `portal_auto/kmulti_current_upload.py`, `hobby_trial/kmulti_safe_delivery.py`, `hobby_trial/kmulti_single_release.py`, `portal_auto/kmulti_hab_fullchain_audit.py`.

### 1. Sicherheit des Eingangs, Stopp-/Fortsetzverhalten
- K0 und K-Multi haben getrennte originale Eingänge. K0 übernimmt die schon vorhandene WordPress-Herkunftsquittung, prüft unveränderliche Original-ID/-Auftragsdaten und verweigert widersprüchliche Weiterführung statt zu überschreiben. K-Multi verarbeitet nur eine tatsächlich **frisch hinzugefügte** `kmulti_inbox/*.json` pro Push; bloße Codeänderung darf keinen alten Auftrag erneut starten.
- K0-Writer-Reparaturen und -Wiederanlauf bleiben an die ursprüngliche Writer-Job-ID gebunden. K-Multi darf diese K0-Mechanik NICHT aufrufen; es behält die eigene unveränderliche Eingangsidentität und die jeweiligen Original-Owner.
- Beide WordPress-Plugins besitzen getrennt gespeicherte MINI-Chargen, MINI-Wiederdownload und `txe_research_stop`. **Der WordPress-Forschungsstopp bricht weder K0 noch K-Multi-GitHub-Actions ab**. Kein angeblicher globaler GitHub-Abbruchknopf; kein Löschen bereits gespeicherter Aufträge. Bei fehlendem aktuellen K-Multi-Upload darf niemals ein archivierter Auftrag ersatzweise genutzt werden.

### 2. Dateiausgabe und Veröffentlichung
- K0 bildet nur **vollständig geprüfte Original-Single-Artikel** in der ursprünglich eingefrorenen Auftragsreihenfolge zu genau **einer WordPress-JSON** zusammen; `publish_allowed=false`. Fehlende/unpassende Einzelartikel, geänderte Artikelidentität oder ungültiges HTML blockieren die Batchbildung.
- Das bestehende K-Multi-Modul `kmulti_safe_delivery.py` schützt die **eine** Ausgabe `KMULTI_WORDPRESS_IMPORT.json`: alte gleichnamige Datei vor jedem Versuch entfernen, eindeutiger JSON-Pfad, echte autorisierte Fremdsignatur aus Runner-Konfiguration, unveränderte gebundene Texte/Nachweise, atomare Ausgabe, `publish_allowed=false`. Bei Fehlfreigabe **keine Importdatei**.
- **Wichtige reale Anbindungslücke:** Der momentan hinter dem sicheren K-Multi-Ausgang liegende `kmulti_single_release.py` ist ausdrücklich noch auf **Hobbydepot** ausgelegt (Original-Portalprüfung auf `hobby_depot`, Hobby-Regelbuch). Obwohl Hab WordPress den allgemeinen Alt-Transportvertrag `PFERDE_ATELIER_WORDPRESS_IMPORT_V1` technisch versteht, ist damit **noch keine vertrauenswürdige Hab-Endfreigabe angeschlossen**. HAB-Original-Fachbelege und K-Multi-Release-Owner dürfen nicht durch Hobby-Belege, simulierte Signaturen oder eine behauptete Regel-Vollabnahme ersetzt werden.
- Der Hab-Gesamtaudit bleibt bei **57/110 real belegten HARD-Regeln pro Artikel, 53 ausdrücklich NOT_EXECUTED**; vollständige fachliche Freigabe sowie echte vertrauenswürdige Hab-Signatur fehlen. Deshalb **KEINE Hab WordPress-Enddatei** und keine Veröffentlichung. Das ist Sicherheits-SOLL, kein versehentlich ausgelassener Export.

### 3. Echter Performance-/Speichervergleich der Original-PHPs
- Pferdeatelier 0.4.46 enthält im ursprünglichen selben Plugin bereits `persistState()` und `streamOptionUpdate()` (einzelne 256-KiB-Chunks für die gespeicherte große WordPress-Option; kompatibler Fallback). Außerdem `ajaxImportDraftOne()`, `ajaxFinalizeDraftOne()` und die bereits vorhandene `txe-staged-import.js`: WordPress-Artikel einzeln pro Request, Wiederaufnahme nach Unterbrechung. Version 0.4.45→0.4.46: **nur 2/92 Dateien geändert** (Haupt-PHP und README), kein neues Modul. **Lokale Tests, keine bestätigte erfolgreiche Live-0.4.46-Installation**; die echte Liveversion war zuletzt 0.4.45 mit 512-MiB-Speicherabbruch.
- Hab 0.4.31.20 hat `miniSingleImport()`, `savedMiniDownload()`, `redownloadBatch()` bereits, **aber noch kein** `persistState()`, `streamOptionUpdate()` oder AJAX-Artikel-Einzelrequest. Der vorhandene `mutate()`-Weg ruft `update_option(self::OPTION,...)` und zweimal vollständiges `get_option` zum Vergleich auf; `TXE_Diagnose::stateChange()` erzeugt für den Änderungsbericht immer die JSON-Gesamtkopie des Bestands und hasht sie. Pferdeatelier reduziert diesen Diagnose-Schritt bei wenig Speicher. Die direkte Codeprüfung belegt diese **zusätzlichen Großdaten-Kopien**; ob sie auf Hab derzeit einen realen Speicherabbruch auslösen, ist ohne Hab-Live-Fehlerdaten **nicht** bewiesen.
- Hab-WordPress-Import läuft bislang alle Artikel des Batches im **einen** PHP-Request; Pferdeatelier 0.4.46 verarbeitet separat. Dies ist eine **konkrete technische Abweichung**, kein Beweis, dass eine kleine Hab-Charge scheitert. Änderungen daran nur als begrenzter Import-/Speicher-Patch **in derselben vorhandenen Plugin-Installation**, wenn ein echter Hab-Speicherfehler oder ein reproduzierter Testfall die Ursache belegt; keine vorsorgliche Übernahme aller Pferdeatelier-Dateien.

### 4. Konkrete, sichere Fortsetzung **nur an bestehender Anbindung**
1. Zuerst K-Multi bei echtem Hab-Import **nur** an seine vorhandenen zuständigen Fakten-, vollständigen Fach-QA- und vertrauenswürdigen Endfreigabe-Owner binden. Genau eine finale Datei erst, wenn der ORIGINAL-K-MULTI-Hab-Freigabenachweis real vorliegt. Keinen neuen Exportpfad bauen, keinen alten K0 aufrufen, keine Datei aus einem Probebericht erzeugen.
2. Unveränderte Hab-0.4.31.20-Quelle und gespeicherte Aufträge als Referenz sichern. Keine stillschweigende Plugin-Änderung oder Performance-Vollübernahme allein wegen des Versionsabstands. Falls echte Hab-Performance betroffen ist, nur den nachgewiesenen gemeinsamen Speicher-/Importaufruf im bestehenden Plugin minimal und geschlossen reparieren und alle Ursprungsfunktionen gegentesten.
3. Einen WordPress-Import ausschließlich nach echter K-Multi-Signatur, unveränderten Auftragsschlüsseln, vollständiger QA und Beweis der Entwurfsspeicherung wagen. Forschung-Abbruchknopf nur für Forschung ausgeben, nicht als K-Multi-Abbruch behaupten.

**In dieser Prüfung ausgeführt:** GitHub-Original-K0/K-Multi gelesen, echte bestehende ZIPs entpackt, Version-zu-Version- und Funktionsvergleich durchgeführt und dieses bestehende Büroprotokoll korrigiert. **Nicht ausgeführt:** Änderungen an K0-/K-Multi-Produktionscode, Artikelregeln oder WordPress-Plugin; keine Live-Publikation; keine neue Plugin-ZIP.

---

## Aktuellster verbindlicher Stand – 22.11.2026: 57/110 echte Hab-HARD-Prüfungen

**Dieser aktuelle Stand gilt vor allen nachfolgenden früheren Zwischenständen.**

- **Jüngster nachweislich erfolgreicher Original-K-Multi-Gesamtlauf:** https://github.com/hallo-netizen/k0-multiportal/actions/runs/45017972662 – **SUCCESS**.
- **Echte 110-HARD-Einzelprüfung pro Artikel:** **56** unterschiedliche kataloggebundene Original-Hab-Regeln im bestehenden K-Multi-Autoren-Owner technisch durchgeführt und bestanden, **eine** weitere echte unabhängige Sprachprüfung durch den bestehenden einzigen LT68-Owner nach Original-Artikel-HTML-Hash und nachgewiesenem gepinntem LanguageTool 6.8 gebunden. **Resultat 57 PASS / 0 FAIL / 53 NOT_EXECUTED je Artikel**. Vollständige 110/110-Freigabe weiterhin verboten.
- **262 technische Regressionstests bestanden:** 77 + 98 + 26 + 61. Darin 3 neue Positiv-/Negativtests zu wiederholtem Satz, gleichförmigem Überschriftenanfang und verbotener generischer Generatorphrase. Technische Tests **nicht** als zusätzlich abgenommene Original-HARD-Regeln zählen.
- **Echtes LanguageTool 6.8 für alle drei aktuellen und alle drei ursprünglichen Hab-Artikel:** zwei unabhängige Original-Owner-Läufe mit jeweils **[0,0,0] offenen Fehlern**. Kein neues Recherche- oder bezahltes Keywordtool.
- **Prüfbeleg wirklich in GitHub gespeichert:** GitHub-Actions-Artefakt `KMULTI-HAB-REAL-57-OF-110-HARD-RECEIPTS-NOT-IMPORT`; der anfängliche Fehler des alten Upload-Dateinamens wurde ursächlich berichtigt. Der neue Lauf bestätigt Upload **SUCCESS**, Artefakt-ID 14752706616; Inhalt ist eine **nicht importierbare** Prüfquittung, keine WordPress-Datei.
- **Artikelkorrekturen beibehalten:** 3 vollwertige Hab-Fachtexte mit jeweils einem Merksatz, Abholbox mit genau einem begründeten „Wichtig“-Kasten; nachweislich reparierte Absatz-, Listen-, Fazit-, Wortobergrenzen- und Abschnittslängenregeln. Abholbox 891 Wörter durch genau fünf entfernte Wiederholungssätze, Vergleich durch Umstellen einer vorhandenen Aussage ausbalanciert, keine neuen Tatsachen/Quellen erfunden.
- **Originale erhalten:** GitHub-Git-Blob-Vergleich der fünf Hab-Originalregelbücher plus ursprünglicher Drei-Artikel-JSON **6/6 byteidentisch**. Ursprüngliche fünf Felder, `plan_slot`, 12 verifizierte Quellenbelege/5 amtliche Seiten, 3 interne Links und 4 Quellenspuren je Artikel im separaten Autoren-Preflight nachgewiesen. Kein alter K0 aufgerufen.
- **Noch 53 unverrichtete Original-HARD-Regeln:** **25** inhaltlich/redaktionell und strukturell zu klären (**12 fachliche Quelle-/Behauptungsregeln, 3 redaktionelle Bedeutungsprüfungen, 2 Tabellenentscheidungen, 8 Artikel-/Link-/Kategorieprüfungen**); **28** in System-, Integritäts-, WordPress-Echtdarstellungs-, Signatur- und Veröffentlichungskontrolle. Eine automatisch grüne Typ-/Strukturprüfung ist **keine** Beurteilung der Wahrheit einer Gefahrenaussage.
- **Harte Freigabesicherung:** `full_hab_110_hard_rules_verified=false`, `semantic_fact_approval=false`, `publish_allowed=false`. Weder echte WP-Rendering-/Farbkontrolle noch eigenständige signierte Endfreigabe nachgewiesen, deshalb **KEINE verifizierte WordPress-Importdatei** und kein Publizieren.

**Nächster zuständiger Original-Arbeitsblock:** Die 25 ausstehenden inhaltlichen Artikel-Owner-Prüfungen nur soweit mit amtlichen Originalfakten und echtem semantischen Nachweis schließen; den realen WordPress-Echtrender und die nachgeschalteten 28 unabhängigen K-Multi-Integritäts-/Signaturprüfungen nicht durch Mocks ersetzen. Keine zweite Typentscheidung, keine neue bezahlte Recherche und kein neues WordPress-Plugin.

**Belegquellen:**
[GitHub-Gesamtlauf 45017972662](https://github.com/hallo-netizen/k0-multiportal/actions/runs/45017972662),
[57/110-Safe-Gate K-Multi-Code](https://github.com/hallo-netizen/k0-multiportal/blob/k0-offline-rule-bindings-20261027/offline_writer_dev/kmulti_authoring_station.py),
[Original-LT68-Owner](https://github.com/hallo-netizen/k0-multiportal/blob/k0-offline-rule-bindings-20261027/offline_writer_dev/hobby_trial/kmulti_lt68.py),
[3 unreleased Hab-Fachbeiträge](https://github.com/hallo-netizen/k0-multiportal/blob/k0-offline-rule-bindings-20261027/offline_writer_dev/portal_auto/hab_current/hab_3_editorial_safety_style_CANDIDATE_NOT_RELEASED.json).

---





## Verbindlicher technischer Anschlussstand – 22.11.2026, Fortsetzung nach dem Ersttest

**Dieser Abschnitt hat Vorrang gegenüber älteren, unten weiterhin als Historie erhaltenen Zwischenständen.**

1. **Merksatz-Pflicht aktiv beim bestehenden Original-K-Multi-Autoren-Owner** für die gegenwärtigen vollwertigen Hab-Fachartikel: Ohne Merksatz wird der aktuelle Originalautoren-Preflight standardmäßig abgewiesen. Die unveränderte alte 3er-Datei dient ausdrücklich nur als historische Kontrollreferenz mit bewusst ausgeschaltetem neuen Stilcheck. Die **separate überarbeitete 3er-Datei** besteht den Standardcheck mit exakt drei Merksätzen und einem thematisch begründeten „Wichtig“-Hinweis. Die bisherigen fünf Fachregelbücher und der Original-K0 wurden nicht geändert. Noch keine pauschale FAQ- oder Berichts-Pflicht – die fachlich vorgesehenen Ausnahmen bleiben getrennt zu prüfen.
2. **Quellenprüfung konkret weitergeführt:** Die 12 bereits bestehenden Textbelege aus den fünf amtlichen Original-Quellenseiten wurden anhand der öffentlich lesbaren Originalseiten im Zusammenhang überprüft. Die neue, gesondert dokumentierte **Kontextprüfung** ist innerhalb des bestehenden Original-Quellen-Owners mit allen 12 ursprünglichen Faktenkennungen, Aussagen, URLs und Original-Auszügen verbunden; 10 Negativ-/Positivtests schützen gegen stilles Austauschen und falsche Vollfreigaben. **Keine** erneute Keyword-/Quellenrecherche in GitHub Actions, keine neue bezahlte API-Abfrage. Vollständige fachliche Freigabe **aller Aussagen der Artikel bleibt weiterhin offen**.
3. **Echter Original-GitHub-Actions-Lauf:** https://github.com/hallo-netizen/k0-multiportal/actions/runs/45010584262 – **SUCCESS**, 69 + 98 + 26 + 53 = **246 technische Tests bestanden**, nicht als 110-Hab-Regelprüfungen ausgegeben. LanguageTool 6.8 **auf den drei Original- und den drei ergänzten Texten jeweils [0,0,0] offene Sprachfehler**.
4. **Gesamtprüfung korrigiert:** Das ursprüngliche K-Multi-Gesamtprotokoll erkennt jetzt tatsächlich **drei geschriebene Artikel**, den vorgeschriebenen Merksatz und die **12 geprüften Quellenbelege aus fünf amtlichen Quellen**. Die ältere Anzeige „NOT_RUN_NO_ARTICLES“ ist als sachlich veraltet ersetzt. K-Multi bleibt ausdrücklich gesperrt, solange die originale vollständige **110-HARD-Prüfung**, alle Artikel-Fakten, die WordPress-Rendering-/Integritätsprüfung und die unabhängige signierte Release-Autorität nicht vollständig bestanden sind.
5. **Erhalt nachgewiesen:** Alle fünf ursprünglichen Hab-Regelbücher und die Original-3er-Artikeldatei waren nach dem Test in GitHub **6/6 byteidentisch** zu ihren vorher festgehaltenen Git-Blob-Werten. Keine WordPress-Inbetriebnahme, kein neues Plugin, kein freigegebener Import.

**Künftiger Arbeitsfokus:** fehlende ursprüngliche vollständige 110-HARD-Fach- und Artikel-Endkontrolle im selben Original-K-Multi schließen; valide Tatsache/Quelle nachweisen; Layout der bestehenden Hab-Warn-/Merksatz-Boxen am echten WordPress-Frontend prüfen, erst danach Signatur und Import. Keine Behauptung einer bereits erfolgten K-Multi-Gesamtfreigabe.

**Nachweise:** [Original-GitHub-Testlauf](https://github.com/hallo-netizen/k0-multiportal/actions/runs/45010584262) · [Quellenkontext 12/12 mit Sperre](https://github.com/hallo-netizen/k0-multiportal/blob/k0-offline-rule-bindings-20261027/offline_writer_dev/portal_auto/hab_current/HAB_12_CLAIMS_OFFICIAL_CONTEXT_REVIEW_PARTIAL_20261122.json) · [aktuelle Hab-Ausgangs- und Textprüfung](https://github.com/hallo-netizen/k0-multiportal/blob/k0-offline-rule-bindings-20261027/offline_writer_dev/portal_auto/kmulti_hab_fullchain_audit.py)

---


**Datum:** 22.11.2026  
**Status:** GESTALTUNGS- UND SPRACHTEST BESTANDEN – KEINE FACHLICHE ENDABNAHME / KEIN IMPORT

## Redaktionelle Grundlage
Siehe `HAB_GEFAHR_SCHUTZ_ZUSATZREGELN_FUENF_BEITRAGSARTEN_20261122.md` im selben Konzeptbüro sowie den ursprünglichen CO-Melder-Nacharbeitsentwurf.

## Tatsächliche Umsetzung
- Im **Original-K-Multi** (nicht im alten K0) wurde die bestehende Autorenprüfung um die Zusatzformat-Prüfung für **Merksatz** und **Wichtig/Achtung** erweitert. Die Funktion ist bewusst opt-in, damit nicht freigegebene neue Konzeptregeln die ursprünglichen Artikel stillschweigend blockieren.
- **Drei** vorhandene Hab-Artikel haben eine separate, noch nicht freigegebene Probeversion. Jeder besitzt **genau einen** Merksatz. Der Abholbox-Artikel zusätzlich einen ausdrücklich auf verlorene/offengelegte Codes bezogenen Warnkasten. Keine Warnkästen in den beiden Kamerabeiträgen ohne konkrete handlungsbezogene Gefahr.
- Die Aussagen stammen aus den vorhandenen Artikeln; es wurden keine neuen Tatsachen formuliert. Die bisherigen Originale, alle fünf Fachregelbücher, Original-IDs, Fünffelder, Quellenmarker, Links und Überschriften sind erhalten.
- **Echter GitHub-K-Multi-Testlauf 45009404608 erfolgreich:** **234 technische Prüfungen**; echtes LanguageTool 6.8 auf den drei Original- und auf den drei überarbeiteten Artikeln je **0/0/0 offene Sprachfehler**.
- Die eigentliche visuelle Darstellung in WordPress ist noch **nicht** geprüft. Bereits bekannte Frontend-Vorlage: orange/beige „Wichtig“-Box nach Hero, salbei-grüner „Merksatz“-Kasten, dreiteilige Alarm-Checkliste im CO-Melder-Beitrag. Kein neues WordPress-Plugin.
- **Weiterhin ungeprüft:** tatsächliche semantische Wahrheit jeder Quelle/Sicherheitsbehauptung; vollständige 110 Hab-HARD-Regeln; finale WordPress-Echtdarstellung und signierter K-Multi-Reimport. Keine Veröffentlichung, keine Importdatei.

## Einheitliche Nachweise
- GitHub-Actions-Lauf: https://github.com/hallo-netizen/k0-multiportal/actions/runs/45009404608
- Ausführliches Original-K-Multi-Prüfprotokoll: https://github.com/hallo-netizen/k0-multiportal/blob/k0-offline-rule-bindings-20261027/offline_writer_dev/QA_HAB_GEFAHR_SCHUTZ_3_ARTIKEL_WIRKLICHER_LT68_TEST_20261122.md
- Nicht freigegebene, verifizierte 3er-Artikelprobe: https://github.com/hallo-netizen/k0-multiportal/blob/k0-offline-rule-bindings-20261027/offline_writer_dev/portal_auto/hab_current/hab_3_editorial_safety_style_CANDIDATE_NOT_RELEASED.json

**Nächste fachliche Entscheidung:** Redaktioneller Merksatzstandard/selektiver Gefahrenhinweis und Sonderfall Mehrfragen-FAQ eindeutig freigeben oder anpassen. Anschließend bei bestehendem Regel-Owner aktivieren und ursprüngliche QA-Endprüfungen fortsetzen.
