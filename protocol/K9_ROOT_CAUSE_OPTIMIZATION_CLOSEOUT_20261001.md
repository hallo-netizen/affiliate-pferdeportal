# K9 Root-Cause Optimization Closeout — 2026-10-01

## Scope
Post-STOP optimization of the real 3-article production batch without lowering or replacing any quality gate.

Preserved gates:
- LanguageTool 6.8
- PPM 6.7.9
- PSERC
- ENDSTEMPEL
- WordPress verify
- publish_allowed=false

Real completed batch:
- external batch sha256: 7e432df903a68c6a1a0a08dedcffa005647917b690de34c5180cb0b27ac897d1
- article_count: 3
- final WordPress sha256: abb27e9ee6755de53c881e45e511a16faa0071ac14b91d38c061aa51138f11de

## Root causes found

### 1. Rules existed but were not compiled into a concrete first-draft plan
The writer received rule sources, but still had to infer the concrete article envelope from them. This caused avoidable first-pass violations around word budgets, section balance, H2 constraints, table compactness, portal links, fact traces and PPM requirements.

### 2. Writer checks still exposed failures in waves
Independent gates were executed in a sequence where a blocking result could prevent later findings from being visible in the same attempt.

### 3. Structural validation also had first-failure behavior
Even when the outer writer preflight collected gate results, several structural checks still raised on the first structural finding.

### 4. Valid domain vocabulary caused repeated LT spelling loops
A small static equine dictionary existed, but new valid topic/category terms could still appear as spelling findings and be handled only after a failed writer attempt.

### 5. Finalizer still discovered content/state errors too late
PSERC trace integrity and WordPress ledger readiness could fail only after all article checks had already completed.

### 6. Failed writer diagnostics required log inspection
The next repair attempt did not have one durable machine-readable all-findings package as the single source of repair work.

### 7. One-time recovery code remained after the real batch
Emergency recovery tooling was useful for the incident but was not suitable as permanent production architecture.

## Implemented root fixes

### Compiled writer acceptance plan
Added k9_writer_plan.py.
WRITE and REPAIR jobs now receive a deterministic, hash-bound acceptance plan containing:
- exact structure requirements
- hard and preferred word budgets
- section-size bounds
- H2 limits
- table limits
- exact portal-link placements
- all required fact ids and one-trace-per-fact rule
- LT 6.8 requirements
- authoritative domain terms
- exact PPM 6.7.9 authoring requirements

### Collect-all writer preflight
k9_write_packager.py now gathers independent findings from:
- structural preflight
- writing-rule preflight
- LanguageTool 6.8
- PPM 6.7.9
and also collects failures across all items in a writer batch.

### Collect-all structural guard
Added quality/k9_structural_guard.py.
It reports all detectable structural findings in one pass. The original hard validator remains as a backstop after a clean structural guard result.

### Authoritative LT domain terms
LanguageTool spelling exceptions can now be derived only from exact authoritative article metadata and bound portal labels.
Safety remains fail-closed:
- only exact token matches
- only GERMAN_SPELLER_RULE may be ignored for those terms
- grammar and every other LT rule remain blocking
- unknown/misspelled variants remain blocking

### Persistent writer all-findings package
Failed writer preflight now persists:
runtime/WRITER_PREFLIGHT_FINDINGS.json
Current points directly to that package and requires all reported findings to be repaired in one draft update.

### Terminal readiness preflight
Added k9_terminal_preflight.py.
Before finalizer dispatch it verifies:
- all article checks completed
- no repair/check work remains
- WordPress ledger state is ready
- full PSERC final integrity passes

The finalizer reuses the hash-bound PSERC PASS only if the ledger is unchanged.

### Removed incident-only recovery workflow
Removed .github/workflows/k9-finalizer-trace-recovery.yml after the permanent root fixes were in place.

## Validation

Latest persistent suite before one-time real-batch verification:
- K9 greenfield selftest run 36904112958
- 84 tests
- PASS

