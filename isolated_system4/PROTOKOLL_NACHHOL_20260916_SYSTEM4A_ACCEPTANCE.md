# PROTOKOLL-NACHHOLUNG — SYSTEM 4A ACCEPTANCE — 2026-09-16

Status dieses Dokuments: **historische Ausführungs- und Entscheidungs-Evidence**.

Dieses Dokument ist **keine CURRENT_STATE**, kein Zielvertrag, keine Bürotür und keine eigene dynamische NEXT-ACTION-Wahrheit. Der aktuelle operative Stand ist immer frisch aus dem tatsächlich aktuellen Branch/Head, den dazugehörigen echten Workflow-Läufen und — sobald autorisiert synchronisiert — der zuständigen Campus-CURRENT_STATE zu bestimmen.

## Arbeitsbindung

- Repository: `hallo-netizen/affiliate-pferdeportal`
- Arbeitsbranch: `hobbyroom/system4a-startgate-test-20260914`
- Ausgangshead der Nachholarbeit: `bffc891870a81bc872d21bc198944969a79eb812`
- Ausgangslage: Exact Head Bundle und Repair Owner Contract grün; Real LT68 PPM679 Acceptance rot.
- Zielvertrag unverändert: `isolated_system4/ZIELVERTRAG_SYSTEM4_MACHINE_POINT0_CODEX_WRITER_20260914.md`
- Textmaschine, PPM 6.7.9, Designvertrag und fachliche Prüfschwellen wurden in dieser Nachholarbeit **nicht gelockert**.

## Tatsächlich ausgeführte Reparaturen und Befunde

### 1. Repair-Continuity — veralteter Import

Der reale Diagnoseweg zeigte zuerst:

`ModuleNotFoundError: No module named 'live_parity'`

Ursache: `test_repair_continuity.py` importierte eine nicht vorhandene alte Schnittstelle, während der aktuelle gebundene Testweg `live_parity_v2.py` ist.

Änderung: Testimport auf `live_parity_v2 as live_parity` gebunden.

WARUM: Nur die aktuelle reale Parity-Schnittstelle darf Testautorität sein; kein Alias auf eine nicht existente alte Teststrecke.

### 2. Authoring Contract — Heading-Distance 27:28

Nach dem Import-Fix erreichte der Repair-Test den Authoring Contract und blockierte mit:

`ARTICLE_AUTHORING_CONTRACT_FAIL:PREWRITE_HEADING_DISTANCE:27:28`

Die Mindestschwelle 28 war korrekt. Die zuvor erfolgte LT-saubere Kürzung der deterministischen Testworker-Tails hatte einzelne Abstände um etwa ein Wort verkürzt.

Änderung: Die deterministischen LT-sauberen Tails wurden wieder ausreichend lang formuliert.

WARUM: Der bestehende 28-Wort-Vertrag bleibt unverändert; die Testausgabe muss den Vertrag erfüllen, nicht der Vertrag an die Testausgabe angepasst werden.

### 3. Repair-Continuity — veraltete Testannahmen

Nach Erreichen des eigentlichen Repair-Pfads waren drei Annahmen veraltet:

- Positivtests suchten frühere Tail-Sätze.
- Der Design-Negativtest veränderte nur eine HTML-Klasse; die Same-Article-Continuity prüft zunächst den sichtbaren Text und erkannte deshalb noch keine fachliche Reparatur.

Änderung:

- `_minor_repair` auf die aktuellen deterministischen Sätze gebunden.
- Design-Negativtest ergänzt zusätzlich eine kleine sichtbare Same-Article-Reparatur, damit anschließend tatsächlich der Design-Guard geprüft wird.

WARUM: Der Negativtest muss die beabsichtigte Schranke erreichen und darf nicht vorher an einer anderen korrekten Schranke hängen bleiben.

Ergebnis auf späterem Acceptance-Lauf: Repair-Schritte 23–28 PASS.

### 4. Batch-Handoff 1..N — Test-Fixture-Schuld nach Authoring-Contract-Hardening

Der nächste reale Fehler lag in `Textmaschine matrix — batch handoff one-to-N`.

Exakte Ursache: Der historische Commit `e342a9a1df6889b9db349c3b302cf6174066869e` hatte im Batch-Gate die verpflichtende Revalidierung durch `authoring_contract.validate_bound(...)` ergänzt. Die alten Batch-Test-Fixtures enthielten jedoch keinen gebundenen Authoring Contract und starben deshalb vor ihren eigentlichen Positiv-/Negativprüfungen.

Änderung:

