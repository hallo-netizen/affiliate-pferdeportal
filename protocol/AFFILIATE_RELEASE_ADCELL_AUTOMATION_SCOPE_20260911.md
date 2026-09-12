# AFFILIATE RELEASE – ADCELL API-V2 AUTOMATISIERUNG – SCOPE 2026-09-11

STAND: 2026-09-12
STATUS: AKTIV / AUTH BELEGT / LOKALER SOURCE-KANDIDAT POSITIV-NEGATIV GEPRÜFT / KANONISCHE RÜCKBINDUNG BLOCKED / LIVE-ZUGANG BLOCKED

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

AF-023 wurde am 12.09.2026 behoben und mit dem originalen unveränderten Release-Guard real geprüft. Der committed Sourcebaum bleibt aktuell noch auf dem partiellen ADCELL-Stand mit Manifest:
`40dc3d56eba71a53edc87e425e8dc04416568365ee4b9e3d48320c3e25fff049`

Protokoll-/Evidence-/Hobbyraum-Commits ändern diesen 26-Dateien-Sourcebaum nicht.

## LOKALER GEPRÜFTER KANDIDAT – NOCH NICHT KANONISCH

Vollständiger Nachweis:
`release/affiliate-zentrale/evidence/adcell_api_v2_local_full_gate_20260912.txt`

Exakt drei freigegebene Traits geändert:
- `trait-ppar-automation-suite.php` – SHA256 `529c1da3cf943885094f7c7eed53c61caa3b11cf7c8eafbb766b77ddadfd4b4b` – Git blob Soll `e2dfa0734363a3c645c8e714edeb6e6ac7fa3e5e`
- `trait-ppar-network-sync.php` – SHA256 `a7183a025ccc55f756b15867ca2598963ea987f6b6baedef7c95078001d4ed12` – Git blob Soll `1bdcc564fe82e1d486523799211c3786c859b758`
- `trait-ppar-provider-registry.php` – SHA256 `87572d4bf2bcc2400fb3fa2cfd02050261c97555ce340f7981f1afbcd6a9e9ae` – Git blob Soll `82241b6451160d02caa92db3c053e96d5263bfb7`

Lokales finales 26-Dateien-Manifest:
`74a5d0d5e48028a9ddd82bcf7a32628dbeb42d0963c9ae431bfe8dee3e2c00e5`

Tatsächlich ausgeführt:
- PHP-Lint 21/21 PASS;
- ADCELL Static Gate PASS;
- ADCELL Runtime Positiv/Negativ PASS;
- AF-062 Hook-Runtime PASS;
- Banner-Regression PASS;
- exakt 3 erlaubte Source-Dateien geändert, außerhalb 0;
- 18/18 Awin-/OTTO-Funktionsblöcke byteidentisch zum kanonischen 6.72.8 – PASS über `AFFILIATE_HOBBYRAUM/test_adcell_awin_otto_unchanged.php`;
- originaler unveränderter `release_guard.py`: governance/source/tree/start jeweils PASS auf dem finalen lokalen Sourcebaum.

Der alte `test_otto_automation.php` ist bereits gegen unverändertes 6.72.8 stale/widersprüchlich. Diese AF-057-Ausprägung ist im aktuellen `TASK.current.json` durch den 18/18-Funktionshash-Test ersetzt. OTTO-Source wurde nicht verändert.

## FEHLERSTATUS

Detailautorität bleibt ausschließlich:
`AFFILIATE_HOBBYRAUM/FEHLERMATRIX.md`

Aktuell relevant:
- AF-023: BEHOBEN für den derzeit committed partiellen Source-Stand; Source/Manifest/Governance wurden atomar gebunden und Guard real PASS.
- AF-057: aktueller Hobbyraum-Task wurde auf den realen ADCELL-Rückbindungsweg nachgezogen; stale OTTO-Mischtest ist nicht mehr aktuelles Gate.
- AF-058 / AF-059 / AF-062: im lokalen Kandidaten positiv/negativ repariert, aber im kanonisch committed Sourcebaum noch NICHT geschlossen. Kein kanonischer PASS bis bytegenauer Rückbindung und erneutem committed Gate.
- AF-060: Auth-Dokumentationsblocker geschlossen; historische Gegenregel bleibt erhalten.

## AKTUELLER BLOCKER

Nicht der ADCELL-Code, sondern die bytegenaue Rückbindung:
Der in dieser Sitzung verfügbare GitHub-Schreibweg kann große lokale Dateien nicht direkt als Datei übernehmen. Manuell transportierte Großinhalte wurden an der Werkzeuggrenze gekürzt/verändert; die resultierenden Git-Blob-SHAs wichen vom lokalen Soll ab. Solche Blobs wurden verworfen und nie in den aktiven Sourcebaum committed.

Der aktive kanonische Sourcebaum darf deshalb nicht mit einem angenäherten oder rekonstruierten Inhalt überschrieben werden.

## VERBINDLICHE NEXT ACTION

GENAU EIN ARBEITSSTRANG:

1. Die drei oben gebundenen lokalen Source-Dateien bytegenau in GitHub-Blobs übertragen; jede Datei nur akzeptieren, wenn der Git-Blob-SHA exakt dem Soll entspricht.
2. Korrigierten ADCELL-Test, finales Manifest und die vollständige aktuelle Governance in denselben atomaren Tree/Commit binden.
3. Governance gemäß bereits vorgebundener `next_state_binding` auf Sequence 7 fortschreiben; Guard-Enum und erlaubte Prefixe unverändert lassen.
4. Commit gegen den vorherigen Head diffen und ausschließlich erwartete Dateien zulassen.
5. `affiliate-release-current` nur per Fast-Forward auf diesen geprüften Commit setzen.
6. Committed Stand frisch zurücklesen und dieselben ADCELL-, Awin/OTTO-Hash-, Banner- und Release-Guard-Gates erneut real ausführen.
7. Danach Fresh-Unpack + Source/ZIP Byte-Identity; erst danach Test-Plugin.
8. Live-PASS weiterhin erst nach wiederhergestelltem ADCELL-Zugang und echtem WordPress/MariaDB/API-E2E.

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
- Plugin-/ZIP-Ausgabe vor den gebundenen Gates;
- Codex.
