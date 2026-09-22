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


## PSTE-ERR-REAL-005 – Live-Paketpfad / Doppelinstallation / nicht identische Downloadbytes
- Reale WordPress-Pluginliste belegte den bestehenden Plugin-Basename `Portal SEO Topic Engine/portal-seo-topic-engine.php`.
- Eine zuvor erzeugte ZIP verwendete den Root `portal-seo-topic-engine`; WordPress behandelte sie dadurch als separate Plugininstallation statt als Ersatz des bestehenden Ordners.
- Reale Folge: zwei Pluginordner lagen parallel; nach Aktivierungs-/Umbenennungsversuchen war die Seite zeitweise nicht erreichbar. Wiederherstellung gelang durch Deaktivieren/Umbenennen der zusätzlichen Pluginordner; keine Datenlöschung als Reparatur.
- Der Paketbuild wurde danach auf den exakten Root `Portal SEO Topic Engine` umgestellt und negativ gegen falschen Lowercase-Root sowie verschachtelten Doppelroot geprüft.
- Neuer Real-WordPress-E2E-PASS: Head `9aa8b1e22679ef0e528e7cd45e9617c880dadd8a`, Run `35626042769`, Artifact `10652182930`, Artifact-Digest `sha256:24e7a54a7d962bd14637de7d2530feaef1d5682700340472e48d9d48b8326db1`.
- Exakt im PASS-Lauf getestete Plugin-ZIP: SHA-256 `962684fe7a3d3d22e677684ab69d9e23771c6000490071a3836993677c8ec2e0`.
- Kritischer Nachholbefund: die anschließend an den Nutzer ausgegebene ZIP mit SHA-256 `30e89d7afd683a2b8bddb5cb6fef1a21d32f5c29ce7ee4c1083e44c306020799` ist **nicht** byteidentisch mit der im PASS-Lauf getesteten ZIP und darf nicht als getesteter Releasekandidat gelten.
- Status: GitHub-/Real-WordPress-Hobbyraum PASS für die exakten `962684fe...`-Bytes; echter Nutzer-WordPress-Live-PASS mit genau diesen Bytes noch offen. PPA-005 CURRENT.zip darf bis dahin nicht ersetzt werden.


## PSTE-ERR-REAL-006 – 0.57.3 Live: FINALIZE PREPARE überschreitet Step-Grenze
- Echter Nutzer-Live-Lauf mit 0.57.3 erreichte Produktionswelle RUNNING.
- Sichtbarer Kindlauf: Datenquellen 3/3, Fragen COMPLETE, Abschluss PREPARE.
- Danach: Server-Driver BLOCKED / PSTE_DRIVER_STEP_OVERDUE.
- Codeprüfung der exakt getesteten 0.57.3-Bytes: PREPARE ruft PSTE_Runner::prepareResearchFinalizeJob() auf. Dort laufen vollständige Quellzusammenführung, Alias-/Deduplikatbildung, Familienprüfung je Gruppe, Kandidatenbau, interne Duplikatbehandlung, Titelharmonisierung, Work-Queue-Anbindung und Kandidatenpersistierung in einem einzigen Request.
- Befund: Der GitHub-E2E hat Funktion und Parallelität geprüft, aber diesen PREPARE-Schritt nicht mit live-repräsentativer Datenlast bewiesen.
- Verbotener Scheinfix: OVERDUE-/Timeout-Grenze erhöhen.
- Erforderlich: PREPARE selbst request-bounded und persistiert machen; danach kompletter Real-WordPress-Stresslauf.

## PSTE-ERR-REAL-007 – 0.57.3 Live: Produktionswellen-UI nach START blind bis Reload
- Nutzerbeobachtung: Nach Klick auf „Produktionswelle starten“ springt die Oberfläche nicht selbst in den aktiven Status; Fortschritt wird erst nach manuellem Neuladen sichtbar.
- Codebeweis: Wenn beim initialen Seitenrender keine aktive Breadth-Queue existiert, wird der HTML-Block mit IDs pste-breadth-status / progress / usable / blocked / detail gar nicht ausgegeben. Der AJAX-START setzt zwar queue=d.queue und ruft renderQueue(queue), aber die Zielelemente existieren in diesem DOM nicht.
- Folge: Server kann laufen, während die Oberfläche weiterhin den Startzustand zeigt; der Nutzer kann Arbeit vs. Hänger nicht zuverlässig erkennen.
- Erforderlich: Start- und Aktiv-UI beide rendern und nach START/Status ohne Reload umschalten; laufenden Child-/Finalize-Stand sichtbar halten.


