# K10 – Arbeits-, Entscheidungs- und Fehlerhistorie bis 2026-10-02

**Rolle dieses Dokuments:** ausschließlich Historie/Nachweis.  
**Keine Current-Autorität. Keine NEXT-ACTION-Quelle.**  
Aktueller Stand steht ausschließlich in `CURRENT_STATE.json`.

## Ziel und Grundentscheidung

K10 wurde als strikt getrenntes Entwicklungsmodell neben dem funktionierenden K9 aufgebaut. K9 darf nicht verändert werden. Ziel ist ein zentraler Regelkatalog nach dem Prinzip:

**eine harte Regel → genau ein fachlicher Owner → genau eine inhaltliche Prüfung → genau ein hashgebundener Receipt.**

Nachgelagerte Stufen prüfen nur Vollständigkeit, Identität, Hash-Bindung und Unverändertheit; sie bewerten dieselbe redaktionelle Regel nicht erneut.

Der normale Produktionsendpunkt ist eine **verifizierte WordPress-Importdatei mit `publish_allowed=false`**. Ein echter WordPress-Write/Render gehört nicht zum normalen K10-Lauf.

## Dauerhafte fachliche Entscheidungen

- Tabelle:
  - `Vergleich`: Tabelle Pflicht.
  - `FAQ`, `Beratung`, `Pflege`: Tabelle optional.
  - Wenn Tabelle vorhanden: echter Informations-/Entscheidungsmehrwert erforderlich.
  - Bei optionaler Tabelle muss die Entscheidung ausdrücklich als `INCLUDE_ADDED_VALUE` oder `OMIT_NO_ADDED_VALUE` mit Begründung festgehalten werden.
- H2:
  - konkrete, abschnittsspezifische Sprache;
  - abstrakte Generatorformulierungen werden hart blockiert.
- Einstieg:
  - jeder Artikel beginnt mit einem kurzen natürlichen Orientierungssatz;
  - er erklärt sofort, worum es geht, was die Sache ist oder welchem Zweck sie dient;
  - keine starre Definitionsformel;
  - Ziel für die gesamte Einleitung: 60–80 Wörter; harter bestehender Maximalwert bleibt unverändert.
- Qualität:
  - keine Qualitätsabsenkung;
  - LT 6.8, PPM-6.7.9-Regelbestand, PSERC, ENDSTEMPEL und WordPress-Dateiverifikation bleiben erhalten;
  - `publish_allowed=false`.

## Architektur-/Implementierungsnachweise

- K10 eigener Branch: `konzept10-rule-ledger-20261001`.
- K9-Baseline nur read-only: `2cc8167fa1e31b4ffa2ff76c9819314be4b98555`.
- K10-Dateibaum ohne K9-Runtime, K9-Artikel, K9-Warehouse, K9-Final oder K9-Submissions.
- PPM 6.7.9 direkt aus dem hashgebundenen Paket inventarisiert.
- Exakte historische PPM-Summe reproduziert: **52 Content + 34 Struktur + 14 Known Error + 4 Render = 104 Regeln**.
- Die 104 PPM-Regeln wurden auf K10-Owner gemappt; alte starre Tabellenpflichten wurden ausschließlich durch die ausdrücklich genehmigte K10-Tabellenregel ersetzt.
- Hashgebundene Article-/System-/Package-Receipts implementiert.
- Artikelzustand bindet Titel, Keyword, Typ, Metadaten, Faktenbindung und HTML; relevante Änderung invalidiert alte Receipts.

## Fehler- und Reparaturprotokoll

### 1. K10-Trennung / Materialisierung

**Befund:** Direkte K10-Branch-/Dateineuanlage war anfangs durch den GitHub-Sicherheitsweg blockiert.  
**Folge:** Keine unsaubere Arbeit im K9-Branch. K9 wurde zunächst auf den sauberen Stand `2cc8167...` zurückgesetzt und danach nicht mehr verändert.  
**Lösung:** separater K10-Branch und eigener Dateibaum.  
**Belege:** K10-Root `c93bf55...`, Materialisierung `3ee2684...`, aktueller K9-Head blieb `2cc8167...`.

