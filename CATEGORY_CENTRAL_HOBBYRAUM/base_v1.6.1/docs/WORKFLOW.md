# Workflow V1.6.1 – HARDLOCK

Verbindlich und ohne alternative Reihenfolge:
1. MASTER LOCK – exakt `ALLGEMEINGUELTIGER_KATEGORIE_MASTER_016_WORKFLOW_HARDLOCK`.
2. PROJECT CONTRACT – Konzept, Scope, Ausschlüsse, Zielmarkt, Sprache, Discovery-Seeds.
3. INITIAL TREE – vollständige drei Säulen.
4. INITIAL VISIBLE REVIEW – kompletter Baum sichtbar; exakter Scope-Hash; serverseitig signierte Nutzerquittung.
5. FREE PREFLIGHT – 0 externe Requests.
6. GLOBAL COVERAGE – exakt 1 ausdrücklich bestätigter Paid Keyword-Ideas-Call.
7. GLOBAL GAP DECISION – jeder relevante Core: MAIN_TOPIC, SUBTOPIC, ARTICLE_ONLY oder OUT_OF_SCOPE; DEFERRED blockiert; Ähnlichkeit entscheidet nie.
8. GLOBAL GAP VISIBLE REVIEW – korrigierter Gesamtbaum + Entscheidungen sichtbar; exakter Scope-Hash; serverseitig signierte Nutzerquittung.
9. DETAIL PREFLIGHT – 0 externe Requests.
10. DETAIL RESEARCH – 1 Keyword-Ideas-Call je freigegebenem Cluster + nur notwendige Overview-Batches; Global wird wiederverwendet.
11. DATA-INFORMED CORRECTION – Chat/Master verbindet Konzept, Baum und Evidenz; DataForSEO verändert Architektur nie autonom.
12. READ-ONLY TOTAL AUDIT – Hierarchie, Evidenz, Longtails, Ownership, Kannibalisierung, Bestand; 0 externe Requests, 0 Content-Writes.
13. FINAL VISIBLE REVIEW – vollständiger finaler Drei-Säulen-Baum sichtbar; exakter Scope-Hash; serverseitig signierte Nutzerquittung.
14. FINAL VALIDATION – nur unveränderter Scope + alle Gates PASS => PASS_FINAL_APPROVED.

## Keine Selbstfreigabe
Review-Status und Review-Hash allein sind wertlos. Jede Review-Quittung ist mit dem WordPress-Auth-Salt HMAC-signiert und an Master-Contract, Stufe, Scope-Hash, Zeit, Zusammenfassung und freigebenden Benutzer gebunden. Der Admin-Signierpfad verlangt `manage_options`, Nonce, explizite Bestätigung und den exakten sichtbaren Review-Scope-Hash.
