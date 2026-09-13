# SYSTEM 4A — SYSTEM-4 PASS-AUTHENTIZITÄTSBEFUND

STATUS: NACH AKTUELLEM CODE GEPRÜFT / SYSTEM 4 UNVERÄNDERT
DATE: 2026-09-13

## Befund

Im aktuellen System 4 liegt `state.json` im Codex-Arbeitsbereich. `batch_gate.py` prüft bei FULL-PASS-Evidence Form und erwartete Werte, führt LanguageTool/PPM an dieser Grenze aber nicht erneut aus und besitzt keine ausschließlich vom echten Prüfer erzeugte Attestation.

Der finale `handoff_transport.py` prüft Fact-Trace, Design und Batchregeln erneut real. LT-/PPM-Daten werden dagegen auf PASS-Werte, Versionen und Content-Hash geprüft, nicht erneut ausgeführt.

## Direkter Beleg im vorhandenen System-4-Test

`isolated_system4/test_batch_gate.py` baut in `production_evidence(draft)` synthetisch:
- `SYSTEM4_FULL_PRODUCTION_CHECK_V1 / PASS`;
- LanguageTool 6.8 / PASS / `finding_count=0`;
- PPM 6.7.9 / PASS;
- `TECHNICAL_CHECK_OK`;
- `CONTENT_QUALITY_CHECK_OK`;
- `fail_closed_aggregate_status=PASS`;
- passenden Content-Hash.

`make_fixture()` schreibt diese Werte direkt in `state['checks']['production_evidence']`. Der positive Test ruft danach `batch_gate.collect_batch(...)` auf und erwartet `SYSTEM4_BATCH_FULL_PASS_COLLECTED`.

Damit kann das Batch-Gate einen formal passenden State mit synthetischer LT-/PPM-PASS-Evidence nicht von einem State unterscheiden, dessen Evidence tatsächlich aus `production_checks.run_all()` stammt.

Das beweist keinen praktischen externen Angriff. Es beweist aber eine Herkunftslücke, sobald der ausführende Worker den kanonischen State selbst schreiben kann.

## Bedeutung für 4A

Keine neue Prüflogik bauen. Die vorhandenen echten Prüfer bleiben unverändert.

4A muss nur verhindern, dass der Worker den kanonischen PASS-State erzeugen kann: Der äußere Supervisor nimmt das echte Prüfergebnis direkt in seinen internen State auf. Worker/Codex erhält keine State-/PASS-Schreibautorität.

Kein Produktions-PASS aus diesem Befund ableiten.
