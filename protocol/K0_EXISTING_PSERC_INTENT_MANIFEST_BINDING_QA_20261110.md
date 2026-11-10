# K0 – einmalige SEO-Entscheidung aus bestehendem PSERC-Plan übernehmen (QA)

**Stand 10.11.2026. Nur isolierte Testkopien. K0 aktiv `konzept0-portal-neutral-20261002` und WordPress NICHT verändert.**

## Nachgewiesene Ursache
- PSTE DataForSEO/SEO-Owner entscheidet Suchintention **vor** der Textproduktion. PSERC übernimmt sie bereits in `PSERC_Compiler::finalizeAllocationRow()['intent_profile']`.
- Der alte Download `PSERC_Plan_Snapshot_Store::materializeReadyBatch` enthält aber nur die **exakt fünf** erlaubten Metadatenfelder; es ist **mathematisch unmöglich**, einen nicht enthaltenen, möglicherweise inhaltlich variierenden Intent aus genau diesen fünf Feldern nachzuweisen.
- Wichtiges KISS-Ergebnis: PSERC besitzt bereits `PSERC_Plan_Snapshot_Store::manifestForSelectedBatch`, das denselben unveränderten **5-Feld-Batch** und die nach `plan_slot` verknüpften **bereits vorhandenen Original-Intentprofile** in **einem** Manifest enthält. Keine neue Fachentscheidung, Tabelle, Worker oder Keyword-Regel erforderlich.

## Kleinstmögliche PSERC-Änderung (neue QA-Test-ZIP 0.28.61)
- BASIS: `PSERC-0.28.60-KISS-EXTERNER-SEO-OWNER-NUR-TEST.zip`.
- **Genau drei Original-Plugin-Dateien geändert**, 60/63 übrige Dateien **byteidentisch**: `includes/class-pserc-admin.php` (ein zusätzlicher Download-Button + schreibfreier Export aus dem BEREITS VORHANDENEN Manifest); `portal-seo-editorial-plan-compiler.php` (Version/Build); `contracts/compiler-package-binding-v1.json` (verifizierte Paketprüfsummen nach Änderungen).
- Originalbutton `Kompakten Produktions-Handoff als JSON herunterladen` und strikter Fünf-Felder-Vertrag **unverändert**. Zusätzlicher Button `K0-Übergabe mit bestätigter Suchintention herunterladen` liefert das **existierende unveränderte** Compiler-Manifest, in dem der gleiche Fünf-Felder-Batch enthalten ist.
- Vor Export: bereits vorhandenen Snapshot-/Abhängigkeitsnachweis, vollständige Metadatenfreigabe, Manifesthash sowie jedes Original-PSTE-`intent_profile` auf Status PASS, Artikeltreue, Nichtleerheit **und echten PSTE-Profilhash** prüfen. Bei Fehlern STOPP; niemals Intent neu berechnen.
- **43/43 PHP-Dateien syntaktisch PASS**; `PSERC_Package_Integrity::validate` mit **61/61** geschützten Dateien PASS; ZIP-CRC PASS. Alte DataForSEO/PSTE-Funktionen und alle 60 übrigen PSERC-Dateien unverändert.
- **PHP positive Funktionsprobe:** tatsächliche originale `PSERC_Plan_Snapshot_Store::materializeReadyBatch + manifestForSelectedBatch` + die neue `PSERC_Admin::exportK0Manifest` im simulierten WordPress-DB-/Optionsumfeld mit den **drei echten PSERC-Artikel-Identitäten**. Quelle der jeweiligen `intent_profile` ist im Test ausdrücklich **synthetisch**, nicht aus dem echten WP-Snapshot; Funktionseigenschaften PASS.
- **4 negative PHP-Gegenproben** PASS: freigegebener Intent fehlt, Intentprofil ist REVIEW_REQUIRED, Profilhash ist falsch, Snapshot ist veraltet. Erwarteter sicherer Abbruch.
- Archiv im persönlichen Pluginbüro: `/pferdeatelier/PLUGINS/QA/PSERC-0.28.61-K0-INTENT-BINDUNG-NUR-QA-NICHT-INSTALLIEREN.zip`, Dateihash (SHA256) `2365a251bb799a2d6d6b2a5c9fd178ec04e874bf3a2a43ab86d21cb2c3b7e20c`.
- PSTE aktuelle TEST-Version `0.57.144.33` **nicht verändert**; DataForSEO normaler dreistufiger Rechercheweg bleibt.

