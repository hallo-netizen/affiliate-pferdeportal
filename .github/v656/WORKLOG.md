# Arbeitsprotokoll – V6.56 BUSINESS Safe-Gap Churn Revalidation Rootfix – 27.08.2026

## Bindung
Priorität: MASTER > aktueller Source > belegte GitHub-Historie > Chat > Vermutung. Keine Änderung außerhalb der nachgewiesenen Ursache. `main` bleibt unberührt.

## Livebefund
- Run: `50dec1a2-799`
- letzter Tick: 24.08.2026 02:00:13
- Pakete: 662
- Phase: `coverage_verify`
- BUSINESS: 7/311, fehlend 304
- Fehler: `business_safe_gap_new_missing_family`
- sicherer Frontend-Stand: unverändert aktiv

## Ursachenbeweis
Der gepinnte V6.55-Installer reproduziert die Live-Signatur deterministisch: Ausgang 8/311, erster Gap-Fill-Zielumfang 303 Familien; fällt während des laufenden Beweises eine zuvor gedeckte Familie aus, ergibt die nächste Coverage 7/311 / 304 fehlend und der unveränderte V6.50-Hard-Guard liefert exakt `business_safe_gap_new_missing_family`.

Die historische V6.50-Prüfung belegt, dass dieses Verhalten ursprünglich absichtlich als Hard-Guard eingeführt wurde. Der Live-Langlauf beweist nun, dass die Annahme „fehlende Familien bleiben zwischen Gap-Fill-Snapshot und späterer Coverage statisch“ für eBay nicht allgemeingültig ist.

## Rootfix
1. Der bestehende Safe-Gap-Hard-Guard bleibt byte-/verhaltensgleich.
2. `coverage_verify` prüft vor dem Guard auf neu fehlende Familien außerhalb des bisherigen kanonischen Beweisumfangs.
3. `public_verify` macht dieselbe Prüfung direkt vor öffentlicher Promotion.
4. Bei normaler Marktplatzänderung wird der Beweisumfang monoton erweitert und nur das neue Delta erneut entdeckt.
5. Discovery- und Selection-Derivate werden geleert; Upstream-Refresh, Quellen, Checkpoint und PRIVATE bleiben unverändert.
6. Der bestehende kanonische BUSINESS-Selector läuft anschließend über den vollständigen erweiterten Beweisumfang.
7. Erst danach entscheidet der unveränderte Safe-Gap-/Public-Vertrag.

## Produktionsscope
Geplant exakt vier Dateien:
- `includes/trait-ppar-ebay-run.php`
- `includes/trait-ppar-ebay.php`
- `pferdeportal-affiliate-router.php`
- `readme.txt`

Unverändert: Designplugin, CSS, Produktbild-Rootfix, Artikelprodukt-Markup, Providerregeln, PRIVATE-Regeln, Safety/Quality, Scheduler-Workflow, GitHub-Heartbeat, Portal-/Kategorielogik.

## Pflichtgates
- gepinnter V6.55-Finalstand + Hashes
- exakter Live-Fehler negativ reproduziert
- positive/negative V6.56 Churn-Gates
- alter Safe-Gap-Hard-Guard weiter aktiv
- selected-but-not-public weiter hart
- unbekannte Familie weiter hart
- monotone, manifestgebundene Begrenzung
- Delta-Discovery
- bestehender V6.55 Architektur-/Heartbeatvertrag als V6.56-Nachfolger
- Real WordPress 7.0.1 und 6.8.3 / MariaDB 11.4
- Produktbild-CONTAIN-Rootfix unverändert
- Artikelprodukt-Renderer unverändert
- Fresh-Unpack
- Source ↔ Installer ↔ MASTER Parität
- finale Gegenprüfung vor Releaseartefakt
