# AFFILIATE-ZENTRALE — EXAKTER LIVEKANDIDAT-BUILD

Stand: 2026-09-02
Workstream: `AFFILIATE_ZENTRALE`
Branch: `affiliate-release-current`
Status: `BOUND_EXECUTION_TASK`

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

- Commit vor Bindung dieses Tasks: `3823363cce198fedd2e49591a9f9f2c103c9a9ba`
- Source-Root: `release/affiliate-zentrale/current/affiliate-portal-router/`
- Manifest: `release/affiliate-zentrale/CURRENT_SOURCE_SHA256.txt`
- Manifest-SHA-256: `109879a3c355dff075db4d0ccfe81e7396ed571e5c180019f85d907d56d55f77`
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

1. Auf `affiliate-release-current` ausführen:

   `python3 control/release-governance/release_guard.py governance-check`

2. Danach:

   `python3 control/release-governance/release_guard.py start --branch affiliate-release-current`

3. Manifest-SHA-256 selbst berechnen und exakt gegen
   `109879a3c355dff075db4d0ccfe81e7396ed571e5c180019f85d907d56d55f77`
   prüfen.

4. Alle 26 Manifestzeilen gegen den direkt committed Source-Tree prüfen:
   - exakt dieselbe Dateiliste;
   - keine zusätzliche Datei;
   - keine fehlende Datei;
   - SHA-256 jeder Datei exakt wie im Manifest.

5. Erst danach einen **temporären Livekandidaten** erzeugen. Die ZIP muss als Root exakt `affiliate-portal-router/` enthalten. Dateiinhalte dürfen beim Verpacken nicht verändert werden.

   Empfohlene deterministische Buildlogik: Manifest einlesen und ausschließlich die dort gelisteten Dateien in eine neue ZIP schreiben. Keine Cache-, Git-, Evidence-, Protocol- oder versteckte Datei aufnehmen.

   Ausgabename:
   `affiliate-zentrale_v6.64.0_LIVE_CANDIDATE_26FILE.zip`

6. ZIP sofort in einen frischen temporären Ordner entpacken und erneut prüfen:
   - exakt 26 Dateien;
   - Pfade exakt wie Manifest;
   - SHA-256 jeder entpackten Datei exakt wie Manifest.

7. SHA-256 der erzeugten ZIP berechnen.

8. Ergebnis als **downloadbares Arbeitsartefakt** der Ausführung bereitstellen. Nicht unter `release/affiliate-zentrale/artifacts/final/` committen.

## Erwartete Endausgabe

Nur diese Fakten ausgeben:

- `GOVERNANCE_CHECK: PASS/FAIL`
- `START_CHECK: PASS/FAIL`
- `SOURCE_MANIFEST_SHA256: ...`
- `SOURCE_FILE_COUNT: 26`
- `SOURCE_BYTE_IDENTITY: PASS/FAIL`
- `FRESH_UNPACK_FILE_COUNT: 26`
- `FRESH_UNPACK_BYTE_IDENTITY: PASS/FAIL`
- `LIVE_CANDIDATE_ZIP_SHA256: ...`
- Pfad/Download des erzeugten `affiliate-zentrale_v6.64.0_LIVE_CANDIDATE_26FILE.zip`

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
