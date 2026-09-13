# UNIVERSAL GLOSSAR ENGINE – HOBBYRAUM

STAND: 2026-09-13
STATUS: NEUTRALER CORE 0.2.9 GEBUNDEN / PFERDE-0.2.10-rc7 NICHT ALS UNIVERSAL-CORE FREIGEGEBEN

## 1-KLICK-ÜBERSICHT

**WAS IST DAS?**  
Der isolierte Arbeitsraum für den allgemeinen Glossar-Core.

**DU DARFST …**  
den neutralen Core und seine gebundenen Positiv-/Negativtests pflegen sowie eine saubere konfigurierbare Grenze für projektspezifische Content-Packs entwickeln und prüfen.

**DU DARFST NICHT …**  
Pferde-Fachlogik als allgemeinen Core ausgeben, `main` verändern, 0.2.6/0.2.7/0.2.8 erneut ausgeben, unterschiedliche Paketbytes unter derselben Version erzeugen oder einen Pferde-Projekt-PASS als Allgemeingültigkeitsbeweis behandeln.

**ALS NÄCHSTES …**  
wenn am allgemeinen Modul weitergearbeitet wird: die Adapter-/Projektkonfigurationsgrenze für Content-Packs explizit trennen und mit einer zweiten Projektkonfiguration beweisen. Die aktuelle Pferde-Live-Abnahme läuft ausschließlich im Projektbüro.

## GEBUNDENER NEUTRALER KERN

Letzter allgemeiner Kandidat:
`0.2.9`

Rewrite-Schema:
`7`

Branch:
`hobbyroom/glossar-livefail-red-green-20260913`

Getesteter neutraler Head:
`f2fa6f0c248acfa6978b5faec5daf42a40d0ba3b`

Run:
`34757795593`

PASS:
- Build `103725094481`
- Fresh/Regression/Null-Rewrite `103725094537`
- 0.2.8 → 0.2.9/erneuter Null-Rewrite `103725094620`
- Real Design 1.50.469/Browser/Null-Rewrite `103725094378`
- gated package `103725295224`

## PFERDE-PROJEKTLINIE

Die Projektlinie `0.2.10-rc7` ist technisch im Pferde-Fachbüro geprüft und paketiert, enthält aber ausdrücklich projektspezifische Content-Pack-Logik (`class-uge-pferde-content-pack.php`).

Sie ist deshalb **keine automatische neue Universal-Core-Version**.

Aktueller Projekt-/Paket-/LIVE-Status:
`PROJEKTE/PFERDE_ATELIER/GLOSSAR/CURRENT_STATE.md`

## HARTE GRENZE

- Neutraler Core und projektspezifische Content-Packs dürfen nicht zu einer zweiten unklaren Modulwahrheit verschmelzen.
- Allgemeingültigkeit erst nach neutraler Adaptergrenze + zweiter Projektkonfiguration.
- Pferde-LIVE-PASS ausschließlich durch realen Nutzer-Readback im Pferde-Fachbüro.
