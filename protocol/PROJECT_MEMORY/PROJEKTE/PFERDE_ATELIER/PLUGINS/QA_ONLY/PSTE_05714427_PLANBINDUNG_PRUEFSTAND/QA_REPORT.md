# PSTE 0.57.144.27 – vollständiger lokaler Ketten-Replay, QA/Testseite, 09.11.2026

## Entscheidender Stand
**KEIN positiver Gesamtworkflow-Abnahmelauf.** Der Betreiber-Screenshot und der reale Bericht beweisen: 60 der 61 FREI-Themen scheiterten an `PSTE_RETAINED_EDITORIAL_PLAN_SNAPSHOT_CHANGED`, das verbleibende Thema am bestehenden manuellen Review. Die fehlerhafte Warteschlange .26 markierte alle 61 als erledigt, ohne die weiteren 60 fachlich neu zu prüfen.

## Getestete Originalkette
- Tatsächlicher PSTE-.26-Quellcode als Ausgangspunkt; originale 1.179-Quellen-Snapshotdaten, 87 SEO-Entscheidungen (61 FREI / 20 BELEGT / 6 KLÄRUNG), originaler 61er-WP-Stapelbericht.
- Ausführung der originalen PHP-Methoden: Import-Annahme der 87 externen Eigentümerentscheide, 61er Planpreflight, Titel-Speicherung und zweiter idempotenter Titel-Durchlauf, Reentry-Warteschlange, echte Hash-Sperre des Planstands.
- Mit kontrolliert veraltetem Planhash reproduzierbarer globaler Fehler. .27-Patch lässt nun bei unveränderter Hash-Sperre 0 fachlich fertig, 61 ausstehend und hält den Wiederanlauf an, statt 61 terminale Fehlentscheidungen zu erzeugen. Schon gespeicherte alte .26-Abschlüsse werden nicht stillschweigend überschrieben.
- Zusätzlich: Ein einziger nonce-geschützter, administrativer Nur-Lese-Export aus der **echten WP-Testseite**: gespeicherter Baseline-Kategoriebaum, aktuell berechneter Kategoriebaum, aktuell berechneter WP-Plan samt Quellenherkunft, Inventar, Kontext/Manifest, Typen- und Inventar-Stage, Status/Schlüssel der Reentry-Warteschlange. Fehler einzelner Quellen erscheinen als Fehler, nicht als fiktiver Ersatz.
- Geringfügige reine Anzeigeberichtigung: Roh-Keyword-Fallback im 61er-Stapelbericht.

## Testbelege
- Originaler v26-Replay: 19/19 lokaler Nachweis PASS (auch gemessene Reproduktion eines falschen Abschlusses).
- Aus v27-ZIP extrahierter Testlauf: **32/32** messbare lokale Prüfungen PASS. Darunter 11 neue Export-/Lese-/Negativprüfungen mit identischen WordPress-Dateien und künstlichen Normal-/Fehler-Optionszuständen.
- 83/83 PHP-Syntaxprüfungen PASS; 121/121 ZIP-Dateien CRC PASS; frische Entpackung erneut syntaktisch geprüft.
- Genau drei PHP-Dateien geändert: `portal-seo-topic-engine.php` (Version), `includes/class-pste-admin.php` (Pause/Anzeige), `includes/class-pste-mini-workflow.php` (nur lesender Nachweisreport und sichtbarer Download bei alten/stalen Läufen).
- 118 andere ZIP-Dateien gegenüber originaler .26 bytegleich; kein neues Schema, keine WordPress-Beiträge, Kategorien oder K0-Schreibvorgänge. Unveränderter PSERC 0.28.55.
- Vollständiges privates Beweisarchiv enthält Quellfassungen, Originaldaten, Testprogramm, SHA256-Liste, Testlog und Diff. Unabhängig in leerem Ordner entpackt, `sha256sum -c CHECKSUMS.sha256` und `PSTE_TEST_PATCHED=1 php tests/run_v27_real_methods.php` erfolgreich wiederholt.

## Unüberwindbare aktuelle Testgrenze
Die originalen 61er Daten enthalten **keinen** vollständigen aktuellen WordPress-Baseline-Kategoriebaum, keine aktuelle plan/context-bound Hash-Paarung, keine echte Registry-Stage. Nach synthetisch übereinstimmendem Planhash tritt im Test deshalb `PSTE_ARTICLE_TYPE_REGISTRY_EMPTY` auf. Dieses Ergebnis ist die Grenze der vorhandenen Daten, nicht der Nachweis, dass WordPress alle Artikeltypen fehlen. Der echte vollständige MySQL-/WP-Lauf bis zu fachlicher Kategoriezuordnung, PSERC und K0 wurde NICHT bestanden oder durchlaufen. Kein Code umgeht diese Schutzprüfungen.

## Weiter
PSTE 0.57.144.27 ist **NUR TEST**, nicht Produktion. Einmal auf isolierter WordPress-Testseite statt .26 installieren; in **SEO Themenengine → Themenprüfung → Externe SEO-Prüfung** die sichtbare Schaltfläche **„Einmaligen Plan- und Kategorien-Prüfstand herunterladen“** verwenden (auch in „Weitere Werkzeuge“). Die resultierende JSON-Datei erlaubt dann die lokal nachweisbare Prüfung mit echten gebundenen Kategorien und Planoptionen, ohne Keyword-/SEO-Neustart. Erst nach vollständiger Kette Freigabe einer produktiven Version. Main, K0, PSERC und ursprüngliche Reservierungen nicht ändern; Draft PR #682 nicht mergen.