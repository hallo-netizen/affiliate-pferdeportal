# Pferdeatelier – Quellen-Gegenprüfung und sichere Rücknahme, 12.11.2026

**Gültigkeit:** Nur isoliertes QA, keine Installation, keine WordPress-/K0-/Produktivänderung. Vorrang hat der bestehende Kisten-Zielvertrag vom 07.11. und die Korrektur `20261112_KORREKTUR_MINI_IST_PRODUKTIONSBESTANDTEIL.md`.

## Originale und direkter Vergleich
Originale unverändert aus der privaten Projektablage materialisiert, ZIP-CRC fehlerfrei und SHA-256 gegen bestehende Protokolle abgeglichen:

| Original | SHA-256 | Dateien |
|---|---|---:|
| PSTE 0.57.144.45 | `d3057946defc035af7abe5522c4845625c98ebd3f2cf621e1b3c5ce019f230a4` | 121 |
| PSTE 0.57.144.46 | `e3461e7bdf8a30eb30f16e445e02499dafaebb496171f53900c068564682352c` | 121 |
| PSERC 0.28.69 | `576e58b51db3f348210dc3d47a894d6551558acc0c6900505be5e11257d2e41b` | 63 |
| PSERC 0.28.70 | `0367fad3be41ac2a79e37397fb9b9e39f787956a887413c951b30f1dc2125c1a` | 63 |

**Exakt neun geänderte Dateien:** PSTE `.45→.46`: `class-pste-mini-workflow.php`, `class-pste-repository.php`, Plugin-Hauptdatei. PSERC `.69→.70`: `class-pserc-compiler.php`, `class-pserc-plan-compile-job.php`, `class-pserc-plan-dependency-fingerprint.php`, `class-pserc-seo-reader.php`, Plugin-Hauptdatei, Paketmanifest. Plugin-Hauptdateien/Manifest enthalten Versions-/Integritätsnachführung, keine eigenständige fachliche Ursache.

## Falsche Annahmen gestrichen
- **Nicht wahr:** „MINI hat grundsätzlich Kategorie, Artikelart und Suchintention verloren.“ Die anfängliche `selectNewRows/createBatch`-Rohkeyword-Datei enthält diese Felder nicht; der **vorhandene zweite Weg** `exportResults` übergibt jedoch optional ausdrücklich `parkhaus_snapshot`, und dessen originale Quellzeilen enthalten `category_slug`, `article_type`, `intent_profile`, bestehende Planplätze. Die beiden Wegarten dürfen nicht verwechselt werden. Aus dem ersten Export allein ist kein Verlust im Gesamtweg bewiesen. Vorhandener PSERC-Plan der drei READY-Aufträge hatte diese Angaben ebenfalls. **Keine Codeänderung aus dieser Annahme ableiten.**
- **Nicht bewiesen:** Jede PSERC-Abfrage ist eine unnötige zweite Fachentscheidung. Der bereits vorhandene Plan und seine echten Reservierungen gehören zur vollständigen Bestandsübersicht. Sicherheitsprüfung von Identität/aktueller Belegung ist keine zweite Keyword-Entscheidung.
- **Nicht bewiesen:** MINI könne gestrichen oder mit dem normalen Einstieg vereinigt werden. MINI bleibt laut ursprünglichem Vertrag fester Produktionsbestandteil.

## Drei tatsächlich geprüfte Rückschritte der letzten QA-Pakete
1. **PSERC `.70` überspringt notwendige Prüfung innerhalb desselben neuen Stapels.** Reale `PSERC_Compiler::compile`-Kontrollwege mit WordPress-Testdaten: zwei sinngleiche Regendecken-Anfragen (`0g` / `ungefüttert`) erreichen in `.70` beide die folgende Stufe, obwohl die unveränderte Prüfmethode beim zweiten `BLOCKED_DUPLICATE` liefert; `.69` lässt nur den ersten weiter. Die neu eingefügte Markierung `upstream_central_coverage_decided` ist ohne geprüften *stapelweiten* Erstbeleg keine sichere Grundlage, den vorhandenen Stapelvergleich abzuschalten. **`.70` nicht übernehmen.**
2. **PSERC `.70` übersieht echte neue Quellenstände.** Am originalen `PSERC_Plan_Dependency_Fingerprint::current` mit festen WordPress-Testoptionen: Wenn der `final_structure_sha256` oder `final_plan_sha256` des Kontextes wechselt, erkennt `.69` beide Änderungen, `.70` keine von beiden, solange der ältere Baseline-Hash gleich bleibt. **`.70` nicht übernehmen.**
3. **PSTE `.46` entfernt zu weitgehend aktuelle Bestandsprüfungen.** `forwardToPlan` verlangt statt erneuter Bestandsidentität nur noch zwei syntaktisch 64-stellige Werte; bei der lokalen Originalmethodenprobe kommt das Beispiel durch, das `.45` wegen nicht übereinstimmenden Bestands zurückstellt. Außerdem entfällt beim `readExistingPsercPlanForParkhaus` die aktuelle `isCurrent`-Kontrolle. Die Annahme „serieller Lauf = zwischendurch keine Änderungen“ ist nicht bewiesen. Die neue Schonung einer gespeicherten `FREI`-Entscheidung in `class-pste-repository.php` wurde positiv und mit beschädigtem Beleg getestet, aber **nicht** gegen sämtliche späteren Änderungen an Kategorie/Artikelart/Planplatz. **`.46` als Gesamtpaket nicht übernehmen.**

