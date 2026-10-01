# HOBBYRAUSCH – TEXT_REDAKTION – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-01
STATUS: HD-001 PRODUKTIV LIVE + READBACK PASS / HD-002 V0.1.2 AUTO-HANDOFF HARD PASS / LIVE-INSTALLATION NÄCHSTES

## Live-Stand

HD-001:
- produktiver Buchbinden-Pilot live;
- Deployment abgeschlossen;
- Schreiben und Readback erfolgreich;
- nicht zurückrollen.

HD-002 aktuell live:
`Hobby Depot SEO Themenengine 0.1.1`
- sichere Migration COMPLETE;
- Backend READY;
- Website-Gesamtbild noch nicht erfasst.

## Owner-Handoff

Der produktive Buchbinden-Handoff ist jetzt fachlich bereit:
- 7 Owner;
- 11 ARTICLE_ONLY;
- 11/11 eindeutig gebunden;
- `READY_FOR_DOWNSTREAM_EDITORIAL_PLANNING`.

## HDTE 0.1.2

0.1.2 beseitigt den manuellen Übergabeschritt.

Beim Klick auf
`Gesamtbestand erfassen`
liest HDTE den **deployed** HD-001-Workspace read-only, validiert FINAL_APPROVED + Research erneut, übernimmt ausschließlich den gültigen Owner-Handoff in eigenen HDTE-Speicher und startet danach den normalen Baseline-/Portalabgleich.

Keine HD-001-Schreiboperation.

Exakter Buchbinden Positivtest:
- Auto-Sync PASS;
- Baseline CURRENT;
- 4 produktive Content-Kategorien;
- 1 Themenfamilie;
- 7 Owner / 11 Assignments;
- HD-001 unverändert.

Negativfälle fail-closed:
not deployed / Final fehlt / nicht final / Live-Kategorie fehlt / Handoff manipuliert.

Installer:
`HOBBY_DEPOT_SEO_THEMENENGINE_V0.1.2_AUTO_OWNER_HANDOFF_HARD_PASS.zip`

SHA:
`330028c8cd38f7f27664c804dfafa7649bea70e1f3647bc18229b52f2ba06003`

## NEXT ACTION

1. HDTE 0.1.2 installieren.
2. `Hobby Depot Themenengine → Übersicht → Gesamtbestand erfassen`.
3. Portalabgleich bis COMPLETE laufen lassen.

Erst danach DataForSEO-/Buchbinden-Themenproduktion starten.
