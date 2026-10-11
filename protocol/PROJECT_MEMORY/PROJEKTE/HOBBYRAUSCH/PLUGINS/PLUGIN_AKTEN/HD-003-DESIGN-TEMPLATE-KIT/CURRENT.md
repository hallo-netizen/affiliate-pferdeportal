# HD-003 – HOBBY DEPOT DESIGN / TEMPLATE KIT – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-11  
STATUS: **1.50.615 LOCAL HARD PASS / LIVE-PASS OFFEN / CAMPUS-CURRENT.ZIP-SYNC BLOCKED**

## Plugin

ID:
`HD-003-DESIGN-TEMPLATE-KIT`

Name:
`Affiliate Portal Template Kit – Hobby Depot Profil`

Theme-Basis:
`ListingHive`

## Aktuelle technische Wahrheit

Version:
**1.50.615**

Kandidat:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.615_HOBBY_DEPOT_PHOTO_HUB_RESPONSIVE_NAV_LOCALPASS.zip`

SHA-256:
`17d03f5704d8f140a86f4bbbdc4109cf564522a663660d0bd333be456dc3fda6`

Library:
`/hobby rausch/AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.615_HOBBY_DEPOT_PHOTO_HUB_RESPONSIVE_NAV_LOCALPASS.zip`

Campus-CURRENT.zip:
nicht synchronisiert; kein Binärartefakt erfunden.

## Scope 1.50.615

Header:
- Topbar dunkel wie Footer;
- Navigation Desktop weiter nach unten;
- Logo und Topbar-Inhalt unverändert.

Kategorietexte:
- Pferdeatelier-Regel übernommen;
- manuelle Texte geschützt;
- Auto-Fallback aus Titel, Ebene, Parent/Children und Themenprofil;
- >~130 Wörter: Lead ~55 Wörter + `Mehr erfahren` + sichtbares `Was du hier findest`;
- Gestalten enthält konkreten Beispieltext.

Unterkategorien:
- Desktop 6-Spalten-Logik gegen leere Restflächen;
- Rest 2 = zwei halbe Karten;
- Rest 1 = letzte Karte volle Reihe;
- Tablet 2 / Mobile 1.

Monetarisierung:
- Direktwerbung direkt nach Unterkategorien;
- attraktives Bildcollage-Modul mit `Hier könnte Ihre Werbung stehen.`;
- CTA `Werbemöglichkeiten & Preise`;
- maximal einmal;
- Affiliate-Banner nativ integriert, kleine Werbekennzeichnung;
- Affiliate-Produkte als native Kartenfläche;
- öffentlich leer unsichtbar, eingeloggt leer sichtbar.

## Scope 1.50.615 Zusatzdelta

Responsive Navigation:
- Vollnavigation >1320 px;
- 761–1320 px Hamburger-/Dropdownmodus;
- <980 px Dropdown 2-spaltig;
- keine abgeschnittene letzte Welt.

Hubfotos:
- nur Hub1/Hub2;
- echtes Featured Image zuerst;
- sonst kontrollierter Crop des Weltmotivs;
- tiefere Ebenen bleiben ohne Bildzwang.

## Lokale Abnahme

- ZIP-Integrität PASS;
- PHP 10/10 PASS;
- statischer Responsive-Test: Breakpoint 1320 / Hamburger sichtbar / Nav aus Desktopreihe gelöst PASS;
- Hubfoto-Test: Featured Image gewinnt PASS;
- Hubfoto-Fallback: Weltasset PASS;
- tiefe Category ohne Bildzwang PASS;
- PHP 10/10 PASS;
- Intro-Accordion-Test PASS;
- Textintegrität Anfang/Ende PASS;
- Gestalten-Beispieltext vorhanden;
- Rest-1/Rest-2-Rasterregeln vorhanden;
- Direktwerbung vor Beiträgen PASS;
- Affiliate-Banner danach PASS;
- Produkte danach PASS;
- Topbar dunkel PASS;
- Navigation-Absenkung PASS;
- 8 Weltassets 1400×620;
- Logo byteidentisch zum freigegebenen Vorgänger.

## Rollback

Bei Livefehler:
kein Blindfix; realen Readback eingrenzen und nur belegtes Delta reparieren.

## EXAKT EINE NEXT ACTION

**1.50.615 installieren und Startseite + Gestalten bei Desktop, mittlerer Breite und Mobile live prüfen.**
