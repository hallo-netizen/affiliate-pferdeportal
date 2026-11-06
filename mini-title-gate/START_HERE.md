# MINI:start – KISS-Konzept (nur Titel, 06.11.2026)

**Zweck:** Fehler bei der Titelerstellung verhindern. **Keine** Absicherung des WordPress-Imports. K0 strikt unverändert.

## Ein einziger Ablauf
1. `MINI:start`: vorhandene Original-Titelregeln und Keyword-Daten übernehmen.
2. Titelworker formuliert Vorschläge, gibt sich **keine eigene Freigabe**.
3. Getrennter GitHub-Qualitätsprüfer kontrolliert Regeln und Sprache mit LanguageTool 6.8, ohne KI-API.
4. Fehlerbericht → nur beanstandete Titel verbessern → erneut prüfen. Kein Qualitäts-PASS ohne bestandenen Prüfbericht.
5. Geprüfte Titel im **bisherigen** redaktionellen Ablauf zurückgeben; WordPress importiert wie bisher. Keine neuen technischen Importfreigaben, Schlüssel oder Signatur-Integration.

## Geprüfter Iststand
GitHub-Negativtest: Run 42196709788 lieferte REPAIR_REQUIRED (fehlender Qualitäts-PASS). GitHub-Positivtest: Run 42196918970 lieferte PASS. Diese zwei Fälle beweisen die GitHub-Regel- und Sprachprüfung, **nicht** eine vollautomatische Texterstellung/Reparatur oder eine vollständige fachliche Titelprüfung.

**Offene Korrekturen:** GitHub prüft manche Regeln nur formal; Natürlichkeit, Suchabsicht und semantische Doppelungen werden dadurch nicht zuverlässig in allen Fällen erkannt. Die Reparaturtexte werden bisher nicht automatisch in GitHub erzeugt. Erst diese Qualitäts- und Ablaufgrenzen lösen, **ohne neue WordPress- oder GitHub-Freigabeinfrastruktur**.

**Altlasten, nicht mehr Teil des Zielkonzepts:** Unterschriften, privater Schlüssel, WordPress-Prüfvertrag und die dazu geplante Kopplung. Entsprechende Felder in der alten `TITELREGELN_V1.json` und frühere QA-Berichte dokumentieren den veralteten Entwurf und sind **keine neuen Arbeitsaufträge**. Die ursprünglichen **fachlichen Titelregeln bleiben gültig**; die Dateien werden nicht ungeprüft umgeschrieben, solange die unabhängige Prüfstelle eine eigene Kopie benutzt.

**Grenze:** Ohne GitHub-Zugriff wird der private Prüfer nicht von ChatGPT verändert. Keine erneute Freischalt-/Sperr-Runde verlangen.

Dies ist nur die MINI-Konzeptkorrektur, **keine zweite Current-/NEXT-ACTION-Autorität**, keine Freigabe für K0 oder LIVE.
