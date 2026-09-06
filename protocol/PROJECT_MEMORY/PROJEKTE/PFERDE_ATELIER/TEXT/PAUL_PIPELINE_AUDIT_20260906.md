# PAUL PIPELINE AUDIT – TECHNISCHE PRÜFKARTE 2026-09-06

ROLLE: READ-ONLY-Prüfkarte / keine zweite Fehlerwahrheit.

QUELLE:
Nutzerübergebener Paul-Bericht „PBone Pipeline Inspection“, 2026-09-06.
Der beliebige Beispielartikel („Duschhocker kaufen“) dient nur als Testdatensatz; geprüft wurde unser System-/Plugin-/Workflowtyp.

AUTORITÄT:
- aktueller TEXT-Stand → CURRENT_STATE.md
- aktuelle Arbeit → HOBBYRAUM.md
- Fehlerwahrheit → FEHLERREGISTER → autoritative Fehlerquelle
- Ziel → ZV-TEXT-001


## HARTE SCOPE-GRENZE

Diese Prüfkarte ist **rein technisch**.

TABU:
- Architekturänderungen;
- Fach-/Inhaltsänderungen;
- Änderung oder Neuinterpretation von Textmaschine, SEO, Link-/Tabellenregeln, LanguageTool, PPM, PSERC/PSTE, Design oder Publish-Regeln.

ZULÄSSIG:
- prüfen, ob bestehende technische Module die vorhandenen Verträge korrekt verbinden;
- Artefaktzustand, Hash, Übergabereihenfolge, Status/Receipt und Fail-closed-Verhalten vergleichen;
- nur technische Implementierungsfehler als Kandidaten markieren.

Ein Fachvertrag wird nicht verändert, nur seine technische Durchsetzung geprüft.


## KERNAUSSAGE

Die wichtigste technische Fehlerklasse ist nicht „alte Regel = schlecht“, sondern:
**zwei jeweils sinnvolle Module/Gates können gemeinsam widersprüchlich werden, wenn sie verschiedene Zustände desselben Artefakts erwarten oder nicht exakt dasselbe Artefakt prüfen/weitergeben.**

Das passt direkt zu B01:
gültiger semantischer Kategorievertrag vs. nachträglich verlangte numerische WordPress-ID vor realem PPM.

## PRIORITÄT A – VOR / INNERHALB DES AKTUELLEN 107007→107008-ZIELS PRÜFEN

### Vertrags-/Gate-Kollisionen
- F1 – Router erzeugt Wert, den Schema nicht akzeptiert.
- F2 / A6 / A12 – Gate-Reihenfolge bzw. unresolved/resolved HTML widersprüchlich.
- F7 / A7 – Tabellenpflicht kann für betreffenden Artikeltyp unerfüllbar sein.
- F9 – Artikeltyp-/Affiliate-Vertrag kann unerfüllbar sein.
- A5 – Gate prüft falsche Schemaform.
- A9 – Blocker nach Vorverarbeitung teilweise nicht mehr erreichbar.
- A11 – derselbe „validated content hash“ bezeichnet zwei verschiedene Artefakte.

### Artefakt-/Render-Konsistenz
- A1 – gemischte Datenformen können Inhalt verlieren.
- A2 – Sanitizer entfernt bewusst erzeugte Tabellenattribute.
- A3 / A8 – TOC verändert/verschiebt Struktur vor nachgelagerten Prüfungen.
- A10 – Sanitizer verändert rel-Attribute nach/gegen Affiliate-Regel.
- A14 – erzeugter Vergleichs-Platzhalter ohne Resolver.
- A15 / A16 – Placeholder-/Linkfehler können Warn-/Strict-Netz umgehen.

### Research/Test-Parität
- F4 – Cannibalization-Weg nicht real durch aktuellen Test abgedeckt.
- F5 / F6 / A37 – Testsuite/Abhängigkeiten liefern kein vollständiges Produktionssignal.
- L2 – Research-Gate laut Paul-Modell nicht zwingend aktiv.

