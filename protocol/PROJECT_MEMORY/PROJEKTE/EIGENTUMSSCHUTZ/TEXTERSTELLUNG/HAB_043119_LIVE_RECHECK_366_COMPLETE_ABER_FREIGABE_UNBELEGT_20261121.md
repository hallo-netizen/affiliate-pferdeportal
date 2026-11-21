# Hab & Bewahr 0.4.31.19 – Live-Recheck abgeschlossen, Ergebnisprüfung offen – 21.11.2026

**Originaldatei:** `texterstellung-diagnose-20261121-174035.json` (UTC 17:40:35), produktive WordPress-Version `0.4.31.19`.

## Tatsächlich nachgewiesen
- Original-Existing-Only-Warteschlange: `COMPLETE`; `local_backlog_processed=366`, `local_backlog_total=366`, `last_error=""`; Abschluss der Queue 17:25:41 UTC.
- Original-Worker: `IDLE`, `PSTE_DRIVER_NO_ACTIVE_WORK`, kein Fehler oder aktiver Lock.
- `provider_fallback_allowed=false`: Auftrag durfte keine bezahlten Fallback-Abfragen starten. Kein Nachweis neuer Providerkosten in dieser Diagnose.
- `local_backlog_title_candidates=0` und `local_backlog_reviews=0`; **diese Felder sind ausschließlich neu erzeugte Titelkandidaten bzw. neu überprüfte bereits vorhandene Reviews**, nicht Gesamtzahl fachlich freigegebener Keywords oder aller unklaren Begriffe.

## Wichtige Lücke im derzeitigen Diagnose-Export (Quellcode im 0.4.31.19-ZIP geprüft)
`includes/class-txe-diagnose.php` gibt beim Existing-Only-Block nur `title_candidates`, `reviews`, `processed`, `total` aus. Die **vom Original-Code gespeicherten Werte** `local_backlog_promoted`, `usable_candidate_count`, `completion_reason`, `local_backlog_retained_non_producing` fehlen im Report. Daher kann aus dieser Datei nicht abgeleitet werden, ob und welche der 366 Bestandszeilen fachlich jetzt freigegeben wurden. `items=[]` bedeutet nur, dass die aktuelle Existing-Only-Queue keine neuen Kategorie-Recherchejobs enthält; **keine Behauptung, alte RAW-Keywords seien gelöscht.**

Die frühere Behauptung `0 Titelkandidaten = 0 brauchbare Keywords` ist unzulässig. Es gab zuvor 192 RAW-/163 gespeicherte Kandidaten der Abholbox; 366 bezieht sich auf den gesamten gespeicherten Backlog, nicht allein Abholbox.

## Nächster Schritt (keine weitere Bezahlung, kein K0)
Den bestehenden Original-Pool beziehungsweise Original-MINI-Leser **nur lesend** auf aktuelle positive Entscheidungen und Ablehnungsgründe prüfen; die Diagnose allein bietet dafür keinen hinreichenden Nachweis. **Keinen zweiten Bestandslauf starten, keine kostenpflichtige Recherche, keine neue Pluginversion aufgrund dieser Diagnose ohne Ergebnisprüfung.**
