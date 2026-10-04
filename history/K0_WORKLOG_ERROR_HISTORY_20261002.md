# K0 Arbeits-/Fehlerprotokoll 2026-10-02

**Rolle:** HISTORIE / NACHWEIS. **Keine CURRENT-, Status- oder NEXT-ACTION-Autorität.**  
Aktuelle K0-Wahrheit ausschließlich: `K0_CURRENT_STATE.json`.

## Zielbindung

- K0-Ziel: `K0_GOAL_CONTRACT.json`
- globaler Medium-Zielvertrag: `control/startmaster0107/ZIELVERTRAG_REASONING_MEDIUM_MAX_STARTMASTER0107.json` auf `main`
- Qualität darf nicht reduziert werden.
- `publish_allowed=false`.

## Ausgangsfehler

Der alte 16er-Pferdeatelier-Batch aus K9 war in allen 16 Artikeln von einer generischen Entscheidungs-/Kauf-Schablonenfamilie betroffen. Besonders sichtbar bei „Warum sagt man du alte Schabracke?“: informationaler Sprach-/Wissensartikel wurde in Auswahl-/Passform-/Entscheidungslogik gedrückt. Die alte Schabracke wurde fachlich in `pferdewissen-grundlagen` verschoben.

## Fehlerfolge dieses Chats

### E1 – erster K0-Neuschreiblauf nutzte einen Sonderweg
- Fertige Texte wurden direkt als `K0_ARTICLE_PACKAGE_V1` erzeugt und erst danach K0-Gates/LT/PPM/Export zugeführt.
- Folge: der echte Writer-Regelblock wurde umgangen.
- Sichtbare Qualitätsregression:
  - zu viele H2;
  - zu kurze Textblöcke zwischen H2;
  - Fazit teilweise zu kurz;
  - „Weiterführende Informationen“ fehlten.
- Die daraus erzeugte 16er-Datei wurde später **widerrufen / nicht importieren**.

### E2 – Writer-Provenance-Lock war zunächst unvollständig
- Erste Reparatur verlangte Writer-Provenance, erlaubte aber, einen bereits fertigen Artikel nachträglich zu stempeln.
- Damit blieb derselbe Sonderweg technisch möglich.
- Ursache: Produktionsworkflow akzeptierte einen fertigen Artikel als Einstieg und konnte den Writer-Nachweis selbst erzeugen.

### E3 – WordPress-Datei wurde vom Importer abgelehnt
- Der damalige K0-Exporter ließ das vom Importer 0.28.30 benötigte kanonische `article_id` weg.
- Der Importer blockierte bereits beim ersten Artikel.
- Richtige Bindung:
  `plan_slot -> genau ein PPM-6.7.9-Registry-Slot -> canonical_article_id`
  und Roundtrip
  `SHA256("pserc-plan-slot-v2|" + article_id) == plan_slot`.

### E4 – direkte Artikelpaket-Produktion wurde deshalb vollständig entfernt
Neue verbindliche K0-Kette:
`5-Feld-Intake -> textfreier AUTHORING_CONTEXT -> unveränderbarer WRITER_JOB -> K0_WRITER_DRAFT_V1 -> Writer-Seal -> K0-Gates/PPM 6.7.9 -> LT 6.8 -> canonical article_id -> WordPress 0.28.30`.

Technische Bindungen:
- `.github/workflows/k0-authoring-context.yml`
- `.github/workflows/k0-writer-accept.yml`
- `engine/k0_writer_station.py`
- `engine/writer_contract_guard.py`
- `engine/k0_production_gate.py`
- `engine/canonical_binding.py`
- `engine/k0_wordpress_export.py`

Harte Negativregeln:
- fertiges `ARTICLE_PACKAGE.json` darf nicht Produktionsstart sein;
- AUTHORING_CONTEXT darf keinen sichtbaren Artikeltext enthalten;
- fertiger Artikel darf nicht als Writer-Draft eingereicht werden;
- Writer-Seal muss an unveränderten Writer-Job, Draft-Hash, Identität, sichtbaren Text und Struktur gebunden sein;
- WordPress-Export ohne gültigen Writer-Seal blockiert;
- WordPress-Export ohne kanonische `article_id` blockiert.

