# K0 QA – Einmaliger SEO-Owner, 4 genehmigte Regeländerungen, DataForSEO geschützt
**Datum:** 10.11.2026. **Branch:** `qa/k0-editorial-owner-only-20261110`, ausschließlich vom aktiven `konzept0-portal-neutral-20261002` abgezweigt. **Aktiver K0-Produktionsbranch/WordPress/PSERC/PSTE NICHT verändert.**

## Verbindliche Entscheidung des Benutzers
1. K0-`title.keyword_required`: exakte Keyword-Wortfolge im Titel **ersatzlos gestrichen**. Die Redaktion bewertet natürliche Titel und Suchintention.
2. K0-`heading.target_phrase_control`: exakte 1–2 Zielkeyword-Phrasen in H2 **ersatzlos gestrichen**. `heading.keyword_staccato_forbidden` **muss erhalten bleiben** – wichtige Keyword-Wörter weiterhin höchstens zweimal in H2.
3. K0-`title.colon_forbidden` und `type.question_mark_policy`: **aus K0 herausnehmen**, nur einmal vom bereits vorhandenen Titel-/Sprach-Owner vor der Übergabe prüfen. Nachweis im unveränderten PSERC .28.60: `includes/class-pserc-title-gate.php::verify` prüft `PPM_QUESTION_MARK_REQUIRED` und `PPM_COLON_FORBIDDEN` (und FAQ-Frageverbot je Vertragslage), `class-pserc-compiler.php::finalizeAllocationRow` setzt bei Nicht-PASS `REVIEW_REQUIRED_TITLE_COMPATIBILITY`, kein READY-Handoff.
4. K0 `engine/k0_production_gate.py::_expected_intent`: **nachgewiesen zweite eigenständige Suchintententscheidung** aus Artikelart und Titel, bisher `K0_SEARCH_INTENT_MISMATCH`; diese zweite Entscheidung aus K0 entfernen. Bereits im Auftrag gelieferter `content_profile.search_intent`-Wert wird nur auf Vorhandensein geprüft und als Schreibauftrag genutzt; der K0-Textschutz gegen Boilerplate und gegen Informations-FAQ-Kauftext bleibt. Kein K0-SEO-Neuurteil.
5. **Punkt 5 des alten Plans vollständig AUSGENOMMEN**: Vor-LT-Qualitätsprüfung und finale Nach-LT-Gesamtprüfung bleiben unverändert. Nach Textreparatur alle notwendigen Prüfungen erneut.
6. K0-Reparatur, sämtliche Regeln für Wörter/Absätze/H2-Zahl/Abschnittsbalancen/Grammatik/Quellen/Links/Tabellen/Listen/Phrasen und technische Übergabe unverändert.
7. **DataForSEO als normaler Erststart**: Originale PSTE-0.57.144.33 und PSERC-0.28.60 vollständig unangetastet. PSTE `class-pste-research-job.php` geht durch KEYWORD_SUGGESTIONS, RELATED_KEYWORDS, KEYWORD_IDEAS mit unveränderten Methoden des `class-pste-dataforseo-client.php`. Test mit vorhandenen Keywords ist lediglich ein Sonderfall. Live-Providerabruf/Credentials waren **nicht** Teil des K0-QA-Tests.

## Exakt geänderte K0-Dateien im **QA-Zweig**
- `RULE_CATALOG.json`: genau 4 ARTICLE/HARD-Originaleinträge entfernt; aus **85 werden 81**. Die anderen 117 ursprünglichen Katalogeinträge in Inhalt und Reihenfolge unverändert.
- `RULE_VALUES.json`: nur historisches Titel-Keyword-Order-Gebot, Titel-Doppelpunktgebot, FAQ-Fragezeichen-K0-Gebot und drei exakte H2-Phrasen-Zahlwerte entfernt. **Alle übrigen Zahlen-/Text-/Faktengrenzen im JSON-Vergleich unverändert** (u.a. 750–900 Wörter, 16 Absätze, vier H2, max. 2 H2-Keyword-Wiederholungen).
- `FIELD_POLICY.json`: nur 4 entsprechende alte HARD-Bindungen durch dokumentierte SUPERSEDED-/Upstream-Owner-Zuordnung abgelöst; unveränderte K9-Feldinventur weiterhin vollständig zugeordnet.
- `engine/checkers.py`: nur die vier fachlichen Einzelprüfungen und deren ausschließlich benutzte lokale Hilfsvariablen/-funktion entfernt; andere 81 Regel-Rechner, insbesondere Anti-Stakkato, unverändert.
- `engine/k0_production_gate.py`: `_expected_intent` als autonome K0-SEO-Entscheidung entfernt; weiterhin NICHT-leerer Intentwert, bestehende Text-/Boilerplate-Sperren; `K0_SEMANTIC_GATE`-Übergabevertrag unverändert.
- `PPM_PARITY_MAP.json`, `engine/ppm_parity_guard.py`: exakt die 3 alten **Titelprüfungen** der geschützten 104er-Legacy-Inventur an externen Titel-Owner delegiert. Andere **101 Original-Mappings** byte-/JSON-inhaltlich unverändert; alle 104 Inventarpositionen weiter geprüft. Jede andere unzulässige Delegation/Abweichung sperrt.
- `tests/test_k10.py`: ein alter Negativtest prüfte fehlenden Receipt der gelöschten Doppelpunkt-Titelregel, prüft nachher stattdessen fehlenden Receipt einer unverändert erforderlichen Strukturregel.
- Neue Datei `tests/test_k0_seo_owner_qa.py`: gezielte Regression der vier Änderungen, des String-/Wortzahl- und PPM-Schutzes, der drei echten exportierten Titel, des H2-Anti-Stakkato-Schutzes, der Soll-Intent-Nicht-Neuentscheidung und des Boilerplate-Schutzes.
- Neue Datei `.github/workflows/qa-k0-seo-owner-20261110.yml`: getrennte CI **nur QA-Branch**, ohne WP-Schreib- oder K0-Produktionsworkflow.