**Befund:** Isolation Guard schlug beim Bootstrap/Workflow auf Git-Metadaten bzw. notwendige read-only Referenzen an.  
**Lösung:** aktive K9-Arbeitsinhalte bleiben verboten; Git-Metadaten/read-only Baseline-Referenzen wurden aus der aktiven Mutationsprüfung herausgenommen.  
**Belege:** `245a3afd...`, `7222d0ea...`, `dadfe9e4...`.

### 2. PPM-104-Inventur

**Befund:** Erster Extraktor zählte rohe Validator-Aufrufstellen statt semantisch eindeutiger Regeln; Content-Validator ergab dadurch 63 statt der historischen 52.  
**Ursache:** dieselbe Regel kommt in mehreren Prüfpfaden vor.  
**Lösung:** Regelidentität = eindeutige Kombination aus Fehlercode + fehlgeschlagener Regel.  
**Beleg:** `acf2aa4f...`; danach exakte Kontrollsumme 52+34+14+4=104.

**Befund:** Regex für PPM-Konstanten war doppelt maskiert und konnte Originalwerte nicht extrahieren.  
**Lösung:** Regex korrigiert, Originalgrenzwerte aus dem echten gebundenen PPM-Paket übernommen.  
**Belege:** `f1f0f543...`, `0637401d...`.

### 3. Doppelte Prüfpfade

**Befund:** Während der K10-Zentralisierung entstanden zeitweise doppelte Prüfpfade/Receipts, u. a. durch zusätzliche PPM-Paritätsprüfung.  
**Lösung:** semantische Doppelprüfung entfernt; pro harter Regel exakt ein Owner und ein Receipt.  
**Nachweis:** Exact-Receipt-Tests in K10-Selftest; Artikel-/Package-Regeln werden auf eindeutige Receipts geprüft.

### 4. Erster Realartikel – Longiergurt

**Artikel:** „Wie lege ich einen Longiergurt an?“  
**Befund:** erste reale LT-Funde mussten sprachlich repariert werden.  
**Lösung:** Text repariert, LT 6.8 anschließend 0 Findings.  
**Beleg:** `ae8d3cb2...`.

**Befund:** Der Lauf wurde zeitweise unnötig bis zu echten WordPress-Renderhaken verfolgt.  
**Entscheidung:** Für den normalen Produktionsweg ist das falsch. Gewollter Endpunkt ist die verifizierte Importdatei; echter WordPress-Write/Render ist nicht nötig.  
**Lösung:** Pre-WordPress-Integrität und spätere Rendergates getrennt; normaler Lauf stoppt nach verifizierter Importdatei.  
**Belege:** `256e732c...`, `dcc2390f...`, `24a2d783...`, `6fe9adc7...`, `6a58e346...`.

### 5. Einleitung und Tabellenentscheidung

**Befund:** Erster Longiergurt-Artikel hatte formal zulässige, mobil aber recht lange Einleitung; außerdem war bei fehlender optionaler Tabelle nicht dokumentiert, ob das bewusst oder versehentlich geschah.  
**Entscheidung:** allgemeiner Orientierungssatz + 60–80-Wörter-Einleitungsziel; explizite Tabellenentscheidung.  
**Implementierung:** `8a390397...`, `b5a04004...`, `3f7c1cae...`, `ed650f04...`.

### 6. Unmöglicher 750-Wörter-Hardlock

**Befund:** K10 hatte alte „nicht mit Tabelle/Fazit künstlich auffüllen“-Flags beim Zentralisieren als zusätzliche harte 750-Wort-Sperre interpretiert. Für Beratung/Pflege/Vergleich war das zusammen mit Abschnittsmaxima rechnerisch teilweise unmöglich.  
**Ursache:** Ziel-/Guidance-Felder wurden zu Hardrules überhärtet; so hatte K9 sie nicht durchgesetzt.  
**Lösung:** echte Qualitätsgrenzen 750–900 Wörter, Abschnittsgrenzen, Fazitgrenzen blieben unverändert. Nur die Padding-Flags wurden zurück zu Writer-Zielen klassifiziert; `exempt_blocks` wurde korrekt dem Owner `words.section_range` zugeordnet.  
**Belege:** `6affa4be...`, `5321e9cf...`, `257c23b0...`, `f98520b4...`, `9e7d1c52...`, `84d31b28...`.