- `test_batch_gate.py` und `test_universal_batch_gate.py` erzeugen den Authoring Contract jetzt mit dem echten `authoring_contract.build()`.
- Die Fixtures lesen die echten statischen PPM-6.7.9-Regeln.
- Das Batch-Gate selbst wurde **nicht** gelockert oder umgangen.
- Ein Negativtest für fehlenden Authoring Contract wurde ergänzt.

WARUM: Die neue Sicherheitsprüfung gehört zum realen Gate und muss in den Tests erhalten bleiben. Testdaten müssen dem aktuellen realen Vertragsstand folgen.

Ergebnis:

- Diagnose-Run `35080032743`: PASS.
- Kanonischer Real-Acceptance-Lauf `35080032773`: Schritt 29 `Textmaschine matrix — batch handoff one-to-N` PASS.

### 5. Zwischenbefund 1-Artikel-Live-Parity — anschließend korrigiert

Im kanonischen Run `35080032773` auf Head `493d1395cbffc2616df2f5fac206419c621d4677` waren die Schritte 1–30 erfolgreich. Der erste rote Schritt war:

`31 — Run complete one article route`

Zur Ursachenfeststellung wurde ein temporärer Diagnoseworkflow auf Head `61927bb6f49d3a03bd07c3b4098b10d0f57d31fe` exakt an denselben 1-Artikel-Weg, denselben Fresh-Run-Token-Mechanismus und dieselben LT-6.8-Hashes gebunden.

Diagnose-Run: `35080766923`.

Der erste Diagnosebericht ordnete den LT-Befund fälschlich `Gummidichtungen` zu. Eine anschließende hash-gebundene LT-6.8-Kandidatenprüfung korrigierte das: Der tatsächliche beanstandete Ausdruck war **`Verriegelungsweg`**.

Belegt wurden unter anderem:

- `Dichtungen dürfen den Verriegelungsweg nicht sichtbar behindern.` → 1 LT-Finding.
- `Dichtungen dürfen die Verriegelung nicht sichtbar behindern.` → 0 LT-Findings.

Änderung: ausschließlich die deterministische Testworker-Formulierung `den Verriegelungsweg` → `die Verriegelung` normalisiert. Eine zuvor versuchte, sachlich falsche `Gummidichtungen`-Normalisierung wurde entfernt.

WARUM: Die reale LT-6.8-Regel bleibt unverändert; nur die exakt nachgewiesene synthetische Testformulierungsursache wurde repariert.

### 6. PPM-6.7.9-Strukturfehler im synthetischen Frischartikel

Nach dem LT-Fix erreichte der echte 1-Artikel-Weg PPM 6.7.9. Dort wurden nacheinander reale Strukturfehler sichtbar:

- wiederholte Sätze / Known-Regression-Muster,
- zu geringer Conclusion-Anteil,
- zu geringer Tabellen-Unique-Token-Anteil.

Die erzeugte Draft-Evidence zeigte als Ursache mehrfach wiederverwendete Fact-Sätze in Details, Tabelle, Further Information und Conclusion.

Änderungen ausschließlich im deterministischen Testworker:

- Fact-Sentence-Tails zyklisch variiert,
- Beobachtung und Handlung in Tabellen auf unterschiedliche Fact-IDs gebunden,
- Conclusion deterministisch bis oberhalb des bestehenden Mindestanteils verlängert,
- in Tabellen verwendete Fact-IDs für nachfolgende Abschnitte reserviert, damit die Tabelle reale exklusive Evidence behält.

Keine PPM-Schwelle, kein Checker und kein Gate wurde verändert.

Ergebnis auf Head `6ba6466b6ec96d77814d4094eb123536b1e8ffed`:

- Exact Head Bundle `35085131506`: SUCCESS.
- Repair Owner Contract `35085131493`: SUCCESS.
- One-Route-Diagnostic `35085131432`: SUCCESS.
- 1-Artikel-Proof: Revision `[1]`, LT PASS, PPM PASS, Freshness PASS, keine historische Wiederverwendung.

### 7. Schritt 33 — 3-Artikel-Repair-Isolation

Im kanonischen Run `35085131467` waren Schritte 1–32 PASS. Erster roter Schritt war:

`33 — Run complete three article route with repair isolation`

Exakte Reproduktion ergab:

- alle drei Artikel LT PASS und PPM PASS,
- aber **kein Repair-Ereignis**,
- Revisionen `[1,1,1]` statt vertraglich erwarteter `[1,2,1]`.

Ursache: Der deterministische Negativtest selektierte Artikel 1 noch über einen alten Titelanfang `Warum muss die Beleuchtung...`. Nach der Freshness-Umstellung hieß Artikel 1 anders; der Negativfehler wurde deshalb nicht mehr injiziert.

