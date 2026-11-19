# Pferdeatelier eBay – QA16-WORK: unabhängige Verfügbarkeit im gemeinsamen Heartbeat

Stand 11.11.2026. **Nur Quell-Arbeitsfassung auf Basis von QA15 6.72.326; keine neue Plugin-ZIP, keine Installation, keine Live-Freigabe.** Die zuletzt festgelegte Reihenfolge bleibt: zuerst echte Ausspielung/Verfügbarkeit, Serverlast zuletzt.

## Vorheriger, konkreter Regelwiderspruch

Im echten QA15-Plugin-Quellcode `includes/trait-ppar-ebay-run.php::handle_ebay_external_tick` wird `ebay_public_availability_tick('heartbeat')` **nur** in den Zweigen für vom Benutzer pausierte oder fehlgeschlagene Recherche aufgerufen. In `running` und beim Leerlauf/Abschluss wird ausschließlich die kanonische Recherche- oder Refresh-Arbeit ausgeführt, bzw. sofort `idle` zurückgegeben. Die Verfügbarkeit wurde in diesen Zuständen nur vom getrennten **WordPress-Cron** angestoßen. Dadurch war die Anforderung „Verfügbarkeit unabhängig von Recherche und nicht von Browser/WP-Cron abhängig“ nicht vollständig erfüllt.

Die öffentliche Produktfreigabe prüft separat `source_state`, `policy_state`, `route_state`, tatsächlich gespeicherte Quellen, `fresh_until > now`, eventuelle Endzeit und den vorhandenen öffentlichen Checkpoint (`ebay_business_campaign_source_allows_delivery[_base]`). Selbst zuvor gespeicherte Angebote können damit nach Ablauf ihrer Quelle korrekt aus der Ausgabe verschwinden. Dass ausgerechnet dieser Grund für die auf der öffentlich abgerufenen `/ausruestung/ausruestung-sattel/schabracken/`-Seite derzeit fehlenden Kacheln verantwortlich ist, **kann ohne aktuelle WordPress-Quellzeilen nicht belegt werden**. Die externe Webansicht zeigte Produktvorschläge, aber keinen sichtbaren eBay-Produkttreffer; ihr eigener Abrufzeitpunkt ist nicht identisch mit einer Echtzeit-DB-Messung.

## Einzige Quelländerung

Die bereits vorhandene `ebay_public_availability_tick('heartbeat')` wird **einmal nach dem bestehenden Recovery-Sicherheitsgate** im zugelassenen Heartbeat aufgerufen, unabhängig davon, ob der Recherchelauf `running`, `paused`, `failed`, `completed` oder noch nicht begonnen ist. Die beiden bisherigen redundanten Aufrufstellen werden entfernt.

- Derselbe vorhandene Taktgeber und dieselbe Availability-Funktion, **kein zweiter Worker/keine zusätzliche Cron-Engine/keine Tabelle**.
- Bestehender Fälligkeits-/90-Sekunden-Bündelmechanismus, Transient-Sperre, höchstens **2 eBay-getItem-Prüfungen pro Heartbeat**, getrennte Verfügbarkeitshistorie und Quell-/Checkpoint-Gates bleiben identisch.
- Ungültige Recovery-Nachricht oder deaktivierter Anbieter führen weiterhin **zu keiner** Availability-Verarbeitung.
- Gespeicherte Angebote, Run-UUID, Suchcursor, Freigaben, eBay_DE-Filter, 6-Stunden-Frische, alte Logs und Einstellungen werden nicht verändert.
- Die vorhandene WordPress-Cron-Verfügbarkeitsprüfung bleibt als optionaler weiterer Aufrufweg erhalten; nicht als erforderlicher einziger Antrieb.

## Testnachweise – Vorher und Nachher am Original-PHP-Entry-Point

`QA16_HEARTBEAT_SEPARATION_REAL_PHP_TEST.php` bindet das echte Trait mit echten `handle_ebay_external_tick`-Methodenkörper ein. WordPress-Settings/DB, eBay-HTTP, Produktdaten und Worker-Antwort sind **nachgestellt**:

| Status im zugelassenen Heartbeat | QA15: Availability-Aufrufe | QA16-WORK: Availability-Aufrufe |
|---|---:|---:|
| Recherche läuft | 0 – fehlerhaft | 1 |
| Benutzer hat Recherche angehalten | 1 | 1 |
| Recherche gescheitert | 1 | 1 |
| Recherche abgeschlossen | 0 – fehlerhaft | 1 |
| Noch kein Lauf | 0 – fehlerhaft | 1 |
| Veraltetes Recovery-Signal | 0 – korrekt blockiert | 0 |
| Provider deaktiviert | 0 – korrekt blockiert | 0 |

**Baseline: 3 von 7 fehlerhaft. Neuer Code: 7 von 7 PASS.** Die bestehenden **17/17 QA15-Regressionstests** wurden zusätzlich gegen den geänderten Quellbaum ausgeführt und bestanden. `php -l` des geänderten Traits bestanden. Es wurde **nur eine** PHP-Datei in der getrennten Arbeitskopie geändert.

## Grenzen, verbindlich vor Ende

**NICHT** als echte Reparatur der leeren Schabracken-Seite oder der Live-Verfügbarkeitsprüfung ausgeben: Kein authentifizierter WordPress-/MariaDB-/eBay-Echtlauf, keine aktuelle Datenbankabfrage der dortigen Kampagnen, keine gemessenen Backend-/Frontend-Zeiten. Es bleibt eine nachvollziehbare Quellkorrektur in der gemeinsamen Abschluss-Arbeitsfassung, **keine neue ZIP zum Installieren**.

Nächster beweisender Schritt im abschließenden, gebündelten WordPress-Praxistest: bisherige sichere Freigaben, tatsächlicher Quell-Frischezeitpunkt und letztes getItem, öffentlicher Checkpoint, Kategorie- und Beitragskarte sowie Availability-Heartbeat bei laufendem UND pausiertem Suchlauf. Erst danach Performance optimieren. **K0, Hobbydepot und Hab & Bewahr nicht ändern.**