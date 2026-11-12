## VERBINDLICHE KLARSTELLUNG: Doppelte Keywords und verschiedene Suchabsichten – 12.11.2026

**Kein neues Konzept, sondern Rückgriff auf bereits beschlossenen Vertrag.** Nachweis im Zielvertrag [Kistenprinzip vom 07.11.](../EVIDENCE/PSTE_KISTENPRINZIP_VERBINDLICHER_ZIELVERTRAG_20261107.md), Abschnitt „Genau vier Kisten“, Nummer 4: **„Umformulieren ist nur erlaubt, wenn eine tatsächlich andere belegbar freie Suchintention entsteht; bloßes Umtiteln eines belegten Themas belegt keinen neuen Parkplatz. Bei geändertem Bedeutungsziel: neue Version desselben Falls zurück in die gleiche zentrale Prüfung, nicht in einen zweiten Gate.“** Auch der Eigentümervertrag [Gesamtworkflow](../EVIDENCE/PSTE_KISTEN_GESAMTWORKFLOW_OWNERSCHAFT_20261107.md) untersagt eine weitere Instanz und erlaubt eine belegbar andere Suchabsicht. Frühere User-Beschlusslage (28.10.) bestätigt: **gleicher Informationsbedarf = ein Artikel; anderer Informationsbedarf = eigener Artikel**.

### KISS – Umsetzung durch genau den einen vorhandenen zentralen Themenentscheider, VOR MINI

1. Ein Keyword kommt an; der zentrale Entscheider sieht **den vollständigen vorhandenen Artikel-/Planbestand und die übrigen neuen Themen im Stapel**.
2. **Wenn die gesuchte Antwort bereits vollständig abgedeckt ist:** dieser Suchabsicht **BELEGT** zuordnen, **kein** weiterer Artikelplatz.
3. **Wenn tatsächlich eine andere Frage / Beratung / ein anderer Vergleich dazu nachweislich einen anderen Informationsbedarf bedient:** genau **diese andere konkrete Suchabsicht** als neue Version **desselben Falls** im **gleichen zentralen Entscheidungsdurchgang** mit dem Bestand vergleichen. Wird sie als eigenständiges Thema bestätigt → **FREI**, passende Kategorie/Art und einmaliger Artikelplatz. Bei fehlendem Beleg → **KLÄRUNG**, nicht automatische Freigabe.
4. Eine andere **Artikelart**, ein Fragezeichen oder ein anderer **Titel allein** machen aus demselben Informationsbedarf **kein** neues Thema. Keine künstliche Umdeklaration nur um BELEGT zu umgehen. Beide dürfen auch in **einem** guten Artikel beantwortet werden, falls die Suchabsicht dieselbe ist.
5. Erst **nach** der endgültigen zentralen Entscheidung und Reservierung erhält der externe MINI-Titelworker **genau einen** gebundenen Titelauftrag. MINI, PSERC und K0 ändern diese Fachentscheidung nicht.

**Kinderleichtes Beispiel:** „Regendecke ohne Füllung“ und „ungefütterte Regendecke“ fragen zunächst nach demselben Ding → **ein** Artikel. „Was bedeutet 0g bei einer Regendecke?“ (*Begriff erklären*) versus „Welche 0g-Regendecke ist bei Dauerregen geeignet?“ (*konkrete Auswahl/vergleichende Beratung*) **können** zwei eigenständige Artikel sein, **wenn** die Keyword-/Bestandsanalyse den unterschiedlichen Leserbedarf bestätigt. Ohne diesen Nachweis nicht künstlich zwei Artikel erzeugen.

### Was davon nachweislich schon umgesetzt ist / noch nicht

