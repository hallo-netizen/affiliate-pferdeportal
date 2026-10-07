# AFFILIATE-ZENTRALE — ÜBERGABEWEGWEISER 07.10.2026

**Rolle:** ausschließlich Navigation für den nächsten Chat. Keine CURRENT-/Status-/NEXT-ACTION-Wahrheit.

## Exakter Einstieg

1. `release/affiliate-zentrale/AGENTS.md`
2. `control/release-governance/CURRENT_RELEASE.json` — einzige Current-Autorität
3. den dort gebundenen Frische-/Release-Guard ausführen
4. exakt die dortige `execution_state.bound_user_scope_action` abarbeiten; beim ersten FAIL stoppen

## Fachlicher Zielvertrag

`protocol/AFFILIATE_RELEASE_BANNER_IMPORT_BASIS_TARGET_20261007.md`

Kern: **Importbasis zuerst vollständig und beweisbar machen; vor bestandenem Basis-Gate keine neue Ranking-/Zuordnungslogik.**

## Fehlerquelle

`protocol/AFFILIATE_RELEASE_ERROR_REGISTER.md` → `AFF-ERR-054` sowie Wiederholung `AFF-ERR-029`.

## Kanonische Source

- `release/affiliate-zentrale/current/affiliate-portal-router/`
- `release/affiliate-zentrale/CURRENT_SOURCE_SHA256.txt`

## Aktuelle Worktests

- `release/affiliate-zentrale/evidence/worktests/test_adcell_banner_import_basis_v672199.php`
- `release/affiliate-zentrale/evidence/worktests/test_adcell_banner_import_basis_e2e_v672199.php`
- `release/affiliate-zentrale/evidence/worktests/test_adcell_banner_basis_upgrade_v672199_e2e.php`

Die Existenz dieser Dateien ist **kein PASS**. Teststatus ausschließlich aus `CURRENT_RELEASE.json` und echter Evidence übernehmen.

## Nicht anfassen

- keine neue Banner-Ranking-/Target-Regel vor bestandenem Basis-Gate;
- keine manuelle FIXED-Zuordnung als Systemlösung;
- keine Hoster-/OPcache-/Serverdiagnose ohne Beleg;
- keine `.github/workflows/**`-Änderung;
- keine historische Root-`affiliate-portal-router/`-Quelle;
- kein ZIP/keine Live-Installation vor den gebundenen Gates;
- keine STARTMASTER-Navigation für diesen Workstream;
- keine Bibliotheksarbeit in dieser Übergabe.

Bei Widerspruch gilt ausschließlich `control/release-governance/CURRENT_RELEASE.json`.