## PSTE-ERR-REAL-008 – 0.57.4 Hobbyraum schließt PREPARE-/UI-Lücke unter Stress
- Ausgang: echter Nutzer-Live-Fail mit 0.57.3 bei FINALIZE PREPARE / PSTE_DRIVER_STEP_OVERDUE sowie blinde Produktionswellen-UI bis Reload.
- Produktänderung: FINALIZE PREPARE in persistierte, begrenzte Teilschritte zerlegt; Start-/Fortschritts-UI wird ohne Reload sichtbar und zeigt laufenden Finalize-Stand.
- Verschärfter Real-WordPress/MySQL/Multiworker-Test: Run `35645482192` — SUCCESS.
- Browser ohne Reload: `PASS_BROWSER_START_NO_RELOAD_LIVE_PROGRESS`.
- Stale Status nach neuem Start: `PASS_BROWSER_STALE_STATUS_IGNORED_AFTER_NEW_QUEUE_START`.
- PREPARE-Stress: 303 Kandidaten, nachweislich mehrere Requests, `PASS_STRESS_PREPARE_MULTI_REQUEST total=303`.
- Danach im selben Workflow normale Produktionswelle: `TARGET_REACHED`, 41 nutzbare / 79 rohe Kandidaten, 26 Items, 22 COMPLETE, 4 ausschließlich fachlich `PSTE_CATEGORY_EXHAUSTION_NOT_PROVEN` geparkt.
- Technische Parkfehler: 0. Providercounts exakt 25 je Stufe. Driver am Ende IDLE.
- Evidence Artifact: `10659823699`, Digest `sha256:f5da0cc4dde3cc5de1eed0ae64f6381f574f676b0792912c4082f015da2ff171`.
- Exakt getestete Plugin-ZIP: `PSTE-0.57.4-HOBBYROOM.zip`, SHA-256 `8695cc5514d19805db8025db7b92097493ed4a2218a0a71c87b090bf7ee0461c`.
- Status: Hobbyraum-PASS. Echter Nutzer-Live-PASS mit exakt diesen Bytes bleibt offen; keine PPA-005-Promotion vorher.


### Finaler Nachlauf derselben 0.57.4-Produktbytes
- Nach dem ersten vollständigen Stress-PASS wurde ausschließlich das Proof-Skript fail-fast gehärtet; kein Produktcode geändert.
- Finaler Real-WordPress-E2E: Run `35646020136` — SUCCESS.
- Finales Evidence Artifact: `10659844649`, Digest `sha256:76ca13601f85aba81fabd1eaa311fd20f6607264b4c18a0496aef3be055a0967`.
- Final exakt getestete ZIP: SHA-256 `ae4fde45bdd42310fae148777701f17067bd3eefde69b8acb54a526a7ccf64e3`.
- Die frühere 0.57.4-PASS-ZIP `8695cc55...` ist als Installationskandidat überholt; für den Live-Test gilt ausschließlich `ae4fde45...`.


