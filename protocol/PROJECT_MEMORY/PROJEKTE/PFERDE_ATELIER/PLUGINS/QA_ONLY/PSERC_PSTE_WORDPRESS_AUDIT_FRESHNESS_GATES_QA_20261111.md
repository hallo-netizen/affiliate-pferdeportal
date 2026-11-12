# Pferdeatelier – letzte PSERC-Schutzlücke nach lokalem Volltest (11.11.2026)

**Stand: QA-Quellpatch vorhanden, 1.280/1.280 echte lokale PHP-Aufrufprüfungen bestanden, KEIN INSTALLATIONSPAKET und keine echte WordPress-DB geprüft.** Keine K0-, Live- oder WordPress-Änderungen.

## Neuer, im Originalcode nachgewiesener Fehler

Die vorhandene `PSTE_Breadth_Research_Queue::existingOnlyAuditCurrent()` entscheidet korrekt über die **Gültigkeit der vollständigen gespeicherten Themenprüfung**. Der reine PSERC-Abgleich `PSERC_Plan_Dependency_Fingerprint::isCurrent()` prüft nur, ob seine technischen Plan-Eingaben dieselbe Identität besitzen. Vor dem Fix wurde der zweite Test verwendet, ohne den ersten direkt zu verlangen:

- `PSERC_Admin::page()` zeigte bei technisch gleichem Plan weiter die drei READY-Artikel, selbst wenn die PSTE-Bestandsprüfung veraltet war.
- `PSERC_Admin::exportSingleHandoff()` konnte den alten Download erneut liefern.
- `PSERC_Plan_Compile_Job::start()` konnte den alten Plan ohne gültige vollständige Auditquittung wiederverwenden.
- `PSERC_Plan_Compile_Job::tickActivate()` prüfte den Auditstatus am Freigabepunkt nicht noch einmal.

**Dies ist keine bloße Hypothese zur Artikelqualität**: Die fehlenden Aufrufe wurden in den tatsächlich physisch geprüften PHP-Klassen des zusammen gepackten PSERC .28.64 nachgesehen. Der dynamische Test verwendet eine Fake-WordPress-Umgebung, kein echtes WP/MySQL.

## Minimaler Quellfix (nur QA-Quellpatch)

- Zentrale Methode `PSERC_Plan_Dependency_Fingerprint::existingPsteAuditCurrent()`: ruft **nur den bestehenden PSTE-Auditwächter** auf; keine zweite eigene Recherche, Prüfung oder gespeicherte Zustandstabelle. Fehlende Klasse, ungültige / unterbrochene Prüfung → false.
- Adminanzeige erlaubt READY/Download nur, wenn sowohl technische Aktualität als auch PSTE-Audit gültig sind.
- Export bricht bei veraltetem Audit **vor** dem Lesen des alten Batches ab.
- Compiler-Start verlangt aktuelles PSTE-Audit vor Wiederverwendung des aktiven Plans.
- Compiler-Aktivierung verlangt es erneut, weil der Nachweis während eines laufenden Auftrags veralten kann.

**QA-Quellen** (GitHub, bewusst nicht als ZIP):
- [Audit-Patch](PSERC_PSTE_AUDIT_FRESHNESS_DOWNLOAD_GATES_20261111.patch), SHA256 `46d6c351666015de49f6fb35de519888e556211bbace3cb647ecb70e2da05658`;
- [wiederholbarer PHP-Routentest](PSERC_PSTE_AUDIT_FRESHNESS_ROUTE_TEST_20261111.php), SHA256 `27e39e806c23117a15956b2542533d4a3dc11c72ce601b1accc9baa84801b07c`.

## Local Replay – tatsächlich ausgeführt

Originale Klassen aus PSERC .28.64 + nur drei gezielte Änderungen in isolierten QA-Quelldateien. Alle drei geänderten PHP-Dateien sowie der Test lint-frei. Ergebnis:
- **1.080 positive/negative lokale Tests** = 60 Wiederholungen × 3 Audit-Zustände (aktuell, fehlend, Exception) × 6 echte Prüfrouten (zentrale Auditfunktion, Compilerstart, Admin-Download-Sichtbarkeit, Altplan-Warnhinweis, tatsächlicher Export-Aufruf, Compiler-Aktivierung).
- **200 zusätzliche Race-Tests** = 50 Wiederholungen mit Nachweis gültig beim Start und ungültig **vor** Aktivierung/Download, anschließend Wiederherstellung. Jede ungültig gewordene Freigabe wurde gesperrt.
- **1.280/1.280 PASS**. Positive Zustände dürfen die jeweiligen nächsten Originalfunktionen erreichen, invalidierte Zustände werden blockiert. Test verwendet Reflectionsaufrufe echter PSERC-Klassen und gefälschte WP-Optionswerte; er überschreibt keine Original-Plugin-Dateien.
- Zuvor protokollierte End-to-End-Simulationen mit 3 echten Artikeldatensätzen und 5.562 Prüfungen / weiteren 331 Prüfungen bleiben gültig **für deren ausdrücklichen Umfang**. Der neue Test deckt jetzt zusätzlich die externe Admin-/Job-Grenze ab.

## Freigabe und Folgearbeit

**Kein neuer Download, keine Installationsbitte.** Die früher archivierte PSERC .28.64-Test-ZIP enthält diesen Zusatzschutz **noch nicht** und darf nicht als endgültig freigegeben werden. Erst nach Integration in einen erneut versiegelten QA-Paketvertrag und wirklichem WordPress-TEST: Audit der vorhandenen PSTE-Bestandsdaten komplett, BOUND_TYPE gespeichert, PSERC-3-READY frisch und eindeutiger Download `mit-suchintent-nachweis`. Der tatsächliche WP/DB-Test wurde weiterhin **nicht** durchgeführt.

**Status:** `QA_SOURCE_GUARD_FIXED`; `LOCAL_POS_NEG_1280_PASS`; `REAL_WP_TEST_OPEN`; `NO_RELEASE`; `K0_UNTOUCHED`.
