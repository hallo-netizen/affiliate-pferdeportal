# HD-003 – HOBBY DEPOT DESIGN / TEMPLATE KIT – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-11  
STATUS: **1.50.613 LOCAL HARD PASS / LIVE-PASS OFFEN / CAMPUS-CURRENT.ZIP-SYNC BLOCKED**

## Plugin

ID:
`HD-003-DESIGN-TEMPLATE-KIT`

Name:
`Affiliate Portal Template Kit – Hobby Depot Profil`

Theme-Basis:
`ListingHive`

## Aktuelle technische Wahrheit

Version:
**1.50.613**

Kandidat:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.613_HOBBY_DEPOT_HUB1_BREADCRUMB_MONETIZATION_LOCALPASS.zip`

SHA-256:
`56aa6f55542570d2383bd6fff92aaddcf155cf103cf14faccf80994636250d34`

Library:
`/hobby rausch/AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.613_HOBBY_DEPOT_HUB1_BREADCRUMB_MONETIZATION_LOCALPASS.zip`

Campus-CURRENT.zip:
nicht synchronisiert; kein Binärartefakt erfunden.

## Scope 1.50.613

Startseite:
- Navigation Desktop real 14 px tiefer;
- Hobbyfinder/Magazin/Wissen einheitlich creme;
- öffentlicher Verkaufswerbeplatz mit „Hier könnte Ihre Werbung stehen.“;
- genau ein Direktwerbeplatz;
- Affiliate-Leerregeln unverändert.

CORE-/Kategoriepfad:
- neues eigenes Contenttemplate;
- Breadcrumb außer Startseite;
- Titel-/Introbereich;
- Hub1-Welthero aus exakt demselben kontrollierten Weltasset wie die Startseitenkarte;
- direkte nächste Ebene;
- Affiliate-Banner;
- Beitragsvorschau;
- Affiliate-Produkte;
- genau ein Direktwerbeplatz.

Unterstützte CORE-Typen:
`hub1`, `hub2`, `category`, `leaf`.

Zusätzlich:
WordPress-Kategoriearchive und `journal_cat` erhalten denselben Breadcrumb-/Contentmodulpfad.

## Lokale Abnahme

Fresh:
- PHP **10/10 PASS**;
- ZIP-Integrität PASS;
- SHA-256 verifiziert.

Homepage:
- Direktwerbeplatz öffentlich PASS;
- Direktwerbeplatz count=1 PASS;
- Affiliate leer öffentlich hidden PASS;
- Affiliate leer eingeloggt visible PASS;
- Editorialkarten einheitlich creme PASS;
- Navigation-Absenkung PASS.

Hub1:
- Breadcrumb PASS;
- identisches Weltasset Startkarte/Hubhero PASS;
- nächste Ebene PASS;
- Bannerplatz PASS;
- Beitragsvorschau PASS;
- Produktplätze PASS;
- Direktwerbeplatz count=1 PASS.

Kategorie:
- Breadcrumb PASS;
- Banner PASS;
- Beiträge PASS;
- Produkte PASS;
- Direktwerbeplatz count=1 PASS.

## Rollback

Bei Livefehler:
kein Blindfix; realen Readback eingrenzen und nur belegtes Delta reparieren.

## EXAKT EINE NEXT ACTION

**1.50.613 installieren und Startseite + eine erste Welt-Hubseite live prüfen.**
