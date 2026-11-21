# Hab & Bewahr: statische Gegenprüfung Original-K0 gegen K-Multi und die fünf Hab-Typen
**Datum: 19.11.2026. Status: PRÜFPROTOKOLL. KEINE FREIGABE UND KEINE REGELÄNDERUNG.**

## 1. Beweissituation
Direkt gelesen (nicht aus älteren Chatbehauptungen erschlossen):
- aktueller Original-K0: `hallo-netizen/affiliate-pferdeportal`, `konzept0-portal-neutral-20261002`: `RULE_CATALOG.json`, `RULE_VALUES.json`, `FIELD_POLICY.json`, `ARTIKELTYPEN/Anleitung.json`.
- K-Multi Entwicklungszweig: `hallo-netizen/k0-multiportal`, `k0-offline-rule-bindings-20261027`: `offline_rules/shared/RULE_CATALOG.json`, `offline_rules/pferdeatelier/RULE_VALUES.json`, `offline_rules/shared/FIELD_POLICY.json`, `offline_rules/OFFLINE_RULE_BINDINGS.json`, `offline_rules/OFFLINE_WRITER_INTEGRATION_V9.json`.
- alle fünf bereits vorhandenen Hab-Fachentwürfe im `BEITRAGSARTEN_HAB_V1`-Ordner.

## 2. Automatischer statischer Regelvergleich – echte Ergebnisse
- Original-K0: **117** Regelkatalog-Einträge.
- K-Multi: **121** Einträge.
- Gleiche Kennung und **vollständig gleicher Eintragsinhalt** bei allen **117** gemeinsamen Regeln.
- **4 zusätzliche alte K-Multi-Regeln** (nicht mehr im aktuellen K0): `heading.target_phrase_control`, `title.colon_forbidden`, `title.keyword_required`, `type.question_mark_policy`.
- Aktuelle K0-Regeln, die in K-Multi ganz fehlen: **0** (der Vergleich gilt nur für diesen Katalog, nicht für die gesamte lauffähige Prozesskette).
- `RULE_VALUES.json` hat **17 Feldabweichungen**. Ihre betroffenen Bereiche sind Quellenmarker-Darstellung, Linkpolitik, Titel- und Fragestellungs-Vorgaben sowie der exakte H2-Keyword-Zwang. Die Zahlen sind kein Beleg für lauffähiges Multi.
- **Wortlängen identisch:** Beide haben 750–900 Wörter, mindestens 4 H2/16 Absätze, 100–220 Wörter pro regulärem H2-Abschnitt. **Keine Änderung vorgeschlagen oder ausgeführt.**
- Original-K0 `FIELD_POLICY.json` beschreibt alte Titel-/Fragezeichen-/Keyword-Vorgaben als überholt bzw. an vorgelagerten Eigentümer verlegt. K-Multi-Feldpolitik dokumentiert diese Verlagerungen noch nicht vollständig.
- **Entscheidung für eine spätere Angleichung nötig:** Nicht allein wegen geringerer Regelzahl behaupten, Qualitätsregeln seien abgebaut. Vier weggefallene Einträge wurden laut aktueller Feldpolitik ersetzt oder an die richtige Stelle verlegt. Nur am originalen Prüf-Eigentümer und mit Regression vergleichen.

**Einzelfelder mit bewiesener Differenz:**
- `global.source_trace.authoring_rule`: K0="Quellen bleiben nachweisbar. Der Quellenmarker selbst enthält niemals sichtbaren Text. Quellen- und Markennamen dürfen im lesbaren Artikel nur als sinnvoller Bestandteil eines vollständigen Satzes stehen, nicht lose angehängt." / Multi="(nicht vorhanden)"
- `global.source_trace.marker_visible_content_forbidden`: K0=true / Multi="(nicht vorhanden)"
- `global.visible_links_min`: K0=1 / Multi="(nicht vorhanden)"
- `global.visible_links_max`: K0=3 / Multi="(nicht vorhanden)"
- `global.mandatory_link_roles`: K0=["parent_category"] / Multi="(nicht vorhanden)"
- `global.link_count_policy`: K0="MEANINGFUL_1_TO_3_SINGLE_PREWRITER_DECISION" / Multi="(nicht vorhanden)"
- `global.title_colon_forbidden`: K0="(nicht vorhanden)" / Multi=true
- `global.title_keyword_required`: K0="(nicht vorhanden)" / Multi=true
- `heading.exact_target_phrase_occurrences_max`: K0="(nicht vorhanden)" / Multi=2
- `heading.exact_target_phrase_occurrences_min_when_no_title_collision`: K0="(nicht vorhanden)" / Multi=1
- `heading.exact_target_phrase_occurrences_when_title_equals_target`: K0="(nicht vorhanden)" / Multi=0
- `ppm_parity.links.minimum_required_count`: K0=1 / Multi="(nicht vorhanden)"
- `ppm_parity.links.maximum_allowed_count`: K0=3 / Multi="(nicht vorhanden)"
- `types.Beratung.question_mark`: K0="(nicht vorhanden)" / Multi="OPTIONAL"
- `types.FAQ.question_mark`: K0="(nicht vorhanden)" / Multi="REQUIRED"
- `types.Pflege.question_mark`: K0="(nicht vorhanden)" / Multi="OPTIONAL"
- `types.Vergleich.question_mark`: K0="(nicht vorhanden)" / Multi="OPTIONAL"

