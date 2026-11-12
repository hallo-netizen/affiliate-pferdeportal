# Unabhängige Änderungsprüfung – reale QA-ZIPs .45/.46 und .69/.70

**Stand: 12.11.2026. Keine Installation, keine neue Plugin-ZIP, kein WordPress-Code geändert.** Prüfgegenstand: die tatsächlichen *unveränderten* älteren und neueren installierbaren ZIPs. Vergleich der neun tatsächlich geänderten Dateien: **2 Verwaltungs-/Versionsdateien**, **1 Paketmanifest**, **6 PHP-Programmdaten-Dateien** (PSTE 2 PHP, PSERC 4 PHP). Der vorherige pauschale Ausdruck „neun programmatische Änderungen“ wäre unpräzise: geänderte Dateien ≠ fachliche Verhaltensänderungen.

## Belege und Grenzen
Frisch aus ZIP-Dateien extrahierte PHP-Klassen statt der bisherigen Arbeitskopie; für die explizit genannten Gegenfälle **echte Klassenmethoden** ausgeführt. WordPress-Speicher/-Arbeiter und teils andere Gates sind **kontrollierte Testdoubles**, keine reale WordPress-Testinstallation. Kein Beweis, dass die Fehler genau so auf der aktuell installierten Testseite aufgetreten sind. **Ein bestandener QA-Positivtest beweist nicht die Notwendigkeit oder Sicherheit eines Patches.**

ZIP-Prüfsummen:
- PSTE .45: `d3057946defc035af7abe5522c4845625c98ebd3f2cf621e1b3c5ce019f230a4`
- PSTE .46: `e3461e7bdf8a30eb30f16e445e02499dafaebb496171f53900c068564682352c`
- PSERC .69: `576e58b51db3f348210dc3d47a894d6551558acc0c6900505be5e11257d2e41b`
- PSERC .70: `0367fad3be41ac2a79e37397fb9b9e39f787956a887413c951b30f1dc2125c1a`

## 1. PSTE .45 → .46

### `includes/class-pste-repository.php` – **lokal positiv belegt, noch keine WP-Abnahme**
`applyPoolRowWithRelations` berechnete in .45 beim Lesen einer als AUTO_RESOLVED, YES und CURRENT gespeicherten signierten MINI-Freigabe erneut die Status-/Planungsregel. PHP-Gegenprobe auf Originalmethoden mit absichtlich blockierender Policy:
- .45: **2 erneute Regelaufrufe**, Ergebnis `planning_suitability=BLOCKED`.
- .46: **0 erneute Regelaufrufe**, bisheriges `YES` erhalten.
- .46 bei ungültigem Freigabenachweis: alte konservative Regel wird weiterhin gerufen, `BLOCKED`.

Das ist ein nachgewiesener Verhaltensunterschied und eine begründete Richtung für KISS. Der externe MINI-Receipt und die Policy wurden im Versuch **simuliert**; keine Behauptung eines echten vollständigen WordPress-GO.

### `includes/class-pste-mini-workflow.php` – **teilweise begründet, teilweise NICHT ausreichend belegt**
* `forwardToPlan`: Die bisherige Funktion ruft nach Annahme der einmaligen externen SEO-Entscheidung den gesamten `readParkhausForMini()` **erneut** auf und vergleicht den globalen Hash. .46 entfernt diesen nachgelagerten Vollread. Im kontrollierten PHP-Versuch mit fehlenden WordPress-Quell-APIs ist .45 BLOCKED, .46 transportiert das ursprünglich gebundene Thema. Das beweist **das Wegfallen der Kontrolle**, aber **nicht**, dass die alte Kontrolle in der echten TEST-WP bei unverändertem Originalplan tatsächlich falsch blockiert hat. Der Versuchsreceipt war im Mock angelegt, nicht durch echten externen Import geschrieben.
* `readExistingPsercPlanForParkhaus`: .45 verlangte neben dem vorhandenen Signaturkopf `PSERC_Plan_Dependency_Fingerprint::isCurrent`; .46 nimmt einen historisch signierten Plan auch bei veralteter Gesamtabhängigkeit als bestehende Plätze auf. Dieser Weg kann unter dem Serien-/Keine-Außenänderung-Vertrag sinnvoll sein. **Der bisherige Gegenprobentest ersetzt `PSERC_Plan_Snapshot_Store::verifyHeader` durch eine Attrappe, die lediglich „64 Zeichen“ prüft.** Er prüft damit gerade **nicht** die reale Signaturprüfung oder die vollständige derzeitige PPM/WP-Reservierung. Daher kein Sicherheits-GO; nicht eigenmächtig diesen Patch freigeben.

### Versionskopf `portal-seo-topic-engine.php`
Nur Version .45→.46, kein fachlicher Fix.

## 2. PSERC .69 → .70

### **KRITISCHER GEGENBEWEIS A: Wegfall des Schutzes gegen zwei neue Artikel mit demselben Thema**
Betroffene **drei** Dateien: `includes/class-pserc-seo-reader.php`, `includes/class-pserc-compiler.php`, `includes/class-pserc-plan-compile-job.php`. Der Reader markiert auch einen normalen, zuvor PASS-geprüften PSTE-Kandidaten als `upstream_central_coverage_decided`. Daraufhin überspringen Compiler und Planjob den bestehenden semantischen Vergleich nicht nur mit vorhandenen WordPress-Artikeln, sondern **auch zwischen zwei gleichzeitig noch nicht importierten Themen im neuen Plan**.

