# Verbindlicher Nachweis – zentraler Normalweg verliert den endgültigen Fachbescheid

**Basis:** Exakt der einzige getestete Original-Arbeitsstand `PFERDEATELIER_EIN_ARBEITSRAUM_QA_STAND_20261112.zip`, SHA-256 `8fc55bca1fc7e4fe019203b2c56d169a734f0c3c941b08606fa9bed6b9183e33`. Original-PSTE `.45` und Original-PSERC `.69` enthalten dieselben hier relevanten Methoden. **Keine weitere Code- oder WP-Änderung.**

## Vorgabe des verbindlichen Zielvertrags

`EVIDENCE/PSTE_KISTENPRINZIP_VERBINDLICHER_ZIELVERTRAG_20261107.md`: exakt **ein zentraler fachlicher Entscheider**, spätere Stellen dürfen Entscheidungen **nicht erneut semantisch bewerten oder umstimmen**. Der zentrale Entscheider muss den **ganzen gleichzeitig bearbeiteten Stapel** und den gültigen Bestandsstand einbeziehen. Wortgleiches/gleichbedeutendes Neuthema darf nicht zweimal freigegeben werden. MINI bleibt im Produktionsweg. Technische Quellenfrische, Herkunft und Planplatz-Belegung sind weiterhin zu prüfen.

## Beweis 1 – aktueller PSERC-Leser verliert die zentrale Entscheidung

- Original-PSTE-`planning_readiness_gate` wurde einem gültigen normalen Thema mit `decision=PASS`, `planning_suitability=YES`, `research_run_status=COMPLETE` als reale Eingangsdatenstruktur übergeben.
- Die **echte Originalfunktion** `PSERC_SEO_Reader::normalizeCandidate` wurde ohne WP-Schreiben mit minimalen WP-Klassen-Dummies aufgerufen.
- Ausgabe der Probe: `original_has_planning_gate=true`, `transmitted_has_planning_gate=false`, `source_eligible=ELIGIBLE`, `source_receipt=[]`.
- Originalquelle: `portal-seo-editorial-plan-compiler/includes/class-pserc-seo-reader.php`, `normalizeCandidate` ab Zeile 81, `$normalized` ab Zeile 163. Die Methode erkennt als eine einheitliche Owner-Quittung nur das **MINI**-Feld `single_external_seo_owner_receipt`, aber **transportiert** den normalen `planning_readiness_gate` nicht zum nächsten Schritt.
- Danach im PSERC `class-pserc-compiler.php` Zeilen 64–88 und `class-pserc-plan-compile-job.php` Zeilen 147–163: **ohne** MINI-Beleg wird der zweite fachliche PSERC-Doppelgängerprüfer aufgerufen. Dies ist der reproduzierte Zielvertragsbruch, kein hypothetischer Live-Fehler.

## Beweis 2 – frühes PASS ist ausdrücklich NICHT das spätere Stapelergebnis

- Die **Originalfunktion** `PSTE_Runner::applyInternalDuplicates` per PHP-Reflection mit zwei gleichbedeutenden Themen im selben Recherchepaket aufgerufen. Beide hatten zunächst `planning_readiness_gate.status=PASS`.
- **Original-Ergebnis:** `before_pass=2`, `after_pass=1`, `after_blocked=1`, `blocked_retains_earlier_planning_gate_pass=true`, `blocked_reason_codes=[DUPLICATE_WITHIN_RESEARCH_RUN]`.
- Originalquelle: `Portal SEO Topic Engine/includes/class-pste-runner.php` Zeilen 191–205, 238–262 und 465–487. Dort wird das zentrale Stapelergebnis **nach** der frühen fachlichen Kandidatenprüfung berechnet und beim Research-Finalisieren gespeichert.
- **Wichtige Konsequenz:** Nur das alte `planning_readiness_gate.ok=PASS` nachträglich an PSERC zu hängen und den zweiten Checker abzuschalten wäre wieder **falsch**. Nur das endgültige gespeicherte, aktuell gültige Ergebnis **nach** der zentralen Paketentscheidung darf Freigabeautorität erhalten.

## Welche konkreten Fehler damit erklärt sind

1. Der normale PSTE-Weg und der MINI-Weg verwenden in PSERC **unterschiedliche Belege**, obwohl der Zielvertrag dieselbe einmalige Fachentscheidung verlangt.
2. Eine vorschnell kopierte frühe Freigabe würde eine im gleichen Recherchepaket später gesperrte Doppelung erneut durchlassen.
3. Daher sind die früheren Pauschallösungen **(a) zweiten Checker ersatzlos streichen** und **(b) `planning_readiness_gate=PASS` unverändert durchreichen** nicht sicher. Dies ist durch zwei Originalmethodenproben nachgewiesen.

## Einzige noch zulässige Codearbeit – vollständig statt kosmetisch

- Den bereits **vorhandenen, abschließenden PSTE-/MINI-Entscheidungsstand** mit eindeutiger Originalfrage, endgültigem PASS/BELEGT/KLÄRUNG, Stapelzugehörigkeit, Quellenstand und unveränderlichem Titel in der **bestehenden** Themenpool-Übergabe technisch binden. Keine neue fachliche Prüfung, kein zweites Datenlager.
- In **beiden** existierenden PSERC-Verbrauchern (`PSERC_Compiler::compile` und `PSERC_Plan_Compile_Job::tickCandidate`) ausschließlich diesen **vollständigen** finalen Beleg akzeptieren. Bei fehlendem/verändertem Beleg nur das betroffene Thema zurückstellen, *nicht* ersatzweise selbst semantisch neu entscheiden.
- Normale und MINI-Themen gegen dieselben Gegenproben prüfen: zwei gleichbedeutende neue Kandidaten, tatsächlich andersartige Fragen, unveränderte gültige Freigabe, Belegmanipulation, neue WP-Belegung, Wiederanlauf, einzelner Datenfehler. Technische Bestands-/Artikelplatzkontrollen bleiben erhalten.
- Erst danach: **genau die fertig verpackte** Original-Pluginpaarung erneut auf Vollintegrität und im **echten** WP-TEST über einen frischen K0-Artikel testen. Kein Installationspaket vor diesen Belegen.

## Ausführung und Grenzen

- `verify_original_normal_handoff.php`: die Originalmethode ausgeführt, Exit 0, Nachweis 1 PASS.
- `verify_pste_batch_gate.php`: Original-`PSTE_Runner::applyInternalDuplicates` ausgeführt, Exit 0, Nachweis 2 PASS.
- PHP-Vorlage für WordPress-Funktionen wurde **nur in diesen lokalen Prüfscripten** gestellt. Keine echte WordPress-Datenbank und kein Provider kontaktiert. Nachgestellte Kontrollflüsse beweisen Programmverhalten, aber keine reale WordPress-0-READY-Ursache.
- Die gesicherte Arbeits-ZIP wird **nicht verändert oder umetikettiert**. Beide Tests sind separat als Nachweis abgelegt.