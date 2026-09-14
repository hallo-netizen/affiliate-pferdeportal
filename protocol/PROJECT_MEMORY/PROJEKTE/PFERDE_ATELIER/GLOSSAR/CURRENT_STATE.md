# BÜRO GLOSSAR – CURRENT_STATE

STAND: 2026-09-14
STATUS: GLOSSAR BREADCRUMB/HERO LIVE PASS / AUTOMATION-SANDBOX LIVE PASS / TERM-EXTRACTOR LIVE PASS / PORTALSEITEN-AUSSCHLUSS 1.3.4 LOKAL HART PASS, LIVE OFFEN / AUTO-PUBLISH AUS

## LIVE bestätigt – nicht regressieren

- Einzelbegriffe öffnen: **PASS**.
- Glossar-Fließtext: **0 Links – PASS**.
- rechte Ocker-Oberkante: **dünn – PASS**.
- Glossar-Breadcrumb Inhalt + Position/Abstand: **LIVE PASS**.
- Glossar-Hero: breites Bild + weicher Übergang: **LIVE PASS**.
- Automation-Sandbox: **LIVE PASS**; `ok:true`, alle Positiv-/Negativtests `true`, `production_write_performed:false`.
- Produktion scharf: **AUS**.
- Auto-Publish: **AUS**.
- Pool-Refresh: **LIVE PASS technisch**.
- Core 1.3.2/1.3.3 Term-Extractor: **LIVE PASS**; 14 PSTE-Rohfundstellen wurden auf 9 fachliche Kopfbegriffe reduziert, komplette Editorialtitel stehen nur noch als Rohfund.

## Aktueller LIVE-Pool nach Core 1.3.3

9 Begriffe:
- Fliegenmaske
- Hindernisstange
- Huffett
- Mistcontainer
- Pellet
- Pferdebürste
- Pferdehaftpflicht
- Regendecke
- Reitplatzbeleuchtung

Alle 9 stehen aktuell auf `QUARANTAENE`, `Dublette=NEIN`, `Kannibalisierung=JA`.
Die reine WordPress-Taxonomieprüfung meldet `Kategorie-Treffer=NEIN`.

## Nachgewiesene Ursache

Die starke Portal-Struktur des Pferde Atelier besteht technisch nicht nur aus WordPress-`category`-Termen. Viele SEO-Hauptseiten sind normale veröffentlichte hierarchische WordPress-Seiten (`post_type=page`). Deshalb konnte Core 1.3.3 diese nicht als Kategorie erkennen; die nachgelagerte Seiten-Kannibalisierung fing sie dennoch ab.

Öffentlich nachgewiesene starke Portal-Hauptseiten existieren für alle 9 aktuellen Begriffe, u. a. Regendecken, Fliegenmasken, Huffett, Pferdebürsten, Pferdehaftpflicht, Reitplatzbeleuchtung, Mistcontainer, Hindernisstangen und Pellets.

## Core-Kandidat 1.3.4 – Portal-Landingpage-Ausschluss

Paket: `UNIVERSAL_GLOSSARY_ENGINE_1.3.4_PORTALSEITEN_AUSSCHLUSS_INSTALLIEREN.zip`

SHA-256: `175e2f1d641a0b46eb9fe0c9de12b721fe4481424572dfdca1d76dbecbe3b6bc`

Neue Prüfreihenfolge:

`WP-Kategorie -> Portal-Landingpage -> Glossar-Dublette/Synonym -> sonstige Artikel-/Seiten-Kannibalisierung`

Regel:
- exakter bzw. gebundener Singular/Plural-Treffer gegen `post_type=page` -> `AUSGESCHLOSSEN_PORTALSEITE`;
- keine Recherche, kein Text, keine Veröffentlichung;
- normale Beiträge (`post`) werden nicht als Portal-Landingpage behandelt und bleiben normale Kannibalisierungsfälle;
- Prüftabelle zeigt zusätzlich `Portal-Seite = JA/NEIN`.

### Hart lokal positiv

Exakt gegen die 9 aktuellen LIVE-Begriffe mit den realen Portal-Seitentiteln geprüft:
- Fliegenmaske ↔ Fliegenmasken -> PASS
- Hindernisstange ↔ Hindernisstangen -> PASS
- Huffett ↔ Huffett -> PASS
- Mistcontainer ↔ Mistcontainer -> PASS
- Pellet ↔ Pellets -> PASS
- Pferdebürste ↔ Pferdebürsten -> PASS
- Pferdehaftpflicht ↔ Pferdehaftpflicht -> PASS
- Regendecke ↔ Regendecken -> PASS
- Reitplatzbeleuchtung ↔ Reitplatzbeleuchtung -> PASS

Alle 9 -> `AUSGESCHLOSSEN_PORTALSEITE` im lokalen Prüffixture.
`Widerrist` ohne Portalseite -> `KANDIDAT` PASS.
Exakter normaler Artikel `Huffett` ohne Portalseite -> weiterhin `QUARANTAENE` PASS.
Portalseiten-Ausschluss hat Vorrang vor generischer Kannibalisierung PASS.

### Hart lokal negativ

- Portalseiten-Gate absichtlich entfernt -> Test ROT.
- Singular/Plural-Familiennormalisierung absichtlich auf exakten Schlüssel reduziert -> Test ROT.
- Page-Inventory-Sammlung absichtlich entfernt -> Vertragscheck ROT.

### Regression/Verpackung

- PHP-Lint aller 3 PHP-Dateien PASS.
- gleicher Dateibestand wie 1.3.3: 3 Dateien.
- Content-Pack bytegleich.
- ZIP-Stamm `universal-glossary-engine/` PASS.
- ZIP-Lesetest PASS.
- Version 1.3.4 PASS.

## Journal

Design `1.50.498` ist lokal hart positiv/negativ gerendert geprüft; realer LIVE-Readback nach 1.50.498 steht noch aus. Kein LIVE-PASS behaupten.

## NEXT ACTION

1. Core `1.3.4` über `1.3.3` installieren.
2. `Glossar -> Automation -> Pool jetzt aktualisieren`.
3. Erwarteter realer Readback: die 9 aktuellen Begriffe wechseln von `QUARANTAENE` auf `AUSGESCHLOSSEN_PORTALSEITE`, sofern ihre Portal-Hauptseiten im WordPress-Inventar als veröffentlichte Seiten vorliegen.
4. Produktion scharf und Auto-Publish bleiben AUS.
5. Kein Automatiklauf vor diesem LIVE-Readback.