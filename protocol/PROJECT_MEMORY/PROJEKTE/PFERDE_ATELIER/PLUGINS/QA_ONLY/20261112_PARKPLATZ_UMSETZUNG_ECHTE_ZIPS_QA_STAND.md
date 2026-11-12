# Pferdeatelier Parkplatzkonzept – tatsächliche QA-Umsetzung (12.11.2026)

## Verbindliche Ausgangslage
Ein Produktionslauf zur Zeit, **keine externen Änderungen**. Ein vorhandener aktueller Redaktions-/Parkhausplan, ein freier Platz, eine einzige zentrale fachliche Freigabe pro Thema. MINI/externe Agenten sind Teil des Serienproduktionswegs. Beim Rücklauf das Originalergebnis nur technisch zuordnen; K0 schreibt und kontrolliert den **Artikeltext**. Nach WordPress-Import genau diesen Platz im vorhandenen PPM-Planregister abschließen; erst danach nächsten Lauf. Bei Abbruch gespeicherten Stand behalten und fortsetzen, keine neue Fachentscheidung.

Vertrag: [VERBINDLICHES_PARKPLATZKONZEPT_EINZELLAUF](20261112_VERBINDLICHES_PARKPLATZKONZEPT_EINZELLAUF.md). **Nicht** die bisherige MINI-Produktionsstrecke beseitigen und nicht die bisherigen 81 K0-Inhaltsregeln abschalten.

## IST – nachgewiesene strukturelle Doppelstellen (Quelle vor jeder Korrektur)
1. `PSTE_Mini_Workflow::forwardToPlan`: nach externem MINI-FREI-Rückimport nochmals **alle Artikel und alle Plätze** lesen und den Gesamt-Hash mit dem bereits gebundenen Nachweis vergleichen. Während eines einzelnen, unveränderten Produktionslaufs widersprüchlich und ein zweiter Vollplan-Check.
2. `PSTE_Mini_Workflow::readExistingPsercPlanForParkhaus`: vorhandenen signierten vorherigen Plan nicht einmal als **Beleg früherer Reservierungen** anerkennen, wenn globaler späterer PSERC-Wiederaufnahme-/WP-Stand seinen Frische-Hash ändert. Dadurch nach normalem Artikelimport alter Reservierungsbeleg nicht mehr lesbar.
3. `PSTE_Repository::applyPoolRowWithRelations`: selbst beim **Lesen** eines bereits signierten und als frei markierten MINI-Platzes konnte `automaticPoolStatus`, `classifyRole`, `planningSuitability` erneut aufgerufen und die sichtbare Freigabe downgraden.
4. `PSERC_Plan_Dependency_Fingerprint::current`: technische Fortschritts- und Jobstatus-Felder im Quellplan-Hash. Veränderter Job, aber kein inhaltlich anderer Plan, führte zu Sperre.
5. `PSERC_Compiler::compile` und `PSERC_Plan_Compile_Job::tickCandidate`: vorhandener PSTE-SEO-/Belegtheitsentscheid wurde nur im MINI-Sonderfall als abgeschlossen erkannt; bei nachweislich bereits erledigter normaler PSTE-SEO-Freigabe zweite semantische Duplikatprüfung möglich.

## KONKRETE Codeänderung, vorhandene Klassen, keine Zusatzarchitektur
**PSTE 0.57.144.46** von signierter QA-.45, nur 3 Quelldateien:
- `includes/class-pste-mini-workflow.php`: `forwardToPlan` übernimmt nach beim vorangehenden `acceptSingleOwnerSeoDecisions` bereits geprüften externen SEO-Bescheid. **Keine zweite vollständige Bestands-/Planlesung.** Prüft weiterhin Originalquelle, signierten Planstand und eindeutige Intent-Slot-Kennung; kaputter oder fehlender Beleg bleibt HELD.
- Ebenda `readExistingPsercPlanForParkhaus`: gültigen unveränderten **früheren signierten** PSERC-Plan zur Bestandsinventur lesen. Es gibt eine Kontrolle, ob der Inhalt beim Lesen gleich blieb. Der **aktuelle WordPress-/PPM-Artikelbestand** wird separat eingelesen; kein Entfernen der Belegungssicherheit.
- `includes/class-pste-repository.php`: beim Nur-Lesen eines mit gültigem MINI-FREI-Bescheid **bereits genehmigten, unveränderten** Topics die vorhandene Freigabe übernehmen, nicht semantisch neu beurteilen. Fehlende/veränderte Originalbelege gehen durch den bisherigen konservativen Ablauf.
- Versionskopf `.46`.

