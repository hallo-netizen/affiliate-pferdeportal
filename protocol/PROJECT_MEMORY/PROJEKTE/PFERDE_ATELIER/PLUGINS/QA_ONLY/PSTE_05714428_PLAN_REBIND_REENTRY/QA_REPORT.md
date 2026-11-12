# PSTE 0.57.144.28 – QA-Prüfbericht (nur isolierte WordPress-TESTseite)

Datum: 09.11.2026, lokale Tests, keine WordPress-/MySQL-Produktionsfreigabe.

## 1. Originaldaten

- Originaler WordPress-TEST-Export aus PSTE 0.57.144.27: `pste-plan-kategorien-pruefstand-2026-11-09.json`, 11.925.212 Byte, generiert 12:22:45 UTC.
- 163 vorhandene WordPress-Artikel (144 veröffentlicht, 19 Entwürfe), 1.176 Kategorien davon 1.165 gültige Produktions-Endkategorien, 267 Themenfamilien, 11 Artikeltypen. Die eine zusätzliche ungeklärte Kategorie wird nicht übernommen.
- Baseline vom 26.10.2026: Inventar- und Strukturprüfsummen stimmen mit den aktuellen Quellen überein; alter Editorial-Plan-Hash stimmt nicht mit dem aktuell semantisch leeren Plan überein.
- Gespeicherte Rohquelle des Editorial-Plans: exakt 9 alte identitätslose `Array`-Platzhalter, keine echten belegten Planartikel. Der echte `PSTE_Snapshot`-Code erkennt die Herkunft `OPTION`, keine zusätzlichen/ungeklärten Inhalte, aktuellen Plan `NOT_AVAILABLE`.
- 87 ursprüngliche einmalige externe SEO-Urteile: 61 FREI, 20 BELEGT, 6 KLÄRUNG. Der ursprüngliche Parkhaus-Export enthält 1.179 Quellreferenzen einschließlich 144 reservierten PPM-Artikelslots. Titel und Schlüssel der 61 FREI wurden gegen die Original-SEO-Datei geprüft.
- Originaler echter 61er-WP-Stapelbericht: 60 technische Abbrüche `PSTE_RETAINED_EDITORIAL_PLAN_SNAPSHOT_CHANGED`, 1 manuelle Sperre. Alte Zählungen sind keine neuen fachlichen Ergebnisse.

## 2. Ursache und Änderungen

Die normale Planung band den Kontext noch an den alten SHA des leeren 9er-Altplans. Wenn alle neun Alt-Datensätze nachweislich inhaltslos sind, liefert der aktuelle Original-Planleser bewusst `NOT_AVAILABLE`. Dadurch kommt es zu einer dauerhaften Hash-Sperre. Der Kontext-Staging-Code hatte `NOT_AVAILABLE` bislang fälschlich wie einen kaputten SHA behandelt.

Die QA-Testversion **0.57.144.28** ergänzt eine **explizite einmalige, nonce-geschützte und eng begrenzte Aktion**:

1. Prüft den echten Mini-SEO-Import, die 61 unveränderten IDs/Titel/Belege, die 60 alten technischen + 1 manuellen Rückstellungsgründe, die 9 leeren Alt-Planzeilen und die unveränderten Originalquellen.
2. Erlaubt `NOT_AVAILABLE` als Kontext-Planwert **nur** beim exakt leeren Plan-Datensatz aus vier Feldern; alle anderen Hashprüfungen bleiben strikt.
3. Führt den **bestehenden** sicheren Baseline-Abgleich mit dem Original-PSTE_Snapshot-Code aus, baut den bestehenden Kontextindex aus Original-WordPress-Inventar und -Kategorien neu auf und prüft den Rücklesestand.
4. Legt die **gleichen 61 Themen** erneut in die bestehende Titel-Warteschlange. Keine nochmalige externe SEO-Entscheidung, keine WordPress-Beitrags- oder Kategorieänderung, kein PSERC-/K0-Freigabeaufruf. Ein alter manueller Halt wird beim Wiederanlauf nicht automatisch fachlich zu PASS.

Nur **3 geänderte PHP-Dateien** gegenüber der originalen .27-ZIP: Hauptversionsdatei, bestehender Mini-Workflow und bestehender Kontextindex. **118 weitere Archivdateien bytegleich**.

