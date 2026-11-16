# K0 Quellen-KISS: Gesamtstand und Leitinstallations-Test
Stand 16.11.2026 – Prüfung der Originaldateien, Commits und GitHub-Actions-Läufe

## Verbindlicher Stand
- Hauptvertrag: `K0_START_HERE.md`, `K0_CURRENT_STATE.json`, `K0_GOAL_CONTRACT.json`. `K0:start` beginnt mit dem gültigen Upload; keine alternative Route, keine Zwischenmeldungen, `publish_allowed=false`.
- K0 verwendet den bestehenden Autor/Writer, die vollständigen 81 Artikelregeln, echtes LanguageTool 6.8, PPM 6.7.9 (unveränderte 104 Vergleichsregeln) und den unveränderten WordPress-Übergabevertrag. Anleitung ist ein eigenes READY-Regelfach (`ARTIKELTYPEN/Anleitung.json`), keine Umdeutung von Kategorienamen.
- Am 16.11.2026 lief die Wassertrog-Anleitung durch die echten K0-Schreib-, Prüf-, LanguageTool- und WordPress-Exportstationen, Lauf https://github.com/hallo-netizen/affiliate-pferdeportal/actions/runs/43871374652. Dennoch **keine endgültige fachliche Quellenfreigabe**: Alle 7 Angaben enthielten als angebliches Quellzitat genau denselben Text wie die selbst formulierte Aussage. Es gab keinen unabhängigen Originaltextnachweis.
- Die Quellenanzeige-Änderung vom 15.11. betrifft unsichtbare Quellenmarker/natürliche Namen im Text; beim Vergleich mit älterem Code wurde keine Änderung der URL- oder Originalquellenkontrolle festgestellt. Dass die neue Regel das Rechercheverhalten verursacht hat, ist nicht bewiesen. Ein früherer Artikel (Horseware am 15.11. nach Änderung) führte 8 getrennte Belegtexte.
- Die neue KISS-Regel arbeitet **an einer Stelle direkt am vorhandenen K0-Rechercheeingang vor dem Writer**: identische/leere Belege oder inkonsistenter eingetragener Text-Fingerabdruck führen zu `REPAIR_REQUIRED` beim `SAME_RESEARCH_OWNER`. Keinerlei neue Prüfstation. Bei reparierter `AUTHORING_CONTEXT.json` derselbe Auftrag/dieselbe Artikelidentität, danach normaler Writer. Das Workflow-Protokoll legt eine `RESEARCH_RETURN.json` im selben K0-Lauf an, statt einen fehlerhaften Writer-Job zu starten.
- Code: `engine/k0_writer_station.py`, `.github/workflows/k0-authoring-context.yml`, Test `tests/test_k0_research_owner_original_data.py`. Änderungen: https://github.com/hallo-netizen/affiliate-pferdeportal/commit/a61e27b0df42f5d6aca535e17397eea140ad985d und https://github.com/hallo-netizen/affiliate-pferdeportal/commit/ed745e46fe2bc9fbb5de064fd15db32fa79c5433.

## Belegter Teststand
- ORIGINAL-Daten positiv: Horseware, 8 voneinander verschiedene Quellentexte -> normaler K0-Writer-Job.
- ORIGINAL-Daten negativ: Wassertrog, 7 identische Pseudobelege -> alle 7 erkannt, `REPAIR_REQUIRED` zur selben Recherche, kein fehlerhafter Writer-Job.
- Reparatur-Test: Horseware-Beleg manipuliert -> Rückgabe; ursprünglichen getrennten Beleg im selben Lauf wiederhergestellt -> normaler Writer-Job. Manipulierter Text-Fingerabdruck -> Rückgabe.
- Gesamter K0-Selbsttest auf GitHub **180/180 bestanden**, 9/9 Portaltests, PPM-Parität und K0-Start-Sperren ebenfalls grün: https://github.com/hallo-netizen/affiliate-pferdeportal/actions/runs/43882495345
- **Wichtig:** Das ist eine bestandene lokale/Workflow-Simulation mit Originaldaten, **keine** WordPress-Live-Abnahme. Der neue K0-Belegcheck beweist nicht per externem Abruf, dass ein angebliches Zitat wirklich auf der Originalwebseite steht. Der GitHub-Workflow speichert eine Rückgabe, führt die erneute Recherche aber **nicht selbstständig** aus. Deshalb keine falsche Behauptung von vollständiger Quellenverifikation oder autonomer Reparatur.

## Leitinstallation / Texterstellung
- **oliver-beil.de** ist die bestehende Test-/Leitinstallation. Produktionsdomain pferde-atelier.de nicht ändern.
- Letzter sicher belegter installierter Stand Texterstellung: **0.4.22**. Bereitliegendes Upgrade **0.4.23** ist lokal geprüft, **noch nicht als installiert bestätigt**: `Texterstellung_KISS_0.4.23_TEST_MINI_Anleitung_K0_KISS.zip`, SHA256 `c2b5b8f8921cf783da87a28f525ec81b99888277fbe9929a0f8ffccdd659a3ab`. Das ZIP ist intakt (88 Dateien). Siehe `protocol/TEXTERSTELLUNG_MINI_ANLEITUNG_0423_TEST_20261116.md`.
- Korrigierter MINI-CATEGORY-Checkpoint `texterstellung-mini-category-korrigiert-anleitung.json` liegt bereit: Kategorie `wassertroege-fuer-weiden-installation` bleibt erhalten, die K0-Schreibart ist **Anleitung**, nicht `Installation`. Eine einzige Entscheidung im vorhandenen CATEGORY-Besitzer. Titel, Keyword, Kategorie und Slot unverändert.
- **Kein bestätigter echter WordPress-Entwurfsimport** mit 0.4.23. Der alte Wassertrog-Export wurde vor der neuen Quellen-Eingangsregel erzeugt und ist kein endgültiger Nachweis.

## Einmaliger sinnvoller Realtest, keine zusätzlichen Testschleifen
1. Backup von oliver-beil.de; das bereits geprüfte Texterstellung-Plugin **0.4.23 über die vorhandene Installation aktualisieren**, nicht löschen.
2. Den korrigierten CATEGORY-Checkpoint **einmal** im bestehenden MINI-Import übernehmen. In der bestehenden Ansicht muss `Anleitung` bei unveränderten übrigen fünf Auftragseigenschaften erscheinen.
3. Den **neuen K0-Export** der Testseite für genau diesen Auftrag ausgeben und mit `K0:start` bearbeiten. Quellenbelege werden am selben Rechercheeingang bei Fehlern an denselben Rechercheverantwortlichen zur echten Beschaffung/Korrektur zurückgegeben, dann regulärer Writer, 81 Regeln, echtes LanguageTool 6.8, WordPress-Ausgabe.
4. **Einen WordPress-Testentwurf** importieren und den tatsächlichen Entwurf einmal prüfen: korrekter Titel, Kategorie, drei sinnvolle interne Links, vollständiger Text. Nicht veröffentlichen. Abnahme **BESTANDEN** erst mit dieser tatsächlichen Beobachtung, ansonsten derselbe Fehlerbesitzer repariert.

## Grenzen / Abschluss
- Software/Tests des konkreten Quellenfalls: umgesetzt und Regression grün.
- Leitinstallations-E2E: **OFFEN**. Kein weiterer Pluginbau vor dem einen Realtest.
- Vollautomatische Nachrecherche nach REPAIR_REQUIRED: **nicht nachgewiesen / im aktuellen GitHub-Workflow nicht eigenständig vorhanden**. Keine falsche Freigabe dafür.
