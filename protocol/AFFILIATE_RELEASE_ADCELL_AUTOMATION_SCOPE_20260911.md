# AFFILIATE RELEASE – ADCELL API-V2 AUTOMATISIERUNG – SCOPE 2026-09-11

STAND: 2026-09-12
STATUS: AKTIV / KANONISCHER ADCELL-SOURCEFIX + COMMITTED FULL GATE + FRESH-UNPACK/IDENTITY PASS / 6.72.9 VERSION-BIND OFFEN / LIVE-ZUGANG BLOCKED

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

Der frühere 6.72.18-Scratch bleibt verworfen und ist keine Source-Autorität.

## KANONISCHE SOURCE-AUTORITÄT

Branch: `affiliate-release-current`
Source: `release/affiliate-zentrale/current/affiliate-portal-router/`
Version: `6.72.8`
Manifest:
`74a5d0d5e48028a9ddd82bcf7a32628dbeb42d0963c9ae431bfe8dee3e2c00e5`

Der ADCELL API-v2 Sourcefix ist kanonisch committed. Tatsächlich erneut auf dem committed Stand ausgeführt und bestanden:
- ADCELL Static Gate PASS;
- ADCELL Runtime Positiv/Negativ PASS;
- AF-062 Hook-Runtime PASS;
- Awin/OTTO-Funktionsblock-Regression 18/18 PASS;
- Banner-Regression PASS;
- PHP-Lint 21/21 PASS;
- originaler unveränderter Release-Guard Governance/Source/Tree/Start PASS;
- Fresh-Unpack 26/26 Source-ZIP-Byte-Identity PASS;
- Fresh-Unpack PHP-Lint 21/21 PASS.

Dauerhafter Nachweis:
`release/affiliate-zentrale/evidence/adcell_api_v2_committed_full_gate_20260912.txt`

## 6.72.9 VERSION-ONLY-KANDIDAT – NOCH NICHT KANONISCH

AF-026/027 verlangen vor einem neuen installierbaren Kandidaten eine Versionsgrenze oberhalb 6.72.8.

Lokal wurde deshalb ausschließlich die Versionsgrenze 6.72.8 -> 6.72.9 vorbereitet:
- Plugin-Header `Version: 6.72.9`;
- Klassenkonstante `VERSION = '6.72.9'`;
- Readme `Stable tag: 6.72.9`.

Keine Fachlogik geändert.

Exakter lokaler 6.72.9-Manifesthash:
`83c75bf16578e986388d684fbd99b4ffff400a11b34aca1c74fd5eb41e6b2f3e`

Gegenprüfung 2026-09-12:
- gespeicherte Manifestdatei: SHA256 exakt `83c75bf16578e986388d684fbd99b4ffff400a11b34aca1c74fd5eb41e6b2f3e`;
- 26/26 Manifestzeilen stimmen gegen den tatsächlichen 6.72.9-Baum;
- aus dem Baum regeneriertes Manifest ist byteidentisch zur gespeicherten Manifestdatei;
- Fresh-Unpack enthält dieselben 26 Dateien und 0 Byte-Abweichungen;
- internes Gate-ZIP SHA256 `03271c48076ef142b12a6fcdb0e03433daeeaf51cde2b5010f0a904e7dea6cd4`.

Die früher dokumentierte Zeichenfolge `83c75bf1359...` war eine Transkriptionsabweichung und ist unter AF-063 als Fehler gebunden. Sie ist keine Autorität.

6.72.9 bleibt bis zur bytegenauen kanonischen Bindung ausschließlich lokaler Versionskandidat.

## FEHLERSTATUS

Detailautorität bleibt ausschließlich:
`AFFILIATE_HOBBYRAUM/FEHLERMATRIX.md`

Aktuell relevant:
- AF-023: BEHOBEN.
- AF-057: BEHOBEN für den aktuellen ADCELL-Meilenstein.
- AF-058 / AF-059 / AF-060 / AF-062: BEHOBEN und auf committed 6.72.8 gegengeprüft.
- AF-063: AKTIV bis alle falschen 6.72.9-Hashreferenzen auf den exakt neu verifizierten Manifesthash korrigiert sind; erst danach darf 6.72.9 kanonisiert werden.

## VERBINDLICHE NEXT ACTION

GENAU EIN ARBEITSSTRANG:

1. AF-063 vollständig schließen: ausschließlich den exakt verifizierten 6.72.9-Manifesthash `83c75bf16578e986388d684fbd99b4ffff400a11b34aca1c74fd5eb41e6b2f3e` in Status/Evidence/Governance/Campus verwenden.
2. Danach nur die bereits lokal geprüfte Versionsgrenze 6.72.8 -> 6.72.9 bytegenau auf `affiliate-release-current` binden; keine Fachlogik ändern.
3. Manifest + Governance atomar an denselben committed 6.72.9-Sourcezustand binden.
4. Committed Stand frisch zurücklesen und dieselben ADCELL-, Awin/OTTO-, Banner-, PHP- und Release-Guard-Gates erneut real ausführen.
5. Fresh-Unpack + Source/ZIP-Identity erneut ausführen.
6. Erst danach Test-Plugin/Live-Testkandidat zulassen.
7. LIVE PASS ausschließlich nach wiederhergestelltem ADCELL-Zugang und echtem WordPress/MariaDB/API-E2E.

## LIVE-BLOCKER

Der ADCELL-Kontozugang ist weiterhin blockiert, weil Passwort-Wiederherstellung/Reset-Mail nicht funktioniert. Deshalb:
- kein echter ADCELL-Live-API-Request;
- kein WordPress/MariaDB/API-Live-E2E;
- kein LIVE PASS.

## NICHT ANFASSEN

- Digistore24;
- OTTO/Awin-FeedScope-Weiterentwicklung;
- STARTMASTER/Textmaschine;
- 6.72.18-Scratch;
- neue Providerarchitektur / separates ADCELL-Plugin;
- manuelle CSV-Import-/Exportlösung als Ersatz;
- neue Workflow-/Runner-Dateien;
- Fachlogik beim 6.72.9-Versionsbind;
- Codex.