## K0-Änderung NUR auf `qa/k0-editorial-owner-only-20261110`
- Neue einzige technische Bindungsfunktion `engine/k0_seo_owner_binding.py`, kein SEO-Entscheidungsworker.
- **Verifiziert** Originalmanifest-HASH und PSTE-INTENT-PROFILHASH (einschließlich der tatsächlichen PHP-Kodierung von Zahlen/SEO-Wahrscheinlichkeiten), Original-`plan_slot`, alle fünf Artikel-Identitätsfelder und READY/PASS, verhindert doppelte oder manipulierte Einträge.
- `bind_context` übernimmt **nur** die bereits vorhandene Suchintention in `AUTHORING_CONTEXT.content_profile.search_intent` und bindet Originalprofil-/Manifest-/Batchhash; bei widersprüchlichem von K0 vorgeschlagenen Wert sicherer STOPP; kein stilles Überschreiben.
- Im **bestehenden** K0-Authoring-Workflow ist das Binden **vor dem Writer** eingefügt. Pro Einzelartikel ist die Original-PSERC-Manifestdatei `PSERC_SOURCE_MANIFEST.json` neben dem bisherigen `WORDPRESS_INTAKE.json` und `AUTHORING_CONTEXT.json` erforderlich. Ohne Quelle sicherer STOPP. Die ursprüngliche 5-Feld-Datei selbst wird **nicht** um ein sechstes Feld erweitert.
- Alle bestehenden K0-Text-/Fakten-/Absatz-/Wort-/Listen-/Tabellen-/Wiederholungs-/Link-/LanguageTool-/WordPress-Export-Regeln und die Vor-/Nach-LT-Prüfung **unverändert**. Original K0-Writer/WordPress-Exportdateien byteidentisch.
- **[GitHub Testlauf 42845622779](https://github.com/hallo-netizen/affiliate-pferdeportal/actions/runs/42845622779) PASS:** **51 alte + 7 SEO-Owner + 11 Quellenbindungs-Tests = 69/69 PASS** sowie vollständiger schreibfreier K0-Regressionstest mit **3 echten Identitätsübergaben und je einem gebundenen Writer-Auftrag**, **1 früher fertigem realem Artikel**, allen 80 Vor-LT-Regeln, **echtem LT6.8 PASS**, 81 finalen Regeln, erstellter/verifizierter WordPress-Importdatei PASS. Für Bindung dient **ausschließlich ein synthetisches PSERC-Profil**; keine echte neue DataForSEO-Recherche und keine echten neuen 3 Artikel.

## NOCH OFFEN – kein Live-GO
1. Die **tatsächlich installierte** WordPress-TEST-Kombination und der **echte aktuelle PSERC-Snapshot mit originalem DataForSEO/PSTE-Profil** wurden **nicht** ausgelesen/aktiviert. Tests an echtem PSERC-Originalsnapshot fehlen. **Nicht als gesichert behaupten**, dass die 3 historischen Titel denselben SEO-Intent haben wie im Testfixture.
2. Die PSERC .28.61 QA-Testdatei wurde erstellt, aber **nicht im WordPress-Testsystem installiert**. Nach einer solchen Installation könnte der alte PSERC-Plan wegen Paket-/Abhängigkeitsprüfsummen als veraltet gelten und einen frischen **PSERC-Plan-Snapshot** verlangen. Kein ungeprüfter Umbau, kein automatischer DataForSEO-Providerabruf.
3. End-to-end-frisch für 3 **neu** recherchierte Artikel und WordPress-TEST-Import ist noch **nicht** durchgeführt.
4. Für die finale Integration des vorhandenen `K0:start`-Eingangs muss der **eine** neue Manifest-Download als Eingang akzeptiert, daraus der unveränderte 5-Feld-Batch entnommen und dieses Manifest für jeden Einzelartikel an den K0-Vorbereitungsjob weitergegeben werden. Die Python-Funktionen `extract`, `bind`, `verify` existieren auf QA; der echte Chat-Eingang wurde nicht umgestellt.

**STAND: QUELLENWEG_CODE_VORBEREITET, PSERC_QA_PAKET_INTEGRITY_PASS, K0_69_REGRESSION_PASS, VOLLER_K0_ECHT_LT_REPLAY_PASS; ECHTES_UPSTREAM_WP_INTENTPROFIL_NICHT_GETESTET; AKTIVIERUNG_NEIN.**