### 7. Dreierlauf – Runner-Abbruch

**Befund:** Der erste Dreier-Runner brach beim ersten LT-Block ab und protokollierte die übrigen zwei Artikel nicht.  
**Lösung:** Runner sammelt alle drei Befunde und stoppt erst nach vollständiger Protokollierung.  
**Beleg:** `a1091705...`.

### 8. Reitplatzplaner – Erstpass

**Befunde:**
- LT: „Glättelemente“ und eine missverständliche Formulierung;
- Fact-Trace in Tabellenzellen zu knapp;
- eine H2 zu abstrakt;
- später noch „zurückverteilt“ als LT-Fund.

**Lösungen:** sprachliche Reparatur, konkretere H2, Faktbindung/Tabellenformulierungen präzisiert.  
**Belege:** `96989eaf...`, `34ef52c6...`, `3a4b5317...`.

### 9. Regendecken – Erstpass

**Befunde:**
- unglückliche Link-Satzkonstruktion in LT;
- Orientierungssatz traf das Thema technisch nicht robust genug;
- abstrakte H2 mit „einordnen“;
- nach Reparatur 749 sichtbare Wörter, also 1 Wort unter dem harten Minimum.

**Lösungen:** Link-Satz neu formuliert, Einstieg klar auf „Regendecken“ bezogen, H2 konkretisiert, sicherer Abstand zur 750-Wort-Untergrenze geschaffen.  
**Belege:** `3485450e...`, `c5df173e...`, `2b915f57...`.

### 10. Schermaschinen – Erstpass

**Befunde:**
- mehrere legitime Fachwörter fehlten in der LT-Fachwortliste;
- „Wattzahl“ und eine Wiederholung wurden sprachlich verbessert;
- echte Quelle „CAVALLO – Schermaschinen im Test“ wurde vom Placeholder-Checker fälschlich als Testquelle blockiert.

**Lösung:** legitime Fachwörter ergänzt; Text verbessert; Placeholder-Prüfung so geändert, dass echte Quellentitel mit dem Wort „Test“ erlaubt bleiben, reine Platzhalter wie „Test“ weiterhin blockieren.  
**Belege:** `96bcfe56...`, `de61b993...`, Regressionstest `fd76e6dd...`.

**Folgefehler:** negativer Placeholder-Schutztest blieb zunächst grün statt zu blockieren, weil die Regex technisch doppelt maskiert war.  
**Lösung:** exaktes Regex-Escaping korrigiert.  
**Belege:** Fehlruns `36938448285`, `36938552197`; Fix `ed3b7269...`; anschließender K10-Selftest PASS.

## Finaler Dreiernachweis

Finaler grüner Dreierlauf:
- Workflow Run: `36938796049`
- getesteter Workload-Commit: `8fa26288c82b6a9d74db5096eb6403f93dbb274f`
- Ergebnis: SUCCESS
- alle drei Artikel:
  - Artikelregeln PASS
  - LanguageTool 6.8: 0 Findings
  - PSERC PASS
  - ENDSTEMPEL PASS
  - WordPress-Importdatei-Verifikation PASS
  - `publish_allowed=false`

Gemessene Maschinenstrecke **nach vorliegendem Artikelinput**:
- Reitplatzplaner: 12.991 s
- Regendecken: 9.271 s
- Schermaschinen: 11.929 s
- Summe: 34.191 s
- Mittel: 11.397 s/Artikel

Die Messung umfasst Category-Binding, LanguageTool 6.8 und K10-Prüf-/Finalisierungsstrecke bis zur verifizierten WordPress-Importdatei.

