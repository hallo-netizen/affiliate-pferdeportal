# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-12
STATUS: **1.50.636 LOCAL HARD PASS / WORDPRESS-LIVE HUB2 OFFEN**

## Kandidat
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.636_HOBBY_DEPOT_HUB2_REFINEMENT_TEST_POSTS_LOCALPASS.zip`

SHA-256:
`d8d45997b136cd7d95e0a790f88dfbb4b3207a29b5b644e415b1ac8e0a72007a`

## Live-Befund 1.50.635
- Grundaufbau Hub2 funktioniert;
- oberer Text zu kurz/technisch;
- identisches Welticon auf zu vielen Unterkategorie-Karten wirkt monoton;
- Beitragsvorschau ohne reale Testbeiträge nicht sinnvoll beurteilbar.

## Delta 1.50.636 – nur Hub2
- oberer Hub2-Einstieg deutlich länger, natürlicher und in vollständigen Sätzen/Absätzen;
- kein Hero-Foto;
- Hub2-Titel und Unterkategorie-Karten erhalten thematisch unterschiedliche Icons statt eines immer gleichen Welticons;
- Beitragsvorschau zeigt auf Hub2 bis zu 4 Beiträge;
- 4 klar markierte veröffentlichte Testbeiträge werden beim ersten Admin-Aufruf einmalig angelegt;
- jeder Testbeitrag erhält ein Beitragsbild aus bereits vorhandenen Designassets;
- Testbeiträge werden allen aktuell vorhandenen WordPress-Beitragskategorien zugeordnet; zusätzlich allen journal_cat-Terms, falls diese Taxonomie Posts unterstützt;
- Testbeiträge tragen Meta `_hd_demo_post_v150636=1` und sind damit später eindeutig entfernbar.

## Freeze / unverändert
- 847/847 Assets byteidentisch zu 1.50.635;
- Hero-Assets byteidentisch;
- Header/Nav unverändert;
- Ebene 1 unverändert;
- Taxonomie-/Kategoriearchitektur unverändert;
- Affiliate-Slotlogik unverändert.

## Lokal geprüft / simuliert
- PHP **22/22 PASS**;
- ZIP PASS;
- Hub2-Simulation 1440 / 1024 / 760: horizontaler Overflow 0;
- längerer Toptext in zwei lesbaren Absätzen;
- 9 Beispiel-Unterkategorien mit thematisch unterschiedlichen Symbolen geprüft;
- 4 Beitragskarten mit Bild bei Desktop, 2-spaltig auf Tablet, 1-spaltig mobil;
- Seed-Code: einmalig, Admin-only, 4 Posts, alle Beitragskategorien, Featured Images;
- keine Hero-Datei geändert.

## EXAKT EINE NEXT ACTION
**1.50.636 installieren; danach live Hub2 einschließlich automatisch angelegter 4 Testbeiträge prüfen.**
