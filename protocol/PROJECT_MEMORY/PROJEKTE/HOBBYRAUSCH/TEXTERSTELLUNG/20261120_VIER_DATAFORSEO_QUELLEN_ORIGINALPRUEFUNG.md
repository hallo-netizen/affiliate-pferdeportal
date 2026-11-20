# Hobbydepot – Beweisprüfung der vier DataForSEO-Recherchewege (20.11.2026)

## Quellprüfung (read-only)
Die tatsächlich gespeicherten Originalpakete **Hobbydepot Texterstellung 0.4.24.13** und **Pferdeatelier Texterstellung 0.4.34** enthalten jeweils `PSTE_Research_Job::VERSION='2.6.0'`. In beiden ist die Phasenkette:
`KEYWORD_SUGGESTIONS → RELATED_KEYWORDS → KEYWORD_IDEAS → QUESTIONS [PAA] → FINALIZE`.
- Suggestions: `PSTE_DataForSEO_Client::keywordSuggestionsDriverStep`, Original-Labs-API `keyword_suggestions/live`
- Related Keywords: `relatedKeywordsDriverStep`, Original-Labs-API `related_keywords/live`
- Ideas: `keywordIdeasDriverStep`, Original-Labs-API `keyword_ideas/live`. Die originale `discoverySeeds` zieht echte Anbieterergebnisse von `KEYWORD_SUGGESTION` **und** `RELATED_SEARCH` (max. 20 Auswahlbegriffe); keine nachträglich erfundene Keyword-Idee.
- People Also Ask: `QUESTIONS` über Original-Task `postPeopleAlsoAskTask` (`/v3/serp/google/organic/task_post`) und spätere Statusabfrage `task_get/advanced/{id}`; Speicherung als `sources.PAA`; maximal vier Klicktiefen.
- `finalize` verweigert Abschluss bei fehlendem `KEYWORD_SUGGESTION`, `RELATED_SEARCH`, `KEYWORD_IDEA` oder `PAA`; in Version 2.6.0 muss zusätzlich `questions_state=COMPLETE` vorliegen.

## Tatsächlich ausgeführte Originalmethoden
PHP-CLI via Reflection ohne Providerkontakt: Original `providerMeta` für alle vier Phasen und Original `discoverySeeds` aus gemischten Suggestions-/Related-Quellen und leeren Quellen. Ergebnis: **6 von 6 PASS je Portal** (insgesamt 12 PASS), inklusive erfolgreicher Seedverarbeitung aus beiden vorangegangenen Quellen. Die beiden Originalpakete unterscheiden sich als Datei, erfüllen aber jeweils dieselben geprüften Schritte.

## Beweisgrenze
Der Nutzerdiagnose-Export vom **20.11.2026 08:21:11 UTC** meldet `original_research.queue_status=RUNNING`, `items=[]`. Er enthält **keine erfolgreichen Providerphasen-Quittungen** für den aktiven Live-Auftrag. Die früheren PAA-Recovery-Events allein beweisen keine vollständig gelaufene vierteilige aktuelle Recherche. Kein echter DataForSEO-POST durch diese Prüfung, keine Kosten, kein WordPress-Eingriff.

**Konsequenz:** Die vier Recherchewege müssen nicht neu entwickelt werden. Zuerst den bereits laufenden Original-Research-Job ohne neue bezahlte Anfrage zum belegten Abschluss führen; erst danach MINI→K0 live nachweisen.