## Geschwindigkeitsvergleich K9/K10

Ein vollständig fairer End-to-End-Vergleich ist noch **nicht** belegt, weil die K10-Zeit oben mit bereits vorliegenden Artikelinputs beginnt, während der historische K9-Auto-Proof Recherche, Schreiben, mehrere Reparaturrunden und Finalisierung umfasst.

Belegbarer K9-Historienrahmen:
- K9 AUTO Research-Job gestartet: Commit `60e8784c...`, 2026-09-30 11:15:53Z.
- Artikel für AUTO-Proof isoliert: `ccc2eea4...`, 11:20:20Z.
- Terminale WordPress-Datei/STOP: `b16299c4...`, 11:37:52Z.

Damit:
- Research-Job → STOP: ca. **21 min 59 s**.
- isolierter Artikel → STOP: ca. **17 min 32 s**.

Diese Werte sind **nicht direkt** gegen die K10-11.397-s-Prüfstrecke zu rechnen. Sie zeigen aber, warum K10 für die reine Prüf-/Finalisierungsstrecke deutlich schlanker wirkt. Für eine belastbare Gesamtgeschwindigkeit muss K10 künftig Recherche/Schreiben ab einem klar definierten Startpunkt mitmessen.

## Abschluss-Nachweis nach Finalisierung

Nach dem final grünen Dreierlauf wurde `CURRENT_STATE.json` auf den geprüften Stand gezogen. Auf dessen Commit `062615af...` liefen erneut:
- K10 isolated selftest: Run `36975267798` → SUCCESS.
- K10 PPM 6.7.9 inventory: Run `36975267711` → SUCCESS.

K9 blieb auf `2cc8167fa1e31b4ffa2ff76c9819314be4b98555` unverändert.

## Nicht betroffen

- Hobbyraum: nicht verwendet.
- Paul/Worker/Parallelbranch außerhalb des getrennten K10-Branches: nicht betroffen.
- Pluginentwicklung: nicht betroffen.


## Redaktionelle Prüfung der drei final grünen Artikel – 2026-10-02

**Geprüfte Grundlage:** Workflow Run `36938796049`, Artifact `11198898150` (`k10-three-article-optimization`), Workload-Commit `8fa26288c82b6a9d74db5096eb6403f93dbb274f`.

Die drei finalen Endfassungen wurden als normale Artikel gelesen, nicht nur über die Maschinenprotokolle bewertet.

### Reitplatzplaner

- Einstieg: redaktionell PASS.
- H2: redaktionell PASS.
- Lesbarkeit und praktischer Nutzwert: insgesamt PASS.
- Tabellenentscheidung: **FAIL gegen die bereits geltende Tabellenregel**.
- Begründung: Die Tabelle wurde als `INCLUDE_ADDED_VALUE` freigegeben, liefert aber in mehreren Zeilen überwiegend tautologische Wiederholungen, z. B. `Walzen | Einebnung | Einebnung prüfen`, `Hufschlagräumer | Randpflege | Randpflege prüfen` und `Arbeitsbreite | Arbeitsbreite nutzen | Zugfahrzeug prüfen`. Damit ist der behauptete eigenständige Informations-/Entscheidungsmehrwert nicht ausreichend belegt.
- Bewertung: kein neuer Tabellenstandard; vorhandene Mehrwertregel wurde zu schwach durchgesetzt.

### Regendecken

- Einstieg: redaktionell PASS.
- Tabellenentscheidung `OMIT_NO_ADDED_VALUE`: redaktionell PASS.
- Lesbarkeit und praktischer Nutzwert: insgesamt PASS.
- H2-Naturalness: **Befund gegen die bereits geltende H2-Regel** bei `Wärme Feuchtigkeit und Passform direkt kontrollieren`. Die Aufzählung ist sprachlich nicht natürlich genug.
- Bewertung: keine neue Stilregel; vorhandene Regel `NATURAL_CONCRETE_SECTION_LANGUAGE_MUST_BE_HARD_CHECKED` hat diesen Fall nicht zuverlässig abgefangen.

