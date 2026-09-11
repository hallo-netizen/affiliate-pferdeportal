# CLAUDE FORENSIC REVIEW — STARTMASTER0107 / PR217 / LANGUAGE TOOL / WORKER-CHECKER BOUNDARY

## Auftrag
Du hast kein Vorwissen. Prüfe ausschließlich forensisch gegen den tatsächlichen Repository-Stand. Ändere keinen Code. Baue keine neue Architektur. Erfinde keine Regeln. Ziel ist die kleinstmögliche, sichere Ursachenlösung.

Repository: hallo-netizen/affiliate-pferdeportal
Aktueller Produktions-main: 5f996d5574b5b4bb33bac917c375d9539d7bf8a8
Dieser Prüf-PR: #224

## Nicht verhandelbare Regeln
- KISS.
- Kein neuer Runner, kein neues Gate, kein neuer Controller, kein Sidecar, kein Parallelweg.
- Keine Änderung an Textmaschine, Inhaltsregeln, SEO-Regeln, Link-/Tabellenregeln, LanguageTool-Regeln, PPM 6.7.9, PSERC, PSTE, Design oder Publish-Sicherheit.
- Codex besitzt keine freie Workflow-/Navigations-/Publish-Autorität.
- Worker PASS-Autorität bleibt NONE.
- stage_proofs bleibt [] im neuen Aggregate-Modell.
- all_other_actions=DENY bleibt.
- publish=false bleibt.
- 107008 bleibt Pflicht vor Publish.

## Zielprozess
Die Titel werden außerhalb dieses Systems in WordPress erzeugt. Der Nutzer lädt eine Datei herunter und gibt sie in den Prozess. Der gewünschte einfache Ablauf ist:

WordPress-Datei -> current_item eindeutig binden -> Codex schreibt/bearbeitet genau diesen Artikel -> reale Facharbeit/Fachwerkzeuge -> unabhängiger Prüfer verifiziert das fertige Ergebnis -> genau ein Gesamt-PASS -> 107008 -> STOP vor Publish.

Codex darf arbeiten und korrigieren, aber keinen eigenen PASS beglaubigen.

## Belegte Historie
Es gab einen echten 7/7-Lauf bis 107008. Themen u.a. Hindernisstangen, Reitplatzbeleuchtung, Mistcontainer, Pferdehaftpflicht, Huffett, Fliegenmasken, Pellets. Codex selbst war der gebundene Fachworkflow-Worker.

Wichtiger Stand VOR PR217:
ffcd7c8dc6451236d58002939421bf9b6b489538

Dort enthielt codex_current_action.py diese 12 Stufen:
- research_fact_pack
- textmachine_article_type_structure
- table_contract
- internal_links
- languagetool
- ppm
- pserc
- pste
- duplicate_cannibalization
- seo
- design_format
- publish_safety

WICHTIG: Der alte Handoff prüfte für 11 dieser 12 Stufen im Wesentlichen vom Worker gelieferte Proof-Strukturen/Hashes/Statusfelder. Nur PPM wurde dort nachweislich im Adapter real ausgeführt. Daher ist der alte 7/7-Lauf KEIN Beweis, dass LanguageTool oder alle anderen Stufen damals real unabhängig erzwungen wurden.

## PR217
PR217: "Hobbyraum: Gesamtbeleg statt 12 externe Stage-Proofs"
Merge: 7fcae6ad09e002903d44ff3800e6f22d9679d92e

Ziel von PR217 war sinnvoll: Codex/Worker sollte seine eigenen PASS-Zettel nicht mehr erzeugen. Stattdessen sollte ein unabhängiger technischer Prüfer reale vorhandene Validatoren benutzen und genau EINEN Gesamt-PASS erzeugen.

PR217 führte in control/startmaster0107/fachworkflow_proof_handoff.py unter anderem _run_languagetool() ein. Diese Funktion führt LanguageTool 6.8 real auf dem fertigen Artikel aus und blockiert sofort, sobald report.matches nicht leer ist:
LANGUAGETOOL_UNRESOLVED_FINDINGS:<count>

