# K0 – vollständige Zuständigkeits- und Sinnprüfung aller 85 HARD-Artikelregeln (10.11.2026)

**Status: Quellengeprüfte Analyse auf K0-Produktionsbranch `konzept0-portal-neutral-20261002`, KEIN Regelwechsel, KEINE K0- oder PSERC/PSTE-Codeänderung.**
Quelle: `RULE_CATALOG.json` (121 Regeln insgesamt, 85 ARTIKEL/HARD), `RULE_VALUES.json`, `FIELD_POLICY.json`, `TEXTMACHINE_SCOPE_REFERENCE.json`, `engine/checkers.py`, `engine/k0_full_rules.py`, `engine/final_integrity.py`, `engine/k0_portal_resolver.py`.

## Prüfverfahren
Jede der 85 eindeutigen HARD-Artikelregeln wurde mit ihrem realen Owner und vorhandener Anwendung abgeglichen und nach **Zuständigkeit** und **fachlicher Sinnhaftigkeit** in eine **vorläufige Entscheidungsklasse** eingeordnet. Klasse "Grenzfall" bedeutet NICHT "überflüssig bewiesen", sondern "ein striktes Muss ist sachlich fragwürdig; mit Betreiber entscheiden, dann sicher testen". Andere Artikelregeln (36 nicht-HARD bzw. SYSTEM/PACKAGE) und dynamische externe LT-Subregeln sind **nicht** Teil der Zahl 85; diese dürfen keinesfalls im Rahmen einer 85er-Artikelregelbereinigung gelöscht werden.

**Verteilung:** 3 echte redaktionelle Titelregeln, die **K0 nicht mehr fachlich entscheiden sollte**; 25 inhaltlich diskutierbare Formzwänge und messwertbasierte Hardlocks; 57 zunächst berechtigte Textproduktions-/Sicherheitsregeln (NICHT als ewige Fehlerfreiheit oder bewiesene Einzigartigkeit ausgeben). **Summe 85/85**. Aktuelle zuständige Code-Owner: lt68_adapter:1, balance_checker:8, fact_trace_checker:14, editorial_checker:16, structural_checker:36, table_checker:10.

## Nachweisbare echte Eigentümerkonflikte
- `title.keyword_required` benutzt `engine.checkers._keyword_tokens_in_order`: **alle Keyword-Wörter einzeln, wörtlich und in Reihenfolge**, nur Sonderzeichen/Großschreibung werden normalisiert. Diese harte Fachregel scheitert an den zwei realen, grammatikalisch richtigen Titeln aus der WordPress-Dreierdatei. Titel und Suchintention sind **vor K0** durch PSTE/externen SEO-Owner fachlich freigegeben. **KISS-Empfehlung: K0-`title.keyword_required` als redaktionellen Hardlock entfernen, nicht als neue zweite Prüfung ins Redaktionsbüro kopieren.**
- `title.colon_forbidden`: pauschales Doppelpunktverbot ist eine Titelstilentscheidung, keine Textproduktions-/Sicherheitsregel. Redaktion entscheidet, kein zweiter K0-Hardlock.
- `type.question_mark_policy`: ist eine **Titelzeichenregel** (FAQ requires `?`, andere optional), daher vor Übergabe an den Titelowner, nicht nochmal fachlich in K0.
- `type.metadata_schema` und `wordpress.semantic_category_binding` bleiben technische **Bindungsprüfungen**: Sie entscheiden keine neue Kategorie / Artikelart, sondern prüfen Unverändertheit bzw. korrekten WP-Artikelvertrag. Nicht unkontrolliert entfernen.
- `heading.intent_binding` ist *keine zweite Suchintententscheidung*: prüft, ob die **produzierten Abschnittsüberschriften** den vorgegebenen Sachverhalt behandeln; diese Produktionsqualitätsprüfung bleibt.

