# HD-001 – KATEGORIE-WORKFLOW – CURRENT

STAND: 2026-10-05
STATUS: V1.9.4 INSTALLIERT / NICHT FRONTEND-PUBLISHED ABGENOMMEN / V1.9.6 LOKAL HARD PASS

## Ausgangslage

V1.9.4 ist der installierte Produktionsstand.

Bisher bewiesen:
- DataForSEO live angebunden;
- Buchbinden Research PASS;
- WordPress-Write + technischer Readback PASS.

Nicht bewiesen:
- veröffentlichte Frontend-Struktur;
- sichtbare Navigation.

Der frühere Begriff „Deployment abgeschlossen“ darf deshalb nicht als „veröffentlicht“ gelesen werden.

## V1.9.6 Kandidat

Gleiche Pluginlinie, kein Zusatzplugin.

### Publish
- WordPress-Seiten Zielstatus `publish`;
- Draft→Publish kontrolliert migrierbar;
- Status Bestandteil von Preflight/Fingerprint/Readback;
- Statusabweichung fail-closed + Rollback.

### Keine Freigabeschleifen
- fachliche/technische Gates bleiben;
- signierte Receipts werden im Normalweg automatisch nach Hard-PASS erzeugt;
- keine zusätzliche Benutzer-Review-Schleife.

### Inkrementelle Erweiterung
Contract:
`APKW_INCREMENTAL_CATEGORY_EXTENSION_V1`

Regeln:
- Sparse Extension enthält nur neue/geänderte Knoten;
- Merge immer gegen produktive Baseline;
- bestehende nicht genannte Knoten bleiben erhalten;
- kein automatisches Delete/Retirement;
- project_id muss passen;
- optionaler Baseline-Hash muss passen;
- Parent muss in Baseline oder Extension existieren;
- vollständiger gemergter Baum durchläuft danach die bestehenden Validator-/Research-/Deployment-Gates;
- Writer schreibt am Ende nur CREATE/UPDATE/ADOPT/UNCHANGED-Deltas.

### Realer Buchbinden-Merge-Test

Echte Preview-Baseline:
7 Knoten.

Test-Extension:
1 synthetischer neuer Kindknoten.

Ergebnis:
- 7 UNCHANGED;
- 1 ADDED;
- 0 RETIRED;
- automatic_delete=false;
- PASS.

## Tests

- 263/263 PASS;
- Fresh Source 263/263 PASS;
- Runtime-Parität 23/23 PASS;
- Installer PHP 17/17 PASS.

Installer:
`AFFILIATE_PORTAL_KATEGORIE_WORKFLOW_V1.9.6_INCREMENTAL_EXTENSION_DIRECT_PUBLISH_HARD_PASS.zip`

Installer SHA-256:
`22d63c37ef61b42452751d40bb3fee11b7048241fb94e0706b76e5b5c8df8dc8`

Source:
`QUELLCODE_KATEGORIE_WORKFLOW_V1.9.6_INCREMENTAL_EXTENSION_DIRECT_PUBLISH_HARD_PASS.zip`

Source SHA-256:
`59d39226f2ef2f3ebaf97fb3802348677368e7ed07c48f9eacfeb20b16c3bfc8`

## Beleggrenze

V1.9.6 ist noch nicht live installiert.
Keine Behauptung von Publish/Frontend-PASS vor realem WordPress-Readback.

## NEXT ACTION

V1.9.6 installieren → Kategorien → **„Bestehenden Stand jetzt veröffentlichen“** → Readback prüfen.