### Schermaschinen

- Einstieg: redaktionell PASS.
- Tabellenentscheidung `OMIT_NO_ADDED_VALUE`: redaktionell PASS.
- Lesbarkeit und praktischer Nutzwert: insgesamt PASS.
- H2-Naturalness: **Befund gegen die bereits geltende H2-Regel** bei `Akku Kabel und Leistung passend abwägen` sowie `Messer Gewicht und Wartung im Alltag prüfen`.
- Bewertung: keine neue Stilregel; vorhandene Naturalness-Prüfung ist für solche Aufzählungsüberschriften zu schwach.

### Scale-Entscheidung

**Entscheidung: `ONE_TARGETED_RETEST_BEFORE_SCALE`.**

Kein größerer K10-Scale-Batch vor einem gezielten Retest derselben drei Artikel.

Grund:
1. Ein als Mehrwert freigegebenes Tabellenartefakt erfüllt die bestehende Mehrwertregel redaktionell nicht zuverlässig.
2. Mehrere H2 bestehen die Maschine, obwohl sie die bereits geltende Naturalness-Regel redaktionell nicht sauber erfüllen.
3. Die Grundarchitektur, LT 6.8, PSERC, ENDSTEMPEL und WordPress-Dateiverifikation bleiben grün; es gibt keinen Grund für Architekturumbau oder Qualitätsabsenkung.

**Keine neue Regel beschlossen. Keine Qualitätsgrenze geändert. Kein K9-Eingriff.**


## Gezielter Editorial-Retest – PASS – 2026-10-02

Nach der redaktionellen Prüfung wurde ausschließlich die bestehende Durchsetzung von `table.value_required_if_present` und `heading.natural_concrete_section_language` geschärft. Es wurde **keine neue Regel** angelegt, kein Owner geändert und kein Qualitätsniveau abgesenkt.

### Reparatur

Commit: `a7a910634e41b9031edb807dbd4fbca54d1e1d20`

- H2-Naturalness: klare unpunktierte Nomen-Aufzählungen wie `Akku Kabel und Leistung ...` werden nun unter dem bereits bestehenden H2-Owner blockiert.
- Tabellenmehrwert: ein vorab gesetztes semantisches PASS reicht nicht mehr aus, wenn die Tabelle überwiegend nur vorhandene Begriffe plus generische Handlungswörter wiederholt.
- Reitplatzplaner-Tabelle wurde inhaltlich auf echte Beziehungen zwischen Kriterium, Hauptnutzen und zusammen zu prüfender Größe umgestellt.
- Regendecken-H2 korrigiert auf `Wärme, Feuchtigkeit und Passform direkt kontrollieren`.
- Schermaschinen-H2 korrigiert auf `Akku, Kabel und Leistung passend abwägen` sowie `Messer, Gewicht und Wartung im Alltag prüfen`.

### Realer Dreier-Retest

Workflow Run: `36978375237`  
Artifact: `11214760852`  
Ergebnis: **SUCCESS**

Alle drei Artikel:
- Artikelregeln: PASS
- LanguageTool 6.8: PASS / 0 Findings
- PSERC: PASS
- ENDSTEMPEL: PASS
- WordPress-Importdatei: PASS
- `publish_allowed=false`

Zusätzliche Belege:
- Reitplatzplaner: `heading.natural_concrete_section_language = PASS`; `table.value_required_if_present = PASS`; `tautological_action_rows = []`.
- Regendecken: korrigierte H2 im Endartefakt; H2-Naturalness PASS.
- Schermaschinen: beide korrigierten H2 im Endartefakt; H2-Naturalness PASS.

Maschinenstrecke im Retest:
- Reitplatzplaner: 17.743 s
- Regendecken: 11.586 s
- Schermaschinen: 14.606 s
- Summe: 43.935 s
- Mittel: 14.645 s/Artikel

### Selbsttest-Zwischenbefund

