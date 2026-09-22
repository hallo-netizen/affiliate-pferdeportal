# FIRST CODEX RUN – B01-ONLY – 2026-09-06

ROLLE: exakter technischer Ablauf für den ersten neuen Live-/Codex-Lauf.
Kein Ersatz für Zielvertrag/Fehlerquelle.

## VORBEDINGUNGEN

Der Lauf darf erst beginnen, wenn:
1. Nutzer den Merge von PR #141 ausdrücklich freigegeben hat.
2. PR #141 regulär in `main` integriert wurde.
3. neuer current-main-SHA frisch gelesen und dokumentiert wurde.
4. der permanente Chat→Codex-Dispatcher #107 wieder exakt auf diesen current-main-SHA zeigt.
5. kein anderer paralleler technischer Schreiber am selben Produktionsweg arbeitet.

Vor Freigabe: KEIN Merge, KEIN Live-Lauf.

## START

Ausschließlich bestehender produktiver Weg.
Keine neue Route, kein Canary, kein neuer Runner.

Im gebundenen Codex-Checkout zuerst:
1. current HEAD == erwarteter current `main`;
2. `python3 control/startmaster0107/codex-production-runtime/codex_environment_preflight.py`;
3. `python3 control/output-quarantine/runtime_entry_gate.py start`;
4. danach ausschließlich:
   `python3 control/single-door-boundary/codex_current_action.py current`

Wenn `CURRENT_BOUND_ACTION_READY`:
- exakt die bestehende gebundene Arbeitsanweisung ausführen;
- nur current_item;
- keine Alternativroute;
- kein separater Executor;
- keine Capability-Suche;
- keine Fach-/Inhalts-/Regeländerung;
- keine WordPress-Schreibaktion.

## STOP-REGEL

Beim **ersten** echten `BLOCKED` oder `USER_ACTION_REQUIRED`:
SOFORT STOP.

Nicht:
- zweiten Fehler suchen;
- weitere Korrekturen vorbereiten;
- mehrere Punkte gleichzeitig ändern;
- alten Fehler automatisch wieder aufrollen.

Nur erfassen:
1. exakter Fehlerstring;
2. exakter Schritt/Funktion;
3. aktueller main-SHA;
4. current_item / plan_slot;
5. ob B01 passiert wurde;
6. letzte erfolgreich durchlaufene technische Stelle;
7. vorhandene Evidence-/Report-Refs.

## ERWARTETE BEOBACHTUNG NACH B01

Wenn #141 wirkt, darf der alte Blocker
`BOUND_WORDPRESS_CATEGORY_ID_MISSING_FOR_REAL_PPM679_EXECUTION`
nicht erneut an derselben Stelle auftreten.

Dann wird ausschließlich der **erste neue reale Zustand** bewertet.

Post-B01-Reihenfolge:
1. `nd_seed_terms([$seedItem])`;
2. Fact-Pack-Import;
3. Source-Hash-Bindung;
4. Einzel-`production_plan_v4`;
5. `PSERC_PPM_Intake_Bridge::execute`;
6. PPM-Normal-Draft-Pipeline;
7. PPM-Report/Technical/Content-Quality;
8. finaler Content-Hash;
9. PPM-Stage-Proof;
10. FACHWORKFLOW_PASS;
11. ITEM_RECEIPT.

Pauls technische Findings werden nur dann herangezogen, wenn der reale Blocker in den dazu passenden inneren PPM-/Gate-Schritt fällt.

## ERFOLGSKRITERIEN

### B01-PASS
B01 ist erst live überwunden, wenn der Lauf die bisherige Kategorie-ID-Stelle real passiert.

### Artikel-1-PASS
Erst wenn Artikel 1 vollständig durch echten PPM + PASS/Receipt abgeschlossen ist.

### 7/7-PASS
Alle sieben Artikel auf exakt demselben current-main-Stand.

### SYSTEM-WIEDERHERGESTELLT
Erst wenn derselbe 7er-Batch auf demselben Stand 107008 erreicht und dort PASS ist.

Regression-/Hardlock-/Prinzip-PASS ist kein Ersatz für diese Ebenen.

## VERBOTENE SCHLÜSSE

- „#141 ist grün, also Live gelöst“ → verboten.
- „B01 ist vorbei, also letzter Fehler behoben“ → verboten.
- „Pauls Befund passt theoretisch, also jetzt fixen“ → verboten.
- „M01–M33 war auf #140 PASS, also #141 live sicher“ → verboten.

## RÜCKKEHR BEI FEHLER

Kein automatischer Rollback.
Wenn der neue Blocker eindeutig durch #141 selbst verursacht wird, Ursache zuerst hart belegen.
Rücknahme/Merge-Revert nur mit ausdrücklicher Nutzerfreigabe.

## REFERENZEN

- `PRE_CODEX_READINESS_20260906.md`
- `PAUL_PIPELINE_AUDIT_20260906.md`
- `HOBBYRAUM.md`
- autoritative Fehlerquelle über `FEHLERREGISTER.md`
- aktiver Zielvertrag über `ZIELVERTRAEGE/REGISTER.md`
