# Verbindliche Kurskorrektur: nur minimale Kopie, keine Neuentwicklung
Stand 18.11.2026; Nutzeranweisung im Hab-&-Bewahr-Texterstellungs-Chat.

## Vorrangiger Auftrag
- Original-Pferdeatelier-Plugin als **unveränderte technische Vorlage** verwenden. Aktuell lokal geprüftes Quellarchiv: Texterstellung 0.4.31-KISS-DURCHGAENGIGER-MINI-ABLAUF-PFERDEATELIER.zip, 88 Dateien, 78 PHP. **Originaldatei nicht überschreiben und Pferdeatelier nicht verändern.**
- Genau zwei getrennte Kopien vorbereiten: (A) **Hab & Bewahr** mit Portalname/Zielsite und leerem Ausgangsregal; (B) **jungfräuliche neutrale Kopie** ohne alte Pferdeportal-Daten und voreingetragene Kategorien.
- Zulässige Änderungen: Portal-Kennzeichnung, Portalbezüge in vorhandenen Konfigurationsdateien und Pferde-spezifische Regeln/Beispiele deaktivieren bzw. dort, wo eindeutig notwendig, durch Kommentar ausklammern. Keine neue fachliche Regel ersetzen oder erfinden.
- **Unverändert übernehmen:** bisherige Oberfläche, Original-PSTE-Recherche/DataForSEO, bestehende Kategorienentscheidung und MINI-Worker, K0-Fünffeld-Vertrag, Importer, Entwurf-Status, bisherige Schutz- und Kostenregeln, Datenablage. Keine neue Architektur, keine neue Datenbank, keine zusätzlichen Klassen/Adapter/Assistenten, keine neuen Prüfstationen, keine fachlichen Fixes oder Verbesserungen.
- Technische interne PSTE/PSERC-Namen und bestehende K0-Kompatibilitätskennungen nicht kosmetisch umbenennen, wenn das die Schnittstelle bricht; vor Freigabe dokumentieren.
- Keine pauschale Änderung an der ursprünglichen K0-Verarbeitung und keine Live-Datenänderungen. Keine fremden Altaufträge in der neuen Kopie übernehmen.

## Nachgewiesene Ausgangslage und Grenze
- Tatsächliches 0.4.31-Original enthält Pferde-konkrete Inhalte sowohl in JSON (große Pferde-Kategoriekarte, Familien-Overrides, Domain-Seeds, Journal-Kategorien) als auch an einzelnen PHP-Stellen (Pferde-Titel-/Journal-Regeln, Pferde-Haftpflicht, Pferde-Krankheiten, Hostcheck). **Nur die JSON leeren würde daher nicht alle Pferde-Sachregeln beseitigen.**
- Bestehende Hab-Arbeitskopie 0.4.23 sowie die frühere separate 0.4.24 sind vorhanden; die bisherigen 0.5.0–0.5.2-Versuche führten neue Universal-Adapter, zusätzliche Runtime-Logik und eine neue Architektur ein. **Diese Entwürfe sind durch die Nutzerkorrektur als Entwicklungsrichtung abgelöst und dürfen nicht als Freigabe oder Quellvorlage verwendet werden.**
- Alle Pferde-Sonderfälle dürfen nur dort in der Kopie auskommentiert werden, wo ihre Abhängigkeiten bekannt sind; wenn dadurch die bisherige Recherche nicht funktioniert, nicht durch erfundene Ersatzlogik kaschieren. Zulässiger Status ist dann 'noch nicht freigegeben' statt neuer Architektur.
- Vollständig installationsfertig heißt weiterhin: PHP/ZIP-Prüfung, unveränderter Originalworkflow, korrekte leere Portaldaten und nachvollziehbare Funktionsabnahme der Kopie; keine Freigabe allein wegen Syntax oder Aktivierbarkeit.

## Download- und Büroregel
- Im Chat **nur tatsächlich freigegebene WordPress-Plugin-ZIPs** als Downloads bereitstellen. Keine Tests, Entwicklungsarchive, Protokolle oder unvollständige ZIPs zum Download.
- Fortlaufend exakten Originalbestand, jede geänderte Originaldatei, den Grund und jedes Testergebnis nur in Hab- und Universal-Büro sowie im Arbeitszweig dokumentieren.

## Nächster technischer Schritt
Original 0.4.31 gegen die bisherigen Portal-Kopien auf Dateiebene vergleichen, alle **fachlich wirksamen** Pferde-Sonderstellen einzeln markieren, in den beiden getrennten Klonen nur diese Stellen und Portaldaten ändern. Keine Erweiterung. Erst danach einmaliger Originalworkflow-Test und zwei installierbare Plugin-ZIPs.

**Sofort wirksam:** laufende 0.5.x-Entwicklungsumbauten gestoppt; keine neuen Funktionen, keine Fixes, keine neuen Prüfstationen.