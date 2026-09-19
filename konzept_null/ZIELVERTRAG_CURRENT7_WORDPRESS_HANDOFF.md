# ZIELVERTRAG – KONZEPT NULL / CURRENT7 WORDPRESS-HANDOFF

Status: VERBINDLICH

## Ziel
Konzept Null reproduziert den historischen, hart geführten Chat-Artikelworkflow ohne Codex für den aktuell gebundenen 7er-Batch und liefert am Ende genau **eine** vom aktuell gebundenen WordPress-Direktimportvertrag akzeptierte JSON-Datei.

## Verbindliche Bedingungen
- kein Codex;
- Chat schreibt die Artikel selbst;
- keine freien Workflow-Entscheidungen;
- Metadaten des gebundenen 7er-Batches bleiben unverändert;
- echte Recherche/Faktenbindung;
- echte LanguageTool-6.8-Prüfung;
- echte PPM-6.7.9-Prüfung;
- keine Text-/Qualitäts-/Designregel lockern;
- nach Full PASS keine inhaltliche Artikeländerung;
- aktueller Live-Importer: `Portal SEO Redaktionsplan Compiler 0.28.23`;
- der exakte Direktimportvertrag darf ausschließlich aus dem read-only exportierten Quellcode des aktuell installierten 0.28.23-Plugins abgeleitet werden; ein System-4-/Chat-Selbstvalidator ist keine Autorität;
- `SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2`, `PSERC_APPROVED_PRODUCTION_PACKAGE_V1` und `PSERC_APPROVED_PRODUCTION_TRIGGER_V3_SIGNED_SUBSET_SUPERVISED` sind als direkter Eingang bereits live negativ belegt und dürfen nicht erneut als finaler Upload ausgegeben werden;
- `publish_allowed=false`;
- kein WordPress-Write und kein Publish durch Konzept Null;
- finale Pflichtausgabe an den Nutzer ist genau eine JSON-Datei, die den aus dem aktiven 0.28.23-Quellcode extrahierten Vertrag erfüllt und lokal gegen diesen echten Importer positiv sowie mit gezielten Mutationen negativ geprüft wurde.

## Erfolgskriterium
PASS nur wenn auf exakt denselben Artikelbytes:
1. 7/7 LanguageTool 6.8 = 0 Findings;
2. 7/7 PPM 6.7.9 = TECHNICAL_CHECK_OK + CONTENT_QUALITY_CHECK_OK + aggregate PASS;
3. der read-only exportierte Quellcode des aktuell installierten WordPress-Plugins 0.28.23 als Importvertrags-Autorität gebunden ist;
4. exakt dieser echte Importer die finale Datei lokal positiv akzeptiert;
5. gezielte Negativmutationen gegen exakt denselben Importer blockieren;
6. die identische geprüfte Datei als Chat-/Download-Artefakt verfügbar ist;
7. kein Publish erfolgt.
