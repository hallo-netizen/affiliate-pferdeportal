# STARTMASTER0107 — REAL7 Live-Protokoll Pflicht vor Start

Stand: 19.09.2026

## Zweck

Dieser Vertrag gilt ausschließlich für den jetzt ausdrücklich freigegebenen echten 7-Artikel-Codex-Lauf.

## Harte Regel bei Codex-Nutzungslimit oder anderem Abbruch

Kein bereits erreichter Fortschritt darf nur in /tmp, einem ephemeren Codex-Workspace oder einem nicht dauerhaft erreichbaren Task-Output verbleiben.

Nach jedem fachlich relevanten Zustandswechsel muss dauerhaft protokollierbar sein:

- aktueller Main-SHA und Dispatcher-Head;
- Batch-ID / Batch-SHA;
- Artikelindex und plan_slot;
- Artikelidentität (Titel + Target-Keyword);
- aktueller Workspace / Same-Article-Bindung;
- aktuelle Phase;
- Revision;
- letzter Draft-/Artikel-SHA256, sofern vorhanden;
- LanguageTool-Status und Findings;
- PPM-6.7.9-Status und Findings;
- Repair-Owner;
- Anzahl der bisherigen Repair-Runden;
- ob der Artikel bereits echten PASS erreicht hat;
- ob der nächste Artikel gestartet wurde;
- Batch-Status;
- 107008-Status;
- Publish immer NO, solange keine separate Nutzerfreigabe vorliegt.

## Nutzungslimit

Wenn Codex wegen Nutzungslimit stoppt:

1. sofort keine neuen Artikel oder neue Repair-Schritte mehr starten;
2. den letzten vollständig erreichten Zustand dauerhaft protokollieren;
3. bereits erzeugte Artikelbytes/Beweisdateien dauerhaft sichern, soweit sie existieren;
4. exakt markieren:
   `CODEX_USAGE_LIMIT_REACHED_AFTER_ARTICLE_<index>_PHASE_<phase>`;
5. `completed_articles`, `current_article_index`, `current_revision`, `last_article_sha256`, `second_or_next_article_started` und `publish_performed=false` dokumentieren;
6. kein Gesamt-PASS behaupten.

## Werkstattprinzip

Reparierbare Qualitätsfehler sind kein Grundsatzblock.

`FAIL -> DRAFT_WORKER -> SAME ARTICLE / SAME WORKSPACE -> RECHECK`

Das wiederholt sich bis PASS oder bis ein wirklich nicht reparierbarer technischer Hardblock vorliegt.

## Reihenfolge

Artikel N+1 darf erst starten, wenn Artikel N real PASS ist.

## Verboten

- historische/Recovery-Artikelkörper als NEW-Schreibquelle;
- freier Direktstart außerhalb des kanonischen Einstiegs;
- Qualitätsgrenzen lockern;
- reparierbare Qualitätsfehler als terminalen Projektblock behandeln;
- nur flüchtige /tmp-Evidence als Abschlussnachweis;
- Auto-Publish oder WordPress-Schreibaktion ohne separate Nutzerfreigabe.
