# SYSTEM 4 — TRUE SINGLE ROOM

Status: **BLOCKED FÜR PRODUKTION — REMOTE CAUSE-FIX UND FEHLERHISTORIEN-REGRESSION SIND GEBUNDEN; EIN REALER CODEX-ARTIKELLAUF IST NICHT FREIGEGEBEN UND WURDE NICHT ERNEUT GESTARTET.**

Diese Datei ist die **eine aktuelle System-4-Statuswahrheit**. Der offizielle Campus-/Projektstand bleibt getrennt und ausschließlich in `control/startmaster0107/CURRENT_STATE.json`.

## Aktueller Remote-Stand

PR #238: `System 4 — true single-room article production`

Branch: `hobbyroom/system4-true-single-room-v1`

Kein Merge. Kein Publish. `publish_allowed=false`.

Der korrigierte System-4-Ursachenstand ist jetzt auf dem Remote-Branch gebunden.

Gebundene Kernblobs:

- `isolated_system4/authoring_contract.py` -> `bab5c3bbb6e1440b3d2e8a52e0ee4fe6f5fd7ae4`
- `isolated_system4/full_local_acceptance.py` -> `738f83748b6ead75a9079b8c89eccf2ee9c43515`
- `isolated_system4/LIVE_BOUND_INPUT_ONE_ARTICLE.json` -> `7c5fffa20a5ef29e9f793903f70259dcfac22a25`

Gebundener Root-Manifestwert im Live-Input:

`63d124c6c83ce6a68368123e55a7b7be61804f870c40f9606c315280c2aa2623`

Der Live-Input bleibt exakt ein Artikel:

- Typ `Beratung`
- Kategorie `putzbox-beratung`
- Titel `Putzbox für Pferde richtig auswählen`
- Keyword `Putzbox für Pferde`
- Plan-Slot `88043c35da332d4b2a500d1b61919721aefadf894bc923c841cc849a132c63b5`
- `publish_allowed=false`

## Ursache und Fix

Wiederholt aufgetretene Fehlerklasse:

**Eine Übergabe wurde als gültig akzeptiert, obwohl ihr Wert nicht gegen dieselbe autoritative Quelle validiert war, die der spätere echte Prüfer verwendet.**

Der aktuelle Fix bindet deshalb vor Draft insbesondere:

- Runtime-Fact-IDs gegen das tatsächlich gebundene kanonische Fact-Pack;
- Runtime-Linkwerte gegen die gebundene Linkquelle;
- erforderliche Runtime-Felder und Artikelidentität;
- Plan-/Fact-Pack-Snapshot-Bindung;
- internen PPM-Marker;
- Fact-Referenzen und Source-Traces gegen die gebundene Fact-Autorität;
- bereits vor Draft bekannte PPM-Strukturpflichten, ohne PPM-Fachregeln zu verändern.

Textmaschine, PPM 6.7.9, PSERC/PSTE, LanguageTool 6.8, Design, WordPress-Plugin und Theme/CSS bleiben READ-ONLY.

## Fehlerhistorie / Regression

Die bekannte Fehlerhistorie wurde als Negativkatalog gegen den Gesamtweg geprüft. Tatsächlich provoziert und fail-closed geprüft wurden unter anderem:

- unbekannte Fact-ID;
- Fact-ID nicht im kanonischen Fact-Pack;
- fehlender interner Marker;
- Runtime-Titel-/Pflichtfeld-Mismatch;
- Runtime-Link-Mismatch;
- Plan-/Fact-Pack-Snapshot-Mismatch;
- fehlende Fact-Referenzen;
- fehlende Source-Traces;
- falsche Source-Trace-Bindung;
- Word-Floor;
- fehlender gebundener Link;
- fehlender Plan-Slot;
- Manifest missing/mismatch;
- Handoff-Tamper;
- Batch-State-Tamper.

Beweis auf den jetzt remote bytegleich gebundenen Produktions-/Testbytes:

- kompletter positiver Root->Research->Facts->Context->Draft->echtes LT->echtes PPM->Repair->Batch->Handoff->Unpack-Weg: **PASS**;
- bestehender Root->Datei-Acceptance-Satz: **10/10 PASS**;
- zusätzlicher Fehlerhistorien-Katalog: **14/14 PASS**;
- zusätzlicher Batch-/Kontext-Negativnachweis: **PASS**;
- Summe dieser ausgeführten Nachweise: **25/25 PASS**;
- echtes LanguageTool 6.8;
- echtes PPM 6.7.9;
- `mocks_used=false` für den Produktionsbeweis.

PPM-6.7.9-SHA256:
`acbda93bd1c4292de7aaf88db2195631103991ff508b36c88cb694714818abd1`

LanguageTool-6.8-SHA256:
`2122882e800d312a0543d895c56c0a84a9bb131c9b9846efd8fc033129353ae8`

## Remote-Hardlock

Auf dem Code-/Live-Input-Head `8bfe1fbb62be3df43651c20e816fed86b58ea1d7` lief der Workflow `Pferde Atelier Immutable Base Hardlock` als **SUCCESS**, Run `34774857418`.

Dokumentationsänderungen nach diesem Head verändern keine System-4-Kritikaldatei des Root-Manifests. Trotzdem muss der Hardlock auch auf dem finalen Dokumentations-Head erneut SUCCESS sein, bevor dieser Stand als sauber abgeschlossen gilt.

## Codex-Regel

**Kein Codex ohne die ausdrückliche Nutzerfreigabe mit den Worten `Starte Codex`.**

`Weiter`, `testen`, `komplett prüfen`, `Null bis Ende` oder ähnliche Formulierungen sind **keine** Codex-Freigabe.

Codex wird ausschließlich für einen konkret gebundenen realen Artikel-/Batch-Produktionslauf verwendet, nicht für Diagnose, Architektur, Patch, Commit, Preflight, Regressionstests oder Dokumentation.

## HOBBYRAUM / NEXT ACTION

Status: **BLOCKED FÜR PRODUKTION**.

Technischer Remote-Cause-Fix und Regressionen sind gebunden. Nächste Produktionsaktion ist ausschließlich nach ausdrücklicher Nutzerfreigabe `Starte Codex`:

- genau ein real gebundener Artikeltest über den vollständigen System-4-Weg;
- kein zweiter automatischer Versuch;
- kein Merge;
- kein Publish.

Bis zu dieser ausdrücklichen Freigabe: **kein Codex-Aufruf.**