- **Schon dokumentiert und zwingend:** Ein anderer tatsächlicher Suchintent ist möglich, aber muss **vom gleichen zentralen Verantwortlichen** belegt werden; keine zweite Prüfung in PSERC und keine Intent-Erfindung durch MINI. Der bestehende `PSTE_Runner::applyInternalDuplicates` kann innerhalb eines Recherchepakets Kandidaten sperren.
- **Bisher nicht belegt/noch offen:** Der aktuelle PSTE-Workflow hält diese Alternativentscheidung durchgehend als finale gebundene Version fest und erstellt nur **einen** Auftrag je tatsächlicher Suchabsicht. Die Original-PHP-Probe hat außerdem Titel-Fallback bei der Dublettenbestimmung gezeigt; das ist **kein** verlässlicher Ersatz für die schon vor MINI vorzunehmende Intententscheidung. Keine Statusmeldung „im Plugin repariert“.
- **Nur genau die bestehende Aufgabe zu Ende bringen:** bereits vorhandene Einmal-Intententscheidung einschließlich Alternativ-Intent desselben Falls abschließen und gebunden weiterreichen, passenden Platz **vor MINI** dauerhaft reservieren; alle nachfolgenden fachlichen Zweitentscheidungen beseitigen, sobald die **echte** Übergabe geschützt ist. Keine neue Prüfstation, kein neuer Worker, keine neue Datenbank, kein pauschaler Neustart der Alt-Keywords.

**Prüfstatus:** Diese Protokollkorrektur folgt direkt den wörtlichen bestehenden Zielvertragsstellen, **kein Programmcode geändert und kein WordPress-Test behauptet**.

---

> **Präzisierung der Platzvergabe nach vollständiger Codeprüfung (12.11.2026):** Die frühere Probe „zweimal unabhängiger Aufruf des nackten `PSERC_Slot_Allocator::allocate` liefert denselben Platz“ ist **kein Beweis**, dass der tatsächliche durchgängige PSERC-Lauf denselben Platz zweimal vergibt. Im realen vorhandenen `PSERC_Plan_Compile_Job::tickSlot` werden `occupied_ids` **plus** `reserved_ids` jeder Zuteilung mitgegeben, die erfolgreiche neue `canonical_article_id` in `reserved_ids` aufgenommen und mit `PSERC_Plan_Snapshot_Store::putJob` in WordPress gespeichert. Laufabschluss aktiviert einen Snapshot, die READY-Zuordnungen werden gesondert gespeichert. **Damit besteht innerhalb desselben fortgesetzten Planlaufs bereits der Schutz vor doppelter Slot-Vergabe. Nicht neu programmieren.** Offen bleibt die ausdrücklich vereinbarte **Vorverlegung** der verbindlichen Reservierung auf **vor MINI** und ihre Haltbarkeit über **getrennte** Aufträge/Neustarts bei geänderten WP-Plänen; das ist mit einer einzelnen Allokatorprobe nicht widerlegt oder bewiesen. Nur hierfür den vorhandenen Speicher-/Auftragsbesitzer prüfen, keinen zweiten Platzwächter schaffen.

> **Präzisierung Titel-Fallback:** `PSTE_Runner::duplicateSignature` baut sowohl aus Originalsuchfrage als auch aus `PSTE_Editorializer::displayTitle` Vergleichsdaten. In `sameAnswerIntentSignature` kommt **zuerst** der Suchfragenvergleich und **falls der keine Gleichheit erkennt** ein **zweiter Vergleich anhand des formulierten Titels**; `sameAnswerIntent` bei leerer Kategorie ähnlich. Damit kann die Textformulierung eine ursprüngliche Themenentscheidung verändern. Für die vereinbarte Vor-MINI-Entscheidung muss die vorhandene zentrale Intentbewertung sich nach **Keyword/Suchabsicht und Bestand**, nicht nach dem erst später formulierten Titel richten. Der Titelarbeiter darf danach nur Sprache/Titelqualität verantworten.

# Verbindlicher Endvertrag – ursprüngliche JA/NEIN/VIELLEICHT-Rolle, Ist-Abgleich, Risikobeweis

**Stand: 12.11.2026.** Maßgeblich ist die letzte ausdrücklich bestätigte **Soll-Folge des Nutzers**, nicht die uneinheitlich formulierten früheren Zwischenkonzepte. Keine parallelen Pluginstände; Originale und aktuelle Arbeitskopie sind weiterhin der eine, unveränderte private QA-Stand.

