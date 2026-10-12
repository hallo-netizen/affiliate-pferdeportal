# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-12
STATUS: **1.50.647 LOCAL HARD PASS / WORDPRESS-LIVE OFFEN**

## Kandidat
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.647_HOBBY_DEPOT_HUB2_RELEASE_CHAIN_FATAL_FIX_LOCALPASS.zip`

SHA-256:
`db5427357bd251f084ab9a8545dee33d760a7b38ace686a5146543ca07210833`

Library:
`/hobby rausch/AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.647_HOBBY_DEPOT_HUB2_RELEASE_CHAIN_FATAL_FIX_LOCALPASS.zip`

## Live-Befund 1.50.646
**KRITISCHER WORDPRESS-FEHLER. 1.50.646 VERWORFEN.**

Exakte Ursache:
- Hauptplugin lud korrekt `Hobby_Depot_Profile_V150646`;
- diese Klasse routete aber weiter auf `hobby-depot-front-v150645.php` / `hobby-depot-content-v150645.php`;
- diese Templates riefen `Hobby_Depot_Profile_V150645::...` auf;
- die 1.50.645-Klasse war im aktiven 1.50.646-Pfad nicht geladen;
- dadurch entstand ein Runtime-Fatal durch gemischte Release-Bindung.

## Fix 1.50.647
Die Release-Kette ist jetzt end-to-end konsistent:
`pferde-template-kit.php → V150647 Profil → v150647 Templates → Hobby_Depot_Profile_V150647`.

Der beauftragte 1.50.646-Inhalt bleibt fachlich erhalten:
- alle Hub2-/Ebene-2-Kategorien erhalten kompakten Hero mit vorhandenem Bild und weichem Verlauf;
- individuelle kurze Brush-/Schreibschrift-Claims;
- Aufklapptext nach der bestehenden Pferdeatelier-Regel;
- vorhandene Assets werden wiederverwendet;
- keine unnötigen neuen Bilder;
- Hub2: Kategorien → Produkte → 3 Beiträge → Werbeplatz;
- kein zusätzlicher unterer Editorial-Block.

## Lokal geprüft
- alle **53 PHP-Dateien** Syntax-PASS;
- ZIP-Integrität PASS;
- Main-Version 1.50.647 PASS;
- aktiver Require-Pfad 1.50.647 PASS;
- aktive Klasse 1.50.647 PASS;
- Front-Template 1.50.647 PASS;
- Content-Template 1.50.647 PASS;
- beide Templates rufen ausschließlich `Hobby_Depot_Profile_V150647` auf;
- aktiver Stale-Reference-Check gegen V150645/V150646: **0 Treffer**.

## EXAKT EINE NEXT ACTION
**1.50.647 installieren und echten WordPress-Readback durchführen.**
