# BÜRO GLOSSAR – HOBBYRAUM

STAND: 2026-09-12
STATUS: AKTIV

## 1-KLICK-ÜBERSICHT

**WAS IST DAS?**  
Der einzige aktuelle Arbeitsraum des Büros GLOSSAR.

**HIER BIST DU RICHTIG, WENN …**  
das Glossar-Konzept, seine WordPress-/Design-Anbindung oder ein technischer Kandidat geprüft wird.

**DU DARFST …**  
den gebundenen Glossar-Auftrag bearbeiten, Nachbarbüros lesen und technische Kandidaten ausschließlich im dafür gebundenen Branch prüfen.

**DU DARFST NICHT …**  
`main` als Experimentierfläche benutzen, die Wissensdatenbank duplizieren, ungeprüfte Plugin-ZIPs ausgeben oder aus einem Konzept automatisch Live-WordPress verändern.

**ALS NÄCHSTES …**  
den unten gebundenen Auftrag abarbeiten.

---

## GEBUNDENER AUFTRAG

**Ziel:**
Die kleinstmögliche saubere technische Architektur für das öffentliche Pferde-Atelier-Glossar bestimmen.

**Pflichtumfang:**
1. aktuellen Pferde-Atelier-Designplugin-Bestand frisch prüfen;
2. bestehende Kategorietext-Mechanik als mögliche Inspiration technisch verstehen;
3. Backend und Frontend getrennt bewerten;
4. Lösung so wählen, dass Glossarbegriffe nicht als normale Beiträge/Karten erscheinen und kein Bildzwang entsteht;
5. pro veröffentlichtem Begriff eigene SEO-Angaben technisch ermöglichen;
6. fachliche Fakten weiterhin ausschließlich aus `../WISSENSDATENBANK/AKTENSCHRAENKE/GLOSSAR/` beziehen;
7. keine zweite große Textmaschine bauen;
8. vor jeder Plugin-Ausgabe Positiv- und Negativprüfung durchführen.

## AKTUELLER ARBEITSBRANCH

`hobbyroom/glossar-office-20260912`

Dieser Branch dient aktuell dem **Campus-/Büroaufbau und Konzeptnachweis**.  
Ein technischer Designplugin-Code-Write benötigt vor Beginn eine frisch gebundene technische Arbeitsbasis. Nicht still denselben Branch zum Produktionsbranch umdeuten.

## NEXT ACTION

Bestehendes Designplugin sowie Kategorietext-Speicherung/-Ausgabe prüfen und daraus 2–3 technisch realistische Glossarvarianten ableiten. Danach KISS-Entscheidung gegen das gesamte Pferde-Atelier-Konzept.

## HARTE GRENZEN

- `main` unangetastet lassen.
- Keine neue Glossar-Faktendatenbank.
- Keine normale Beitragspflicht pro Glossarbegriff.
- Keine Seite pro Glossarbegriff als Standardmodell.
- Kein Beitragsbild-/Grafikzwang.
- Keine Plugin-Orgie.
- Keine neue Textmaschine ohne echten Nachweisbedarf.
- Keine Live-Veröffentlichung.
- Kein PASS aus Codeansicht; Positiv-/Negativtest ist Pflicht.

## RÜCKGABEWEG

Belastbarer neuer Glossar-Stand → `CURRENT_STATE.md` aktualisieren.  
Dauerhafte Architektur-/WHY-Entscheidung → `protocol/PROJECT_MEMORY/AENDERUNGSREGISTER.md`.  
Fachliche Definition/Fakten → ausschließlich Wissensdatenbank/Aktenschrank Glossar.  
Design-Code/-Darstellung → gebundener DESIGN-Arbeitsweg.  
SEO-/Kannibalisierungsregel → TEXT/SEO-Hauptquelle.

## PFLICHT VOR TECHNISCHER AKTION

`protocol/PROJECT_MEMORY/FEHLERREGISTER.md` → relevante autoritative Fehlerquelle vollständig prüfen. Bekannten Fehlerweg nicht erneut ausprobieren.

## Globale Arbeitsort-Sperre

Tresor, Archiv, Backup und Git-Mirror sind niemals Werkbank oder Runner-Quelle.
