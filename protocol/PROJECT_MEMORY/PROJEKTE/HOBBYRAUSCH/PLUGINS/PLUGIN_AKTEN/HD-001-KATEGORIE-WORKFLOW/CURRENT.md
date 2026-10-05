# HD-001 – KATEGORIE-WORKFLOW – CURRENT

STAND: 2026-10-05
STATUS: V1.9.9 PFERDEATELIER-TAXONOMIE LOCAL HARD PASS / LIVE-READBACK OFFEN

## Harte Korrektur

V1.9.7 und V1.9.8 NICHT installieren.

Der funktionierende Pferdeatelier-Aufbau wurde erneut direkt geprüft:
- drei Seitenebenen nativ;
- Ebene-4-Kategorien sind Root-`category`-Terme;
- kein technischer Bridge;
- Kontext steckt in Kategorie-Name/Slug und Routing/Renderer.

## V1.9.9

Korrigierte gleiche Pluginlinie.

Content:
- Level 1–3 WordPress-Seiten;
- Level 4 Root-`category`, `parent=0`;
- stabile logische Bindung an die Ebene-3-Seite;
- Speichername kontextuell eindeutig;
- Frontend-Bezeichnung kurz;
- bestehende IDs bleiben migrierbar.

Magazin:
- `journal_cat` separat.

HivePress:
- `hp_listing_category` separat.

## Prüfung

- 270/270 PASS;
- Full Builder Flex PASS;
- realer Buchbinden-Altbestand PASS;
- Full E2E Positiv PASS;
- Full E2E Negativ PASS;
- Fresh-Unpack erneut PASS;
- Runtime-Parität 19/19;
- Installer PHP 19/19 PASS.

Installer SHA-256:
`601a7c7e8a796a12cb9f27388899cdd82264e460314284e29f5ef0018c33e05a`

Source SHA-256:
`6ace7bb651025729da6a80d055076c689ee5ff3ba619ec783c1bebb07cda25e9`

## ERSTER BLOCKER

`HD001_V199_LIVE_INSTALL_AND_FRONTEND_READBACK_OPEN`

## NEXT ACTION

V1.9.9 installieren → Buchbinden publish/republish → echtes Frontend prüfen.
