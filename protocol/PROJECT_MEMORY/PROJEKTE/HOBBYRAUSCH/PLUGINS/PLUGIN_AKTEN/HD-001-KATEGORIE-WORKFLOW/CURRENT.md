# HD-001 – KATEGORIE-WORKFLOW – CURRENT

STAND: 2026-09-30
STATUS: V1.9.1 EDITORIAL INTENT OWNERSHIP LOKAL HARD PASS / LIVE-ROLLBACK + RETEST OFFEN

## Aktueller belastbarer Stand

V1.9.1 ist die direkte Fortsetzung derselben Pluginlinie. Kein Zusatz-/Companion-Plugin.

Plugin:
`Affiliate-Portal Kategorie-Workflow V1.9.1`

Installer:
`AFFILIATE_PORTAL_KATEGORIE_WORKFLOW_V1.9.1_EDITORIAL_INTENT_OWNERSHIP.zip`

Installer SHA-256:
`92c8b4ee6e1c53ce677b7a059766796c02afc9d39cdcd5f86511bf51b8808b1f`

Source:
`QUELLCODE_KATEGORIE_WORKFLOW_V1.9.1_EDITORIAL_INTENT_OWNERSHIP.zip`

Source SHA-256:
`7ccb6f45f2728466392b4a56e6fcda44e71265b7138cdb55be9921b4d576cc32`

V1.9.1 enthält vollständig den V1.9.0-Stage-Hardlock:
- exakter serverseitiger Stage-Guard;
- stale spätere Aktionen BLOCKED;
- Downstream-Artefakte bei Upstream-Ersatz invalidiert;
- aktiver Deployment-Run blockiert neuen Upstream-Import bis Rollback.

Zusätzlich neu, allgemeingültig:
- finaler Report exportiert `research_evidence.editorial_handoff`;
- alle aktiven Strukturknoten werden als Kategorie-Owner-Registry ausgegeben;
- explizite `ARTICLE_ONLY`-Intents können mit `owner_concept_id` genau einem Owner zugeordnet werden;
- fehlender/ungültiger Owner oder derselbe exakte Intent bei mehreren Ownern blockiert nur den Editorial-Handoff;
- bestehender Kategorien-/Deployment-PASS wird dadurch nicht rückwirkend verändert;
- Residual-Research wird niemals automatisch zum Artikel;
- keine Beitragstitel- oder Textproduktion im Kategorie-Plugin.

## Harte lokale Prüfung

- Source Vollsuite: 248/248 PASS;
- Fresh-Unpack Source: 248/248 PASS;
- Source PHP-Lint: 18/18 PASS;
- Installer Runtime PHP-Lint: 17/17 PASS;
- Source↔Installer Runtime-Parität: 22/22 byteidentisch;
- Source-/Installer-Checksummen: PASS.

Realer bisheriger Hobby-Depot-Testbestand:
- 20 aktive Struktur-Owner erkannt;
- 27 bestehende `ARTICLE_ONLY`-Entscheidungen besitzen noch keinen `owner_concept_id`;
- deshalb Editorial-Handoff korrekt BLOCKED;
- Kategorienstand bleibt davon unberührt.

## Live-Status

V1.8.9 ist weiterhin der zuletzt dokumentierte Live-Stand und zeigt den unerwartet ausgeführten Test-Deployment-Run.

V1.9.1 ist lokal hart geprüft, aber noch NICHT live abgenommen.

## NEXT ACTION

V1.9.1 über V1.8.9 installieren → vorhandenen Test-Deployment-Run vollständig zurückrollen → denselben READ_ONLY_PREVIEW erneut übernehmen.

Erwartung:
- Stage exakt `structure_ready`;
- kein automatischer/staler Write;
- Kategorienprüfung unverändert;
- Editorial-Handoff zeigt die alten ungebundenen ARTICLE_ONLY-Intents sichtbar als offen/BLOCKED, bis ihre Owner fachlich zugeordnet sind.
