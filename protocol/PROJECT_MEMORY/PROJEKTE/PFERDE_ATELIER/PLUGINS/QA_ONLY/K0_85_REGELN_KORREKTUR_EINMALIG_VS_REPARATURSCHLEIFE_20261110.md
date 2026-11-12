# K0-Regelaudit KISS: Einmalige Eigentümerentscheidung versus Reparaturprüfung (korrigiert, 10.11.2026)

**Korrektur/Vertragspräzisierung für alle Nachfolge-Chats, insbesondere gegenüber dem ersten 85er-Audit.** Original-K0 `konzept0-portal-neutral-20261002` wurde schreibfrei gelesen. Aktive K0-Regeln und Originale bleiben **unverändert**; nichts gelöscht, verschoben, migriert oder auf TEST/LIVE installiert.

## Bindende Benutzerentscheidung (10.11.2026)
1. **Alle eigentlichen Text-/Schreibregeln bleiben unangetastet:** 750–900 Wörter, Absätze, Überschriften-Anzahl/-Längen, Abschnittslängen/-verhältnisse, Fazit, Mindestlisten, natürliche Sprache, Wiederholungsgrenzen, Grammatik, Faktenregeln, Rechtschreibung, Tabellenmehrwert, Design-/HTML-Aufbau. Diese strikten Grenzen wurden über Wochen empirisch für verlässliche K0-Texte abgestimmt; nicht als vermeintlich veraltet streichen.
2. **Eine fachliche Entscheidung nur einmal:** SEO, Suchintention, Zielkeyword, Titel, Artikelart, Kategorie und redaktionelle Zuordnung vor K0. K0 darf keine zweite eigenständige Titel-/SEO-Redaktion sein. Integrität des übergebenen Auftrags ist keine erneute fachliche Entscheidung.
3. **Produktionsqualität darf mehrfach geprüft werden**, wenn Writer-/Reparaturschleifen Text, Quellenzuordnung, Tabelle oder einen anderen prüfungsrelevanten Wert verändern. Wiederholung einer Qualitätskontrolle ist **nicht automatisch doppelte fachliche Zuständigkeit**.
4. **Ohne Änderung** derselben geprüften Werte und Regelquellen reichen die vorhandenen unveränderlich gebundenen Prüfbelege; unnötige Neukalkulation ist KISS-Kandidat, darf aber erst nach Provenienz-/Integritäts-/Regressionstest optimiert werden.

## Tatsächlich geprüfter Stand und Klassen
- Originalkatalog `RULE_CATALOG.json`: 121 Regeln insgesamt, exakt **85 eindeutige ARTICLE/HARD-Regeln**. Sie wurden mit `RULE_VALUES.json`, `FIELD_POLICY.json`, `engine/checkers.py`, `engine/k0_full_rules.py`, `engine/final_integrity.py` und dem realen Eingangsweg verglichen.
- **A: 3 redaktionelle Titel-Fachentscheidungen, einmalig vor K0**: `title.keyword_required`, `title.colon_forbidden`, `type.question_mark_policy`. Die erste davon sollte **als hartes wörtliches K0-Gebot entfallen**, nicht am Redaktionsort erneut eingeführt werden. Welche Titelregeln die Redaktion selbst anwenden möchte, wird dort einmalig festgelegt. Der Schreiber darf den freigegebenen Titel nicht ändern; K0 prüft **Titel-Unverändertheit und Datei-/Auftragsintegrität**, nicht die SEO-Fachentscheidung.
- **B: 2 unveränderliche Auftragsbindungen, einmal an der Produktionsvorbereitung prüfen**: `type.metadata_schema`, `links.runtime_roles_bound`. Sie gehören **nicht zur SEO-Entscheidung**. Bei Finale nur Unverändertheit und Bindung der ursprünglichen Prüfung verifizieren; bei geänderten Metadaten erneut prüfen.
- **C: 80 artikel-/datenabhängige Ausführungs-/Qualitätsprüfungen**: Nach Writer, bei jeder relevanten Reparatur und bei überprüfungsrelevanter Daten-/Regeländerung erneut kontrollieren. Nach **vollständig unverändertem** Artefakt nicht unnötig wiederholt ausführen. Hierunter liegen die hart erarbeiteten Textregeln sowie Kategorie-/Link-Bindungschecks, die Ausgabe gegen echte Text-/Umgebungswerte prüfen.
- Diese Klassifikation beschreibt **Prüfhäufigkeit und Eigentümerschaft**, **keine Löschfreigabe**, keine Behauptung, dass 80 Regeln bei jeder kleinsten Änderung immer erneut laufen müssen: nur jeweils betroffene Regeln und ihre möglichen Folgewirkungen.