## Kritisch zu besprechende Grenzfälle (thematisch gebündelt)
1. **Wörtliche SEO-Muster:** `heading.target_phrase_control` erzwingt 1–2 exakte Keyword-Nennungen in H2. Keine Google-Pflicht; darf den natürlichen Text nicht verschlechtern. `heading.phrase_family_repetition_forbidden` und `heading.grammatical_variety` können brauchbare Formulierungen anhand starrer Wortanfänge ablehnen. Anti-Keyword-Stakkato und echte Verständlichkeitsprüfung sollen bleiben.
2. **Fixe Längen/Geometrie:** 750–900 Wörter (oft nur historischer Projektmaßstab, keine Google-Vorgabe), mindestens 16 Absätze und vier H2; jede Hauptsektion 100–220 Wörter, längste höchstens 1,5-mal kürzeste, Mindest-Haupttextanteil 50 %, extra Text zwischen H2; Regeln können nützliche kürzere Antworten blockieren oder zum Fülltext zwingen. Mehrere Regeln messen dieselbe Textlänge auf verschiedene Weise, sind aber nicht unbedingt codeidentische Prüfungen.
3. **Fazit-Form:** Mindestanteil 8–10 % des Artikels und mindestens zwei Fazit-Absätze; kann künstlich aufblähen. Sachlicher Schluss, keine neuen unbelegten Fakten, bleibt.
4. **Listen/Tabellen:** Listenpflicht je Textart und mindestens vier Listeneinträge; Tabellen häufig `REQUIRED_UNLESS_EXCEPTION`, bestimmte Mindestmaße, extrem kurze Tabellenzellen und Pflichtzusammenfassung; Mehrwert-Regeln sind vorhanden und wurden zuvor vom Betreiber bewusst genehmigt. Nicht pauschal löschen; eher Mehrwert vor Größe statt formaler Füllzeilen. `table.required_for_comparison`, `table.value_required_if_present`, `table.optional_decision_documented` ausdrücklich erhalten, bis Betreiber anders entscheidet.
5. **Quellen-Mathematik:** `facts.fact_pack_coverage` verlangt mindestens 75 % des Faktensatzes zu verwenden; `facts.trace_lexical_support` verlangt 80 % lexikalische Unterstützung. Kann sachlich richtige Auswahl/paraphrasierte Formulierungen unnötig sperren. **Fakten-Nachweise, Quellen-Echtheit, Zahlenbelege, zulässige Fakten und Schutz vor Erfindungen bleiben**.
6. **Wortlautähnlichkeit:** `surface.duplicate_sentence_ratio` unter 2 % und `surface.intro_similarity` bis 55 % könnten faire Standardformulierungen sperren. Originalität und keine wortgleiche Massenware trotzdem erhalten.
7. **H2-Länge** max. neun Wörter / 65 Zeichen – als Qualitätsleitlinie sinnvoll, hartes Scheitern an geringem Überhang ist diskutierbar. Kein stilles Entfernen der Überschriftenqualität.

**Externe Quellenabgleichung:** Google Search Central SEO Starter Guide (`https://developers.google.com/search/docs/fundamentals/seo-starter-guide`) stellt ausdrücklich klar, dass Google Seitenbezug auch ohne wörtliche Suchbegriffe erkennen kann. Google Helpful Content (`https://developers.google.com/search/docs/fundamentals/creating-helpful-content`) erklärt, dass Google **keine bevorzugte Wortanzahl** hat und Warnsignale entstehen, wenn man wegen angeblicher SEO-Wortmengen schreibt. Beide Aussagen rechtfertigen NICHT den Verzicht auf gründliche Artikel, nachweisbare Fakten oder einen projektintern bewusst genehmigten Stil.

