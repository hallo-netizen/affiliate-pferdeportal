# Hab & Bewahr – Gefahr & Schutz: praktischer K-Multi-Teststand

## Nur-Anbindung-Abgleich mit dem aktuellsten Pferdeatelier-K0 und Textplugin – 22.11.2026

**Prüfung, keine Code-/Plugin-/Regeländerung.** Dieser Quellenvergleich ergänzt den letzten nachgewiesenen Hab-K-Multi-Stand 57/110, ohne ihn freizugeben. Quellen: aktuellster K0-Zweig in GitHub, archivierte originale Plugin-ZIP 0.4.46, geprüfte originale Hab-ZIP 0.4.31.20 und Büroprotokolle.

1. **Echte Pferdeatelier-K0-Autorität ist NICHT `main`:** `hallo-netizen/affiliate-pferdeportal`, Branch `konzept0-portal-neutral-20261002` (22.11.2026 letzter verifizierter Writer-Single-Commit `00b79716f33d64cbe7fde0dbae0f355eacfeeaab`; erfolgreicher Workflow `45008261702`). Original-K0 bleibt ein eigener Lauf und darf aus Hab-/K-Multi-Dateien **nicht aufgerufen oder kopiert** werden.
2. **K0-Original-Eingang:** `WP_K0_UPLOAD_PACKAGE_V1` mit `word_press_order_receipt` und eingefrorenem `k0_intake` (fünf Felder). Die bestehende K0-Eingangsfunktion erstellt daraus ihre eigenen Standarddateien, ohne zusätzliches altes PSERC-Manifest vom Nutzer. Keine zweite Keyword-/Intent-/Typentscheidung; gleicher Writer-Job beim Reparaturrücklauf und unveränderter Wiederaufnahme. Pro Originalartikel echte Vollprüfungen, LanguageTool 6.8, Canonical-ID und `SYSTEM4_WORDPRESS_HANDOFF_V1`. Die originalen Einzelergebnisse werden in ursprünglicher Auftragsreihenfolge als `WORDPRESS_BATCH.json` vereinigt. `publish_allowed=false`.
3. **WICHTIG: K0-Artikelregeln nicht nach Hab übertragen.** Neuere K0-Regeln vom 19.–21.11.: 1–3 sinnvolle Links (Elternlink Pflicht; optionale Links nur mit thematischem Beleg), Tabellen in FAQ/Beratung/Pflege nur bei wirklichem Nutzen, Vergleich mit sinnvoller Tabelle. Die bestehenden Hab-Fachbücher und der aktuelle 57/110-Hab-Owner verlangen für die drei Testtexte bisher drei Linkrollen und eine Tabelle. Diese Unterschiede sind **getrennte Fachregeln, kein verbindlicher Anlass für K-Multi-Umbau oder stillen Regeltransfer**. Prüfen nur am zuständigen Hab-Regelowner, falls der Nutzer redaktionell eine Änderung beschließt.
4. **Pferdeatelier Texterstellung aktuellste Büro-ZIP 0.4.46** (22.11., `Texterstellung-0.4.46-MINI-UND-K0-SPEICHERWEG.zip`, geprüfte SHA256 `2358975027ecb5b30bcd923014a4c24c086688f6d220f07c648cc4b0d3991fd2`, 92 Dateien / 79 PHP). Letzte **echt nachgewiesene Live-Version nur 0.4.45**, die beim 15er-MINI-Import unter 512 MiB mit `PHP_MEMORY_EXHAUSTED` abbrach. 0.4.46 hat einen **lokal untersuchten** persistierenden Speicherweg; 90/92 Dateien bytegleich zu 0.4.45, neue ZIP auf Live **nicht** nachgewiesen.
5. **Hab-&-Bewahr-Textplugin letzter Kandidat 0.4.31.20** (original ZIP `Texterstellung_HAB_UND_BEWAHR_0.4.31.20_MINI_EINMALREIMPORT_PFERDEATELIER.zip`, SHA256 `404090884e80ade8d963859395ebaa5271f062199889d0a955cbfb0f6adc49e7`, 87 Dateien / 78 PHP; letzter Live-Installationsstatus offen). Die echte `miniSingleImport`-Funktion wurde in dieser Version aus Pferdeatelier 0.4.39 übernommen, **ein einziges MINI-Freigabe-JSON** statt drei Zwischenimporte; 3/3 lokaler Funktionstest inklusive idempotenter Wiederholung und Mutationstest PASS, **kein Live-Beweis**.
6. **Beide echten ZIP-Codes direkt gegengeprüft:** Beide erkennen `MINI_SINGLE_FILE_REIMPORT_V1` für die vorgelagerte MINI-Auftragsdatei und `PFERDE_ATELIER_WORDPRESS_IMPORT_V1` sowie `SYSTEM4_WORDPRESS_HANDOFF_V1` bei der späteren WordPress-Entwurfsübernahme. **Damit existiert der benötigte technische Vertragsanschluss bereits; keine neue Schnittstelle/Architektur nötig.** Die althergebrachte Zeichenfolge `PFERDE_ATELIER_...` bezeichnet den gemeinsamen historischen Transportvertrag, *nicht* das Zielportal.
7. **Echte Differenz nur im WordPress-Speicher-/Rückimportweg:** Pferdeatelier 0.4.46 besitzt die schon vorhandenen `ajaxImportDraftOne` / `ajaxFinalizeDraftOne`, separates `txe-staged-import.js`, wiederaufnehmbaren Import **ein Artikel pro Serveraufruf**, gesonderte Statusspeicherung und `streamOptionUpdate`. Das Hab-Paket 0.4.31.20 besitzt diese späteren Techniken **nicht**, sondern nutzt seinen eigenen vorhandenen `importDraftsIndividually`-Aufruf in einem PHP-Request. **Kein Beweis**, dass Hab bei drei Artikeln deshalb scheitert; Pferde-Fix **nicht** pauschal portieren und kein neues Plugin. Bei echtem Hab-Importfehler die konkrete Ursache messen und nur an bestehender zuständiger Stelle reparieren.
8. **Wiederaufruf / Abbruch richtig zuordnen:** Pferdeatelier hat gespeicherte MINI-/K0-Aufträge und gezielten Wiederdownload, bestehenden `research_stop` nur für eigene Recherche, GitHub-K0-Writer-Retries mit unveränderter Original-ID. **Kein Beweis**, dass ein WordPress-Forschungstopp einen GitHub-K0-/K-Multi-Lauf abbricht. K-Multi hat unabhängig schon `kmulti_current_upload.py` (nur frischer Upload), `kmulti_safe_delivery.py` (alte Ausgabe löschen, neue finale JSON nur nach echtem signierten QA-Zertifikat, atomar, `publish_allowed=false`). Diese Sicherheitsgrenzen bleiben.
9. **Konkrete Anbindung, keine Neuanlage:** Nur gültigen aktuellen WordPress-Hab-Eingang an die **bestehende** K-Multi-Portal-/Owner-Weiche, genau die bestehende Hab-110-Regelkette und unabhängige LanguageTool-/Endprüf-Quittungen, dann **dieselbe** finale sichere Ein-Datei-Ausgabe (`KMULTI_WORDPRESS_IMPORT.json`), die den **schon unterstützten** ursprünglichen WordPress-Importer-Vertrag erfüllt. **Nicht** das MINI-Freigabehash als unabhängige K-Multi-Artikel-Signatur missverstehen. Vor echtem K-Multi-Import müssen die noch **53 ungeprüften Hab-HARD-Regeln**, semantische Fakten, WordPress-Echtdarstellung und unabhängiger vertrauenswürdiger Signaturbeleg vorhanden sein.

**Quellen und Nachweise:** [K0 aktuell](https://github.com/hallo-netizen/affiliate-pferdeportal/blob/konzept0-portal-neutral-20261002/K0_CURRENT_STATE.json) · [K0 letzte erfolgreiche Originalwriter-Action](https://github.com/hallo-netizen/affiliate-pferdeportal/actions/runs/45008261702) · [K-Multi sichere Ausgabe](https://github.com/hallo-netizen/k0-multiportal/blob/k0-offline-rule-bindings-20261027/offline_writer_dev/hobby_trial/kmulti_safe_delivery.py) · [K-Multi 57/110 erfolgreich](https://github.com/hallo-netizen/k0-multiportal/actions/runs/45017972662).

**Dieser Abgleich hat ausschließlich vorhandene Protokolle erweitert.** Keine Änderung an K0, K-Multi-Stationen, fünf Hab-Regelbüchern, Plugin-ZIPs, WordPress-Livebestand oder externen Startbefehlen.

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
