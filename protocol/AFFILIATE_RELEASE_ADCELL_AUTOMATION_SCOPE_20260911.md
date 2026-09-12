# AFFILIATE RELEASE – ADCELL API-V2 AUTOMATISIERUNG – SCOPE 2026-09-11

STAND: 2026-09-12
STATUS: AKTIV / AUTH BELEGT / KANONISCHER SOURCE-FIX COMMITTED + FULL GATE + FRESH-UNPACK/IDENTITY PASS / 6.72.9-VERSIONSBINDUNG OFFEN / LIVE-ZUGANG BLOCKED

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
ADCELL-Source-Commit: `99bcc5796226254f7e190f40397210fca96e7d0b`
Aktuelles 26-Dateien-Manifest:
`74a5d0d5e48028a9ddd82bcf7a32628dbeb42d0963c9ae431bfe8dee3e2c00e5`

Der kanonische ADCELL-Fix ist damit nicht mehr lokal/ungebunden. Die drei gebundenen Source-Dateien sind committed und Manifest/Governance wurden an denselben Sourcezustand gebunden.

## COMMITTED FULL GATE

Dauerhafter Nachweis:
`release/affiliate-zentrale/evidence/adcell_api_v2_committed_full_gate_20260912.txt`

Nach kanonischer Rückbindung tatsächlich ausgeführt und bestanden:
- committed Blob-/Source-Readback;
- ADCELL API-v2 Static Gate;
- ADCELL Runtime Positiv/Negativ;
- AF-062: kein Legacy-Basic-Auth-Runtimeweg für ADCELL-v2;
- accepted + active + programId-Allowlist positiv;
- non-allowlisted / inactive / not accepted / malformed / falscher Host / mehrdeutige CSV-Lage fail-closed;
- kein Awin-Fallthrough für `provider=adcell`;
- Awin/OTTO-Funktionsblock-Regression 18/18 byteidentisch;
- Banner-Regression;
- PHP-Lint 21/21;
- originaler unveränderter `release_guard.py`: Governance/Source/Tree/Start PASS;
- Fresh-Unpack PASS;
- Source/Unpack-Byte-Identity 26/26 PASS.

## FEHLERSTATUS

Detailautorität bleibt ausschließlich:
`AFFILIATE_HOBBYRAUM/FEHLERMATRIX.md`

Für den aktuellen kanonischen Stand:
- AF-023: geschlossen;
- AF-058: geschlossen;
- AF-059: geschlossen;
- AF-060: Auth-Dokumentationsblocker geschlossen;
- AF-062: geschlossen;
- AF-026/AF-027 bleiben als Versionsgrenzen aktiv und verhindern eine neue Test-/Live-ZIP mit erneutem internen Stand 6.72.8.

## 6.72.9 – VERSIONSSCHRITT

Für den nächsten installierbaren ADCELL-Testkandidaten ist deshalb der kleinste Versionsschritt `6.72.9` vorgesehen.

Lokal aus dem kanonischen 6.72.8-Sourcebaum vorbereitet und geprüft:
- exakt WordPress-Plugin-Header `6.72.8 -> 6.72.9`;
- exakt `const VERSION` `6.72.8 -> 6.72.9`;
- exakt readme `Stable tag` `6.72.8 -> 6.72.9`;
- keine fachliche ADCELL/Awin/OTTO-Logik geändert.

Lokales 6.72.9-Manifest:
`83c75bf1359aa989313416c9f9c7d1d4193bfe44a15bef08a83ac45580911bc8`

Auch auf diesem version-only Kandidaten ausgeführt PASS:
- PHP-Lint 21/21;
- ADCELL Static Gate;
- ADCELL Runtime Positiv/Negativ;
- Awin/OTTO-Identität 18/18;
- Banner-Regression;
- Fresh-Unpack;
- Source/Unpack-Identity 26/26.

WICHTIG: 6.72.9 ist noch **nicht kanonisch committed**. Der große Hauptplugin-Blob darf nur über einen bytegenau nachgewiesenen Transportweg geschrieben werden. Kein angenäherter, gekürzter oder rekonstruierter Großinhalt wird Release-Autorität.

## VERBINDLICHE NEXT ACTION

GENAU EIN ARBEITSSTRANG:

1. Den bereits lokal geprüften reinen Versionsschritt 6.72.8 -> 6.72.9 bytegenau auf `affiliate-release-current` binden.
2. Neues 26-Dateien-Manifest + Governance an exakt diesen committed Sourcezustand binden.
3. Dieselben ADCELL-, Awin/OTTO-, Banner-, PHP- und Release-Guard-Gates auf den committed 6.72.9-Bytes erneut real ausführen.
4. Fresh-Unpack + Source/ZIP-Identity für den committed 6.72.9-Testkandidaten wiederholen.
5. Erst danach darf ein 6.72.9-Test-Plugin ausgegeben/installiert werden.
6. LIVE-PASS erst nach wiederhergestelltem ADCELL-Zugang und echtem ADCELL-API + WordPress/MariaDB-E2E.

## LIVE-BLOCKER

Der ADCELL-Kontozugang ist weiterhin blockiert, weil Passwort-Wiederherstellung/Reset-Mail nicht funktioniert. Deshalb aktuell:
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
- Codex;
- Plugin-/ZIP-Ausgabe vor gebundener 6.72.9 + committed Gates + Fresh-Unpack/Identity.