Änderung: Der Testselektor wurde minimal auf die bereits maschinengebundene Artikelidentität `target_keyword = Bodenprüfung am Pferdeanhänger` umgestellt. Marker, Repair-Loop, Prüfer und Schwellen blieben unverändert.

Ergebnis auf sauberem Head `64a4cb416bc89968748f010710024ddcbc4af712`:

- Exact Head Bundle: SUCCESS.
- Repair Owner Contract: SUCCESS.
- Real LT68 PPM679 Acceptance: SUCCESS bis einschließlich Schritt 35.
- 1 Artikel: Revision `[1]`.
- 3 Artikel: Revisionen `[1,2,1]`.
- exakt ein Repair auf Artikel 1 mit `BLOCKED_KNOWN_REGRESSION_PATTERN`.
- LT und PPM für alle finalen Artikel PASS.
- Inline-Transport byte-identisch.

Damit ist die eigentliche System-4A-Artikelroute bis zum V2-Handoff technisch grün belegt.

### 8. Neuer echter Fehler — unbewiesene WordPress-Direct-Import-Behauptung

Nach dem grünen Artikelweg wurde die Übergabestrecke gegen den tatsächlich vorhandenen WordPress-Importer geprüft.

Befund:

- `SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2` deklarierte zuletzt selbst `WORDPRESS_DIRECT_IMPORT`, `direct_wordpress_upload_ready=true` und Pluginversion `0.28.23`.
- Die Handoff-Tests bestätigten diese Werte nur gegen dieselben hart codierten Werte; das war kein realer Importer-Nachweis.
- Historische System-4-Evidence hatte die Datei dagegen ausdrücklich als PREIMPORT mit notwendigem PSERC-/ENDSTEMPEL-Schritt beschrieben.
- Der echte Repository-Probe `wordpress_import_contract_probe.py` liest `control/startmaster0107/runtime_packages/PSERC-FIX.zip`.
- Der dort tatsächlich gebundene Importer ist `0.28.18-endstempel-import-envelope-binding-ppm679`.
- Dieser bindet `PFERDE_ATELIER_ENDSTEMPEL_RELEASE_V1`; ein direkter Eingang `SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2` ist dort nicht vorhanden.

Entscheidung: fail-closed. Kein erfundener Direct-Import-PASS.

Dauerhafte Änderung:

- eine zentrale `wordpress_review()`-Wahrheit in `handoff_transport.py`;
- `intended_next_step = WORDPRESS_PREIMPORT_REVIEW`;
- `direct_wordpress_upload_ready = false`;
- Blockgrund `REQUIRES_SIGNED_ENDSTEMPEL_PACKAGE_AND_PSERC_IMPORT_ENVELOPE`;
- erforderliche Downstream-Komponenten: `PSERC_APPROVED_PRODUCTION_PACKAGE_V1` und `PFERDE_ATELIER_ENDSTEMPEL_RELEASE_V1`;
- real gebundener Importer-Build `0.28.18-endstempel-import-envelope-binding-ppm679`;
- alle aktuellen Handoff-Erzeuger beziehen diese zentrale Wahrheit statt eigener hart codierter Direct-Import-Angaben.

Negativtests blockieren jetzt ausdrücklich:

- `direct_wordpress_upload_ready=true`,
- `WORDPRESS_DIRECT_IMPORT`,
- fehlenden Blockgrund,
- fehlende Downstream-Komponenten,
- die unbewiesene Versionsangabe `0.28.23`.

Der fokussierte Patch wurde vor Persistierung wiederholt geprüft:

- `test_handoff_transport.py`: 16/16 PASS,
- `test_local_end_to_end_chat_handoff.py`: 5/5 PASS,
- `test_machine_route_lock_contract.py`: 6/6 PASS,
- zusammen 27/27 PASS.

Persistierter Python-Patch: Commit `7fb9b4bd1ca6ccaa07c954652404784c29d58061`.

Zusätzlich wurde `wordpress_import_contract_probe.py` fail-closed verschärft: Er verlangt den realen Importer-Build und den ENDSTEMPEL-Vertrag und blockiert, falls der rohe V2-Handoff wider Erwarten als direkter Importvertrag auftaucht. Dadurch prüft der bereits vorhandene Real-Acceptance-Schritt die reale WordPress-Grenze selbst, ohne einen zweiten Workflow-Wahrheitsweg einzuführen.

### 9. Temporäre Diagnose-/Patchwege entfernt

Die nur zur Ursachenfindung bzw. Patch-Persistierung angelegten Workflows wurden nach Gebrauch entfernt:

