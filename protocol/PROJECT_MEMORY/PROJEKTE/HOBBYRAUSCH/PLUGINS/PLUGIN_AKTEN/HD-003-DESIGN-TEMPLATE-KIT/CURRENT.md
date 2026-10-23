# HD-003 – HOBBY DEPOT DESIGN / TEMPLATE KIT – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-23
STATUS: **LIVE 1.50.711 / 1.50.717 UPDATE LOKAL HARD PASS / CYBERDUCK-INSTALLATION OFFEN**

Plugin-ID:
`HD-003-DESIGN-TEMPLATE-KIT`

Fach-Current:
`../../../DESIGN/CURRENT_STATE.md`

## Live

Aktiv und zuletzt belastbar:
**1.50.711**.

## Lokaler Kandidat 1.50.717 – UPDATE

Artefakt:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.717_UPDATE_MAGAZIN_STARTSEITE.zip`

SHA-256:
`8e03ce1e5915edd62901494362b70194ce09f971146dbcec424e927db1f46b59`

Größe:
577,238 Bytes.

Enthält unter dem unveränderten Hauptordner `affiliate-portal-template-kit/` exakt:
- `pferde-template-kit.php`;
- `includes/class-hobby-depot-profile-v150709.php`.

## Magazin-Startseite

Die bestehende Seite `/magazin/` wird als eigene redaktionelle Hobby-Depot-Hubseite gerendert.

Verwendete 12 bestehende Magazin-Ziele:
Hobbyfinder; Alter & Lebensphasen; Geschichte & Herkunft; Hobby-Porträts; Hobby-Ideen & Inspiration; Menschen & Geschichten; Neue Hobbys & Trends; Saison, drinnen & draußen; Ungewöhnliche & skurrile Hobbys; Vergleiche & Alternativen; Wissen & Glossar; Zeit, Budget & Platz.

Keine neue Magazin-Kategorie angelegt.

Design:
- eigenes Magazin-Hero;
- 12 Bildkacheln;
- gleiche Farb-/Typo-/Kartenlogik wie Hobby Depot;
- responsive 3 / 2 / 2 Spalten;
- kein altes Pferde-Journal-Layout.

Monetarisierung:
- bestehender Slot `journal_banner`;
- bestehende Slots `journal_product_1–3`;
- eigener Bereich für erkannte/markierte Affiliate-Artikel;
- bestehende Rental-Werbefläche Placement `journal`;
- keine neue Affiliate-Architektur.

1.50.715 bleibt vollständig enthalten:
- FAQ-Seite;
- PB one öffnet in neuem Fenster;
- Footeränderungen.

Lokale QA:
- PHP-Lint PASS;
- ZIP exakt 2 Dateien;
- Fresh-Unpack PASS;
- 13/13 verwendete Bildassets vorhanden;
- Magazin-Sonderroute nur für Slug `magazin`;
- Banner/Produkte/Affiliate-Artikel integriert.

Evidence:
`EVIDENCE_1.50.717.md`

1.50.717 ist **nicht live**.

## EXAKT EINE NEXT ACTION

**1.50.717-UPDATE lokal entpacken und den enthaltenen Ordner `affiliate-portal-template-kit` per Cyberduck auf `wp-content/plugins/` ziehen/zusammenführen; die zwei enthaltenen Dateien überschreiben. Danach live ausschließlich Magazin-Startseite, FAQ, Footer/PB-one und Plugin-Version prüfen.**


## 1.50.717 Routingkorrektur

Die echte Magazinseite läuft unter `/journal/`. 1.50.716 hörte nur auf `magazin` und ließ `journal` zugleich als Service-Seite laufen. 1.50.717 korrigiert genau diese drei Routingstellen; Inhalt/Design/Slots bleiben unverändert.
