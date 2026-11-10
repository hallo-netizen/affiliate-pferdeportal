# PSERC 0.28.58: KISS-Planbindung und verlustfreie Admin-Vereinfachung — 10.11.2026

## Stand
**Echte WordPress-Testseite noch nicht durchlaufen.** Die vorhandene PSERC-0.28.55-Test-ZIP wurde in einer **eigenen** isolierten QA-Arbeitskopie korrigiert. K0, PSTE, WordPress-Daten, gespeicherte Themen, Recherchen, Original-ZIPs und Live wurden **nicht geändert**. Keinerlei Migrations-/Löschfunktion.

Private Test-ZIP: `/pferdeatelier/PLUGINS/QA/PSERC-0.28.58-KISS-PLANBINDUNG-NUR-TEST.zip`, **SHA256 `799488f1b42788b207a26ea9e5d115d3406f065b2c8a82041f673869f298c1f0`**.

## Harte Code-Ursache
- Die originale PSTE-Klassenfunktion `PSTE_Compiler_Read_Capability::requireFreshPlanningSources` akzeptiert **nach belegtem, validem Runtime-Index-Rebind** den aktuellen WordPress-Baseline-Plan statt des früheren Context-Jobs (historische Prüfsumme). Dabei werden tatsächliche WP-Quelle, ursprüngliche Kontextidentität und aktueller Index weiter verifiziert.
- Die originale PSERC-Funktion `PSERC_Plan_Dependency_Fingerprint::liveEditorialPlanMatches` wertete bisher **nur die historische** `context.final_plan_sha256` aus. Wenn die nachweislich gültige laufende Baseline eine andere Plan-Prüfsumme hat, blockiert sie erst am Ende: `PSERC_PLAN_LIVE_EDITORIAL_PLAN_CHANGED_BEFORE_ACTIVATE`. Dies erklärt einen **möglichen** Fehlstopp bei korrekt umgebundener Quelle; das konkrete Datenpaar auf der Benutzer-Testseite wurde nicht ausgelesen und die Ursache dort ist daher noch nicht endgültig bestätigt.
- Die Ausgangs-PSERC-Dateiausgabe `PSERC_Admin::exportLivePreview` und `PSERC_Plan_Snapshot_Store::materializeReadyBatch` bleiben bytegleich. Kein neuer Exporter.

## Minimaländerung
Nur vier vorhandene PHP/Basisdateien plus das Integritätsmanifest (5 von **63 ZIP-Dateipfaden**):
1. `class-pserc-plan-dependency-fingerprint.php`: bindet **zusätzlich** den bereits vorhandenen aktuellen `PSTE_OPTION_SITE_BASELINE.editorial_plan_sha256`-Wert in die bisherige Planabhängigkeit ein. Der historische Wert bleibt für Nachweise erhalten. **Beide** Aufrufvarianten (normal und explizite Kategorie-ID-Liste beim ACTIVATE) lesen denselben Baseline-Wert. Bei veränderter Planquelle oder Baseline bleibt Sperre.
2. `class-pserc-plan-compile-job.php`: ruft die **bereits vorhandene** finale Quellfrischeprüfung schon beim Start auf, statt Arbeit erst bei ACTIVATE zu blockieren; finale Kontrolle bleibt unverändert.
3. `class-pserc-admin.php`: vorhandenes Formular **„Artikel → WordPress-Entwürfe“** ist hinter dem ausklappbaren Abschnitt **„Nach K0 ...“** verborgen. Funktion/Hooks/POST bleiben erhalten, nur Übersicht einfacher. Kein Code gelöscht.
4. `portal-seo-editorial-plan-compiler.php`: Versions- und Buildkennung.
5. `contracts/compiler-package-binding-v1.json`: vorhandene 61 verifizierte Paketdateien mit neuen Hashes/Größen, korrekt neu gebunden.

## Lokal belegter Test
- **9/9 direkte Original-PHP-Testfälle** mit ursprünglicher `PSTE_Compiler_Read_Capability`, tatsächlich geladener neuer `PSERC_Plan_Dependency_Fingerprint` und `PSERC_Plan_Compile_Job`: aktueller Rebind A→B PASS; originaler PSTE-Leser mit B PASS; normale und erzwungene ID-Abhängigkeit identisch PASS; bestehender READY-Snapshot erreichbar PASS; wirkliche Live-Planänderung früh gesperrt PASS; finale Sperre bleibt PASS; nachträglich geänderte Baseline invalidiert Fingerprint PASS; unvollständiger Kontext gesperrt PASS.
- **Original-PSERC-Paketintegrität PASS (61/61 Dateien gebunden)**.
- **43/43 PHP-Syntaxprüfungen PASS**; **63 gleiche ZIP-Pfade**, übrige 58 Dateien bytegleich; ZIP CRC PASS.
- **Vorherige K0-Metadaten-Abnahme 0.28.55 unverändert**: exakt fünf Pflichtfelder, keine Inhalte, keine Publikationsfreigabe. Diese Abnahme wurde NICHT als echter 1-READY-WordPress-Test ausgegeben.

## Einziger nächster Test (nur WordPress-TEST)
1. **Vorher Testdatenbank/aktuelle .55-Plugin-ZIP sichern**. Nur PSERC **0.28.58** auf der isolierten Testseite aktualisieren, PSTE und K0 unverändert lassen.
2. Im PSERC-Menü den alten BLOCKED-Status **einmal** über die vorhandene Aktion `Snapshot nach der Produktionswelle aktualisieren` erneut durchlaufen lassen; keine Keyword-Neuimporte und kein externer MINI-Neustart. Prüfstatus der Seite mitteilen.
3. Wenn `Metadaten-Handoff bereit >=1`: **bestehende** Schaltfläche `Kompakten Produktions-Handoff als JSON herunterladen`, unveränderte Datei als echten Nachweis prüfen. Bei `0 READY`: direkt den konkreten vorhandenen PSERC-Statusgrund auslesen und ausschließlich diesen beheben; keine weitere globale Prüfkampagne.
4. Erst wenn echtes TEST-WordPress→PSERC→K0-V2-Dateiformat bestanden ist, den restlichen toten Code per Referenz-/Hook-/Datenspeicher-Abhängigkeitsprüfung entfernen. **Keine Tabellen, Optionen, Forschungen, registrierten Funktionen oder Datensätze löschen.**

**Einschränkung:** Dies ist ein WordPress-TEST-Paket, **keine Live-Freigabe** und noch kein bestandener vollständiger Dateihandoff auf der Benutzer-Testseite. Draft-PR #682 bleibt isoliert/unmerged.