## Wirkliche Doppelberechnung der Artikelregeln – auch ohne Redaktion
`engine/k0_full_rules.py::verify_pre_lt68` erzeugt vor LanguageTool 6.8 alle **84** Inhaltsprüfungen via `run_article_content_checks`. `verify_final` erzeugt via `run_article_checks` **dieselben 84 Inhaltsprüfungen erneut** plus den einen LT-Check (`engine/checkers.py`). Dagegen sagt `TEXTMACHINE_SCOPE_REFERENCE.json`: `CONTENT_RULES_CHECK_ONCE_BY_OWNER; HARD_INTEGRITY_RULES_VALIDATE_BINDING_AND_IMMUTABILITY; FINAL_STAGE_DOES_NOT_RECHECK_PASSED_CONTENT_RULES`.
**Befund:** Doppelte Ausführung besteht im Originalcode, fachliche Eigentümerschaft ist die gleiche, d.h. keine neue Redaktion, aber operative Doppelarbeit. **Saubere KISS-Lösung:** Wenn der sichtbare Text **byte-/hashidentisch** bleibt und die vollständigen Regelquellen nachweislich unverändert sind, könnte der finale Schritt dieselben bereits bestandenen signierten Prüfergebnisse wiederverwenden; nach Reparatur/Änderung muss betroffene Qualität erneut geprüft werden. Nicht blind abschalten oder Hash-/LT-Bindungen entfernen. Vollständiger Nachweis und Regression erforderlich; noch nicht umgesetzt.

## 85/85 Regel-für-Regel-Inventur

Die rechte Spalte beschreibt die **vorläufige Zuordnung**, keine vollzogene Löschung.

