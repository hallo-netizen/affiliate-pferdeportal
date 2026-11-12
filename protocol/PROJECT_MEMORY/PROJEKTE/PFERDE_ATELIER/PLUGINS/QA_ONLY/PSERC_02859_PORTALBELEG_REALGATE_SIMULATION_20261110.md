# QA 10.11.2026: Warum PSERC .59 trotz 8 geeigneten Themen 0 READY liefert

**NUR READ-ONLY-Quelltest; keine Pluginänderung und keine Installation.** Grundlage: tatsächlich vom Anwender auf oliver-beil.de bestätigte PSERC 0.28.59, Original-.59-PHP und PSTE .32 aus privatem Pluginbüro. **Die acht einzelnen aktuellen WordPress-Topic-Payloads sind NICHT vorliegend.** Die folgenden Tests sind daher reproduzierte **kontrollierte Simulationen**, KEINE Behauptung, die acht individuellen Grundcodes seien aus WordPress ausgelesen.

## Gesicherter realer Nutzerbefund
- 5.016 Themen gesamt / 8 geeignet / 5.008 zurückgehalten / 0 READY.
- Aktueller PSERC-Plan-Snapshot **PASS**. Alle 8 geeigneten Positionen erhalten **BLOCKED_PORTAL_TOPIC_EVIDENCE**.
- Damit ist der Plan-Snapshot-Fehler aus früherem Screenshot nicht mehr die aktuelle Sperre. Kein sinnvolles weiteres Plan-Refresh.

## Echte Original-Code-Ursache
1. `PSERC_Plan_Compile_Job::tickCandidate` ruft **unbedingt** nach Titel- und Dubletten-Vorbereitung `PSERC_Portal_Topic_Evidence_Gate::evaluate(PSERC_Compiler::evidenceView($topic),$structure)` auf, auch dann, wenn das Thema über `single_external_seo_owner_receipt` bereits von **einem** externen SEO-Owner entschieden wurde.
2. `PSERC_Portal_Topic_Evidence_Gate::evaluate` prüft weiter Altbelege: `PSTE_AUTOMATIC_LONGTAIL_RESEARCH_JOB_V2`, `research_run_status=COMPLETE`, komplette `query_record` und Provider-Belege, alten `semantic_consensus`, `title_quality`, `language_quality`, `editorial_quality_gate`, `pre_title_duplicate_gate` etc. Das ist eine **eigene alte fachliche Zweitprüfung**, obwohl die neue PSTE/MINI-Architektur eine einzige gebundene externe SEO-/Titelentscheidung verlangt.
3. Der für die neuere Route validierte `single_external_seo_owner_receipt` in `PSERC_SEO_Reader::normalizeCandidate` wird zwar gesetzt und für das Überspringen der PSERC-Dubletten-Nachprüfung genutzt. **Der nachfolgende `PSERC_Portal_Topic_Evidence_Gate` unterscheidet diese Route überhaupt nicht**. Er prüft unverändert den Altvertrag. **Das ist der nachgewiesene Architektur-/Implementierungswiderspruch**, der in den alten .59-Browser-Simulationen nicht getestet war.

## Echte PHP-Simulation – bereits ausgeführt
- In der **unveränderten** `PSERC_Portal_Topic_Evidence_Gate`-PHP-Klasse aus tatsächlich gespeicherter .59 und echten `PSERC_Metadata_Boundary` / `PSERC_Article_Type_Extension_Registry` wurden **sieben echte zuvor mit PASS gemeldete Keyword-/Titel-Paare** aus dem privaten v29-WordPress-Batchbericht getestet. **Nur die Portalevidenz-Felder** wurden synthetisch angesetzt, nicht aus dem aktuellen WordPress ausgelesen; die Titel wurden **nicht** nach GitHub übertragen.
- Variante A: Externe FREI-Bestätigung und korrekte fünf Hand-off-Felder, aber ohne altes Recherche-Job-Objekt: **7/7 BLOCKED `PORTAL_TOPIC_RESEARCH_JOB_CONTRACT_INVALID`**.
- Variante B: Synthetisch zusätzlich alter `research_job_contract`, `research_run_status`, `query_record` und gültig geformter Quellenbeleg: **7/7 BLOCKED `PORTAL_TOPIC_SEMANTIC_CONSENSUS_NOT_PASSED`**.
- Beide Varianten zusätzlich **mit und ohne externen Owner-Beleg** durchgeführt: exakt **gleiche** Sperren, 14/14 Vergleichsfälle. Der externe Ownerbeleg wird in diesem alten PSERC-Gate nicht verwendet.
- Die PHP-Test-Simulation bestätigt die **Lücke in der Ablaufprüfung**, nicht den genauen, jeweils tatsächlich fehlenden Beleg bei den acht aktuellen WordPress-Themen.

## Vor dem nächsten Plugin zwingend
1. Die **acht gespeicherten Einzelgründe** aus dem bestehenden, aktiven PSERC-Plan auf WordPress-TEST **rein lesend** ermitteln (`item.production_reason_codes` aus `PSERC_Plan_Snapshot_Store`), einschließlich vorhandener `single_external_seo_owner_receipt`-Bindung. Nicht blind neue Daten importieren/Pläne neuberechnen.
2. Korrektur ausschließlich in den **bestehenden PSERC-Reader/Gate-Klassen**, die validierte neue externe Route technisch akzeptieren lassen und den Altpfad für echte Alt-Themen beibehalten. **Keine** Sicherheitsprüfungen der Quelle/Frische/ID/Kategorie/Platzkapazität entfernen, kein neuer Worker, kein neuer Exporter.
3. **Ganzes altes und neues Verfahren testen**: mit nachweislich gültigem realem Einzelbeleg muss mindestens ein THEMA READY + echte bestehende `PSERC_TEXTMACHINE_METADATA_BATCH_V2` erzeugen; fehlender/abgelaufener/manipulierter Beleg, Kategorie-/Planänderung, DUPLIKAT, leerer Titel und leerer Export müssen sicher blockieren; bisheriger Legacy-Altweg unverändert. Danach einmal auf WP-TEST mit realer Datei nachprüfen. Vorher **KEINE neue Installations-ZIP anbieten**.
4. Private Arbeitsdaten und Originaltitel ausschließlich im privaten Pluginbüro halten, nicht ins GitHub committen. K0, PSTE, gespeicherte WP-Pläne/Recherche und LIVE unverändert.

**Erkenntnis:** Die bisherigen .58/.59-Prüfungen waren Plan- und UI-Tests, kein End-to-End-Test der echten fachlichen PSTE-/MINI→PSERC→K0-Schnittstelle. Ihre PASS-Meldungen bewiesen daher NICHT eine Produktionsfreigabe.
