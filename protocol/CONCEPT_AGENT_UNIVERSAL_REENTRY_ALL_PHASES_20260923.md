# Concept Agent — Universal Reentry All Phases — 2026-09-23

Ziel: Nach jeder Unterbrechung darf ausschließlich der vollständig gebundene aktuelle Produktionszustand die Fortsetzung bestimmen.

Umgesetzt:
- universelle Entscheidung `CONCEPT_AGENT_UNIVERSAL_REENTRY_DECISION_V2`;
- jeder Wiedereinstieg validiert die Gesamtstrecke von INTAKE bis zum tatsächlich erreichten Stand und fast-forwardet nur nachgewiesene Stufen;
- der Chat darf weder Stufe noch Artikel wählen;
- jede produktive Aktion in `progress_guard.py` verlangt die exakt zum aktuellen Binding und Checkpoint passende Reentry-Entscheidung;
- exakte aktuelle Draft-Bytes werden mit SHA-256, Größe und Revision dauerhaft im Checkpoint gespeichert;
- Wiederherstellung eines laufenden Textes ist nur bytegenau aus diesem Checkpoint erlaubt;
- falsche/tampered Binding-, Checkpoint-, Decision-, Draft-, Reihenfolge- und Prüferzustände blockieren fail-closed;
- freie Chat-Ausführung, freie Repository-Suche, freie Binär-/Prüfersuche und Alternativrouten sind verboten;
- fehlt die kanonische Ausführungsumgebung: STOP;
- Artikelproduktion, PSERC, ENDSTEMPEL und finaler STOP liegen hinter derselben Reentry-Entscheidung;
- text-start, Qualitätskern, LT 6.8, PPM 6.7.9, PSERC, ENDSTEMPEL und Publish-Regeln bleiben unverändert.

Verbindliche Stufen:
INTAKE → RESEARCH → RESEARCH_BOUND → AUTHORING_BOUND → ARTICLE_PRODUCTION → PSERC_PACKAGE → ENDSTEMPEL → COMPLETE.

Regressionspflicht:
- Einstieg nach jeder bereits erreichten Gesamtstufe;
- keine Stufe überspringbar;
- falsche Cross-Stage-Bindung blockiert;
- aktive Artikelaktionen ohne exakte V2-Entscheidung blockieren;
- manipulierter Decision-Hash blockiert;
- aktuelle Draft-Bytes lassen sich bytegenau wiederherstellen;
- fehlende/manipulierte Draft-Bytes blockieren;
- PSERC → ENDSTEMPEL → STOP bleibt strikt gebunden;
- Policy bleibt: keine freie Chat-/Repo-/Binary-/Alternativroute.

PUBLISH: NO
