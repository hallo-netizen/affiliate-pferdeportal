# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-19
STATUS: **1.50.695 TECHNISCH PASS / REDAKTIONELL NICHT FREIGEGEBEN – WIEDERKEHRENDE SATZBAUSTEINE GEFUNDEN**

Zielvertrag: **ZV-HOBBYRAUSCH-DESIGN-001 Fassung 5.5 / 2026-10-19**

## AKTUELLER BELASTBARER STAND

Direkt am realen 1.50.695-ZIP neu geprüft:
- SHA-256: `8afd735e7cdd918e2daa60c62dbd5a029b168d8b06e6fd566c56fc0758dc6f8a`;
- ZIP-Integrität PASS;
- 395/395 Textdatensätze, Keyset exakt gleich 395er Masterbestand;
- 10/10 Texte aus 1.50.694 exakt erhalten;
- Leads 45–60 Wörter;
- Aufklapptexte 150–193 Wörter;
- 395/395 Aufklapptexte genau 2 Absätze;
- PHP 123/123 PASS;
- 971/971 Bilddateien byte-identisch zu 1.50.694;
- allgemeiner Petrol-Leadblock ist im 1.50.695-CSS vorhanden.

## REDAKTIONELLER FEHLER

Die unabhängige N-Gramm-Prüfung zeigt wiederkehrende Satzbausteine, die gegen die verbindliche Regel „keine Massenproduktion aus Satzbausteinen / keine wiederkehrenden Absatzgerüste“ verstoßen. Beispiele:
- `zeigt sich viel vom Charakter dieses Hobbys` in 21 Texten;
- `zeigt sich, was dieses Hobby besonders macht` in 13 Texten;
- `ein wesentlicher Teil des Hobbys zeigt sich` in 12 Texten;
- `seinen eigenen Charakter bekommt das Hobby in` in 10 Texten;
- `seinen besonderen Charakter zeigt das Hobby im` in 10 Texten.

Damit ist die frühere Aussage „1.50.695 redaktionell HARD PASS“ widerrufen.

## ERSTER OFFENER BLOCKER

Wiederkehrende Satzbausteine im 395er Textbestand müssen redaktionell entfernt werden, ohne die 1.50.694-Benchmarktexte zu verändern.

## EXAKT EINE NEXT ACTION

**Nur die nachgewiesenen wiederkehrenden Satzbaustein-Gruppen in den betroffenen Texten redaktionell neu formulieren, anschließend vollständige N-Gramm-/Wortlängen-/Benchmark-/PHP-/ZIP-Regressionsprüfung wiederholen.**

## ARBEITSBINDUNG

- 1.50.694 bleibt Qualitätsbenchmark.
- Keine pauschalen Wortersetzungen.
- Keine neue Architektur.
- 1.50.695 nicht als finalen Uploadkandidaten behandeln.
