# Gesamter Entscheidungsweg – QA-Prüfung der **ausgelieferten** PSTE .45 / PSERC .69 und aktiven K0-Dateien
Stand: 2026-11-12. **Nur QA, keine WordPress-Live-Abnahme, keine neuen Plugins.**

## 1. Warum früher „alles geprüft“ sachlich falsch war
- Die frühere Test-Quelle und PSTE-.44-ZIP waren nicht bytegleich; in .44 fehlten zwei bereits getestete Änderungen. Korrigiert durch konsolidierte .45, SHA-256 `d3057946defc035af7abe5522c4845625c98ebd3f2cf621e1b3c5ce019f230a4`.
- PSERC .69 SHA-256 `576e58b51db3f348210dc3d47a894d6551558acc0c6900505be5e11257d2e41b`.
- Das lokale 3-Artikel-/64-Fälle-Setup benutzte **nachgebildete WordPress-Daten**, nicht den echten Datenbankzustand mit 5.016 Themen. Es prüfte nicht alle Wege (MINI-Übergabe, Status-Neustart, globaler Snapshotwechsel). „Vollständig getestet“ wäre falsch.

## 2. Geprüft und bereits erledigt – nicht wieder anfassen
- K0: Titel-/Keyword-/Suchintent-**Neubeurteilung** entfernt; bestehende 81 Artikel-/Inhaltsregeln, PPM-Parität und LanguageTool 6.8 bleiben. Aktiver K0-CI **PASS** https://github.com/hallo-netizen/affiliate-pferdeportal/actions/runs/43201428924. K0 trifft keine zweite SEO-Entscheidung, prüft aber weiterhin das fertig geschriebene Produkt.
- PSTE .45: Bei Kontext-Neustart/Fehler **kein pauschales Zurücksetzen aller Freigaben**; normaler alter signierter Intent wird nur transportiert; normaler bereits freigegebener unveränderter Datensatz passiert nachweislich ohne erneute SEO-/Titelentscheidung. Bei geänderten Belegen oder Struktur bleibt Sicherung aktiv.
- PSERC .69: Ein historischer fehlgeschlagener Kontextjob ist allein keine globale Sperre für nachweislich gültige Einzelentscheidungen. Echtes Geändertsein/fehlende Bindung bleibt blockierbar.
- 9 lokale PHP-Retestprogramme der unveränderten .45/.69-Prüfumgebung erneut erfolgreich; darunter 64/64 kombinierte WP-**Mock**-Fälle, 30/30 Original-Metadaten-Lesefälle und 35/35 Vorbereitungsfälle. Keine WordPress-Live-/DataForSEO-Abnahme.

## 3. **Weitere, jetzt belegte** nachgelagerte Hürden – in .45/.69 noch NICHT beseitigt
### A. Abhängigkeitskreis im gesonderten MINI-/externen Agentenweg
- `PSTE_Mini_Workflow::readParkhausForMini` liest einen **aktiven PSERC-Redaktionsplan** und wirft bei fehlendem/veraltetem PSERC-Plan `PSERC_PLAN_NOT_PROVEN_COMPLETE`: `class-pste-mini-workflow.php` Z. 741–750, 976–985.
- `PSTE_Mini_Workflow::forwardToPlan` verlangt das vollständige „Parkhaus“ **vor** Freigabe/Weiterleitung: Z. 625–686.
- Umgekehrt beginnt `PSERC_Plan_Compile_Job::tick(INIT)` nur, wenn PSTE wenigstens ein Quellthema liefert: `class-pserc-plan-compile-job.php` Z. 68–74.
- **Kreis möglich:** PSERC ist veraltet oder leer → MINI kann keine Freigabe weitergeben → PSERC kann ohne Freigabe keinen neuen Plan erzeugen. Das betrifft diesen MINI-Weg, nicht zwangsläufig jedes bereits normal freigegebene PSTE-Thema.
- **Native PHP-Probe auf Originalklasse:** Fehlender PSERC-Snapshot → `PSTE_Mini_Workflow::readParkhausForMini` meldet `complete=false`, Grund `PSERC_PLAN_NOT_PROVEN_COMPLETE`. WordPress-DB simuliert.

### B. Globale Bestands-Hash-Sperre statt Prüfung des betroffenen Themas
- `readParkhausForMini` hasht die **gesamte** WordPress/Plan-Bestandsliste, inklusive Post-Änderungszeit und Inhalt: Z. 841–848, 1121–1142.
- `forwardToPlan` vergleicht den **gesamten** Snapshot-Hash mit der externen Einzel-SEO-Entscheidung: Z. 656–668. Schon eine andere, fachlich irrelevante Artikeländerung kann `PSTE_MINI_PARKHAUS_CHANGED_SINCE_ONE_SEO_DECISION` und eine erneute SEO-Freigabe verlangen.
- **Zulässige Kontrolle:** Ist *genau dieser* Artikel inzwischen schon vorhanden? **Nicht zulässig als Routine:** Unveränderten anderen Artikelbestand zum Anlass einer neuen SEO-Entscheidung nehmen.

### C. Der Redaktionsplan verliert seine Gültigkeit durch Statusänderungen statt durch inhaltliche Änderungen
- `PSERC_Plan_Dependency_Fingerprint::current` bindet den globalen Snapshot ausdrücklich an `context_status`, `context_generation` und `job_uuid`, zusätzlich zu wirklichen Quellenständen: `class-pserc-plan-dependency-fingerprint.php` Z. 65–72, 127–148.
- `::isCurrent` vergleicht den **gesamten Hash**: Z. 168–171. Die Adminanzeige und der Export verweigern bei abweichendem Hash: `class-pserc-admin.php` Z. 24, 92, 106.
- **Native Original-Hash-Probe:** Unveränderte Themen-/WordPress-Quellwerte, nur Kontextjobstatus/Generation geändert → anderer Snapshot-Hash. Das ist eine globale nachgelagerte technische Sperre, *keine* zweite semantische Entscheidung. Sie ist trotzdem ein Hindernis trotz unverändertem SEO-Bescheid.

