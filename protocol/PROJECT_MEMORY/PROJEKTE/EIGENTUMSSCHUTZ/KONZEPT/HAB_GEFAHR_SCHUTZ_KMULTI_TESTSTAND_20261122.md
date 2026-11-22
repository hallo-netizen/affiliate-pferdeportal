# Hab & Bewahr – Gefahr & Schutz: praktischer K-Multi-Teststand

## Aktuellster Original-K-Multi-Stand am 22.11.2026 – tatsächlich ausgeführter 110-Regel-Ausschnitt

**Dieser Abschnitt hat Vorrang vor unten stehenden älteren Testzahlen (223/234/246) und veralteten „0 von 110“-Meldungen.**

- **GitHub-Gesamttest:** https://github.com/hallo-netizen/k0-multiportal/actions/runs/45016997529 — **SUCCESS**.
- **Technische Tests:** **251 bestanden** (74 + 98 + 26 + 53). Unabhängige echte LanguageTool-6.8-Prüfung auf den drei ursprünglichen und den drei überarbeiteten Hab-Texten jeweils **[0,0,0] ungelöste Sprachfehler**.
- **Echter Original-Hab-Regelkatalog:** 110 HARD-Regel-IDs pro Artikel, davon **49 pro Artikel im bestehenden originalen K-Multi-Autoren-Owner tatsächlich ausgeführt und PASS**, **0 FAIL**, **61 explizit NOT_EXECUTED**. Die noch offenen 61 Regeln werden nicht als bestanden ausgegeben. Der jeweils vollständige 110-Regel-Bericht ist im GitHub-Actions-Artefakt `KMULTI-HAB-THREE-ORIGINAL-FULLCHAIN-RECEIPT-NOT-IMPORT` sowie im bestehenden K-Multi-Gesamtaudit enthalten. Die 251 technischen Unit-Tests sind **nicht** 251 Artikel-Regelprüfungen.
- **Tatsächlich gelöste alte HARD-Probleme:** Absatz-Untergrenze, mindestens vier Punkte in einer Liste, zwei Fazit-Absätze, absolute Wortobergrenze und ausgewogene Länge der Hauptabschnitte. Gegenprobe über Positiv-/Negativtests. Die drei aktuellen Testfassungen erfüllen alle 49 jetzt ausgeführten Regeln. Bereits vorhandene Merksatz- und Warnkastenprüfung integriert.
- **Gezielte Texterhaltung:** Abholbox-Fassung auf **891 Wörter** (gegenüber vorher 943) durch Entfernen genau fünf repetitiver Sätze, ohne neue Fakten; im Kameravergleich wurde genau eine vorhandene Aussage in den passenden Abschnitt verschoben. Der dritte Artikel unverändert gegenüber der vorherigen Merksatz-Testfassung. Links, Original-Fünffelder, `plan_slot`, Quelle-Faktenkennungen, 4 Quellenspuren je Artikel sowie Überschriften und Tabellen vorhanden.
- **6/6 Originale bytegleich geblieben:** Alle fünf vorhandenen Hab-Regelbücher und `hab_3_original_authored_drafts_NOT_RELEASED.json` mit den vorher dokumentierten Git-Blob-Werten abgeglichen und unverändert. Original-K0 nicht aufgerufen, kein neues WordPress-Plugin, keine kostenpflichtige neue Recherche.
- **Original-Quellenprüfung:** 12 konkrete Belege aus fünf amtlichen Quellenseiten vorhanden und im Original-Quellen-Owner inhaltlich abgeglichen, keine Vollfreigabe aller Artikelbehauptungen.
- **Sperren ausdrücklich aktiv:** `semantic_fact_approval=false`, vollständige **110/110**-Fachprüfung nicht erbracht, kein WordPress-Frontend-Rendering nachgewiesen, keine signierte unabhängige K-Multi-Release-Freigabe und keine importierbare WordPress-Datei. K-Multi meldet **publish_allowed=false**.
- **Weiterer zulässiger Arbeitsweg:** Die noch **61 nicht ausgeführten Original-HARD-Regeln** nach bestehendem Owner (insbesondere Artikel-Fakten/semantische Prüfung, Links/WordPress-Verifikation, Endintegrität und Signatur) einzeln schließen. Fehlende Beweise dürfen nicht durch synthetische PASS-Quittungen ersetzt werden. Vorhandene Warn-/Merksatz-Boxen erst bei echtem WordPress-Rendering als fertig bezeichnen.

**Beweispfade:**
https://github.com/hallo-netizen/k0-multiportal/blob/k0-offline-rule-bindings-20261027/offline_writer_dev/kmulti_authoring_station.py

https://github.com/hallo-netizen/k0-multiportal/blob/k0-offline-rule-bindings-20261027/offline_writer_dev/portal_auto/kmulti_hab_fullchain_audit.py

https://github.com/hallo-netizen/k0-multiportal/blob/k0-offline-rule-bindings-20261027/offline_writer_dev/portal_auto/hab_current/hab_3_editorial_safety_style_CANDIDATE_NOT_RELEASED.json

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
