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


## HARD RULE — NO-STOP BIS ZIELPUNKT

KEINE ZWISCHENBERICHTE, KEINE RÜCKFRAGEN, KEIN ABSCHLUSS, BEVOR DER DEFINIERTE ZIELPUNKT ERREICHT IST.

WEITERARBEITEN, AUCH NACH PASS-ZWISCHENSCHRITTEN.

STOPP NUR BEI EINEM OBJEKTIV UNBEHEBBAREN BLOCKER.

Ein Zwischen-PASS ist niemals ein Abschluss und niemals ein Stoppsignal.


## WORDPRESS-ENDDATEI-HARDLOCK
1. Interne Concept-Agent-Dateien sind niemals WordPress-Uploaddateien.
2. Als WordPress-ready darf ausschließlich der aktuell real belegte Direktimportvertrag `SYSTEM4_WORDPRESS_HANDOFF_V1` bezeichnet und im Chat ausgegeben werden.
3. Pflicht vor Ausgabe: lokale Validierung gegen die echte PSERC-0.28.23-Vertragslogik inklusive Positiv- und Negativfällen.
4. `publish_allowed` bleibt immer `false`; der Importzielstatus ist ausschließlich WordPress-`draft`.
5. Die korrekte WordPress-Dateiausgabe hier im Chat ist fester Bestandteil des Produktionswegs.
6. Verboten als WordPress-Datei: `CONCEPT_AGENT_FINAL_ARTICLE_V1`, `CONCEPT_AGENT_7_ARTICLE_CHAT_HANDOFF_V1`, `SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2`, `PSERC_APPROVED_PRODUCTION_PACKAGE_V1`, ENDSTEMPEL-Signierauftrag und ENDSTEMPEL-Wrapper.

## BEITRAGSART-HARDLOCK
1. `article_type` kommt gebunden aus dem aktuellen Metadatenbatch und wird unverändert übernommen.
2. Kein Default/Fallback darf einen unbekannten oder gemischten Batch pauschal auf `Beratung` umstellen.
3. Typspezifische Regeln gelten nur für den passenden Typ.
4. `Produktvergleich` und weitere Typen dürfen angeschlossen werden, sobald ihr eigener upstream Fach-/Qualitätsvertrag gebunden ist; die allgemeine Agentenkette bleibt 1..N und typneutral.
5. Codex ist im aktuellen Produktionsweg verboten.

## REDAKTIONSSPRACHE-HARDLOCK
1. Beratungstitel werden vor dem Schreiben erneut gegen die aktuelle Titeloberfläche geprüft. Bereits natürliche/gute Titel bleiben unverändert. Nackte Aktions-Titel der Form `<Keyword> wählen/auswählen/finden` sowie `So findest du <Keyword>` ohne sinnvolle sprachliche Ergänzung dürfen nicht als FINAL passieren; sie müssen natürlich formuliert werden, ohne das Target Keyword zu verändern.
2. Natürliche Titelattribute wie `passend`, `geeignet`, `richtig`, `optimal` oder `ideal` sind reine Präsentationssprache und dürfen das unveränderte Target Keyword natürlich einbetten.
3. Zwischenüberschriften müssen wie normale menschliche Abschnittstitel klingen und den konkreten Nutzen/Inhalt der folgenden Passage benennen. Bürokratische Restphrasen wie `am Pferd sicher beurteilen`, `fachlich einordnen`, `realistisch bewerten` oder `nach Bedarf beurteilen` sind verboten.
4. Jeder Inline-Link muss im sichtbaren Satz einen korrekten Textfluss haben. `</a>` direkt vor einem Buchstaben/Ziffer ist ein Hard-Fail; Satzzeichen direkt nach dem Link bleiben erlaubt.
5. Diese Regeln sind keine bloßen Writer-Hinweise: `textmachine_guard.py` muss sie vor FINAL fail-closed prüfen; positive und negative Regressionstests sind Pflicht.
