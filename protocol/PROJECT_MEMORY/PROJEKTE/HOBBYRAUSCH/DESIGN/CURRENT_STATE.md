# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-14
STATUS: **1.50.653–1.50.656 VERWORFEN / FALSCHE BASISWAHL ERKANNT / EXAKTER RUNTIME-RESTORE AUF LIVE-BESTÄTIGTEM 1.50.650 / 65 HEROES + 65 VORSCHAUEN STATISCH ERSETZT / LOKALER RENDER-PASS / KEIN LIVE-PASS**

## Exakter Fehlerbefund
Der entscheidende Basisfehler war, 1.50.651 als „funktionierenden“ Runtime-Stand zu behandeln.

Die Fehlerhistorie sagt eindeutig:
- **1.50.650: Text PASS + Grundaufteilung PASS**;
- **1.50.651: LIVE FAIL / verworfen** wegen Hero-/Bildmapping-/Unterstrich-/Zoomproblemen;
- 1.50.652 war nur der letzte paketierte VISUAL-FAIL-Stand, nicht freigegeben.

Damit durfte 1.50.651 nicht als technische Ausgangsbasis für weitere Reparaturpakete benutzt werden.

## Verworfen
- 1.50.653: Release-Ketten-Fatal;
- 1.50.654: LIVE FAIL;
- 1.50.655: LIVE FAIL;
- 1.50.656: LIVE FAIL.

## Neuer Reparaturstand
Paket:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.650_RUNTIME_RESTORE_NEW_IMAGES.zip`

SHA-256:
`c1717b196619a9decb1f5afe7946b56225d9d3f31889ccf7e8c07b3b5f0c928d`

### Harte Regel dieses Pakets
Der komplette ausführbare Runtime-Code bleibt exakt der bestätigte 1.50.650-Stand.

Geändert wurden ausschließlich statische Bilddateien:
- **65 Hero-Dateien** → 600×220;
- **65 Kategorievorschauen** → 200×107;
- insgesamt exakt **130 statische WebP-Dateien**.

Nicht geändert:
- 55/55 PHP-Dateien byte-identisch zu original 1.50.650;
- Plugin-Header und interne VERSION bleiben 1.50.650;
- Profilklasse bleibt `Hobby_Depot_Profile_V150650`;
- Routing unverändert;
- Front-/Content-Templates unverändert;
- CSS unverändert;
- Text/Grundaufteilung unverändert;
- keine Mapping-/Methodenänderung;
- keine neue Releaseklasse.

### Lokale Prüfung
- PHP-Dateien: **55/55 SHA-identisch zu original 1.50.650**;
- Nicht-Bild-Dateien: **0 Unterschiede**;
- PHP-Syntax: PASS;
- kompletter Hub2-Render `Druck & Fotografie`: **RENDER_OK**;
- Render-Fehlerausgabe: 0 Byte;
- geänderte Bilder: exakt **65× 600×220 + 65× 200×107**;
- ZIP-Integrität: PASS.

## EXAKT EINE NEXT ACTION
**Alle 1.50.653–1.50.656-Pakete nicht mehr verwenden. Den exakten 1.50.650-Runtime-Restore mit den neuen 130 Bilddateien installieren und nur /gestalten/druck-foto/ live prüfen. Erst bei realem Live-PASS weiterarbeiten.**
