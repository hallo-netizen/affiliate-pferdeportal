# STARTMASTER0107 — REAL7 Live-Protokoll bei Nutzungslimit

Stand: 19.09.2026

## Zweck

Dieser Vertrag gilt ausschließlich für den ausdrücklich freigegebenen echten 7-Artikel-Codex-Lauf.

## Dauerhafte Mindestprotokollierung

Kein erreichter Fortschritt darf nur in /tmp, einem ephemeren Codex-Workspace oder einem nicht dauerhaft erreichbaren Task-Output verbleiben.

Nach jedem fachlich relevanten Zustandswechsel muss dauerhaft rekonstruierbar sein:

- aktueller Main-SHA und Dispatcher-Head;
- Batch-ID / Batch-SHA;
- Artikelindex und plan_slot;
- Titel und Target-Keyword;
- Same-Article-/Same-Workspace-Bindung;
- aktuelle Phase und Revision;
- letzter Draft-/Artikel-SHA256, sofern vorhanden;
- LanguageTool-Status und Findings;
- PPM-6.7.9-Status und Findings;
- Repair-Owner und Zahl der Repair-Runden;
- Artikel-PASS ja/nein;
- ob der nächste Artikel gestartet wurde;
- Batch-Status und 107008-Status;
- Publish bleibt NO ohne separate Nutzerfreigabe.

## Codex-Nutzungslimit

Wenn Codex wegen Nutzungslimit stoppt:

1. keine neue Artikel- oder Repair-Arbeit mehr beginnen;
2. den letzten vollständig erreichten Zustand dauerhaft protokollieren;
3. vorhandene Artikelbytes/Beweisdateien dauerhaft sichern;
4. exakt markieren:
   `CODEX_USAGE_LIMIT_REACHED_AFTER_ARTICLE_<index>_PHASE_<phase>`;
5. mindestens `completed_articles`, `current_article_index`, `current_revision`, `last_article_sha256`, `next_article_started` und `publish_performed=false` dokumentieren;
6. kein Gesamt-PASS behaupten.

## Werkstattprinzip

Reparierbare Qualitätsfehler sind kein terminaler Grundsatzblock:

`FAIL -> DRAFT_WORKER -> SAME ARTICLE / SAME WORKSPACE -> RECHECK`

Wiederholen bis PASS oder echter nicht reparierbarer technischer Hardblock.

## Reihenfolge

Artikel N+1 darf erst starten, wenn Artikel N real PASS ist.

## Verboten

- historische/Recovery-Artikelkörper als NEW-Schreibquelle;
- freier Direktstart außerhalb des kanonischen Einstiegs;
- Qualitätsgrenzen lockern;
- reparierbare Qualitätsfehler als terminalen Projektblock behandeln;
- nur flüchtige /tmp-Evidence als Abschlussnachweis;
- Auto-Publish oder WordPress-Schreibaktion ohne separate Nutzerfreigabe.