Der erste isolierte Selbsttest auf `a7a9106...` (Run `36978375274`) war rot, obwohl der reale Dreierlauf grün war.

Ursache: Der neu hinzugefügte positive Tabellen-Test hängte eine zusätzliche Tabelle an einen bereits großen künstlichen Testartikel und überschritt dadurch ausschließlich die unveränderte 900-Wörter-Obergrenze. Die neue Tabellenprüfung selbst war nicht fehlerhaft.

Lösung: Nur die Testassertion wurde isoliert auf den zuständigen Receipt `table.value_required_if_present` begrenzt. Keine Produktionsregel wurde gelockert.

Test-Fix-Commit: `6e0b7be9f28adf31079d8e1cdd370e89a5e8eff7`

Danach:
- K10 isolated selftest Run `36978562825` → **SUCCESS**
- K10 PPM 6.7.9 inventory Run `36978562813` → **SUCCESS / 104 von 104**

### Ergebnis

Der Editorial-Blocker ist geschlossen.  
`first_open_blocker = null`.

Nächste Current-Aktion:
`RUN_ONE_SMALL_K10_LIVE_BATCH_WITH_END_TO_END_TIMING_FROM_RESEARCH_START_TO_VERIFIED_WORDPRESS_IMPORT_FILE`

K9 blieb unverändert. `publish_allowed=false`.


## Frischer realer End-to-End-Test ab Recherche – 2026-10-02

**Artikel:** „Wie oft muss ein Pferdeanhänger zum TÜV?“  
**Typ:** FAQ  
**PSERC-Plan-Slot:** `53c8c859fbbc1b9a2a17ffe53efaf31d74520ac7a89aebc1e84ec9a6ea95ea6f`

### Messstart

Research-Startmarker:
- Commit `1633a766c41a4d878320ae889c702de996306e57`
- GitHub-Zeit: 2026-10-02 08:00:33 UTC
- Scope: frische Recherche → Schreiben → K10-Prüfung → verifizierte WordPress-Importdatei

Die Recherche wurde nach diesem Marker frisch gegen aktuelle Quellen durchgeführt:
- StVZO § 29;
- Anlage VIII StVZO;
- TÜV Rheinland Anhänger-HU.

### Erster realer Durchlauf

Workload-Commit:
`7fb82705177512c8f397dd3a66ece4e546c36e00`

Workflow Run:
`36981858130`

Ergebnis:
**BLOCKED**

Vor dem realen Lauf lokaler Struktur-Preflight:
- 766 Wörter;
- Einleitung 61 Wörter;
- 16 Absätze;
- normale H2-Abschnitte 179 / 171 / 220 Wörter;
- 3 gebundene interne Links;
- 4 Listenelemente;
- optionale Tabelle bewusst `OMIT_NO_ADDED_VALUE`.

Im realen Lauf:
- PSERC-Bindung: PASS
- WordPress-Kategorie live: PASS / ID 1061
- LanguageTool 6.8: PASS / 0 Findings
- Block bei Artikelregeln:
  - `facts.conclusion_no_new_untraced_facts`
  - `facts.numeric_claim_supported`

Gemessene Zeit bis zum Block:
**187.291 ms = ca. 3:07 min**

### Ursache und Reparatur

Kein K10-Systemfehler.

Der Artikel selbst war an vier Stellen nicht exakt genug an die gebundenen Fakten gekoppelt:
- „750 Kilogramm“ statt des im Fakt gebundenen „0,75 Tonnen“;
- im Fazit fehlte der sichtbare F6-Trace;
- „§ 29“ war als zusätzliche Zahl im Fließtext nicht durch den dort gebundenen F5-Fakt abgedeckt.

Die harten Gates haben diese Abweichungen korrekt geblockt.

Reparatur:
- Einheiten exakt auf `0,75 Tonnen` gebunden;
- fehlenden F6-Trace ergänzt;
- „§ 29 StVZO“ im Fließtext ohne Informationsverlust zu „die StVZO“ vereinfacht.

Repair-Preflight:
- numeric_bad = []
- untraced_conclusion = []

