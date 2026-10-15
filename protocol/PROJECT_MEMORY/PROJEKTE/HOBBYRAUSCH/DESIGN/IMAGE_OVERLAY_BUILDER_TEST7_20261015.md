# HOBBYRAUSCH – IMAGE-ONLY OVERLAY BUILDER – TEST 7

STAND: 2026-10-15
STATUS: PASS / ARBEITSHILFE / KEIN RELEASE

Werkzeug:
`tools/hobby_image_overlay_builder.py`

SHA-256:
`a5c6c73c84e5a4b1830b94befa3828191e1a2e4be329483a8b856b8f7ab6e0cc`

Zweck:
Aus der eingefrorenen echten 1.50.650-Basis einen reinen Bildersatz-Kandidaten bauen, ohne andere Dateien anzufassen.

## Realtest mit 7 vorhandenen neuen Quellen
Basis:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.650_BASE.zip`

Eingesetzte Kategorien:
- Astronomie
- Papierkunst
- Textilgestaltung
- Malen & Zeichnen
- Schrift & Lettering
- Guss & Formen
- Miniaturen & Szenen

Ergebnis:
- 7/7 Kategorien ersetzt;
- exakt 14 Dateien geändert;
- 0 Dateien hinzugefügt;
- 0 Dateien entfernt;
- 0 unerwartete Änderungen;
- Mapping SHA vor/nach identisch;
- alle Heroes 600×320;
- alle Previews 200×107;
- ZIP-Roundtrip vollständig identisch zum simulierten Dateibaum;
- `pass_technical=true`.

Test-ZIP SHA-256:
`0018f903f9c987a4ac87c727d05f6f0d92dd927bb798c0767ef8930f99b10b98`

Report SHA-256:
`43770942ecd9d7ada3615970c81a2a6765a3b7d4dd089fcd06a674275214e14a`

## Schutz
Standardmäßig ist ein unvollständiger Stage gesperrt. `--allow-partial` ist nur für WIP-/Testläufe vorgesehen.

Das Werkzeug:
- ersetzt nur im Manifest freigegebene bestehende Bildpfade;
- stoppt bei falschen Bildmaßen;
- prüft nach dem Build den gesamten Dateibaum;
- verlangt Mapping-Identität;
- meldet jede zusätzliche/entfernte/unzulässig geänderte Datei;
- ersetzt keine visuelle Motivprüfung und keinen Live-Readback.
