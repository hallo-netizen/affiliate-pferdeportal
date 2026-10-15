# HOBBYRAUSCH – IMAGE STAGE BUILDER – TEST 7

STAND: 2026-10-15
STATUS: PASS / ARBEITSHILFE / KEIN PLUGIN / KEIN RELEASE

Werkzeug:
`tools/hobby_image_stage_builder.py`

SHA-256:
`4fef9d3586f8dd0f30c8e67b8912343a8a1e3b988343d07f4469d0e28fe0c9ad`

Zweck:
Nach Erzeugung einer echten neuen Einzelquelle automatisch dieselbe Quelle in:
- Hero 600×320;
- Preview 200×107
ableiten, ohne Hochskalierung.

Zusätzliche harte Technikprüfungen:
- fehlende Quelldatei = FAIL;
- Quelle kleiner als Ziel = FAIL;
- Hero/Preview falsches Maß = FAIL;
- exakte Bilddublette = FAIL;
- dHash-Abstand wird für Nah-Dubletten protokolliert;
- keine Plugin-, CSS-, Mapping- oder Templateänderung.

## Realtest mit den 7 vorhandenen neuen Einzelquellen

PASS:
- 7/7 Quellen verarbeitet;
- 0 Fehler;
- 7/7 Heroes exakt 600×320;
- 7/7 Previews exakt 200×107;
- 0 Hochskalierungen;
- 0 exakte Hero-Dubletten;
- 0 exakte Preview-Dubletten;
- kleinster Hero-dHash-Abstand: 105/256;
- kleinster Preview-dHash-Abstand: 109/256.

Report SHA-256:
`e78624050abfd2f1d8bc54650dec5751b71bd810b5c78e4705aa52dbae098fca`

Wichtig:
Das Werkzeug ersetzt keine visuelle Motivprüfung. Ausgabe bleibt `PASS_TECHNICAL_PENDING_VISUAL`, bis Semantik, Zoom und sichtbarer Ausschnitt geprüft sind.