### E5 – paralleles Anlegen der 16 Authoring-Kontexte verursachte Workflow-Kollisionen
Mehrere `AUTHORING_CONTEXT.json` wurden zu schnell hintereinander committed. Die Workflow-Concurrency führte zu Cancel/Fail; ein Lauf scheiterte beim Push mit `non-fast-forward`.

Beleg:
- Authoring run `37056827345`: Vorbereitung PASS, Persist-Writer-Job FAIL durch non-fast-forward.
- Dadurch blieben Artikel 13 und 14 zunächst ohne `WRITER_JOB.json`.
- Das ist kein Artikel-/Qualitätsfehler; die vorhandenen AUTHORING_CONTEXT-Dateien sind textfrei und gültig.

### E6 – K0-Selftest kollidierte mit geerbter K10-Isolationsregel
- Die geerbte Isolationsprüfung verbot jeden Pfad namens `writer_drafts`, obwohl K0 diesen Pfad nun als einzigen kanonischen Texteingang benötigt.
- Folge: K0-Selftests blockierten, obwohl Writer-Accept-Läufe selbst korrekt PASS waren.
- K0-spezifische Reparatur: `engine/isolation_guard.py` akzeptiert in `writer_drafts/` ausschließlich JSON mit:
  - `contract=K0_WRITER_DRAFT_V1`;
  - gültiger `k0w-...` Job-ID;
  - `publish_allowed=false`.
  Andere Inhalte dort bleiben BLOCKED.
- Nachweis: K0-Selftest run `37059664443` = **SUCCESS**.

## Aktueller belegter Produktionsfortschritt bei Erstellung dieses Protokolls

Kanonisch vollständig bis verifiziertem `WORDPRESS_SINGLE.json`:
- 0 Das Wichtigste über Reitplatzplaner für Pferde
- 1 Frieren Pferde unter Regendecken?
- 2 Ist eine Reitplatzbewässerung von unten möglich?
- 3 Kann man mit Kappzaum spazieren gehen?
- 4 Longiergurte mit Bogen im Ratgeber
- 5 Passende Kühlgamaschen für Pferde wählen
- 6 Pferdehaftpflicht mit Fremdreiterrisiko auswählen
- 7 So findest du einen passenden Kappzaum für dein Pferd
- 8 So wählst du passende Schermaschinen für Pferde
- 9 Warum sagt man eigentlich „alte Schabracke“? – `pferdewissen-grundlagen`
- 10 Was ist der Unterschied zwischen Schabracke und Satteldecke?
- 11 Was ist ein Reitplatzplaner?
- 12 Welche Magnetfelddecke ist besser geeignet BEMER oder ActivoMed?
- 15 Wie teuer ist der TÜV beim Pferdeanhänger?

Noch nicht kanonisch bis Writer-Job/Seal geführt:
- 13 Wie lege ich einen Longiergurt an?
- 14 Wie oft muss ein Pferdeanhänger zum TÜV?

Alle 14 vorhandenen WordPress-Singles:
- Vertrag `SYSTEM4_WORDPRESS_HANDOFF_V1`;
- Plugin `0.28.30`;
- Build `0.28.30-pste-v5-binding-safe`;
- `direct_wordpress_upload_ready=true`;
- gültige `article:[0-9a-f]{24}`-ID;
- gültiger plan_slot-Roundtrip;
- `publish_allowed=false`.

Letzter Writer-Accept vor Closeout:
- run `37058612043` = SUCCESS.

## Widerrufene / nicht zu verwendende Artefakte

Nicht importieren:
- der frühere kombinierte 16er-K0-Export mit SHA-256 `c9a4dbfa517cb8af9f914bbb6b24090b4b3bc8c3ca7d526f65460b7a6024b7e3`;
- alle daraus abgeleiteten Aussagen „16/16 canonical normal path“;
- direkte `ARTICLE_PACKAGE.json`-Altprodukte in alten Run-Verzeichnissen sind keine Produktionsautorität.

## Nicht betroffen / unverändert

- K9-Produktion selbst wurde durch den K0-Fix nicht als Produktionspfad umgebaut.
- Plugins wurden in diesem Arbeitsstrang nicht entwickelt oder geändert.
- Kein Publish.


