# Pferdeatelier – KISS-/Worker-Ursachenprüfung der PSTE 0.57.144.28, 09.11.2026

**Status: geprüfte Bestands- und Codeanalyse mit negativem Gesamtfreigabeurteil.** Keine Installation, kein WordPress-Eingriff, keine Löschung, K0/PSERC/PPM unverändert. Testdaten: echter WordPress-TEST-Kontext-Export, echter 61er-Bericht und der tatsächliche Originalcode von PSTE .28 + PSERC .28.55. **`FULL_WORKFLOW_PASSED = false`.** Die vollständige echte WordPress-MySQL-/PSERC-/PPM-/K0-Kette ist weiterhin nicht positiv durchlaufen; keine Freigabe behauptet.

## 1. Tatsächliche Ursache der 61 Blockaden

- Der echte WordPress-Export zeigt **eine aktive importierte PSTE-Planquelle** (Herkunft: `OPTION`, **kein zusätzlich aktiver konkurrierender Filter**). Darin liegen **neun inhaltsleere alte Einträge** (Text `Array`, keine gültige Artikelidentität). Der aktuelle Planleser wertet sie folgerichtig nicht als belegte Planartikel: **Planstatus `NOT_AVAILABLE`**.
- Die **gespeicherte Bestandsaufnahme** (`PSTE_OPTION_SITE_BASELINE`) und der **technische Kontextindex** (`PSTE_OPTION_CONTEXT_INDEX_MANIFEST`) tragen dagegen den alten Plan-Fingerabdruck. Dadurch scheitern 60/61 Themen an `PSTE_RETAINED_EDITORIAL_PLAN_SNAPSHOT_CHANGED`; das 61. Thema bleibt gesondert in der manuellen Prüfung. Die neue `.28`-Stapelausgabe zeigt weiterhin diese alten Ergebnisse; sie beweist **nicht**, dass die gesonderte Reparaturaktion auf WordPress erfolgreich oder überhaupt ausgeführt wurde.
- Die bisherige Aussage „mehrere Redaktionspläne als gleichberechtigte Speicher“ war **zu ungenau**. Tatsächlich gibt es **Planquelle, eingefrorene Vergleichswerte und daraus erzeugte Such-/Prüfdaten**. Vergleichswerte sind für die Sicherheit sinnvoll, dürfen aber nicht selbst zur zweiten fachlichen Planentscheidung werden.
- **Systemische Schwachstelle:** Ein angeblicher Leseweg (`PSTE_Context_Index_Store::runtimeBinding()`) kann bei einem fehlenden/abweichenden Kontextmanifest `rehydrateCompletedRuntimeIndex()` aufrufen und damit über `stageInventory()`, `stagePlan()`, `stageRegistry()` und `buildFromStages()` WordPress-Optionsdaten schreiben. **Lesen und Neubauen sind damit nicht konsequent getrennt.** Das sollte in einen ausdrücklich zuständigen Worker mit nachvollziehbarem Wiederanlauf überführt werden; nicht durch Löschen von Prüfsummen umgehen.

## 2. Bestand und eindeutige Zuständigkeit – was behalten, was bereinigen?

