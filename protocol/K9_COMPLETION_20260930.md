# K9 Abschlussprotokoll – Schermaschinen-E2E – 2026-09-30

**Rolle:** Historie und Nachweis. Keine CURRENT-Wahrheit und keine NEXT-ACTION-Quelle.  
**Aktuelle Wahrheit:** ausschließlich `CURRENT_STATE.json`.

## Ziel und Ergebnis

Der reale Einartikel-Beweis für **„So wählst du passende Schermaschinen für Pferde“** wurde vollständig bis STOP geführt:

`RESEARCH → WRITE → CHECK (LT 6.8 + PPM 6.7.9) → REPAIR/CHECK-Schleifen → PSERC → ENDSTEMPEL → WordPress-Endformatprüfung → STOP`.

Finale Evidence:
- Finalizer-Run: `36730449323` – SUCCESS.
- STOP-Commit: `82269ab1d9d9ffa552a5ec422111b1feb6644dd3`.
- Finalpaket: `final/GEN1_7_ARTIKEL_PSERC_APPROVED_PRODUCTION_PACKAGE_107008_FINAL.json`.
- Final SHA-256: `5e39f9e9790a9444daf8b7dc185b9199ed9245ff5257e6295e20612b2bf4ff94`.
- Batch SHA-256: `ccba8b677e9a66f50d7415352d91af8df17cc6c10c0273c14728dbb090554b1e`.
- `publish_allowed=false`.

## Ausgeführte dauerhafte Reparaturen und Warum

1. **Writer-Handoff auf den bewährten Draft-Packager-Weg zurückgeführt.**  
   Worker schreiben `K9_WRITER_DRAFT_V1` nach `writer_drafts/`; `k9_write_packager.py` baut das vollständige Artikelprodukt. Grund: direkte Worker-Submissions erzeugten einen falschen Vertrag und umgingen die etablierte Paketierung.

2. **Research-Gate verschärft.**  
   Portal-Links, Decision-Support, Evidence-Hashes, artikeltypspezifische `article_types` je Claim und deterministischer `title_scope` werden vor WRITE gebunden/geprüft. Grund: fehlende Research-Bindungen dürfen nicht erst in WRITE, PPM oder PSERC sichtbar werden.

3. **PPM-Struktur vorgezogen.**  
   Kanonische Tabellenklassen und PPM-Source-Traces werden vor CHECK verbindlich gemacht. Grund: PPM-kompatible Struktur darf nicht erst in späteren Gates rekonstruiert werden.

4. **Alle verwendeten Fakten erhalten vollständige Source-Traces.**  
   Der Packager ergänzt fehlende technische Traces deterministisch an bereits faktgebundene Absätze und prüft die vollständige Fakt-ID-Menge. Grund: PSERC verlangt Claim-Traces für sämtliche verwendeten Fakten; eine frühere Mindestzahl von drei war zu schwach.

5. **Scope-Bindung Research → Artikel → PSERC vereinheitlicht.**  
   `fact_pack.title_scope` und `runtime_order.subject_scope` stammen aus derselben deterministischen Bindung. Grund: `CANONICAL_FACT_PACK_SCOPE_MISMATCH` darf nicht im Finalizer auftreten.

6. **Terminale Current-Synchronisierung nachgezogen.**  
   Der Finalizer schreibt künftig zusammen mit `K9_STOP.json` auch die alleinige `CURRENT_STATE.json` auf STOP. Grund: nach dem erfolgreichen E2E-Lauf blieb Current zuvor fälschlich auf einem bereits erledigten Repair-Job stehen.

## Fehlerhistorie dieses Beweislaufs

- direkter WRITE-Output statt Writer-Draft → behoben;
- Research ohne notwendige Portal-/Decision-Bindung → behoben;
- Claims ohne `article_types:["Beratung"]` → behoben;
- fehlende/inkonsistente Evidence-Hashes → behoben;
- nicht kanonische Tabelle / unvollständige Source-Traces → behoben;
- `CANONICAL_FACT_PACK_SCOPE_MISMATCH` → behoben;
- `CANONICAL_ARTICLE_CLAIM_TRACE_MISSING` für FACT-CLIPPER-001/002 → behoben;
- terminale Current-Autorität blieb stale → mit Finalizer-Sync behoben.

Keine dieser historischen Meldungen ist eine aktuelle Fehlerquelle. Aktuelle Blocker stehen ausschließlich in `CURRENT_STATE.json`.

## Tests / Evidence

- Unit-/Engine-Regressions wurden während des Laufs wiederholt ausgeführt.
- Artikeltyp-Bindung: Negativfall ohne/falsche Claim-Typbindung blockiert; Positivfall mit `Beratung` akzeptiert.
- Tabellen-/Trace-Struktur: gegen PPM 6.7.9 positiv geprüft.
- Scope: Negativ-/Positivregression im Selftest; Negativprüfung wurde beim Abschluss so korrigiert, dass auch das PSERC-Ergebnisfile ausgewertet wird.
- Realer Endlauf `36730449323`: PSERC PASS, ENDSTEMPEL PASS, WordPress-Endformat PASS, durable Release PASS.
- Terminale Evidence: `runtime/K9_STOP.json`, `runtime/K9_PSERC_RESULT.json`, `runtime/K9_ENDSTEMPEL_VERIFY.json`, `runtime/K9_WORDPRESS_IMPORT_VERIFY.json`.

## Nicht verändert

- LT 6.8;
- PPM 6.7.9;
- PSERC;
- ENDSTEMPEL;
- Qualitätsniveau;
- `publish_allowed=false`;
- bestehende K9-Stationslogik als Produktionskern.

Die nächste Arbeit darf den erfolgreichen Einzelartikel nicht wieder öffnen. Sie baut auf diesem E2E-Beweis auf.
