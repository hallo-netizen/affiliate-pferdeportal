# GLOSSAR – HOBBYRAUM

STAND: 2026-09-13
STATUS: AKTIV / 0.2.10-rc7 TECHNISCH + PAKET PASS / LIVE-READBACK OFFEN

## 1-KLICK-ÜBERSICHT

**WAS IST DAS?**  
Der einzige aktuelle Arbeitsraum des Büros GLOSSAR.

**DU DARFST …**  
den exakt getesteten und hashgebunden paketierten 0.2.10-rc7-Kandidaten für den realen Pferde-Readback verwenden und danach nur anhand des tatsächlichen Live-Ergebnisses weiterarbeiten.

**DU DARFST NICHT …**  
`main` verändern, 0.2.6/0.2.7/0.2.8 erneut ausgeben, 0.2.9 als aktuellen Entwicklungsstand behandeln, unterschiedliche Paketbytes unter derselben Version erzeugen, aus CI einen Pferde-LIVE-PASS ableiten oder den Altbestand automatisch löschen.

**ALS NÄCHSTES …**  
das exakt hashgebundene `0.2.10-rc7`-Paket installieren und den realen Pferde-Live-Readback durchführen. Erst danach Live-Fehler schließen oder den Altbestand löschen.

## ARBEITSORT

Branch:
`hobbyroom/glossar-livefail-red-green-20260913`

Exakt getesteter Plugin-Quell-Commit:
`1e74b7454e84f97182dbb185614371a48157bc21`

Autoritative Fehlerquelle:
`FEHLERQUELLEN.md`

Autoritativer Stand:
`CURRENT_STATE.md`

Produktionswahrheit Begriffe:
`BEGRIFFSREGISTER.md`

## VERBRAUCHTE / ABGELÖSTE VERSIONEN

- 0.2.6: historisch / nicht verwenden.
- 0.2.7: LIVE FAIL / nicht verwenden.
- 0.2.8: LIVE FAIL / nicht verwenden.
- 0.2.9: früherer gated technischer Kandidat; durch 0.2.10-Entwicklung als CURRENT/NEXT ACTION abgelöst; kein bestätigter Pferde-LIVE-PASS.
- 0.2.10-rc1 bis rc6: Entwicklungs-/Diagnosestufen, nicht ausgeben.

## 0.2.10-rc7 TECHNISCHER STAND

Hardtest Run `34762048546` → SUCCESS.

Jobs:
- Build `103736483729` PASS
- Fresh/Positiv/Negativ/Regression `103736483608` PASS
- echtes Design 1.50.469 + Browser-Klickkette + Loop-Poison `103736483696` PASS
- no-package-gate `103736720142` PASS

Der Browser hat tatsächlich geklickt:
`Gesundheit → Hufbein` sowie `Gesundheit → Hufrehe → Strahlfäule → Hufabszess → Gesundheit`.

Marker:
- `UGE0210_EXISTING_SINGLE_CLICK_PASS`
- `UGE0210_NEW_CLUSTER_CLICK_CHAIN_PASS`
- `UGE0210_SINGLE_SURVIVES_EMPTY_MAIN_LOOP_PASS`
- `UGE0210_PFERDE_BREADCRUMB_AXIS_PASS`

## PAKETSTATUS

Closeout Run `34764046870`, Job `103741741909` → SUCCESS.

Installierbares Paket:
`universal-glossary-engine-0.2.10-rc7.zip`

SHA-256:
`3611229aa33ca50a00ec88be87e6ef92592e87d313c152f05d0c7a31ab281152`

Actions-Artefakt-ID:
`10319439428`

Outer artifact SHA-256:
`cbf72dc81229adf33febca085c43d70a12188880cd62c7aafd3f687cb62f2bab`

Paketbeweise:
- aus exakt getestetem Commit gebaut;
- `unzip -t` PASS;
- Source-vs-Unpack `diff -qr` PASS;
- Version PASS;
- PHP-Lint PASS;
- SHA PASS;
- `CURRENT.zip` + `MANIFEST.md` im PLUGINS-Büro synchronisiert.

## NÄCHSTE HARTE REIHENFOLGE

1. exakt dieses hashgebundene Paket verwenden;
2. reale Pferde-Installation/Readback durchführen;
3. bestehenden `Hufbein`-Weg und neue Clusterbegriffe im echten Frontend anklicken;
4. responsive Hero, Kategorie-Vollrahmen, AJAX und obere Abstände real mitprüfen;
5. erst bei realem PASS Fehlerstatus schließen;
6. Altbestand nur nach Nutzerentscheidung löschen;
7. bei materiellem FAIL neue Version bauen und volle Teststrecke wiederholen.

## NICHT ANFASSEN

- `main`.
- Pferde-Designplugin.
- vorhandene Live-Glossarbeiträge bis zur Nutzerentscheidung.
- Pferderassen: gehören nicht ins Glossar.
- Zielvertrag V1: unverändert aktiv.