**Testgrenze:** Echte Pluginmethoden und Originaldateien, aber WordPress-Datenbank und Provider wurden in diesen Gegenproben **nachgebildet**. Kein Nachweis eines tatsächlich verursachten Doppelartikels in WordPress und keine produktive End-to-End-Abnahme.

## Tatsächlich durchgeführte sichere Rücknahme
Die beiden nicht abgenommenen Pakete wurden **nur in einer isolierten lokalen Arbeitskopie** durch quellgenaue Rücknahme ihrer Änderungen wieder auf `.45` und `.69` gebracht. Ergebnis:
- PSTE: exakt 3 Dateien rückgenommen, **121/121 Dateien byteidentisch** zu `.45`, **83/83 PHP-Syntaxprüfungen bestanden**.
- PSERC: exakt 6 Dateien rückgenommen, **63/63 Dateien byteidentisch** zu `.69`, **43/43 PHP-Syntaxprüfungen bestanden**.
- Zusätzlich am zurückgesetzten PSERC-Code gegengeprüft: die zweite sinngleiche Anfrage wird abgefangen, echte Kontext-Struktur-/Planänderungen werden erkannt. Am PSTE-Altstand wird ein unpassender Gesamtbestand nicht automatisch freigegeben.
- Die existierenden Original-ZIPs bleiben unverändert. **Kein neuer Installer und kein Update auf WordPress**; `.45/.69` sind nur kontrollierte QA-Vergleichsbasen, keine Produktionsfreigabe.

## Kleine, begründete Korrektur getrennt geprüft
Der tatsächlich nachgewiesene Fehler „Jobstatus allein ändert den PSERC-Plan-Fingerabdruck“ lässt sich *ohne* Wegfall der Inhaltsbindung beheben: Im vorhandenen `class-pserc-plan-dependency-fingerprint.php` nur `status`, `generation`, `job_uuid` aus dem Fingerabdruck entfernen; **echte** `final_structure_sha256`, `final_plan_sha256`, Baseline, WordPress-Inventarversion und Themen-Wasserstände erhalten. Gegen original `.69` als eine lokale Quelländerung **8/8 Positiv-/Negativfälle bestanden**: drei reine Jobfortschritte ändern den Fingerabdruck nicht, fünf reale Quellen-/Bestandsänderungen ändern ihn weiterhin. **Nur geprüfter Quellpatch, kein installierbares vollständiges Paket**; vor jeder WordPress-Freigabe sind Paketintegrität und echte WP-Staging-Endabnahme neu erforderlich.

## Weiter nur nach Beweisen
- **Nicht** vorhandene 5.016 Themen neu recherchieren, keine drei historischen READY-Metadaten als frisch erzeugte Artikel ausgeben.
- Die **tatsächliche Ursache** von `READY=0` auf der vorhandenen WordPress-Testseite ist mit diesen nachgebildeten Prüfungen nicht belegt. Keine entsprechende Datenbankänderung, kein Reset und keine angebliche Reparatur behaupten.
- Nur den bestehenden wirklichen Ablauf gegen seinen Zielvertrag und aktuelle Quelldaten prüfen: Originalquelle → vollständiger Bestand → **ein** externer MINI-/SEO-Fachentscheider → technische Herkunft/Belegung → PSERC-Plan und fünf Felder → unveränderte K0-Text-/Sprachprüfung → WordPress-Testentwurf. Ein Fehler betrifft zunächst das konkrete Thema; defekte Gesamtbestandsquelle sperrt sichere Freigaben.
- Neue Quelländerung nur dort, wo der exakt gebrochene Originalweg mit positiver **und** negativer Probe bestätigt ist. Bis dahin **kein** neues Installationspaket, kein Merge, kein Live.