| Daten | Im Code beobachtete Rolle | Entscheidung ohne riskante Löschung |
|---|---|---|
| `pste_editorial_plan_import_v1` | Optionale importierte Vergleichsquelle, auf dieser Testseite nur 9 leere historische Platzhalter | **Nur diese nachweislich leeren Alteinträge** nach gesicherter Abhängigkeitsprüfung endgültig aus der fachlichen Planung entfernen; keine aktiven Planartikel unterstellen, niemals ohne Migration einfach `delete_option` auf der Testseite |
| `pste_site_baseline_v1` | Gespeicherte Bestandsaufnahme aus WP-Artikeln, Kategorien und Plan-Fingerabdruck | **Behalten als Prüfbeleg**, aber nur eine zuständige Aktualisierung, keine zweite fachliche Planhoheit; Änderungen zentral im Kontext-Worker bestätigen |
| `pste_context_index_manifest_v2`, Kontext-Shards, Inventar-/Artikeltyp-Stages | Abgeleiteter technischer Suchindex und Prüfnachweise | **Bei nachgewiesenem Quellwechsel kontrolliert erneuern**, niemals als eigenständige Entscheidung behandeln; keine spontanen Schreibvorgänge beim bloßen Lesen |
| `pste_context_stage_plan_v1` | Temporärer Planaufbau | **Wird im Originalcode nach Abschluss bereits gelöscht.** Kein Grund für zusätzliche Neuimplementierung |
| `pste_context_snapshot_bundle_v1` | Historisches Paket | **Im geprüften Code keine aktive Leseverwendung**, nur bestehende Lösch-/Aufräumstellen; vor endgültiger Entfernung auf externe Referenzen prüfen, nicht als zweite Produktionsquelle verwenden |
| `pste_context_refresh_job_v1` und Reentry-Warteschlange | Arbeitsfortschritt / Wiederanlauf | **Behalten**, nur ein zuständiger Worker, keine Schlussmeldung „erledigt“ nach technischem Abbruch |
| `pste_mini_keyword_roundtrip_v1` | Einmalige externe SEO-Entscheidungen und Nachweise | **Behalten als einziges SEO-Entscheidungsprotokoll**; Reentry darf die 61 Entscheidungen nicht nochmals fällen |
| `pste_editorial_ownership_import_v1` | Separater Kategorie-/Themenzuständigkeits-Handoff | **Nicht mit einem Artikelplan verwechseln oder blind löschen**; eigene Zuständigkeit prüfen |
| PSERC-Plan-Snapshot und `ppm679_editorial_plan_runtime_state_v1` | Aktiver Plan für Produktionsübergabe bzw. bereits belegte Artikelplätze | **Nicht blind löschen.** Mit PSTE importierten historischen Referenzen unterschiedliche Stufe. Ein verbindlicher Produktionsplan-Eigentümer ist als Vertrag festzulegen; PSTE darf nur lesen und keine zweite Freigabe erteilen |
| SQL-Thementabelle: Statusfelder sowie Status im gespeicherten Thema | Verarbeitungs-/Suchspalten und detaillierte Begründung im Datenfeld | **Potenziell redundante Status-Abbilder**, aber kein Beweis für zwei Entscheidungsträger. Vor Entfernung Konsistenz mit echter MySQL-Abfrage/Indexnutzung nachweisen |

## 3. Zweiter **bewiesener**, vom alten Plan unabhängiger Fehler

Die echten 1.165 WordPress-Produktionskategorien haben **45 doppelt vorkommende sichtbare Namen** (90 Kategorien). Diese sind größtenteils in verschiedenen Fachzweigen legitime Kategorien und **dürfen nicht aufgrund des Namens gelöscht werden**.

- Im Originalcode `PSTE_Snapshot::normalizeEditorialPlanItemsAgainstStructure()` wurde `byName[$name]=$row` gesetzt. Bei gleichen Namen verdrängt der spätere Eintrag den früheren – **still und ohne Eindeutigkeitsprüfung**.
- ORIGINAL-PHP-REPRO: Bei `FAQ Sicherheitshalfter` ohne ID/Slug wird **Kategorie 942** (Training) genommen; die ebenfalls passende **Kategorie 55** (Ausrüstung) bleibt unberücksichtigt. Mit eindeutiger ID 55 oder eindeutigem Slug wird dagegen korrekt 55 ausgewählt. Ebenso `FAQ Schermaschinen`: nur mit Namen -> 714 (Gesundheit) statt auch möglicher 75 (Ausrüstung).
- Besonders kritisch: **5 Paare haben sogar denselben vollen Portalpfad** für `Weide > Zauntechnik > Weidezaungeräte`: FAQ, Beratung, Vergleich, Installation, Kosten. Die Kategorien 291 und 293 haben in der vorliegenden WordPress-Inventarliste tatsächlich je einen Beitrag; die jeweils parallelen Einträge 381–385 sind dort leer. **Nicht löschen**, bevor Nutzungen, Links, Metadaten, historische Artikel und Einträge der geschützten Kategorieabbildung vollständig verglichen sind.
- Minimaler **nur lokaler QA-Diff**, keine neue Speicherung und keine neue Instanz: `byName[$name][]=$row`; ist allein der Name gegeben und mehrfach vorhanden, dann **gezielt blockieren**. Explizite ID oder Slug bleiben vorrangig; widersprüchliche explizite ID/Slug werden blockiert. Die existierende Repository-Methode `categoryIdByName()` blockiert doppelte Namen bereits – diese Regel ist dort richtig und wird nicht dupliziert.

## 4. Tatsächlich ausgeführte positive und negative Prüfungen

