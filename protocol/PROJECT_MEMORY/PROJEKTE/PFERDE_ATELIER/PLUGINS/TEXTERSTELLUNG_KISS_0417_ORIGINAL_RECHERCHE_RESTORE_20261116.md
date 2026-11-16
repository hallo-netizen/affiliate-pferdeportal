# Texterstellung KISS 0.4.17 – ursprüngliche Recherche wiederhergestellt
Stand: 2026-11-16. **Nur isolierte Testseite oliver-beil.de. Kein Live-Go.**

## Ursache
Version 0.4.16 führte eine zweite, neue Laufzeitentscheidung ein: Abbruch nach 120 Sekunden ohne neue Daten bzw. maximal 300 Sekunden pro Kategorie. Das konnte den ursprünglichen asynchronen DataForSEO-/Google-Fragen-Workflow vor regulärem Ende stoppen. Testdaten belegen Start und einzelne Roh-Keywords, aber noch keinen erfolgreich abgeschlossenen frischen DataForSEO-Test.

## KISS-Korrektur
- Der PSTE_Research_Driver aus 0.4.10/0.4.11 ist wieder der einzige unveränderte **Ausführungskern**. Ursprüngliche Datei-SHA256: c85fd3e2d38394e2bbd9e4c98042a3777acbd39574337777a9f6382efe07807e.
- An ihm verbleibt ausschließlich der minimale manuelle Halt-/Aktivierungs-Schutz, der die vorhandene native Queue-Stornierung aufruft. Keine neue Zeitschranke, keine zweite Keyword- oder Kategorieentscheidung, kein erneuter Cron-Worker.
- Der DataForSEO-Originalclient ist byteidentisch zu 0.4.10.
- UI zeigt originale gespeicherte Phase, Roh-Keywords und abgeschlossene Kandidaten statt eines frei erfundenen „Ergebnisfortschritts“. Vor Start zeigt sie das erste Thema derselben originalen Auswahl; keine neue Auswahlentscheidung.
- Alte Keyword-, Lauf- und K0-Daten unverändert, gesperrte/geparkte Jobs nicht pauschal freigegeben.

## Verifizierter Teststand
Lokale Simulation des tatsächlichen PSTE_Research_Driver-Codes mit nachgebildetem WordPress-Speicher und **synthetischen** Providerantworten: 10/10 Assertions PASS (Halt bei Seitenaufruf, manueller Start, drei Providerphasen, langer Wartezustand, Verarbeitung zum Ergebnis, native Queue-Stornierung, keine automatische Wiederaufnahme). 77/77 PHP-Dateien syntaxfehlerfrei. 86 Archiv-Dateien, ZIP CRC OK. Gegenüber 0.4.16 genau drei Dateien geändert: Main, Original-Research-Driver, README. 
**Nicht getestet:** echter WordPress-/MySQL-/DataForSEO-Ende-zu-Ende-Durchlauf; keine Livefreigabe.

## Büroablage (vollständige ZIP und QA)
- `/pferdeatelier/PLUGINS/ARBEITSRAUM_PSTE_KISS/Texterstellung_KISS_0.4.17_TEST_Originalrecherche_wiederhergestellt.zip`
- `/pferdeatelier/PLUGINS/ARBEITSRAUM_PSTE_KISS/TEXTERSTELLUNG_KISS_0.4.17_RESTORE_ORIGINAL_RECHERCHE_STAND_20261116.md`
ZIP SHA256: `7b2b849853e1fd4e3aac160ffd5cddce479b6bd4f2f8a304b907f2353934fda1`.

## Weiterführung
Nach Backup nur auf oliver-beil.de bestehendes Plugin durch ZIP ersetzen, **nicht löschen**. Keine automatische Wiederaufnahme des alten Jobs. Exakt ein neuer bewusster Forschungsstart; erst bei echtem Abschluss MINI Kategorie/Redaktion/Titel -> K0 -> WordPress-Entwurf. Kein neuer Plugin-Fix an Einzelereignissen ohne Ursachennachweis.