## Originalcode-Befunde, wichtige Korrekturen
1. **Zwei verschiedene H2-Keyword-Regeln, NICHT miteinander verwechseln:**
   - `heading.keyword_staccato_forbidden`: jedes bedeutende Keyword-Wort max. **zweimal** in allen H2, mit fachlichem Stopwortfilter. **Diese Schutzregel bleibt vollständig**.
   - `heading.target_phrase_control`: bei abweichendem Titel 1 bis 2 **exakte Keyword-Wortfolgen** in H2, bei Titel = Zielkeyword ausnahmsweise 0. Diese zusätzliche Verpflichtung auf wortwörtliche H2-Phrasen **gesondert** prüfen/entscheiden; vorläufig unverändert lassen, **nicht** die Antiwiederholungsregel entfernen.
2. **Tabellen nicht pauschal Pflicht, aber auch nicht völlig frei:** `table.presence_policy` sagt `REQUIRED_UNLESS_EXCEPTION` für Beratung, FAQ, Pflege; nur wenn definierte Ausnahme inkl. Dokumentation gilt, ohne Tabelle. Artikelart Vergleich verlangt `REQUIRED`, **genau eine** Tabelle. Ergänzend `table.value_required_if_present` verlangt echten Mehrwert; `table.optional_decision_documented` bindet die begründete Entscheidung. **Vom Betreiber bewusst erarbeiteter Aufbau bleibt**.
3. **Listen sind Pflicht:** Artikeltypen benötigen vorgeschriebene, benannte Listen und mindestens vier Listeneinträge. Keine Empfehlung mehr, die Mindestlisten unkontrolliert zu streichen.
4. **Wiederholungsbegrenzungen sind bewusst und wirksam:** `heading.phrase_family_repetition_forbidden`, `heading.grammatical_variety`, `surface.repetition_forbidden`, `surface.duplicate_sentence_ratio`, `surface.intro_similarity`, `heading.keyword_staccato_forbidden` und weitere prüfen unterschiedliche Arten der repetitiven Sprache. **Nicht als nutzlose Doppelprüfung behandeln**.
5. **Exakte Faktenklausel korrigiert:** `facts.fact_pack_coverage` nutzt in `engine/checkers.py` `required_selected_fact_coverage_ratio=1` (100 % der **ausdrücklich als `required_fact_ids` ausgewählten** Fakten), **nicht** pauschal 75 % aller recherchierten Fakten. `minimum_fact_pack_coverage_ratio=0.75` existiert als Historienwert in `RULE_VALUES.json`, wird in dieser Artikelprüfstelle **nicht verwendet**. Es ist falsch, die Regel als Pflicht zu „75 % aller recherchierten Fakten“ zu beschreiben.
6. **80-%-Quellenprüfung korrigiert:** `facts.trace_lexical_support` verlangt, dass mindestens 80 % der mit Fakten-IDs belegten tatsächlichen Text-Einheiten **mindestens ein bedeutsames Wort** mit ihren zugelassenen Faktentexten gemeinsam haben. Sie verlangt **nicht**, dass 80 % aller Wörter wörtlich übereinstimmen. Beleg-Echtheit, erlaubte Quellen, korrekte Zahlen und nachvollziehbare Faktentexte bleiben hart.
7. **Tatsächliche zweifache Rechenarbeit im K0-Kern:** `verify_pre_lt68` ruft alle 84 Inhalts-/Strukturregelprüfungen auf, `verify_final` führt nach LanguageTool dieselben 84 plus LT-Regel erneut aus. Das bleibt zum Schutz bei geändertem Artikel sinnvoll. Das bestehende `TEXTMACHINE_SCOPE_REFERENCE.json` fordert aber `CONTENT_RULES_CHECK_ONCE_BY_OWNER; ... FINAL_STAGE_DOES_NOT_RECHECK_PASSED_CONTENT_RULES`. Empfehlung: vorhandene unverändert gebundene Belege **nur bei vollständig identischem Artikel-/Regel-/Quellenzustand** wiederverwenden, nicht einfach Qualitätssperren entfernen. Umsetzung und Regression noch ausstehend.
8. **Live-/WordPress-Kategorie:** Die Kategorie **fachlich** einmalig vor K0 auswählen; K0 kann die erhaltene Zuordnung und Linkziele technisch prüfen, bei tatsächlichem Import/Live-Zustand technische Existenz/Freshness erneut absichern. Keine redaktionelle Zweitentscheidung.
9. **Quellensuche:** K0 recherchiert nach Auftragseingang selbst; die Verlässlichkeit einer neu gefundenen Quelle kann naturgemäß nicht vollständig vor K0 beurteilt werden. K0 Quellen- und Belegkontrolle bleibt; nach Textkorrekturen dürfen Zitate/Behauptungen nicht ungeprüft geändert werden.
10. **Regelkatalog und Tests:** keine der 85 artikelbezogenen Regeln wurde hier im produktiven Code verändert. Frühere QA-Aussagen „25 veraltet/fragwürdig“ oder „75% recherchierte Fakten“ sind NICHT verbindliche Löschentscheidungen und werden durch diesen geprüften Nachtrag eingegrenzt.