| Teststrecke | Ergebnis |
|---|---|
| Original-PSTE: echte 9 Alt-Placeholder, alte Planhashbindung, Quellenkonfliktlogik, Plan-Leerzustand, Reentry-Beleg | **19/19 PASS** inkl. positive/negative Quellenkombinationen |
| Original-PHP beweist falsche Namenszuordnung | **reproduziert** (ID 942 statt 55) |
| QA-Änderung: **alle 45 doppelten Namen werden ohne eindeutige ID/Slug blockiert**; passende IDs und Slugs für beide Zweige zugelassen; **alle 1.075 eindeutigen Namen** weiterhin korrekt; Konflikt-ID/Slug blockiert; unbekannte Namen bleiben ungeklärt | **1.304/1.304 PASS** |
| Vorherige Gesamtketten-Simulation PSTE .28 mit originalen WP-Daten, Hash-/Typ- und Queue-Proben | **51/51** Originaldatenprüfungen, **12/12** simulierte Worker/Queue-Prüfungen PASS |
| Nach genau **einer** isolierten PHP-Datei-Änderung dieselbe komplette vorhandene `.28`-Teststrecke erneut | PASS; **83/83 PHP-Syntax** PASS |

**Einschränkung:** Die lokale Testdatenbank bildet WordPress-Optionen nach. **Kein tatsächlicher WP-/MySQL-/PSERC-/PPM-/K0-Produktionsdurchlauf.** Insbesondere dürfen die 61 Themen nicht zu „freigegeben“ umetikettiert werden. Beim echten letzten WordPress-Bericht stand weiterhin `COMPLETE / 61 abgearbeitet / 61 gehalten` – Status nicht durch einen Test überschreiben.

## 5. Rootfix ohne Überbau – Reihenfolge

1. **Eine Eigentümerregel pro Inhalt:** Produktionsplan bei PSERC/PPM, SEO-Urteil einmalig bei MINI, Kategorien und Beiträge in WordPress. PSTE-Altimport nur noch Referenz, nie zweite Planfreigabe. Technische Hashes sind Zustandsbelege, keine Entscheidungen.
2. **Ein einziger Kontext-Worker:** Wenn sich die maßgebliche Planquelle tatsächlich ändert, prüft er Inventar + Taxonomie + alte/nachweislich leere Fremdeinträge und baut alle **abgeleiteten** Prüfstände aus dieser Quelle geschlossen neu. Ein Leseaufruf schreibt nichts; ein fehlerhafter Worker meldet `PAUSED`, nie abgeschlossen. Mehrere alte Sonder-Rebind-Wege erst **nach vollständiger Referenzprüfung** entfernen.
3. **Kategorieidentität statt Anzeigename:** ID/Slug eindeutig; Namen allein nur bei exakt einem Treffer, sonst fachlich offen. Keine Kategorien blind löschen.
4. **Bestandsaufnahme aller abgeleiteten Statusfelder:** Nur echte Eigentümerentscheidungen speichern, sonst eindeutige, wiederberechenbare Ansicht. Bestehende SQL-Indizes/WordPress-Kompatibilität vor physischem Entfernen beweisen.
5. **Abnahmevertrag:** normaler Plan, nur neun leere Alt-Platzhalter, wirkliche neue Pläne, absichtlich abweichender Hash, abgebrochener Worker/Wiederanlauf, doppelte Kategorienamen, 61 historische SEO-Belege, 144 geschützte Plätze; danach kompletter WordPress-/PSERC-/PPM-/K0-Weg ohne automatische Veröffentlichung. **Vorher kein Installationsplugin.**

## 6. Beweisquellen

- `PSTE 0.57.144.28 / includes/class-pste-snapshot.php`: `editorialPlanInputs()` und `normalizeEditorialPlanItemsAgainstStructure()`.
- `includes/class-pste-context-index-store.php`: `stagePlan()`, `buildFromStages()`, `runtimeBinding()`, `rehydrateCompletedRuntimeIndex()`, `cleanupCompletedJobArtifacts()`.
- `includes/class-pste-admin.php`: `importEditorialPlan()` – genau ein Schreiber der importierten Planoption.
- `includes/class-pste-repository.php`: `categoryIdByName()` mit Eindeutigkeitsprüfung.
- `PSERC 0.28.55 / includes/class-pserc-plan-compile-job.php`, `class-pserc-system4-import.php`: Produktions- und Laufzeitplan-Verbraucher.
- Original-WordPress-Export `pste-plan-kategorien-pruefstand-2026-11-09.json` und Original-61er-WordPress-Bericht `pste-stapelbericht-2026-11-09(1).json`.
- Reproduzierbare Skripte `qa_plan_sources.php`, `qa_category_test.php`, `audit_probe.php`, Regression `prior_v28_tests/run_checks.sh`, Ergebnisse und `QA_SAFE_CATEGORY_FIX.patch`.