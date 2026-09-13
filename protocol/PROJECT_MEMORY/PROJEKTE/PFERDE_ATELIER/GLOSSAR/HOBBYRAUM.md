# GLOSSAR – HOBBYRAUM

STAND: 2026-09-13
STATUS: AKTIV / 0.2.10-rc7 TECHNISCH HARDTEST PASS / PAKET BLOCKED / LIVE OFFEN

## 1-KLICK-ÜBERSICHT

**WAS IST DAS?**  
Der einzige aktuelle Arbeitsraum des Büros GLOSSAR.

**DU DARFST …**  
auf dem gebundenen Branch ausschließlich vom frisch geprüften 0.2.10-rc7-Stand weiterarbeiten, zuerst die Paket-/Pluginbüro-Pflichten schließen und erst danach eine neue reale Pferde-Übergabe erzeugen.

**DU DARFST NICHT …**  
`main` verändern, 0.2.6/0.2.7/0.2.8 erneut ausgeben, 0.2.9 als aktuellen Entwicklungsstand behandeln, unterschiedliche Paketbytes unter derselben Version erzeugen, aus CI einen Pferde-LIVE-PASS ableiten oder den Altbestand automatisch löschen.

**ALS NÄCHSTES …**  
aus dem exakt getesteten rc7-Stand einen regelkonformen gated Releasekandidaten bauen und prüfen; danach `PROJEKTE/PFERDE_ATELIER/PLUGINS/` samt hashgebundenem `CURRENT.zip` + `MANIFEST.md` synchronisieren; erst dann Nutzer-Live-Readback.

## ARBEITSORT

Branch:
`hobbyroom/glossar-livefail-red-green-20260913`

Frisch geprüfter Head vor Closeout-Dokumentation:
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
- 0.2.9: letzter vorhandener gated technischer Kandidat, aber durch aktive 0.2.10-Entwicklung als CURRENT/NEXT ACTION abgelöst; kein bestätigter Pferde-LIVE-PASS.
- 0.2.10-rc1 bis rc6: Entwicklungs-/Diagnosestufen, nicht ausgeben.

## 0.2.10-rc7 TECHNISCHER STAND

Run `34762048546` → SUCCESS.

Jobs:
- Build `103736483729` PASS
- Fresh/Positiv/Negativ/Regression `103736483608` PASS
- echtes Design 1.50.469 + Browser-Klickkette + Loop-Poison `103736483696` PASS
- no-package-gate `103736720142` PASS

Der Browser hat nicht nur URLs geprüft, sondern tatsächlich geklickt:
`Gesundheit → Hufbein`, danach den neuen Cluster `Hufrehe → Strahlfäule → Hufabszess → Gesundheit`.

Marker:
- `UGE0210_EXISTING_SINGLE_CLICK_PASS`
- `UGE0210_NEW_CLUSTER_CLICK_CHAIN_PASS`
- `UGE0210_SINGLE_SURVIVES_EMPTY_MAIN_LOOP_PASS`
- `UGE0210_PFERDE_BREADCRUMB_AXIS_PASS`

Damit ist der technische Klickbarkeitsbeweis erbracht. Die reale Pferde-Seite wurde damit nicht abgenommen.

## AKTUELLER BLOCKER

Der rc7-Hardtest endet ausdrücklich mit:
`UGE0210RC7_HARD_GATES_PASS_NO_PACKAGE`.

Es gibt deshalb noch kein rc7-Installations-ZIP, keinen rc7-ZIP-SHA und keine zulässige `CURRENT.zip`-Synchronisierung.

Zusätzlich war beim Abschlusscheck der vom Nutzer vorgeschriebene Pfad
`PROJEKTE/PFERDE_ATELIER/PLUGINS/`
nicht vorhanden. Solange Paket und Pluginbüro nicht regelkonform hergestellt und geprüft sind, bleibt die Übergabe BLOCKED.

## NÄCHSTE HARTE REIHENFOLGE

1. rc7-Bytes als Basis binden; bei materieller Änderung neue Version verwenden.
2. finalen/gated Kandidaten bauen.
3. ZIP-Lesetest, Struktur, Version und SHA prüfen.
4. erforderliche Positiv-/Negativ-/Regressionstests auf exakt diesen Paketbytes ausführen.
5. erst danach Projekt-PLUGINS-Büro und `ISOLIERTE_PLUGINS/<PLUGIN-ID>/CURRENT.zip` + `MANIFEST.md` synchronisieren.
6. genau einen PU-Vorgang dokumentieren.
7. dann Installations-ZIP an Nutzer geben.
8. Nutzer prüft real; erst nach echtem Live-Readback Fehlerstatus ändern bzw. Altbestand löschen.

## NICHT ANFASSEN

- `main`.
- Pferde-Designplugin.
- vorhandene sechs Live-Glossarbeiträge bis zur Nutzerentscheidung.
- Pferderassen: gehören nicht ins Glossar.
- Zielvertrag V1: unverändert aktiv.