### D. Zweite semantische Doppelgängerentscheidung für normal freigegebene Themen
- PSTE hat die inhaltliche Duplicate-/Kannibalisierungsentscheidung bereits zentral: `PSTE_Planning_Readiness_Gate::evaluate` (Z. 19–63) und `::apply`.
- In `PSERC_Compiler::compile` wird beim Kandidaten **ohne speziellen MINI-Beleg** erneut `PSERC_Semantic_Duplicate_Gate::againstExisting` und `::againstPreparedCandidates` aufgerufen: `class-pserc-compiler.php` Z. 66–100; identischer Fall in `class-pserc-plan-compile-job.php` `tickCandidate` (Z. 148ff.). Der MINI-Sonderweg überspringt den Zusatzscan.
- **Native PHP-Probe mit Original-`PSERC_Compiler::compile`-Kontrollfluss und bewusst ersetzten Gates:** Bereits als `planning_readiness_gate=PASS` geliefertes Thema ohne MINI-Beleg ruft den zweiten semantischen Checker auf; mit MINI-Beleg wird er übersprungen. Die Probe beweist den **aufrufbaren doppelten Prüfweg**, nicht, dass der zweite Checker schon einen realen Artikel zu Unrecht geblockt hat.

## 4. Kein Doppelurteil: notwendige Kontrollen erhalten
- PSERC prüft die Original-Signatur, unveränderten Titel, Kategorie-/Typ-Zuordnung, unterstützte Beitragsart und eindeutige Planplatz-ID; **keine neue Suchabsicht festlegen**.
- K0 prüft die **neu geschriebenen Texte** und ihre Qualitätsregeln sowie LanguageTool 6.8. Qualitätsprüfung ist ein anderer Gegenstand als die schon entschiedene SEO-Freigabe.
- Der WordPress-Import `PSERC_System4_Import::importPayload` schreibt Entwürfe und meldet den Import an die vorhandene PPM-Redaktionsplan-Verbuchung `PPM679_Editorial_Plan_Runtime_Gate::record_readback`: `class-pserc-system4-import.php` Z. 41–118. Er setzt **nicht direkt** eine PSTE-`topic_pool`-Zeile auf „erledigt“. Der spätere Bestandsabgleich muss bereits importierte Artikel daher erkennen – aber **ohne** alle übrigen SEO-Freigaben neu zu beurteilen.

## 5. KISS – eine einzige konsistente Zielregel, keine vier lokalen Sonderfixes
1. PSTE/externer beauftragter SEO-Eigentümer entscheidet **einmal pro Thema** mit signiertem Quellbeleg (Titel/Keyword/Artikeltyp/Kategorie/Suchabsicht).
2. PSERC **liest und überprüft die Unversehrtheit** dieser Entscheidung, vergibt einen noch freien Artikelplatz. Es startet niemals einen zweiten semantischen Entscheidungsversuch, solange der vorhandene, authentische Erstbeleg für die aktuelle Artikelquelle gültig ist.
3. **Kreis auflösen:** Die Ersterteilung einer SEO-Freigabe darf nicht von einem **erst aus dieser Freigabe erzeugbaren** PSERC-Snapshot abhängen. Die belegten echten WordPress-/PPM-/vorhandenen Planplätze sind der Bestandsbezug; veraltete zukünftige PSERC-Ansichten dürfen nicht die Originalentscheidung ungültig machen.
4. Reine Jobstatus-/Generation-Änderungen **ohne Änderung fachlicher Quellen** dürfen einen freigegebenen Auftrag weder widerrufen noch einen Gesamtrebuild erzwingen. Ist ein bestimmtes Thema tatsächlich betroffen, nur diese konkrete Freigabe zur erneuten Klärung geben.
5. K0 verfasst und prüft den Artikel nach bestehenden 81 Regeln. Beim WordPress-Import wird der Planplatz im existierenden PPM-Register als erledigt verbucht; beim nächsten Themenvergleich wird **nur die neu hinzugekommene Artikelbelegung** berücksichtigt. Keine zweite SEO-Entscheidung.

**Wichtig:** Diese Punkte sind zunächst ein **geprüfter Architekturvertrag**, nicht in die Installations-ZIPs eingebaut. Nächste Umsetzung nur gemeinsam an den originalen Codepfaden, anschließend die **echten ZIPs** mit 5.016 gemischten Themen, 8 gültigen Freigaben, 3 gespeicherten Aufträgen, leerem/veraltetem PSERC-Plan, nicht betreffender WP-Änderung, echter Doppelbelegung, Ausfall/Wiederaufnahme und WordPress-Import simulieren. Ein Test mit nur drei vorausgewählten READY-Einträgen ist kein Beweis.

## Nachweisprotokoll
- Frisch entpackt: PSTE `.45` 121 ZIP-Elemente, PSERC `.69` 63; sha256 oben.
- Native PHP: `qa_native_circular_handshake.php` PASS; `qa_snapshot_invalidation_demo.php` PASS; `qa_native_psc_secondary_duplicate.php` PASS. Alle mit beschriebenen Testdoubles, keine reale WP-DB.
- Vorherige 9 PHP-Mock-/Originalmethodenprogramme alle mit Exit 0 erneut erfolgreich.
- **Echte Ursache des 0-READY-Zustands auf der WordPress-Testseite ist weiterhin nicht nachgewiesen**, da kein Datenbanklesezugriff vorliegt. Keine Releasebehauptung, keine neue ZIP, keine produktive Änderung.