| Nr. | echte K0-Regel | Eigentümer im K0-Katalog | Einschätzung |
|---:|---|---|---|
| 1 | `lt68.language_zero_unresolved` | lt68_adapter | K0 Text-/Sicherheitsregel |
| 2 | `conclusion.hard_limits` | balance_checker | K0 Text-/Sicherheitsregel |
| 3 | `conclusion.type_minimum_ratio` | balance_checker | Grenzfall zu entscheiden |
| 4 | `facts.conclusion_no_new_untraced_facts` | fact_trace_checker | K0 Text-/Sicherheitsregel |
| 5 | `facts.trace_binding` | fact_trace_checker | K0 Text-/Sicherheitsregel |
| 6 | `facts.trace_required` | fact_trace_checker | K0 Text-/Sicherheitsregel |
| 7 | `facts.trace_required_blocks` | fact_trace_checker | K0 Text-/Sicherheitsregel |
| 8 | `heading.duplicate_normalized_forbidden` | editorial_checker | K0 Text-/Sicherheitsregel |
| 9 | `heading.grammatical_variety` | editorial_checker | Grenzfall zu entscheiden |
| 10 | `heading.hard_length` | editorial_checker | Grenzfall zu entscheiden |
| 11 | `heading.keyword_staccato_forbidden` | editorial_checker | K0 Text-/Sicherheitsregel |
| 12 | `heading.natural_concrete_section_language` | editorial_checker | K0 Text-/Sicherheitsregel |
| 13 | `heading.phrase_family_repetition_forbidden` | editorial_checker | Grenzfall zu entscheiden |
| 14 | `heading.target_phrase_control` | editorial_checker | Grenzfall zu entscheiden |
| 15 | `links.required_roles` | structural_checker | K0 Text-/Sicherheitsregel |
| 16 | `links.visible_exact` | structural_checker | K0 Text-/Sicherheitsregel |
| 17 | `structure.duplicate_block_names_forbidden` | structural_checker | K0 Text-/Sicherheitsregel |
| 18 | `structure.required_blocks` | structural_checker | K0 Text-/Sicherheitsregel |
| 19 | `structure.required_lists` | structural_checker | Grenzfall zu entscheiden |
| 20 | `surface.non_template_language` | editorial_checker | K0 Text-/Sicherheitsregel |
| 21 | `surface.repetition_forbidden` | editorial_checker | K0 Text-/Sicherheitsregel |
| 22 | `table.canonical_classes` | table_checker | K0 Text-/Sicherheitsregel |
| 23 | `table.compact_cells` | table_checker | Grenzfall zu entscheiden |
| 24 | `table.compact_labels` | table_checker | Grenzfall zu entscheiden |
| 25 | `table.post_summary_policy` | table_checker | Grenzfall zu entscheiden |
| 26 | `table.required_for_comparison` | table_checker | K0 Text-/Sicherheitsregel |
| 27 | `table.value_required_if_present` | table_checker | K0 Text-/Sicherheitsregel |
| 28 | `title.colon_forbidden` | structural_checker | vor K0 / Redaktion |
| 29 | `title.keyword_required` | structural_checker | vor K0 / Redaktion |
| 30 | `type.metadata_schema` | structural_checker | K0 Text-/Sicherheitsregel |
| 31 | `type.question_mark_policy` | structural_checker | vor K0 / Redaktion |
| 32 | `words.further_information_maximum` | balance_checker | K0 Text-/Sicherheitsregel |
| 33 | `words.hard_total_range` | balance_checker | Grenzfall zu entscheiden |
| 34 | `words.main_text_minimum_ratio` | balance_checker | Grenzfall zu entscheiden |
| 35 | `words.section_balance_ratio` | balance_checker | Grenzfall zu entscheiden |
| 36 | `words.section_range` | balance_checker | Grenzfall zu entscheiden |
| 37 | `structure.body_h1_forbidden` | structural_checker | K0 Text-/Sicherheitsregel |
| 38 | `structure.title_not_repeated_in_body` | structural_checker | K0 Text-/Sicherheitsregel |
| 39 | `structure.visible_test_marker_forbidden` | structural_checker | K0 Text-/Sicherheitsregel |
| 40 | `structure.machine_status_word_forbidden` | structural_checker | K0 Text-/Sicherheitsregel |
| 41 | `structure.paragraph_floor` | structural_checker | Grenzfall zu entscheiden |
| 42 | `structure.h2_floor` | structural_checker | Grenzfall zu entscheiden |
| 43 | `structure.required_blocks_nonempty` | structural_checker | K0 Text-/Sicherheitsregel |
| 44 | `structure.section_ids_unique` | structural_checker | K0 Text-/Sicherheitsregel |
| 45 | `structure.section_order` | structural_checker | K0 Text-/Sicherheitsregel |
| 46 | `structure.section_h2_exact_one` | structural_checker | K0 Text-/Sicherheitsregel |
| 47 | `structure.section_paragraph_required` | structural_checker | K0 Text-/Sicherheitsregel |
| 48 | `structure.list_minimum_items` | structural_checker | Grenzfall zu entscheiden |
| 49 | `structure.intro_first` | structural_checker | K0 Text-/Sicherheitsregel |
| 50 | `structure.intro_structure` | structural_checker | K0 Text-/Sicherheitsregel |
| 51 | `structure.adjacent_headings_forbidden` | structural_checker | K0 Text-/Sicherheitsregel |
| 52 | `structure.faq_direct_answer` | structural_checker | K0 Text-/Sicherheitsregel |
| 53 | `structure.text_between_headings_minimum` | structural_checker | Grenzfall zu entscheiden |
| 54 | `structure.html_balanced` | structural_checker | K0 Text-/Sicherheitsregel |
| 55 | `heading.intent_binding` | editorial_checker | K0 Text-/Sicherheitsregel |
| 56 | `heading.semantic_duplicate_forbidden` | editorial_checker | K0 Text-/Sicherheitsregel |
| 57 | `surface.known_regression_patterns_forbidden` | editorial_checker | K0 Text-/Sicherheitsregel |
| 58 | `surface.known_unnatural_language_forbidden` | editorial_checker | K0 Text-/Sicherheitsregel |
| 59 | `surface.duplicate_sentence_ratio` | editorial_checker | Grenzfall zu entscheiden |
| 60 | `surface.intro_similarity` | editorial_checker | Grenzfall zu entscheiden |
| 61 | `facts.real_source_trace` | fact_trace_checker | K0 Text-/Sicherheitsregel |
| 62 | `facts.source_label_option_match` | fact_trace_checker | K0 Text-/Sicherheitsregel |
| 63 | `facts.visible_unit_fact_refs` | fact_trace_checker | K0 Text-/Sicherheitsregel |
| 64 | `facts.referenced_fact_exists` | fact_trace_checker | K0 Text-/Sicherheitsregel |
| 65 | `facts.referenced_fact_verified` | fact_trace_checker | K0 Text-/Sicherheitsregel |
| 66 | `facts.referenced_fact_type_allowed` | fact_trace_checker | K0 Text-/Sicherheitsregel |
| 67 | `facts.numeric_claim_supported` | fact_trace_checker | K0 Text-/Sicherheitsregel |
| 68 | `facts.fact_pack_coverage` | fact_trace_checker | Grenzfall zu entscheiden |
| 69 | `facts.trace_lexical_support` | fact_trace_checker | Grenzfall zu entscheiden |
| 70 | `facts.runtime_fact_allowlist` | fact_trace_checker | K0 Text-/Sicherheitsregel |
| 71 | `links.bound_pairs_exact` | structural_checker | K0 Text-/Sicherheitsregel |
| 72 | `links.registry_active` | structural_checker | K0 Text-/Sicherheitsregel |
| 73 | `links.section_placement` | structural_checker | K0 Text-/Sicherheitsregel |
| 74 | `links.relative_internal_only` | structural_checker | K0 Text-/Sicherheitsregel |
| 75 | `links.further_information_position` | structural_checker | K0 Text-/Sicherheitsregel |
| 76 | `links.distributed_across_blocks` | structural_checker | K0 Text-/Sicherheitsregel |
| 77 | `links.runtime_roles_bound` | structural_checker | K0 Text-/Sicherheitsregel |
| 78 | `links.not_clustered_at_end` | structural_checker | K0 Text-/Sicherheitsregel |
| 79 | `table.presence_policy` | table_checker | Grenzfall zu entscheiden |
| 80 | `table.minimum_rows` | table_checker | Grenzfall zu entscheiden |
| 81 | `table.structure` | table_checker | Grenzfall zu entscheiden |
| 82 | `conclusion.minimum_paragraphs` | balance_checker | Grenzfall zu entscheiden |
| 83 | `wordpress.semantic_category_binding` | structural_checker | K0 Text-/Sicherheitsregel |
| 84 | `intro.orientation_sentence` | editorial_checker | K0 Text-/Sicherheitsregel |
| 85 | `table.optional_decision_documented` | table_checker | K0 Text-/Sicherheitsregel |

