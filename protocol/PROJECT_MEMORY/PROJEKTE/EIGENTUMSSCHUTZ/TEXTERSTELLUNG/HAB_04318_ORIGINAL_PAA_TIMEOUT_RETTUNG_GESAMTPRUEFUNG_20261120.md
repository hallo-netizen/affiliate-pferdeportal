# Hab & Bewahr v0.4.31.8 – Originalworkflow/K0/Hobbydepot PAA-Reparatur, 20.11.2026

**Echt angehängte WordPress-Diagnose** `texterstellung-diagnose-20261120-094148.json`: live installiert `0.4.31.7`, `original_research.queue_status=COMPLETE`, ein `BLOCKED_PARKED`-Auftrag, `PSTE_PAA_TASK_TIMEOUT`, alte Phase `QUESTIONS/TASK_PENDING`, `archived_paid_task_id_present=true`. 5 erhaltene rohe Keywords, **0** Nutzkandidaten; kein aktueller echter K0-Auftrag/WordPress-Draft. Diese Diagnose beweist den Timeout, **nicht** dass DataForSEO den alten Task gelöscht hat.

## 1. Originaldateien tatsächlich entpackt und byteweise verglichen
- Pferdeatelier `Texterstellung-0.4.34-MANUELLES-VEROEFFENTLICHEN.zip`, SHA256 `14a3976702fa782e110184c3abc8eba82a0225f28384b4d540488c96f65dfb6b`.
- Hab 0.4.31.7, SHA256 `974cc101c52f274a1abf0a4777ada114e08610a5f08b10f386c3da1ff0760459`.
- Hobby 0.4.24.13, SHA256 `71447b3d31f758d292153695971845d13e035f60932244bfe3f5e499a9d887b5`.
- Hobby 0.4.24.15, SHA256 `22048ef1850d44d922d6738a40c5cebcd4a6a474a393c26b5d1f86888510092b`.

**Gleicher Fehler in Original Pferd und Hab:** `original/pste/includes/class-pste-research-job.php::advanceQuestionsTask` fragt vor dem direkten Task-GET nur `serp/google/organic/tasks_ready`; nach 1800 Sekunden setzt der Originalcode `PSTE_PAA_TASK_TIMEOUT`, obwohl `tasks_ready` nicht beweist, dass die spezielle bereits erstellte Task-ID nicht mehr abrufbar ist. **Hobby v0.4.24.15 enthält bereits den besseren Originalweg**, `inspectPeopleAlsoAskTaskById` mit `GET /serp/google/organic/task_get/advanced/<exakte alte ID>` sowie `restoreParkedPaaResult` und `resumeTimedOutPaaChild`. Keine neue Task, kein neues POST, keine doppelte kostenpflichtige Recherche.

## 2. Reparatur im bestehenden HAB-Plugin, keine neue Architektur
Exakt den PAA-Direkt-ID-Abruf und archivierten sicheren Wiederaufnahmeweg der bereits geprüften Hobby-Originalfunktionen auf die Hab-Version 0.4.31.7 angewandt. Vorhandener Admin-Menüpunkt `Texterstellung → Recherche`: Nur bei einem passenden einzelnen archivierten PAA-Timeout steht neu `Gesperrten Auftrag prüfen und falls fertig fortsetzen`. Der bereits existierende, **selbe** Auftrag wird abgefragt, kein neuer bezahlt.

Neues Ersatz-ZIP **0.4.31.8**: `Texterstellung_HAB_UND_BEWAHR_0.4.31.8_ORIGINAL_PAA_RETTUNG.zip`, SHA256 `386f303f97c117ad639f2ceeaafe26c86045705b33d810fe4667c615c50ec24a`, 522842 Bytes. **82/87 Dateien byteidentisch** mit installierter 0.4.31.7; 5 Änderungen ausschließlich `class-pste-dataforseo-client.php`, `class-pste-research-job.php`, `class-pste-breadth-research-queue.php`, `texterstellung.php` (Aktion, Knopf, Versionsnummer) und README. Unverändert: PSTE-Research-Driver, vier originale Keyword-/PAA-Wege, Hab v0.4.31.7-Produktseed, Original-MINI, PSERC-Importer, K0-Fünffelder, sämtliche Original-K0-GitHub-Quellen.