Es gibt dort aktuell keinen Korrekturrückweg zum Worker.

## LanguageTool-Runtime
Die technische LT-Runtime wurde separat bereits repariert und hashgebunden (u.a. PR207, PR210, PR213, PR214). Der aktuelle Fehler ist NICHT: LT fehlt, JAR fehlt, Hash falsch, Runtime nicht erreichbar.

Der aktuelle Live-Lauf beweist: LT wurde real ausgeführt.

## PR221 / PR223
PR221 band alte Produktionspaket-Kontexte vor R_001/107007 und führte später zu Startblockern.

PR223: "Hobbyraum: einfachen Codex-Einstieg wiederherstellen, Gesamtprüfer behalten"
Merge/current main: 5f996d5574b5b4bb33bac917c375d9539d7bf8a8

PR223 reparierte den Einstieg: current_item darf wieder direkt zur Texterstellung führen; Fact-Pack/Production-Plan/source_snapshot_id sind nicht mehr zwingende Startvoraussetzung. Der Aggregate-Prüfer blieb erhalten.

PR223 änderte NICHT die LanguageTool-Runtime oder LT-Regeln.

## Aktueller echter Live-Blocker
Im echten 7/7-Live-Test auf aktuellem main schrieb Codex den ersten frischen Artikel. Danach führte fachworkflow_proof_handoff.command LanguageTool real aus.

Ergebnis:
LANGUAGETOOL_UNRESOLVED_FINDINGS:47
FACHWORKFLOW_PROOF_HANDOFF_BLOCKED

## Bereits vorliegende unabhängige Gegenprüfung
Eine erste Claude-Analyse kam zu folgendem Kernbefund:
- Hauptthese nur TEILWEISE bestätigt.
- Vor PR217 gab es keine nachweisliche echte LT-Korrekturschleife.
- Vor PR217 war LT im Handoff im Wesentlichen Worker-Selbstattest.
- PR217 machte LT erstmals real und unabhängig, aber als Single-Shot-Hartblock ohne Rückkopplung.
- Weitere alte Stage-Namen (table_contract, internal_links, duplicate_cannibalization, seo, design_format, pste) sind im aktiven Python-Livepfad nicht mehr einzeln sichtbar; unklar ist, ob sie innerhalb PPM/PSERC/PSTE-Paketen real abgedeckt sind.

## Zu prüfende Alternativen OHNE Architekturumbau
Bewerte mindestens diese drei Varianten kritisch:

A) Alte Worker-/Prüfergrenze weitgehend wiederherstellen.
Risiko: Rückfall in Worker-Selbstbeglaubigung / nur strukturelle Proofs.

B) Im bestehenden fachworkflow_proof_handoff.py eine begrenzte LT-Rückgabe/Korrekturschleife einbauen.
Beispiel: echter LT-Lauf -> Findings strukturiert zurück -> Worker korrigiert -> maximal ein erneuter LT-Lauf -> danach finaler Prüferentscheid.
Prüfe, ob dafür wirklich ein neuer Status/Rückkanal nötig wäre oder ob dies den bestehenden Lebenszyklus unnötig erweitert.

C) KEIN neuer Rückkanal: Codex arbeitet vor finalem materialize bereits bis "prüfreif". Dafür wird derselbe bereits vorhandene LanguageTool-Runtime-Aufruf als reine Arbeitsprüfung genutzt, ohne PASS-Autorität. Codex korrigiert Findings, danach ruft derselbe unveränderte finale Aggregate-Prüfer LanguageTool nochmals unabhängig auf. Prüfe, ob dies die kleinste Lösung ist und ohne neue Architektur/zusätzlichen Raum/Controller auskommt.

## Pflichtprüfung weiterer Stufen
Prüfe nicht nur LT. Für jede Stage bestimmen:
- Wer führte sie vor PR217 tatsächlich aus?
- Wer führt sie heute tatsächlich aus?
- War/ist es echte Facharbeit, echte unabhängige Prüfung oder nur Proof-Struktur?
- Ist die Stage heute real innerhalb PPM/PSERC/PSTE enthalten? Nur maschinellen Beleg akzeptieren.

