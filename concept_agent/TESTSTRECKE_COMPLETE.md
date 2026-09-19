# CONCEPT AGENT — KOMPLETTE TESTSTRECKE

## Phase 1 — Isolation
PASS-Kriterium:
- alle Änderungen nur unter concept_agent/**
- kein Import fremder Konzepte
- kein WordPress-Write
- kein Publish

## Phase 2 — Eingang
Reale WordPress-Auftragskopie.
Pflicht: Titel, Keyword, Artikeltyp, Kategorie, exakt drei gebundene interne Links.
Fehlende Links: BLOCK vor Research.

## Phase 3 — Research Agent
Nur gebundener Quellenpool.
Ungültige URL / leere Quelle / doppelte source_id: BLOCK.

## Phase 4 — Facts Agent
Jeder Fakt muss auf akzeptierte source_id zeigen.
Unbekannte source_id: BLOCK.

## Phase 5 — Writer
Austauschbarer Writer-Port.
Aktuell:
- interner Testwriter
- manueller Chat-Writer
- Claude-Port vorbereitet, nicht verbunden

## Phase 6 — Artikelprüfung
- Identität
- Keyword
- drei interne Links
- kein externer Link
- Tabelle
- Mindeststruktur

## Phase 7 — Repair
Nur derselbe Artikel.
Danach vollständige Wiederprüfung.

## Phase 8 — Finale Datei
Genau eine CONCEPT_AGENT_FINAL_ARTICLE_V1 je Artikel.
SHA256-Bindung.

## Phase 9 — 1..N
Getestete Größen:
- 1 Artikel
- 3 Artikel
- 7 Artikel
Kein Drop, keine Umordnung.
Fehler eines Artikels stoppt fail-closed.

## Phase 10 — reale Prüfer
PPM 6.7.9 liegt als eigene Byte-Kopie unter concept_agent/runtime/.
LanguageTool 6.8 wird über eigenen hashgebundenen Download beschafft.
runtime_preflight.py akzeptiert nur exakt diese Hashes.

Wichtig:
Der aktuelle Chat-Lauf konnte echte LT-/PPM-Ausführung nicht lokal starten, weil die verfügbare Ausführungsumgebung keine externe Binärdatei laden kann und kein LT-6.8-JAR vorinstalliert ist.
Das ist ein Laufzeitumgebungs-Blocker, kein Agentenketten-PASS.
Daher gilt noch KEINE Produktionsparität.

## Phase 11 — Produktionsgrenze
Kein Merge.
Kein WordPress-Write.
Kein Publish.
Andere Konzepte unverändert.
