# QA62 – eBay-Status nur einmal aus dem gespeicherten Lauf entscheiden

**Datum:** 14.11.2026  | **Plugin:** 6.72.345  | **Umfang:** kompletter WordPress-Plugin-ZIP als QA-Artefakt, nicht live installiert.

## Ausgangslage / echter Beleg

Original-Live-Screenshot 14.11.2026 08:54: eBay-Lauf `97507628-4f4...` weiterhin `running` und `gapfill_discovery/complete`, nach 469 Workeraufrufen 5/283 Familien abgedeckt. Original-GitHub-Job 132368416061 antwortete am 14.11.2026 07:16:59 UTC mit `idle` nach zuvor 15 tatsächlichen `advanced`-Aufrufen und beendete die Selbstverkettung. Die WordPress-REST-Rohantwort und die tatsächliche installierte ZIP sind nicht bekannt. Der Nachweis erklärt deshalb den Stop des Zeitgebers, **nicht** die konkrete WordPress-Ursache von `idle`.

## Was geändert wurde

Original vollständig entpackte Testversion 6.72.344 benutzt, NICHT den alten Github-CURRENT-Plugincode. Vollständig erhalten: 66 Dateien, 64 unverändert, nur zwei Änderungen:

1. `includes/trait-ppar-ebay-run.php`: `ebay_external_tick_saved_run_state()` wertet den **vorhandenen zentralen aktiven Lauf-Prädikat** `ebay_run_is_active()` aus und ordnet den gespeicherten Zustand einmal zu: aktiv, manuell pausiert, abgeschlossen, fehlgeschlagen, leer oder widersprüchlich. Ein noch aktiver Lauf darf nicht als `idle` oder abgeschlossen ausgegeben werden. Bei widersprüchlichem Zustand **keinen neuen Lauf schreiben, keinen Cursor oder Produktbestand löschen**; stattdessen klarer harter Fehler. Eine Worker-Aussage „fertig/fehlgeschlagen“ ohne gespeicherten Endzustand wird nicht fälschlich als `busy` beschönigt. In REST-Antworten sind tatsächlicher gespeicherter Laufstatus, Phase und Pluginversion auch bei `idle` dokumentiert.
2. `pferdeportal-affiliate-router.php`: Nur die beiden Versionsangaben 6.72.344 -> 6.72.345, keine anderen Änderungen.

**Keine Änderungen an:** GitHub-Workflows, WP-Cron, Zweit-Worker, eBay-Suchprofilen, Produkt-/Familienentscheidung, Produktwahl, Kategorien, öffentlichen Kacheln, SAFE-Freigabedaten, anderen Affiliate-Partnern oder dem Frontend. Die sechs Stunden Frische-Prüfung aus QA58 bleibt unverändert.

## Tatsächlich ausgeführte Prüfungen

- Ausführung des **unveränderten echten Lauf-Traits** mit simuliertem WordPress-Speicher und einmaligem Worker-Return: **16/16 PASS**. Testfälle u.a. normaler Fortschritt, irrtümliches `idle`, falsch gemeldetes Worker-Ende, fehlend gespeicherter Fehler, ungültiges Schema, widersprüchlicher Status/Phase, echte manuelle Pause, automatische Pause, gespeicherter Fehler, wirklicher Abschluss, geplanter neuer Lauf nach echtem Abschluss, leere Daten und Dateistandsrückfall. In **jeder Testfall-Simulation bleibt der bisherige öffentliche SAFE-Checkpoint unverändert.** Kein neuer Lauf, wenn alter noch aktiv oder inkonsistent ist.
- Roter Vergleich gegen Original 6.72.344: Bei ungültigem gespeicherten Schema, widersprüchlicher Laufphase und ungültigem Laufstatus löste die alte Methode testweise **1 neuen Lauf** aus; 6.72.345 verhindert dies bei identischen Eingangsdaten. Bei falsch gemeldetem ungespeichertem Abschluss/Fehler gab die alte Methode `busy` zurück, neue Version erklärt den Konflikt eindeutig.
- QA58 Original-Trait für ausgewählte Frische nach eBay-Kandidaten: **9/9 PASS**, einschließlich simulierten 153 ausgewählten/abgelaufenen Artikeln. Keine echten Live-eBay-Anfragen in der QA-Simulation.
- Original-QA50 PHP-Gesamtphasenmodell: sieben Varianten `normal`, `no_new`, `old_blocked`, `new_blocked`, `db_down`, `churn`, `save_fail`. Die echten modellierten Vorfälle schließen korrekt ab oder scheitern eindeutig, **ohne unbegründete Verluste alter Modellfreigaben** (in `old_blocked`/`churn` genau eine nachweislich gesperrte Freigabe entfernt). Das sind Modellprüfungen, keine echte öffentliche Familienabdeckung.
- **23/23 PHP-Dateien** Syntaxprüfung bestanden, auf den ausgepackten bytes der *fertigen neuen ZIP* nochmals geprüft. **66/66 ZIP-Einträge** vollständig und CRC gültig, der Bytevergleich mit der Vorlage bestätigt exakt zwei modifizierte Dateien und 64 identische.
- Neue ZIP SHA256: `e1746fc394f7bdb19520758db8eb250bb32a796172fa66e960003385f1877a44` (5.391.166 Byte).

## Grenzen und verbindlicher nächster Schritt

**Nicht bestätigt:** Live installierte Version, WordPress-/eBay-Live-Durchlauf, regelmäßige tatsächliche GitHub-Schedule-Takte, echte Abdeckung 283 Produktfamilien, 578 reale Freigaben. Auch die vorangehende Version 6.72.344 war lediglich QA. Die neue Version kann vorhandene Zustände korrekt lesen/antworten, aber einen externen GitHub-Zeitgeber **nicht** selbst neu starten, wenn dieser keine weiteren Takte auslöst. Es wird nichts zu einer Live-Reparatur oder einem garantierten Fertigstellungsdatum behauptet.

**Kein geplanter GitHub-Eingriff erforderlich,** um dieses Plugin zu installieren und den Status dort zentral auszugeben. PR #759 bleibt separat geschützt und wurde hier nicht geändert; **keine** Freigabe des geschützten Workflows durchgeführt. Kontrollierte WordPress-Abnahme erst mit tatsächlichem installierten Stand und echten eBay-Daten. Kein Live-Neustart oder Datenreset im Rahmen dieser QA.