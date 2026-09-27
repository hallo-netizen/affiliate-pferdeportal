# STARTMASTER0107 — KONZEPT 7 OPTIMIERUNG / REAL4 / ABSCHLUSS-NACHHOLPROTOKOLL — 2026-09-27

> Rolle: Historie/Nachweis. **Keine CURRENT- oder NEXT-ACTION-Autorität.**
> Aktueller Stand kommt ausschließlich aus `control/startmaster0107/CURRENT_STATE.json` auf `main`.

## Zielvertrag

Autoritative Zielquelle unverändert:

`control/startmaster0107/ZIELVERTRAG_REASONING_MEDIUM_MAX_STARTMASTER0107.json`

Ziel: `MAXIMIZE_MEDIUM_WITHOUT_ANY_GATE_OR_QUALITY_CHANGE`.

Unverändert:
- LanguageTool 6.8;
- PPM 6.7.9;
- PSERC;
- ENDSTEMPEL;
- Publish-Sicherheit `publish_allowed=false`.

## Ausgangslage / Sicherung

Konzept 6 wurde vor den K7-Experimenten als Goldstand gesichert:
- Gold-Commit: `2327a3c9f2bbdfbc9b0c6244a5b815d126aac203`;
- Freeze-Branch: `fallback/konzept6-frozen-20260927` = identisch zu Gold-Commit;
- Archivanker: `archive/konzept6-gold-20260927` = identisch zu Gold-Commit;
- dauerhafter K6-Release:
  `konzept6-endstempel-df59b8428c5e3f0750c5523091c00a1172975109823ee816d2234cf9052505d0-g000002`;
- Release-Asset:
  `GEN1_7_ARTIKEL_PSERC_APPROVED_PRODUCTION_PACKAGE_107008_FINAL.json`;
- Asset-ID: `592281735`;
- bekannte finale Datei-SHA-256:
  `b2c53e17e209cdafa8a631330ad397818bb5544b94cebc5849958d6dea87e351`.

K6 bleibt unangetasteter Rückfallstand.

K7-Baseline:
- Branch: `konzept7/baseline-isolated-20260927`;
- SHA: `bdaa69eb9c96e4586f57e9b7da5aa96c7f23c9b6`.

## Was tatsächlich gemacht wurde

K7 wurde aus dem gesicherten K6-Stand als isolierte Experimentierlinie aufgebaut. Keine K6-Artikeltexte, kein K6-ENDSTEMPEL-Payload und keine K6-Laufartefakte wurden als K7-Laufquelle übernommen.

Eingebaut wurden:
- idempotenter Start-/Execution-Lock: gleicher Batch => Resume; widersprüchlicher Start => Block;
- exakte Research-Reuse-Prüfung vor neuer Recherche;
- Planung paralleler Recherche-Spuren;
- paralleler Artikelcontroller mit 1/2/4/8 technisch prüfbaren Spuren;
- harte Artikeltrennung ohne Cross-Article-State-Sharing;
- Writer-Sicherheitsreserve oberhalb der Mindestgrenzen;
- vorgebundene mechanische Anforderungen;
- gebündelte Reparatur je Checker-Befundpaket;
- Repair-Historie mit Vorher-/Nachher-Bytes und Hashes;
- Messung der Laufzeiten pro Phase;
- vorbereiteter Closeout-Pfad PSERC -> ENDSTEMPEL -> finale WordPress-JSON;
- mechanischer Fact-Trace-Preflight ohne Änderung des sichtbaren Textes;
- K7-eigene Bound-Fact-Context-Erzeugung aus persistierter Research-Bindung für alle 16 Items;
- vorhandene PPM-Regeln für Title-Repeat / Fact-Trace / Tabellenwert in den Writer-Preflight vorgebunden, ohne PPM selbst zu ändern.

Arbeitsbranch zum Zeitpunkt dieses Frischechecks:
`konzept7/working-copy-20260927`
Head:
`726b48c5d9e91cc7cf804ff0966d9e2022c1e722`.

Seit K7-Baseline: 48 Commits, 0 Commits hinter Baseline.

## Tatsächlich ausgeführte Tests / Evidence

### Real4 — echter 4-Spur-Lauf

Run: `36305892513`
Workflow: `Konzept 7 Real4 Parallel Validation`
Head: `587c584e6b736e9f5169287b6a133195bfcda2d9`
Ergebnis: **SUCCESS**

Messwerte:
- 4 Artikel;
- 4 parallele Spuren;
- Wallclock: `22.486 s`;
- serielles Äquivalent: `83.933 s`;
- gemessener Parallel-Speedup: `3.733x`;
- Batch-Distinctness: PASS;
- max. Pairwise-Shingle-Jaccard: `0.00115` bei Grenzwert `0.2`;
- 4/4 LanguageTool 6.8 PASS;
- 4/4 PPM 6.7.9 PASS;
- `publish_allowed=false`.

