# PROTOKOLL / ÜBERGABE — SYSTEM 4 — FINAL CLOSEOUT 2026-09-13

Dieses Dokument ist das aktuelle Abschluss-/Übergabeprotokoll. Es ist **kein CURRENT_STATE**. Aktuelle System-4-Statuswahrheit bleibt ausschließlich `isolated_system4/README.md`; offizieller Campus-/Projekt-CURRENT bleibt ausschließlich `control/startmaster0107/CURRENT_STATE.json`.

## AKTUELLER REMOTE-STAND

PR #238 bleibt isolierter Draft-PR, unmerged und unpublished.

Branch: `hobbyroom/system4-true-single-room-v1`.

Der korrigierte Cause-Fix und der erweiterte Fehlerhistorien-Regressionsweg sind jetzt remote gebunden.

Gebundene Zielblobs:

- `authoring_contract.py` -> `bab5c3bbb6e1440b3d2e8a52e0ee4fe6f5fd7ae4`
- `full_local_acceptance.py` -> `738f83748b6ead75a9079b8c89eccf2ee9c43515`
- `LIVE_BOUND_INPUT_ONE_ARTICLE.json` -> `7c5fffa20a5ef29e9f793903f70259dcfac22a25`

Root-Manifest des gebundenen Live-Inputs:

`63d124c6c83ce6a68368123e55a7b7be61804f870c40f9606c315280c2aa2623`

## URSACHE / REPARATUR

Die wiederkehrende Fehlerklasse war eine unvollständige Autoritätsprüfung an Übergaben: Werte konnten vor Draft als gebunden gelten, obwohl sie nicht gegen dieselbe autoritative Quelle geprüft wurden, die der spätere echte PPM verwendet.

Der aktuelle Fix bindet die bekannten nicht reparierbaren Vorbedingungen vor Draft gegen ihre autoritativen Quellen. Dazu gehören insbesondere Runtime-Fact-IDs, Runtime-Linkwerte, Runtime-Pflichtfelder, Artikelidentität, Plan-/Fact-Pack-Snapshot, interner Marker, Fact-Referenzen und Source-Traces.

Keine Änderung an Textmaschine, PPM 6.7.9, PSERC/PSTE, LanguageTool-Regeln, Design, WordPress-Plugin oder Theme/CSS.

## TATSÄCHLICH AUSGEFÜHRTE TESTS

Auf den jetzt remote bytegleich gebundenen Produktions-/Testbytes wurden ohne Codex ausgeführt:

- vollständiger positiver Weg `Root -> Research -> Facts -> Context -> Draft -> echtes LT -> echtes PPM -> Repair -> Batch -> Handoff -> Unpack`: PASS;
- bestehender Root->Datei-Acceptance-Satz: 10/10 PASS;
- zusätzlicher Fehlerhistorien-Negativkatalog: 14/14 PASS;
- zusätzlicher Batch-/Kontext-Negativnachweis: PASS;
- Summe: 25/25 PASS.

Unter den aktiv provozierten historischen Fehlerklassen: unbekannte Fact-ID, Fact-Pack-Mismatch, interner Marker, Runtime-Felder/-Titel/-Links, Context/Snapshot, fehlende Fact-Refs, fehlende/falsche Source-Traces, Word-Floor, fehlender gebundener Link, Plan-Slot, Manifest, Handoff-Tamper und Batch-State-Tamper.

Echte Prüfer:

- LanguageTool 6.8 SHA256 `2122882e800d312a0543d895c56c0a84a9bb131c9b9846efd8fc033129353ae8`
- PPM 6.7.9 SHA256 `acbda93bd1c4292de7aaf88db2195631103991ff508b36c88cb694714818abd1`

`mocks_used=false` für den Produktionsbeweis.

## REMOTE-HARDLOCK

Auf Code-/Live-Input-Head `8bfe1fbb62be3df43651c20e816fed86b58ea1d7` war der `Pferde Atelier Immutable Base Hardlock` SUCCESS, Run `34774857418`.

Nach den reinen Dokumentationsnachzügen ist der Hardlock auf dem finalen Head erneut frisch zu prüfen. Erst dieser finale Head ist der Abschlussreferenzpunkt.

## CODEX

In dieser Reparatur-/Remote-Übertragung wurde **kein weiterer Codex-Lauf gestartet**.

Verbindlich bleibt:

**Kein Codex ohne ausdrückliche Nutzerfreigabe mit den Worten `Starte Codex`.**

`Weiter`, `testen`, `komplett prüfen`, `Null bis Ende` oder ähnliche Formulierungen sind keine Codex-Freigabe.

## STATUS / NEXT ACTION

System 4 bleibt **BLOCKED FÜR PRODUKTION**, weil der reale Ein-Artikel-Codex-Produktionslauf nach diesem Fix nicht freigegeben und nicht ausgeführt wurde.

Nächste Produktionsaktion nur nach ausdrücklicher Nutzerfreigabe `Starte Codex`:

- exakt ein real gebundener Artikel;
- kompletter System-4-Weg;
- kein automatischer zweiter Versuch;
- kein Merge;
- kein Publish.

## EINE WAHRHEIT

- offizieller Campus-/Projekt-CURRENT: `control/startmaster0107/CURRENT_STATE.json`
- System-4-CURRENT: `isolated_system4/README.md`
- System-4-Ziel: `isolated_system4/ZIELVERTRAG_SYSTEM4_CODEX_STRICT_PIPELINE_20260913.md`
- dieses Dokument: Abschluss-/Übergabeprotokoll, keine zweite CURRENT-Wahrheit
- PR-Text: nur Wegweiser

## PLUGINS

NICHT BETROFFEN.