Repair-Commit:
`147e62ab3d2668edfee8c477ca0290de7dd35c5d`

### Zweiter realer Durchlauf

Workflow Run:
`36982026936`

Artifact:
`11215459134`

Ergebnis:
**SUCCESS / READY_FOR_WORDPRESS_DRAFT_IMPORT**

Final:
- LanguageTool 6.8: PASS / 0 Findings
- Artikelregeln: PASS
- Systemregeln: PASS
- PSERC: PASS
- ENDSTEMPEL: PASS
- WordPress-Dateiverifikation: PASS
- `publish_allowed=false`

Maschinenstrecke im finalen Lauf:
- LanguageTool: 9.170 s
- K10-Proof: 1.270 s
- gesamte Validierung: **10.440 s**

Gemessene reale Wandzeit vom Research-Startmarker bis zur final verifizierten WordPress-Datei:
**287.955 ms = ca. 4:48 min**

Diese 4:48 Minuten enthalten ausdrücklich:
- frische Recherche;
- Artikelerstellung;
- ersten realen Block;
- Fehleranalyse;
- Reparatur;
- zweiten vollständigen Lauf;
- verifizierte WordPress-Importdatei.

### Vergleich mit K9

Historisch belegter K9-Wert:
- Research-Start → STOP: ca. **21:59 min** = 1.319 s

Aktueller K10-Wert:
- frische Recherche → verifizierte WordPress-Datei inklusive einer Reparaturrunde: ca. **4:48 min** = 287,955 s

Beobachtetes Verhältnis:
- K10 in diesem Test ca. **4,58× schneller** als der belegte K9-Research-Start→STOP-Lauf.

Einschränkung:
Die K10-Recherche und das Schreiben wurden in diesem Chat interaktiv durchgeführt, nicht durch eine vollständig autonome GitHub-Research/Writer-Kette. Der Vergleich ist deshalb deutlich aussagekräftiger als die frühere 10–15-Sekunden-Prüfstrecke, aber noch nicht vollkommen identisch zur K9-Automation.

### Bewertung

**Weiterarbeit an K10 ist nach diesem Test sinnvoll.**

Begründung:
- echter frischer Artikel;
- harte Gates haben reale Faktenbindungsfehler korrekt gestoppt;
- eine Reparaturrunde genügte;
- final alle Qualitätsgates grün;
- trotz Reparatur vollständige Wandzeit unter fünf Minuten;
- K9 blieb unverändert auf `2cc8167fa1e31b4ffa2ff76c9819314be4b98555`.

Aktueller Blocker:
`null`

Nächste Current-Aktion:
`RUN_ONE_SMALL_MULTI_ARTICLE_K10_BATCH_FROM_FRESH_RESEARCH_AND_MEASURE_FIRST_PASS_RATE_AND_END_TO_END_VARIANCE`


## K10 Optimierung nach realem E2E-Test – 2026-10-02

### Ziel

Ohne Qualitätsabsenkung und ohne Architekturwechsel wurden die drei im realen Lauf sichtbar gewordenen Optimierungspunkte geschlossen:

1. vereinfachten Vorabcheck durch die echten K10-Regel-Owner vor LanguageTool ersetzen;
2. fehlende Source-Traces deterministisch aus bereits gebundenen Fact-IDs und Research-Claims materialisieren;
3. LanguageTool 6.8 für Mehrartikelläufe in einem einzigen Java-Prozess ausführen.

### Implementierung

Kerncommit:
`4135fab77e9f258be435acafe66d240f7ce6d1b1`

Testkorrektur:
`e35b7635c26ae86aa0be60a11cabfcd78b30dbb2`

Workflow-Bindung:
`d8ddb52914a1401d0a96fcad9e8a0e3b9120829e`

Historische Altlast aus automatischer Regression genommen:
`90f1d77e9feaf1c7fbf0f6d7a6a3246a77a03607`

### Exakter Preflight

Neu: `engine/preflight.py`

