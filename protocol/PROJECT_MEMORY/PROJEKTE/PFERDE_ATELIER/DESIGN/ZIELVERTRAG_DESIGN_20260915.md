# ZIELVERTRAG – PFERDE ATELIER DESIGN – 2026-09-15

STATUS: AKTIV
FASSUNG: 1.0

## ZIEL
Die bestehende funktionierende Pferde-Atelier-Seitenarchitektur bleibt erhalten. Die neue Pagination-/Link-/Hover-Regel wird nur so ergänzt, dass Pferderassen und Glossar vollständig erreichbar und funktionsfähig bleiben.

## VERBINDLICHE ERGEBNISSE

1. **Pferderassen**
- Startseite: 16 Einträge je Seite;
- Rassengruppen/Unterkategorien: 16 Einträge je Seite;
- Pagination oben und unten, nur wenn mehr als eine Seite existiert;
- bestehendes Routing, Templates, Breadcrumbs und Seitenstruktur bleiben erhalten.

2. **Glossar**
- Glossar-Startseite: 16 Begriffe je Seite;
- Themenwelten/Unterkategorien: 16 Begriffe je Seite;
- Pagination oben und unten, nur wenn mehr als eine Seite existiert;
- A–Z-/Filterzustand bleibt beim Blättern erhalten;
- `Alle Glossarbegriffe` führt zur paginierten Glossar-Startseite und löst keine unlimitierte Gesamtabfrage aus;
- bestehendes Routing, Templates, Breadcrumbs und Seitenstruktur bleiben erhalten.

3. **Glossar – Mehr zum Thema**
- Design rendert das vom Glossar-Datensatz gelieferte `primary_target`;
- fachliche Zielpriorität liegt im Glossar-Strukturvertrag: zuerst starke obere Affiliate-Portal-Kategorie/-Hauptseite, Journal nur als Fallback;
- Design erfindet kein eigenes Ziel.

4. **Beitragsnavigation**
- Zurück-/Vor-Links unter normalen Beiträgen behalten ihre bestehende Grunddarstellung;
- Hover: ocker + unterstrichen, analog zum Standard-Linkhover.

5. **Allgemeines Design**
- die allgemeine Pagination-Regel darf zentral wiederverwendbar sein;
- sie darf projektbezogene Routen/Renderer/Queries nicht ersetzen oder still übernehmen;
- Freigabe nur nach isolierter und kombinierter Positiv-/Negativprüfung.

## PASS-BEDINGUNG
PASS erst wenn gleichzeitig belegt:
- real installierte Versionen beider Designplugins vor Reparatur bestimmt;
- Fehler aus `DESIGN-LIVE-20260915-001` reproduziert und Ursache isoliert;
- Pferderassen Start + Untergruppe positiv;
- Glossar Start + Themenwelt + A–Z positiv;
- Negativtests erkennen Ausfall jeder dieser Welten;
- Universal + Pferde-Design gemeinsam geprüft;
- ZIP, Version, Install-over-old und Regression PASS;
- realer WordPress-Readback bestätigt Pferderassen + Glossar;
- erst danach Plugin-CURRENT-/Artefaktsync.

## NICHT ZULÄSSIG
- keine unlimitierte `Alle`-Abfrage;
- kein Austausch funktionierender Router/Renderer nur für Pagination;
- kein PASS aus Codeansicht;
- kein isolierter Plugin-PASS als Gesamtfreigabe;
- kein CURRENT-Sync vor realem Gesamt-PASS.
