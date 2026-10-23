# HD-003 – EVIDENCE 1.50.715

STAND: 2026-10-23
STATUS: LOCAL HARD PASS / NICHT LIVE

Kandidat:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.715_DELTA_FAQ_PBONE.zip`

SHA-256:
`2c6594ee4fae4d37cc9fa43a6e5183e190bcb86ae13db29c924346d73a2ae33a`

Größe:
574,666 Bytes.

## Delta

Enthält exakt zwei Dateien:
- `pferde-template-kit.php`
- `includes/class-hobby-depot-profile-v150709.php`

## Änderungen

- Plugin-/Runtime-Version 1.50.715.
- PB-one-Link im Footer öffnet extern mit `target="_blank" rel="noopener noreferrer"`.
- Bestehende WordPress-Seite `/faq/` bleibt Datenbank-/Seitenobjekt; HD-003 liefert nur bei genau dieser Seite den sichtbaren FAQ-Inhalt.
- 6 Themenbereiche, 30 Fragen.
- Native HTML-`details`/`summary`-Akkordeons; kein JavaScript, kein Zusatzplugin.
- Kurze, direkte Antworten in Du-Ansprache.
- Eigene responsive FAQ-CSS-Regeln.
- FAQ-Meta-Description als Fallback, solange auf der WordPress-Seite keine eigene SEO-Description gesetzt ist.

## QA

- ZIP enthält exakt 2 Dateien: PASS.
- PHP-Lint beider Dateien vor dem Packen: PASS.
- Fresh-Unpack + PHP-Lint beider Dateien: PASS.
- FAQ-Render-Harness: 6 Bereiche / 30 `details`: PASS.
- alter FAQ-Seiteninhalt wird auf `/faq/` nicht doppelt ausgegeben: PASS.
- FAQ-Renderer greift nur auf singulärer Seite mit Slug `faq`: PASS.
- kein FAQ-JavaScript vorhanden: PASS.
- PB one neues Fenster: PASS.

Kein Live-PASS behaupten.
