# BÜRO GLOSSAR – CURRENT_STATE

STAND: 2026-09-13
STATUS: 0.2.8 LIVE FAIL / 0.2.10-rc7 TECHNISCHER HARDTEST PASS / KEIN PAKET / PFERDE-LIVE OFFEN

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

## Letzter paketierter technischer Kandidat

0.2.9 war ein gated, technisch geprüfter Kandidat. Er wurde jedoch in diesem Chat durch die aktive 0.2.10-Entwicklung abgelöst und ist **nicht mehr CURRENT/NEXT ACTION**. Ein Pferde-LIVE-PASS für 0.2.9 wurde nicht festgestellt.

## Aktueller technischer Kandidat 0.2.10-rc7

Version: `0.2.10-rc7`
Rewrite-Schema: `7`
Getesteter Head: `1e74b7454e84f97182dbb185614371a48157bc21`
Workflow: `.github/workflows/glossar-0210-rc7-hardtest.yml`
Run: `34762048546` → SUCCESS

Jobs:
- Build `103736483729` → SUCCESS
- Fresh inkl. bestehender Positiv-/Negativ-/Regressionstests `103736483608` → SUCCESS
- Real Design 1.50.469 + echter Browserklick + Loop-Poison `103736483696` → SUCCESS
- `no-package-gate` `103736720142` → SUCCESS

**Wichtig:** Der Workflow endet absichtlich mit `UGE0210RC7_HARD_GATES_PASS_NO_PACKAGE`. Für rc7 existiert noch kein gated Übergabe-ZIP und daher kein rc7-Paket-SHA.

## Neu technisch bewiesen

### Klickbarkeit bestehender und neuer Glossarbegriffe
Unter dem rekonstruierten echten Design-Hauptcode 1.50.469 (SHA-256 `580fa6c7f5566f29df9254ce92f687a4831554e1d84bf03fbd936bb7577edfe5`) wurde im echten Browser geklickt:
1. Kategorie → vorhandener `Hufbein`-Link → echte Einzelansicht mit H1 und Sentinel-Inhalt;
2. Kategorie → `Hufrehe`;
3. `Hufrehe` → sichtbarer Link unter `Verwandte Begriffe` → `Strahlfäule`;
4. `Strahlfäule` → sichtbarer Link → `Hufabszess`;
5. `Hufabszess` → sichtbarer Kategorienlink → zurück zu `Gesundheit`.

Belege im Job `103736483696`:
- `UGE0210_EXISTING_SINGLE_CLICK_PASS`
- `UGE0210_NEW_CLUSTER_CLICK_CHAIN_PASS`
- `UGE0210_SINGLE_SURVIVES_EMPTY_MAIN_LOOP_PASS`
- `UGE0210_PFERDE_BREADCRUMB_AXIS_PASS`
- `UGE0210RC7_REAL_DESIGN_CLICKABILITY_BREADCRUMB_LOOP_POISON_PASS`

Damit ist die **technische Klickbarkeits-Freigabeschranke** aus `BEGRIFFSREGISTER.md` im Testsystem erbracht. Das ist ausdrücklich **kein Pferde-LIVE-Readback** und keine automatische Löschfreigabe; der Nutzer entscheidet über den Altbestand erst nach eigener Prüfung.

### Cluster-Produktion
Die neue Pferde-Clusterproduktion erzeugt `Hufrehe`, `Strahlfäule` und `Hufabszess` als zusammenhängenden Satz. Verwandte Begriffe werden als echte Links ausgegeben; Pferderassen bleiben ausgeschlossen; kurze Beiträge erhalten keine erzwungenen Zwischenüberschriften.

### Gefundener RC6-Fehler und RC7-Reparatur
RC6 erzeugte die drei Pack-Begriffe als eigene Entwürfe, scheiterte aber an der Veröffentlichung, weil die bestehende UGE-Publikationspolicy eine gültige primäre Portal-Kategorie verlangt und diese Bindung fehlte.

RC7 stellt vor Erzeugung/Publikation die reale Portal-Kategorie `Gesundheit` fest und setzt `primary_category_id`. Die normale Publikationspolicy wird nicht umgangen.

## Offene Grenzen

- Kein rc7-Übergabe-ZIP / kein rc7-Paket-SHA.
- Kein Pferde-LIVE-PASS für 0.2.10-rc7.
- Die bekannten realen Live-Fehler bleiben bis zum realen Nutzer-Readback offen.
- Das vorgeschriebene Projektbüro `PROJEKTE/PFERDE_ATELIER/PLUGINS/` existierte beim Abschlusscheck nicht; der Plugin-Artefaktexport ist deshalb zusätzlich BLOCKED, bis Büro + gated Paket regelkonform vorliegen.

## PASS-Grenze

**0.2.10-rc7 technische Hardtests: PASS.**

**Übergabe-/Paketstatus: BLOCKED.**

**Pferde-LIVE-PASS: NEIN / OFFEN.**
