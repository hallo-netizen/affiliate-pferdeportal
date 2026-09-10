# TEMPORÄRER PR223-HOBBYRAUM — NUR REPARATUR UND LOKALE TESTS

Diese Datei gilt NUR auf dem PR223-Hobbyraum-Branch `hobbyroom/107007-simple-entry-aggregate-checker-v2` und NUR für den ausdrücklich beauftragten KISS-Ursachenfix.

Für diesen Branch ist `python3 control/cloud-entry-gate/cloud_entry.py start` ausdrücklich NICHT der Arbeitsstart und darf für Reparatur-/Kandidatentests NICHT ausgeführt werden. Ebenso darf `control/output-quarantine/runtime_entry_gate.py` NICHT als Voraussetzung für die Reparatur-/Kandidatentests ausgeführt werden.

Zulässig ist ausschließlich:
- betroffene bestehende Dateien für den PR223-Ursachenfix lesen/ändern;
- bestehende lokale POS/NEG-Tests, Selftests und `HOBBYRAUM_M01_M33_REGRESSION.py` ausführen;
- keine Produktion, kein 107007-Live-Lauf, kein Publish, kein Merge;
- keine neue Architektur, Runner, Gates, Controller, Contracts, Sidecars, Fallbacks oder Signer;
- keinerlei Fach-, Inhalts-, Qualitäts-, Textmaschinen-, PPM-, PSERC-, PSTE-, LanguageTool-, SEO-, Design-, WordPress- oder Publish-Regel ändern.

Vor finaler Kandidatenabnahme MUSS diese temporäre Datei vollständig durch die exakte `AGENTS.md` aus `main` ersetzt werden. Die temporäre Ausnahme darf niemals gemergt werden.
