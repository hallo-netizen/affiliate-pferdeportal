# AFFILIATE – CURRENT STATE

STAND: 2026-09-11
STATUS: ADCELL API-V2-AUTOMATISIERUNG AKTIV / PARTIELLER SOURCEFIX / BLOCKED AUF SOURCE-MANIFEST-BINDUNG

## AUTORITÄT

Diese Datei ist die einzige aktuelle Campus-Standzusammenfassung des Büros AFFILIATE.

- aktuelle Arbeit / NEXT ACTION → `HOBBYRAUM.md`
- Fehler → `protocol/PROJECT_MEMORY/FEHLERREGISTER.md` → Originalquelle
- Zielvertrag → `protocol/PROJECT_MEMORY/ZIELVERTRAEGE/REGISTER.md`
- Warum/Änderungen → `protocol/PROJECT_MEMORY/AENDERUNGSREGISTER.md`
- technische Release-Autorität → Branch `affiliate-release-current` → `control/release-governance/CURRENT_RELEASE.json`
- kanonische Source → `release/affiliate-zentrale/current/affiliate-portal-router/`

## AKTUELLER AUFTRAG

Explizite Nutzerentscheidung 11.09.2026:

**ADCELL vollautomatisch über API v2 integrieren. Kein manueller Import/Export als Normalbetrieb. Vor Pluginabnahme harte lokale Positiv-/Negativ-/Gesamtworkflow-Prüfung.**

Digistore24 bleibt nicht erledigt, BLOCKED und zurückgestellt. Detailwahrheit ausschließlich `DIGISTORE24_STATUS.md`.

OTTO/Awin ist nicht erledigt; die bisherige FeedScope-Aufgabe ist durch den aktuellen ADCELL-Auftrag pausiert, nicht als PASS/abgelöst erklärt.

## ADCELL – HART BELEGT

Der offizielle API-v2-Authentifizierungsvertrag ist inzwischen autoritativ gebunden:
- API-Basis `https://api.adcell.org/api/v2/`;
- Token über `/user/getToken` mit `userName` + `password`;
- Folgerequests mit Parameter `token`;
- kein belegter Basic-/Bearer-Vertrag für diesen v2-Weg;
- Programme über `/affiliate/program/export`;
- Werbemittel über `getPromotionTypeCsv`, `getPromotionTypeBanner`, `getPromotionTypeDeeplink`.

Zielweg:
`accepted + active Programme -> explizite programId-Allowlist -> CSV/Banner/Deeplink automatisch -> bestehende zentrale Relevanz-/Creative-/Output-/Veto-Logik`.

Alte/fachfremde akzeptierte ADCELL-Partnerschaften dürfen ohne explizite `programId`-Freigabe nicht eingelesen werden.

## AKTUELLE FEHLERLAGE

Keine zweite Fehlerliste hier. Detailautorität:
Branch `affiliate-release-current` → `AFFILIATE_HOBBYRAUM/FEHLERMATRIX.md`.

Aktuell für diesen ADCELL-Weg relevant:
- AF-023: kanonische Source wurde geändert, Source-Manifest/Governance-Bindung wurde noch nicht atomar nachgezogen;
- AF-058: ADCELL-Automatisierung ist noch nicht vollständig provider-spezifisch vom Awin-Pfad getrennt;
- AF-059: Automationskern enthält noch den manuellen `csv-feed`-/CSV-URL-Normalweg;
- AF-060: fehlender Auth-Beleg ist fachlich geschlossen; die Gegenregel bleibt historisch erhalten;
- AF-062: kanonische Provider-Registry ruft weiterhin den Legacy-Verbindungstest auf, der im Router Basic Auth sendet.

## TECHNISCHER ISTSTAND

Technische Release-Autorität:
- Branch `affiliate-release-current`;
- Kandidatenversion im Plugin weiterhin `6.72.8`;
- Release weiterhin **NICHT freigegeben**.

