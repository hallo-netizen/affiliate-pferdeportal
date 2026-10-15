# HOBBYRAUSCH – RELEASE SOURCE PREFLIGHT

STAND: 2026-10-15
STATUS: AKTIVER HARD-GATE / KEIN RELEASE

Werkzeug:
`tools/hobby_release_source_preflight.py`

Zweck:
Vor einem finalen Plugin-Build erzwingt der Preflight:
- exakt 30 Kategorien im Manifest;
- jede Kategorie muss Status `ready_source` besitzen;
- jede zugehörige echte Einzelquelle muss vorhanden sein;
- Quelle muss mindestens 600×320 groß sein;
- erst dann darf der Image-stage-/Overlay-Build weiterlaufen.

## Aktueller Stand
Der aktuelle Manifest-Stand ist absichtlich **FAIL**:
- 30 Kategorien gesamt;
- 7 Kategorien `ready_source`;
- 23 Kategorien noch nicht `ready_source`;
- Release-Source-Gate daher **FAIL**.

Damit kann aus dem derzeitigen WIP kein versehentlich als vollständig deklarierter Plugin-Release entstehen.

## Weiterer Ablauf
Sobald eine echte neue Einzelquelle visuell PASS ist:
1. Kategorie im Manifest auf `ready_source` setzen;
2. echte Quelle an den deterministischen Stage-Slug binden;
3. Source-Preflight;
4. automatischer Hero-/Preview-Ableiter;
5. Image-only-Overlay auf 1.50.650;
6. kompletter Tree-/Mapping-/ZIP-Roundtrip-Test;
7. erst nach 30/30 zusätzlich globales Release-Gate und Live-Readback.