Coverage includes:
- positive/negative PPM binding
- positive/negative PSERC scope
- auto-chain wiring
- compiled writer plan
- authoritative LT domain terms
- batch collect-all writer diagnostics
- terminal preflight positive/negative
- structural collect-all diagnostics

One-time read-only verification was then run against the real completed 3-article batch using the actual current ledger and actual PPM/PSERC packages. The batch-specific fixture was removed again after verification so it cannot become a future-batch dependency.

## Expected workflow effect

Old behavior:
draft -> first visible error -> edit -> next error -> edit -> next gate -> edit -> finalizer surprise

New behavior:
compiled acceptance plan -> draft -> one collect-all preflight -> one complete repair pass if needed -> native check -> terminal readiness preflight -> finalizer/stamp/export

This does not guarantee that every future article will always pass on the first draft. It does guarantee that independently detectable failures are surfaced together as early as possible instead of intentionally being revealed one by one.

## Next production validation
Use the next explicit real WordPress metadata batch through the normal existing K9 start route. Do not reopen or modify the completed 3-article batch. Measure:
- writer attempts per article
- repair cycles per article
- late finalizer content/state failures
- whether any finding appears only after a previous independent finding was repaired

Acceptance target:
- no regression in any quality gate
- no repeated one-error-at-a-time diagnostic loop
- finalizer discovers no article-quality defect that terminal preflight could have detected


## Zusatzschluss nach hartem 3er-Lauf-Review

Zwei weitere Schleifenursachen wurden nach dem realen 3er-Lauf geschlossen, ohne irgendein Qualitätsgate oder eine Schwelle zu verändern.

### 1. Quellen-Traces sind jetzt vollständig maschinengeführt
Der Writer darf die unsichtbaren `ppm-source-trace`-Tags nicht mehr als eigenständige Verantwortung tragen. Vor der Writer-Abnahme entfernt der Packager vorhandene leere Trace-Tags und erzeugt aus der versiegelten Recherche deterministisch exakt einen kanonischen Trace pro Fakt.

Damit kann der reale Heutaschen-Fehler „derselbe Fakt zweimal getraced“ nicht mehr als Writer-Schleife entstehen. Sichtbarer Artikeltext bleibt unverändert.

### 2. Konkreter First-Pass-Wortbauplan
Der Writer erhält zusätzlich zu den unveränderten harten Regeln einen daraus berechneten sicheren Schreibkorridor pro Artikeltyp:
- konkrete Zielspanne je normalem Hauptabschnitt;
- konkrete Zielspanne fürs Fazit;
- konkrete Zielspanne für „Weiterführende Informationen“;
- Mindestziel für Nicht-Tabellen-Wörter.

Der Bauplan ist nur ein Sicherheitsziel innerhalb der bestehenden Grenzen. Er ersetzt oder lockert keine Regel. Sein unterer Zielrand ist so berechnet, dass der harte 750-Wörter-Nicht-Tabellen-Floor bereits beim ersten Entwurf erreicht werden kann, statt erst im CHECK aufzufallen.

### Evidence
- deterministische Trace-Ownership: commits `d4ad60ec8cbfabe11881e2ddf1575ff71c027291`, `87359f157599fe7e9cf0ca838763b8a8683d7341`, `e3f91e0228080d36da0403b4ef1b933483b9b65b`;
- konkreter First-Pass-Bauplan: `ffeaf77558ab24ccff2463ddc607653e096ad983`;
- Regressionstests: `09223477efdf336222747ac3050904bc259dbb96`, `f93f11a0f88e447af9d132cab4814f626b80141f`;
- vollständiger K9 greenfield selftest auf aktuellem HEAD: Run `36904919863` — SUCCESS.

## Ergebnis der Ursachenprüfung