## 3. Reproduzierbare echte lokale Tests der vorhandenen PHP-Funktionen
- **48/48** unveränderte vier Keywordrecherchewege/Abholbox-Seed und Kategorieidentität.
- **17/17** originale Hab-MINI/Artikelarten/Kategorieprüfungen.
- **14/14** originale Hab K0-Paket/PSERC-Entwurfsimportprüfungen (fiktiver Artikeltext).
- **11/11** unveränderte originale PAA-Direkt-Clientfunktion im WP-/Provider-Mock: READY, PENDING 40601/40602, echte Fehlerstatus, falsche ID, Duplicate, ungültige ID, READ transport error, GET-only.
- **8/8** originale archivierte Warteschlangen-Wiederaufnahme mit tatsächlichem Client im Provider/WP-Mock: alter Task PENDING/READY/PROVIDER_ERROR, fremder Besitzer, fehlendes Archiv, fremder aktiver Job, manipulierte Task-ID, falscher Queuezustand.
- **11/11** originale `PSTE_Research_Job::restoreParkedPaaResult` und `persistQuestionsResponse` tatsächlicher PHP-Funktionen: 3 vorangegangene Keyword-Phasen behalten, alte signierte Originalkennung behalten, Fragen FULLY persisted und `FINALIZE`, PAA-Kosten nur einmal, Mehrfach-/Fremd-/Manipulationsfälle gesperrt.
- **Summe 109/109 PASS**, zusätzlich **78/78 PHP-Syntax**, **87/87 ZIP-CRC**, 82 Dateien absolut unverändert.
- Original Hobby13 `e2e-ported-mini.php` reproduziert `FAIL ORIGINAL HORSE AUTO-FINAL on last TITLE`; Hobby15 derselbe Test **PASS** bis Original K0-Paket und **simuliertem** WP-Import.
- Pferdeatelier: 2 echt früher geschriebene, verifizierte K0-Artikel erfolgreich durch original PSERC-Importer in **simuliertem WP** als zwei Drafts aufgenommen, fehlerhafte Planplätze/Slug abgewiesen, Duplikate verhindert.
- Isolierter K-Multi: Signierter fünfteiliger Original-Hobby15-Auftrag bis `KMULTI_EXISTING_RESEARCH_HANDOFF_V1` getestet, Ergebnis `writer_can_run=false` mit **synthetischen** Forschungsdaten. **Kein KMulti-Text, kein neuer Horse K0-Lauf**.

**Keine** echte HTTP-Anfrage und keine WordPress-Schreiboperation bei diesen Tests; kein Live-E2E-PASS. Tests, Originaldiff und ausführliche Nachweise liegen im Hab-Büro `/hab-und-bewahr/TEXTERSTELLUNG/PRUEFUNG_PAA_20261120/`; Ersatz-ZIP unter `/hab-und-bewahr/TEXTERSTELLUNG/PLUGIN_FREIGABEKANDIDATEN/`. Upload in die Library nachgeprüft.

## 4. Konkreter nächster Schritt, ohne neue Kosten
1. WordPress-Backup; **bestehendes** Hab-Texterstellung 0.4.31.7 durch 0.4.31.8 ersetzen. Nicht deinstallieren; alte Originalwarteschlange muss erhalten bleiben.
2. `Texterstellung → Recherche → Letzte Kategorien-Recherche → Gesperrten Auftrag prüfen und falls fertig fortsetzen` einmal drücken.
3. Das Ergebnis direkt auf der Seite prüfen; danach die aktuelle Diagnose-JSON exportieren. **Nie** kostenpflichtige Kategorie-Neurecherche starten, solange der alte Task wiederaufnehmbar ist.
4. Bei PENDING/PROVIDER_ERROR bleibt altes Archiv unverändert; keine Erfolgsmeldung ohne Anbieter-Readback.
5. Danach ursprüngliche post-research Familien-/Synonymrelevanz (`Paketbox`) **einmalig** am zuständigen originalen Owner prüfen. K-Multi-Writer, LT68, realer WP-Draft und echte aktuelle Keyword-Daten bleiben als fehlende Produktionsabnahme vermerkt.

**Kein Original-K0 geändert. Nicht als vollständig funktionsfähige neue Artikelschreibmaschine melden.**