## 85/85-Inventar: Wann ist erneut zu prüfen?
A = fachliche Titelentscheidung nur vor K0 (K0 unverändert übernehmen). B = einmal pro gebundenem Auftrag (danach Integritätsnachweis; wenn geändert, erneut). C = nur wenn Text/Umgebung/prüfungsrelevante Grundlage neu oder geändert ist, nach Writer und Reparatur.

| Nr. | Originalregel | Prüfhäufigkeit / Zuständigkeit | Zweck / Klarstellung |
|---:|---|---|---|
| 1 | `lt68.language_zero_unresolved` | C: BEI TEXT-/DATENÄNDERUNG | Sprache/Grammatik am sichtbaren Text |
| 2 | `conclusion.hard_limits` | C: BEI TEXT-/DATENÄNDERUNG | Länge/Fazit/Textverhältnis |
| 3 | `conclusion.type_minimum_ratio` | C: BEI TEXT-/DATENÄNDERUNG | Länge/Fazit/Textverhältnis |
| 4 | `facts.conclusion_no_new_untraced_facts` | C: BEI TEXT-/DATENÄNDERUNG | Quellenbelege und verwendete Fakten |
| 5 | `facts.trace_binding` | C: BEI TEXT-/DATENÄNDERUNG | Quellenbelege und verwendete Fakten |
| 6 | `facts.trace_required` | C: BEI TEXT-/DATENÄNDERUNG | Quellenbelege und verwendete Fakten |
| 7 | `facts.trace_required_blocks` | C: BEI TEXT-/DATENÄNDERUNG | Quellenbelege und verwendete Fakten |
| 8 | `heading.duplicate_normalized_forbidden` | C: BEI TEXT-/DATENÄNDERUNG | Überschriften/Lesbarkeit/Sprachstil |
| 9 | `heading.grammatical_variety` | C: BEI TEXT-/DATENÄNDERUNG | Überschriften/Lesbarkeit/Sprachstil |
| 10 | `heading.hard_length` | C: BEI TEXT-/DATENÄNDERUNG | Überschriften/Lesbarkeit/Sprachstil |
| 11 | `heading.keyword_staccato_forbidden` | C: BEI TEXT-/DATENÄNDERUNG | Keyword-Wiederholung in Zwischenüberschriften begrenzen |
| 12 | `heading.natural_concrete_section_language` | C: BEI TEXT-/DATENÄNDERUNG | Überschriften/Lesbarkeit/Sprachstil |
| 13 | `heading.phrase_family_repetition_forbidden` | C: BEI TEXT-/DATENÄNDERUNG | Überschriften/Lesbarkeit/Sprachstil |
| 14 | `heading.target_phrase_control` | C: BEI TEXT-/DATENÄNDERUNG | Exakte Keyword-Phrase in Zwischenüberschriften erzwingen (separat von Keyword-Stakkato) |
| 15 | `links.required_roles` | C: BEI TEXT-/DATENÄNDERUNG | Struktur/Links/Textausgabe |
| 16 | `links.visible_exact` | C: BEI TEXT-/DATENÄNDERUNG | Struktur/Links/Textausgabe |
| 17 | `structure.duplicate_block_names_forbidden` | C: BEI TEXT-/DATENÄNDERUNG | Struktur/Links/Textausgabe |
| 18 | `structure.required_blocks` | C: BEI TEXT-/DATENÄNDERUNG | Struktur/Links/Textausgabe |
| 19 | `structure.required_lists` | C: BEI TEXT-/DATENÄNDERUNG | Struktur/Links/Textausgabe |
| 20 | `surface.non_template_language` | C: BEI TEXT-/DATENÄNDERUNG | Überschriften/Lesbarkeit/Sprachstil |
| 21 | `surface.repetition_forbidden` | C: BEI TEXT-/DATENÄNDERUNG | Überschriften/Lesbarkeit/Sprachstil |
| 22 | `table.canonical_classes` | C: BEI TEXT-/DATENÄNDERUNG | Tabellenaufbau und Mehrwert |
| 23 | `table.compact_cells` | C: BEI TEXT-/DATENÄNDERUNG | Tabellenaufbau und Mehrwert |
| 24 | `table.compact_labels` | C: BEI TEXT-/DATENÄNDERUNG | Tabellenaufbau und Mehrwert |
| 25 | `table.post_summary_policy` | C: BEI TEXT-/DATENÄNDERUNG | Tabellenaufbau und Mehrwert |
| 26 | `table.required_for_comparison` | C: BEI TEXT-/DATENÄNDERUNG | Beim Vergleich genau eine Tabelle |
| 27 | `table.value_required_if_present` | C: BEI TEXT-/DATENÄNDERUNG | Vorhandene Tabelle muss eigenständigen Nutzen haben |
| 28 | `title.colon_forbidden` | A: EINMAL VOR K0 | Pauschales Doppelpunktverbot im Titel |
| 29 | `title.keyword_required` | A: EINMAL VOR K0 | Exakte Keyword-Wörter in Titel-Reihenfolge |
| 30 | `type.metadata_schema` | B: EINMAL AM AUFTRAG | Feste Metadaten zu Artikelart vorhanden |
| 31 | `type.question_mark_policy` | A: EINMAL VOR K0 | FAQ-Titel mit Fragezeichen |
| 32 | `words.further_information_maximum` | C: BEI TEXT-/DATENÄNDERUNG | Länge/Fazit/Textverhältnis |
| 33 | `words.hard_total_range` | C: BEI TEXT-/DATENÄNDERUNG | Länge/Fazit/Textverhältnis |
| 34 | `words.main_text_minimum_ratio` | C: BEI TEXT-/DATENÄNDERUNG | Länge/Fazit/Textverhältnis |
| 35 | `words.section_balance_ratio` | C: BEI TEXT-/DATENÄNDERUNG | Länge/Fazit/Textverhältnis |
| 36 | `words.section_range` | C: BEI TEXT-/DATENÄNDERUNG | Länge/Fazit/Textverhältnis |
| 37 | `structure.body_h1_forbidden` | C: BEI TEXT-/DATENÄNDERUNG | Struktur/Links/Textausgabe |
| 38 | `structure.title_not_repeated_in_body` | C: BEI TEXT-/DATENÄNDERUNG | Struktur/Links/Textausgabe |
| 39 | `structure.visible_test_marker_forbidden` | C: BEI TEXT-/DATENÄNDERUNG | Struktur/Links/Textausgabe |
| 40 | `structure.machine_status_word_forbidden` | C: BEI TEXT-/DATENÄNDERUNG | Struktur/Links/Textausgabe |
| 41 | `structure.paragraph_floor` | C: BEI TEXT-/DATENÄNDERUNG | Struktur/Links/Textausgabe |
| 42 | `structure.h2_floor` | C: BEI TEXT-/DATENÄNDERUNG | Struktur/Links/Textausgabe |
| 43 | `structure.required_blocks_nonempty` | C: BEI TEXT-/DATENÄNDERUNG | Struktur/Links/Textausgabe |
| 44 | `structure.section_ids_unique` | C: BEI TEXT-/DATENÄNDERUNG | Struktur/Links/Textausgabe |
| 45 | `structure.section_order` | C: BEI TEXT-/DATENÄNDERUNG | Struktur/Links/Textausgabe |
| 46 | `structure.section_h2_exact_one` | C: BEI TEXT-/DATENÄNDERUNG | Struktur/Links/Textausgabe |
| 47 | `structure.section_paragraph_required` | C: BEI TEXT-/DATENÄNDERUNG | Struktur/Links/Textausgabe |
| 48 | `structure.list_minimum_items` | C: BEI TEXT-/DATENÄNDERUNG | Struktur/Links/Textausgabe |
| 49 | `structure.intro_first` | C: BEI TEXT-/DATENÄNDERUNG | Struktur/Links/Textausgabe |
| 50 | `structure.intro_structure` | C: BEI TEXT-/DATENÄNDERUNG | Struktur/Links/Textausgabe |
| 51 | `structure.adjacent_headings_forbidden` | C: BEI TEXT-/DATENÄNDERUNG | Struktur/Links/Textausgabe |
| 52 | `structure.faq_direct_answer` | C: BEI TEXT-/DATENÄNDERUNG | Struktur/Links/Textausgabe |
| 53 | `structure.text_between_headings_minimum` | C: BEI TEXT-/DATENÄNDERUNG | Struktur/Links/Textausgabe |
| 54 | `structure.html_balanced` | C: BEI TEXT-/DATENÄNDERUNG | Struktur/Links/Textausgabe |
| 55 | `heading.intent_binding` | C: BEI TEXT-/DATENÄNDERUNG | Überschriften/Lesbarkeit/Sprachstil |
| 56 | `heading.semantic_duplicate_forbidden` | C: BEI TEXT-/DATENÄNDERUNG | Überschriften/Lesbarkeit/Sprachstil |
| 57 | `surface.known_regression_patterns_forbidden` | C: BEI TEXT-/DATENÄNDERUNG | Überschriften/Lesbarkeit/Sprachstil |
| 58 | `surface.known_unnatural_language_forbidden` | C: BEI TEXT-/DATENÄNDERUNG | Überschriften/Lesbarkeit/Sprachstil |
| 59 | `surface.duplicate_sentence_ratio` | C: BEI TEXT-/DATENÄNDERUNG | Überschriften/Lesbarkeit/Sprachstil |
| 60 | `surface.intro_similarity` | C: BEI TEXT-/DATENÄNDERUNG | Überschriften/Lesbarkeit/Sprachstil |
| 61 | `facts.real_source_trace` | C: BEI TEXT-/DATENÄNDERUNG | Quellenbelege und verwendete Fakten |
| 62 | `facts.source_label_option_match` | C: BEI TEXT-/DATENÄNDERUNG | Quellenbelege und verwendete Fakten |
| 63 | `facts.visible_unit_fact_refs` | C: BEI TEXT-/DATENÄNDERUNG | Quellenbelege und verwendete Fakten |
| 64 | `facts.referenced_fact_exists` | C: BEI TEXT-/DATENÄNDERUNG | Quellenbelege und verwendete Fakten |
| 65 | `facts.referenced_fact_verified` | C: BEI TEXT-/DATENÄNDERUNG | Quellenbelege und verwendete Fakten |
| 66 | `facts.referenced_fact_type_allowed` | C: BEI TEXT-/DATENÄNDERUNG | Quellenbelege und verwendete Fakten |
| 67 | `facts.numeric_claim_supported` | C: BEI TEXT-/DATENÄNDERUNG | Quellenbelege und verwendete Fakten |
| 68 | `facts.fact_pack_coverage` | C: BEI TEXT-/DATENÄNDERUNG | Alle ausdrücklich als Pflicht markierten Fakten im Text verwenden (100 % dieser Auswahl) |
| 69 | `facts.trace_lexical_support` | C: BEI TEXT-/DATENÄNDERUNG | Mind. 80 % der belegten Text-Einheiten haben mindestens eine sachlich signifikante Wortüberschneidung mit ihrem Beleg |
| 70 | `facts.runtime_fact_allowlist` | C: BEI TEXT-/DATENÄNDERUNG | Quellenbelege und verwendete Fakten |
| 71 | `links.bound_pairs_exact` | C: BEI TEXT-/DATENÄNDERUNG | Struktur/Links/Textausgabe |
| 72 | `links.registry_active` | C: BEI TEXT-/DATENÄNDERUNG | Die im fertigen Text benutzten Links stehen aktiv im Register |
| 73 | `links.section_placement` | C: BEI TEXT-/DATENÄNDERUNG | Struktur/Links/Textausgabe |
| 74 | `links.relative_internal_only` | C: BEI TEXT-/DATENÄNDERUNG | Struktur/Links/Textausgabe |
| 75 | `links.further_information_position` | C: BEI TEXT-/DATENÄNDERUNG | Struktur/Links/Textausgabe |
| 76 | `links.distributed_across_blocks` | C: BEI TEXT-/DATENÄNDERUNG | Struktur/Links/Textausgabe |
| 77 | `links.runtime_roles_bound` | B: EINMAL AM AUFTRAG | Vorgegebene Linkrollen im Auftrag gebunden |
| 78 | `links.not_clustered_at_end` | C: BEI TEXT-/DATENÄNDERUNG | Struktur/Links/Textausgabe |
| 79 | `table.presence_policy` | C: BEI TEXT-/DATENÄNDERUNG | Bei Beratung/FAQ/Pflege Tabelle oder dokumentierte Ausnahme; Vergleich immer Tabelle |
| 80 | `table.minimum_rows` | C: BEI TEXT-/DATENÄNDERUNG | Tabellenaufbau und Mehrwert |
| 81 | `table.structure` | C: BEI TEXT-/DATENÄNDERUNG | Tabellenaufbau und Mehrwert |
| 82 | `conclusion.minimum_paragraphs` | C: BEI TEXT-/DATENÄNDERUNG | Länge/Fazit/Textverhältnis |
| 83 | `wordpress.semantic_category_binding` | C: BEI TEXT-/DATENÄNDERUNG | WordPress-Kategorie ist technisch gültig gebunden; keine neue redaktionelle Zuordnung |
| 84 | `intro.orientation_sentence` | C: BEI TEXT-/DATENÄNDERUNG | Überschriften/Lesbarkeit/Sprachstil |
| 85 | `table.optional_decision_documented` | C: BEI TEXT-/DATENÄNDERUNG | Tabellenentscheidung einschließlich Ausnahmebegründung dokumentieren |

