# TODO – DataForSEO / Google-PAA-Fragen für Pferde-Atelier-FAQ

Stand: 14.09.2026

## Ziel
Echte, von Google bereits fertig formulierte „Ähnliche Fragen“ / People Also Ask (PAA) systematisch als FAQ-Themenquelle für das Pferde-Atelier sammeln und kategorisieren.

## Bereits bestätigt
- DataForSEO ist bereits angebunden.
- Der vorhandene SEO/PSTE-Datenbestand enthält bereits echte `PAA`- und `PAA_RELATED`-Fragen aus DataForSEO SERP.
- Die FAQ-Verarbeitung kennt `PAA_RELATED` bereits als Evidence Source.
- Keine neue DataForSEO-Anbindung und kein Umbau der Textmaschine als Voraussetzung.

## To-do
1. Aktuellen DataForSEO-SERP-Request im SEO/PSTE-Code exakt lokalisieren.
2. Prüfen, ob aktuell `people_also_ask_click_depth` gesetzt wird.
3. Falls nicht: separaten FAQ-Recherchemodus ergänzen, der denselben DataForSEO-Zugang nutzt.
4. Click-Depth 1, 2, 3 und 4 gegen denselben Seed vergleichen.
5. Deutschland / Deutsch fest binden.
6. Nur echte `PAA` / `PAA_RELATED`-Fragen als FAQ-Rohquelle übernehmen; Keyword Ideas/Suggestions getrennt halten.
7. Originalfrage unverändert speichern; vor der Kategorisierung keine Umformulierung durch die Textmaschine.
8. Seed-Frage / Elternbeziehung mitführen, damit der Google-Fragenbaum erhalten bleibt.
9. Dubletten und nahezu identische Fragen erkennen, Originalformulierungen als Quelle erhalten.
10. Fragen den bestehenden Pferdeatelier-Themen-/FAQ-Kategorien zuordnen.
11. Bereits vorhandene FAQ-Fragen gegenprüfen, damit keine Doppelanlage entsteht.
12. Relevante neue Fragen als FAQ-Kandidaten markieren.
13. Kosten pro Seed / Click-Depth messen und dokumentieren.
14. Positivtest: bekannte Google-PAA-Fragen werden vollständig und unverändert übernommen.
15. Negativtest: Keyword-Suggestion-Fragmente dürfen nicht als echte Google-PAA-Fragen gekennzeichnet werden.
16. Skalierung prüfen: viele Seeds / große Themenbereiche ohne Vermischung der Fragenbäume.
17. Erst nach erfolgreichem Test über dauerhafte Automatisierung entscheiden.

## Testbeispiel
Seed / Referenz: `Pferd`

Bekannte Google-Frage: `Kann man ein Pferd streicheln?`

Ziel: PAA-Fragenbaum bis zur maximal sinnvollen Click-Depth erfassen, Originalformulierungen behalten, deduplizieren und den FAQ-Kategorien des Pferde-Ateliers zuordnen.

## Grenze
Dieses Dokument ist nur eine To-do-Liste. Es ändert weder System-4A-Zielgrenze noch README-/Statuswahrheit, HOBBYRAUM, Textmaschinenregeln oder Produktionsfreigaben.
