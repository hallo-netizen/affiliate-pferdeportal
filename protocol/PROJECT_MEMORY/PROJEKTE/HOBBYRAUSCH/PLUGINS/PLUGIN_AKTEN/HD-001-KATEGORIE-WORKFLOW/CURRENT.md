# HD-001 – KATEGORIE-WORKFLOW – CURRENT

STAND: 2026-09-28
STATUS: V1.8.6 HOBBY-DEPOT-SIMPLE ROOTFIX GEBAUT / LIVE-BLOCKER BEHOBEN

## Aktueller Stand

Plugin:
`Affiliate-Portal Kategorie-Workflow V1.8.6 Hobby Depot Simple Rootfix`

Installer:
`AFFILIATE_PORTAL_KATEGORIE_WORKFLOW_V1.8.6_HOBBY_DEPOT_SIMPLE_ROOTFIX.zip`

Installer SHA-256:
`2854f41f060a4f13abc2721ae76c74f8cf8689e4e7224592060b24b79929ab15`

Source:
`QUELLCODE_KATEGORIE_WORKFLOW_V1.8.6_HOBBY_DEPOT_SIMPLE_ROOTFIX.zip`

Source SHA-256:
`a73e28307fde3ad42a4a18a79bd6ff627065494bf8f4921b92065e5aa048ddc9`

## Live-Befund V1.8.5

Nach erfolgreicher kostenloser Konzept-Vorprüfung und gesetzter DataForSEO-Bestätigung blockierte der Klick auf `SEO-Erstentwurf erzeugen` mit:

`Ausdrückliche sichtbare Nutzerfreigabe fehlt.`

## Rootcause

`build_concept_draft()` rief fälschlich `require_review_actor()` auf.
Diese Prüfung gehört ausschließlich zu den separaten sichtbaren Human-Review-Signaturen und verlangt Felder, die der Konzeptstart absichtlich nicht sendet.

## Fix V1.8.6

Der Konzeptstart prüft jetzt exakt:
- Administratorrecht;
- eigenen Nonce;
- ausdrückliche `apkw_concept_paid_confirmation=1`.

Die späteren sichtbaren Initial-/Global-/Final-Review-Gates bleiben unverändert verpflichtend.

Keine Research-, Qualitäts-, Deployment- oder Sicherheitsfunktion wurde entfernt.

## Tests

- Source Vollsuite: 227/227 PASS;
- Fresh-Unpack-Installer mit identischem Test-Runner: 227/227 PASS;
- Source PHP-Lint: 17/17 PASS;
- Installer Runtime PHP-Lint: 16/16 PASS;
- Runtime-Parität Source↔Installer: 21/21 Dateien byteidentisch.

## Testinput

`HOBBY_DEPOT_TESTLABOR_KATEGORIE_KONZEPT_20260928.json`

## NEXT ACTION

V1.8.6 über V1.8.5 installieren. Danach Testlabor-Konzept erneut kostenlos vorprüfen, Paid-Calls bestätigen und `SEO-Erstentwurf erzeugen` erneut ausführen.
