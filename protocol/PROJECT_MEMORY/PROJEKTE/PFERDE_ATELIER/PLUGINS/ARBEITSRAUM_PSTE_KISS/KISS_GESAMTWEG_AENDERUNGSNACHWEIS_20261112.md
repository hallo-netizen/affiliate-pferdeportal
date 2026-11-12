# Pferde Atelier – KISS-Gesamtweg: bewiesener Soll-/Iststand und Ablaufprobe
12.11.2026. **Einziger Ausgangsstand:** privates ZIP `AKTUELLER_ARBEITSSTAND_TESTIDENTISCH_NICHT_INSTALLIEREN.zip`, SHA-256 `8fc55bca1fc7e4fe019203b2c56d169a734f0c3c941b08606fa9bed6b9183e33`. Die Originalplugins sind PSTE .45 und PSERC .69. Im bestehenden QA-Stand sind **genau zwei** vorher nachgewiesene Stellen geändert (PSTE `class-pste-repository.php`, PSERC `class-pserc-plan-dependency-fingerprint.php`); **in dieser Fortsetzung keine weitere Plugin-Datei geändert**.

## Endgültiger, vom Nutzer bestätigter Zielvertrag
1. **PSTE Keyword-Recherche:** liefert neue Stichwörter und Bestandsdaten.
2. **Eine zentrale Entscheidung VOR MINI:** Portalrelevanz JA/NEIN/VIELLEICHT, Thema FREI/BELEGT/KLÄRUNG, **Suchabsicht**, Kategorie, Artikelart; ganzer bestehender Inhalt/Plan und andere neue Themen berücksichtigt. Gleiche Suchabsicht: ein Artikel. Wirklich andere belegte Suchabsicht: eigener Artikel möglich. Kein künstlicher zweiter Artikel durch neues Fragezeichen / Beratungs-Label.
3. **Einmalig und dauerhaft reservierter Artikelplatz VOR MINI:** bestehende technische Slotverwaltung verwenden, keine neue Tabelle und keine neue inhaltliche Prüfstelle.
4. **MINI außerhalb WordPress:** ausschließlich Titel für genau das bereits freigegebene Thema; ändert nicht Suchabsicht, Art, Kategorie oder Artikelplatz.
5. **Externer Titelprüfer:** nur Titel/Sprache, ggf. Korrektur derselben Titelaufgabe.
6. **PSERC Redaktionsplan:** fertigen Auftrag übernehmen, **genau fünf** Felder an K0; kein zweites SEO-/Dublettenurteil.
7. **K0 Writer:** Artikel schreiben, Sprache, Fakten, Links und geltende Content-QA; nicht noch einmal entscheiden, welches Thema freigegeben ist.
8. **WordPress Re-Import:** richtigen fertigen Entwurf am gespeicherten Platz einlesen, Plan-/PPM-Status aktualisieren. Kein neues SEO-Urteil.

## Originalcode: konträre Iststellen mit Ort und Änderungsbedarf
| Festgestellte Iststelle am aktuellen ZIP | Beweis | Bestehende Aufgabe, die angepasst werden muss |
| --- | --- | --- |
| MINI exportiert rohe, nicht zuvor endgültig freigegebene Keywords | `PSTE_Mini_Workflow::selectNewRows` und `createBatch` | Nur feststehende, gebundene Aufträge an Titelworker weitergeben |
| MINI-Batch enthält JA/NEIN/VIELLEICHT-Worker und erlaubt mehrere Intentionen/Titel | `PSTE_Mini_Workflow::createBatch`, `validateResult`; vorhandene Originaltests 6/6 | Diesen Arbeitsschritt an die zentrale **Vorentscheidung** zurückbinden; MINI nur Titel |
| Spätere SEO-FREI/BELEGT-Auswertung nach Titelrunde | `PSTE_Mini_Workflow::exportResults`, `forwardToPlan`; `PSTE_MINI_RESULTS_FOR_EDITORIAL_V1` | Zentrale Entscheidung abschließen VOR MINI; nicht zweite SEO-Stelle nachgeschaltet behalten |
| Die bestehende Stapelvergleichsfunktion benutzt zusätzlich Titeltexte | `PSTE_Runner::sameAnswerIntentSignature` / `duplicateSignature` | Einmalig vor MINI nach Suchfrage + tatsächlicher Suchabsicht entscheiden; **bestehenden sinnvollen Dublettenschutz nicht abschalten** |
| Platzvergabe erfolgt später im PSERC-Kompilierlauf | `PSERC_Plan_Compile_Job::tickSlot` | Bestehende Platzvergabe/PPM-Reservierung vor MINI verbindlich abschließen; gleichzeitige Buchungen nicht allein durch bloßes `allocate` absichern |
| Normaler PSERC-Weg trifft noch zweites semantisches Urteil | `PSERC_Compiler::compile`, `PSERC_Plan_Compile_Job::tickCandidate`, Originalmethoden-Gegenprobe | Nur das **endgültige** upstream-Urteil weitergeben; später nicht neu bewerten. Nicht ungesichert die Checker ausknipsen wie in verworfener QA .70 |
| Gleiche Rohfrage mit anderer Suchabsicht erhält denselben **PSTE-Themen-Schlüssel** | Originalmethode `PSTE_Repository::normalizedKeyForCandidate`, Test `PRUEFE_GLEICHES_KEYWORD_VERSCHIEDENE_ABSICHT.php` = `same_storage_topic_key=true` | Vor einer Änderung **bestehende Varianten-/Occurrence-/Intentzuordnung prüfen**, ob zwei eigenständige Artikelaufträge sauber möglich sind. **Nicht** pauschal den Themen-Schlüssel umbauen (Migration, Altbestand). |
| K0 fünf Metadaten und WP Re-Import sind bereits vorhanden | `PSERC_Metadata_Boundary::validateBatch`, `PSERC_System4_Import::importPayload` | **Nicht neu bauen**, unverändert erhalten; echtes WordPress/K0-Testing noch offen. |

