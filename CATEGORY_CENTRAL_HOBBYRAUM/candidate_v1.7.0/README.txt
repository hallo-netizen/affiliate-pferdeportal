=== Affiliate-Portal Kategorie-Workflow ===
Version: 1.6.1
Status: FINALER HARDLOCK-TESTKANDIDAT
Plugin-Slug: affiliate-portal-kategorie-workflow
Master-Contract: ALLGEMEINGUELTIGER_KATEGORIE_MASTER_016_WORKFLOW_HARDLOCK

GLEICHE PLUGIN-LINIE
Kein Parallelplugin. DataForSEO bleibt ausschließlich Evidenz/Gate. Keine WordPress-/HivePress-Content-Writes.

CONTENT-ROOTFIX
Eine tragfähige Content-Kategorie benötigt mindestens 3 wichtige, eigenständige, node-gebundene DataForSEO-Longtails. FAQ, Tipps, Beratung, Vergleich, Ausrüstung/Werkzeug usw. dürfen selbst Content-Kategorien sein, wenn sie dasselbe Gate erfüllen. Einzelbeiträge liegen darunter.

WORKFLOW-HARDLOCK
1 MASTER LOCK -> 2 PROJECT CONTRACT -> 3 INITIAL TREE -> 4 INITIAL VISIBLE REVIEW -> 5 FREE PREFLIGHT -> 6 GLOBAL COVERAGE -> 7 GLOBAL GAP DECISION -> 8 GLOBAL GAP VISIBLE REVIEW -> 9 DETAIL PREFLIGHT -> 10 DETAIL RESEARCH -> 11 DATA-INFORMED CORRECTION -> 12 READ-ONLY TOTAL AUDIT -> 13 FINAL VISIBLE REVIEW -> 14 FINAL VALIDATION.

V1.6.1 ROOTFIX
- Jede der drei Nutzerfreigaben benötigt eine serverseitig HMAC-signierte Review-Quittung. Manuell injizierter Status/Hash ist BLOCKED.
- Jede Signierung benötigt zusätzlich den exakten Review-Scope-SHA-256 aus der sichtbaren Prüfung; falsches Paket = BLOCKED.
- Zielmarkt und Sprache sind Teil von Project-, Discovery-, Research- und Review-Scope.
- Global-/Research-Pakete werden auch nach neu berechnetem Außenhash blockiert, wenn Markt/Sprache nicht zum gebundenen Projektvertrag passen.
- Global-Coverage-Ähnlichkeit ist nur Hinweis; jeder relevante Core braucht eine explizite fachliche Entscheidung. DEFERRED blockiert.

SICHERHEIT
APKW_CONTENT_WRITE_CAPABILITY=false. Preflights/Finalaudit: 0 DataForSEO-Requests. Global: genau 1 bestätigter Paid Call. Detail: nur deklarierte Cluster + erforderliche Overview-Batches.