**Geprüftes Originalarchiv:** `AKTUELLER_ARBEITSSTAND_TESTIDENTISCH_NICHT_INSTALLIEREN.zip` SHA-256 `8fc55bca1fc7e4fe019203b2c56d169a734f0c3c941b08606fa9bed6b9183e33`. PSTE .45 und PSERC .69 als unveränderte Originale darin. Die **zwei vorher bereits lokal korrigierten** Stellen bleiben unverändert. In dieser Prüfung **keine neue Plugin-Datei, kein WP-Eingriff und keine Änderung an MINI-/K0-Programmen**.

## 1. Ur-Bedeutung JA / NEIN / VIELLEICHT – nicht mit Kategorien verwechseln

- Originaler MINI-Titelvertrag `mini-title-gate/START_HERE.md` auf GitHub-Zweig `feature/mini-title-gate-independent-v1-20261104`: `MINI:start` begann mit **Keyword-Rohdatei und JA/NEIN/VIELLEICHT-Zuordnung**. Nur JA bekommt Titel. 100 Originalfragen: 87 JA, 9 VIELLEICHT, 4 NEIN.
- Aktuelle Originalprogrammquelle `Portal SEO Topic Engine/includes/class-pste-mini-workflow.php`, `createBatch` Z. 359–366: wörtlich **„Worker 1 entscheidet JA/NEIN/VIELLEICHT. Nur JA geht an Worker 2.“** Ein separater Kommentar erläutert **Relevanzworker erhält nur Rohfragen** (Z. 386).
- **Daraus folgt:** Diese drei Ergebnisse kennzeichnen die **Portalrelevanz** einer Suchanfrage, **nicht** Hauptnavigation/Magazin/Redaktionsbüro und auch **nicht** die endgültige Dubletten-/Artikelplatzfreigabe.
- Die Kategorieentscheidung hat im selben Plugin **andere** Aktionen: `class-pste-admin.php` Z. 518–519: `ROUTE_FACH` (Hauptnavigation), `ROUTE_MAGAZIN` (Magazin), `ROUTE_REVIEW` (Redaktionsbüro ohne Produktionsfreigabe). Beides war in Antworten fälschlich vermischt worden.
- **Normative Änderung aus der letzten Nutzerfestlegung:** Portalrelevanz samt aktueller umfassender Belegung, einheitlicher SEO-/Kategorie-/Artikelartentscheidung und Reservierung werden **vor** MINI einmal durch die vorgesehene zentrale Stelle erledigt. **MINI ist danach ausschließlich die externe Titelwerkstatt**, keine selbständige zweite JA/NEIN/VIELLEICHT-Freigabe und kein Erfinder weiterer Suchabsichten.

## 2. Endgültiger Sollablauf – eindeutiger Verantwortlicher

| Schritt | Zuständigkeit | Genau eine Aufgabe | Keine Wiederholung bei Nachfolger |
|---|---|---|---|
| 1 | WordPress/PSTE Recherche | Originalkeywords und Daten sammeln; keine endgültige Freigabe nur aus dem Rohkeyword | |
| 2 | Zentrale Recherche-/SEO-/Kategorieentscheidung **vor MINI** | Portalbezug JA/NEIN/VIELLEICHT; vollständigen aktuellen Artikel-/Planbestand und neue Themen im Stapel berücksichtigen; **einmalig** FREI/BELEGT/KLÄRUNG, eindeutige Suchabsicht, vorhandene Kategorie und Artikelart festlegen | |
| 3 | Vor-MINI-Artikelplatzvergabe | Auf Basis endgültiger freier Entscheidung mit bestehendem Plan einen passenden **eindeutigen** Artikelplatz **dauerhaft** reservieren; Originalauftrag unverwechselbar speichern | Keine neue SEO-Entscheidung |
| 4 | **MINI außerhalb WP** | **Genau einen** sprachlich passenden Titel zur schon feststehenden Suchabsicht formulieren | Kein JA/NEIN/VIELLEICHT, kein eigener Artikelplatz, keine neue Suchabsicht |
| 5 | Externer Titelprüfer | Titelqualität/Deutsch und Bindung an vorgegebenen Sinn sichern; Fehler innerhalb dieser Werkstatt korrigieren | Keine neue SEO-/Kategorieentscheidung |
| 6 | WordPress/PSERC Redaktionsplan | Fertigen Auftrag mit unverändertem Platz/Zuordnung organisieren; **genau fünf Metadatenfelder** an K0 | Keine fachliche Nachprüfung |
| 7 | K0 Textworker | Artikel erstellen, Sprache/Fakten/Links und geltende Qualitätsregeln prüfen | Keine neue Themenentscheidung |
| 8 | WordPress Re-Import / PPM | Fertigen Artikel am bestehenden Auftrag/Platz einsetzen, Originalzuordnung wiederlesen, Redaktionsplan aktualisieren | Kein neues SEO-Urteil |

