# BÜRO GLOSSAR – CURRENT_STATE

STAND: 2026-09-14
STATUS: EINZELARTIKEL LIVE PASS / 0 FLIESSTEXTLINKS LIVE PASS / DUENNE OCKERLINIE LIVE PASS / BREADCRUMB-ABSTAND + KACHELKLICK + HERO-AUSSCHNITT LIVE FAIL / KANDIDAT 1.2.3 + 1.50.491 LOKAL PASS, NICHT LIVE

## Belastbarer aktueller Stand

- Arbeitsbranch: `hobbyroom/glossar-livefail-red-green-20260913`.
- Einzelbegriffe öffnen real: **LIVE PASS**.
- Glossar-Fließtext 0 Links: **LIVE PASS**.
- rechte Ocker-Oberkante dünn: **LIVE PASS**.
- Diese beiden PASS-Punkte nicht erneut anfassen.

## Aktuell offen – Nutzerreadback 2026-09-14

1. Breadcrumb-Inhalt ist korrekt; **Abstand nach oben ist zu groß**. Er muss auf allen Glossarseiten einheitlich sein: Glossar-Startseite, `uge_group`-Kategorie und `uge_term`-Einzelansicht.
2. Begriffskacheln müssen **komplett anklickbar** sein, nicht nur `Zum Begriff`.
3. Glossar-Hero muss **weiter herausgezoomt / Motiv rechts vollständig erkennbar** sein.

## Lokaler Design-Kandidat 1.50.491

Paket: `PFERDE_ATELIER_DESIGN_V1.50.491_GLOSSAR_NAV_HERO_FIX_INSTALLIEREN.zip`

SHA-256: `e5913fd60b59ce6b49a354a98f0f2bd132df6356720ed8d5ee76309abd811d51`

Geändert und lokal geprüft:
- einheitlicher Glossar-Topabstand über `.site-content`: 18 px für Startseite/Kategorie/Single;
- Single-Innenpadding so angepasst, dass keine Doppeladdition entsteht;
- komplette Begriffskachel ist ein Link;
- Hero-Bild `object-fit: contain` + rechts ausgerichtet statt starkem `cover`-Beschnitt;
- 0-Link-Endschranke im Fließtext bleibt unverändert;
- 2-px-Ockerlinie bleibt unverändert;
- PHP-Lint PASS, statischer Positiv-/Negativvertrag PASS, ZIP-Lesetest PASS.

## Lokaler Core-Kandidat 1.2.3

Paket: `UNIVERSAL_GLOSSARY_ENGINE_1.2.3_NEUE_BEITRAEGE_INSTALLIEREN.zip`

SHA-256: `997cd888fe3ea1a102a8d5c9e614497404d5049e5c64086f330f0dc77c07049f`

Zusätzlich zum 14er Bestandsupdate:
- `Aalstrich` wird aus frisch gelesenem WDB-Status `GEPRUEFT` übernommen/überschrieben;
- `Zuchtbuch` wird als neuer Glossarbegriff aus frisch gelesenem WDB-Status `GEPRUEFT` ergänzt;
- beide 150–200 Wörter, 0 Fließtextlinks;
- State `1.2.3:16` erzwingt sauberen Update-Lauf;
- Gruppe `Zucht & Genetik` wird technisch gebunden;
- PHP-Lint PASS, beide neuen Texte Wortlänge PASS, 0 Links PASS, ZIP-Lesetest PASS.

Fachquellen bleiben ausschließlich die WDB-Datensätze `term-aalstrich.json` und `term-zuchtbuch.json`; keine Fachwahrheit im Glossarbüro duplizieren.

## Harte Grenze

**Noch kein LIVE PASS für 1.2.3 / 1.50.491.** Erst Installation und realer Readback dürfen die offenen Punkte schließen.

## Nächster Schritt

1. Core `1.2.3` installieren.
2. Design `1.50.491` installieren.
3. real prüfen: Breadcrumb-Abstand auf Glossar-Startseite, Kategorie und Einzelbegriff einheitlich; komplette Kacheln klickbar; Hero-Motiv vollständig verständlich.
4. prüfen: 0 Fließtextlinks und 2-px-Ockerlinie bleiben PASS.
5. `Zuchtbuch` und `Aalstrich` real öffnen und Inhalts-/Darstellungsprüfung durchführen.