Die reale Schleifenursache war nicht „zu strenge Qualität“, sondern zu späte bzw. zu verteilte Regelanwendung:
1. harte Regeln waren vorhanden, aber noch nicht als kompakter First-Pass-Akzeptanzplan verdichtet;
2. unabhängige Writer-/Struktur-/LT-/PPM-Fehler wurden früher teilweise nacheinander sichtbar;
3. Fachbegriffe aus autoritativen Metadaten wurden von LT 6.8 unnötig als Rechtschreibfehler behandelt;
4. unsichtbare Quellen-Traces lagen teilweise beim Writer statt vollständig in deterministischer Maschinenhand;
5. Finalizer prüfte Zustände/PSERC, die vorher noch nicht vollständig als Terminal-Readiness geprüft waren.

Diese fünf Ursachen sind jetzt geschlossen. Der nächste echte Batch dient ausschließlich der Messung, ob die erwartete Wirkung real eintritt: deutlich weniger Writer-Versuche, höchstens ein gebündelter Reparaturdurchgang pro Artikel und keine neuen Content-/State-Fehler erst im Finalizer.


## Offene redaktionelle Nachprüfung nach Nutzerreview — H2 und Tabellen

Nach dem technisch vollständig abgeschlossenen 3-Artikel-Lauf hat der Nutzer den finalen FAQ-Beitrag „Was ist eine Longierpeitsche?“ inhaltlich geprüft.

### Befund 1 — Tabelle
Die aktuelle K9-Regel erzwingt global exakt eine Tabelle (`table_count_exact: 1`) und führt bei FAQ den Block `table` als Pflichtblock.

Im Longierpeitschen-FAQ ist die Tabelle formal regelkonform, aber ihr inhaltlicher Mehrwert ist fraglich:
- „Funktion / Hilfe beim Longieren / ergänzt Stimme und Leine“
- „Ausrüstung / Teil der Ausrüstung / für das Longieren vorgesehen“
- „Sicherheit / Position und Handhabung / sichere Technik erhält Kontrolle“
- „Einsatz / klar und pferdegerecht / Angst und Schmerz vermeiden“

Die Tabelle verdichtet hier überwiegend bereits unmittelbar zuvor erklärten Inhalt und erzeugt dadurch den Eindruck eines Pflichtformats statt eines echten Informationsgewinns.

Offene fachliche Frage:
Soll die Tabelle künftig nur dann Pflicht sein, wenn sie einen eigenständigen Vergleichs-, Auswahl-, Strukturierungs- oder Überblicksmehrwert liefert, statt in jedem Artikel zwingend vorhanden zu sein?

### Befund 2 — Zwischenüberschriften
Die aktuelle H2-Policy verhindert Wiederholung, Keyword-Stakkato und überlange H2. Sie lässt aber weiterhin formal korrekte, jedoch abstrakte Metaformulierungen zu, zum Beispiel:
- „Funktion beim Longieren verständlich erklärt“
- „Hilfen beim Longieren sinnvoll abstimmen“
- „Ausrüstung beim Longieren einordnen“

Diese Überschriften benennen den Abschnitt, wirken aber eher redaktionell-generiert als natürlich gesprochen bzw. leserorientiert.

Offene fachliche Frage:
Soll die H2-Regel zusätzlich verlangen, dass die Überschrift einen konkreten Leserinhalt, eine konkrete Frage, einen konkreten Nutzen oder eine konkrete Aussage des folgenden Abschnitts natürlich benennt und abstrakte Meta-Verben wie „einordnen“, „erklären“, „abstimmen“ nur verwendet werden, wenn sie in diesem konkreten Abschnitt wirklich natürlich sind?

### Arbeitsgrenze
- Der abgeschlossene 3-Artikel-Batch bleibt unverändert und wird nicht wieder geöffnet.
- Keine Qualitätsgate-Schwelle wird gesenkt.
- Vor einer Regeländerung zuerst kritische redaktionelle Bewertung am finalen Longierpeitschen-Beispiel und Gegenprüfung an weiteren vorhandenen Artikelformen.
- Erst danach minimal entscheiden, ob und wie Tabellenpflicht und H2-Natürlichkeit geändert werden.