**Übergabeprinzip:** Der nächste Worker muss nicht wissen, *warum* der Vorgänger freigegeben hat. **Die vorgelagerte Reservierung/Transportstelle** muss Verwechslungen, unvollständige Daten, doppelte Zustellung oder Wiederanlauf sicher handhaben. Das ist *keine* fachliche Zweitentscheidung.

## 3. Ist-Abgleich – tatsächliche Quellstellen und Proben

| Verbindliche Aufgabe | Aktueller Code | Sachstand / Beleg |
|---|---|---|
| Keine ungeprüften Rohkeywords an MINI | `PSTE_Mini_Workflow::selectNewRows`, Z. 331–356, wählt **alle** bisher nicht als abgeschlossen markierten Rohfragen; weder gebundene Freigabe noch reservierten Platz verlangt | **FEHLT**: Originalmethode exportierte in QA bewusst `raw-not-approved` → Test PASS als **Fehlerreproduktion**, nicht Workflow-PASS |
| MINI nur Titel, keine weitere Relevanzentscheidung | `createBatch`, Z. 359–366, verlangt explizit JA/NEIN/VIELLEICHT-Worker **und** Titelworker | **ABWEICHUNG**: zweiter Relevanzworker sitzt weiterhin in MINI |
| Genau eine feststehende Suchabsicht je Auftrag | `createBatch` lässt mehrere voneinander verschiedene Absichten als Titel zu. `validateResult`, Z. 437–451, akzeptiert **mehrere** Titel/Absichten pro Rohkeyword | **ABWEICHUNG**: Originalmethode akzeptierte in QA zwei unterschiedliche Intents für eine Rohfrage |
| Zentraler Vor-MINI-Dublettenentscheid ohne TITEL-Abhängigkeit | `PSTE_Runner::applyInternalDuplicates`, `sameAnswerIntentSignature`: nutzt neben Suchfrage auch **Titel-Fallback** | **ABWEICHUNG**: Originaltest blockiert bei identischem Titel 1 von 2 Testfällen, ohne Titel blockiert er keinen. Vorverlagerung erfordert eigene vollständige Suchintent-Evidenz, **nicht** blindes Abschalten des Titel-Fallbacks |
| Artikelplatz wird vor MINI **dauerhaft** reserviert | `PSERC_Slot_Allocator::allocate` wählt anhand `category_slug` + `article_type` ohne Titel, gibt aber nur `reserved_ids` des **einzelnen Aufrufs** zurück. `PSERC_Plan_Compile_Job::tickSlot` Z. 217–223 führt Slotvergabe erst **nach** der Kandidaten- und Titelphase aus; aktive Planversion erst `tickActivate` | **ABWEICHUNG**: Original-Allokator vergab ohne gespeicherten Beleg bei zweitem unabhängigen Aufruf **wieder denselben Platz**. Mit übergebenem occupied-Id wurde korrekt der nächste gewählt. Das beweist, dass Reservieren mehr als einmaliges Wählen ist. Keine daraus folgende Behauptung, dass Live parallel tatsächlich doppelt reserviert hat |
| Redaktionsplan behandelt normal freigegebene Themen nicht erneut fachlich | `PSERC_Compiler::compile` und `PSERC_Plan_Compile_Job::tickCandidate` rufen ohne speziellen MINI-Receipt weiterhin semantischen Dublettenprüfer auf; `PSERC_SEO_Reader::normalizeCandidate` verliert den frühen normalen `planning_readiness_gate` | **BELEGT OFFEN**: zweiter fachlicher Aufruf im Normalweg (Originalmethodentest im Arbeitsraum). Ein **frühes** PASS ist aber nicht das endgültige Stapelergebnis; deshalb darf dessen einfaches Kopieren nicht Freigabe sein |
| K0 liest fünf Daten und erstellt Text | Vorhandener PSERC-Fünffeldvertrag; aktiver K0-Zweig bereits mit PR #757 von zweiter SEO-Entscheidung bereinigt | **Keine neue K0-Codeänderung nötig** nach vorliegenden Nachweisen; echter neuer Artikel fehlt |
| Re-Import aktualisiert Plan und sieht Artikelkonflikte | `PSERC_System4_Import::importPayload`: `findCollision` vor WP-Schreiben, `readback` und `PPM679_Editorial_Plan_Runtime_Gate::record_readback` | **Vorhanden**. Nicht fälschlich als Ersatz für vorzeitige korrekte Themen-/Slotvergabe ausgeben. Echter WP-Test fehlt |

