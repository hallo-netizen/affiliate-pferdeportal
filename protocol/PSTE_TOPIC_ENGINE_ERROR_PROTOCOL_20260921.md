# PSTE Fehlerprotokoll – 2026-09-21

Rolle: Fehlerhistorie/Nachweis. **Keine CURRENT-Autorität.**
Aktueller Status und genau eine NEXT ACTION stehen ausschließlich in `control/pste-topic-engine/CURRENT_STATE.json`.

## PSTE-ERR-REAL-001 – Live 0.57.1 blieb in STEP_OVERDUE
- Beobachtung: reale WordPress-Installation zeigte nach Start sowohl beim Einzellauf als auch bei der Produktionswelle `PSTE_DRIVER_STEP_OVERDUE`.
- Wirkung: frühere GitHub-/In-Process-PASS-Belege waren kein ausreichender Live-Systembeweis.
- Status: als ursprünglicher Live-Fail belegt; der echte WordPress-Hobbyraum reproduziert inzwischen die komplette HTTP-/Multiworker-Ausführung und hat den aktuell tieferen Parallelitäts-/Persistenzfehler sichtbar gemacht.

## PSTE-ERR-REAL-002 – alter WordPress-E2E Seed scheiterte vor Driver
- Fehler: Sandbox-Initialzustand/Record-Store-Hash im alten 0.57.0-Testaufbau.
- Status: Testaufbau korrigiert; aktueller Hobbyraum erreicht WordPress, Admin-AJAX, echten Einzellauf und Produktionswelle.

## PSTE-ERR-REAL-003 – nicht atomare Option-Lock-Freigaben
- Befund: mehrere Locks verwendeten Check-then-delete.
- Relevante Locks: Driver, Breadth, Research-Step sowie weitere Option-Locks.
- Reparatur im Hobbyraum: atomare DB-Löschung mit Owner-/Value-Bindung; Build-Postconditions brechen ab, wenn alte unsichere Driver-/Step-/Queue-Löschpfade verbleiben.
- Ergebnis: echter Einzellauf bleibt PASS; Race-Häufigkeit wurde verändert/reduziert, aber Produktionswelle bleibt nicht vollständig sauber.
- Status: Teilursache behoben, nicht aktueller erster Blocker.

## PSTE-ERR-REAL-004 – AKTUELL OFFEN: veralteter Job-Snapshot wird erneut verarbeitet
Autoritative Evidence:
- Branch: `pste-05700-server-step-driver-proof`
- letzter relevanter technischer Head: `f2cc6c058b0a52b4cf3df77cd83dd1144a63849a`
- Workflow: `PSTE Real WordPress HTTP E2E`
- Run: `35595789702`
- Ergebnis: FAILURE ausschließlich im Schritt `Positive production wave 40 through real admin-ajax and real loopbacks`
- Evidence artifact digest: `sha256:9be70b2ad78b811f90115e6be69c05cabc1075c02242233f621b5bcd617b8fe7`
- Hobbyroom candidate: `0.57.2-HOBBYROOM`
- Candidate SHA-256: `49d972e1569e5d6cd09668a2817265c53ddf39d32a10c72cfea35830abb39da3`

### Positiv belegter Teil
- echter WordPress/MySQL/Multiworker-Aufbau: PASS
- echter Admin-Login/Nonce: PASS
- manueller Einzellauf über echtes Admin-AJAX + echte Loopbacks: `PASS_REAL_WORDPRESS_SINGLE`
- Einzellauf: 15 Kandidaten, 5 direkt nutzbar
- Providerzählung Einzellauf exakt: 1× keyword_suggestions, 1× related_keywords, 1× keyword_ideas, 1× PAA POST, 1× tasks_ready, 1× PAA GET
- Produktionswelle erreicht fachlich `TARGET_REACHED`: 40 nutzbare / 84 rohe Kandidaten, 28 Items, 22 COMPLETE, 6 BLOCKED_PARKED.

### Aktueller echte Fehler
Der finale Breadth-Verifier bricht mit
`PROVIDER_COUNT_MISMATCH_/v3/dataforseo_labs/google/keyword_suggestions/live_27_22`
ab.

Mindestens ein fachlich unerwarteter Fehler ist im selben Lauf belegt:
- Familie: `Boxenmatten`
- job_uuid: `4ef084fb-24b6-4675-aa55-c43197941eee`
- park_reason: `PSTE_COST_LEDGER_ATTEMPT_MISMATCH`

Chronologie dieses ersten belegten Cost-Mismatch:
1. `RELATED_KEYWORDS:PERSISTING` verbucht `actual=0.001` korrekt.
2. Job schreitet zu `KEYWORD_IDEAS`, danach zu `QUESTIONS:IDLE`.
3. Job wird anschließend zu `QUESTIONS:TASK_PENDING` gespeichert.
4. Danach schreibt ein neuer Request denselben Job wieder als **älteren Zustand** `RELATED_KEYWORDS:PERSISTING`.
5. Derselbe Endpoint `related_keywords` wird erneut mit `actual=0.000` gegen bereits gespeicherte `actual=0.001` verbucht.
6. Der Cost-Ledger-Hardlock blockiert korrekt mit `PSTE_COST_LEDGER_ATTEMPT_MISMATCH`.
7. Erst **danach** wird der `PAUSED_ERROR`-Job durch `deleteIfSame()` aus der aktiven Option entfernt.

Damit ist belegt:
- das Löschen der aktiven Job-Option ist beim ersten Cost-Mismatch **Folge**, nicht Ursache;
- das Cost-Ledger ist Wächter, nicht Primärursache;
- der aktuelle erste offene Fehler ist die Quelle des veralteten Job-Snapshots, der trotz vorhandener Driver-/Queue-/Job-Locks erneut verarbeitet wird.

### Noch NICHT bewiesen
- welcher konkrete Read-Pfad den veralteten Snapshot liefert;
- ob er vor oder nach Lock-Erwerb gelesen/gecached wird;
- ob weitere Provider-Count-Abweichungen dieselbe Ursache haben.
Keine Vermutung als Root Cause übernehmen.

## Nicht als Fehler werten
Im Run wurden fünf weitere Items mit `PSTE_CATEGORY_EXHAUSTION_NOT_PROVEN` geparkt. Diese sind fachliche Fail-Closed-Ergebnisse und werden **nicht** ohne eigenen Beweis als Ursache des aktuellen Systemfehlers gewertet.
