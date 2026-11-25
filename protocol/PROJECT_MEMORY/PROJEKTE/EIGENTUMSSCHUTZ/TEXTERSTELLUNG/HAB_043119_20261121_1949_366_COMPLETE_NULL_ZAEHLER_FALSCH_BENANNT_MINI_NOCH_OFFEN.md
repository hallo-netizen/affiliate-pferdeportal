# Hab & Bewahr 0.4.31.19 – 21.11.2026 19:49 CET – Kostenfreier Recheck ist technisch COMPLETE; Freigabe noch NICHT bewiesen

## Beweismittel
- Nutzer-Screenshot `Bildschirmfoto 2026-11-21 um 19.49.38.png`
- Diagnose `texterstellung-diagnose-20261121-184945.json` (UTC 18:49:45), mit voriger `texterstellung-diagnose-20261121-174035.json` verglichen.
- Die beiden Diagnosen sind bei Original-Recheck-Zustand unverändert: `COMPLETE`, `processed=366, total=366, cursor=927, title_candidates=0, reviews=0, last_error=""`, `provider_fallback_allowed=false`, Driver `IDLE`, Abschluss 17:25:41 UTC. Keine weitere Aktivität zwischen den Exporten belegt.

## Quellcodebeleg aus installierter 0.4.31.19
- `texterstellung.php` 2317–2318 labelt `local_backlog_title_candidates` als **„Fachliche Kandidaten“** und `local_backlog_reviews` als **„zur Klärung“**. Beide bedeuten laut der Originalqueue nur neu generierte Titelkandidaten bzw. revalidierte zuvor gespeicherte Reviews, NICHT alle fachlich JA/unklar aus der Neuprüfung.
- `class-pste-breadth-research-queue.php` 703 hat getrennte Werte `local_backlog_promoted`, `usable_candidate_count`, `local_backlog_retained_non_producing`, `completion_reason`; diese werden durch `includes/class-txe-diagnose.php` 641ff nicht ausgegeben.
- `class-pste-repository.php` 3027ff bearbeitet die bestehenden Daten mit `PSTE_Normal_Metadata_Path::applyToPayload`; auch Nicht-PASS-Ergebnisse werden in `persistFreshRetainedNonPass` mit Readback geschrieben. Der Zähler 366 ist technisch real, nicht Beleg erfolgreicher Freigaben.
- `texterstellung.php` 866ff `appendOriginalProvenResearch` nimmt ausschließlich anhand positiver signierter aktueller `normal_metadata_path.portal_relevance_gate`-Belege in den MINI-Export auf. Es wertet **nicht** die zwei angezeigten Nullzähler aus. Bei `seoExport` 1094 wird `NO_PROVEN_JA_KEYWORDS_FOR_MINI` gemeldet, wenn keine positive Freigabe existiert. MINI hat eigene Bestandsvoraussetzungen, daher noch kein Abschlussbeweis.

## Ergebnis / KISS
**Belegt:** Der frühere Worker-Stillstand ist technisch behoben. Alle 366 gespeicherten Topic-Pool-Zeilen wurden verarbeitet, Original-Queue COMPLETE, 0 Provider-Fallback. Keine neue DataForSEO-Abfrage erforderlich.
**Nicht belegt:** Die Anzahl tatsächlich relevanter `JA`-Keywords bzw. die erfolgreiche Aufnahme eines konkreten Hab-Keywords in MINI. „0 Fachliche Kandidaten“ ist eine missverständliche Falschbeschriftung, **kein Beweis**, dass 0 Keywords relevant seien.
**Nächster Prüfungsschritt ohne Plugin:** Ein einzelner `MINI-Export` (Anzahl=1, wenn kein Alt-MINI-Auftrag existiert) prüft den bestehenden echten Leser. Erfolgreich: ein konkret belegtes Keyword im ausgegebenen MINI-Dokument. Fehler `NO_PROVEN_JA_KEYWORDS_FOR_MINI`: reale positive Freigabe fehlt, Ursachen dann am originalen Pool untersuchen. Vorher keine Version, kein Recheck, keine paid DataForSEO-Recherche. **K0 nicht anfassen**.
