# HD-007 – EVIDENCE 1.1.1 HOBBYREGISTER KORREKTUR

STAND: 2026-10-23
STATUS: LOCAL HARD PASS / LIVE OFFEN

Artefakt:
`HOBBY_DEPOT_HOBBYREGISTER_CORE_HD007_V1.1.1_FULL_KORREKTUR.zip`

SHA-256:
`f963a0c07a4e5f9275992db8eea82f92721a4c12b62a3a7f0e78ed9b7a094d7c`

Größe:
933,489 Bytes.

## Behobene Beanstandungen

- Gruppen auf der Register-Startseite sind keine großen Kacheln mehr, sondern – nach dem bewährten Pferderassen-Prinzip – reine Icon-Navigation mit runden Iconflächen und Beschriftung.
- Breadcrumb besitzt keinen künstlichen 38px-Mindestblock mehr und folgt der Hobby-Depot-Standardgeometrie: 12px Schrift / 1.4 line-height / 18px oberer und 15px unterer Abstand.
- Der 4-Zeilen-Kurzprofil-Fallback wurde vollständig entfernt.
- Alle 862 Detailprofile erzeugen acht Schema-F-Fließtextabschnitte.
- Die linke Faktenleiste ist deutlich größer, cremefarben hinterlegt, mit petrolfarbener Oberkante und eigenen kleinen SVG-Icons.
- „Ähnliche Hobbys“ wird nicht mehr doppelt in Sidebar und Seitenende ausgegeben; Sidebar: gleiche Hobbygruppe, unten: ähnliche Hobbys einmal.

## Textaufbau für alle Profile

1. Worum geht es?
2. Passt das Hobby zu dir?
3. Wo und wann?
4. Platz, Alltag und Pflege
5. Kosten und Ausrüstung
6. Was musst du können?
7. Was entsteht daraus?
8. Grenzen, Sicherheit und Regeln

Die bestehenden Kurzprofilfelder und 54 gebundenen Basistraits werden in natürliche Fließtexte übersetzt.
Buchbinden und Slacklining behalten ihre redaktionell ausformulierten Mustertexte.
Die drei Schema-1.2-Zusatztraits werden nur dort ausgegeben, wo sie in der aktuellen HD-007-Laufzeitprojektion bereits explizit gebunden sind; keine Werte werden geraten.

## QA

- Core-ready: 862/862 PASS.
- 862/862 Profile: genau acht nichtleere Textabschnitte PASS.
- kürzester generierter Text: 486 Wörter.
- repräsentative Vollrenders: Buchbinden, Slacklining, Geocaching, Aquaristik, Münzen, 3D-Druck PASS.
- keine Compact-4-Line-Fallback-Ausgabe mehr.
- 8 Gruppen-Icons PASS.
- Registerseite weiterhin 16 Hobbykarten + Pagination.
- Sidebar-Faktenicons PASS.
- „Ähnliche Hobbys“ pro Detailseite nur einmal PASS.
- PHP-Lint / Fresh-Unpack PASS.
- keine DB-Writes / Cron / Netzwerkänderung.

Kein Live-PASS behaupten.
