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
## Praxiskontrolle: echter 100er-Bestand (06.11.2026)
- 100 Original-Keyworddatensätze gegen 100 überarbeitete Datensätze abgeglichen; alle Rohqueries, Entscheidungen, Batch- und Zeitfelder sowie Intentbezeichnungen sind unverändert.
- 87 JA, 9 VIELLEICHT, 4 NEIN; 97 Titelvorschläge; 0 formale Regelverstöße in der lokalen Gesamtprüfung (Doppelpunkt, Sonderzeichen, Länge, Leerzeichen, Fragezeichen, Titelduplikat, unzulässige Überschriftenfüllsel).
- Frühere 90 Titel mit Doppelpunkt sind in der korrigierten Fassung bereinigt.
- **Diese Gesamtprüfung ist nicht gleichbedeutend mit einem kompletten unabhängigen LanguageTool- oder semantischen Durchlauf aller 97 Titel in GitHub.** Die zwei echten GitHub-Läufe belegen allein den positiven und negativen Testfall.
- Ob automatisch wiederholte Texte vom Chat-Titelworker bei einem GitHub-Fund ohne manuellen Transfer entstehen, ist **nicht** technisch eingerichtet. GitHub erstellt einen Reparaturbericht; die eigentliche Korrektur durch den Titelworker ist ein separater Schritt. Keine automatisierte Endlosschleife oder vollständige Sprachqualität behaupten.

## Fortsetzung 06.11.2026 – inhaltliche Vier-Punkte-Reparatur der 100 Titel

- In der bestehenden 100er-Datei wurden die **Titeltexte von genau vier bestehenden Einträgen** gezielt korrigiert. Entscheidungen, Keyword-Rohdaten, Intentbezeichnungen, Batch- und Zeitfelder bleiben unverändert:
  - `pfriemenschwanz pferd eier`: „Pfriemenschwanz-Eier beim Pferd erkennen und einen Befall abklären“ (Eier-Absicht wieder sichtbar).
  - `teuerstes pferd deutschland`: „Welches Pferd gilt als das teuerste Deutschlands?“ (einzelnes Rekordpferd statt allgemeiner Preistreiber).
  - `teuerste pferd der welt`: „Welches Pferd war das teuerste der Welt?“ (Rekordfrage statt Ursachen hoher Preise).
  - `anhängerkamera pferd`: „Anhängerkameras zur Überwachung beim Pferdetransport auswählen“ (keine unbelegte Sicherheitsgarantie).
- **100 Datensätze, 97 Titel:** bestehender Prüfcode lokal mit `--skip-lt-for-tests` ausgeführt; Formregeln PASS.
- **Reparaturdurchlauf:** absichtlich falscher Doppelpunkt wurde abgelehnt, `reparaturauftrag.json` entstand, nach Korrektur PASS. **9 bestehende Tests PASS.**
- **Ehrliche Grenze:** Kein LanguageTool-6.8-Gesamtlauf über alle 97 Titel in dieser Nachkorrektur, kein automatisches ChatGPT↔GitHub-Rückkopplungssystem, keine unabhängige endgültige semantische Abnahme. Deshalb **nur vorbereitete/korrigierte Titelvorschläge, keine Produktionsfreigabe**.
- Kein GitHub-Privatrepo-Zugriff angefordert; keine Änderung an K0, WordPress oder bestehenden Plugins. Die Original-Titelregeln bleiben byteidentisch.
