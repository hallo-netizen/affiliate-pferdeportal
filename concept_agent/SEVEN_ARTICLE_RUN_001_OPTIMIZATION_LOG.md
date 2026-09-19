# Concept Agent – 7-Artikel-Lauf 001 – Fehler- und Optimierungsprotokoll

## Endergebnis
Der komplette 7-Artikel-Lauf wurde von ChatGPT als Writer ausgeführt.

Final:
- 7/7 LanguageTool 6.8: PASS, jeweils 0 Findings
- 7/7 PPM 6.7.9: TECHNICAL_CHECK_OK
- 7/7 PPM 6.7.9: CONTENT_QUALITY_CHECK_OK
- 7/7 Fail-Closed-Aggregat: PASS
- 0 exakte artikelübergreifende Satzdubletten, verpflichtende KI-Offenlegung ausgenommen

## Gefundene Fehler und Optimierung

### 1 – Hindernisstangen
Erster Versuch:
- BLOCKED_CONTENT_WORD_FLOOR
- BLOCKED_CONTENT_SOURCE_TRACE_COUNT
- BLOCKED_CONTENT_TRACE_LEXICAL_SUPPORT

Ursache:
Faktenspuren zunächst über Listenposition statt echten Plan-Slot zugeordnet; Text außerdem zu kurz.

Dauerhafte Lehre:
- Identität ausschließlich über Plan-Slot/Artikel-ID binden.
- Abschnittslängen vor LT/PPM vorprüfen.

### 2 – Reitplatzbeleuchtung
LanguageTool beanstandete unter anderem „blendarm“, „Wattzahl“ und „mastlose“.

Dauerhafte Lehre:
- ungewöhnliche Komposita und umgangssprachliche technische Begriffe vor LT vermeiden.

### 3 – Mistcontainer
LanguageTool beanstandete technische Komposita wie „Befüllhöhe“, „Befülltechnik“ und „Leerungsreserve“.

Dauerhafte Lehre:
- bei technisch korrekten, aber sprachprüferanfälligen Komposita verständliche Mehrwortformulierungen bevorzugen.

### 4 – Pferdehaftpflicht
Erster Versuch:
- BLOCKED_CONTENT_WORD_FLOOR
- BLOCKED_WAVE2_HEADING_INTENT_MISMATCH

Dauerhafte Lehre:
- H2 vorab gegen gebundene Suchintention prüfen.
- Mindestlänge nicht erst nach dem Schreiben prüfen.

### 5 – Huffett
Erster Versuch:
- LanguageTool: Subjekt-Verb-Kongruenz
- danach BLOCKED_CONTENT_DUPLICATE_SENTENCE_RATIO

Dauerhafte Lehre:
- nach jeder Sprachreparatur vollständigen PPM-Recheck.
- Quellensätze nicht doppelt als Stütze und Fließtext verwenden.

### 6 – Fliegenmasken
Erster Versuch:
- BLOCKED_CONTENT_DUPLICATE_SENTENCE_RATIO
- BLOCKED_WAVE2_HEADING_INTENT_MISMATCH
- nach erster Reparatur noch eine Satzdoppelung vorhanden

Dauerhafte Lehre:
- Satzdubletten nach jeder Reparatur neu rechnen.
- H2 aus gebundenem Intent ableiten, nicht frei formulieren.

### 7 – Pellets
Erster Versuch:
- LanguageTool beanstandete „Pelletform“, „raufutterbasierte“, „Pelletfütterung“, „Pelletmenge“
- danach BLOCKED_CONTENT_DUPLICATE_SENTENCE_RATIO

Dauerhafte Lehre:
- problematische Komposita früh erkennen.
- nach LT-Reparatur PPM immer komplett neu ausführen.

## Batch-weite Qualitätsoptimierung
Nach dem ersten Einzel-PASS wurden identische Schablonensätze zwischen Artikeln gefunden. Diese wurden artikelbezogen neu formuliert. Danach wurden alle sieben Artikel erneut vollständig durch LT 6.8 und PPM 6.7.9 geprüft.

Final:
- 7/7 PASS
- 0 exakte artikelübergreifende Satzdubletten, KI-Offenlegung ausgenommen

## Produktionsoptimierungen
1. Plan-Slot statt Listenposition als einzige Identitätsbindung.
2. Abschnittslängen vor LT/PPM prüfen.
3. H2-Intent vor Writer-Abgabe prüfen.
4. problematische Komposita vor LT filtern.
5. Satzdubletten innerhalb jedes Artikels vor PPM prüfen.
6. Satzdubletten über den gesamten Batch prüfen.
7. jede Reparatur mit vollständigem LT- und PPM-Recheck desselben Artikels.
8. Batch-Handoff erst nach 7/7 PASS erzeugen.