Im Source-Commit `9815caaa24a6d2587da8890fb24773b2e67e76d8` wurde `trait-ppar-network-sync.php` partiell auf den offiziellen ADCELL-v2-Token-/Allowlist-Weg umgestellt.

Noch nicht fertig:
- Provider-Registry hängt noch am Legacy-`test_adcell_connection()`;
- Automationssuite hängt noch am alten `csv-feed`-Pfad und manuellen ADCELL-CSV-Button;
- Banner-/Deeplink-/CSV-Automation ist noch nicht als vollständiger kanonischer Laufweg abgenommen.

### SOURCE-MANIFEST-BLOCKER

`CURRENT_RELEASE.json` und `release/affiliate-zentrale/CURRENT_SOURCE_SHA256.txt` binden weiterhin den Stand vor der Sourceänderung; der in Governance geführte Manifest-Hash ist weiterhin:
`816f49dc5178e32ead1ea7fd53f0962acb3f457b08a0139f6b9ff1f9239a0a8d`.

Da `trait-ppar-network-sync.php` danach geändert wurde, ist AF-023 offen. **Kein Release-Source-/Tree-PASS darf behauptet werden.**

## TATSÄCHLICH AUSGEFÜHRT IN DIESEM CHAT

Dauerhaft auf `affiliate-release-current` gebunden:
- offizieller ADCELL-v2-Auth-Beleg;
- zusätzlicher offizieller Endpoint-/Feldbeleg;
- aktueller ADCELL-Scope/Testvertrag;
- Hobbyraum-Testdatei für AF-058/059/060/062;
- partieller kanonischer Network-Sync-Sourcefix;
- AF-062 in der autoritativen Fehlermatrix;
- Abschluss-/Nachholbefund im technischen ADCELL-Scope.

Nicht als PASS gewertet:
- kein vollständiger kanonischer Hobbyraumlauf;
- kein aktueller Positiv-/Negativ-Runtime-Test;
- kein Awin/OTTO-/Pause-/Veto-Gesamtworkflow nach ADCELL-Sourceänderung;
- kein erfolgreicher Release-Source-/Tree-Guard nach der Sourceänderung;
- kein Fresh-Unpack / keine Source-ZIP-Identity / keine Test-ZIP;
- kein echter ADCELL-Live-API-/WordPress-/MariaDB-E2E.

## LIVE-BLOCKER

Der Nutzerzugang zu ADCELL ist weiterhin nicht wiederhergestellt; deshalb ist ein echter Live-API-/WordPress-E2E aktuell nicht möglich.

Das blockiert **nicht** die lokale kanonische Reparatur, aber jeden Live-PASS.

## PARALLELWEG

Side-Branch `hobbyroom/adcell-api-v2-automation-20260911` ist keine Arbeitsautorität. Er steht weiterhin auf `cb563f914690cea473db6e02177544f61bd0f2d8` und ist gegenüber `affiliate-release-current` veraltet. Keine dortige Statuswahrheit zurückschreiben.

## NEXT ACTION

Exakt aus `HOBBYRAUM.md` arbeiten:

1. **zuerst AF-023 schließen:** aktuellen kanonischen 26-Dateien-Sourcebaum neu hashen; `CURRENT_SOURCE_SHA256.txt` und Governance-Bindung atomar auf denselben Iststand setzen; danach Release-Governance-/Source-Guard real ausführen;
2. erst dann AF-062 reparieren: Provider-Registry auf `adcell_api_v2_test_connection()` umstellen und Legacy-Basic-Auth aus dem ADCELL-v2-Runtimeweg entfernen;
3. danach AF-058/059 im kanonischen Automationskern fertigstellen;
4. gebundene Positiv-/Negativ-/Gesamtworkflow-/Fresh-Unpack-/Identity-Prüfung;
5. erst danach Test-Plugin; Live-PASS erst nach wiederhergestelltem ADCELL-Zugang.
