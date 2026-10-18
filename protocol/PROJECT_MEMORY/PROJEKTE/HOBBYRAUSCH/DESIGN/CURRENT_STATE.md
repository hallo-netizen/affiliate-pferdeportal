# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-18
STATUS: **LETZTER FUNKTIONIERENDER LIVE-STAND 1.50.677 / 1.50.679 LIVE-VERSUCH FATAL / 1.50.680 RELEASEKETTEN-FIX GEBAUT UND LOKAL POSITIV+NEGATIV GEPRÜFT / WORDPRESS-READBACK OFFEN**

Zielvertrag: **ZV-HOBBYRAUSCH-DESIGN-001 Fassung 4.7 / 2026-10-18**

## REALER LIVE-BEFUND 1.50.679

Nach Installation von 1.50.679 zeigte WordPress auf den Hobby-Depot-Seiten einen kritischen Fehler.

Exakte Ursache:
- Main lud `Hobby_Depot_Profile_V150679`;
- deren `route_template()` zeigte noch auf `hobby-depot-front-v150678.php` und `hobby-depot-content-v150678.php`;
- diese Templates riefen `Hobby_Depot_Profile_V150678` auf;
- damit war die aktive Versionskette erneut gemischt.

Das ist derselbe bereits bekannte Fehlertyp wie AF-043/AF-026. Die frühere 1.50.679-Aussage `Release-Kette PASS` war falsch und ist zurückgezogen.

## REPARATUR 1.50.680

Artefakt:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.680_HOBBY_DEPOT_RELEASE_CHAIN_FATAL_FIX.zip`

SHA-256:
`ed34fece94970fc5be1ddd9c4116f1cb5029360a99515484a2656f19b307b40a`

KISS-Delta gegenüber 1.50.679:
- geändert: nur `pferde-template-kit.php`;
- neu: `class-hobby-depot-profile-v150680.php`;
- neu: `hobby-depot-front-v150680.php`;
- neu: `hobby-depot-content-v150680.php`;
- keine Datei entfernt;
- 901/901 Bildassets byte-identisch;
- Texte, Hero-Logik, Kategoriebaum und Mega-Menü unverändert.

Aktive Kette:
- Main → V150680-Klasse;
- V150680 `route_template()` → V150680-Templates;
- V150680-Templates → `Hobby_Depot_Profile_V150680`.

## QA

- ZIP-Test PASS;
- PHP 87/87 PASS;
- Main-Version/Require/Classbindung PASS;
- realer `route_template()`-Positivtest: Front → V150680 PASS;
- realer `route_template()`-Positivtest: Content → V150680 PASS;
- beide V150680-Templates mit ausschließlich V150680-Klasse ausgeführt: PASS;
- Negativtest: nur V150679-Klasse vorhanden → beide V150680-Templates scheitern erwartungsgemäß auf fehlender V150680-Klasse;
- Paketdelta gegen 1.50.679 exakt 1 geänderte + 3 neue Dateien;
- keine Bildänderung.

## EXAKT EINE NEXT ACTION

**1.50.680 in WordPress über 1.50.679 installieren und eine Hobby-Depot-Start-/Kategorieseite aufrufen. Erst bei Frontend-PASS geht die visuelle Prüfung der 69 Hub2 weiter.**

## NICHT ANFASSEN

- Texte nicht erneut ändern;
- Bilder nicht ändern;
- Hero-/CSS-Regel nicht ändern;
- Mega-Menü nicht ändern;
- Kategoriebaum nicht ändern;
- keine Architekturänderung.