## Wirklich ausgeführte QA und Grenzen
- Ursprungs-PSTEs 121/121 Dateien, PSERC 63/63, nur zwei alte QA-Codeabweichungen; **83+43 PHP-Syntaxchecks PASS**, 5 bestehende Originalmethoden-Testgruppen PASS.
- Eigene, neue **Sollreihenfolge-Simulation** in `SIMULIERE_SOLL_WORKFLOW.php`: **18/18 PASS**. Der echte PSERC-Platzverteiler wählt zwei verschiedene Plätze und beim simulierten gespeicherten PPM-Zustand den dritten; echter PSERC-Fünffeld-Validator verwirft denselben Platz / unerlaubte weitere Felder; echter PSERC-WP-Importer schreibt **zwei Mock-Entwürfe** und ruft eine **nachgebildete PPM-Planverbuchung** auf. Falsche Importzuordnung abgelehnt.
- Separater Originalmethodentest `PRUEFE_GLEICHES_KEYWORD_VERSCHIEDENE_ABSICHT.php`: **PASS – beide verschiedenen Absichten zur gleichen Rohfrage ergeben denselben globalen PSTE-Themenschlüssel**. Dies beweist nur die Schlüsselberechnung, **nicht** das spätere Schicksal zweier Article-Intent-Occurrences in echtem WordPress.
- **NICHT simuliert/ausgeführt:** tatsächliche DataForSEO-Anfrage, echte zentrale SEO-Entscheidung für neue Keywords, sicherer dauerhafter **WordPress-übergreifender** Slot-Commit vor MINI, tatsächlicher externer MINI-Titelworker samt LanguageTool, K0 Writer samt Sprach-/Fakten-/Linkprüfung, echte WordPress-Datenbank, wirklicher WordPress-Re-Import. Diese Schritte sind **nur festgelegte Fixture-Aufgaben**, **keine bestandene E2E-Abnahme**.
- **Keine Plugin-Modifikation, kein ZIP-Installer, keine Live- oder Test-WordPress-Schreibaktion.** Die 18/18 PASS beweisen die Machbarkeit der gezeigten Funktionsverknüpfung in einer nachgebildeten Umgebung, **nicht** dass das Original-Plugin bereits entsprechend umgestellt ist.

## KISS-Fazit – nächster tatsächlicher Umsetzungsschnitt
**Die bestehende zentrale Themenentscheidung, Vorab-Reservierung und Titelübergabe müssen in den vorhandenen Funktionen zu EINER lückenlosen Auftragskette werden.** Ohne Zugriff auf den tatsächlichen persistierten PPM-Reservierungsbesitzer und ohne echten integrierten WordPress-TEST lässt sich ein sicherer abschließender Source-Patch nicht nachweisen: ein angeblich fertiger ZIP-Umbau allein wäre riskant und würde den verbindlichen Nachweispflichten widersprechen.

**Nicht erneut anfassen:** Die bereits erfolgreich getesteten zwei alten lokalen Korrekturen, den MINI-Einzelfehler-Weiterlauf, K0-Schreibqualität und den vorhandenen Re-Import. **Keine** zweite SEO-/Kategorie-/Titel-Entscheiderklasse, keine neuen Datenbanken oder Workarounds.