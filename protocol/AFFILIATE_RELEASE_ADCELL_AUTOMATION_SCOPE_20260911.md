# AFFILIATE RELEASE – ADCELL API-V2 AUTOMATISIERUNG – SCOPE 2026-09-11

STAND: 2026-09-12
STATUS: AKTIV / 6.72.19 KANONISCH + FULL GATE + KANONISCHER ARTEFAKT-26/26-PASS / AF-066 READ-ONLY LIVE-API-PREFLIGHT OFFEN

## VERBINDLICHES ZIEL

Normalbetrieb:

`ADCELL API v2 -> accepted + active Programme -> explizite programId-Allowlist -> CSV/Banner/Deeplink API -> bestehende zentrale Creative-/Relevanz-/Asset-/Output-/Pause-/Veto-Logik`

Pflicht:
- kein Awin-Fallthrough für `provider=adcell`;
- keine manuelle ADCELL-CSV-URL als Normalbetrieb;
- nur explizit allowlisted `programId` und gleichzeitig aktuell `affiliateStatus=accepted` + `isActive=1`;
- nicht allowlisted / inactive / nicht accepted / malformed / falscher Host / mehrdeutige CSV-Lage fail-closed;
- keine neue Providerarchitektur und kein separates ADCELL-Plugin;
- keine automatische Veröffentlichung außerhalb der bestehenden zentralen Sicherheitslogik.

Digistore24 bleibt DEFERRED. OTTO/Awin bleibt PAUSED_UNRESOLVED_NOT_PASSED_NOT_REPLACED.

## AUTORITATIVE API-V2-FAKTEN

Evidence:
`release/affiliate-zentrale/evidence/adcell_api_v2_auth_contract_20260911.txt`

Belegt:
- API-Basis `https://api.adcell.org/api/v2/`;
- Token über `/user/getToken` mit `userName` + `password`;
- weitere Requests mit Parameter `token`; kein belegter Basic-/Bearer-Vertrag für diesen v2-Weg;
- Programme: `/affiliate/program/export`, u. a. `programId`, `programName`, `isActive`, `affiliateStatus`;
- Promotionen: `getPromotionTypeCsv`, `getPromotionTypeBanner`, `getPromotionTypeDeeplink`;
- CSV liefert `csvUrl`;
- Banner liefert u. a. `promotionId`, `programId`, `clickoutLink`, `trackViewLink`, `width`, `height`, `bannerUrl`;
- Deeplink ist programmspezifisch und liefert u. a. `promotionId`, `programId`, `clickoutLink`.

## KANONISCHE SOURCE-AUTORITÄT

Branch: `affiliate-release-current`
Source: `release/affiliate-zentrale/current/affiliate-portal-router/`
Version: `6.72.19`
Source-Bind-Commit:
`df3e97119fe44ac864701d8de6b946c7c6c3416c`

Kanonisches 26-Dateien-Manifest:
`694af9869c7aa2b01a51f164173b1c51d9be7c24912c2e129420c3d111346a4b`

Pluginbüro-Stand 6.72.17 und der geprüfte ADCELL-API-v2-Fix wurden konfliktfrei als 6.72.19 zusammengeführt und kanonisch gebunden.

## KANONISCHER PRÜFSTAND

Full-Gate-Lauf:
- Run `34690118524`
- Job `103543774405`
- Ergebnis: PASS

Tatsächlich belegt PASS:
- ADCELL API-v2 Static Gate;
- ADCELL Runtime Positiv/Negativ über exakt hash-identische kanonische ADCELL-Dateien;
- offizieller Tokenweg; kein Legacy-Basic-Auth-Runtimeweg für ADCELL-v2;
- accepted + active + programId-Allowlist positiv;
- non-allowlisted / inactive / not accepted / malformed / falscher Host / mehrdeutige CSV-Lage fail-closed;
- kein Awin-Fallthrough;
- Awin/OTTO-Funktionsblock-Regression 18/18 PASS;
- Banner Positiv/Negativ PASS;
- PHP-Lint 21/21 PASS;
- originaler Release-Guard Governance/Source/Tree/Start PASS;
- Fresh-Unpack PASS;
- Source/ZIP-Byte-Identity 26/26 PASS;
- Plugin-Header / `const VERSION` / Stable tag = 6.72.19 PASS.