### E7 – Abschlussrefresh entfernte kurz das K10-Isolationsfeld
- Beim Closeout-Refresh von `K0_CURRENT_STATE.json` wurde `k10_unchanged` zunächst entfernt, obwohl der K0-Selftest dieses Feld als Isolations-Hardlock verlangt.
- Selftest Run `37061273870`: FAIL ausschließlich bei `K0 current hardlocks` mit `KeyError: k10_unchanged`.
- Feld wiederhergestellt; K10 bleibt zugleich als separater Arbeitsbereich über seine eigene Current referenziert und ist keine K0-Abhängigkeit.
- Reparatur-Commit: `ebdef6afba593e419358b2a224ac272b5b6cbe56`.
- Finaler K0-Selftest Run `37061356909`: SUCCESS.
- Kein Produktionsfortschritt verändert; K0 bleibt 14/16 mit Artikel 13 als erstem offenen Blocker.


### E8 – K0-START_HERE ohne ausdrückliche Current-Zuordnung
- Abschlussprüfung: `K0_START_HERE.md` nannte den K0-Startweg, aber nicht ausdrücklich `K0_CURRENT_STATE.json` als alleinige Current-Autorität.
- Minimalfix: `K0_START_HERE.md` ist jetzt ausdrücklich Navigation und routet genau auf `K0_CURRENT_STATE.json -> Frischecheck -> genau eine NEXT ACTION`.
- Keine Produktionslogik, Qualitätsregel, LT-/PPM-/WordPress-Bindung oder Publish-Regel geändert.
- Für die aktuelle K0-Fortsetzung gilt ausschließlich die K0-Current auf dem K0-Branch. Andere Arbeitsbereiche werden nicht zu einer gemeinsamen Statuswahrheit zusammengesetzt.
- `tmp/k0-rewrite16-content-20261002` ist nur alter Sonderweg-Nachweis, keine Current-/NEXT-ACTION-Autorität. Seine alten kombinierten Exporte bleiben widerrufen.


### E9 – Abschluss-Frischecheck nach Bürotür-Fix
- Frischecheck gegen Branch-Head `0751522ecf9e513da9a302d6f1a1c0447681e902` durchgeführt.
- Neuester K0-Selftest auf diesem Head: Run `37062998789` = **SUCCESS**.
- Seit dem 14/16-Produktionsstand gab es **keinen weiteren kanonischen Writer-/WordPress-Produktionsfortschritt**; die späteren Änderungen betrafen Current-/Bürotür-/History-Closeout.
- Der fachliche Status bleibt daher unverändert: 14/16 kanonische WordPress-Singles vollständig; Artikel 13 und 14 offen; erster Blocker weiterhin Artikel 13.
- NEXT ACTION bleibt ausschließlich aus `K0_CURRENT_STATE.json`: `RETRY_AUTHORING_CONTEXT_ITEM_13_SEQUENTIALLY_THROUGH_CANONICAL_K0_WRITER_PATH`.
- Keine Qualitäts-, LT-, PPM-, WordPress- oder Publish-Regel wurde durch diesen Abschlusscheck geändert.

## 2026-10-03 – Delta: interne Linkverteilung / offener Rendering-Abstand

### E10 – Interne Links waren formal vollständig, aber falsch verteilt
- Reale 3er-Ausgabe zeigte bei Kühlgamaschen drei gebundene interne Links, davon jedoch nur einen im eigentlichen Hauptteil; ein Link lag im Intro, einer im Hauptteil, einer in `further_information`.
- Nutzerbindung: exakt drei interne Links bleiben bestehen; `parent_category` und `semantic_related` müssen in zwei verschiedenen Haupttextblöcken liegen; `further_information` bleibt ausschließlich im Block `further_information`. Intro, Fazit und Tabelle zählen nicht als Haupttext.
- Minimalfix ausschließlich in der Linkverteilung:
  - `engine/k0_full_rules.py`: Regelkontext blockiert `parent_category` oder `semantic_related` außerhalb des Haupttexts;
  - Regressionstest ergänzt;
  - `K0_START_HERE.md` bindet dieselbe Verteilung.
