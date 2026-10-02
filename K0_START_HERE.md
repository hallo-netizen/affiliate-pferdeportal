# K0 START

## Zuständige Current-Autorität

Diese Datei ist **nur Navigation**.

Einzige aktuelle K0-Status-/Blocker-/NEXT-ACTION-Autorität:
`K0_CURRENT_STATE.json`

Pflichtweg für Status-/Fortsetzungsfragen:
`K0_START_HERE.md -> K0_CURRENT_STATE.json -> Frischecheck -> genau eine NEXT ACTION`

Keine andere K0-Datei, Evidence, History, Run-Datei oder Übergabe darf als CURRENT verwendet werden.

## Zentraler Befehl

`K0:start`

## HARD RULE — SOFORT SCHREIBEN

Wenn eine gültige K0-Datei angehängt ist und der Nutzer `K0:start` schreibt:

**SOFORT MIT DER ARTIKELPRODUKTION BEGINNEN.**

Vor dem Schreiben verboten:
- Current lesen;
- Branch prüfen;
- Repository prüfen;
- Workflowstatus prüfen;
- alten Laufstatus prüfen;
- Blocker suchen;
- Teststände vergleichen;
- Prüfergebnisse zusammenfassen;
- irgendeine Vorabdiagnose durchführen.

Die angehängte Datei ist im Normalbetrieb die unmittelbare Job-Autorität.

Nur wenn beim tatsächlichen Produktionslauf ein technischer Fehler oder eine fehlende Bindung auftritt, dürfen Current/Repository/Workflow intern zur Fehlerauflösung gelesen werden.

## SICHTBARES CHATVERHALTEN

Keine Vorrede.
Kein Plan.
Keine Statusmeldung.
Keine Prüfankündigung.
Keine Prozessbeschreibung.

Insbesondere verboten:
- „Wo stehen wir?“
- „Ich prüfe zuerst …“
- „Ich lege jetzt den Job an …“
- „Ich löse jetzt den Lauf aus …“
- „Die Live-Autorität steht …“
- „Der Upload ist gültig …“

Die erste sichtbare Antwort nach `K0:start` ist ausschließlich:
1. die fertige verifizierte WordPress-Datei, oder
2. ein echter terminaler Blocker, der intern nicht lösbar ist.

## Normalweg

`Upload -> K0:start -> schreiben -> prüfen -> reparieren falls nötig -> WordPress-Datei`

Portalzuordnung automatisch.

Job-Identität:
`title + target_keyword + category + article_type + plan_slot`

## Interner Produktionsweg

1. aktuellen Upload binden;
2. Portal automatisch erkennen;
3. Recherche;
   - bei `Eigenschaftssieger`: Produkt-Eigenschaftsrecherche vor dem Writer; vergleichbare Messwerte, eindeutiger Sieger und zentrale Ablage in `K0_PRODUCT_PROPERTY_STORE.json`;
4. intern `content_profile.search_intent` binden;
5. **Artikel schreiben**; bei `Eigenschaftssieger` ausschließlich aus dem gebundenen Produkt-Eigenschaftspaket;
6. K0-Regeln prüfen, inklusive Search-Intent-Konsistenz und Anti-Boilerplate-Gate;
7. PPM 6.7.9;
8. LanguageTool 6.8;
9. reparierbare Fehler intern beheben und weiterlaufen;
10. `SYSTEM4_WORDPRESS_HANDOFF_V1` erzeugen;
11. Export verifizieren;
12. finale Datei an Chat ausgeben.

Kein Warten auf `weiter`.

## Fest gebundener Produktionsweg

Repository: `hallo-netizen/affiliate-pferdeportal`

Branch: `konzept0-portal-neutral-20261002`

Canonical authoring workflow: `.github/workflows/k0-authoring-context.yml`

Canonical writer/production workflow: `.github/workflows/k0-writer-accept.yml`

Direkter `ARTICLE_PACKAGE.json`-Produktionsstart ist entfernt und verboten.

Exporter: `engine/k0_wordpress_export.py`

Gate: `engine/k0_production_gate.py`

WordPress-Importer: `Portal SEO Editorial Plan Compiler 0.28.30-pste-v5-binding-safe`

WordPress-Vertrag: `SYSTEM4_WORDPRESS_HANDOFF_V1`

`publish_allowed=false`

Der alte `SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2` ist kein WordPress-Endvertrag.

## Hardlocks

- keine Qualitätsreduzierung;
- keine Performance-Regressionsänderung;
- K10 unverändert;
- kein manuelles Portal;
- keine Vorabprüfung im Normalbetrieb;
- keine sichtbaren Zwischenmeldungen;
- kein Stopp bei intern lösbaren Fehlern.


## Semantik-Hardlock

Ein Artikel darf den WordPress-Export **nicht** erreichen, wenn:
- `article_type` und `content_profile.search_intent` nicht zusammenpassen;
- ein informationales FAQ in Kauf-, Auswahl-, Passform-, Bedarfs- oder Entscheidungslogik kippt;
- bekannte verbotene Schablonen wie „Für die Praxis heißt das: Betrachte …“, „Trenne Muss-Kriterien …“, „Ein guter Vergleich beginnt …“ oder die alte generische Tabellenform wieder auftauchen.

Diese Sperre ist in `engine/k0_production_gate.py` technisch erzwungen und in `engine/k0_wordpress_export.py` nochmals als Pflicht-Gate gebunden.


## PRODUKTIONSWEG-HARDLOCK

Ein sichtbarer Artikeltext darf K0 ausschließlich als `K0_WRITER_DRAFT_V1` betreten.

Verboten:
- fertigen Artikel als `ARTICLE_PACKAGE.json` in den Produktionslauf legen;
- Writer-Nachweis nachträglich auf einen fertigen Artikel stempeln;
- Produktion direkt aus einem frei angelegten Artikelpaket starten;
- WordPress-Export ohne versiegeltes Writer-Produkt.

Zwingende Kette:

`5-Feld-Intake -> textfreier AUTHORING_CONTEXT -> unveränderbarer WRITER_JOB -> K0_WRITER_DRAFT_V1 -> Writer-Seal -> K0/PPM/LT -> kanonische article_id -> WordPress 0.28.30`

Nur `.github/workflows/k0-writer-accept.yml` darf aus einem Writer-Draft ein `K0_ARTICLE_PACKAGE_V1` erzeugen.
