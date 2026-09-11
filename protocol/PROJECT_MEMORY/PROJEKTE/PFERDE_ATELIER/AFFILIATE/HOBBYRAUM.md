# AFFILIATE – HOBBYRAUM

STAND: 2026-09-11
STATUS: BLOCKED

## AKTUELLER AUFTRAG

ADCELL vollautomatisch über API v2 anbinden.

Normalweg:
`accepted + active Programme -> explizite programId-Allowlist -> CSV/Banner/Deeplink automatisch -> zentrale Affiliate-Prüfung/Ausgabe`.

Kein manueller Import/Export als Normalbetrieb.

## AKTUELLER BLOCKER

**AF-023 – Source/Manifest/Governance-Bindung ist nach dem partiellen ADCELL-Sourcecommit nicht mehr atomar.**

Der kanonische Sourcecommit `9815caaa24a6d2587da8890fb24773b2e67e76d8` änderte `trait-ppar-network-sync.php`, während `CURRENT_SOURCE_SHA256.txt` und die in `CURRENT_RELEASE.json` gebundene Manifest-SHA weiterhin den vorherigen Stand repräsentieren.

Deshalb:
- kein weiterer Sourcefix vor Wiederherstellung der Bindung;
- kein Release-Source-/Tree-PASS behaupten;
- kein Plugin bauen;
- keine Alternative/Side-Branch verwenden.

Zusätzlich fachlich offen, aber **nach** AF-023:
- AF-062: Provider-Registry ruft noch den Legacy-Basic-Auth-Verbindungstest auf;
- AF-058: ADCELL-Routing/Seite noch nicht vollständig vom Awin-Pfad getrennt;
- AF-059: Automationssuite nutzt noch den alten `csv-feed`-/manuellen CSV-URL-Normalweg.

Der offizielle API-v2-Auth-Vertrag selbst ist belegt; der frühere Dokumentationsblocker AF-060 ist insoweit geschlossen. Live-PASS bleibt wegen fehlendem ADCELL-Zugang zusätzlich gesperrt.

## NEXT ACTION

**GENAU EIN SCHRITT:**

Aktuellen kanonischen 26-Dateien-Sourcebaum auf `affiliate-release-current` neu hashen und **`CURRENT_SOURCE_SHA256.txt` + zugehörige Governance-Bindung atomar** auf denselben Iststand setzen; anschließend den echten Release-Governance-/Source-Guard ausführen.

Nur bei PASS dieses Schritts:
1. AF-062 Provider-Registry → `adcell_api_v2_test_connection()`; Legacy-Basic-Auth aus dem ADCELL-v2-Runtimeweg entfernen;
2. AF-058/059 im kanonischen Automationskern fertigstellen;
3. gebundene Positiv-/Negativ-/Gesamtworkflow-Prüfung;
4. Fresh-Unpack + Source/ZIP-Identity;
5. erst danach Test-Plugin.

## ARBEITSWEG

Technische Arbeits-/Rückgabeautorität:
`affiliate-release-current`

Technischer Scope:
`protocol/AFFILIATE_RELEASE_ADCELL_AUTOMATION_SCOPE_20260911.md`

Fehler:
`AFFILIATE_HOBBYRAUM/FEHLERMATRIX.md`

Task:
`AFFILIATE_HOBBYRAUM/TASK.current.json`

**WICHTIG:** Der bestehende Task ist bereits auf den nachfolgenden dreiteiligen ADCELL-Sourcefix gebunden. Solange AF-023 offen ist, darf er nicht als freigegebener Lauf gestartet werden. Erst Source-/Manifest-/Governance-Bindung reparieren, dann Task gegen den neuen gebundenen Source-Stand erneut validieren.

Side-Branch `hobbyroom/adcell-api-v2-automation-20260911` ist veraltet und keine technische Standwahrheit.

## RÜCKGABEWEG

Nur über den kanonischen Branch `affiliate-release-current` und die bestehende Release-Governance. Kein Side-Branch-Merge als Ersatzweg, keine Rekonstruktion.

## NICHT ANFASSEN

- Digistore24: BLOCKED/zurückgestellt, siehe `DIGISTORE24_STATUS.md`;
- OTTO/Awin: ungelöst und pausiert, nicht parallel fortsetzen;
- keine neue Providerarchitektur;
- kein eigenes ADCELL-Plugin;
- keine Pluginversionskette;
- keinen 6.72.18-Scratch übernehmen;
- keine manuelle CSV-URL als Ersatz für Vollautomatik;
- keine vom belegten Tokenvertrag abweichende Authentifizierung;
- kein Codex.
