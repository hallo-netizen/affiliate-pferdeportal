# Pferdeatelier MINI:start – Einfacher Titelworkflow

**Nur Titelerstellung. K0 wird nicht verändert. Keine externe KI-API. Keine WordPress- oder Signaturlogik.**

1. **MINI:start** plus die vorhandene WordPress-Rohkeyworddatei.
2. Relevanz je Keyword **JA / NEIN / VIELLEICHT** entscheiden. Nur für **JA** Titel vorschlagen; mehrere Titel nur für unterschiedliche Suchabsichten.
3. Titelworker beachtet die **bestehenden unveränderten Titelregeln** aus `TITELREGELN_V1.json` und `contracts/intent-first-title-governance-v1.json`. Der Titelworker darf seine eigenen Ergebnisse nicht freigeben.
4. Die **getrennte GitHub-Prüfung** kontrolliert Regeln und Sprache mit LanguageTool 6.8. Bei Fehlern: Reparaturbericht → nur beanstandete Titel korrigieren → **dieselbe Prüfung erneut**, bis kein gemeldeter Fehler mehr vorliegt.
5. Danach **geprüfte Titelideen zurückgeben**, keine SEO-/Produktionsfreigabe. Der bestehende WordPress-Redaktionsplan entscheidet später allein über vorhandene Artikel und Kannibalisierung.

**Keine zusätzliche Installation, keine Schlüssel, keine Importfreigabe, keine zweite Titelkontrolle.**

## Technisch bestätigt
- Eigenständiger Prüfer im privaten `hallo-netizen/mini-titelpruefer`; ChatGPT-Zugriff vom Eigentümer wieder entzogen.
- Reale GitHub-Gegenprobe mit fehlerhaftem Doppelpunkt: `REPAIR_REQUIRED`, Run 42196709788.
- Reale GitHub-Gegenprobe nach Reparatur: `PASS`, Run 42196918970.
- Die 100 historisch korrigierten Titel: 97 Vorschläge, 0 Doppelpunkte, 9 lokale Form- und Schleifentests bestanden; **die 100 Titel wurden nicht vollständig mit LanguageTool gegen GitHub geprüft**.

## Ehrliche technische Grenze
GitHub kann die Prüfregeln abarbeiten und Reparaturberichte ausgeben, aber **ohne Schreibmodell/externen Aufruf die Formulierungen nicht selbst neu schreiben**. Die Reparatur erfolgt durch den Titelworker, nicht durch einen unsichtbaren KI-Dienst in GitHub. Sprachliche Natürlichkeit und die exakte Suchabsicht sind mit festen Regeln/LanguageTool nicht lückenlos beweisbar. Keine gegenteilige Behauptung oder künstliche 100-%-Freigabe.

Die bisherigen Signatur-/WordPress-Verknüpfungsentwürfe gehören **nicht** zu diesem Mini-Auftrag. Die ursprünglichen fachlichen Regeln bleiben erhalten; obsolete technische Metadaten im alten JSON sind kein Auftrag zum Aufbau eines Import-Freigabesystems.

**K0, PSERC, Live-Plugins und Produktionssysteme unverändert.**
