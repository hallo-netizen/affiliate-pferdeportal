# STARTMASTER0107 — Konzept 6 Speed/Repair/Textmaschine Closeout — 2026-09-26

**Rolle:** HISTORIE / NACHWEIS. **Keine CURRENT- oder NEXT-ACTION-Autorität.**  
Operative Wahrheit bleibt ausschließlich `control/startmaster0107/CURRENT_STATE.json`.

## Zielvertrag

Autoritative Zielquelle:
`control/startmaster0107/ZIELVERTRAG_REASONING_MEDIUM_MAX_STARTMASTER0107.json`

Ziel unverändert:
`MAXIMIZE_MEDIUM_WITHOUT_ANY_GATE_OR_QUALITY_CHANGE`.

Unverändert bleiben insbesondere LT 6.8, PPM 6.7.9, PSERC, ENDSTEMPEL, Design, Publish-Sicherheit und `publish_allowed=false`.

## Arbeitsbindung / Fallbacks

- Main / Konzept-5-Basis: `48eaad387df2a24c9de94e5f0a8210dd22f2ba32`
- Konzept 5 frozen: `fallback/konzept5-frozen-20260926` @ `48eaad387df2a24c9de94e5f0a8210dd22f2ba32`
- Konzept 6 Working Copy: `konzept6/working-copy-20260926` @ `e5ae051caf3c383bb02b9640bd108693343db916`
- Konzept 6 technischer Rückfallpunkt: `konzept6/tech-stable-20260926` @ `2371dae7cc6adaf17c27c4358effe0e5589465da`
- Konzept 6 Rückfallpunkt direkt vor Textmaschinenarbeit: `konzept6/pre-textmachine-stable-20260926` @ `e5ae051caf3c383bb02b9640bd108693343db916`

Konzept 5 wurde in diesem Arbeitsstrang nicht verändert.

## Was tatsächlich gemacht wurde

### 1. Finale 16er-Ausgabe / ENDSTEMPEL

GitHub Actions Run `36270302507`: SUCCESS.

Nachweis:
- Batch SHA-256: `df59b8428c5e3f0750c5523091c00a1172975109823ee816d2234cf9052505d0`
- Artikel: 16
- final SHA-256: `02a7d66732176106d1ef49640f27c34ff2a4523d6b7b8eaefa5e74f74b9fe359`
- `publish_allowed=false`
- `content_mutation_performed=false`
- Durable Release erzeugt:
  `konzept6-endstempel-df59b8428c5e3f0750c5523091c00a1172975109823ee816d2234cf9052505d0-g000001`

### 2. Rein technische Beschleunigung

Nur Konzept 6:
- PPM-6.7.9-Runtime wird hashgebunden wiederverwendet statt bei jedem Check neu entpackt.
- LanguageTool-Runtime-Suche nutzt einen bereits bekannten, hashverifizierten Pfad.
- unveränderliche PPM-Autoritätsmetadaten werden im Prozess wiederverwendet.

Run `36271582092`: SUCCESS.

Messung über 16 bereits fertige echte Artikel:
- 16/16 PASS
- Gesamt-Prüfzeit: 29.178 s
- erster kalter Artikel: 14.362 s
- warme Artikel Durchschnitt: 0.988 s
- warm max: 1.444 s
- warm min: 0.808 s

Keine Qualitätsregel, Prüfreihenfolge oder PPM/LT-Regel wurde dafür geändert.

### 3. A — vorhandene Regeln vor dem Schreiben vollständig geben

Konzept 6 wurde erweitert, damit der Schreiber vor `WRITE_DRAFT` den bereits gebundenen Authoring-Vertrag exakt erhält.

Run `36272223094`: SUCCESS.

Belegt:
- vorhandene Regeln werden vor dem Schreiben transportiert;
- der vorbereitete Workspace exponiert den exakten gebundenen Authoring-Vertrag;
- keine neue Qualitätsregel erzeugt.