## Änderungs- und Freigabereihenfolge (kein stückweises Symptompatchen)
1. Mit dem Betreiber **nur 7 fachliche Grenzfallgruppen** abstimmen, inklusive Titel-, Längen- und Quellenzwänge, bevor irgendeine Regel entfernt wird.
2. Die 85er-Zuordnung als gemeinsamen **Zielvertrag** vereinbaren: eine SEO-/Titelentscheidung im Redaktionsbüro, K0 nur Produktion, gleichbleibende technische Integrität; historische 104/151 andere Pflichtwerte und Import-/Designvertrag nicht übersehen.
3. **K0 auf isolierter Kopie** und anschließend PSTE/PSERC-Schnittstelle **als zusammengehörenden Vertrag** abgleichen. K0-Bundle- und Policy-Hashes/Hard-Count aktualisieren, erforderliche Tests/Regressionen 3 ursprüngliche Titel+negative Manipulationen bestehen. Bloß `RULE_CATALOG.json` editieren ohne eingebundene Prüfer wäre falsch.
4. Gültige externe SEO-Einmalentscheidung **vor** K0; gleiche Fachentscheidung nicht noch einmal im K0-Writer-/Final-Checker. Bei Reparatur nur erneut prüfen, was sich geändert hat; K0-Sicherheits-/Fakten-/Sprach- und WordPress-Gates behalten.
5. GitHub Branch `konzept0-portal-neutral-20261002` und Live/TEST sind **nicht** verändert. Bis zur abgestimmten Gesamtfreigabe alle aktuellen Hardlocks gültig; keine vorzeitigen "K0 wird schon produzieren"-Versprechen.

**AUDIT_STATUS=SOURCE_REVIEWED_85_OF_85; REMOVALS_PERFORMED=0; FULL_SYSTEM_REGRESSION=NOT_RUN.**
