# K0 START

## Zentraler Befehl

`K0:start`

## SICHTBARES CHATVERHALTEN — HARD RULE

Nach `K0:start` mit gültiger angehängter Datei:

**SOFORT AUSFÜHREN. NICHT ERKLÄREN. NICHT ANKÜNDIGEN. NICHT ZUSAMMENFASSEN.**

Verboten sind insbesondere sichtbare Zwischenmeldungen wie:
- „Wo stehen wir?“
- „Ich prüfe jetzt …“
- „Ich starte zuerst …“
- „Der aktuelle Stand …“
- „Ich habe erkannt …“
- Pläne, Statusmeldungen, Prozessbeschreibungen oder Prüferklärungen.

Die erste sichtbare Antwort nach `K0:start` darf ausschließlich sein:
1. die **fertige verifizierte WordPress-Datei**, oder
2. ein **echter terminaler Blocker**, der intern nicht lösbar ist.

Alle notwendigen Prüfungen erfolgen intern und still. Bei einem reparierbaren Fehler wird intern weitergearbeitet. **Kein Warten auf „weiter“.**

## Normalbetrieb

Nutzerablauf:

`Datei hochladen -> K0:start -> intern vollständig produzieren -> fertige WordPress-Datei`

Keine Portalangabe. Keine manuelle Portalauswahl.

## Job-Identität

Exakt:

`title + target_keyword + category + article_type + plan_slot`

Portalzuordnung automatisch über `K0_PORTAL_REGISTRY.json`; unbekannt oder mehrdeutig = fail-closed.

## Interner Produktionsweg

Ohne sichtbare Zwischenkommunikation:

1. aktuellen Upload als `WORDPRESS_INTAKE.json` binden;
2. Portal automatisch erkennen;
3. Recherche;
4. Schreiben;
5. K0-Regeln inklusive Tabellenregel;
6. PPM 6.7.9;
7. LanguageTool 6.8;
8. falls reparierbar: intern reparieren und erneut prüfen;
9. echten WordPress-Export `SYSTEM4_WORDPRESS_HANDOFF_V1` erzeugen;
10. Export verifizieren;
11. Artifact herunterladen;
12. finale JSON-Datei direkt im Chat ausgeben.

## Live-Bindung

Repository: `hallo-netizen/affiliate-pferdeportal`

Branch: `konzept0-portal-neutral-20261002`

Current: `K0_CURRENT_STATE.json`

Workflow: `.github/workflows/k0-production-e2e.yml`

Exporter: `engine/k0_wordpress_export.py`

Gate: `engine/k0_production_gate.py`

WordPress:
- Vertrag: `SYSTEM4_WORDPRESS_HANDOFF_V1`
- Importer: `Portal SEO Editorial Plan Compiler 0.28.27`
- PPM: `6.7.9`
- `direct_wordpress_upload_ready=true`
- `publish_allowed=false`

Der alte `SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2` ist kein WordPress-Endvertrag.

## Hardlocks

- keine Qualitätsreduzierung;
- keine Performance-Regressionsänderung;
- K9 unverändert;
- K10 unverändert;
- kein manuelles Portal;
- keine sichtbare Zwischenantwort;
- kein Stopp bei intern lösbaren Fehlern.