**Zusätzlicher heutiger Quellenbeweis (tatsächliche PHP-Methoden, nicht Textsuche):** Privater Ordner `/pferdeatelier/PLUGINS/ARBEITSRAUM_PSTE_KISS/`, Dateien `QA_ENDVERTRAG_SOLL_IST_ORIGINALMETHODEN_20261112.php` und `QA_ENDVERTRAG_SOLL_IST_ORIGINALMETHODEN_ERGEBNIS_20261112.jsonl`. **6 von 6 erwarteten Ist-Abweichungen nachgestellt**, Exit 0. Skript SHA-256 `48a7caea00f26b975da4ae1176308ebeedd3dfc43002815b1ee792760c79a6a8`, Ergebnis SHA-256 `a8f2030ea8d0d3a55b584e0c5b96d451d6edd658fbe118ccdad315d9bfb04590`. Daten sind **lokal modelliert**; echte WP-Datenbank fehlt. Quelltextbeobachtungen separat `QA_WORKFLOW_QUELLNACHWEIS_20261112.json`, **15/15 Verankerungen**.

## 4. Strengste Risikoabwägung

1. **Freigabe zu früh oder aus unvollständigem Bestand** → reale inhaltliche Doppelartikel möglich. Schutz **am einmaligen zentralen Entscheid mit komplettem bestehenden Bestand und Stapel**. Spätere SEO-Zweitmeinung nicht nötig, spätere Reimportkontrolle kann den Erstfehler nicht rückgängig machen.
2. **Titelabhängigkeit heute im Erstentscheid** → wenn MINI zukünftig *nachher* formuliert, darf ein zuvor zugelassener Sinn nicht erst durch die Titelwortwahl frei/belegt werden. **Originalcode ist hier noch nicht titelunabhängig.** Fachliche Entscheidung muss unabhängig vom späteren Wortlaut stabil sein; MINI darf Sinn nicht verschieben.
3. **„Ausgewählt“ ist nicht gleich „dauerhaft reserviert“** → bei zweitem Aufruf derselbe Platz möglich. Reservierung muss vor Auftragsausgabe **gespeichert und bei Wiederanlauf/gleichzeitigem Zugriff** nachgewiesen werden. Keine zweite SEO-Prüfung beim nächsten Worker.
4. **Alter Auftrag, neuer WP-Inhalt** → nur echte konkurrierende Änderungen am belegten Auftrag technisch auffangen; kein Fachurteil durch PSERC. Für die Vollständigkeit und Aktualität des anfänglichen Bestands fehlt ein echter WordPress-TEST-Beleg.
5. **MINI macht zwei Titel aus einer Rohfrage** → bei den alten 97 Titelvorschlägen historisch möglich. Neue Aufträge brauchen **genau die vorher entschiedene eine Suchabsicht**; alte vollständige Datensätze nicht stillschweigend löschen oder als neu freigegeben umetikettieren.
6. **Fehlerhafter Transport, Doppelzustellung, Abbruch** → den bestehenden Auftrag unverwechselbar und wiederholbar verarbeiten. Die empfangende Fachstation muss die vorherige Fachprüfung **nicht selbst wiederholen**.
7. **Inhaltliches Problem des K0-Artikels** → K0-Qualitätskontrolle bleibt; weder MINI noch PSERC müssen die Artikel-SEO neu beurteilen.
8. **Reimport kann nur nachgelagerte Identität/Zuordnung prüfen**, keine falsche Vorentscheidung heilen. Seine vorhandene Kollisionserkennung und PPM-Synchronisation nicht entfernen.