### 4. B — alle Findings eines einzelnen Prüflaufs gemeinsam übergeben

Konzept 6 wurde erweitert, damit bei `REPAIR_REQUIRED` das vollständige Findings-Paket desselben Prüfers gemeinsam zum selben Artikel/Writer zurückgeht.

Run `36272430191`: SUCCESS.

Nicht geändert:
- LT bleibt vor PPM;
- LT und PPM werden nicht zu einem neuen Super-Prüfer zusammengelegt;
- Same-Article-Repair bleibt erhalten.

### 5. Frischer Beratungsartikel — realer Repair-Test

Testartikel:
`concept_agent/konzept6/live_writer_probe/00_reitplatzplaner_fresh.md`

Fehlerfolge:

1. Run `36272135733`: FAILURE  
   `PREWRITE_SOURCE_TRACE_MISMATCH:fact-rp-0-c`  
   Ursache im Test: der erste Vorab-Informationsweg enthielt nicht den vollständigen exakten gebundenen Quellenwert. Danach wurde A auf den vollständigen Authoring-Vertrag umgestellt.

2. Run `36272249149`: FAILURE / REPAIR_REQUIRED  
   LanguageTool meldete 7 Findings, alle `GERMAN_SPELLER_RULE` zum Wort `Striegelzinken`.  
   Alle 7 wurden in einem Reparaturschritt behandelt.

3. Run `36272315893`: FAILURE / REPAIR_REQUIRED  
   PPM 6.7.9 meldete gleichzeitig 3 Findings:
   - `BLOCKED_CONTENT_TRACE_LEXICAL_SUPPORT`: Ist 0.5862068965517241, Soll >= 0.8
   - `BLOCKED_CONTENT_DUPLICATE_SENTENCE_RATIO`: Ist 0.03389830508474576, Soll <= 0.02
   - `BLOCKED_WAVE2_TABLE_VALUE`: unique_token_ratio 0.17307692307692307, Soll >= 0.18

4. Run `36272727354`: FAILURE / REPAIR_REQUIRED  
   Nach gemeinsamem Repair war `TRACE_LEXICAL_SUPPORT` beseitigt. Übrig:
   - `BLOCKED_CONTENT_DUPLICATE_SENTENCE_RATIO`: 0.03389830508474576
   - `BLOCKED_WAVE2_TABLE_VALUE`: unique_token_ratio 0.13725490196078433

5. Run `36272997322`: SUCCESS  
   Realer LT-6.8-/PPM-6.7.9-PASS nach gemeinsamer Reparatur.
   - Draft SHA-256: `eabc30dc3cec4686201ebef591525ee0858d59717c87996ebaf13b854c6b27c5`
   - Wortzahl: 1112
   - Prüfzeit im Job: 13.03 s

Damit ist belegt:
- A funktioniert technisch;
- B funktioniert technisch;
- ein frischer Beratungstext kann mit A+B real LT 6.8 + PPM 6.7.9 erreichen.

Nicht belegt:
- allgemeine Parität für alle Artikeltypen;
- FAQ-Test nach A+B;
- dass B immer in genau einer Reparatur zum PASS führt.

## Textmaschinen-/Überschriftenbefund

Vor Änderung der Textmaschine wurde ein eigener Rückfallpunkt erzeugt:
`konzept6/pre-textmachine-stable-20260926` @ `e5ae051caf3c383bb02b9640bd108693343db916`.

Danach wurde **noch keine Textmaschinen-/H2-Regel geändert**.

Frisch belegte Regelquellen:
- aktueller Metadaten-Snapshot enthält `keyword_staccato_forbidden=true`;
- aktueller Metadaten-Snapshot enthält `phrase_family_repetition_forbidden=true`.

Die vom Nutzer erinnerte konkrete Regel
**„Target Keyword in Zwischenüberschriften nur ein- oder zweimal; ansonsten Synonyme“**
konnte im gezielten Frischecheck **noch nicht autoritativ belegt** werden.

