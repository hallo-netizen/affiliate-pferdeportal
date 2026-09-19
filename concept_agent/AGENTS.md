# CONCEPT AGENT — HARTE ISOLATIONSREGELN

Scope: ausschließlich `concept_agent/**`.

## Null-Schnittstellen-Regel
1. Keine Änderung außerhalb `concept_agent/**`.
2. Kein Import, Aufruf, Wrapper, Exec, Schreibzugriff oder Runtime-Abhängigkeit zu Konzept 1, 2, 3, 4, 4A, STARTMASTER, Affiliate, WordPress-Plugin oder deren Produktionscode.
3. Fremde Bereiche dürfen ausschließlich READ-ONLY als Informationsquelle gelesen werden.
4. Kein Rückschreiben von Ergebnissen, Status, Dateien oder Regeln in andere Konzepte.
5. Kein Merge nach main, kein Publish, kein WordPress-Write.
6. Keine bestehende Regeldatei, Textmaschine, Prüferlogik, Plugin-, Theme- oder Workflowdatei verändern.
7. Concept Agent besitzt eigene Verträge, eigenen Status, eigene Tests und eigene Laufzeitlogik.
8. Jeder Test-Input wird in das Büro kopiert oder als unveränderlicher Testinput referenziert; die Quelle selbst wird nie verändert.
9. Jeder Output bleibt im Concept-Agent-Arbeitsbereich oder in einem expliziten temporären Testverzeichnis.
10. Ein PASS von Concept Agent darf niemals als PASS eines anderen Konzepts ausgegeben werden.

## Arbeitsprinzip
Concept Agent untersucht ausschließlich, ob eine strikt getrennte Agenten-Produktionsstraße zuverlässig funktionieren kann.

Zielkette:
`Input → Research Agent → Übergabeprüfung → Facts Agent → Übergabeprüfung → Writer Agent → bestehende/noch nachzubauende eigene Prüfgrenze → Repair Agent → Final File`

Jeder Agent darf nur seinen eigenen Auftrag bearbeiten.
Kein Agent darf seinen eigenen PASS vergeben.
