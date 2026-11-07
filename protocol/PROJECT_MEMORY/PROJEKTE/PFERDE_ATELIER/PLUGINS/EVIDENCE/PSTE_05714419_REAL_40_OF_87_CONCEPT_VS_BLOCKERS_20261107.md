# Pferdeatelier PSTE 0.57.144.19 — REAL-Lauf und Konzeptvergleich (07.11.2026)

**Basis:** Nutzer-JSON `pste-stapelbericht-2026-11-07(2).json`, generated_utc `2026-11-07T11:36:58Z`; WordPress `pste_version=0.57.144.19`; `RUNNING` **40/87** verarbeitet, **47 PENDING**, **7 PASS, 32 HELD, 1 BLOCKED**, 0 Transportfehler. Die zwei im Chat eingereichten Berichte sind identisch. NICHT als Endergebnis von 87 ausgeben.

## Drei vereinbarte Kategoriepfade
1. **Fach OBEN** – vorhandene passende Fachkategorie.
2. **Magazin UNTEN** – vorhandene passende Magazinkategorie.
3. **Redaktionszwischenbüro** – kein sicherer passender bestehender Ort; Thema behalten und Kategorieentscheidung zur Bearbeitung sammeln. Keine automatische neue WordPress-Kategorie erzwingen.

In GitHub `CURRENT_STATE.md` ist dieser KISS-Dreifachweg ausdrücklich festgelegt. Der aktuelle Plugin-Code (`PSTE_Normal_Metadata_Path::applyToPayload`) gibt bei fehlendem Kategorienmatch `STRUCTURE_GAP` + `structure_gap_backlog_required=true` + `PSTE_TITLE_READY_CATEGORY_DECISION_OPEN` zurück. `PSTE_Admin::processOneTitleDeskReentry` erklärt jedoch **jedes Nicht-YES** zu `HELD` mit generischem `PSTE_TITLE_DESK_REENTRY_OWNER_NOT_READY`; dadurch wirkt eine normal eröffnete Redaktionsaufgabe wie ein fehlgeschlagener Transfer. **Nicht ohne weitere Daten behaupten, ob/wo der jeweilige Auftrag in der WordPress-Redaktionsbürooberfläche sichtbar ist**; Bericht allein beweist nur die Vormerkung im gespeicherten Themenstatus.

## Aufteilung der 33 nicht erfolgreichen bearbeiteten Fälle (gegenseitig exklusiv)
- **21 Kategorie-/Artikelart offen:** 18 mit `PSTE_TITLE_READY_CATEGORY_DECISION_OPEN` als erster Ursache + 3 mit `PSTE_INTENT_PRIMARY_TYPE_CANDIDATE_MISSING` als erster Ursache und zugleich `PSTE_TITLE_READY_CATEGORY_DECISION_OPEN`. Kein Grund, den Titel neu zu schreiben oder erneut auf Relevanz zu prüfen.
- **11 Planungssperren:** 7 `PRE_TITLE_ACTIVE_TITLE_CONTAINS_SOURCE_QUERY` (existierender WP-Titel enthält ganze Quellfrage; Bericht enthält KEINE konkreten Trefferartikel), 1 `BROAD_SCOPE_EXISTING_SEO_KEYWORD_UNKNOWN_FAIL_CLOSED` (Bestandsartikel ohne bekanntes Zielkeyword), 1 `QUESTION_TITLE_NOT_FAQ` (Fragetitel ohne FAQ-Typ), 1 `CATEGORY_HEAD_INTENT_COLLISION` (Thema deckt Kategorie-Head ab), 1 `NON_EDITORIAL_TRANSACTIONAL_QUERY` (Kaufsuche). Für alle Schutzmechanismen gilt: Beleg gegen tatsächlichen WP-Beitragsbestand prüfen, nicht pauschal entfernen.
- **1 Produktauswahl:** `PSTE_PRODUCT_CHOICE_CANDIDATE_RETAINED` + `PSTE_PRODUCT_CHOICE_DOWNSTREAM_NOT_REGISTERED`, gesondert `BLOCKED`; Nachverarbeitung im vorhandenen Workflow klären, nicht blind als normalen Artikel zulassen.

**Relevanzstatus:** Unter 40 bearbeiteten Fällen **0 `PSTE_PORTAL_RELEVANCE_NOT_PROVEN`**, die zuvor vier gesperrten Regendecken-Themen sind nun PASS; ein Wassertrog `STRUCTURE_GAP` statt Relevanzproblem. Bei 47 PENDING keine Aussage über vollständigen 87er-Fix.

## Gemeinsame Ursache statt Einzelsymptome
Der bestehende dreifache Weg wird **nicht konsistent bis zum Ergebnis des Wiedereinstiegs abgebildet**: Nicht bereit für fertigen Redaktionsplan heißt nicht grundsätzlich „Fehler“. Der bisherige Bericht bündelt Kategorie-Aufträge, möglicherweise bereits abgedeckte Themen und tatsächliche Verarbeitungssperren unter `HELD`. Nächster umfassender Arbeitsschritt: Alle 87 gegen die drei Kategorieziele routen; jeden Kategorie-Open-Fall als normal offenen Redaktionsauftrag mit prüfbarer Persistenz behandeln; 3 Intententscheidungen am EXISTIERENDEN Owner klären (nicht zweite Entscheidung bauen); alle 11 Planungssperren samt tatsächlichen Bestands-Treffern verifizieren; echten Dublettenschutz und Sicherheitsprüfungen erhalten; Produktauswahl gesondert zuordnen; anschließendes Statusreporting auf die realen drei Kategorien/Arbeitsresultate abstimmen. Kein neues Plugin/Version bloß aus diesem Diagnosebericht ableiten. K0, PSERC, fremde Büros unverändert.