## 3. Artikelarten-Abgleich
| Hab-Fachart | Tatsächliche K0-Grundlage | K-Multi-Status | Urteil |
|---|---|---|---|
| FAQ | `RULE_VALUES.types.FAQ` | Hab `NO_VALUES_BLOCKED` | Fachkopie sinnvoll; aktuell nicht abrufbar |
| Ratgeber & Wissen | `Beratung` nur bei echter Auswahl | Hab `NO_VALUES_BLOCKED` | Reines Erklärwissen **nicht** als Beratung mit erfundenen Kriterien tarnen |
| Vergleich | `RULE_VALUES.types.Vergleich` | Hab `NO_VALUES_BLOCKED` | Weitgehende inhaltliche Übernahme sinnvoll; technisch noch nicht abrufbar |
| Anleitung & Checkliste | Original `ARTIKELTYPEN/Anleitung.json` READY und zusätzlich `types.Pflege` | Multi 4 Originaltypen, keine Anleitung-Bindung | Ein Hab-Regelpaket kann zwei sinnvolle Aufbauformen enthalten; deren vorhandene Verträge unterscheiden sich |
| Bericht & Praxisfall | Kein Originaltyp `Bericht` im geprüften Bestand | Hab `NO_VALUES_BLOCKED` | Neue fachliche Regeln nötig; Magazin-WP-Kategorie ebenfalls offen |

- Die geprüfte K-Multi-Bindung hat `production_enabled=false`, `publish_allowed=false`, `hab_und_bewahr.state=NO_VALUES_BLOCKED`, `implicit_values_fallback_allowed=false`; Status der isolierten Writer-Integration: `full_original_k0_writer_station_run=false`. **Kein echter Writer-/LT-/WordPress-Endtest durchgeführt.**
- Die fünf Hab-Dateien enthalten noch `gemeinsame_regeln` und `hab_querschnitt`-Verweise. Es sind **fünf separat abgelegte Fachentwürfe**, noch **keine fünf fachlich eigenständigen Vollpakete**. Keine der fünf Dateien im Rahmen dieser Prüfung editiert.

## 4. Prüfmatrix nach Leserabsicht (10 statische Zuordnungen, KEIN K0- oder K-Multi-Test)
1. **FAQ** – „Was bedeutet RC2 bei Fenstern?“; Nutzerziel: Eine konkrete Frage schnell beantwortet bekommen. Fachlicher Hinweis: Sicherheitsnorm / Wirkungsgrenze.
2. **FAQ** – „Zahlt die Hausratversicherung bei Fahrraddiebstahl?“; Nutzerziel: Einzelne vertragliche Frage beantworten. Fachlicher Hinweis: Echte Vertragsbedingungen.
3. **Ratgeber & Wissen** – „Ferienhaus bei längerer Abwesenheit sichern“; Nutzerziel: Allgemeines Schutzproblem verstehen und planen. Fachlicher Hinweis: Restgefahr, Ausfall, Nutzung.
4. **Ratgeber & Wissen** – „Wie entsteht Rückstau im Keller?“; Nutzerziel: Neutral fachliche Ursachen erklären. Fachlicher Hinweis: Gefahrenart, sichere Erklärung, keine Schein-Kaufentscheidung.
5. **Vergleich** – „Funkalarm gegen Kabelalarm“; Nutzerziel: Zwei Systeme anhand gleicher Kriterien auswählen. Fachlicher Hinweis: Ausfallsicherheit, Betriebsaufwand, Evidenz.
6. **Vergleich** – „Hausrat-Außenversicherung Tarif A und Tarif B“; Nutzerziel: Zwei Vertragsvarianten anhand echter Unterlagen vergleichen. Fachlicher Hinweis: Originalpolicen / Stand.
7. **Anleitung & Checkliste** – „Rauchmelder nach Herstellerangaben prüfen“; Nutzerziel: Einmalige sichere Handlung Schritt für Schritt. Fachlicher Hinweis: Original-Anleitung, Laiengrenze.
8. **Anleitung & Checkliste** – „Wohnmobil vor Abwesenheit regelmäßig prüfen“; Nutzerziel: Wiederkehrende Kontrollliste anwenden. Fachlicher Hinweis: Original-Pflege: andere Blöcke als Anleitung.
9. **Bericht & Praxisfall** – „Amtlicher Bericht über Starkregenereignis“; Nutzerziel: Belegten Vorfall sachlich darstellen. Fachlicher Hinweis: Quelle, Ort, Datum, Korrektur.
10. **Bericht & Praxisfall** – „Polizei meldet Einbruchzahlen“; Nutzerziel: Belegte aktuelle Statistik einordnen. Fachlicher Hinweis: Bezugsgröße, Veröffentlichungsdatum, Überdehnungsverbot.

