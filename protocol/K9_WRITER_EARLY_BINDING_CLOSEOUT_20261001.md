# K9 WRITER EARLY-BINDING CLOSEOUT – 2026-10-01

ROLLE: Protokoll/Nachweis, **keine CURRENT-Autorität**.
Aktueller Produktionsstatus ausschließlich aus `CURRENT_STATE.json`.

## Anlass

Der reale 2-Artikel-Batch
`082d5b49f73f9e57c850a1d969ee2b65b0b1634afdff09ddebb84f69e9c174a9`
lief vollständig bis STOP.

Dabei zeigte sich:
- Artikel 1 musste nach dem ersten Writer-Entwurf wegen PPM-Faktbindungen, Wiederholungen und H2-Intent repariert werden;
- Artikel 2 musste wegen 13 LanguageTool-6.8-Findings repariert werden;
- die Regeln existierten bereits, wurden aber teilweise erst nach Writer-Annahme hart geprüft.

## Dauerhafte KISS-Änderung

Keine Qualitätsregel wurde geändert oder gelockert.

Stattdessen greifen dieselben Regeln früher:

1. Writer-/Repair-Job enthält explizit:
   - PPM-6.7.9-Preflight erforderlich;
   - LT-6.8-Preflight erforderlich;
   - Faktbindung aller sichtbaren Fakteneinheiten;
   - Duplicate-Sentence-Grenze;
   - gebundene H2-Intent-Regeln;
   - Tabellen-Nachabsatz;
   - quality_change_allowed=false.
2. `k9_write_packager.py` führt vor Annahme des Writerprodukts:
   - bestehende K9-Writing-Rules;
   - exakten PPM-6.7.9-Autoren-Preflight;
   - exaktes LanguageTool 6.8
   aus.
3. Ein Writerprodukt mit PPM-/LT-Fehlern wird **vor** Übergabe an die Checkstation blockiert.
4. Das erfolgreiche LT-Ergebnis wird hashgebunden im Artikelprodukt mitgeführt.
5. Die spätere Checkstation darf dieses versiegelte LT-Ergebnis wiederverwenden, prüft aber Engine, Jar-Hash, Artikel-Hash, geprüften Text-Hash und 0 Findings.
6. Manipulierte oder nicht passende LT-Evidence wird fail-closed blockiert.

PSERC bleibt Final-Integrity-only und führt LT/PPM nicht erneut als eigene Fachprüfung aus.

## Reale/problemnahe Positiv-/Negativbelege

- alter Pferdehaftpflicht-Erstentwurf mit realen PPM-Fehlern → vor Writer-Annahme BLOCK;
- reparierter Pferdehaftpflicht-Text → PPM-Preflight PASS;
- alter Kappzaum-Erstentwurf mit 13 realen LT-Findings → vor Writer-Annahme BLOCK;
- reparierter Kappzaum-Text → LT PASS;
- manipulierte LT-Evidence → BLOCK;
- exakte LT-Evidence-Reuse → PASS.

Workflow-/Regression:
- Run `36874190237` – greenfield selftest – SUCCESS;
- Run `36874234247` – native LT68 selftest inklusive Writer Positiv/Negativ – SUCCESS;
- Run `36874532830` – combined check selftest – SUCCESS;
- Run `36874572438` – LT-Reuse + Tamper-Block – SUCCESS;
- Run `36874572430` – greenfield regression – SUCCESS.

## Vorheriger 2-Artikel-Batch – Terminalbeleg

- Finalizer Run `36872540706` – SUCCESS;
- Artikelanzahl: 2;
- LT 6.8 final: PASS / 0 Findings;
- PPM 6.7.9 final: PASS;
- Writing Rules final: PASS;
- PSERC Final Integrity: PASS;
- ENDSTEMPEL: PASS;
- WordPress-Datei: PASS;
- publish_allowed=false.

## Dauerhafte Bewertung

Die Qualitätsgates waren nicht zu schwach.
Der Fehler war die zu späte harte Anwendung beim Erstentwurf.

Nach diesem Closeout gilt:
**Writer darf keinen Entwurf an die nächste Station übergeben, der die bereits gebundenen PPM-/LT-/Writing-Regeln nicht erfüllt.**

Der nächste reale Batch ist der Nachhaltigkeitstest.