## Tatsächliche Tests / Messwerte
- GitHub Actions **PASS**, [K0 editorial-owner-only QA / Run 42837580167](https://github.com/hallo-netizen/affiliate-pferdeportal/actions/runs/42837580167), Commit `d3ff0c489954688b3be6b531a69483f8f47f068b`.
- **51/51 Bestandstests K10 PASS** und **7/7 neue K0-QA-Tests PASS**. Python-Compile PASS.
- Vollständiger `git diff` Originalbranch→QA für `engine/k0_writer_station.py`, `engine/writer_contract_guard.py`, `engine/k0_wordpress_export.py`, `engine/lt68_external.py`, `.github/workflows/k0-writer-accept.yml`, `.github/workflows/k0-authoring-context.yml`: **0 Unterschiede**.
- Separate strukturelle Original-/QA-JSON-Prüfung: 117 übrige Katalogeinträge exakt gleich, alle nicht gezielt entfernten RULE_VALUES-Daten exakt gleich, 101 übrige PPM-Mappings exakt gleich; 104/104 PPM-Inventar abgedeckt.
- Echte Original-Dreierdatei `real_runs/k0/batch-20261110-42619ca7/BATCH_INTAKE.json` weiterhin mit Original-K0-Intake technisch PASS. Geschützte Input-Regeln, Hash, exakte fünf Felder, plan_slot und WordPress-Import weiterhin gültig.
- **DataForSEO Codepakete nicht geändert**: ursprüngliche lokale PSTE ZIP `PSTE-0.57.144.33-KISS-BEREINIGT-NUR-TEST.zip` SHA-256 `cd62e7c58dce4bfe9c75026bb604e0182f45a12f5d26075d9b1a85a859472ae2`, PSERC `PSERC-0.28.60-KISS-EXTERNER-SEO-OWNER-NUR-TEST.zip` SHA-256 `c9c7e90b265e650739d2568a7cb807238db7f081ddcf7d8698fe64961b84f22a`. ZIP-Versionen NICHT neu gebaut oder installiert.

## Nachweisgrenzen / NICHT Live-freigegeben
1. **Eingang 5 Felder OHNE Suchintentfeld:** Der Redaktionsplan hat zwar vorangegangene Intent-Entscheidungen, K0 bekommt im Metadatenvertrag keinen unmittelbaren Intentbeleg. Der Wert kommt erst im `K0_AUTHORING_CONTEXT.content_profile.search_intent` vor. Bevor K0-Produktionsfreigabe erfolgt, einmal kontrollieren, dass genau der bereits im Redaktionsbüro entschiedene Intent im Writer-Kontext ankommt, ohne sechstes Metadatenfeld oder neue zweite Redaktion. **Nicht stillschweigend als bewiesen behandeln.**
2. **Bestehende K0 Writer-Jobs sind an den 85er-Regelkatalog gebunden**. Nur neuer, verifizierter Lauf mit korrekt neu gebundenen Regeln kann 81er-Layout nutzen. Kein In-place-Edit vorhandener Jobs; die zwei alten, gestoppten Jobs nicht gewaltsam weiterlaufen lassen.
3. **QA-Zweig ist KEIN Produktionszweig**. Die unveränderte Produktions-`K0_CURRENT_STATE.json` hat weiterhin 85/84 und die laufenden CI-Workflows bleiben am unveränderten Produktionsbranch. Beim kontrollierten späteren Übergang müssen K0-/K10-Zielvertrag, Regelzahl und PPM-Delegationsfreigabe korrekt abgestimmt und die Aktivierung gesondert geprüft werden.
4. **Noch kein echter vollständiger frisch produzierter 3-Artikel-Lauf**, keine echte WordPress-Testinstallation und kein echter DataForSEO-Liveabruf in diesem QA-Verfahren. 58 Code-/Regressionstests beweisen nur die getesteten Pfade.
5. **Separater Altbefund nicht mit dieser Änderung vermischen**: Eine alte FORBIDDEN_BOILERPLATE-Phrase enthält `ß`, der vorhandene K0-Vergleich nutzt `.casefold()` auf sichtbarem Text, nicht aber auf den alten Fingerprints. Dadurch kann konkret `für die praxis heißt das: betrachte` entgehen (`heißt` vs `heisst`). Die K0-Textregel wurde entsprechend Nutzervorgabe **NICHT** verändert; zur späteren getrennten Fehlerbehebung dokumentiert.

## Status / Anschluss
**KISS_USER_APPROVED_QA_CODE=IMPLEMENTED; 58/58 REGRESSION_PASS; K0_ACTIVE_BRANCH=UNCHANGED; WP_PLUGINS=UNCHANGED; DATAFORSEO_CODE=UNCHANGED; RULES_PRE_POST_LT=UNCHANGED; UPSTREAM_INTENT_BINDING_E2E=NOT_YET_PROVEN; LIVE_GO=NO.**

Als nächstes verbindlich: Original-Intent aus unverändertem PSTE/PSERC-Kontext gegen die vorhandenen, fünf-Felder-K0-`plan_slot`-Berechtigungen prüfen; gezielten frischen End-to-end-Writer-Test auf QA durchführen; **erst danach** eine kontrollierte Übernahme planen, ohne alte Jobs/Hashes zu gefährden.
