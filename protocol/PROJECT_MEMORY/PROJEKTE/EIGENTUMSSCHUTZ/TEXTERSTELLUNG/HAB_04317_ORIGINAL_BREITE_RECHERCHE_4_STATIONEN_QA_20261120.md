# Hab & Bewahr – 20.11.2026: vierfach breite Original-Keywordrecherche, v0.4.31.7

**Quelle zuerst geprüft:** Unveränderte Pferdeatelier-Texterstellung 0.4.34, Hab 0.4.31.6 und Hobbydepot 0.4.24.15 aus den echten ZIPs. In **allen drei Original-PHP-Quellen** ist der originale PSTE-Research-Job `2.6.0` mit denselben vier vorhandenen Methoden enthalten:

1. `KEYWORD_SUGGESTIONS` → `dataforseo_labs/google/keyword_suggestions/live` (Keyword-Vorschläge).
2. `RELATED_KEYWORDS` → `dataforseo_labs/google/related_keywords/live` (verwandte Begriffe).
3. `KEYWORD_IDEAS` → `dataforseo_labs/google/keyword_ideas/live` (weitere Ideen, inklusive vorhandener Längen-/Volumenmischung der schon gelieferten Keywords).
4. `QUESTIONS` / People Also Ask → `serp/google/organic/task_post+task_get/advanced`, `questions_required=true`, `questions_state` muss für neue 2.6.0-Jobausgabe COMPLETE werden.

**Wichtig:** Die vier Originalmethoden waren schon vorhanden! Keine dieser Methoden neu implementiert, verkleinert, umgeordnet oder zusätzlich verdoppelt. **Keyword-/Portalentscheidung findet wie im Original erst NACH dieser Recherche statt.**

## Nachgewiesener Hab-Beginn-Fehler und minimale neue Korrektur
- Original `PSTE_Breadth_Research_Queue::openFamilies` schrieb den gesamten redaktionellen C23-Text `topic_family_name` unverändert als Suchseed, z. B. `Abholbox mit passenden Zugangsrechten und Schutz ausstatten`.
- Neue Hab-Version 0.4.31.7: An der **vorhandenen, alleinigen Seed-Zuständigkeit** liest die Originalqueue die bereits signierte R1/R2/R3-Vorfahrenfolge der aktuellen WP-Kategorie. R3 ist der vorhandene Themenbesitzer, kein neuer Kategorie-Entscheid.
- R3 `Abholbox-Diebstahlschutz` + C23 beginnt ausdrücklich mit `Abholbox` → breiter Seed **`Abholbox`**. Für R3 ohne exakt beweisbaren Produkt-Präfix wird der echte R3-Themenname verwendet; fehlende R3-Bindung sperrt sicher.
- Die Original-C23-Kategorie und ihr `term_id`, Slug, `topic_family_key`, originaler fünfteiliger Auftrag und späterer Artikeltyp bleiben **unangetastet**. Keine Querverwechslung der Geschwisterkategorien.
- `PSTE_Category_Context::portalContextTerm` ergänzt bei eindeutiger Site-Identität `Hab & Bewahr` beziehungsweise `Hab und Bewahr` nicht mehr die sachfremden Begriffe `Hab`/`Bewahr` an Produktseeds.
- Kosten-, Retry-/Status-, Originalprovider-, PAA- und K0-Stationen unverändert.

## Tatsächlich ausgeführte Prüfungen (lokal, echte Original-PHP-Klassen)
- **48/48**: vier vorhandene Provider-Methoden, zwingende Fragen, weitere Ideen aus verwandten Treffern, kurze Starts, 5 verschiedene Kategoriezuordnungen mit gleicher R3, negative fehlende R3, unveränderte IDs, ursprüngliche Pferde-Seed-Kontextregel.
- **17/17**: bestehende Hab-MINI-/originale PHP-Auftragsprüfungen erneut ausgeführt.
- **14/14**: bestehende originale Hab-K0-Fünffeld-/simulierte Entwurfsimportprüfungen erneut ausgeführt.
- **78/78** PHP-Lints, **87/87** ZIP-CRC, **83/87** Quelldateien byteidentisch. Lediglich `class-pste-breadth-research-queue.php`, `class-pste-category-context.php`, `texterstellung.php` (Version/Anzeige) und `README-TESTINSTALLATION.txt` verändert.
- Keine echte DataForSEO-Anfrage, keine neue Gebühr, keine WordPress-Schreiboperation, **keine Änderung an Original-K0 oder unabhängigem K-Multi**.
- ZIP: `Texterstellung_HAB_UND_BEWAHR_0.4.31.7_BREITE_ORIGINALRECHERCHE.zip`; **SHA256** `974cc101c52f274a1abf0a4777ada114e08610a5f08b10f386c3da1ff0760459`; **518285 Bytes**.
- **Im Büro gespeichert**: `/hab-und-bewahr/TEXTERSTELLUNG/PLUGIN_FREIGABEKANDIDATEN/` (ZIP) sowie `/hab-und-bewahr/TEXTERSTELLUNG/PRUEFUNG_BREITE_RECHERCHE_20261120/` (voller Prüfbericht, QA-JSON, Original-Patch).
- **Noch nicht als live installiert oder echt durch DataForSEO bestätigt.**

## Nachweisgrenzen / nächste Stufe
1. Der Screenshot um 09:27 zeigte noch eine bereits bezahlte Hab-Recherche in RUNNING mit altem Seed. **Kein Wechsel bei aktiver Recherche, keine neue bezahlte Recherche ohne erneute Freigabe**. Bereits gestartete Aufgaben behalten Originalseed der gespeicherten Queue. Nach Abschluss aktuelle Diagnose exportieren und prüfen.
2. Die **nachgelagerte** bestehende Familienrelevanz kann weiterhin Synonyme (`Paketbox`) und semantisch verwandte Abholbox-Keywords wegen fehlender Pflichtwörter sperren oder in REVIEW stellen. Das wurde nicht durch die Recherche-Korrektur als gelöst erklärt: separater, an genau einem Originalowner nachzuweisender Regressionstest vor kompletter Artikelproduktion erforderlich.
3. Unabhängiger neuer K-Multi-Schreiber, echte LT68-Artikelprüfung und WordPress-Entwurfsimport weiterhin offen. K0 niemals verändern.

**Nächster Schritt:** Den jetzigen DataForSEO-Job abarbeiten lassen und aktuelle Diagnose prüfen; dann erst dieses vorhandene Plugin ersetzen und **einen** ausdrücklich erlaubten breiten echten 4-Methoden-Lauf prüfen. Danach vorhandene Nachprüfung der Keyword-Passung ohne Doppelentscheid. Keine falsche K0-Endabnahme.
