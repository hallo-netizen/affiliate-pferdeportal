# AFFILIATE-ZENTRALE — EXAKTER LIVEKANDIDAT-BUILD

Stand: 2026-09-03
Workstream: `AFFILIATE_ZENTRALE`
Branch: `affiliate-release-current`
Status: `BOUND_EXECUTION_TASK`

## ARBEITSGLOCKE — ZWINGENDER EINLASS

Dieser Affiliate-Auftrag darf **nicht** über STARTMASTER oder die globale Cloud-Eingangstür navigiert werden.

**VERBOTEN für diesen Auftrag:**

- `python3 control/cloud-entry-gate/cloud_entry.py start`
- `control/output-quarantine/runtime_entry_gate.py`
- `control/single-door-boundary/codex_current_action.py`
- jede Navigation über `control/startmaster*`, `.pferde-capsule/` oder `.pferde-quarantine/`

Diese Pfade gehören zu anderen Workstreams und dürfen den Affiliate-Auftrag nicht blockieren oder umleiten.

**Einziger technischer Einstieg:**

```bash
python3 protocol/AFFILIATE_RELEASE_WORK_BELL.py current
python3 protocol/AFFILIATE_RELEASE_WORK_BELL.py run
```

Die Glocke validiert selbst Workstream, Branch, Current-Release-Bindung, Manifest, 26 Source-Dateien, Governance/Start-Guard, Source-Byteidentität, ZIP-Build und Fresh-Unpack-Byteidentität. Sie darf nur bei echtem belegtem Mismatch oder nach erzeugtem Livekandidaten für die zwingende WordPress-Nutzerhandlung stoppen.

## Ziel

Aus der **direkt committed kanonischen Quelle** einen temporären, installierbaren WordPress-Livekandidaten bauen, damit anschließend der gebundene WordPress-Live-Readback durchgeführt werden kann.

Dies ist **kein finaler Release**. Die ZIP darf nicht als finaler Release unter `release/affiliate-zentrale/artifacts/final/` committed oder als Release-PASS gewertet werden, bevor die Live-Gates geschlossen sind.

## Verbindliche Autorität

Vor Ausführung zwingend lesen:

1. `control/release-governance/CURRENT_RELEASE.json`
2. `protocol/AFFILIATE_RELEASE_ERROR_REGISTER.md`
3. `protocol/AFFILIATE_RELEASE_ERROR_REGISTER_CURRENT_SCOPE_AMENDMENT_20260902.md`
4. `protocol/AFFILIATE_RELEASE_CURRENT_USER_SCOPE_LOCK_20260902.md`
5. `release/affiliate-zentrale/AGENTS.md`

Aktuell gebundener Source-Stand:

- Source-Root: `release/affiliate-zentrale/current/affiliate-portal-router/`
- Manifest: `release/affiliate-zentrale/CURRENT_SOURCE_SHA256.txt`
- Manifest-SHA-256: `5a7409487432b460921312380b975e40328615298bdbc5f5485e13ed507d933c`
- Source-Dateien: exakt `26`
- Kandidat: `6.64.0`

Vor dem Build erneut prüfen, dass `CURRENT_RELEASE.json` weiterhin exakt diesen Manifest-SHA und 26 Dateien bindet. Wenn nicht: **FAIL_CLOSED**, nichts rekonstruieren.

## Current-Scope-Vorrang

Für diesen Auftrag gilt ausdrücklich AFF-ERR-017 / Current-Scope-Amendment:

- manueller Ein-Feld-Bulkimport ist autorisiert;
- automatische Digistore24-Partnerschafts-Discovery ist OUT OF SCOPE / NON-BLOCKING;
- keine erneute Partnerlisten-Abfrage;
- keine erneute Anforderung derselben DS24-CSV;
- keine Browser-/Network-Screenshot-Anforderung;
- keine historische 6.71-ZIP als Voraussetzung;
- kein Rücksprung in alte Discovery-/Rekonstruktionswege.

## Erlaubter Arbeitsumfang

**Nur Build + Verifikation des vorhandenen Source-Trees.**

VERBOTEN:

- keine PHP-/JS-/CSS-/JSON-/Readme-Source ändern;
- keine Version hochsetzen;
- keine neue Architektur;
- keine `.github/workflows/` ändern;
- keine alten ZIPs als Source verwenden;
- keine Base64-/GZIP-/Patch-/Historien-Rekonstruktion;
- keine Final-Release-ZIP committen;
- keine bestehenden PASS-Gates vorsorglich wiederholen;
- keine Release-/Live-PASS-Behauptung ohne echte Evidence.

## Exakte Ausführung

Die Ausführung erfolgt ausschließlich durch die Arbeitsglocke:

```bash
python3 protocol/AFFILIATE_RELEASE_WORK_BELL.py run
```

Die Glocke führt gebunden aus:

1. `release_guard.py governance-check`
2. `release_guard.py start --branch affiliate-release-current`
3. Manifest-SHA exakt gegen `5a7409487432b460921312380b975e40328615298bdbc5f5485e13ed507d933c`
4. exakt 26 Manifestdateien und jeden Datei-SHA gegen den direkt committed Source-Tree
5. deterministischen temporären Livekandidaten `affiliate-zentrale_v6.64.2_LIVE_CANDIDATE_26FILE.zip`
6. Fresh-Unpack und erneute exakte 26-Dateien-/SHA-Prüfung
7. ZIP-SHA-256
8. Status `USER_ACTION_REQUIRED` erst für die echte WordPress-Installation

Bei irgendeinem Mismatch: **keine ZIP zur Installation freigeben**, erster belegter Fehler + tatsächlicher Hash/Pfad, dann STOP FAIL_CLOSED.

## Danach gebundener Live-Schritt

Erst mit byteidentischem Livekandidaten:

`WordPress-Dashboard -> Plugins -> Installieren -> Plugin hochladen`

Danach:

`WordPress-Dashboard -> Affiliate-Zentrale -> Anbieter & APIs -> Datei importieren`

mit der bereits autorisierten aktuellen Digistore24-CSV.

Live muss anschließend mindestens belegen:

- Plugin lädt ohne Fatal Error;
- KISS-Navigation bleibt erreichbar, kein `remove_submenu_page()`-Regressionsfehler;
- genau ein Uploadfeld;
- DS24-Datei wird eindeutig erkannt;
- 18 genehmigte Partnerschaften werden synchronisiert;
- 10 Werbemittelquellen/Vendoren werden dem bestehenden DS24-Downstream übergeben;
- Fehler eines Vendors blockiert die übrigen nicht;
- Partner-&-Einnahmen delegiert weiterhin an die zentrale Analytics;
- eBay/idealo/Awin/ADCELL bleiben regressionsfrei;
- echter WordPress-Readback wird dokumentiert.

Erst danach dürfen die noch offenen Live-/Installer-/Final-Gates im gebundenen Releaseprozess geschlossen und die **finale** Release-ZIP erzeugt werden.