- Relevante Commits:
  - `fd90514ba2738d282784d5255102cc109aa4cd1b`
  - `f5fcbb417dfe47a2d11421559d9fd8fd29d4a36a`
  - `87044b5733f4ea10800fa5f881a66d672b6d4741`
- K0-Selftest Run `37136204080` auf Head `87044b5733f4ea10800fa5f881a66d672b6d4741`: **SUCCESS**.
- Noch nicht belegt: frische reale Artikelproduktion nach diesem Linkfix. Der PASS belegt Code/Regression, nicht einen neuen real importierten Artikel.

### E11 – Große sichtbare Lücken vor Zwischenüberschriften bleiben offen
- Im ausgegebenen Kühlgamaschen-Artikel sind vor den betroffenen H2 keine zusätzlichen Leerabsätze oder `<br>` als Ursache belegt.
- Die großen vertikalen Abstände entstehen daher im Renderingpfad; die konkrete aktive CSS-/Renderursache ist noch **nicht abschließend isoliert**.
- Am Rendering wurde in diesem Arbeitsabschnitt **noch nichts geändert**.
- Tabellenlogik wurde nicht geändert. Für Kühlgamaschen war `OMIT_NO_ADDED_VALUE / EXISTING_CHECKLIST_EQUIVALENT` eine ausdrücklich gebundene Tabellenentscheidung.
- Nutzer-Hardlock für die Fortsetzung: **nur Rendering-Abstand reparieren; Linkverteilung nicht neu konzipieren; alles andere unverändert lassen.**

### E12 – frischer Chat konnte zunächst auf falsche Startwahrheit fallen
- Ein frischer K0-Chat las auf `main` den allgemeinen alten Current-Pfad statt direkt den K0-Branch.
- Ursache: auf `main` fehlte die eindeutige K0-Routingtür; der K0-Branch besaß zwar seine Current-Autorität, war für einen frischen Chat aber nicht ausreichend vorgeschaltet.
- Minimalfix wurde auf `main` über PR #490 gemergt: `main:K0_START_HERE.md` routet auf `konzept0-portal-neutral-20261002:K0_START_HERE.md`.
- K0-Regressionstest für den Router wurde ergänzt.
- Dieser Routingfix ändert keine Artikel-, LT-, PPM-, Tabellen-, WordPress- oder Publish-Regel.

### E13 – Repo-Hardlock kann die erste sichtbare Chat-Vorrede nicht zuverlässig verhindern
- Trotz Repo-Regel `NICHT ANTWORTEN. SOFORT INTERN PRODUZIEREN.` wurden in bereits laufenden/frischen Chats weiterhin sichtbare Startformulierungen wie „Ich starte K0 … ich prüfe zuerst …“ beobachtet.
- Befund: diese erste Chat-Ausgabe kann entstehen, bevor der Repo-Einstieg gelesen und angewandt wurde.
- Deshalb ist ein Repo-Selftest für die Startdatei **kein Beleg**, dass die Chat-Oberfläche garantiert keine erste Arbeitsmeldung ausgibt.
- Status darf daher nicht als produktseitig garantiertes `PASS` geführt werden.
- Kein weiterer Eingriff in Artikelproduktion oder Qualitätsregeln daraus abgeleitet.



## 2026-10-03/04 – Delta: Fresh-Run-/Inhaltsisolation, Rendering-Fix und frischer K0-Testartikel

### E14 – Frischer K0-Start konnte alte fertige Ausgabe desselben Batch-Hashes wiederverwenden
- Beobachteter Fehlweg: neuer Auftrag wurde zunächst gegen K9 geprüft und anschließend eine bereits vorhandene K0-`WORDPRESS_BATCH.json` desselben Batch-Hashes als Ergebnis akzeptiert.
- Korrektur: K0-Fresh-Execution-Hardlock. Neuer Upload + `K0:start` verlangt immer einen neuen Run mit neuer Run-Identität und frischer Gate-Kette.
- Alte `WORDPRESS_SINGLE.json`/`WORDPRESS_BATCH.json`, Writer-, LT-, PPM- oder Export-PASS dürfen einen neuen Auftrag nicht ersetzen.
- Main-Router-Merge: `9a00fb6ee60fd908521e0be345754684e8a60e02`.
- K0 bleibt alleiniger Produktionsweg; K9/K10 sind keine Laufroute.