## PSTE-ERR-REAL-009 – 0.57.6 schließt Safe-Cancel-/Fortsetzungs-Lücke im Hobbyraum
- Reale Ausgangsfehler: Live-Hänger in FINALIZE/PREPARE, sicherer Abbruch ließ Driver hängen, Neustart definierte den Wellenfortschritt neu und zeigte wieder 0/40.
- 0.57.5 entfernt die schwere Admin-Inventory-Hydration aus PREPARE und beweist Safe-Cancel im echten WordPress-E2E.
- 0.57.6 ergänzt ausschließlich die persistente Fortsetzung einer bewusst abgebrochenen Zielwelle: ursprüngliche PASS-Baseline bleibt erhalten; bereits erreichte PASS-Themen werden beim Neustart wieder eingezählt; abgeschlossene lokale Bestandsprüfung wird weiterverwendet.
- Finaler Real-WordPress/MySQL/Multiworker/Server-Cron-Lauf: `35693065234` — SUCCESS.
- Safe Cancel exakt in PREPARE: `PASS_CANCEL_PROOF_REACHED_PREPARE cursor=0 total=303` -> `PASS_SAFE_CANCEL_DURING_PREPARE_SETTLES_CLEANLY`.
- Fortschritt vor Abbruch: `usable=2 complete=1`.
- Neustart: `PASS_CANCELLED_WAVE_PROGRESS_CONTINUED old=2 new=2`; neuer Queue-Status trägt `continued_usable_candidate_count=2`, `local_backlog_complete=true`, `local_backlog_reused=true`.
- PREPARE-Stress danach: `PASS_STRESS_PREPARE_MULTI_REQUEST total=303`.
- Abschließende 40er Welle im selben Run: `TARGET_REACHED`, 40 nutzbare / 123 rohe Kandidaten, 27 Familien, Driver terminal IDLE, Provider-Stufen exakt 26.
- Exakt getestete ZIP: `PSTE-0.57.6-HOBBYROOM.zip`, SHA-256 `71bae2436fc1c3d52c06cefe551517af32a89eeb005457331e2c44136a1c888f`.
- Evidence Artifact: `10679790400`, Digest `sha256:dfb41d91aaa6b485bef8c0497e2ed6888dec514ce4144286177439fd282d3cab`.
- Status: Hobbyraum vollständig PASS; echter Nutzer-Live-PASS mit exakt diesen Bytes bleibt offen. Keine PPA-005-Promotion vorher.


## PSTE-ERR-REAL-009 – Live PREPARE vor erstem Cursor durch globales Workflow-Inventory überladen
- Live-Nachweis 0.57.4: `FINALIZE/PREPARE_CANDIDATES`, Cursor `0/96`, Driver/Queue/Step-Locks aktiv, anschließend `PSTE_DRIVER_STEP_OVERDUE`.
- Technische Ursache: `previousCandidateInventory()` erzeugte für PREPARE eine globale Kandidatenprojektion über `allCandidates()` inklusive Relation-Hydrierung. Für den konkreten Duplicate-/Readiness-Pfad besitzt jedoch nur die aktuelle Themenfamilie Entscheidungsautorität.
- Reparatur 0.57.5: familienbezogene Topic-Pool-Projektion; keine Occurrence-/Assignment-Hydrierung im Workflow-Inventory. Semantik wurde separat gegen Legacy-Projektion geprüft.
- Gegenprobe: PREPARE-Stress mit 303 Kandidaten läuft mehrschrittig vollständig durch; kein STEP_OVERDUE.
- Status: FIXED_AND_REPROVEN im finalen 0.57.6 Run `35693065234`.

## PSTE-ERR-REAL-010 – Sicherer Abbruch verlor Wellenfortschritt / Neustart bei Null
- Fehlerbild: bewusst abgebrochene Produktionswelle wurde bei erneutem Start als neue Baseline behandelt; bereits erzielte PASS-Themen und abgeschlossenes lokales Audit wurden nicht als Fortsetzung der gleichen Zielwelle übernommen.
- Reparatur 0.57.6: Fortsetzung nur für kompatible, bewusst `CANCELLED_BY_USER` beendete TARGET_USABLE_CANDIDATES-Welle mit identischem Target, Max-Items und identischer Context-Binding-Hashbasis. Ursprüngliche Baseline und lokaler Audit-Zustand werden übernommen.
- Positivbeweis: `PASS_CANCELLED_WAVE_PROGRESS_CONTINUED old=2 new=2`.
- Negativschutz: Fortsetzung wird bei abweichendem Status, Ziel, Max-Items oder Context-Binding verweigert.
- Safe-Cancel selbst: `PASS_SAFE_CANCEL_DURING_PREPARE_SETTLES_CLEANLY`; terminal Driver IDLE.
- Status: FIXED_AND_REPROVEN im finalen 0.57.6 Run `35693065234`.
