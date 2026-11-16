# QA88 – KISS: redundanten stündlichen Vollabgleich beseitigt (16.11.2026)

**Bindender Vertrag:** QA69. **Quelle:** vollständiges Originalpaket 6.72.353 (66 Dateien), nicht alte GitHub-Releasequelle.

## Nachgewiesene Ursache

Der direkte PHP-Code `includes/trait-ppar-ebay-run.php::ebay_external_tick_due_operation()` startet nach einem erfolgreichen, noch keine 7 Tage alten Sync **jede Stunde** erneut den kanonischen `refresh`. Der Handler startet diesen mit `reconcile_local`; der Original-`ebay_run_tick_reconcile()` arbeitet über `run_ebay_maintenance_v2` und `ebay_run_tick_remote()` über einen **breiten** `ebay_start_inventory_refresh_job(true,true)`. Dieser Weg bearbeitet nicht ausschließlich die 309 SAFE-Produkte.

Dies ist **zusätzliche Arbeit** neben dem bereits vorhandenen, unabhängigen, klein begrenzten `ebay_public_availability_tick()`, der in QA87 schon ausschließlich die tatsächlich im SAFE-Checkpoint publizierten BUSINESS-Quellen aktualisiert. Dieser doppelte regelmäßige Weg widerspricht QA69 Abschnitt C/D/E (nur ausgewählte Quellen aktuell halten; keine globalen wiederholten Bestandsdurchläufe).

**Wichtig:** Der WordPress-Screenshot vom 16.11.2026 14:28 zeigt `refresh_remote` und 309 gesicherte Freigaben; er enthält aber keine ausdrücklich sichtbare `operation`. Ohne neuen authentifizierten Live-Auszug ist **nicht bewiesen**, dass genau jener einzelne Lauf `operation=refresh` und nicht `sync` war. Der automatisch stündlich fällige Pfad ist trotzdem direkt im unveränderten Originalcode bewiesen.

## Eine KISS-Korrektur, vorhandene Funktionen bleiben

- Der **automatische** Heartbeat darf nur noch eine volle `sync`-Suche nach 7 Tagen ansetzen. Den redundant jede Stunde gestarteten kanonischen Inventory-`refresh` gibt es nicht mehr.
- Der **bestehende** unabhängige `ebay_public_availability_tick()` aktualisiert weiterhin die im SAFE-Checkpoint verzeichneten Quellen (bis zu 20 pro Paket, maximal 22 Sekunden; keine neue Auswahl).
- Vorhandene manuelle Refresh-Funktion und bereits gespeicherte aktive Refresh-/Sync-Aufträge bleiben vollständig unangetastet. **Ein schon laufender breiter Refresh wird absichtlich NICHT abrupt abgebrochen**, damit seine gespeicherte UUID, Cursor und Quelle nicht zerstört werden. Nach dessen Abschluss wird nicht erneut automatisch stündlich breit gescannt.
- Fehltext `0/298` aus der Backendanzeige entfernt; der richtige Zielvertrag fordert 283 Familien, deren bestätigter öffentlicher Endstand weiterhin separat bewiesen werden muss.
- **Keine** geänderten Providerregeln, Produktquellen-/SAFE-Gates, Datenbanktabellen, gespeicherten Produktlisten, Github-Workflows, neuen Zeitgeber, Webhoster- oder K0-Konfiguration.

## Gegenprobe gegen die echte QA87-Quelle

- **Automatische Fälligkeit in echtem PHP:** QA87 4 von 9 Zielvertragsfällen FEHLER (stündlicher doppelter `refresh`), korrigiertes QA88 9/9 PASS. Die wöchentliche `sync`-Fälligkeit und ein aufgeschobener abgeschlossener Suchversuch bleiben korrekt.
- **15 echte PHP-Heartbeat-Zustandsfälle:** 15/15 PASS. Pausierte, abgeschlossene und fehlgeschlagene Recherche blockiert die reine Quellenaktualität nicht.
- **309 SAFE-Kampagnen, 496 historische ausgegebene Objekte, 9792 Quellzeilen im synthetischen Modell:** 309/309 in 16 zeitlich simulierten Paketen, 0 historische Fremdquelle, 0 neue Produktsuche, ursprünglicher öffentlicher SAFE-Checkpoint erhalten, 0 doppelt. Leerer SAFE-Checkpoint: 0 Anbieteraufrufe.
- **66 Archivdateien identischer Pfadbestand**, nur vier bearbeitet (zwei eBay-Traits; Hauptdatei-Versionsnummer und Readme); 23/23 PHP-Syntaxprüfungen; ZIP erneut entpackt und byteidentisch mit lokal getesteter Quellkopie.
- Bestehender sehr alter QA75-Gesamttest ist mit **QA87 und QA88 gleichermaßen** inkompatibel und zeigt in beiden Versionen bei der finalen Cleanup-Phase einen Mock-Laufzeitfehler. Er wird **nicht** als erfolgreicher QA88-End-to-End-Test ausgegeben.

## Artefakt/Status

**Einziger vollständiger Testkandidat:** `QA88_PFERDEATELIER_AFFILIATE_ZENTRALE_6.72.354_KISS_FINALER_ZEITLAUF_FIX.zip`.
SHA256 `15980cfd0e0e5e2179ed889b045404e10857a164beb42dcb9d76224a84bd251e`.
Ablage: persönliche Projektbibliothek `/pferdeatelier/PLUGINS/QA/QA88_KISS_KEIN_STUENDLICHER_VOLLABGLEICH/` mit vollständigem Original-delta `QA88_GESAMTPATCH.patch`, `QA88_GESAMTPRUEFUNG.json` und ausführbarem PHP-Fälligkeitstest.

**QA69 LIVE weiterhin NICHT BESTANDEN:** Echte eBay-Prüfdauer, verlässlicher Zeittakt, neue sichtbare eBay-Frontend-Karten und 283er publizierte Familien-Endbilanz wurden nicht direkt gemessen. Ein lokaler Quelltest ist keine WordPress-Live-Freigabe.

**Betriebsweg:** Bisherige WordPress-Datenbank sichern, nur die bestehende Affiliate-Zentrale durch genau diese ZIP ersetzen, keinen Suchlauf manuell neu starten und den begonnenen alten Lauf unangetastet lassen. Danach eine einzige vorhandene eBay-Sichtbarkeitsdiagnose gegen den bekannten Morgenstand vergleichen (293 wegen Ablauf ausgeblendete SAFE-Kampagnen, 309 insgesamt). Keine GitHub- oder Hoster-Einstellung für die Korrektur nötig.