**Fazit:** Die Einmal-Entscheidung ist konzeptionell **sinnvoll, aber eine blanke Übergabe ohne verbindlich gespeicherte Freigabe/Reservierung nicht sicher**. Der zweite Worker braucht keine fachlichen Prüfergebnisse, nur einen **fertigen, eindeutigen Auftrag**. Dazu müssen die **vorgelagerten** Entscheidungen und die Reservierung tatsächlich vollständig sein.

## 5. Änderungsregeln – Umsetzung nur mit Originalbeleg

Die **noch notwendigen** Programmänderungen in *dieser* eingefrorenen PSTE/PSERC-Arbeitskopie sind genau:

- A. `selectNewRows/createBatch/validateResult`: nur **vorher endgültig freigegebene und reservierte** Themen an MINI, **Titel-only**, keine zweite Relevanz-/Intententscheidung. **Beweis:** sechs lokale Originalmethodenproben oben; **Ziel:** Stationen 2–5.
- B. Erste zentrale Recherche-/Dublettenentscheidung **vor MINI unabhängig vom späteren Titel** endgültig abschließen, nachweislich stapelweit und auf vollständigem aktuellem Bestand, eindeutige Kategorie und Artikelart. **Beweis:** Titel-Fallback-Probe plus Original-PSTE-Research-Finalisierung; **Ziel:** Station 2.
- C. Bestehende PSERC-Slotvergabe **vor MINI** ausführen und die tatsächliche Belegung **dauerhaft** innerhalb des bereits vorhandenen Plan-/Laufzeitbesitzers sichern. Nicht nur einen lokalen Array-Index aufrufen, keine neue Tabelle. **Beweis:** zweimal identischer Slot ohne gespeicherten Beleg; **Ziel:** Station 3.
- D. Nach MINI trägt derselbe Auftrag den ursprünglich reservierten Platz und den geprüften Titel; normaler und MINI-PSERC-Weg entfernen **erst nach belegter vollständiger A–C-Übergabe** die nachträgliche semantische Eigentümerschaft. **Beweis:** vorherige Originalmethodenprobe des zweiten PSERC-Aufrufs und gefährliche gescheiterte QA-.70; **Ziel:** Station 6.
- E. Vollständiges unverändertes K0 mit fünf Feldern und **Reimport** am reservierten Slot in der realen WordPress-Testumgebung durchführen. Erst nach Positiv-/Negativfällen und **Paketintegrität der exakten fertigen ZIPs** eine installierbare Testdatei freigeben. **Ziel:** Stationen 7–8.

**Nicht ändern:** bestehende Fehlerisolation für ein einzelnes Keyword, Backend/Frontend, K0-Textprüfungen, bereits funktionierenden Reimport oder 5.016 alte Themen pauschal neu recherchieren.

**Wichtige Unterlagenkorrektur:** Ältere Berichte, die „MINI bestimmt FREI/BELEGT/KLÄRUNG“ behaupten, bezogen sich vermischend auf einen **separaten externen SEO-Entscheider, der *nach* MINI verankert wurde**. Der MINI-**Titel**worker selbst ist nach ursprünglichem Quellvertrag **nicht** diese Instanz. Die letzte Nutzerfestlegung korrigiert die Arbeitsreihenfolge verbindlich. Nicht alte Konzept-Gegenworte als Freigabe für neuen Umbau verwenden.

**Stand der tatsächlichen Ausführung in diesem Audit:** Quellarchiv/Tests/Fehlerbelege gesichert und GitHub-Dokumentation korrigiert, **keine weitere Plugin-Programmänderung**. A–E sind an den Originalcode gebundene Umsetzungsaufträge, keine erledigten Reparaturen. Der jetzige Code hat keine vollwertige **dauerhafte Vor-MINI-Reservierung**, die man ohne echten WP-DB-Test gefahrlos nur mit einem einzelnen Textpatch einschalten könnte. Eine stillschweigende Freigabe eines halbfertigen ZIPs würde ausdrücklich gegen den Zielvertrag verstoßen.
