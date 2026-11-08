# Pferdeatelier – Sicherheitsquellfund und PSERC-0.28.55-Gegenprobe (08.11.2026)

**Arbeitszweig:** `fix/pste-kisten-einmalige-pruefung-20261107`, PR #682 nur Draft. K0, gespeicherter PPM679-Redaktionsplan, Original-ZIPs und alle Sicherheitsdateien unverändert.

## 1. Sicherheitsdatei wirklich gefunden – Wiederherstellung NICHT blind ausgeführt

Aktueller Sicherheitslauf `42466410773` endet tatsächlich mit `python3: can't open file '.../control/paul-scope-gate/paul_scope_gate.py': [Errno 2] No such file or directory`. Der fehlende Pfad ist sowohl im unveränderten PR-Ausgangsbranch `fix/pste-mini-workflow-kiss-20261107` als auch im isolierten QA-Branch jeweils GitHub `404 Not Found`.

**Gefundene echte historische Quellen:** Die Datei `control/paul-scope-gate/paul_scope_gate.py` ist in den drei vorhandenen Sicherheitszweigen
- `security/paul-project-memory-hardlock-20260905`
- `security/fix-immutable-hardlock-yaml-20260907`
- `security/fix-hardlock-base-candidate-worktree-20260907`

vorhanden, jeweils **identischer Git-Blob `5eb7a77c4b5e95ca901862695a22118389024267`**, Umfang 669 Zeilen. Die zugehörige ursprüngliche Testdatei `control/paul-scope-gate/paul_scope_gate_ci_test.py` ist in denselben drei Zweigen vorhanden, jeweils gleicher Blob `3b0963481cae0ad02f611c14837208eddff1b165`.

**Wichtige Grenze:** Die historischen Sicherheitszweige sind gegenüber dem aktuellen PR-Ausgangsbranch **tausende Commits alt** (für `security/paul-project-memory-hardlock-20260905`: GitHub-Vergleich `behind_by=4293`, `ahead_by=41`). Daher ist es **nicht sicher**, deren Datei ungeprüft in den aktuellen Plugin-Branch zu kopieren. Die Datei enthält eigene Sicherheits-/Campus-Referenzen. **Kein Sicherheits-Gate umgangen, abgeschaltet oder verändert.**

**Zuständige autorisierte Security-/Baseline-Stelle:** Historische Originalblob-Identität plus zugehörige Testdatei und aktuellen Originalworkflow gemeinsam prüfen, nur innerhalb eines **separaten Security-Auftrags** die vertrauenswürdige aktuelle Quelle wiederherstellen und den vollständigen Original-Hardlock auf PASS bringen. Nicht den vorliegenden Plugin-PR dafür verwenden.

## 2. Vollständige PSERC-v0.28.55-PHP-Quelle nochmals direkt geprüft

**Tatsächlich gegen das lokale vollständig extrahierte ZIP** `PSERC-0.28.55-EIN-OWNER-STALE-PROOF-STOP-NUR-QA-NICHT-INSTALLIEREN.zip` (SHA256 `5fb82d0b35346d71d1cc0d9a796e5ca19d1ac3ad595ec5aab9643154db8a8578`) mit PHP **direkt** `PSERC_SEO_Reader::normalizeCandidate` aufgerufen. Die vorhandenen beiden Klassen `class-pserc-metadata-boundary.php` und `class-pserc-seo-reader.php` wurden geladen; nur WordPress/PSTE-Leseantworten durch Testdummies ersetzt. **Alle sechs** konkreten Prüfungen PASS:

1. Gültige externe FREI-Antwort ist ELIGIBLE.
2. Zurückgezogene/fehlende gespeicherte Antwort ist HELD, mit `SEO_EXTERNAL_SINGLE_OWNER_PROOF_MISSING_OR_STALE`.
3. Nachträglich veränderter Titel ist HELD.
4. Fehlender externer Beleg ist HELD.
5. Externes Markerfeld ohne echte Antwort ist HELD.
6. Altes, tatsächlich unbeteiligtes Thema bleibt ELIGIBLE nach bestehendem Altweg.

Dies ist eine **reale PHP-Klassenprobe** gegen echte PSERC-v0.28.55-Dateien, **kein** echter WordPress/MySQL-/PSERC-K0-Endlauf. Kein zweiter inhaltlicher SEO-Prüfer eingebaut.

## 3. Zulässiger nächster Schritt

Den echten Sicherheitshardlock in seinem zuständigen Sicherheits-/Basisauftrag korrekt wiederherstellen und dort mit dem Originalworkflow testen. Der echte Staging-Test des vorhandenen PSTE-/PSERC-Paares bleibt bis zu dessen Freigabe gesperrt. Der echte externe SEO-Owner kann **erst anhand des vollständigen unveränderten WordPress-Testexports** korrekt urteilen; eine künstliche 100er-Keyword-Simulation ist dafür kein Ersatz.

**Freigabe bleibt: NEIN – keine Installation, kein Merge, kein K0-Umbau.**
