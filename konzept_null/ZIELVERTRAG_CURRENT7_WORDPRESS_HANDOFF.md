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
- aktueller Direktimportvertrag: `SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2`;
- gebundener Direktimport-Validator: Portal SEO Editorial Plan Compiler 0.28.23;
- `publish_allowed=false`;
- kein WordPress-Write und kein Publish durch Konzept Null;
- finale Pflichtausgabe an den Nutzer ist genau die kanonische `SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2.json`.

## Erfolgskriterium
PASS nur wenn auf exakt denselben Artikelbytes:
1. 7/7 LanguageTool 6.8 = 0 Findings;
2. 7/7 PPM 6.7.9 = TECHNICAL_CHECK_OK + CONTENT_QUALITY_CHECK_OK + aggregate PASS;
3. der originale 0.28.23-System-4-Handoff-Validator die kanonische Datei akzeptiert;
4. der falsche alte Top-Level-Contract negativ blockiert wird;
5. die kanonische Datei als Chat-/Download-Artefakt verfügbar ist;
6. kein Publish erfolgt.