## Konkreter KISS-Auftrag für Folge-Chat, ausdrücklich ohne Änderung derzeit
1. Zielvertrag „Einmalige SEO-Entscheidung vor K0; K0 Textproduktionsmaschine“ mit den 3 Titelschnittstellenregeln abgleichen, nicht blind auf K0-Kanonbranch löschen. Der bestehende `K0_WRITER_DRAFT_TITLE_MISMATCH`-Schutz wird gebraucht.
2. Exakte H2-Zielkeyword-Phrase (1–2) separat vom **unverändert beizubehaltenden** Anti-Stakkato-Cap diskutieren; der 3er-Handoff von 10.11.26 ist Pflicht-Regression.
3. Keine der anderen **82** K0-Artikelregeln, insbesondere **nicht** Wortzahlen, Absätze, Überschriften-Anzahl, Section-Grenzen, Längenverhältnisse, Listen/Tabellen, Phrasen-/Fakten-/Quellensicherung, ohne eindeutigen Vertrag und vollständigen Nachweis ändern.
4. Als **getrennte optionale KISS-Optimierung** einmalige Prüfung und unveränderte, signierte Belege nach LT wiederverwenden, falls vollständig unverändert; bei Änderungen Prüfschleife beibehalten, einschließlich Folgewirkungen.
5. Erst nach isoliertem K0-Kopietest + unverändertem K0-Batch-/WordPress-Draft-Schutz, negativem Datei-/Fakten-/Sprach-/Link-Test und nachweisbarem Rollback in den aktuellen Produktionsbranch übernehmen.

**QA_STATUS=85/85 inventoried with once-or-after-edit tags; NO_PRODUCTION_CHANGE; NO_RULE_REMOVED; POST_LT_OPTIMIZATION_NOT_IMPLEMENTED; USER_TEXT_RULE_LOCKED.**
