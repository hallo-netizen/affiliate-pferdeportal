# HD-003 – EVIDENCE 1.50.717

STAND: 2026-10-23
STATUS: LOCAL HARD PASS / NICHT LIVE

Kandidat:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.717_UPDATE_MAGAZIN_ROUTING_FIX.zip`

SHA-256:
`8e03ce1e5915edd62901494362b70194ce09f971146dbcec424e927db1f46b59`

Größe:
577,238 Bytes.

Ursache:
Die produktive Magazinseite ist `/journal/`. 1.50.716 aktivierte die neue Magazin-Root-Darstellung nur für den Slug `magazin`. Zusätzlich war `journal` noch als Plain-Service-Seite klassifiziert und wurde daher nicht durch das Owned-Content-Template geroutet.

Fix:
- Magazin-Root akzeptiert `journal` und `magazin`;
- `journal` ist nicht mehr Plain-Service;
- Owned-Content-Routing erkennt die reale Magazinseite;
- Magazin-Renderer wird für beide Slugs genutzt;
- Affiliate-Page-Type erkennt beide Slugs.

Unverändert erhalten:
- 12 Magazin-Ziele;
- `journal_banner`;
- `journal_product_1–3`;
- Affiliate-Artikelbereich;
- FAQ;
- PB one neues Fenster.

QA:
- PHP-Lint PASS;
- ZIP exakt 2 Dateien;
- Fresh-Unpack + PHP-Lint PASS;
- Routing-/Service-/Renderer-Positivchecks PASS.
