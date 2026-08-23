# PSTE 0.56.6 – Research FINALIZE bounded – STARTMASTER0065

Scope: ausschließlich der lokale Abschluss eines bereits vollständig bezahlten Einzellaufs nach 3/3 Provider-Schritten.

Root Cause: Der normale Research-FINALIZE fiel trotz vorhandenem record-local Sandbox-Store in den monolithischen Legacy-Sandbox-Lese-/Schreibpfad zurück. Bei großem Bestand konnte die AJAX-Hülle verloren gehen; Transport-Recovery und Koordinations-Readback ließen den persistenten Job anschließend RUNNING.

0.56.5 → 0.56.6: 8 Produktionsdateien geändert, 1 Changelog neu, 197 Dateien byteidentisch. Keine Datei entfernt.

Wichtiger Realtest: alter Job 2.1.0, RUNNING/FINALIZE, 3/3 Provider-Schritte, 0,048 USD, 549 Sandbox-Datensätze → COMPLETE in request-bounded Advances; 0 zusätzliche Provider-/DataForSEO-Aufrufe.

QA Source/Fresh:
- PSTE PHP 72/72 + 72/72 PASS; JSON 52/52 + 52/52 PASS
- PSTE Source↔Fresh 206/206 byteidentisch
- aktuelle 619er Projektion identisch: b1950e47c0200830cb71394370bf63f2b22f9f18a1ba5e2bec1f7fd5f170933f
- reale 562er Semantik + Exact Five PASS
- Safe Migration, 549 Record Store, Browser Progress, Breadth Cancel PASS
- Compiler Capability unverändert: 9d2636ecda87e2d93106deaff4f1358e4fa9cf906c1d55177e3119d94df65d8f
- PPM 6.7.9: 137/137 Source + 137/137 Fresh PASS
- Link Policy 1.0.1: 19/19 Source + 19/19 Fresh PASS
- PSERC 0.28.3 Source/Fresh: Normal 41/41, Terminal 58/58, Package Repository 9/9, One-Click Draft PASS; Snapshot-/Batch-Drift BLOCKED; Package Integrity PASS; Publish false

Installer SHA-256: 37df8fa6af1c26d82471f75b5935465346a1eb5ea01b21f2ad6fc1048cf41d67

Kein Merge auf main. Live-E2E bleibt bis Installation und Readback des realen 3/3-Jobs offen.