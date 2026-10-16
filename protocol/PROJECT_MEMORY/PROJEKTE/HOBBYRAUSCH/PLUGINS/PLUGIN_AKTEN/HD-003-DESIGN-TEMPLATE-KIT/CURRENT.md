# HD-003 – HOBBY DEPOT DESIGN / TEMPLATE KIT – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-16
STATUS: **1.50.664–1.50.667 VERWORFEN / 1.50.668 REGISTRY-FUNDAMENT LOCAL HARD PASS / LIVE NACH STRUKTUR-SYNC**

## Aktiver Grundstand

Affiliate Portal Template Kit **1.50.650** bleibt Ausgangsbasis.

Nicht verwenden:
- 1.50.664;
- 1.50.665;
- 1.50.666;
- 1.50.667.

Diese Versionen lösten die Live-Probleme Mega-Menü/Kategorietext nicht zuverlässig und dürfen nicht als Basis weitergeführt werden.

## Kandidat 1.50.668

`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.668_HOBBY_DEPOT_REGISTRY_FOUNDATION_LOCALPASS.zip`

SHA-256:
`0fb575aeddd19aac285188507d0753eaa554b558183d6686c2a900322c865a5a`

Library:
`/hobby rausch/releases/AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.668_HOBBY_DEPOT_REGISTRY_FOUNDATION_LOCALPASS.zip`

QA:
`/hobby rausch/releases/HOBBY_DEPOT_REGISTRY_FOUNDATION_150668_QA_20261016.json`

## Aufgabe dieses Kandidaten

Nur Fundament:
- Struktur ausschließlich aus HD-004;
- rohe WordPress-Altseiten dürfen nicht mehr durchrutschen;
- terminale `category`-Ebene wird korrekt ausgegeben;
- Hub2-Unterebene Icon/Text;
- keine Zufalls-Fotofallbacks;
- fail-closed ohne Registry.

Nicht enthalten:
- neuer Mega-Menü-Entwurf;
- Kategorietext-Redesign;
- weitere Bildänderungen.

## Local Hard QA

- PHP 58/58 PASS;
- 0 Bilddateien geändert;
- ZIP-Roundtrip 984/984;
- absichtliches falsches Trainspotting wird von Registry ausgeschlossen;
- Ameisenhaltung zeigt 7 Registry-Kategorien;
- Browser 1440 / 1024 / 768 / 390: 0 horizontaler Overflow;
- fehlende Registry: fail-closed.

## Abhängigkeit

HD-004 muss als Runtime-Wahrheit vorhanden sein. 1.50.668 fällt bewusst **nicht** still auf die alte WordPress-Struktur zurück.

## EXAKT EINE NEXT ACTION

**Noch nicht installieren: zuerst V3-Kategorie-Sync + Readback abschließen. Danach HD-004 aktivieren und 1.50.668 als Fundament live prüfen.**
