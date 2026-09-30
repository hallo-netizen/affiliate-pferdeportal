# ZV-PLUGINS-CLEANUP-001 – Pferde Atelier Plugin-/Datenbank-/Performance-Aufräumvertrag

STATUS: AKTIV
FASSUNG: 2026-09-30
GELTUNGSBEREICH: PFERDE_ATELIER / PLUGINS / DATENBANK / PERFORMANCE / AUFRÄUMEN
VERANTWORTLICHER BEREICH: PROJEKTE/PFERDE_ATELIER/PLUGINS

## ZIEL

Pferde Atelier technisch verschlanken und aufräumen, ohne fachliche Funktion oder bereits erreichte Performanceverbesserungen zurückzubauen.

Verbindlicher Endzustand:
- Datenbank unnötig gewachsene Altlasten kontrolliert und belegbar bereinigt;
- betroffene Eigenplugins nachhaltig gegen erneutes unbegrenztes Datenwachstum geschützt;
- vorhandene Performanceoptimierungen bleiben erhalten;
- keine Qualitäts-, Ranking-, Provider-, Slot-, Veto-, Publish-, Recherche-, Kategorie-, Produktions- oder Designfunktion wird wegen der Aufräumarbeit abgesenkt;
- Plugin für Plugin, keine Plugin-Salami: zusammengehörige Datenbank-/Storageänderungen je betroffenem Plugin gebündelt;
- kein neues Hilfsplugin, Runner oder neue Architektur, wenn die Ursache im betroffenen Plugin selbst behoben werden kann;
- irreversible Datenlöschung nur nach belegter Schutz-/Recovery-/Rollbackprüfung;
- nach Bereinigung gleiche Speicher- und Performance-Messung erneut ausführen und gegen den Ausgangszustand vergleichen.

## ARBEITSREIHENFOLGE

1. Reale installierte Version + zuständige Fach-/Releasequelle bestimmen.
2. Pro Plugin Datenwachstum, Retention, Recovery und Performancepfade prüfen.
3. Nur bei belegtem Bedarf einen gebündelten Pluginstand bauen und positiv/negativ/regressiv testen.
4. Erst danach vorhandene Altbestände logisch bereinigen.
5. Danach physischen DB-Speicher zurückholen, soweit technisch nötig.
6. Gleiche DB-/Performance-Diagnose vor/nachher vergleichen.
7. Temporäre/inaktive Hilfsplugins erst nach Abhängigkeits- und Rollbackprüfung aufräumen.

## NICHT ANFASSEN OHNE EIGENEN BEWEIS

- aktive Produktions-/Recoveryzustände;
- Keyword-/Topic-Autoritäten;
- aktuelle Plan-/Produktionsdaten;
- fachliche Qualitäts- und Publish-Gates;
- bestehende Performanceoptimierungen.

## PASS-BEDINGUNGEN

PASS erst wenn:
- alle im aktuellen Scope betroffenen Kernplugins geprüft sind;
- notwendige Schutzfixes installiert und per Readback bestätigt sind;
- bestehende DB-Altlasten nur anhand belegter Regeln bereinigt wurden;
- keine fachliche/Performance-Regression vorliegt;
- physische DB-/Speicherlage neu gemessen wurde;
- abschließender Performancevergleich vorliegt;
- Update-/Rollback-/Evidence-Nachweise und Plugin-Inventar synchron sind.

Keine einzelne Plugininstallation erfüllt diesen Zielvertrag allein.
