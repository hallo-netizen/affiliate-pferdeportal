# HOBBYRAUSCH – ANZEIGEN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-24
STATUS: **ANZEIGENBÜRO ANGELEGT / ANZEIGENFÜLLER 1.0.0 INSTALLIERBARER KANDIDAT / LIVE-ZUGANGSTEST OFFEN**

## Ziel
Eigenes Anzeigenbüro für Hobby Depot. HivePress bleibt Anzeigenmodell und Frontend-Autorität.

## Anzeigenfüller
Plugin: **Hobby Depot Anzeigenfüller 1.0.0**

Artefakt:
`HOBBY_DEPOT_ANZEIGENFUELLER_1.0.0.zip`

SHA-256:
`dff617355e87dea82b4dbfe55d6cda572df8ed1b57351a9cc08d6504870ecbc9`

Pluginordner:
`hobby-depot-anzeigenfueller/`

## Übernommenes Pferdeatelier-Prinzip
Nur der alte PRIVATE/INDIVIDUAL-Weg wurde fachlich übernommen:
- eBay Browse API;
- Verkäuferkontotyp ausschließlich `INDIVIDUAL`;
- Marketplace ausschließlich `EBAY_DE`;
- Ausgabe als `hp_listing`;
- Bild wird als WordPress-Beitragsbild übernommen;
- eBay itemId verhindert Dubletten;
- Affiliate-Link in `hp_url`.

Nicht übernommen:
- Pferde-/Reitsportbegriffe;
- Pferde-Kategorien;
- Pferdeportal-Klassen/Optionen;
- BUSINESS-Produktstrecke;
- übrige Affiliate-Zentrale.

## Sicherheitsvertrag
- Standard: Draft-only.
- Direkt-Publish nur nach expliziter Aktivierung im Backend.
- Ohne eindeutige HivePress-Kategorie wird ein Angebot übersprungen.
- Optionaler Automatiklauf alle 6 Stunden.
- Live-eBay-Verbindung benötigt Client-ID, Client-Secret und EPN Campaign-ID.

## QA
- PHP-Lint PASS.
- ZIP-Integrität PASS.
- statischer Pferde-/Reitsport-Altbezug: 0.
- lokaler Harness: Query-Parsing PASS, INDIVIDUAL akzeptiert, BUSINESS blockiert, erzwungenes und automatisches Kategorien-Mapping PASS.
- externer Live-eBay-Zugang nicht ohne echte Zugangsdaten getestet.

## Nächster Schritt
Plugin auf Hobby Depot installieren, Zugangsdaten hinterlegen, zunächst 2–3 Suchzeilen mit exaktem Kategorie-Slug als Draft importieren und Ergebnis im HivePress-Anzeigenmarkt prüfen.
