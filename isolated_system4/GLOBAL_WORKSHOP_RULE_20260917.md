# SYSTEM4 GLOBAL WORKSHOP RULE

## Unveränderliche Workflow-Invariante

FEHLER -> WERKSTATT.

Diese Regel gilt global fuer den gesamten System-4-Produktionslauf, unabhaengig davon:
- welcher Pruefer oder welche Stufe den Fehler erzeugt,
- ob es ein Einzelartikel-, Batch-, Handoff- oder Ausgabefehler ist,
- wie viele Findings gleichzeitig vorliegen,
- ob der Fehler heute bereits bekannt ist oder erst spaeter durch einen neuen Pruefer hinzukommt.

Kein Pruefer und keine Zwischenstufe darf einen Fehler eigenstaendig als terminales Workflow-Ende behandeln.

Die zentrale Werkstatt entscheidet ausschliesslich:
1. REPAIRABLE: alle verfuegbaren Findings erhalten, zustaendigen Owner/Target bestimmen, gezielt reparieren, danach den vollstaendigen fachlich erforderlichen Recheck ausfuehren und den normalen Lauf fortsetzen.
2. NON_REPAIRABLE: nur wenn Integritaet, Autoritaet, fehlende Pflichtquelle, ungueltige Bindung oder ein sonst objektiv nicht reparierbarer Zustand vorliegt; dann fail-closed mit dauerhaftem Befund.

## Harte Anforderungen

- Keine Qualitaets-, Inhalts-, Design-, LanguageTool-, PPM-, Link-, Fact-, Batch- oder WordPress-Regel wird abgeschwaecht oder entfernt.
- Findings duerfen nicht auf das erste Finding reduziert werden.
- Mehrere Findings duerfen gemeinsam bearbeitet werden, soweit sie demselben autoritativen Owner/Target zugeordnet sind.
- Nach jeder Reparatur gilt der vollstaendige erforderliche Recheck; kein PASS darf durch die Werkstatt selbst erzeugt werden.
- Batch-Fehler muessen die betroffenen Artikel/Findings strukturiert an die Werkstatt liefern statt nur eine Summenzahl und STOP.
- Neue zukuenftige Pruefer fallen automatisch unter dieselbe globale Fehler->Werkstatt-Invariante.
- Keine Legacy-/Fachworkflow-Ersatzroute, kein Auto-Publish, publish_allowed=false.

## Implementationsprinzip

Die Invariante wird am zentralen Produktions-Orchestrator oberhalb der einzelnen Stufen erzwungen. Bestehende lokale Repair-Router bleiben nur Owner-/Repair-Ausfuehrung und sind nicht mehr die Autoritaet darueber, ob ein Fehler die Werkstatt erreicht.
