# SYSTEM 4A — POSITIVBEWEIS TEXTMASCHINE

Stand: 17.09.2026
Zweck: Punkt 2 des eingeschlossenen Hobbyraum-Arbeitsauftrags.

## Ergebnis

Für die in Punkt 1 abgegrenzten 153 Projekt-Textmaschinenregeln ist der Positivpfad bestimmt und real ausgeführt.

### PPM 6.7.9 — 104/104

Jeder der 104 aktiven PPM-Textregel-Einträge besitzt im unveränderten `hard-rule-registry-v1.json` einen gebundenen `positive_test` und einen echten Validatorbezug.

Verteilung der gebundenen Positivtests:
- 52 -> `tests/test-runtime-safety.php`
- 38 -> `tests/test-wave2-content-structure-language-gate.php`
- 14 -> `tests/test-wave1-known-error-gate.php`

Unabhängig von dieser Registerzuordnung ist der reale PPM-Produktionsprüfer im System-4A-Fullcheck tatsächlich ausgeführt worden: der vollständige 1-Artikel- und 3-Artikel-Realweg meldet PPM jeweils `PASS`.

### Content Guard — 31/31

`test_content_guard.py::test_positive_research_facts_pack_and_article_trace` erzeugt gültige Research-/Facts-/Fact-Pack-Daten und ruft den echten `content_guard.validate_single_article()` auf. Dieser wiederum führt `validate_fact_pack()` und `validate_article_fact_ids()` aus und liefert `PASS`. Damit ist der gültige Positivzustand der 31 Fullcheck-Regeln am echten Prüfer gebunden.

### Design Guard — 16/16

`test_design_guard.py::test_existing_canonical_design_passes_without_mutation` führt den echten `design_guard.validate_design_neutrality()` mit kanonischem Beratung-HTML aus und erwartet `PASS`; Tabelle, Root-Klassen und Typbindung werden real geprüft und der Body bleibt unverändert.

### External-Link-Regeln — 2/2

`production_checks.run_all()` führt `no_external_links(article_html)` zwingend vor LT/PPM aus. Der vollständige reale 1- und 3-Artikel-Weg ist PASS; damit ist der gültige Artikel ohne externe Links real durch genau diesen Prüfer gelaufen.

### LanguageTool 6.8 — externer dynamischer Prüfer

Der Acceptance-Workflow lädt LanguageTool 6.8 hashgebunden, führt den echten Prüfer im Fullcheck aus und verifiziert für 1 Artikel `lt == ['PASS']` sowie für 3 Artikel `lt == ['PASS','PASS','PASS']`.

## Remote-Beleg

Workflow: `System 4A Real LT68 PPM679 Acceptance`
Run: `35137504179`
Head: `73d791fd8d9a988c3119db4b3d822b38e54302dd`
Ergebnis: `SUCCESS`

Der aktuelle Hobbyraum-Branch liegt exakt auf diesem Head plus ausschließlich:
- Repair-/Hard-Block-Klassifikationsänderung in `isolated_system4/production_checks.py`
- Hobbyraum-Dokumentation.

Die Positiv-Prüfengine `production_checks_engine.py`, `content_guard.py`, `design_guard.py`, PPM-Paket und Acceptance-Workflow sind gegenüber dem belegten Head unverändert. Die neue Klassifikationsschicht greift nur im Fehlerpfad und verändert keinen PASS-Pfad.

## Ergebnis Punkt 2

**POSITIVBEWEIS = PASS für 153/153 Projektregeln; LanguageTool-Positivpfad real PASS.**

Dies beweist ausdrücklich noch nicht Punkt 3 (gezielter Negativbeweis je Regel).