**Kritischer Grenzfall:** Eine Frage im Titel (`Was tun nach einem Einbruch?`) ist nicht automatisch FAQ. Wird eine sofortige sichere Handlungsliste gewünscht, passt Anleitung/Checkliste; soll die Frage knapp beantwortet werden, passt FAQ; wird Vorsorge erklärt, passt Ratgeber. Die **einzige** Leserabsichts-Entscheidung findet vor K0 statt, nicht in einem neuen Writer-Modul.

## 5. Priorisierte, bislang NICHT freigegebene Entscheidungen
1. **Textlänge unverändert lassen** (750–900), bis gegebenenfalls anhand **echter** Beispielartikel eine andere schriftlich beschlossene Lösung vorliegt. Keine Kurz-FAQ-Ausnahme auf Vorrat.
2. **Bestehende Regeln wörtlich/wertgleich kopieren**, vor allem Quellen-, Struktur-, Sprach-, Tabellen-, Link- und Qualitätsvorgaben. Ausnahmen nur einzeln und vorab vom Nutzer beschlossen.
3. **Ratgeber ohne Schein-Kaufentscheidung:** eigene Hab-Struktur für neutralen Wissensartikel; bei einem Auswahl-Ratgeber existierende Beratungsregeln verwenden. Eine Hab-Art mit einem eindeutig vor K0 geplanten passenden Aufbau, keine zweite Artikelartentscheidung.
4. **Anleitung & Checkliste:** einmalige und wiederkehrende Handlung nach der bereits vor K0 festgelegten Leserabsicht abbilden. Zwei sachlich unterschiedliche Ursprungs-Pflichtstrukturen nicht heimlich zusammenwerfen.
5. **Bericht:** Original-Hardchecks (inklusive Länge) beibehalten, fachlich neue Fall-/Zeit-/Quell-/Datenschutzstruktur nur mit Zustimmung. Berichte nur über tatsächlich belegte Fälle, reale Magazin-WP-Termbindung noch nicht nachgewiesen.
6. **Eigene Hab-Spezialregeln pro Typ:** genau bei inhaltlicher Relevanz kopieren; in der Quellabnahme prüfen, ob eine Fachwarnung tatsächlich erforderlich ist. Keine pauschalen Warnungen in jedem Text.
7. **K-Multi erst nach eigener separater Freigabe angleichen**: Der Katalogunterschied allein rechtfertigt keine ungenehmigte Änderung; die vier abweichenden Altregeln und alle 17 Feldabweichungen gehören in *eine* zentrale, rückbaufreie technische Regression.

## 6. Schutz vor unbeabsichtigten Änderungen
- Keine der fünf Hab-Regeldateien, keine Basis-Hilfsregeldatei, keine K0-/K-Multi-Datei, kein Plugin und kein WordPress geändert.
- Dieses Dokument ist eine **schreibgeschützte Fach- und Ist-Zustands-Prüfung**, kein programmatisch ausführbares Regelpaket.
- Erst nach **ausdrücklicher Zustimmung zur jeweiligen fachlichen Änderung** werden fünf autarke Hab-Vollpakete als neue Entwurfsfassungen gefertigt. Erst nach Originaltests können sie technisch READY werden.
