# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-12
STATUS: **1.50.631 LOCAL HARD PASS / WORDPRESS-LIVE OFFEN**

## Kandidat
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.631_HOBBY_DEPOT_REAL_ZOOMOUT_UNIQUE_IMAGES_HEADER_LINE_FIX_LOCALPASS.zip`

SHA-256:
`94b31dad40c8806fad72ab1a8c576cd6333832224c5fbd122820ce7859a184f0`

Library:
`/hobby rausch/AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.631_HOBBY_DEPOT_REAL_ZOOMOUT_UNIQUE_IMAGES_HEADER_LINE_FIX_LOCALPASS.zip`

## Letzter echter Live-Befund
PASS / nicht anfassen:
- Hero-Texte Ebene 1;
- Seitenendtexte Ebene 1 mit maximal drei internen Links;
- acht Navigationspunkte bleiben auf gemeinsamer Baseline.

FAIL:
- 1.50.629 änderte die sichtbaren Kategorie-Vorschaubilder nicht belastbar;
- 1.50.630 band fälschlich den alten v150623-Bildsatz vor und erzeugte dadurch wieder sichtbar wiederholte Szenen;
- Claim war nicht sauber mittig unter HOBBY DEPOT;
- Claim-Unterkante und Navigations-Unterkante lagen nicht auf einer Linie.

## Root Cause 1.50.630
- v150623 enthält zwar byte-eindeutige Dateien, aber mehrere wiederverwendete Szenenfamilien (u. a. Outdoor, Werkbank, Sammeln);
- die 1.50.630-Bindung bevorzugte genau diesen Satz;
- im Header verbreiterte `.hd-logo-claim-v150622{transform:scaleX(1.06)}` den Claim nach rechts;
- lokale Geometriesimulation zeigte Claim/Navi-Abstand: Desktop 7 px, 761–1000 px 38 px.

## Delta 1.50.631
Bilder:
- ausschließlich die 65 eindeutigen v150629-Quellmotive werden verwendet;
- daraus wurden 65 tatsächlich neue v150631-Dateien erzeugt;
- jedes Motiv wurde sichtbar auf 80 % verkleinert und mit ruhigem, weich erweitertem Bildumfeld auf 600×320 gesetzt;
- kein v150623-Bild ist im aktiven Hub1-Bildpfad;
- Hub1 fällt bei fehlendem kontrolliertem Asset nicht mehr auf alte WordPress-Featured-Images zurück.

Header:
- Claim-Skalierung nach rechts entfernt;
- Claim exakt gleich breit/zentriert wie die HOBBY-DEPOT-Wortmarke;
- Logo gezielt nach unten gesetzt;
- lokale Geometriesimulation: Claim-Unterkante = Navigations-Unterkante bei 1600/1440/1200/1024/900/800/761 px, Delta jeweils 0 px.

## Lokal
- PHP 13/13 PASS;
- ZIP-Integrität PASS;
- V150631 Main/Klasse/Templates konsistent;
- 65 v150631-Bilder;
- 65/65 exakt 600×320;
- 65/65 SHA-256-eindeutig;
- kein aktiver v150623-Bildpfad;
- lokaler visueller 65er-Gesamtcheck ohne die in 1.50.630 sichtbaren wiederholten Szenenfamilien;
- Header-Geometrie 7 Viewports: 0 px Claim/Navi-Delta.

## EXAKT EINE NEXT ACTION
**1.50.631 installieren und live nur zwei Dinge prüfen: Kategorie-Vorschaubilder sowie Logo/Claim/Navigation. Bei PASS danach direkt nächste Kategorieebene.**