## DIREKTER STARTMASTER-BEFUND AUS HEUTIGEM CODE

Fachvertrag:
„PASS-Reuse nur bei identischem, hashgebundenem Input/Vertrag.“

Aktueller Handoff:
- jede Stage hat `input_sha256`;
- bei Nicht-PPM-Stufen wird technisch nur 64-Hex-Format erzwungen;
- keine generische Bindung beweist dort, welches konkrete Artikelartefakt der Hash bezeichnet oder dass Vor-/Nachstufe dieselbe Artefaktkette verwenden;
- PPM ist enger und bindet `input_sha256` explizit an `final_article_sha256`.

WICHTIGE EINORDNUNG:
Dieses lose Nicht-PPM-Verhalten bestand schon auf den belegten 7/7-Ständen `d841ed…` und `de21f6…`.
Daher aktuell **latente Vertrags-/Paritätslücke, nicht als Ursache des B01-Livefehlers belegt.**

## PRIORITÄT B – REAL, ABER NICHT IN AKTUELLEN B01/#140-FIX MISCHEN

- A17–A22 – Recovery/Fill/Budget/Cost/Yield/Bookkeeping.
- A4 – Responsive Images.
- A28 – Reader-Performance/Pagination.
- N1–N3 – Routing-/Leercorpus-Notizen.

Diese Punkte getrennt bearbeiten, wenn der aktuelle Produktionsweg wieder bis 107008 trägt.

## PRIORITÄT C – WORDPRESS/PUBLIC NACH DEM AKTUELLEN ZIEL

Aktueller ZV-TEXT-001 endet bewusst bei 107008 **vor Publish**.

Deshalb jetzt NICHT in PR #140 mischen:
- A13 – WP-Sync verliert internal_links/infoboxes.
- A23–A27 – Canonical/Sitemap/Reader/Links.
- A29 – Publish-Sync ohne Validierung.
- A30 – Draft→Approve→Publish Kurzschluss.
- A31 – record_id/post_id-Verwechslung.
- A32 – Bild-URL-Umschreibung nach Gate/Hash.
- A33 – fehlender WP-Create-Weg.
- A34 – done trotz fehlgeschlagenem Sync.
- A35 – BLOCKED-Draft öffentlich/Sitemap.
- A36 – approved-State downstream abgelehnt.
- L4 – kein WP-Ziel → terminal FAIL.

Diese Befunde sind sicherheits-/produktionsrelevant, aber **nicht Teil der jetzigen 107008-Wiederherstellung**, solange kein früherer Vertrag sie direkt beeinflusst.

## HARTE ARBEITSREGEL

1. Kein 41-Punkte-Sammelfix.
2. Erst Wirkungskette des aktiven 107007→107008-Wegs.
3. Pro Kandidat: konkretes Eingangsartefakt → Prüfung → Ausgangsartefakt → nächster Verbraucher.
4. Nur reproduzierter Widerspruch wird aktueller Fehlerkandidat.
5. Historische Fehlerquelle gegenprüfen.
6. KISS-Fix einzeln.
7. Bestehender Regressionstest danach.
8. Echter 7/7-Lauf bleibt Produktionsbeweis.
9. WordPress/Public-Funde separat nach Wiederherstellung des 107008-Ziels.

## KRITISCHER GEGENCHECK GEGEN BISHERIGE REPARATURVERSUCHE

### Was NICHT neu ist
- Übergabe-/Handoff-Probleme wurden bereits vielfach repariert (B02, B03, B07–B13).
- PASS/Live-Paritätsproblem ist bereits B14.
- PPM content_hash == final article SHA ist bereits M13.
- Batch-/Release-/Final-Context-Identität ist bereits M29/M30.
- Der Grundsatz „ein Modul kann lokal PASS sein und im Gesamtweg trotzdem scheitern“ ist daher nicht neu.