## 3. Nachweise – keine Placebo-Tests

| Umfang | Ergebnis | Beleg |
|---|---|---|
| Originale WP-Daten, 61 IDs, externe SEO-Bindung, Kategorie-/Plan-Gates und negative Änderungen | **51/51 PASS** | `test_v28_real_snapshot.php`, `V28_REAL_SNAPSHOT_QA_RESULTS.json` |
| ORIGINALER PSTE_Snapshot: exakte neun alte Datensätze, realer Planstatus, nur Plan-Drift, Original-Baseline-Rebase, idempotenter Wiederholungsschutz | **PASS** | `test_v28_original_snapshot_rebase.php`, `V28_ORIGINAL_SNAPSHOT_REBASE_QA_RESULTS.json` |
| ORIGINALER PSTE_Article_Type_Registry::build aus 1.165 Blattkategorien | **11 Typen / 267 Familien / 1.165 Zuordnungen / identischer Registry-SHA** | Dasselbe Skript |
| ECHTER `commitLegacyEmptyPlanRebind` mit WordPress-Optionen **lokal nachgebildet**, vollständige Kontext-Neuerstellung, Warteschlangen-Schreiber und WP-Cron-Einplanung | **12/12 PASS** | `test_v28_commit_queue_integration.php`, `V28_COMMIT_QUEUE_QA_RESULTS.json` |
| Plugin-ZIP | **83/83 PHP-Syntax; 121/121 ZIP-CRC; 3 geänderte, 118 unveränderte Dateien** | `V28_BINARY_QA_RESULTS.json` |

Das **reproduzierbare Beweispaket** enthält die Originaldaten, PHP-Testskripte, vollständigen getesteten Plugin-Code und Ergebnisse. `./run_checks.sh` muss in einem neu entpackten, frischen Ordner dieselben Ergebnisse liefern. Das alte Manifest und der reale damalige WordPress-Optionsdatensatz der 61er-Warteschlange wurden vom Export nicht komplett übertragen: Die lokalen Tests rekonstruieren diese **ausdrücklich als QA-Attrappe** anhand der originalen Einträge. Keine unzutreffende Behauptung eines realen WP/MySQL-Laufs.

## 4. Offene Grenze / nächster echter Test

**FULL_WORKFLOW_PASSED = false.** Die tatsächliche WordPress-Datenbank und die echte Kategorieneuentscheidung der 61 Themen nach dem Wiederanlauf sind lokal nicht als durchlaufener WP-MySQL-Prozess belegt. Ebenso keine echte PSERC-/K0-Artikelübergabe. Ein erfolgreicher QA-Wiederanlauf ist keine fachliche 61er-Freigabe.

**Nächste Aktion nur auf der isolierten WordPress-TESTseite:** Plugin .28 installieren, `SEO Themenengine → Themenprüfung → Externe SEO-Prüfung → Nur nach geprüftem Bericht: alte Planbindung erneuern und MINI-Themen sicher erneut prüfen` **einmal** auslösen. Anschließend **keine weitere Übergabe**, sondern unter `Themenprüfung → Weitere Werkzeuge (nur für Sonderfälle) → Nur aktuellen Stapelbericht herunterladen` den aktuellen Bericht ausgeben und prüfen. Bei Fehlermeldung STOP und konkrete Meldung erfassen, nicht erneut klicken. K0, Live und PSERC .55 bleiben unangetastet. PR #682 bleibt DRAFT.

## 5. Offene technische Grenzen und Sicherung

- In einem echten MySQL-/WordPress-Ausfall zwischen Baseline-Schreibvorgang und Warteschlangen-Planung kann eine manuelle Einzelfehlerdiagnose nötig sein. Der QA-Prozess erfindet keinen Plan-HASH und erzwingt keine Freigabe. Daher Testseite und **keine automatische Liveinstallation**.
- Die realen Kategoriekandidaten und Plan-Gates können nach dem sicheren Wiederanlauf weitere fachliche Rückstellungen liefern; diese dürfen nicht durch fingierte Kategorien/SEO-Urteile wegoptimiert werden.
- Exakt 9 alt-platzhalterhafte `Array`-Einträge bleiben physisch erhalten, werden aber als nicht belegte Planartikel bewertet. Alle 144 PPM-Planplätze und WordPress-Kategorien bleiben unverändert.