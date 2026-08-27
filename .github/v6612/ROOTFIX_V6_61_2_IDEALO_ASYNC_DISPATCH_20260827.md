# Affiliate-Zentrale V6.61.2 – idealo Async Dispatch Rootfix

Datum: 27.08.2026

## Live-Ursache
V6.61.1 beseitigte den blockierenden Admin-Aufruf, verließ sich für den tatsächlichen Start des idealo-Vollfeeds aber weiterhin auf WordPress-Cron (`wp_schedule_single_event` / `spawn_cron`). Der produktive Screenshot vom 27.08.2026 14:04 zeigte deshalb dauerhaft `Refresh: queued`: Einreihen PASS, Workerstart nicht erfolgt.

## Rootfix
- Manueller idealo-Start hängt nicht mehr von WordPress-Cron ab.
- Primärtransport ist ein signierter, nicht blockierender Loopback-Worker über `admin-post.php` (`blocking=false`).
- WordPress-Cron bleibt nur als 30-Sekunden-Fallback.
- Bereits aus V6.61.1 auf `queued` hängende Zustände werden beim ersten normalen WordPress-Request selbstheilend neu angestoßen; kein erneuter Benutzerklick nötig.
- Einmal-Worker-Token wird nur als SHA-256-Hash gespeichert und kann nicht wiederverwendet werden.
- Provider-Lock verhindert parallele idealo-Vollfeed-Läufe.
- Recovery-Impulse sind auf 45 Sekunden gedrosselt; keine Dispatch-Schleife.
- `running` ohne aktiven Lock wird erst nach 45 Minuten als abgebrochen betrachtet und sicher neu eingereiht.
- PHP-Fatal im Worker setzt idealo auf `failed`; Last-Good bleibt erhalten.

## Gesamtworkflow-Schutz
Gegen V6.61.1 byteidentisch geblieben: eBay-Provider, eBay-Run, eBay-Account-Deletion, Network-Sync-Grundlogik, Output-Objects, Article-Plans, Provider-Registry/Intake, Automation, Control Contract, Creative Library, Awin-Gate, Frontend CSS/JS sowie Produktionskataloge.

Die fachliche idealo-Logik ist ebenfalls byteidentisch geblieben: Feed-Metadaten, Zugangsspeicherung, Feed-URL-Gate, Streamdownload, GTIN-Normalisierung, 311er-Matcher, Feed-Import, Materialisierung, Hybrid-/Preisvergleichslogik, Multi-Provider-GTIN-Zusammenführung und Remote-Refresh-Verarbeitung.

## Lokale Hard-Gates
- Async-Dispatch positive/negative Matrix PASS.
- V6.61.1 `queued` Self-Heal PASS.
- Retry-Throttling PASS.
- Parallel-Run-Lock PASS.
- Stale-Running-Recovery PASS.
- Article-Mode-Matrix PASS.
- Single-/Multi-Provider-Markup PASS.
- 1000 randomisierte ebay_only-Auswahl-Paritätsfälle PASS.
- 1000 randomisierte eBay-Provider-Cohort-Paritätsfälle PASS.
- idealo/Multi-Provider positive/negative Matrix PASS.
- Materialisierung/Hybrid PASS.
- PHP-Lint 14/14 PASS, auch Fresh-Unpack.
- Fresh-Unpack 19/19 Dateien byteidentisch.

## Feed-/Zielvertrag unverändert
- idealo: Standardfeed 2901.
- Portalvertrag: 311 Produktkonzepte / 59 Hub-Familien.
- Hybrid: idealo eigenständig als Familien-/Preisvergleich; konkretes idealo-Angebot nur als Zusatzbutton bei exakter gemeinsamer GTIN.
- Feed-2901-Evidenz bleibt: 2.041.826 Zeilen, 1.633 konservative Treffer, 83/311 Konzepte, 27/59 Hub-Familien, 3 mehrdeutige Treffer verworfen.
- Providerfehler bleiben isoliert; eBay läuft unabhängig weiter.