Stages:
research_fact_pack
textmachine_article_type_structure
table_contract
internal_links
languagetool
ppm
pserc
pste
duplicate_cannibalization
seo
design_format
publish_safety

Insbesondere die Runtime-ZIPs unter control/startmaster0107/runtime_packages prüfen/entpacken, soweit nötig, um table_contract/internal_links/seo/design_format/pste/duplicate_cannibalization nicht nur zu vermuten.

## Positive/negative Sicherheitsprüfung des bevorzugten KISS-Wegs
Ohne Code zu ändern, bewerte ob der bevorzugte Weg diese Garantien erhält:
- current_item eindeutig gebunden
- falscher Artikel/Slot/Batch -> BLOCK
- Worker PASS-Autorität NONE
- stage_proofs=[]
- Fake-PASS -> BLOCK
- Hash-/Adapter-Tamper -> BLOCK
- LT wirklich real auf finalem Artikel
- LT-Findings können vor finalem PASS korrigiert werden
- finaler Prüfer prüft LT erneut unabhängig
- PPM 6.7.9 real unverändert
- PSERC unverändert
- PSTE unverändert
- Link-/Tabellen-/SEO-/Design-/Duplicate-Regeln nicht verschwunden
- publish=false
- 107008 bleibt Pflicht
- all_other_actions=DENY

## Tests
Keine Implementierung. Nur sagen, welche Tests ein Kandidat zwingend bestehen müsste:
1. realistischer frischer Artikel mit absichtlichen LT-Findings -> Arbeitskorrektur möglich, KEIN PASS vor sauberem Endtest.
2. finaler Aggregate-Prüfer findet noch einen LT-Treffer -> BLOCK.
3. finaler Aggregate-Prüfer findet 0 LT-Treffer -> LT-Teil PASS.
4. Worker versucht eigenen PASS/stage_proofs -> BLOCK.
5. falscher Artikel/Batch/Slot/Hash -> BLOCK.
6. alle anderen realen Fachstufen nachweislich erhalten.
7. bestehende vollständige M01-M36 Regression PASS.
8. danach erst echter 7/7-Live-Test, publish=false, bis 107008 oder erster echter Blocker.

## Ausgabeformat
A. HAUPTBEFUND: BESTÄTIGT / TEILWEISE BESTÄTIGT / WIDERLEGT

B. URSACHE: max. 8 kurze Sätze.

C. STUFENMATRIX: für jede Stage ALT / HEUTE / echte Ausführung? / Korrekturmöglichkeit? / unabhängige Endprüfung? / Beleg.

D. ALTERNATIVEN A/B/C: jeweils Vorteile, Nachteile, Sicherheitsrisiko, Architekturaufwand.

E. EMPFOHLENER KISS-WEG: genau ein Weg. Begründe, warum kleiner/sicherer als die anderen.

F. MAXIMAL BETROFFENE BESTEHENDE DATEIEN. Keine neue Datei vorschlagen, wenn nicht zwingend.

G. GESAMTUMBAU NÖTIG? JA/NEIN mit harter Begründung.

H. NEGATIVPRÜFUNG: Welche bekannte Sicherheitsgarantie könnte der empfohlene Weg versehentlich schwächen?

I. OFFENE UNKLARHEITEN: nur Dinge, die trotz Repository-Prüfung nicht maschinell entscheidbar sind.

WICHTIG: Keine Codeänderung. Keine Implementierung. Kein Symptomfix. Nicht fragen "wie ignorieren wir 47 LT-Findings?" Sondern prüfen: "Wie bleibt LT real und streng, während die Facharbeit den Text vor dem finalen unabhängigen PASS tatsächlich korrigieren kann – und ist dieselbe Lebenszykluslücke auch bei anderen Fachstufen vorhanden?"