Finale Real4-Draft-SHA-256:
- Artikel 0: `4f0e9871ef620f87713fc47399339b51d9638eb12a9b131c0fa91ca40ca027c9`;
- Artikel 1: `b0cf9cbbfa002a98245eeeea6178eaa60a470cbb81a851dd4851fcb9b762c650`;
- Artikel 2: `d36559f667a466d5399bfdda9140897ac91b6a8d1a343bda3eb92a650fa3fa69`;
- Artikel 3: `cdcc0ed80a8abeb62a32fb394d20399553e184e84e6d903fd56877430b47bf45`.

### Aktueller K7-Head — technische Acceptance

Run: `36307627144`
Head: `726b48c5d9e91cc7cf804ff0966d9e2022c1e722`
Ergebnis: **SUCCESS**

Belegt:
- 9/9 K7-Optimierungstests PASS;
- Real16 Bound-Fact-Context wird aus persistierter Research-Bindung ohne neue Recherche aufgebaut;
- Start-Lock / Duplicate-Resume / Conflict-Block;
- gebündelte Repair-Historie;
- Closeout-Preallocation;
- Messlogik;
- Research-Reuse;
- Parallelcontroller;
- Writer-Blueprint für Real16;
- bestehende Production-Guard-Suite 18/18 PASS;
- 16er-Binding initialisiert 1/2/4/8 Spuren korrekt.

Isolation Run: `36307627091`
Head: `726b48c5d9e91cc7cf804ff0966d9e2022c1e722`
Ergebnis: **SUCCESS**.

### Writer-Effect PASS-Reuse

Letzter echter `Konzept 7 Live Writer Check` PASS:
- Run: `36307336342`;
- Head: `605bbe82ccd145af4f268e1e1af4d54a5748e815`;
- Ergebnis: SUCCESS.

Frische-/Reuse-Prüfung gegen aktuellen Head `726b48c5...`:
Seit `605bbe82...` wurden ausschließlich
- `concept_agent/konzept7/k7_bound_fact_context.py` und
- `concept_agent/konzept7/test_k7_optimizations.py`
geändert.

Der vom Live-Writer-Check verwendete Writer-/Checkerpfad sowie dessen Probe-/Real4-Kontext blieben unverändert. Der bestehende Writer-PASS ist deshalb für diesen Teil hash-/delta-basiert wiederverwendbar; kein unnötiger identischer Wiederholungslauf nötig.

## Vollständiges Fehlerprotokoll dieses Arbeitsstrangs

1. **Falscher alter Host-Signer-Weg nach K6**
   - Symptom: Abschluss wurde zunächst über `PSERC_SIGNER_CMD` betrachtet.
   - Ursache: falscher historischer Pfad statt bereits bewiesenem K6-GitHub-ENDSTEMPEL.
   - Korrektur: zurück auf vorhandenen K6-Endstempel-Workflow mit `ENDSTEMPEL_PRIVATE_KEY`.
   - Ergebnis: K6-Endstempel / finale JSON erfolgreich; alter Host-Signer-Weg für K6/K7 nicht als Abschlussroute verwenden.

2. **Real4 Fact-Trace-Metadaten falsch erzeugt**
   - Symptom: massenhaft `SOURCE_TRACE_FIELDS_MUST_MATCH_REFERENCED_FACT`.
   - Ursache: manuell erzeugte Testdrafts trugen ausgeschriebenen Quellentitel; PPM erwartet gebundene `source_id`.
   - Korrektur: `k7_mechanical_preflight.py` bindet Fact-Trace-Felder mechanisch gegen den Fact-Pack.
   - Sichtbarer Text bleibt unverändert.
   - Ergebnis: Metadatenblocker entfernt.

3. **Real4-Testworkflow: Variable `mechanical` nicht gesetzt**
   - Symptom: Testlauf brach im Report-Wiring ab.
   - Ursache: Report-Feld ergänzt, Vorab-Schritt im ausgeführten Skript zunächst nicht verdrahtet.
   - Korrektur: Import und Aufruf des mechanischen Preflights im Real4-Workflow nachgezogen.
   - Ergebnis: Testpfad funktionsfähig.

4. **Echte PPM-Befunde: Fact-Trace lexikalisch zu schwach + Tabelle zu wenig eigenständig**
   - PPM unverändert.
   - Exakte vorhandene PPM-Regel ermittelt:
     - Fact-Trace-Einheit braucht mindestens 2 relevante gemeinsame Lexikaltokens;
     - mindestens 80 % der Fact-Trace-Einheiten müssen getragen sein;
     - Tabellen brauchen mindestens 18 % Tokens, die außerhalb der Tabelle nicht vorkommen.
   - Korrektur: gebündelter sichtbarer Repair auf den vier Testartikeln; kein Fact-Pack- oder PPM-Regelwechsel.
   - Ergebnis: fachliche PPM-Befunde beseitigt.

