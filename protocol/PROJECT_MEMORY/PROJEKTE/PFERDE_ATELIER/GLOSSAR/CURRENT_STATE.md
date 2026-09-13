# BÜRO GLOSSAR – CURRENT_STATE

STAND: 2026-09-13
STATUS: 0.2.8 LIVE FAIL / 0.2.10-rc7 TECHNISCHER HARDTEST + PAKET/ARTEFAKT PASS / PFERDE-LIVE OFFEN

## Belastbarer aktueller Stand

- Büro `GLOSSAR` steuert das öffentliche Pferde-Atelier-Glossar.
- Fachwahrheit bleibt in `../WISSENSDATENBANK/AKTENSCHRAENKE/GLOSSAR/`.
- Vorhandene WordPress-Seite `Glossar` bleibt Hauptseite.
- Das bestehende Pferde-Designplugin und `main` bleiben unangetastet.
- Aktueller Arbeitsbranch: `hobbyroom/glossar-livefail-red-green-20260913`.

## Letzter real widerlegter Stand

0.2.8 bleibt **LIVE FAIL / BLOCKED / NICHT VERWENDEN**. Nutzer-Readback:
1. Hero/Bild real nicht responsive;
2. Kategorien nicht wie die Glossar-Startseite gestaltet;
3. Einzelartikel-Links laufen ins Leere.

0.2.6/0.2.7 bleiben historische Zwischen-/Fehlstände und werden nicht mehr ausgegeben.

## Letzter früherer paketierter Kandidat

0.2.9 war ein gated, technisch geprüfter Kandidat, wurde aber durch die aktive 0.2.10-Entwicklung abgelöst. Ein Pferde-LIVE-PASS für 0.2.9 wurde nicht festgestellt.

## Aktueller technischer Kandidat 0.2.10-rc7

Version: `0.2.10-rc7`
Rewrite-Schema: `7`
Exakt getesteter Quell-Commit: `1e74b7454e84f97182dbb185614371a48157bc21`
Workflow: `.github/workflows/glossar-0210-rc7-hardtest.yml`
Run: `34762048546` → SUCCESS

Jobs:
- Build `103736483729` → SUCCESS
- Fresh inkl. Positiv-/Negativ-/Regressionstests `103736483608` → SUCCESS
- Real Design 1.50.469 + echter Browserklick + Loop-Poison `103736483696` → SUCCESS
- no-package-gate `103736720142` → SUCCESS

## Klickbarkeitsbeweis

Unter dem rekonstruierten echten Design-Hauptcode 1.50.469, SHA-256 `580fa6c7f5566f29df9254ce92f687a4831554e1d84bf03fbd936bb7577edfe5`, wurde im Browser tatsächlich geklickt:
1. Kategorie → vorhandener `Hufbein`-Link → echte Einzelansicht mit H1 und Sentinel-Inhalt;
2. Kategorie → `Hufrehe`;
3. `Hufrehe` → `Strahlfäule` über sichtbaren `Verwandte Begriffe`-Link;
4. `Strahlfäule` → `Hufabszess`;
5. `Hufabszess` → sichtbarer Kategorienlink → zurück zu `Gesundheit`.

Belege Job `103736483696`:
- `UGE0210_EXISTING_SINGLE_CLICK_PASS`
- `UGE0210_NEW_CLUSTER_CLICK_CHAIN_PASS`
- `UGE0210_SINGLE_SURVIVES_EMPTY_MAIN_LOOP_PASS`
- `UGE0210_PFERDE_BREADCRUMB_AXIS_PASS`
- `UGE0210RC7_REAL_DESIGN_CLICKABILITY_BREADCRUMB_LOOP_POISON_PASS`

Damit ist die **technische Klickbarkeits-Freigabeschranke** erbracht. Das ist kein Pferde-LIVE-Readback und keine automatische Löschfreigabe; der Nutzer entscheidet über den Altbestand nach eigener realer Prüfung.

## Cluster-Produktion / RC6 → RC7

Der neue Testcluster enthält `Hufrehe`, `Strahlfäule`, `Hufabszess` mit echten verwandten Links und Kategorieverweisen. Pferderassen bleiben ausgeschlossen; kurze Beiträge erhalten keine erzwungenen H2/H3.

RC6 scheiterte an der Veröffentlichung, weil die bestehende UGE-Publikationspolicy eine gültige primäre Portal-Kategorie verlangt und die Bindung fehlte. RC7 prüft vor der Publikation die reale Portal-Kategorie `Gesundheit` und setzt `primary_category_id`; die Policy wird nicht umgangen.

## Paket-/Artefaktstatus – nachgeholt

Der ursprüngliche rc7-Hardtest erzeugte absichtlich noch kein Paket. In der Abschlussprüfung wurde deshalb **aus exakt dem getesteten Quell-Commit `1e74b7454e84f97182dbb185614371a48157bc21`** neu gebaut und paketiert.

Closeout-Run: `34764046870` / Job `103741741909` → SUCCESS.

Installierbares Paket:
`universal-glossary-engine-0.2.10-rc7.zip`

Innerer Plugin-ZIP SHA-256:
`3611229aa33ca50a00ec88be87e6ef92592e87d313c152f05d0c7a31ab281152`

Actions-Artefakt:
- ID `10319439428`
- Outer artifact SHA-256 `cbf72dc81229adf33febca085c43d70a12188880cd62c7aafd3f687cb62f2bab`

Paketprüfungen:
- `unzip -t` PASS;
- Source-vs-Unpack `diff -qr` PASS;
- Version `0.2.10-rc7` PASS;
- PHP-Lint auf Source und entpacktem Paket PASS;
- SHA-256 PASS;
- Paket aus exakt getestetem Commit gebaut: `RC7_EXACT_TESTED_SOURCE_PACKAGE_PASS`;
- Synchronisierung ins PLUGINS-Büro: `GLOSSAR_RC7_ARTIFACT_SYNC_PASS`.

Isolierte Ausgabekopie:
`../PLUGINS/ISOLIERTE_PLUGINS/MOD-008/CURRENT.zip`
mit `MANIFEST.md`.

## Offene Grenzen

- Kein Pferde-LIVE-PASS für 0.2.10-rc7.
- Die bekannten realen Live-Fehler bleiben bis zum realen Nutzer-Readback offen.
- Der Nutzer entscheidet über das Löschen des Altbestands erst nach eigener realer Prüfung.

## PASS-Grenze

**0.2.10-rc7 technische Hardtests: PASS.**

**Paket-/Artefaktsynchronisierung: PASS.**

**Pferde-LIVE-PASS: NEIN / OFFEN.**
