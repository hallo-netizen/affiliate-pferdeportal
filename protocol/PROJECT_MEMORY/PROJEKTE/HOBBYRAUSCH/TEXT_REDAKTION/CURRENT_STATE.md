# HOBBYRAUSCH – TEXT_REDAKTION – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-09-30
STATUS: ARCHITEKTURGRENZE KORRIGIERT / EIGENES HOBBY-DEPOT-TEXT-/SEO-PLUGIN NOCH NICHT GEBAUT / PSTE NUR REFERENZ

## Rolle

Einzige aktuelle Zustandsautorität des Scopes `HOBBYRAUSCH_TEXT_REDAKTION`.

## Harte Projektgrenze

Hobby Depot darf das Pferdeatelier-PSTE weder verändern noch als installierten Produktivbaustein voraussetzen.

Pferdeatelier-PSTE ist für Hobby Depot ausschließlich:
- technische Referenz;
- Vergleichsquelle für bewährte Duplicate-/Kannibalisierungslogik;
- Vergleichsquelle für Performance-/Storage-Learnings.

Nicht erlaubt:
- Installation eines für Pferdeatelier gebauten PSTE-Pakets als Hobby-Depot-Zielplugin;
- Änderung des live installierten Pferdeatelier-PSTE aus diesem Scope;
- technische Abhängigkeit Hobby Depot → Pferdeatelier-PSTE.

## Korrektur des bisherigen Arbeitsstands

Die zuvor erzeugten PSTE-0.57.14-Ownership-Pakete waren lokale Referenz-/Machbarkeitsprototypen.

Sie sind für Hobby Depot:
**NICHT INSTALLIEREN / NICHT PRODUKTIV VERWENDEN.**

Es wurde kein live installiertes Pferdeatelier-PSTE verändert.

Der lokale Prototyp hat fachlich/technisch trotzdem belegt, dass folgende allgemeine Mechanismen funktionieren:
- `owner_concept_id`;
- `semantic_intent_key`;
- semantische Dublettenblockade;
- Frageform besitzt keine FAQ-Owner-Autorität;
- V1.9.1-Kategorie-Handoff kann technisch konsumiert werden.

Diese Erkenntnisse dürfen in ein eigenes Hobby-Depot-Plugin übernommen werden, nicht das Pferdeatelier-Plugin selbst.

## Zielarchitektur

Hobby Depot erhält genau **einen eigenen Text-/SEO-Pluginstrang**.

Dieser soll:
- den allgemeinen V1.9.1-Kategorie-Handoff lesen;
- Artikel-Intent und Owner-Kategorie eindeutig binden;
- Dubletten/Kannibalisierung fail-closed blockieren;
- später die Hobby-Depot-Redaktionslogik tragen;
- projektneutralen Code nutzen, wo sinnvoll;
- keine Pferdeatelier-Fachdaten oder -Produktivzustände übernehmen.

Performance-/Storage-Learnings aus PSTE werden nur per Diff/Review übernommen, wenn sie für das neue Plugin tatsächlich relevant sind.

## Aktueller belastbarer Fachstand Buchbinden

Fachliche Ownership-Matrix und lokaler E2E-Prototyp sind belegt.

DataForSEO-Bestand:
- Einstieg: Evidenz vorhanden;
- Ausrüstung: Evidenz vorhanden;
- Material: Mindestbreite vorhanden;
- Techniken/Praxis: Evidenz vorhanden;
- Fragen/Probleme: Research-Gap;
- FAQ: Research-Gap.

## Erster offener Blocker

Kein fachlicher Ownership-Blocker.

Technisch fehlt der **eigene Hobby-Depot Text-/SEO-Pluginstrang**.

## NEXT ACTION

Kein PSTE installieren oder verändern.

Als Nächstes:
1. kleinsten Funktionsumfang des einen Hobby-Depot Text-/SEO-Plugins aus dem bereits bewiesenen Ownership-Vertrag ableiten;
2. nur allgemeine, relevante PSTE-Mechanismen als Referenz übernehmen;
3. eigenes Namespace, eigene Options/Storage-Identitäten und eigenes Release-Artefakt;
4. danach Buchbinden als erster E2E-Testfall.

Keine Plugin-Orgie: genau ein Hobby-Depot Text-/SEO-Plugin.
