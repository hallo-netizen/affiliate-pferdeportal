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

## E-654-003 – Reale HTTP-Prüfung vermischte Prozesszustände

**Symptom:** Die V6.54-Gesamtläufe bestanden Produktcode, Architektur, Kernworkflow-Parität und Real-WordPress-In-Process-Prüfungen, stoppten aber im nachgelagerten separaten HTTP-Test.

**Ursache:** Die Testinfrastruktur setzte voraus, dass ein in einem WP-CLI-Prozess künstlich auf `enabled=true` gesetzter eBay-Zustand nach einem frischen HTTP-/Plugin-Bootstrap unverändert aktiviert bleibt. Der reale Bootstrap normalisiert die Providerkonfiguration jedoch zulässigerweise und deaktiviert eBay ohne erforderliche Provider-Credentials. Das ist kein Fehler des externen Tick-Transports.

**Korrektur:** ausschließlich Prüfinfrastruktur. Die Due-/Autostart-Semantik bleibt im deterministischen echten WordPress-Prozess geprüft. Der separate HTTP-Prozess prüft nur seine eigene Aufgabe: Server erreichbar, falscher Schlüssel = HTTP 403, korrekter Schlüssel = HTTP 200 und gültige JSON-Antwort mit Status. Eine künstliche `enabled=true`-Persistenz über Prozessgrenzen ist kein Releasekriterium mehr.

**Schutz:** Reale HTTP-Transporttests dürfen nicht von fachfremden Provider-Fixture-Annahmen abhängen. Produktionspatch bleibt unverändert.

## E-654-004 – Bindende README enthielt widersprüchlichen historischen Transportvertrag

**Symptom:** Das erste vollständig grüne V6.54-Release enthielt im `readme.txt` neben dem korrekten neuen 6.54-Vertrag noch einen historischen Absatz, der den alten browsergebundenen Admin-AJAX-Betrieb als weiterhin gültig bezeichnete und Browser-Unabhängigkeit ausdrücklich verneinte.

**Ursache:** Der Runtime-Rootfix ersetzte den tatsächlichen Transport, aber ein älterer dokumentarischer Betriebsabweichungsabschnitt blieb im bereits zum Produktionsscope gehörenden `readme.txt` erhalten. Damit wären Runtime und bindende MASTER-Dokumentation widersprüchlich gewesen.

**Korrektur:** Der historische Absatz wird innerhalb desselben bestehenden 4-Dateien-Scopes ausdrücklich als durch 6.54.0 abgelöst markiert und durch den aktuellen externen REST-Taktgeber-Vertrag ersetzt. Source und Fresh-Unpack werden negativ auf den alten Satz und positiv auf den aktuellen Satz geprüft; der Korrekturpatch wird in der MASTER abgelegt.

**Schutz:** Ein automatisches Runtime-PASS genügt nicht, wenn die bindende Release-Dokumentation einen gegenteiligen aktuellen Betriebsvertrag enthält. Die gesamte erzeugte MASTER wird deshalb vor Freigabe auf solche Widersprüche geprüft. Runtime-/Worker-/Providerlogik wird durch diesen Dokumentationsrootfix nicht verändert.
