# Pferdeatelier – K0-Dateiübergabe / verlustfreie Verschlankung, 10.11.2026

**Status: QA-Quell- und Screenshotprüfung; KEINE Code-/DB-/Live-Änderung, KEINE End-to-End-Freigabe.** K0 unverändert. PSERC-v0.28.56 ist eine frühere isolierte QA-Variante, ausdrücklich nicht zur Installation aus dieser Prüfung freigegeben.

## Konkreter TEST-Screenshot vom 10.11.2026, 10:32 Uhr
- WordPress-Testseite oliver-beil.de, PSERC-Admin-Build `0.28.55-one-owner-no-fallback`.
- Anzeige: letzter aktiv geprüfter Snapshot mit **5.016 Themen, 0 READY** (veraltet).
- Neuer asynchroner Lauf: `BLOCKED`, `phase=ACTIVATE`, `error_code=PSERC_PLAN_LIVE_EDITORIAL_PLAN_CHANGED_BEFORE_ACTIVATE`. Vorheriger Screenshot: `1 geeignet / 1 geprüft / 0 READY`.
- **Nicht** als Ursache behaupten, dass 5.016 Kandidaten fachlich erneut beurteilt würden: `PSERC_Plan_Compile_Job::start` liest den Gesamtzähler nur für Statistik; `PSTE_Repository::compilerPlanningTopicCount/Page` filtert `planning_suitability=YES` und `context_state CURRENT/NOT_REQUIRED` plus Route K0. Die eine geeignete Position aus dem Screenshot ist plausibel, aber die konkreten WP-Datensätze sind nicht vorliegend.
- Der ACTIVATE-Fehler entsteht **exakt** in `PSERC_Plan_Compile_Job::tickActivate`, wenn `PSERC_Plan_Dependency_Fingerprint::liveEditorialPlanMatches` den zu Start gebundenen `final_plan_sha256` gegen `PSTE_Snapshot::editorialPlan()` neu vergleicht und der Wert nicht mehr übereinstimmt. Ohne read-only Vergleich der zwei tatsächlichen WP-Werte ist **nicht** bewiesen, welcher Planinhalt sich wann warum verändert hat. Sperre nicht umgehen.

## Vorhandene richtige Dateiausgabe bereits nachgewiesen
- `PSERC_Admin::exportLivePreview` ruft `PSERC_Plan_Snapshot_Store::materializeReadyBatch` und `PSERC_Metadata_Boundary::validateBatch` aus bestehenden Klassen auf. **Keine neue Ausgabestelle erforderlich.**
- Vertrag `PSERC_TEXTMACHINE_METADATA_BATCH_V2`, Status `READY_FOR_TEXTMACHINE_METADATA_INTAKE`, exakt fünf Felder je Thema: `title, target_keyword, category, article_type, plan_slot`; zusätzliche Batch-Steuerfelder und `batch_sha256`; `publish_allowed=false`. Das aktive K0-`K0_CURRENT_STATE.json` bestätigt diesen Eingang.
- Tatsächlich im unveränderten PSERC 0.28.55 wieder ausgeführt: 7/7 unabhängige lokale Format-/Sicherheitstests PASS (gültige 2 Metadatenpositionen, `requireReadyBatchForExport`, leere Liste blockiert, Zusatzfeld blockiert, Doppel-Slot blockiert, Titelmanipulation blockiert, Publikationsfreigabe blockiert). **Kein echter WordPress-Handoff mit >=1 READY, kein kompletter K0-Produktionslauf.**
- Das in .55 bereits vorhandene `requireReadyBatchForExport` sperrt leere Daten; `exportLivePreview` verwendet in .55 nur `validateBatch`. Der frühere .56-Entwurf tauscht nur den Funktionsaufruf aus und ist kein relevanter Integrationsfix. Nicht ohne Freigabe installieren.