### E15 – Alte Inhalte waren noch nicht hart genug als Writer-/Repair-Quelle ausgeschlossen
- Ziel: Jeder neue Artikel inhaltlich von Null; aktueller Upload ist Auftrags-/Artikelidentität.
- Erlaubt: frische Recherche dieses Runs, aktuelle K0-Regeln, aktuelle Kategorie-/Link-Bindungen.
- Verboten: alte Artikel, frühere Writer-/Repair-Texte, alte Fact-/Research-Pakete, frühere `real_runs/**`, `recovery/**`, Archive und bestehende Pferdeatelier-Artikel als Recherchequelle.
- Zusätzlich gebunden: finale verifizierte WordPress-Datei muss als echte Chat-Datei geliefert werden; GitHub-/Raw-/Actions-/Artifact-Link ist keine Endausgabe.
- Main-Router-Merge: `cff4ae618b2990d72856debaec9a12edce2de51f`.

### E16 – Freshness-Hardlock brach bestehende K0-Selftests
- Roter Selftest: Run `37153131743`, Ergebnis 3 Failures + 11 Errors.
- Hauptursachen:
  - Freshness-Isolation lief vor bestehenden Blockern und überdeckte erwartete Negativfälle;
  - mehrere Test-Fixtures hatten noch keine frischen Research-Sources/Freshness-Receipts;
  - Historical-Guard-Tokenisierung war fehlerhaft;
  - validierter Freshness-Receipt wurde nicht in den immutable Writer-Job für die Seal-Nachprüfung übernommen.
- Reparatur ohne Schutzabschwächung:
  - bestehende Blocker-Reihenfolge wiederhergestellt;
  - Fixtures angepasst;
  - Tokenisierung korrigiert;
  - Freshness-Receipt im Writer-Job gebunden.
- Positiv-/Negativtest: PASS.
- Vollständiger Reparatur-Selftest: 108/108 PASS.
- Merge/Fix: `2d10588eb500490c3c36c05ce2e56700b5145385`.
- Nachlauf-Selftest auf K0-Branch: Run `37184150503` = SUCCESS.

### E17 – Rendering-Abstand wurde durch doppelte vertikale Margins vergrößert
- Lokaler Negativtest reproduzierte 64 px Übergang: 32 px Rest-Margin des letzten sichtbaren Elements + 32 px Section-`margin-top`.
- Positivtest mit ausschließlich dieser Korrektur: normale H2 32/32 px, Liste/Fazit-Übergang 32 px.
- Kein Farb-, Linien-, Karten-, Schrift-, Inhalts-, Tabellen-, LT-, PPM- oder Importer-Umbau.
- Main-Merge: `f853fb61384385fb97d5de020b7ea6903890ea35`.
- Main-Head beim Abschlussrefresh: exakt derselbe Commit.
- Live-WordPress-Readback dieses Designfixes wurde in diesem Chat nicht durchgeführt.

### E18 – Freshness-Guard blockierte den aktuellen Writer-Draft fälschlich gegen sich selbst
- Frischer Testlauf: `real_runs/k0/test-20261004-fremdreiter-ae3b6c46`.
- Writer-Accept Run `37184874665` und Wiederholung `37185114685`: FAIL.
- Writer-Seal selbst war jeweils PASS; Blocker:
  `K0_HISTORICAL_TEXT_REUSE_BLOCKED:writer_drafts/test-20261004-fremdreiter-ae3b6c46.json`.
- Ursache: Historical-Content-Guard verglich den frisch zu prüfenden aktuellen Draft als vermeintliche Historie mit seinem eigenen versiegelten Text.
- Minimalfix: ausschließlich den exakt aktuellen Source-Draft vom Historien-Scan ausschließen; echte historische Drafts bleiben blockiert.
- Reparaturcommit: `7c9293d4b0ac1038eaa049aecb9bb06b9dfaa804`.
- K0-Selftest danach: Run `37185402642` = SUCCESS.

