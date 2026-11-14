# Robotik V60 – 0.4.7: 40101-Suchmaschinenfehler als eigenen Anbieterfehler behandeln, bestehenden Lauf 9/38 fortsetzen
**14.11.2026 | Nur Test, kein kostenpflichtiger API-Aufruf durch dieses Update, keine WordPress-Live-Installation durch den Assistenten.**

## Nachgewiesener Fehler
- WordPress-Live-Screenshot des Nutzers: In der installierten Version **0.4.6** steht der einmalig gestartete SEO-Gesamtauftrag bei **BLOCKED_UNCERTAIN / 9 von 38**, angezeigte Anbieter-Kosten **0,3535 USD** von Budget **1,00 USD**.
- Der gesendete **zehnte Auftrag** ist `serp/google/organic/live/advanced` für den vorhandenen Suchbegriff `telepräsenzroboter zuhause familie videobesuche`; der Nutzer hat die tatsächliche gesendete Anbieter-Datensatzansicht beigefügt. Daten, Land und Sprache werden nicht verändert.
- Angezeigter Fehler aus der gespeicherten Antwort: **`DataForSEO-Abfrage: Internal SE Server Error.`**. Der Anbieter dokumentiert den **inneren Task-Status 40101** für Suchmaschinen-Serverfehler (und getrennt HTTP 500 / DataForSEO 50000). Quelle: https://docs.dataforseo.com/v3/appendix/errors/
- **Die konkret nachgewiesenen Plugin-Mängel:** Die V59-Fehlerbehandlung erkannte nur den Text `DataForSEO: HTTP 500 `; den andersartigen Task-Status **40101** erkannte sie nicht. Außerdem verlangte die Wiederaufnahme `count(charges)==index` und `skipped_steps` leer; bei 9/38 mit acht erfolgreichen und dem bereits ausdrücklich übersprungenen vierten Auftrag war das rechnerisch unmöglich. **Die korrekten Zugangsdaten und 437 Keyword-Suchbegriffe waren nicht die Ursache.**

## Einziger gezielter Fix in derselben Pluginidentität
- `robotik-kategorie-workflow` **0.4.6 → 0.4.7**, keine zweite Pluginlinie, keine neue Tabelle und keine Änderung des WordPress-Importers oder der Veröffentlichung.
- Der bestehende `request()` bewahrt die *tatsächlich vom Anbieter gelieferten* inneren und äußeren `status_code` in der PHP-Fehlermeldung/Exception. Der eine zentrale Anbieterfehlerentscheid unterscheidet jetzt nachweisbare **40101**, **50000** und **HTTP 500** von fehlerhaften Eingabeparametern **40506** und nicht klassifizierten Fehlern.
- Für den bereits gespeicherten V59-Fehlertext `DataForSEO-Abfrage: Internal SE Server Error.` ist eine enge Kompatibilitätsregel vorhanden, damit keine neuen Daten oder Passwörter verlangt werden.
- Die kontrollierte Wiederaufnahme prüft den aktuellen Auftrag und dessen unmittelbar letzten Fehler, die gespeicherten vorherigen Ergebnisse **einschließlich bereits als ungeprüft markierter Aufträge**, die unveränderte V52-Prüfsumme, das Budget und eine laufende Sperre. Der Benutzer bestätigt **einmal** die Fortsetzung innerhalb seines bestehenden Budgets; der gescheiterte zehnte Auftrag wird **NICHT** erneut gesendet.
- Danach werden die ausstehenden 28 Aufgaben ausgeführt. Künftige belegte Anbieterfehler der genannten Arten werden ohne automatische Wiederholung als **NICHT_GEPRUEFT** protokolliert und innerhalb der alten Budgetreserve übersprungen. Andere Fehler, insbesondere ungültige Felder oder unklare Antworten, bleiben gesperrt. Kein ungeprüfter SEO-PASS; Ergebnisstatus bei Lücken `COMPLETE_WITH_GAPS`.

## Prüfungen vor Ausgabe
- Original-Plugin **0.4.6** als vollständiges ZIP geöffnet; gleiche **8 ZIP-Dateipfade**, `ZIP CRC PASS`, **PHP-Lint 5/5 PASS**.
- Ursprüngliche WP-Inventur, WordPress-Erstimport, Sammelveröffentlichung und **beide** JSON-Plan-Assets gegenüber dem Original-ZIP **bytegleich**. Nur vorhandenes DataForSEO-Include, Versionszeilen und README wurden verändert.
- Exakte **437/437** V52 Keywordzuordnungen und **38/38** Planaufträge unverändert; zehnter Auftrag und sein Keyword unverändert.
- Wiederaufnahme-Mock mit gesichertem **9/38**-Lauf, **0,3535 USD**, acht alten erfolgreichen Ergebnissen + einem früheren Fehlerloch: **Index wird 10, kein einziger Netzaufruf beim Wiederaufnehmen**, alte Ergebnisse und Budget unverändert.
- Wiederholtes Betätigen des Buttons kann keinen weiteren Auftrag still überspringen. Unrichtiger Task/fehlende Ergebnisse/nicht-passender Fehlertext blockieren.
- Vollständige Probe bis **38/38** mit den drei weiteren Providerfehlern **40101, 50000 und HTTP500**: jeder ausstehende Auftrag wurde **genau einmal** ausgeführt, kein alter Fehlerauftrag wiederholt, alle Fehler als Lücken erfasst, `COMPLETE_WITH_GAPS` und 16 fachliche HOLDs bleiben ohne verfügbares SERP-Ergebnis ungeprüft.
- Echter Parameterfehler **40506** bleibt blockiert, nicht als Anbieterstoerung maskiert. Kostenreservetest stoppt weitere Aufträge **vor** der Anbieteranfrage. Der ältere 3/38-Fall bleibt unterstützbar.
- Keine echten DataForSEO-Aufrufe oder Kosten in den lokalen Tests; WordPress-Live-Funktion erst nach Installation dort beurteilbar.

## Installation und anschließende einzige Handlung
1. Vorhandenes Robotik-Kategorie-Plugin auf **0.4.7** aktualisieren. Keine Deinstallation und kein Neuimport.
2. WordPress → `Robotik Kategorie → DataForSEO` → **„Mit gespeicherten Ergebnissen fortfahren – Fehler nicht wiederholen“** → den vorhandenen Kostenrahmen ausdrücklich bestätigen.
3. Nach abgeschlossenem Lauf **„EINEN SEO-Gesamtbericht (JSON) herunterladen“** und hier bereitstellen.

**ZIP:** `PLUGIN/CURRENT.zip` und `PLUGIN/VERSIONEN/0.4.7.zip` werden identisch aufbewahrt; SHA256 `1b40052cb8d959de30bc950839d2d58d9b964d9e60cf9a1faf5f058ba44574eb`, **57.513 Bytes**.