## Konkrete Lücke in der Anbindung
- Der echte v29-WP-Stapelbericht vom 09.11.2026 dokumentiert **7 PASS in NORMAL_PATH** mit `planning_gate_status=PASS, planning_suitability=YES`; dies ist nicht identisch mit `READY_FOR_METADATA_HANDOFF` in PSERC.
- `PSERC_SEO_Reader::normalizeCandidate` fordert zusätzlich K0-Route, Artikelrolle, genaue fünf Feldnamen, `textmachine_handoff_status=READY_FOR_COMPILER_CAPABILITY_CHECK`, gespeicherten Titel, Kategorie-Slug, Artikeltyp und gültigen externen Freigabebeleg; ungeprüfte/alte Kandidaten bleiben HELD. `PSTE_Normal_Metadata_Path::applyToPayload` setzt diese Handoff-Felder im bestehenden PSTE-Pfad.
- Die alte ACTIVATE-Sperre ist **separat** vom noch unbelegten erfolgreichen READY-Export. Erst den tatsächlichen TEST-Plan-Fingerprint vergleichen, dann prüfen, welche vorhandenen PASS-Kandidaten welchen konkreten Handoff-Status und Sperrgrund tragen.
- Kein automatisches oder manuelles Erfinden eines Plan-Slots; der Slot wird aus der vorhandenen verifizierten PSERC/PPM679-Planung gebunden.
- **Nächster Beweis:** Ein konkretes freigegebenes PSTE-Thema über die bestehenden WP- und PSERC-Klassen als `READY_FOR_METADATA_HANDOFF` nachweisbar lesen, vorhandenen Download erzeugen, ZIP/JSON nicht umformatieren, Datei gegen original `PSERC_Metadata_Boundary` und K0-Eingangsvertrag prüfen; ohne Artikelproduktion. Bei 0 READY die tatsächlichen gespeicherten Detail-Statusgründe auslesen, keinen Compilerblindlauf wiederholen.

## Verschlankung – zwingende Trennung
1. **Sofort behalten**: PSTE-Rohdaten/Recherche/Historie, externe einmalige SEO-Entscheidungen, Titel, Kategorie und Redaktionsbüro; PSERC-Reader, Slot-/Kanonikbindung, Original-`Metadata_Boundary`, Export, signierte Pläne, Aktivierungs-/Frische- und Integritätsprüfungen, PPM679, K0.
2. **Frontend/Backend vereinfachbar (bei nachgewiesenem neuen Normalweg)**: PSERC-Admin zeigt den *Artikel-WordPress-Entwurfsimport* über der reinen K0-Metadatenansicht, obwohl er erst **nach** K0 relevant ist. Als eigene, klar beschriftete Experten-/Nachproduktionsfunktion erhalten statt löschen. Alte Diagnoseflächen in PSTE lediglich unter `Weitere Werkzeuge` bündeln, sofern weiterhin erreichbar.
3. **Potentieller Codeabbau, noch nicht freigegeben**: redundante semantische Entscheidung im PSERC-Legacypfad, wiederholte manuelle Titel-/Kategoriefreigaben, alte globale UI-Navigation und Sonderwege. Zuerst alle PHP-Direkt-/Hook-/AJAX-/Cron-/CLI-Referenzen, gespeicherte Options- und DB-Leser, GitHub-Zielverträge und Altfall-Fallbacks nachweisen. Dann nur tatsächlich verwaisten Code auf isolierter Kopie entfernen.
4. **Verbote**: Keine Tabellen/Optionen/Snapshots/ZIP-Archive/Recherche/Funktionen/gespeicherten Resultate löschen; keine Schutzsperren entfernen; keine Nutzer- oder Live-Daten verändern; K0 unangetastet; keine neue Datei-Engine; keine .56-Installation wegen bloßer Codeänderung.

**Abnahmebedingung für technische Verschlankung:** Vorher/Nachher identische Datenanzahl, alle benötigten Funktionen erreichbar, identisches PSERC-V2-K0-Dateiformat, echte WP-TEST-Wiederholprobe samt Negativfällen, NULL Datenmigrationen bzw. verifizierte Verlustfreiheit, ursprüngliche K0-Grenze unverändert. Erst dann darf eine alte Funktion entfallen.
