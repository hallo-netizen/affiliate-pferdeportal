# PA-E-003 – Affiliate-Zentrale – isolierter Artefaktstatus

PLUGIN_ID: PA-E-003
NAME: Affiliate-Zentrale (Portal-kompatibel)

LETZTER_EXPLIZITER_LIVE_VERSIONSREADBACK: 6.72.170
LETZTER_EXPLIZITER_LIVE_STATUS: AKTIV
LIVE_READBACK: WordPress-Uploadvergleich des Nutzers am 01.10.2026 zeigt `Aktuell 6.72.170`. Kein neuerer Live-Versionsreadback wird erfunden.

LETZTER_VOLLSTÄNDIG_FREIGEGEBENER_TECHNISCHER_RELEASE: 6.72.210
FINAL_INSTALLER_REF: release/affiliate-zentrale/artifacts/final/AFFILIATE_ZENTRALE_6.72.210.zip
FINAL_INSTALLER_SHA256: 43ca6033a0f8dc929f777fc6580f2b41dfd711c6f561db99658f402cc5af88a1
FINAL_RELEASE_CHECK_RUN: 37788785260 = PASS
RELEASE_STATUS_6_72_210: RELEASED / release_allowed=true

AKTUELLER_TECHNISCHER_KANDIDAT: 6.72.211
CANDIDATE_STATUS: CANDIDATE_LOCAL_HARDTEST_PASS / release_allowed=false
CANDIDATE_SOURCE_MANIFEST_SHA256: 9f15bf679f44456c18c32aa6e04504e87248bc2748cfbca880532318915d311f
CANDIDATE_SOURCE_IMPLEMENTIERUNGSSTAND: 164cb789abcbfcffe70975fd463182041c5c923a
CANDIDATE_EVIDENCE: release/affiliate-zentrale/evidence/affiliate_router_v672211_frontend_context_cache_block8_20261008.md
CANDIDATE_TESTSTATUS: lokaler Positiv-/Negativ-/Regressionstest PASS; PHP-Lint 22/22 PASS; exakter WordPress-7.1.2/MariaDB-10.11-Gate für diesen Manifeststand OPEN.
CANDIDATE_RELEASE_INSTALL: KEIN RELEASE / KEINE INSTALLATION / KEIN FINALER INSTALLER.

AUTORITATIVE_FACHQUELLE: release/affiliate-zentrale/AGENTS.md -> control/release-governance/CURRENT_RELEASE.json

CURRENT_ZIP_STATUS: BLOCKED
BLOCKER: Für 6.72.211 existiert noch kein final freigegebener, exakt gegateter Installer. Eine isolierte `CURRENT.zip` darf deshalb nicht auf 6.72.211 ersetzt oder rekonstruiert werden.
ERFORDERLICHER_ARTIFAKTWEG: Erst exakten 6.72.211 WordPress/MariaDB-Gate PASS erreichen, danach exakt getesteten finalen Installer bauen/binden; erst dann isolierte `CURRENT.zip` byteidentisch synchronisieren und SHA-256 im Manifest nachziehen.

ROLLBACK: letzter vollständig freigegebener technischer Release 6.72.210 / SHA-256 43ca6033a0f8dc929f777fc6580f2b41dfd711c6f561db99658f402cc5af88a1.

ROLLE: Manifest/Blockerbeleg; keine Fach-/Release-/LIVE-Autorität.