**Original-PHP-Beweis mit realem `PSERC_Semantic_Duplicate_Gate` und echtem `PSERC_Compiler` aus den jeweiligen ZIPs**, kontrollierten übrigen Gate-/WP-Antworten:
- Kandidat A „regendecke pferd 0g“ und Kandidat B „regendecke pferd ungefüttert“, identischer Artikel-Titel, gleiche Familie und Art; beide tragen den von .70 übernommenen vorgelagerten „bereits zentral entschieden“-Vermerk.
- `againstPreparedCandidates` im UNVERÄNDERTEN Original meldet für B **`BLOCKED_DUPLICATE`**.
- .69 lässt nur **A** zur nächsten technischen Stufe; B wird beim bisherigen Dublettenvergleich erkannt.
- .70 lässt **A und B** zur nächsten technischen Stufe. Der neue Umgehungsweg überspringt die belegte Schutzentscheidung.

**Grenze:** Der Test stoppt bewusst vor finaler Slotvergabe/WordPress-Import. Deshalb nicht behaupten, beide Artikel wären tatsächlich veröffentlicht worden. Er beweist aber, dass der .70-Patch einen vorhandenen Schutz zwischen zwei vorbereiteten Kandidaten entfernt, ohne zu belegen, dass der zentrale PSTE-Freigabebeleg *beide gegeneinander* geprüft hatte. `PSTE_Planning_Readiness_Gate::preTitleDuplicate` durchsucht vor allem vorhandene `publish/draft`-Artikel, **nicht** automatisch das jeweils noch offene PSERC-Kandidatenpaar. Der Gesamtbeleg zur Gleichwertigkeit der Vorprüfung fehlt.

**Freigabeentscheidung: DIESE DREI .70-ÄNDERUNGEN NICHT ÜBERNEHMEN.** Erst nachgewiesener, vorgelagerter eindeutiger Slot-/Batch-Schutz und Entfernung des tatsächlich dann redundanten Vergleichs.

### **KRITISCHER GEGENBEWEIS B: Gültige neue Kontext-Quellen werden nicht mehr im Planstand erkannt**
Betroffene Datei: `includes/class-pserc-plan-dependency-fingerprint.php`. .70 entfernt Jobstatus/Generation (unter Serienlaufannahme möglicherweise sinnvoll), ersetzt aber zugleich die beiden konkreten Kontext-Quellhashes **mit älteren Baseline-Werten**.

Native Original-PHP-Gegenprobe mit vollständigem tatsächlichem Quellfingerprint und identischen anderen Antwortwerten:
- Ausgangs-WordPress-Baseline (Plan, Struktur) bleibt gespeichert.
- Eine neue gültige Kontext-Strukturquelle (oder Planquelle) wird gespeichert, Baseline aber noch nicht aktualisiert.
- **.69 erkennt BEIDE fachlichen Quelländerungen**, Planfingerprint ändert sich.
- **.70 erkennt KEINE** der beiden Änderungen, Planfingerprint bleibt identisch.

**Grenze:** Test benutzt kontrollierte WordPress-Optionen; er beweist den technischen Blindfleck für genau diesen Zwischenzustand, nicht dass dieser auf der aktuellen Testseite bereits eingetreten ist. **Die gezielte Bereinigung der Jobstatusabhängigkeit darf nicht zugleich fachliche Quellenänderungen unsichtbar machen.**

**Freigabeentscheidung: DIESE .70-ÄNDERUNG NICHT ÜBERNEHMEN.**

### Version und Paketmanifest
`portal-seo-editorial-plan-compiler.php` und `contracts/compiler-package-binding-v1.json` wurden der neuen Paketquelle angepasst; keine eigenständige fachliche Entscheidung. Ein zurückgenommener Quellpatch erfordert ein dazu passendes neu generiertes, separat geprüftes Paketmanifest. Keine Manipulation am bestehenden .69-Vertrag.

## Gesamtfazit / zwingender Stand
- **.46 und .70 weiterhin KEINE Installationsfreigabe.**
- **.70 enthält jetzt in zwei unabhängigen Gegenproben reproduzierbare gefährliche Verhaltensänderungen**, die in .69 nicht vorkamen. Nicht auf der WordPress-Testseite installieren.
- .46 beinhaltet die im kontrollierten Test begründete Bewahrung bestehender Freigaben, daneben aber zwei Änderungen an MINI, deren vollständige Sicherheits-/Bestandswirkung noch nicht an den tatsächlichen Quellen belegt wurde. Nicht pauschal als fertig einstufen.
- Die später zurückgenommene Behauptung „MINI bekommt keine Kategorie, Artikelart oder Intent“ löste **keine der zwischen .45/.46 oder .69/.70 verglichenen Codeänderungen aus**; sie wurde als reine fehlerhafte Diagnose auf GitHub berichtigt. Keine neuen Kategorie-Arbeiter/Gates daraus bauen.
- **KISS-Auftrag beibehalten:** nur Serienlauf, keine externen Änderungen, ein zentraler ursprünglicher Redaktionsplan/Platzentscheid, MINI fester externer Agentenweg, K0-Artikelqualitätsregeln unverändert. Abbruch/Fortsetzung gesondert.
- Sicherer nächster technischer Schritt: Bei der späteren integrierten Reparatur nur Patches übernehmen, deren Originalfehler **und vollständige Gegenfälle** bewiesen sind. Die zwei .70-Änderungsgruppen müssen verworfen oder fundamental korrigiert werden. Keine neue ZIP und kein 5.000er-Wiederholungslauf ohne Freigabe.

## Wiederholbare Testartefakte (Library, nur private QA)
`/pferdeatelier/PLUGINS/QA/PFERDEATELIER_AUDIT_GEAENDERTE_STELLEN_20261112.zip`: direkte unabhängige PHP-Gegenproben, vollständige Ergebnisdatei und Quell-Diffs. Keine WordPress-Instanz verändert.
