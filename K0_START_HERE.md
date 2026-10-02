# K0 START

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
4. **Artikel schreiben**;
5. K0-Regeln prüfen;
6. PPM 6.7.9;
7. LanguageTool 6.8;
8. reparierbare Fehler intern beheben und weiterlaufen;
9. `SYSTEM4_WORDPRESS_HANDOFF_V1` erzeugen;
10. Export verifizieren;
11. finale Datei an Chat ausgeben.

Kein Warten auf `weiter`.

## Fest gebundener Produktionsweg

Repository: `hallo-netizen/affiliate-pferdeportal`

Branch: `konzept0-portal-neutral-20261002`

Workflow: `.github/workflows/k0-production-e2e.yml`

Exporter: `engine/k0_wordpress_export.py`

Gate: `engine/k0_production_gate.py`

WordPress-Importer: `Portal SEO Editorial Plan Compiler 0.28.27`

WordPress-Vertrag: `SYSTEM4_WORDPRESS_HANDOFF_V1`

`publish_allowed=false`

Der alte `SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2` ist kein WordPress-Endvertrag.

## Hardlocks

- keine Qualitätsreduzierung;
- keine Performance-Regressionsänderung;
- K9 unverändert;
- K10 unverändert;
- kein manuelles Portal;
- keine Vorabprüfung im Normalbetrieb;
- keine sichtbaren Zwischenmeldungen;
- kein Stopp bei intern lösbaren Fehlern.