- `.github/workflows/system4a-temp-wordpress-failclosed.yml`
- `.github/workflows/system4a-one-route-diagnostic.yml`

Der temporäre Python-Patchhelper `_temp_wordpress_failclosed_patch.py` wurde ebenfalls entfernt.

WARUM: Der finale Acceptance-Head darf keine Hilfsdiagnose als parallele Test-/Statuswahrheit enthalten.

### 10. Zielvertrags-Wegweiser korrigiert

`CODEX_LIVE_TASK.md` ist ausdrücklich historisch. Seine Liste „Aktuell verbindlich“ zeigte trotzdem noch auf den älteren Zielvertrag vom 13.09.

Änderung: Wegweiser auf den ausdrücklich aktuellen Zielvertrag `ZIELVERTRAG_SYSTEM4_MACHINE_POINT0_CODEX_WRITER_20260914.md` korrigiert.

WARUM: Keine widersprüchliche Pflichtlektüre; der historische Wegweiser darf keinen abgelösten Zielvertrag als aktuell ausgeben.

## Campus-/CURRENT_STATE-Befund

Die offizielle Bürotür auf `main` führt eindeutig:

`control/CURRENT_STARTMASTER.json`
→ `control/startmaster0107/PFERDE_ATELIER_START_HERE.json`
→ `control/startmaster0107/CURRENT_STATE.json`

Die dortige CURRENT_STATE bildet den aktiven System-4A-Branch/Head/Teststand nicht ab und enthält weiterhin den älteren 107007-/PPM679-Stand sowie einen anderen Hobbyraum.

Die CURRENT_STATE legt `state_write_authority = ENTRANCE_GATE_ONLY` fest. Der autoritative Gate-Code `control/deterministic-entrance-gate/door.py` erlaubt State-Fortschreibung ausschließlich nach einem PASS-Receipt entlang einer bereits vorgebundenen monotonen `next_binding`. Worker-Receipts dürfen weder Navigation entscheiden noch State-Schreiben anfordern.

Entscheidung: **Keine direkte Chat-/Branch-Umschreibung der Campus-CURRENT_STATE und keine zweite CURRENT_STATE anlegen.** Die Campus-Synchronisation bleibt BLOCKED, bis ein autorisierter Entrance-Gate-/State-Owner-Weg den System-4A-Stand bindet.

## Nicht verändert

- kein Plugin entwickelt oder aktualisiert;
- keine Plugin-Ausgabekopie erzeugt;
- keine Textmaschinenregel gelockert;
- keine PPM-6.7.9-Regel geändert;
- kein Designvertrag geändert;
- kein zweiter Zielvertrag angelegt;
- keine zweite CURRENT_STATE angelegt;
- keine Bürotür mit dynamischer Branch-/Head-/Run-Wahrheit angereichert;
- kein Publish und kein Merge freigegeben.

## Fortgeschriebener Prüfstatus

Dieser Abschnitt ersetzt den früheren Zwischenstand, in dem Schritt 31 noch rot war.

- System-4A-Artikelroute bis V2-Handoff: auf Head `64a4cb416bc89968748f010710024ddcbc4af712` vollständig remote grün bewiesen, einschließlich 1 Artikel `[1]`, 3 Artikel `[1,2,1]`, realem LT 6.8, realem PPM 6.7.9 und exakt einem gebundenen Repair.
- WordPress-Direct-Import: **BLOCKED / nicht bewiesen**. Die frühere `0.28.23`-/Direct-Ready-Selbstdeklaration wurde fail-closed korrigiert.
- Reale WordPress-Grenze: vorhandener Importer `0.28.18-endstempel-import-envelope-binding-ppm679`; erforderlich sind signierter ENDSTEMPEL-/PSERC-Importweg und dessen echter Importnachweis.
- Focused Fail-Closed-Tests: 27/27 PASS vor Persistierung.
- Temporäre Diagnose-/Patchwege: entfernt.
- Finaler Same-Head-Gesamtlauf nach letzter Dokumentations-/Cleanup-Änderung: **noch auszuführen**; daher aus diesem Dokument kein neuer Gesamt-PASS.
- Campus-CURRENT_STATE-Synchronisation: weiterhin BLOCKED durch fehlende vorgebundene State-Owner-/Entrance-Gate-Bindung für diesen System-4A-Arbeitsstand.
- Parent-Chat-Endnachweis: Gesamt-PASS weiterhin nicht erteilt; gemäß `PROTOKOLL_TESTSTRECKE_V2_20260914.md` genügt kein Remote-Run allein.