### Was nachweislich bereits Wirkung hatte
- B02 `BOUND_CURRENT_FACHWORKFLOW_EXECUTION_CONTEXT_MISSING`: durch Worker-Rollenbindung live überwunden; nächster Liveblocker wurde B01.
- B03 PPM/PASS-Reihenfolge: Kreisschluss technisch auf Request → realer PPM → erst danach PASS/Receipt korrigiert; Prinziptests PASS.
- B04 Fake-PPM: technische Selbstbehauptungs-Lücke fail-closed geschlossen.
- B05 current-main/Environment: letzter Live-Lauf passierte diesen Blocker.
- B07–B13 führten historisch jeweils weiter in der Kette bis 7/7 bzw. 107008/Endstempel.

Diese Fixes waren deshalb nicht „erfolglos“; sie beseitigten konkrete technische Sperren, lieferten aber keinen dauerhaften Gesamtbeweis.

### Was Paul tatsächlich NEU hinzufügt
1. **Unerfüllbarer technischer Vertrag zwischen zwei ansonsten gültigen Stufen** als eigener Prüfgegenstand.
2. **Artefaktzustands-Parität:** Gate A kann auf Version X PASS melden, während Gate B/Output Version Y konsumiert.
3. **Hash-Semantik statt nur Hash-Format:** derselbe Feldname/Hash kann technisch verschiedene Artefakte meinen.
4. **Pre-/Post-Transformation-Gate-Reihenfolge:** Prüfung kann vor oder nach Resolver/Sanitizer/Transformation auf dem falschen Zustand sitzen.
5. **Systematische End-to-End-Wirkungskarte eines einzigen Datensatzes**, statt nur den jeweils ersten sichtbaren Blocker einzeln zu reparieren.

### Direkter STARTMASTER-Abgleich
- Nicht-PPM-`input_sha256` wird im aktuellen Handoff nur formal als 64-Hex validiert; keine generische technische Bindung erzwingt die konkrete Artefaktidentität.
- Diese Lücke bestand bereits auf den letzten 7/7-Ständen. **Nicht als aktuelle Regressionsursache behandeln.**
- Der exakte reale PPM-6.7.9-Executor wurde jedoch erst nach dem letzten echten 7/7 hart in den Handoff eingebaut. Dadurch können bereits vorhandene Plugin-/Gate-Widersprüche erstmals zwingend im heutigen Liveweg wirksam werden.
- B01 ist dafür bereits ein belegtes Beispiel: der neue reale PPM-Handoff verlangte numerische WP-ID, obwohl der gültige Upstream-Kategorievertrag sie nicht vorsieht.

### Konsequenz
Pauls Konzept wird NICHT als neuer Sammelfix umgesetzt.
Es wird ausschließlich verwendet, um auf der technischen Ebene zu unterscheiden:
- bereits früher geprüft/behoben;
- alt und nachweislich nicht kausal;
- erst durch späteren realen PPM-/Handoff-Pfad neu wirksam;
- tatsächlich neuer reproduzierbarer Vertragskonflikt.

Nur die letzten beiden Klassen dürfen neue Reparaturkandidaten werden.

## ERGEBNIS DER DREI PRIORISIERTEN TECHNISCHEN PRÜFUNGEN

### 1. F2 / A6 / A12 – Pre-/Post-Transformation-Gate-Reihenfolge

**Neu gegenüber bisherigen Reparaturen:** JA.
B03 reparierte die Makro-Reihenfolge „Fachoutput → realer PPM → PASS/Receipt“, nicht die interne Reihenfolge Render/Resolve/Sanitize/Validate innerhalb des Prüfpfads.

**Aktiver STARTMASTER-Bezug:** NOCH NICHT HART BELEGT.
Im aktuellen 107007-Handoff werden weder `affiliate_mode`, Affiliate-Placeholder noch ein entsprechender Placeholder-Status als eigene Schnittstelle geführt. Der direkte Handoff bindet finalen Artikel, Produktionsplan, Fact-Pack und PPM-Report.

