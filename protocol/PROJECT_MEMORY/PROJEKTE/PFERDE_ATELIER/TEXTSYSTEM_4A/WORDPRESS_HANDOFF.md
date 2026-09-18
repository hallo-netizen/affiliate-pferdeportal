# TEXTSYSTEM 4A – WORDPRESS-HANDOFF / REALER IMPORTER 0.28.23

STAND: 2026-09-13
STATUS: FRISCH GEPRÜFT

## Geprüfte Quelle

Library-Datei:
`portal-seo-editorial-plan-compiler_0.28.23_SYSTEM4_DIRECT_IMPORT.zip`

ZIP SHA-256:
`22a8459b64db488852841d894d887ec51e531a0872ee5f33afdd64e43a8a8c7f`

Geprüfte Importklasse:
`portal-seo-editorial-plan-compiler/includes/class-pserc-system4-import.php`

Datei SHA-256:
`2fbcd2f4451d553cd440848cc45ccbf1d1fbe877fe213a258e1c15251fc84f61`

Plugin-Header:
`Version: 0.28.23`

## Eingang vor der Textproduktion

Der reale Metadatenvertrag `PSERC_TEXTMACHINE_METADATA_BATCH_V2` erlaubt pro Artikel exakt fünf skalare Felder:

- `title`
- `target_keyword`
- `category`
- `article_type`
- `plan_slot`

Zusätzlich gilt auf Batchebene:
- `publish_allowed=false`;
- `content_or_format_payload_present=false`;
- `maximum_articles=0`;
- `maximum_articles_per_type=0`.

`0` bedeutet ausdrücklich unbegrenzt.

Inhalts-, Format-, Design-, Fact-Pack- und Promptfelder sind an dieser Grenze ausdrücklich verboten. Damit kann der vorgelagerte SEO-/WordPress-Prozess weder Text noch Design noch Codex-Routing steuern.

## Finaler System-4-Importvertrag

Der Importer 0.28.23 akzeptiert:
- Legacy: `SYSTEM4_7_ARTICLE_CHAT_HANDOFF_V1`;
- aktuell generisch: `SYSTEM4_WORDPRESS_HANDOFF_V1`.

Der generische Vertrag ist der Zielvertrag. Der Legacy-Name ist kein Ziel für die bereinigte Produktion.

Top-Level-Pflichtfelder:
- `contract`
- `batch_sha256`
- `publish_allowed`
- `signing_deferred`
- `batch_gate_status`
- `no_legacy_status`
- `test_suite_status`
- `wordpress_review`
- `articles`

Pflichtzustände:
- `publish_allowed=false`;
- `signing_deferred=true`;
- `batch_gate_status=SYSTEM4_BATCH_FULL_PASS_COLLECTED`;
- `no_legacy_status=PASS`;
- `test_suite_status=PASS`;
- `wordpress_review.file_format=JSON`;
- `wordpress_review.mime_type=application/json`;
- `wordpress_review.intended_next_step=WORDPRESS_DIRECT_IMPORT`;
- `wordpress_review.direct_wordpress_upload_ready=true`;
- `wordpress_review.direct_upload_block_reason=null`;
- `wordpress_review.required_downstream_components=[]`;
- `wordpress_review.ppm_version_verified_against=6.7.9`.

## Pflichtfelder pro Artikel

- `index`
- `title`
- `target_keyword`
- `category`
- `article_type`
- `plan_slot`
- `final_draft_sha256`
- `revision_count`
- `body`
- `production_context`
- `languagetool`
- `ppm679`

Der Importer verlangt **mindestens einen Artikel**, besitzt an dieser Stelle aber keine feste 7er-Obergrenze.

`article_type` wird nicht auf `Beratung` festgelegt. Er muss stattdessen mit dem gebundenen Produktionskontext und dessen Runtime-Daten exakt übereinstimmen.

## Prüfung vor dem ersten WordPress-Write

Für **alle** Artikel wird zuerst vollständig geprüft:
- Kategorie-Slug existiert als reale WordPress-Kategorie;
- aufgelöster Kategorie-Slug stimmt byte-/wertgleich;
- kanonischer Post-Slug ist im gebundenen `production_plan_item.runtime_order.slug` vorhanden;
- Slug ist bereits kanonisch sanitisiert;
- keine Kollision über `plan_slot`;
- keine Kollision über Slug;
- keine normalisierte Titelkollision.

Erst wenn der komplette Stapel diese Preflightprüfung bestanden hat, beginnt das Schreiben.

## WordPress-Ausgabe

Jeder Artikel wird als:
- `post_type=post`
- `post_status=draft`
- gebundene reale Kategorie-ID
- gebundener Titel
- final geprüfter Body
- gebundener Slug

geschrieben.

Wesentliche Metadaten:
- `_pserc_system4_import=1`
- `_pserc_system4_contract`
- `_pserc_system4_batch_sha256`
- `_pserc_system4_plan_slot`
- `_pserc_system4_content_sha256`
- `_pserc_system4_article_type`
- `_pserc_system4_target_keyword`
- `_pserc_system4_revision_count`
- `_pserc_publish_blocked=1`
- `_ppm679_normal_draft=1`
- `_ppm679_content_hash`
- `_ppm679_article_type`
- `_ppm679_publish_blocked=1`
- `_ppm679_category_slug`

## Readback / Rollback

Nach jedem Write wird WordPress wieder ausgelesen und geprüft:
- Draftstatus;
- Post-Type;
- Titel;
- Slug;
- SHA-256 des gespeicherten Contents;
- Kategorie-ID;
- alle Importmetadaten.

Bei einer Abweichung werden bereits im aktuellen Import erzeugte Posts wieder gelöscht.

Der Importer liest oder verändert den SEO-Redaktionsplan dabei ausdrücklich nicht:
- `redaktionsplan_read_attempted=false`
- `redaktionsplan_write_attempted=false`
- `publish_allowed=false`.

## Konsequenz für Konzept 4 / 4a

Der WordPress-Ausgang braucht **keine neue 4a-Schnittstelle**. 0.28.23 besitzt bereits den universellen Zielvertrag.

Die bereinigte Produktionsmaschine muss nur exakt `SYSTEM4_WORDPRESS_HANDOFF_V1` erzeugen. Keine zusätzliche Signatur-, Receipt-, Room- oder Umwandlungsstufe ist dafür erforderlich.