Der Preflight verwendet dieselben K10-Artikelchecker und erzeugt deren normale hashgebundene Receipts bereits vor LanguageTool.

Nach LanguageTool werden diese Content-Regeln nicht erneut inhaltlich geprüft. Der finale Proof übernimmt die Preflight-Receipts, ergänzt ausschließlich den echten LT68-Receipt und prüft danach Identität, Hash, Vollständigkeit und Status.

Damit bleibt das K10-Prinzip erhalten:
**eine harte Regel -> ein Owner -> eine Inhaltsprüfung -> ein Receipt**.

Positiv-/Negativtests:
- unsupported numeric claim wird vor LT68 geblockt;
- fehlender Conclusion-Trace wird deterministisch aus vorhandenem Fact-ID/Claim ergänzt;
- sichtbarer Text bleibt dabei unverändert;
- Preflight-Receipts + echter LT-Receipt ergeben einen vollständigen Artikel-PASS;
- LT-Batch ruft die Engine bei mehreren Artikeln genau einmal auf;
- Cross-Boundary-LT-Finding blockiert fail-closed.

### Realer Einzeltest nach Optimierung

Run:
`36986342204`

Artifact:
`11218105119`

Artikel:
„Wie oft muss ein Pferdeanhänger zum TÜV?“

Ergebnis:
**READY_FOR_WORDPRESS_DRAFT_IMPORT**

Nachweise:
- Preflight: PASS / 217 ms
- LanguageTool 6.8: PASS / 0 Findings / 13.906 ms
- finaler Proof: PASS / 712 ms
- Content-Recheck nach Preflight: false
- PSERC: PASS
- ENDSTEMPEL: PASS
- WordPress-Dateiverifikation: PASS
- publish_allowed=false

### Realer Dreierlauf mit einem LanguageTool-Prozess

Run:
`36986342158`

Artifact:
`11217332231`

Alle drei Artikel:
- Reitplatzplaner: PASS
- Regendecken: PASS
- Schermaschinen: PASS

Alle:
- Preflight: READY_FOR_LT68
- LT68: PASS / 0 Findings
- Artikelregeln: PASS
- Systemregeln: PASS
- PSERC: PASS
- ENDSTEMPEL: PASS
- WordPress-Dateiverifikation: PASS

Messwerte:
- Preflight gesamt: 630 ms
- LanguageTool Batch für 3 Artikel: 21.571 ms
- LanguageTool Java-Prozesse: **1**
- Proof gesamt: 1.961 ms
- Validierungskern gesamt: 24.162 ms

Der ältere Dreierlauf lag bei 43.935 ms für seine damalige Maschinenstrecke. Die Scopes sind nicht vollständig identisch, weil der alte Wert Category-Binding enthielt und der neue Kernwert nicht; die Richtung der Einsparung durch einen LT-Prozess ist dennoch real belegt.

### Historischer Workflow

Run `36986523354` des alten Longiergurt-Snapshots wurde durch aktuelle Regeln bei
`table.optional_decision_documented`
geblockt.

Das ist kein Current-Fehler: Der historische Input stammt aus der Zeit vor der verpflichtenden optionalen Tabellenentscheidung. Der Snapshot wurde nicht nachträglich verändert. Stattdessen ist `.github/workflows/k10-first-real-e2e.yml` jetzt nur noch manuell/historisch und kein automatisches Current-Regressionsgate mehr.

### Abschlussprüfung

Finale Tests auf Commit `90f1d77e9feaf1c7fbf0f6d7a6a3246a77a03607`:
- isolated selftest Run `36986680834`: PASS
- PPM 6.7.9 inventory Run `36986680960`: 104/104 PASS
- K9 Head unverändert: `2cc8167fa1e31b4ffa2ff76c9819314be4b98555`
- publish_allowed=false
- first_open_blocker=null

### Nächster Schritt

`RUN_INDEPENDENT_NEIGHBOR_CHAT_TEST_WITH_FRESH_EXACT_FIVE_FIELD_WORDPRESS_INPUT_AND_K10_START_COMMAND`
