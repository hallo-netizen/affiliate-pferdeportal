# QA82 – KISS Gesamtworkflow: Originalfamilien, echter PHP-Controller, korrekte Abschluss-/Suchfrist

**16.11.2026 – ausschließlich lokal. Keine Freigabe zur WordPress-Installation.**

## A. Gesamtsimulation mit Originalfamilien

Originale Eingaben: der 283er-Katalog, die 278 historischen Fehlfamilien, die Original-Audit-CSV (2.811 / 3.832 / 87 Ereignisse) und die früheren 95 identifizierbaren übersprungenen Artikelkennungen. Die GetItem-, WordPress-DB- und öffentlichen Kampagnendaten wurden **explizit simuliert**, weil diese nicht aus den Original-CSV ableitbar sind.

- Der tatsächlich vorhandene PHP-Gesamtcontroller wurde mit **allen 283 realen Familien-IDs** ausgeführt, davon im Modell **fünf öffentlich gültige Kampagnen** und 278 offene Fächer. Ergebnis **completed nach 12 Arbeitspaketen**, nur ein gezielter Suchlauf, keine Endlosschleife, öffentliche SAFE-Mitgliedschaft gleichbleibend. Dies ist **keine** aktuelle Live-Abdeckungszahl.
- Belastungsfall **0 gültige Angebote / 283 offene Fächer**: derselbe Controller, ebenfalls **completed nach 12 Paketen**, ein Suchlauf. Leere Fächer sind also kein Grund zum endlosen Suchen.
- **Fachlicher Wahrheitscheck mit echten ursprünglichen 278 Fehlfamilien:** ohne vollständigen passenden Auswahlbeleg verweigert die unveränderte PHP-Schlussregel ein scheinbar beweisbares „nicht auf eBay vorhanden“ mit `business_safe_gap_proof_missing`. Erst mit einem ausdrücklich simulierten **vollständigen** Beleg akzeptiert sie diese als `safe_supply_gap_open`. Insbesondere die 215 historisch noch nicht einzeln gesuchten Familien dürfen **nicht** als echte Nullangebote ausgegeben werden. Die historisch 32 angenommenen, nicht veröffentlichten Familien sind ebenfalls keine echten Markt-Nichtverfügbarkeiten.

## B. Neu nachgewiesener QA81-Codefehler und minimale lokale QA82-Korrektur

QA81 aktualisiert `last_sync.finished_at` auch, wenn die öffentliche Freigabe **deferred** wurde: damit wird ein nicht bestätigter Public-Checkpoint wie eine erfolgreich abgeschlossene Veröffentlichung datiert. Bei einem nachfolgenden Refresh kann die zeitliche Trennung verlorengehen. Dies widerspricht dem Zielvertrag „letzter bestätigter öffentlicher Zustand bleibt gültig“ und „ein vollständiger Suchlauf pro Frist“.

**KISS-Quellkorrektur nur in `includes/trait-ppar-ebay-run.php`:**
- In derselben bestehenden `last_sync`-Option steht nun `last_attempt_finished_at` für den beendeten Suchversuch; die bisherige `finished_at` und `last_public_family_result` werden **nur bei vorhandenem gespeicherten bestätigten SAFE-Abschlussmanifest** aktualisiert.
- Die **eine vorhandene** Fälligkeitsentscheidung verwendet den jeweils letzten Suchversuch oder bestätigten Abschluss für das bereits vorgesehene 168h-/7-Tage-Intervall. Dadurch startet nach einem aufgeschobenen Abschluss und nachfolgendem Refresh **nicht sofort wieder ein Vollsuchlauf**; bei abgelaufener Frist ist die erneute normale Suche fällig.
- Keine neue Tabellenstruktur, kein neuer Arbeiter, keine zweite Produktprüfung, keine zweite Publikation, keine neuen Marktplatzanfragen. `trait-ppar-ebay.php` ist **bytegleich** zu QA81.

**Vorher/Nachher-Test:** QA81 **RED**, QA82 **GREEN**: alte öffentliche Prüfbilanz erhalten, altes öffentliches Abschlussdatum erhalten, Suchversuch gespeichert, Refresh löscht nichts, nach 7 Tagen erneut fällig.

## C. Lokale Ausführung / Regression

- **26.967/26.967 Assertions PASS**, überwiegend Originaldatei-Integritätsprüfungen und Modellfälle, **nicht** 26.967 unabhängige echte Produkttests.
- 13/13 Zeit-/Fälligkeitsfälle, 11/11 reine Availability-Controller-Fälle, 8 vollständige Controller-Szenarien inkl. korrekter Fehlerstopps, 16 REST-PHP-Statusfälle, 95 historische Anbieter-IDs mit nachgestellten Antworten.
- Gemeinsamer Test beider echten PHP-Traits: 21 kontrollierte Modellquellen je genau einmal, zwei fortgesetzte kanonische Pakete, gleiche UUID, keine Veränderung am alten SAFE-Checkpoint.
- Beide PHP-Quelltraits syntaktisch gültig. Aus dem frisch **entpackten** QA82-Archiv wurde `bash run_qa82.sh` erneut mit **QA82_ALL_TESTS_PASS** durchlaufen.

Reproduzierbares Archiv (im Gespräch): `QA82_GESAMTABLAUF_ORIGINALDATEN_NUR_LOKAL_KEIN_PLUGIN.zip`, SHA256 `db4e42d3d1f2c84b04cba25784be0e222962f64766e6e317eae7a2a13ebcdc95`. Einzige quellcodewirksame Änderung gegenüber QA81 ist die vorhandene PHP-Run-Datei (im Archiv `QA81_to_QA82_RUN.patch`).

**Gesamtstatus:** QA69 Live-Abnahme NICHT bestanden. Die aktuellen WordPress-Quell-/Creative-/Checkpoint-/Seitenzuordnungen und echten eBay-Anbieterantworten fehlen weiterhin. Keine Live-Datei geändert, kein Neustart, GitHub-Sicherheitssperre unberührt.