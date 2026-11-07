# PSTE-KISS – Quellcode- und Laufbeweis (07.11.2026)

**Wichtig: Dies ist ein lokaler Nachweis am echten PSTE-PHP-Code, kein 1:1-Test deiner produktiven WordPress-Installation.** Keine neue ZIP wird freigegeben.

## 1. Reproduzierbare Ursache in 0.57.144.18

Aufrufkette im Original-Plugin:

1. `PSTE_Mini_Workflow::approvedRelevanceFor` in `includes/class-pste-mini-workflow.php` Zeile 108 liefert das richtige, an die Originalsuchfrage gebundene JA.
2. `PSTE_Admin::processOneTitleDeskReentry` in `includes/class-pste-admin.php` Zeile 2135 startet den bestehenden Themenprüfer.
3. `PSTE_Repository::reanalyzeRetainedBacklogBatch` in `includes/class-pste-repository.php` Zeilen 2998–3040 führt die **erste** Relevanz-/Titelbewertung mit JA-Beleg aus. Der Bestands-/Dublettenprüfer folgt in Zeile 3117.
4. Dieselbe Repository-Methode stößt in Zeile 3191 die gezielte Kontext-Aktualisierung an.
5. `PSTE_Repository::refreshPortalContextForRow` in derselben Datei Zeile 3479 startet *erneut* `prepareEditorialPayload`, das in Zeile 1854 `applyToPayload` **ohne JA-Beleg** aufruft. In Zeile 3515 wird bei NORMAL_PASS außerdem nochmals der Planungsprüfer aufgerufen.

**Das ist der doppelte Prüfpfad.** Es handelt sich um zwei Funktionsaufrufe im bestehenden Ablauf – nicht um ein WordPress-Verlangen.

## 2. Nachweis mit 100 realen MINI-Ergebnissen und WordPress-Ersatzfunktionen

Die nicht produktive Probe verwendet die originalen 100 MINI-Entscheidungen und die mitgelieferte Portal-Kategorieliste mit 1.165 Einträgen (die numerischen WordPress-Kategorie-IDs sind *simuliert*).

| Prüfung | Originalversion 0.57.144.18 | Bereinigte QA-Arbeitsfassung |
|---|---:|---:|
| Akzeptierte JA-Quellen als Testbasis | 87/87 | 87/87 |
| Beim nachfolgenden Kontext-Schritt auf UNPROVEN zurückgesetzt | **7/87** | **0/87** |
| Davon NORMAL_PASS vor Kontext-Aktualisierung | 24 | 24 |
| Zusätzliche Bestandsabrufe in gezielter Kontext-Aktualisierung | **20** | **0** |
| Absichtlich eingebaute exakte WordPress-SEO-Dubletten schon bei erster Bestandsprüfung geblockt | – | **24/24** |
| Diese Dublettensperren nach der Kontext-Aktualisierung erhalten | – | **24/24** |
| Eigenständige vollständige Kontext-Aktualisierung (Bestand kann sich geändert haben) führt die nötige Bestandsprüfung aus | – | **24** |
| JA mit verfälschter Suchfrage zu Recht abgelehnt | – | **87/87** |
| NEIN/VIELLEICHT zu Recht nicht als JA übernommen | – | **13/13** |

**Negative Kontrollen:** Alle 7 bekannten Relevanzfälle reproduzieren den Fehler im Originalcode; in QA bleibt bei allen 7 die Relevanz nach der Kontext-Aktualisierung bestehen. 24 Dubletten werden auch ohne zweite Prüfung nicht freigegeben. Kein Titel verändert. 83 PHP-Dateien ohne Syntaxfehler.

## 3. Vereinfachung (noch KEIN Plugin)

Nur **eine vorhandene Datei** wird in der isolierten QA-Kopie geändert: `includes/class-pste-repository.php`.

- Die Kontext-Aktualisierung startet die bereits abgeschlossene Relevanz-/Titelbewertung nicht mehr neu.
- Für einen gezielten Stapellauf wird die gerade vorgenommene Planungsprüfung nicht wiederholt.
- Ein unabhängiger vollständiger Kontext-Neuaufbau oder ein fehlendes Planungsergebnis darf weiterhin eine notwendige Bestandsprüfung auslösen.
- Keine neue Datenbanktabelle, neuer Worker, neue Sperre oder Änderung an K0/PSERC.

Gegenstand der QA-Änderung: `15344794337def5392b7dd06c1516a6680f0ba2f32ce19477b20076069eb0554` (Original-Quelldatei) → `3a6282a524e36136da301b2cc2603ba046f17c889e8dc318c317c284923e90fe` (QA-Quelldatei). Vollständige Änderung steht in `PSTE_MINI_KISS_QA_PATCH_20261107.diff`.

## 4. Was NICHT bewiesen ist

**Ein realer WordPress-1:1-Test ist nicht durchgeführt.** Es fehlen ein isolierter Klon der konkreten WordPress-Installation und eine Kopie ihrer aktuellen Datenbank (inkl. gespeicherter MINI-Entscheidungen, Themenpool, WordPress-Beiträgen/Kategorien sowie laufendem Kontextindex). Daher sind tatsächliche Datenbank-Speicherung, WP-Cron, Plugin-Zusammenspiel und sämtliche alten historischen Datensätze **nicht** unter Live-Bedingungen bestätigt.

**Auch die Aussage „im gesamten Plugin gibt es keinerlei überflüssige Doppelprüfungen mehr“ wäre nicht bewiesen.** Andere bewusst getrennte Routinen (Migration, Reparatur, vollständiger Kontext-Neuaufbau, normale Neu-Recherche) besitzen eigene Prüfpunkte. In der **konkret untersuchten MINI-Wiederaufnahme** wurden zwei unmittelbar aufeinanderfolgende doppelte Bewertungen entfernt; die Folgeprobe zeigt den Effekt. Eine vollständige Laufzeitinventur aller Betriebsarten mit echten WordPress-Daten steht aus.

**Freigabe:** BLOCKED – **KEINE neue Installer-ZIP**. Ein belastbarer 1:1-Beweis erfordert die echte WordPress-Testumgebung mit entsprechendem Datenspiegel. Bis dahin keine Aussage „alles 1:1 simuliert“ und keine Aufforderung zur Installation.