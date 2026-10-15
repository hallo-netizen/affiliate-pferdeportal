# HOBBYRAUSCH – FINAL IMAGE-ONLY PLUGIN BUILDER – TEST 30

STAND: 2026-10-15
STATUS: **TECHNISCH PASS / KEIN ECHTER RELEASE**

Werkzeug:
`tools/hobby_final_image_plugin_build.py`

Lokale Werkzeug-SHA-256:
`c9fed12eb45467adf325c3ddccfab2561bab3c1ee7dbeec44da9635c4ee9ad8b`

## Zweck
Ein einziger finaler Buildschritt, sobald 30/30 echte visuell freigegebene Einzelquellen vorliegen.

Der Builder erledigt in einem Lauf:
1. Manifest muss exakt 30 Kategorien enthalten;
2. außerhalb Testmodus muss `release_allowed=true` gesetzt sein;
3. 30/30 Kategorien müssen `ready_source` sein;
4. 30/30 deterministische Quelldateien müssen existieren;
5. Upscaling ist verboten;
6. Hero 600×320 + Preview 200×107 werden aus derselben Quelle erzeugt;
7. exakte und technische Nah-Dubletten werden gesperrt;
8. 60/60 bestehende Zielpfade auf 1.50.650 müssen existieren;
9. exakt 60 Bilddateien dürfen sich ändern;
10. 0 Dateien dürfen hinzukommen oder verschwinden;
11. Mapping muss byte-identisch bleiben;
12. ZIP-Roundtrip muss vollständig identisch sein.

## Volltest mit 30 synthetischen Quellen
Synthetische Quellen dienen ausschließlich zum technischen Pipeline-Test und wurden nicht als Hobbybilder oder Releasebestand verwendet.

PASS:
- 30/30 Quellen verarbeitet;
- 60 Bilddateien geändert;
- 0 Dateien hinzugefügt;
- 0 Dateien entfernt;
- 0 unerwartete Änderungen;
- Mapping identisch;
- ZIP-Roundtrip identisch;
- finaler Testbuild technisch PASS.

Test-ZIP SHA-256:
`5a2269f71f841ec1e83b65b163d80d70cbd0fa26b6277182f9998794aa7e49c0`

Die synthetische Test-ZIP ist **kein auslieferbares Plugin**.

## Negativtests
PASS:
- `release_allowed=false` → sauberer STOP / Exit 2;
- fehlende Quelle → sauberer STOP / Exit 2;
- exakte doppelte Quelle → sauberer STOP / Exit 2.

## Ergebnis
Sobald der echte 30/30-Quellenbestand visuell PASS ist, ist kein weiterer Architektur-, Mapping-, CSS-, PHP- oder Packaging-Schritt mehr zu entwickeln. Der Builder erzeugt dann direkt den reinen Image-only-Plugin-Kandidaten auf Basis 1.50.650.
