# QA28 KISS – Pferde Atelier Affiliate 6.72.333 (12.11.2026)

**Status: vollständiges lokal geprüftes Plugin, noch NICHT live abgenommen.** Vollständige Original-ZIP 6.72.331 („Anzeige pass“) als unveränderte Ausgangsbasis. Der vorherige verwerfene QA27-Test 6.72.332 wurde nicht übernommen und der von ihm vorgeschlagene WordPress-Rettungs-Cron nicht installiert.

## Warum der bestehende eBay-Lauf immer wieder stoppte

Im Code haben GitHub und WordPress denselben kanonischen eBay-Lauf **beide angestoßen**: GitHub rief `handle_ebay_external_tick()` auf, dieser führte genau einen kanonischen Worker aus und startete dann einen weiteren asynchronen Self-Drive-Aufruf über `admin-post.php`. Auch Admin-Start/-Pause/-Fortsetzung lösten diese zweite, unbestätigte Kette aus. Zusätzlich rief derselbe externe Handler die **unabhängige** eBay-Verfügbarkeitsprüfung auf; deren Rückgabe `idle` konnte GitHub trotz `run_status=running` fälschlich als Ende der Recherche auswerten. Dieser Unterfall ist durch die echte WordPress-/GitHub-Auditkorrelation am 11.11. belegt. GitHub-Cron-Läufe waren außerdem unregelmäßig; das ist eine **eigene, weiterhin nicht behobene** Frage der Zuverlässigkeit des externen Weckers.

## Umgesetzt: direkt an den Originalstellen, ohne Überbau

- **Ein ausführender Eingang:** Bestehender `POST /wp-json/affiliate-zentrale/v1/ebay/tick` führt für Recherche/Refresh höchstens **ein kanonisches Worker-Paket** aus. Der GitHub-Workflow ist nur ein externer Aufrufer.
- **Doppelte WordPress-Selbstkette komplett entfernt:** Self-Drive-HMAC-Signaturen, der eigene nopriv/admin-post-Endpoint und sämtliche Dispatch-Aufrufer wurden gelöscht, nicht ersetzt. Kein neuer Cron, keine Queue, kein zusätzlicher Worker.
- **Eine einzige Statusentscheidung:** Der gespeicherte kanonische eBay-Lauf ist maßgeblich. Bei laufendem/automatisch pausiertem Lauf darf nicht mehr `idle` als Endmeldung zurückgegeben werden. `local_checked` wird korrekt in das vom bestehenden GitHub-Vertrag unterstützte `completed` übersetzt. Manueller Stop bleibt `idle`, echter Fehler `failed`.
- **Verfügbarkeit eigenständig:** Nur bestehender `EBAY_REFRESH_CRON_HOOK` in WordPress ruft `ebay_public_availability_tick` auf. Der Recherche-Tick ruft diese Funktion **nicht mehr** auf und kann nicht von ihr gestoppt werden. Dies ist **eine getrennte Fachfunktion**. Achtung: WordPress-Cron hängt ohne System-Cron von WordPress-Anfragen ab; zuverlässiger Verfügbarkeitsstart auf IONOS ist noch **nicht** bewiesen.
- **Bestand gewahrt:** Derselbe gespeicherte Run, Cursor, Lease, öffentliche Checkpoints und Freigaben; alte gespeicherte `orchestrator_contract=self_drive_v1`-Metadaten bleiben aus Rückwärtskompatibilität erhalten, während der echte Transport künftig `external_tick` heißt. Kein eBay-Neustart/Neuimport; Amazon-ASIN/idealo-Import/Frontend-/Katalogregeln unverändert.
- **Andere Anbieter und Wege geprüft:** Im vollständigen eBay-Orchestrator keine direkten Referenzen auf Amazon/idealo; nur ein aktiver eBay-Recherche-Ausführungseingang. Der Amazon-Regressionstest auf unveränderten echten ASIN-Gegenfällen bleibt grün. Der unabhängige eBay-Datenlösch-Compliance-Prozess bleibt aus rechtlichen Gründen unangetastet; der Verfügbarkeits-Cron ist nicht der kanonische Rechercheworker.

## Exakte lokale Prüfergebnisse

- 70/70 Proben mit **originalem** PHP-Trait `PPAR_Ebay_Run_Trait` und simulierten WordPress-/Worker-/Speicher-Rückgaben erfolgreich, einschließlich Leerlauf bei laufendem Lauf, Zeitpause, manuellem Stopp, Ende, Fehler, Drosselung, Stale-Recovery, nur einer Worker-Ausführung
- 13/13 Abgleichproben zum vorhandenen GitHub-Statusvertrag PASS
- 41/41 originaler Amazon-idealo-Regressionstest PASS, inkl. 7 echter Diagnose-ASIN-Fälle
- 10 eBay-Klassifikatorprüfungen unverändert; PHP-Lint 23/23 PASS; ZIP-Test 66/66 Einträge PASS
- **4 von 66 Plugin-Dateien geändert:** `includes/trait-ppar-ebay-run.php`, `includes/trait-ppar-ebay.php`, `pferdeportal-affiliate-router.php`, `readme.txt`
- Vollständige ZIP in persönlicher Library `/pferdeatelier/PLUGINS/QA/Pferdeatelier_Affiliate_6.72.333_KISS_EINE_EBAY_STEUERUNG_GESAMT.zip`; SHA256 `9a0df676e2b3aeeb3ddd309f9615ac55952797b1580cb4b7cb867d0baa45a393`. Diff, originale PHP-Testdatei, Prüf- und Hash-Protokolle ebenfalls dort.

## Freigabegrenzen und nächste notwendige reale Abnahme

**Noch kein** echter unbeaufsichtigter kompletter WordPress/eBay/DB-Durchlauf und kein Beweis, dass GitHub-**Zeitpläne** regelmäßig starten. Das Paket beseitigt den Code-Ursachenfehler der doppelten Workerausführung und des falsch terminalen WordPress-Status, aber nicht eine eventuelle Verspätung des äußeren GitHub-Weckers. Die bestehende GitHub-Heartbeat-Zeitsteuerung bleibt aktuell **eine** eingerichtete Taktquelle; einen IONOS-Cron nur **anstelle** davon verwenden, wenn ein echter POST-Aufruf unterstützt/getestet ist. Keine parallelen GitHub/IONOS-Takte.

Nach einmaliger Installation: existierende gespeicherte Run-ID/Cursor/Freigaben vorher/nachher abgleichen, nur bestehende Recherche weiterlaufen lassen, echten Fortschritt und eBay-Frontend-Freigabe nachweisen, anderen Anbieter nicht verändern. Der Status `running` allein ist **kein** End-to-End-Beweis. Sicherungen/Main-Hardlock/K0 bleiben unberührt.
