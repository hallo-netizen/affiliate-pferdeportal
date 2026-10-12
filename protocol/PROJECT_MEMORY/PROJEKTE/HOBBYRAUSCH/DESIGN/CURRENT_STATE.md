# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-12
STATUS: **1.50.629 LOCAL HARD PASS / WORDPRESS-LIVE BILDABNAHME OFFEN**

## Kandidat
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.629_HOBBY_DEPOT_WIDER_CLEARER_CATEGORY_IMAGES_LOCALPASS.zip`

SHA-256:
`6efba12354975852d8253e6141b0bbbcaf1174f60244a0e982e4caac0659c5cb`

Library:
`/hobby rausch/AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.629_HOBBY_DEPOT_WIDER_CLEARER_CATEGORY_IMAGES_LOCALPASS.zip`

## Live-Readback 1.50.628
**PASS / nicht mehr anfassen:**
- Hauptnavigation: alle acht Welten auf einer Ebene;
- Hero-Texte oben auf Ebene 1;
- Seitenendtexte auf Ebene 1 mit maximal drei internen Links.

**FAIL:**
- Kategorie-/Link-Bilder weiterhin zu eng hineingezoomt;
- teilweise nur Motivteile statt verständlichem Gesamtmotiv;
- zu viele Details / zu viel Bildinhalt;
- Thema nicht schnell genug erkennbar.

## Delta 1.50.629
Nur Kategorie-/Link-Bilder:
- die überenge 1.50.627-Bildrichtung wird zurückgenommen;
- 65 kontrollierte, ruhigere und weiter gefasste Motive werden als neue v150629-Assets gebunden;
- Grundlage ist der bereits lokal geprüfte einfache/klare 1.50.625-Motivsatz;
- Kartenfläche aus 1.50.628 bleibt unverändert;
- Navigation, Hero-Texte, Seitenendtexte, Monetarisierung, Taxonomie und Architektur bleiben unverändert.

## Lokal
- PHP 10/10 PASS;
- ZIP PASS;
- V150629 Main/Klasse/Templates konsistent;
- aktive V150628-Klassen-/Templatebindung 0;
- 65 v150629-Bildassets;
- alle 65 exakt 600×320;
- 65/65 eindeutige SHA-256;
- Weltabdeckung: Gestalten 7, Fertigen 11, Technik 9, Forschen 5, Pflanzen 10, Tiere 7, Bewegen 8, Sammeln 8;
- neue 65 Assets byteidentisch zum lokal geprüften einfachen/weiteren 1.50.625-Motivsatz;
- Diff gegen 1.50.628 bestätigt: Navigations-/Text-/Layoutlogik unverändert, nur Releasebindung + aktiver Bildsatz geändert.

## EXAKT EINE NEXT ACTION
**1.50.629 installieren und live nur die Kategorie-/Link-Bilder prüfen. Bei PASS danach direkt auf die nächste Kategorieebene gehen.**
