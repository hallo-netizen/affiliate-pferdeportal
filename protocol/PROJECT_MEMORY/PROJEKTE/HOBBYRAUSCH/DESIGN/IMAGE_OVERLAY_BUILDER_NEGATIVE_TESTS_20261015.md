# HOBBYRAUSCH – IMAGE-ONLY OVERLAY BUILDER – NEGATIVTESTS

STAND: 2026-10-15
STATUS: PASS / KEIN RELEASE

Werkzeug:
`tools/hobby_image_overlay_builder.py`

## Negativtest 1 – unvollständiger Stage
Eingabe:
- Manifest erwartet 7 Kategorien;
- Stage enthält nur 1 Kategorie;
- kein `--allow-partial`.

Ergebnis:
- sauberer STOP;
- Meldung: `incomplete stage: missing 6 categories`;
- Exit-Code **2**;
- kein Kandidat freigegeben.

## Negativtest 2 – falsches Hero-Maß
Eingabe:
- Hero 599×320 statt 600×320.

Ergebnis:
- sauberer STOP;
- Meldung: erwartete 600×320, erhalten 599×320;
- Exit-Code **2**;
- kein Kandidat freigegeben.

## Ergebnis
**2/2 Negativpfade PASS.**

Damit kann der spätere Image-only-Build weder mit unvollständigem 30er-Satz noch mit falschen Bildmaßen versehentlich als vollständiger Kandidat durchlaufen.
