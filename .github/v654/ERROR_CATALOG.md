# FEHLERKATALOG V6.54.0

## E-654-001 – Self-Pump machte Hostingverhalten zur Laufvoraussetzung

**Live-Symptom:** neuer V6.52-Run blieb auf Pferde Atelier bei `reconcile_local`, `letzter Worker-Tick —`, `Pakete 0`, obwohl die lokale Release-Pipeline grün war.

**Ursache:** Ein erfolgreicher nicht-blockierender WordPress-Cron/Loopback-Dispatch belegte nur die Übergabeabsicht, nicht den tatsächlichen Start des nachfolgenden Workers auf jedem Hosting. Damit konnte ein Run ohne Browser dauerhaft als laufend stehenbleiben.

**Unzulässiger weiterer Fix:** weitere Timeout-, Lock-, `spawn_cron()`-, Loopback- oder hosterspezifische Sonderfälle.

**Rootfix:** der kanonische Worker wird ausschließlich durch einen provider-neutralen authentifizierten REST-Taktgeber in genau einem Paket pro HTTP-Aufruf fortgesetzt. Alte eBay-Cron-/Worker-Hooks werden auf Init entfernt. Fachworker, Lease/CAS und Checkpoints bleiben einmalig.

## E-654-002 – Kandidatbezogene BUSINESS-Fehler konnten den Gesamtfortschritt unnötig blockieren

**Symptomklasse:** ein einzelnes inzwischen ungültiges, unklassifizierbares oder nicht materialisierbares BUSINESS-Angebot konnte als normaler Materialisierungsfehler in den harten Fehlerpfad geraten, obwohl Coverage/Gap-Fill einen Ersatzkandidaten verwalten kann.

**Rootfix:** kandidatbezogene Source-/Quality-/Import-/Materialisierungsfehler werden als Soft-Failure aus der aktiven Auswahl entfernt, mit Item/Code/Concept im kanonischen `skipped_item_errors`-Audit protokolliert und anschließend von Coverage/Gap-Fill behandelt.

**Explizit hart:** fehlende globale Creative Library, Storage/Database, Checkpoint, Runtime, CAS/Lease/Invarianten und Public-Verify-Verletzungen. Diese werden nicht übersprungen.

## Schutzregel

„Fehler überspringen“ bedeutet ausschließlich kandidatbezogene Einzelfehler. Es ist kein allgemeines Abschalten von Safety-/Quality-/Checkpoint-Gates. Der letzte sichere öffentliche Checkpoint darf durch V6.54 nicht geschwächt werden.

## E-654-003 – Reale HTTP-Prüfung erbte adversarialen In-Process-Testzustand

**Symptom:** Der erste vollständige V6.54-Run bestand alle Produktcode- und Real-WordPress-In-Process-Prüfungen, der nachgelagerte echte HTTP-Aufruf antwortete jedoch `status=disabled` statt `idle`.

**Ursache:** Zwei getrennte Testfälle teilten versehentlich denselben persistierten Optionszustand. Der HTTP-Test hatte damit keinen deterministischen eigenen Enabled-Fixture. Zusätzlich lagen die Assertion-Zähler des `wp eval-file`-Skripts wegen Include-Scope nicht im selben globalen Scope wie die Hilfsfunktion.

**Korrektur:** ausschließlich Testinfrastruktur: `$GLOBALS`-basierte Zähler; expliziter frischer Enabled-Fixture am Ende des Realtests; separater Fixture-Reset und Readback direkt vor dem realen HTTP-Prozess. Produktionspatch bleibt bytegleich.

**Schutz:** Reale HTTP-Tests dürfen niemals implizit vom Endzustand eines vorherigen adversarialen Tests abhängen.
