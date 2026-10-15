# HOBBYRAUSCH – IMAGE STAGE BUILDER – NEGATIVTESTS

STAND: 2026-10-15
STATUS: PASS / ARBEITSHILFE / KEIN PLUGIN / KEIN RELEASE

Werkzeug:
`tools/hobby_image_stage_builder.py`

## Negativtest 1 – Quelle fehlt
Eingabe:
- Queue enthält eine Quelldatei, die im Source-Ordner nicht existiert.

Ergebnis:
- Prozess endet mit Fehlerstatus;
- `pass_technical=false`;
- Exit-Code **2**;
- kein fälschlicher PASS.

## Negativtest 2 – Quelle zu klein
Eingabe:
- Quelle nur 300×160 px.

Ergebnis:
- Prozess stoppt;
- Fehler: `upscale forbidden: source 300x160 smaller than 600x320`;
- `pass_technical=false`;
- Exit-Code **2**.

Damit wird sichtbare Hochskalierung technisch verhindert.

## Negativtest 3 – exakte Dublette
Eingabe:
- dieselbe reale Quelle unter zwei verschiedenen Dateinamen/Kategorien.

Ergebnis:
- Hero-Dublette erkannt;
- Preview-Dublette erkannt;
- dHash-Abstand jeweils **0**;
- `pass_technical=false`;
- Exit-Code **2**.

## Gesamtergebnis
**3/3 Negativpfade PASS.**

Das Werkzeug akzeptiert damit weder:
- fehlende Quellen;
- zu kleine Quellen;
- exakte Mehrfachbelegung derselben Bildquelle.

Die visuelle semantische Prüfung bleibt zusätzlich verpflichtend.