Daher gilt:
- die 1–2-Grenze darf nicht erfunden werden;
- vor jedem Textmaschinenfix muss zuerst die exakte autoritative Quelle / historische Regelsemantik gefunden werden;
- PPM 6.7.9 wird dafür nicht verändert.

## Exakter offener Punkt

`KONZEPT6_H2_KEYWORD_RULE_SOURCE_UNVERIFIED`

Belegt:
- Keyword-Stakkato verboten;
- Phrase-Familien-Wiederholung verboten.

Nicht belegt:
- numerische H2-Grenze 1 oder 2;
- genaue Synonympflicht/Synonymdefinition;
- ob die Grenze pro Artikel, pro H2-Gruppe oder pro Phrase-Familie gilt.

## Exakter nächster Schritt

Die autoritative bestehende H2-/Zwischenüberschriftenregel zur Keyword-Häufigkeit finden.

Nur wenn die konkrete 1–2-Regel belegt ist:
1. kleinsten Konzept-6-only Fix implementieren;
2. PPM/LT unverändert lassen;
3. Positivtest;
4. Negativtest mit zu häufiger Keyword-Wiederholung;
5. realen Beratungs- und FAQ-Test durchführen.

Wenn die Regel nicht belegt werden kann:
**BLOCKED – keine Schwelle erfinden.**

## Was nicht gemacht wurde

- Kein Textmaschinen-H2-Fix nach dem Rückfallpunkt.
- Kein FAQ-A+B-Realtest.
- Kein Publish.
- Kein Merge von Konzept 6 nach main.
- Keine Änderung an Konzept 5.
- Keine PPM-6.7.9- oder LT-6.8-Regeländerung.
- Kein Plugin entwickelt/geändert.
- Kein Hobbyraum als Current-Autorität benutzt.
- Kein Paul-Parallelweg benutzt.



## Closeout-/Current-Sync-Fehlerprotokoll

- PR #440 erster Head `af3b61e11acb59e151a5215513bdc2f0fbf344fc`:
  - Deterministic Entrance Gate: PASS.
  - Immutable Base Hardlock Run `36273885762`: FAIL.
  - Exakter Grund: Der Hardlock erlaubt einen Current-Sync nur als **exakt zwei Dateien**:
    `control/startmaster0107/CURRENT_STATE.json` und
    `control/startmaster0107/PFERDE_ATELIER_START_HERE.json`.
    Das im selben PR zusätzlich enthaltene Historienprotokoll machte den Pfad absichtlich unzulässig:
    `IMMUTABLE_SECURITY_PATH_CHANGE_BLOCKED`.
- Fix:
  - Historienprotokoll aus dem Current-Sync entfernt.
  - Current-Sync auf exakt die zwei autorisierten Dateien reduziert.
  - Neuer Head `98de5d6d80a6c3be2d55d6edcdedbc7e9da0d104`.
  - Deterministic Entrance Gate Run `36273941581`: PASS.
  - Immutable Base Hardlock Run `36273940237`: PASS.
  - PR #440 gemergt als `442d5f1cad2ce0bb25409e050925c64f48fb1008`.
- Der erste separate Protokoll-PR #441 war auf dem alten Main geprüft. Nach Merge von #440 verlangte GitHub die zwei Required Checks auf dem neuen Base; #441 wurde deshalb geschlossen und das identische Protokoll frisch von neuem Main als PR #442 aufgesetzt. Das ist kein Produkt-/Fachfehler.

## Current-/Campus-Synchronisierung

Die zuvor auf main vorhandene `CURRENT_STATE.json` beschrieb noch den alten Artikel-11-/Konzept-5-Produktionsstand. Der relevante Konzept-6-Delta wurde im Closeout auf einen separaten Current-Sync-Branch nachgezogen und die `PFERDE_ATELIER_START_HERE.json` hashgebunden an die aktualisierte Current-Datei rebunden.

Dieses Protokoll selbst bleibt Historie und darf nicht als Current verwendet werden.