### E19 – Frischer Testartikel hatte anschließend zwei echte LanguageTool-6.8-Funde
- Writer-Accept Run `37185402627`: FAIL erst bei LanguageTool 6.8.
- Vor LT waren Historical-Guard, Writer-Contract, PPM 6.7.9/104 Regeln und alle 84 Pre-LT-Hardrules PASS.
- LT 6.8 meldete exakt 2 Funde:
  - `GERMAN_WORD_REPEAT_BEGINNING_RULE`;
  - `DE_SUBJECT_VERB_AGREEMENT`.
- Nur diese Textfunde wurden im frischen Draft repariert; Commit `5837c9d9a114b9618f491ef217bb500249767cdc`.

### E20 – Frischer K0-Testartikel vollständig PASS
- Artikel: „Pferdehaftpflicht mit Fremdreiterrisiko auswählen“.
- Writer-Accept Run `37185472620`: SUCCESS.
- Parallel-Selftest Run `37185472673`: SUCCESS.
- Persistenzcommit des fertigen Outputs: `2e515462a425f826aa711fca2dda53058891e58b`.
- Run-ID: `run:f83847e91c2fec0d855df87f`.
- Historical-Content-Guard: PASS, `historical_text_reuse=NOT_DETECTED`, 79 historische Dateien geprüft.
- Writer: 756 Wörter, Fazit-Ratio 0.100529, Writer/Section/Fazit/Weiterführende-Informationen PASS.
- Pre-LT: 84 Hardrules PASS; PPM 6.7.9 = PASS, 104 Regeln.
- LanguageTool 6.8: PASS, 0 Findings.
- Finale Regeln: PASS (WordPress-Export wurde nur nach finalem Full-Rule-PASS erzeugt).
- `WORDPRESS_SINGLE.json`: `SYSTEM4_WORDPRESS_HANDOFF_V1`, `direct_wordpress_upload_ready=true`, `publish_allowed=false`.
- Artikel-ID: `article:11bf036b5c0473935b65167e`.
- Finaler Body-Hash: `df66e162267769c5e8273ac525ad68ccc4ebf65b473cf00daf5f9396706fe0d0`.
- `WORDPRESS_VERIFY.json`: PASS, canonical binding PASS.
- Offene Benutzeranforderung nach diesem PASS: echte Chat-Datei materialisieren und HTML-Vorschau aus genau diesem verifizierten Body erzeugen. Keine neue Produktion nötig.


### E21 – Lokale HTML-Vorschau wurde zeitweise mit nicht autorisiertem Design angereichert
- In lokalen Vorschauen wurden zeitweise visuelle Regeln ergänzt, die nicht als autoritativer Produktionsstand belegt waren (u. a. zusätzliche H2-Akzentlinie/Fazit-Darstellung).
- Danach wurden bei Korrekturversuchen zunächst zu viele Überschriftenlinien verändert und eine Nutzerbeanstandung „fehlender Fließtext vor Fazit“ fälschlich als reines Abstandsproblem interpretiert.
- Diese lokalen Preview-Artefakte sind **keine Designautorität**.
- Verbindliche Konsequenz: neue Vorschau ausschließlich aus dem verifizierten Artikelbody + autoritativem aktuellem Plugin-CSS erzeugen; keine eigenen Designentscheidungen.

### E22 – Unbelegte Chat-Status-/PR-Behauptungen
- Im Chat wurden zwischenzeitlich Repo-Zustände behauptet, die zu diesem Zeitpunkt nicht verifiziert waren, darunter ein angeblicher PR #494 sowie später ein angeblicher PR #498/Status.
- Ebenfalls wurde einmal behauptet, Current sei aktualisiert, obwohl noch kein entsprechender Repo-Write erfolgt war.
- Diese Behauptungen sind **keine Evidence** und dürfen nicht als Projektstand verwendet werden.
- Verifizierte relevante Repo-Fakten sind stattdessen:
  - Freshness-Reparatur: PR #499 / Merge-Fix `2d10588eb500490c3c36c05ce2e56700b5145385`;
  - Rendering-Main-Head: `f853fb61384385fb97d5de020b7ea6903890ea35`;
  - frischer Testartikel-Produktionscommit: `2e515462a425f826aa711fca2dda53058891e58b`.