**Einordnung:** realer Systembefund aus Pauls Reproduktion, aber derzeit kein belegter aktueller STARTMASTER-Blocker. Nicht vorab reparieren.

### 2. F7 / A7 – technisch unerfüllbare Tabellenbedingung

**Neu gegenüber bisherigen Reparaturen:** JA.
Bisher wurde geprüft, dass `table_contract` als Pflichtstufe vorhanden bleibt; nicht systematisch, ob der durch den realen PPM konsumierte technische Artikelzustand die bereits bestehende Tabellenbedingung überhaupt erfüllen kann.

**Historischer Gegencheck:**
- `table_contract`-Hash auf letztem echten 7/7/107008-Stand `de21f6…`: `1ab3e892c37e5a48517519afcccbf8ec01b9f08da141eef93d577acd456756c7`.
- aktueller Kandidat: exakt derselbe Hash.
- Article-Type-Templates-Hash `dc79a6d7…` ebenfalls unverändert.
- Generation-1-Batch, Source-Snapshot und Batch-SHA sind auf `de21f6…` und aktuellem `main` identisch.
- entscheidender technische Delta danach: exakter echter PPM-6.7.9-Pfad wurde ab `6818cc…` / `9d7fe0…` in 107007 verpflichtend.

**Einordnung:** stärkster Paul-Folgekandidat nach B01. Nicht weil Tabellenregel oder Inhalt geändert wurden, sondern weil derselbe bestehende Vertrag jetzt erstmals im realen PPM-Pfad zwingend technisch ausgeführt wird.

**Grenze:** aktueller Live-Lauf stoppt noch vor `PSERC_PPM_Intake_Bridge::execute` an B01. Daher noch kein Beleg, dass F7/A7 der nächste reale Blocker ist. Kein Vorab-Fix.

### 3. A11 – unterschiedliche Hash-Semantik

**Neu gegenüber bisherigen Reparaturen:** TEILWEISE.
M13 bindet bereits PPM-`content_hash` exakt an den finalen Artikel-SHA. Pauls A11 betrifft dagegen `validated_content_hash` mit zwei unterschiedlichen technischen Bedeutungen.

**Aktiver STARTMASTER-Bezug:** schwach.
`validated_content_hash` ist in den aktuell offen lesbaren 107007-STARTMASTER-Schnittstellen kein verwendetes Feld; die harte Außengrenze arbeitet mit `final_article_sha256` und PPM-`content_hash`.

**Einordnung:** realer Systembefund, aber derzeit kein belegter aktueller 107007-Blocker. Zurückstellen, bis ein realer PPM-Fehler genau auf diesen inneren Hashpfad zeigt.

## KAUSALER KORRIDOR NACH LETZTEM ECHTEN 7/7

Vergleich `de21f6… → c8a96e7…`:

Gleich geblieben:
- Generation-1-Batch-SHA;
- Source-Snapshot-SHA;
- Source-Manifest-SHA;
- Production-Package-SHA;
- Article-Type-Templates-Hash;
- Tabellenvertrag-Hash;
- Fach-/Inhaltsregeln.

Neu/härter geworden:
- PPM 6.7.9 wird nicht mehr nur durch Stage-Proof behauptet, sondern im Handoff real ausgeführt;
- exakter PPM-/PSERC-Paketpfad und Hash werden erzwungen;
- finaler Artikel wird an Production-Plan und PPM-`content_hash` gebunden;
- realer PPM-Handoff erzeugt erst danach PASS/Receipt;
- Worker-/Context-Bindung wurde nach späteren Blockern zusätzlich gehärtet.

Aktueller erster realer Blocker liegt innerhalb genau dieses neuen Korridors:
`BOUND_WORDPRESS_CATEGORY_ID_MISSING_FOR_REAL_PPM679_EXECUTION`.

**Schluss:** Pauls Mehrwert ist real, aber kein Grund für einen Sammelfix. Nach B01 ist ausschließlich der noch nie live bewiesene reale PPM-Korridor der nächste technische Beobachtungsbereich.

