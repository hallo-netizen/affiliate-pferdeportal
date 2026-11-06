# MINI:start – Pferdeatelier Titelideen

**Einfacher Ablauf wie bei K0. K0 selbst bleibt unverändert. Keine KI-API, keine WordPress-Änderung, kein neues Plugin, kein Signatursystem.**

1. `MINI:start` mit bestehender Keyword-Rohdatei. Zuordnung `JA / NEIN / VIELLEICHT`.
2. Titelworker macht nur Vorschläge nach den vorhandenen ursprünglichen Titelregeln. Er darf sich nicht selbst freigeben.
3. Die getrennte GitHub-Prüfung kontrolliert die festen Regeln und Deutsch mit **LanguageTool 6.8**.
4. Fehler → Reparaturbericht → Titelworker verbessert beanstandete Titel → **dieselbe Prüfung erneut**. Keine erfundene Freigabe.
5. Prüfergebnis und Titelvorschläge zurückgeben. Die spätere redaktionelle SEO-Entscheidung bleibt beim vorhandenen WordPress-Ablauf.

**Keine zusätzliche WordPress-Kopplung.** Die früher in `TITELREGELN_V1.json` enthaltenen Signatur-/Importfelder sind veralteter technischer Entwurf, kein Auftrag. Die dortigen fachlichen `hard_rules` und `contracts/intent-first-title-governance-v1.json` gelten unverändert.

## Nachweis zur vorliegenden 100er-Titeldatei

- **Endfassung:** `mini-title-gate/ERGEBNIS_100_TITEL_20261106.json`
- 100 echte Ausgangskeywords abgeglichen, 87 JA, 9 VIELLEICHT, 4 NEIN; 97 Titel. Original-Queries, Entscheidungen, Intentfelder und Paketdaten unverändert.
- Lokale feste Titelprüfung und neun positive/negative Prüf- bzw. Reparaturtests bestanden.
- **Alle 97 Titel mit LanguageTool 6.8 geprüft**, realer GitHub-Lauf [42207349100](https://github.com/hallo-netizen/affiliate-pferdeportal/actions/runs/42207349100): 11 Hinweise, davon 11 exakt verifizierte Fachbegriffe/Eigennamen; **0 ungeklärte Sprachbefunde**. Keine pauschale Abschaltung der Rechtschreibprüfung.
- Reale unabhängige GitHub-Gegenproben im privaten Titelprüfer: [Fehler abgelehnt](https://github.com/hallo-netizen/mini-titelpruefer/actions/runs/42196709788), [Korrektur akzeptiert](https://github.com/hallo-netizen/mini-titelpruefer/actions/runs/42196918970). Private Prüfstelle ist wieder außerhalb des ChatGPT-Zugriffs.
- K0 und Live-Plugins wurden **nicht geändert**. Keine Produktions-/Kannibalisierungsfreigabe.


**Exakte LanguageTool-Fachwortliste für spätere Prüferpflege:** Horseware-Regendecken, Abschwitzfunktion, Wasserführanlagen, Pfriemenschwanz-Eier, Gräsermischung, Heucobs, Schleich-Pferdeanhänger, Deichselabdeckungen, Humbaur-Pferdeanhänger. Dazu die korrekte Eigennamenschreibung „des Westfälischen Warmbluts“ (LanguageTool meldet fälschlich DE_CASE). Nur diese konkret bestätigten Treffer ausnehmen; alle anderen Befunde müssen weiterhin gesperrt bleiben. Diese Ausnahmen sind **im privaten Prüfer noch nicht nachgewiesen**.

**Eine reale Grenze bleibt:** Der private Dauerprüfer kennt die elf Fachwort-Ausnahmen derzeit nicht nachweislich. Seine automatische Rückgabe an den Chat-Titelworker ist nicht eingerichtet. Deshalb gilt der vollständige Sprachtest als **QA der vorliegenden 97 Titel**, nicht als Beweis einer vollständig automatischen Endlosschleife oder eines privaten 97er-PASS. Der Titelworker kann beanstandete Titel hier korrigieren und erneut vorlegen, aber GitHub kann ohne Schreibmodell keine neue Formulierung erfinden. Keine weitere Freischalt-Runde für diesen Chat verlangen.

**Gültigkeit:** Diese Datei ist MINI-Orientierung und keine Änderung der zentralen K0- oder Produktionsautorität.

## Gebündelte Endprüfung (06.11.2026)

**100 Original-Keywords / 97 Titel**, 87 JA, 9 VIELLEICHT, 4 NEIN. Rohqueries, Titelabsichten, Entscheidungen und Paketzuordnung vollständig unverändert. Enddatei: `ERGEBNIS_100_TITEL_20261106.json`, Git-Blob `13051feaef974e57a7ec358cccaeb434679e750b`. 23 formale/strukturelle Prüfungen und 11 Positiv-/Negativ-Fälle am bestehenden Prüfer lokal bestanden; **diese lokalen Tests überspringen LanguageTool ausdrücklich**. Der getrennte echte LanguageTool-6.8-Lauf mit allen 97 Titeln (GitHub-Run 42207349100) lieferte 11 erkannte Fachwort-/Eigennamenbefunde, 0 ungeklärte Befunde.

**Sechs mögliche Doppel-Suchabsichten für den bereits vorhandenen Redaktionsplan**, keine Titel- oder Artikelfreigabe:
- Regendecken allgemein: 1 und 8.
- Fleece-Regendecken und Wärme: 3 und 19.
- Günstige Regendecken: 7 und 85.
- Regendecken im Test/Vergleich: 9, 11 und 86.
- 0g/ungefütterte Regendecken: 82 und 84.
- Gebrauchte Pferdeanhänger prüfen und Schwachstellen: 94 und 99.

**Wichtige, nicht verheimlichte Grenze:** Im privaten Titelprüfer sind Fachwort-Ausnahmen für diese 97 Titel und eine durchgehend automatische ChatGPT↔GitHub-Reparaturrückgabe nicht verifiziert. Ein echter privater 97-Titel-PASS ist deshalb **nicht** behauptet. Reparaturbericht → Korrektur durch Titelworker → erneute Prüfung funktioniert als Ablauf; GitHub schreibt die Korrektur ohne Schreibmodell nicht selbst. Keine zusätzliche Technik, WordPress-Kopplung oder Freischalt-/Sperrrunde anfordern.

**Nur MINI-Qualitätskontrolle.** K0, WordPress und vorhandene Produktionswege unverändert. Die Daten sind Titelvorschläge, keine SEO- oder Produktionsfreigabe.
