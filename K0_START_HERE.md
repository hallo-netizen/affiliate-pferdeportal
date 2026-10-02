# K0 START

## Zentraler Befehl

`K0:start`

## Normalbetrieb

Bei angehängter gültiger `PSERC_TEXTMACHINE_METADATA_BATCH_V2`-Datei sofort arbeiten.

Der Nutzerablauf ist ausschließlich:

`Datei hochladen -> K0:start -> Portal automatisch erkennen -> vollständig produzieren -> verifizierte WordPress-Datei an Chat`

Keine Portalangabe im Befehl. Keine manuelle Portalauswahl.

## Auftrag

Die fünf Felder

`title + target_keyword + category + article_type + plan_slot`

sind die alleinige Job-Identität.

Die Portalzuordnung kommt ausschließlich aus `K0_PORTAL_REGISTRY.json` und muss eindeutig sein. Unbekannte oder mehrdeutige Zuordnung blockiert fail-closed.

## Reale Chat-Startverdrahtung

1. Aktuellen Upload als `WORDPRESS_INTAKE.json` unter genau einem neuen `real_runs/k0/<job-id>/` binden.
2. Recherche und Schreiben nach den unveränderten K0-Regeln ausführen.
3. Fertigen Text samt gebundenem Produktionskontext als `ARTICLE_PACKAGE.json` im selben Job ablegen.
4. **Erst zuletzt** `START.json` mit Vertrag `K0_CHAT_START_V1` anlegen.
5. Dieser Push startet ausschließlich `.github/workflows/k0-production-e2e.yml`.
6. Workflow führt automatisch aus:
   `Portalzuordnung -> K0-Struktur/Tabelle -> PPM 6.7.9 -> LT 6.8 -> SYSTEM4_WORDPRESS_HANDOFF_V1 -> Export-Verifikation -> Chat-Artifact`.
7. Nach SUCCESS das Artifact `k0-chat-delivery-<run_id>` herunterladen.
8. Aus diesem Artifact ausschließlich `K0_WORDPRESS_DIRECT_IMPORT_<batch_sha256>.json` an den Nutzer ausgeben.

Keine Zwischenantwort vor fertiger Datei. Ein echter Terminalblocker darf gemeldet werden.

## Echter WordPress-Vertrag

- Vertrag: `SYSTEM4_WORDPRESS_HANDOFF_V1`
- geprüfte Importer-Version: `Portal SEO Redaktionsplan Compiler 0.28.27`
- PPM: `6.7.9`
- `direct_wordpress_upload_ready=true`
- `publish_allowed=false`

Der alte `SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2` ist **kein** direkter WordPress-Endvertrag und darf nicht als fertige Importdatei ausgegeben werden.

## Qualität

Keine Qualitätsregel lockern. Keine Performanceverbesserung zurücknehmen. K9 und K10 bleiben unverändert.

## Autorität

Repository: `hallo-netizen/affiliate-pferdeportal`

Branch: `konzept0-portal-neutral-20261002`

Current: `K0_CURRENT_STATE.json`

Portalregister: `K0_PORTAL_REGISTRY.json`

Startworkflow: `.github/workflows/k0-production-e2e.yml`

Exporter: `engine/k0_wordpress_export.py`

Gate: `engine/k0_production_gate.py`