Dauerhafter Nachweis:
`release/affiliate-zentrale/evidence/adcell_67219_canonical_full_gate_20260912.txt`

Status-Closeout danach ebenfalls Release-Guard-PASS:
- Run `34690263204`
- Job `103544153132`

Temporäre Transport-/Gate-Workflows wurden anschließend wieder entfernt. Es bleibt kein zusätzlicher dauerhafter Runner zurück.

## FEHLERSTATUS

Detailautorität bleibt ausschließlich:
`AFFILIATE_HOBBYRAUM/FEHLERMATRIX.md`

Für den aktuellen ADCELL-Meilenstein geschlossen:
- AF-023 Source/Manifest/Governance-Bindung;
- AF-057 aktueller Task-/Regressionstest-Bind;
- AF-058 kein Awin-Fallthrough;
- AF-059 kein manueller CSV-Normalweg;
- AF-060 offizieller API-v2-Auth-Vertrag;
- AF-062 Legacy-Basic-Runtimeweg;
- AF-063 falsche 6.72.9-Hashtranskription;
- AF-064 falsche Versionsbasis;
- AF-065 Governance-Vertragswert `new_version_policy`.
- AF-067 falsches Vor-Bind-ZIP; kanonischer Artefaktneubau Run `34692865477` PASS.

Aktiv:
- AF-066 read-only Live-API-Preflight im echten WordPress noch nicht ausgeführt.

## AKTUELLER TASK

Autorität:
`AFFILIATE_HOBBYRAUM/TASK.current.json`

Status: `BLOCKED`

Keine weitere Sourcearbeit. AF-067 ist geschlossen: aus der kanonischen 6.72.19-Source wurde ein neues Testartefakt gebaut und 26/26 gegengeprüft.

Artefakt-Nachweis:
- Run `34692865477` / Job `103551115066` → PASS;
- Test-ZIP SHA-256 `72f437e5235aaec53631db052e2184b588366c7f8aa7eb72ae1c9e043cdf157f`;
- GitHub-Actions-Artefakt-ID `10297556084` (temporärer Übergabe-/Testbeleg, keine finale Releasefreigabe).

PLUGIN-KONTROLLREF: `PU-20260912-001` im Campus-PLUGINS-Updateprotokoll. Fach-/Release-/LIVE-Wahrheit bleibt hier.

## LIVE-PREFLIGHT / VERBINDLICHE NEXT ACTION

AF-066 korrigiert den früher zu früh angenommenen Weblogin-Blocker.

Nächster echter Gate:
1. im realen WordPress den kanonischen 6.72.19-Stand verwenden/readbacken;
2. dort read-only **`Token + Programme prüfen`** mit den bereits gespeicherten ADCELL-API-Zugangsdaten ausführen;
3. bei PASS einen vorhandenen `accepted` + aktiven `programId` explizit allowlisten und direkt den realen ADCELL-/WordPress-/MariaDB-E2E fortsetzen;
4. nur wenn gespeicherte API-Zugangsdaten fehlen/ungültig sind, wird Credential-Recovery zum echten Blocker.

Bis zum realen Ergebnis:
- kein Live-PASS;
- `release_allowed=false`;
- Zielvertrag bleibt AKTIV;
- keine weitere ADCELL-Sourceänderung;
- keine neue Versionskette.

## NICHT ANFASSEN

- ADCELL-Source bis zum Live-Test;
- Digistore24;
- OTTO/Awin-Weiterentwicklung;
- STARTMASTER/Textmaschine;
- 6.72.18-Scratch;
- neue Providerarchitektur / separates ADCELL-Plugin;
- manuelle CSV-Import-/Exportlösung als Ersatz;
- neue Workflow-/Runner-Dateien;
- neue Versionsnummer vor dem realen Live-Test;
- Codex.
