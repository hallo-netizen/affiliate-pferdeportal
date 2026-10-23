# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-23
STATUS: **VOLLERSATZ HD-003 1.50.729 + HD-007 1.1.5 LOCAL HARD PASS / LIVE OFFEN**

Zielvertrag:
**ZV-HOBBYRAUSCH-DESIGN-001 Fassung 5.5 / 2026-10-19**

## Aktueller belastbarer Kandidat

`HOBBY_DEPOT_VOLLERSATZ_20261023_HD003_1.50.729_HD007_1.1.5.zip`

SHA-256:
`f735f41fa1740904e13428350bef04cb89c34664fbb6e8ff1014b8581b6de046`

Größe:
28,936,964 Bytes.

Enthält zwei vollständige bestehende Pluginwurzeln:
- `affiliate-portal-template-kit/`;
- `hd-hobbyregister-core/`.

Kein Delta, kein drittes Plugin.

## Korrigiert

- Footer-Logo kleiner/vollständig, Unterzeile physisch entfernt;
- Breadcrumb exakt nach Hobby-Depot-Standard statt falschem Astra-Hook;
- Auf einen Blick nur Icon + Wert;
- gleiche Hobbygruppe und ähnliche Hobbys disjunkt;
- Buttons gleiches helles Petrol;
- Gruppenüberschrift zweizeilig.

## QA

- Fresh-Unpack 954 Dateien;
- 14/14 PHP-Lint PASS;
- HD-007 4 E2E-Profile PASS;
- 862/862 Relationsaudit PASS;
- HD-003 Footer-Render PASS.

## EXAKT EINE NEXT ACTION

**Bestehende zwei Pluginordner vollständig ersetzen, nicht mergen; danach Live-Readback auf Version/HTML-Marker und sichtbare Änderungen.**
