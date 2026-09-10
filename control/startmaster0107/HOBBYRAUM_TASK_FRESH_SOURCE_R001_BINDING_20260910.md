# TEMPORÄRER HOBBYRAUM-AUFTRAG – 107007 FRESH SOURCE → R_001

Nur isolierter Test-/Reparaturauftrag. Vor Abnahme löschen.

ZIEL
- Die jeweils frische, vom Nutzer bereitgestellte WordPress-Quelldatei pro Lauf als unveränderliche, hash-gebundene Quelle der fünf R_001-Rohkontexte anbinden.
- Bestehenden Runtime-Lifecycle/Slot beibehalten; keine neue Architektur.

HARTE NULL-ALTLASTEN-REGEL
- Kein alter 7/7-/Recovery-/SEO-Snapshot, kein altes Produktionspaket und kein synthetischer Fact-Pack darf Quelle der fünf Rohkontexte sein.
- Keine Übernahme alter Generator-/Stage-Proof-/Pre-Submit-Logik.
- Keine neuen Runner, Gates, Controller, Sidecars, Signer, Fallbacks oder Parallelwege.
- Keine Änderung an Textmaschine, Inhalts-/Qualitätsregeln, PPM, PSERC, PSTE, LanguageTool, SEO, Design, WordPress-Fachlogik, Publish/Endstempel.
- Worker/Codex erzeugt oder beglaubigt die fünf source-owner Rohkontexte nicht; er konsumiert sie nur aus der gebundenen frischen Quelle.

KISS-KANDIDAT
- Bestehende per-run Dateiidentität/Generation/SHA-Bindung weiterverwenden.
- Nur den fehlenden Übergang von der frischen gebundenen Quelle in den bestehenden Current-Action/R_001-Handoff ergänzen.
- Alte widersprüchliche 107007-Anweisung, wonach der Worker fact_pack/production_plan/workflow_release-Kontexte selbst erzeugt, nur soweit nötig auf source-owner consumption korrigieren.

PFLICHTTESTS VOR JEGLICHER FREIGABE
POSITIV:
- frische Quelle → bestehender Intake/Lifecycle → R_001 → Handoff → Aggregate-Consumer; publish=false.

NEGATIV fail-closed:
- Quelle fehlt
- falscher Source-Hash
- stale Generation
- Batch mismatch
- plan_slot mismatch
- canonical_article_id mismatch
- Quelle nach Bindung manipuliert
- abgeleiteter Rohkontext manipuliert
- irgendeine Altquelle (recovery_sources, historischer 7/7-Snapshot, alte SEO-Fixture, bestehendes leeres Generation-1-Produktionspaket) als Rohkontextquelle
- non-empty worker stage_proofs

GESAMT:
- bestehende M01–M36 auf exakt demselben Kandidaten-Head
- bestehende current_action/handoff selftests
- hardlock/hardlock-base
- KEIN echter 7/7-Produktionslauf vor lokalem Gesamt-PASS.

Wenn die echte frische WordPress-Datei / ihr aktuelles Format im Repo nicht verfügbar ist: NICHT durch alte Fixture ersetzen. Dann exakt BLOCKED melden und nur die fehlende Input-Spezifikation benennen.