5. **LT-Befunde nach Repair durch künstliche Wortbildungen**
   - Beispiele: `Striegelzinken`, künstliche `...profil`-Formulierungen.
   - Korrektur: normale, LT-sichere Formulierungen bei Erhalt der gebundenen Faktbegriffe.
   - Ergebnis: 3/4 Artikel LT+PPM PASS.

6. **Letzter LT-Grammatikbefund Artikel 0**
   - Formulierung: `Tretschicht lockern vor Planierschild`.
   - Korrektur: `Die Tretschicht vor dem Einebnen lockern`.
   - Ergebnis: finaler Real4-Lauf 4/4 LT+PPM PASS.

7. **Workflow-Trigger erfasste Repair-Datei zunächst nicht**
   - Symptom: Repair-Codeänderung startete Real4-Prüfung nicht automatisch.
   - Korrektur: Real4-Workflow beobachtet nun Repair-/Preflight-Dateien.
   - Ergebnis: Folgeänderungen lösen Prüfung aus.

8. **Writer-Probe / FAQ- und Title-Repeat-Nacharbeiten im späteren K7-Delta**
   - mehrere Live-Writer-Läufe schlugen während der Entwicklung fehl;
   - anschließend bestehende Title-Repeat-Regel und FAQ-Antwortboden aus gebundenen Fakten in K7 vorgebunden;
   - letzter Writer-Check auf unverändertem Writer-/Checkerpfad PASS;
   - aktueller Head Acceptance + Isolation PASS.

Kein Fehler wurde durch Abschwächung von LT 6.8, PPM 6.7.9, PSERC oder ENDSTEMPEL behoben.

## Architektur-/Warum-Entscheidungen

- K6 ist Gold-/Rollback-Stand und wird nicht mehr verändert.
- K7 ist isolierte Experimentier-/Optimierungslinie.
- Standardziel K7: 4 Artikelspuren parallel; 1/2/4/8 bleiben Benchmark-Matrix.
- Innerhalb eines Artikels bleibt die Reihenfolge strikt:
  WRITE_DRAFT -> LT68 -> PPM679 -> ggf. Repair desselben Artikels -> zurück zu LT68 -> PASS.
- Parallelisierung nur zwischen Artikeln, niemals als Aufweichung der Einzelartikelreihenfolge.
- Exakte persistierte Recherche wird vor neuer Recherche wiederverwendet.
- Mechanische Metadaten sollen deterministisch gebunden werden; sichtbare Textqualität bleibt Writer-Aufgabe und wird durch unveränderte Gates geprüft.
- Abschlussroute wird zu Beginn vorgebunden; nach Artikel-PASS keine freie Suche nach einem Abschlussweg.
- Optimierung gilt nur bei Mess-/PASS-Nachweis als bewiesen.

## Was noch nicht bewiesen ist

Noch **nicht** real end-to-end bewiesen:
- kompletter 16er-K7-Lauf auf dem aktuellen K7-Stand;
- 4 parallele echte Schreibspuren für alle 16 Artikel;
- anschließender PSERC-Batch-PASS;
- K7-ENDSTEMPEL-PASS;
- finale K7-WordPress-JSON aus diesem vollständigen Lauf.

Das ist kein nachgewiesener Produktfehler, sondern der erste offene Validierungsschritt.

## Nicht anfassen

- K6 Freeze/Goldstand;
- K5 Freeze;
- LanguageTool 6.8 Regeln;
- PPM 6.7.9 Regeln;
- PSERC-Regeln;
- ENDSTEMPEL-Semantik;
- Publish-Sicherheit;
- alte Artikel als Schreib-/Repair-/Faktenquelle;
- persistierte Research-Bindung ohne belegten Invalidierungsgrund.

## Hobbyraum / Parallelworker / Plugins

- Hobbyraum: NICHT BETROFFEN.
- Separater Paul-Worker: NICHT BETROFFEN.
- K7 verwendet technisch parallele Artikelspuren; deren Ergebnis ist Evidence, nicht CURRENT.
- Plugins: NICHT BETROFFEN.

## Nächster Validierungsschritt

Die CURRENT-Autorität muss als einzige NEXT ACTION festlegen:

**K7 auf dem frisch geprüften Head mit dem aktuellen 16er-Binding als vollständigen 4-Spur-End-to-End-Lauf ausführen: Start/Lock -> Research-Reuse -> 16 Artikel -> LT 6.8 -> PPM 6.7.9 -> PSERC -> ENDSTEMPEL -> finale WordPress-JSON; `publish_allowed=false`.**

Dieses Protokoll ist nur Historie/Nachweis und darf diese NEXT ACTION nicht ersetzen.
