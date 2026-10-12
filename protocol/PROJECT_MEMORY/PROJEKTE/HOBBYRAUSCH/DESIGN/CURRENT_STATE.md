# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-12
STATUS: **1.50.648 LOCAL HARD PASS / WORDPRESS-LIVE OFFEN**

## Kandidat
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.648_HOBBY_DEPOT_ALL_HUB2_EXACT_645_LAYOUT_PFERDE_RULE_PERF_LOCALPASS.zip`

SHA-256:
`8ffc125dcbe95d2657c29ea43ebb69e9be609268ec4c40277a34a15c49502038`

Library:
`/hobby rausch/AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.648_HOBBY_DEPOT_ALL_HUB2_EXACT_645_LAYOUT_PFERDE_RULE_PERF_LOCALPASS.zip`

## Ausgang
**1.50.647 wird verworfen.**
Der technische Fatal war dort zwar beseitigt, aber der Rollout hatte den akzeptierten 1.50.645-Aufbau von Buch & Papier wieder durch eine andere Hub2-Logik ersetzt.

## 1.50.648
Basis ist deshalb wieder **1.50.645**. Der akzeptierte sichtbare Aufbau wird auf alle 65 Hub2-/Ebene-2-Seiten ausgerollt, nicht neu erfunden.

Verbindlich:
- derselbe kompakte Split-Hero wie bei Buch & Papier;
- rechts das bereits vorhandene Kategorie-Vorschaubild mit weichem Verlauf ins Weiß;
- kurzer individueller Claim in derselben Schreibschrift-/Brush-Optik;
- Pferdeatelier-Textregel 1:1: ca. 55 Wörter Lead → `Mehr erfahren` → `Was du hier findest` dauerhaft sichtbar;
- Öffnen des Texts verändert die Hero-Bildgröße nicht;
- Unterkategorien als Fotokarten, kein Icon-Rückfall;
- vorhandenes Featured/Controlled Image zuerst; nur wenn keines existiert, wird performance-schonend das vorhandene Elternmotiv wiederverwendet;
- 3er-Raster; Restkarten linksbündig; Affiliate-Banner füllt den freien Restplatz bzw. bei voller Reihe eine eigene Bannerzeile;
- danach konkrete Produkte → 3 Beiträge → genau ein Werbeplatz;
- kein zusätzlicher Textblock am Seitenende.

## Performance / Regression
- **keine neuen Bildassets**;
- 859/859 Assets byteidentisch zu 1.50.645;
- 65/65 Hub2-Hero-Motive aus vorhandenem Bestand gefunden;
- 65/65 individuelle Claims vorhanden;
- Header/Navigation/Ebene 1/Taxonomie unverändert;
- PHP **52/52 PASS**;
- ZIP PASS;
- Release-Kette vollständig 1.50.648;
- aktive Stale-V150645/V150646/V150647-Bindung im aktiven Pfad: 0;
- Browser 1440 / 1024 / 900 / 760: Overflow 0;
- Desktop 1440/1024: 3 + 2 + Banner;
- Bild/Slot-Abweichung 0;
- Foto-Radius 0;
- Aufklappen: Hero-Bild Δ Breite/Höhe 0;
- `Was du hier findest` bleibt sichtbar.

## EXAKT EINE NEXT ACTION
**1.50.648 installieren und live zuerst Buch & Papier plus zwei weitere Hub2-Kategorien aus unterschiedlichen Welten prüfen.**