**PSERC 0.28.70** von signierter QA-.69, 6 Dateien:
- `includes/class-pserc-plan-dependency-fingerprint.php`: reine Worker-/Jobstatus-/Generationsänderungen aus Plan-Quellfingerprint entfernt. **Echte** Struktur-/WP-/Redaktionsplanänderungen bleiben erkennbar.
- `includes/class-pserc-seo-reader.php`: erkennt auch einen **echten abgeschlossenen** PSTE-Planungsfreigabebeleg ohne MINI-Ausnahme als `upstream_central_coverage_decided`, nur bei PASS plus beiden dokumentierten bestandenen ursprünglichen Belegtheitskontrollen. Fehlender, gescheiterter oder unvollständiger Altbeleg bekommt keine automatische FREI-Freigabe.
- `includes/class-pserc-compiler.php`, `includes/class-pserc-plan-compile-job.php`: für diesen autorisierten bereits entschiedenen Fall keine weitere PSERC-Semantik-Doppelprüfung. Sonst altes konservatives Schutzverhalten.
- Version und **echtes Paketmanifest neu gebunden**.

**Nicht geändert:** WordPress-Seite, WordPress-Core, MINI externe Agenten, K0-Code, 81 Artikel-/Sprachqualitätsregeln, PPM-Abschluss- und Importlogik, vorherige Fallback-Archive.

## Ausgelieferte QA-ZIP-Bytes – exakter Testgegenstand
- `PSTE-0.57.144.46-PARKPLATZ-EINZELLAUF-NUR-QA.zip` = SHA-256 `e3461e7bdf8a30eb30f16e445e02499dafaebb496171f53900c068564682352c`; **121 Dateien**, 653424 Bytes.
- `PSERC-0.28.70-PARKPLATZ-EINZELLAUF-NUR-QA.zip` = SHA-256 `0367fad3be41ac2a79e37397fb9b9e39f787956a887413c951b30f1dc2125c1a`; **63 Dateien**, 269859 Bytes.
- Beide finalen ZIPs frisch in einen **leeren** Ordner entpackt und sämtliche **184 Dateien bytegenau** gegen bearbeitete Quelle geprüft, ZIP CRC jeweils OK.
- **126/126 PHP-Syntaxprüfung PASS**. Echte `PSERC_Package_Integrity::validate` vom neu entpackten ZIP **61/61 PASS**.
- Native, anhand neu ausgepackter Original-Methoden ausgeführte positive/negative PHP-Fälle (WordPress-Daten nachgebaut): gültige MINI-Rückgabe ohne erneutes Planlesen; verfälschte Quelle/Intent-Slot nicht weiterleiten; alter unveränderter PSERC-Plan wird gelesen, beschädigter/verschwindender/beim Lesen geänderter nicht; geänderte Job-IDs ändern nicht den Plan, aber geänderte WP-/Plan-/Strukturquellen schon; richtige PSTE-Owner-Freigabe vermeidet PSERC-Zweitsemantik, fehlender Beleg fällt auf Originalprüfweg zurück; signierter MINI-Platz beim Lesen ohne Neuentscheidung, ungültiger Beleg ohne Freigabe. **Alle Testskripte Exit-Code 0.**
- Bestehender früherer Original-/Simulations-Workflow erneut auf **neue** ZIP-Dateien umgeleitet: **64/64 PASS** (3 historische Themen, 3 simulierter K0-Draft-Output, Web/Provider/WordPress nachgebaut).
- Tests wurden **an der tatsächlichen installierbaren ZIP**, nicht nur an einer anderen Arbeitskopie, ausgeführt.

## Was ausdrücklich noch NICHT bewiesen / geändert ist
- **Keine Installation auf der vorhandenen WordPress-Testseite**, kein echter 5.016-Themen-Datenbanklauf, keine tatsächlichen K0-Artikeltexte 2/3, kein WordPress-Import während dieser QA.
- **Reservierung der fertigen PSERC-`plan_slot` schon VOR dem externen MINI-Lauf ist in dieser QA noch nicht belegt**: Es gibt den ursprünglichen externen MINI-`intent_slot` und später den PSERC-`plan_slot`; sie dürfen nicht ohne Nachweis als identisch behauptet werden.
- **Persistente Wiederaufnahme bei Abbruch jeder Agenten-Stufe** bislang nicht als vollständiger E2E-Fall bewiesen. Nutzer wollte Abbruch separat betrachten, aber den letzten Zustand sichtbar halten.
- Alter, durch früheren 5.000er-Lauf ggf. gelöschter READY-Datenbankzustand wird durch diese ZIPs nicht automatisch wiederhergestellt. Keine unbewiesene künstliche Freigabe.
- WordPress-Import schreibt bestehende PPM-Redaktionsplanmeldung, aber noch kein Live-Nachweis, dass nächster vollständig serieller Lauf **genau diesen erledigten Platz** nicht neu besetzt.
- Deshalb **QA ONLY – nicht auf der produktiven Website installieren und nicht „voller Produktionsworkflow funktioniert“ behaupten**.

## Ablage
Echte ZIPs und exakte Quellcode-Patches im persistenten Library-Ordner `/pferdeatelier/PLUGINS/QA/`. Dieser Bericht im bestehenden GitHub-Branch. Original .45/.69 sowie frühere Versionen bleiben erhalten; keine zweite Freigabeautorität, keine neue Tabelle, kein neues Plugin.
