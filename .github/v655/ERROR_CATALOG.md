# FEHLERKATALOG V6.55.0

## E-655-001 – V6.54 erforderte operativ noch einen zusätzlichen Cron-Anbieter

**Symptom:** Nach Installation von V6.54 war technisch ein externer Heartbeat vorhanden, der Nutzer hätte dafür aber noch einen zusätzlichen Cron-Dienst/Account einrichten müssen.

**Ursache:** Die Transportarchitektur war zwar hoster- und browserunabhängig, der operative Taktgeber war aber absichtlich providerneutral offen gelassen worden. Für dieses Projekt existiert mit GitHub bereits Infrastruktur, die diese Aufgabe ohne neuen Anbieter übernehmen kann.

**Rootfix:** Heartbeat ohne Shared Secret, POST-only, ohne Steuerparameter, serverseitig zeitbegrenzt; GitHub-Scheduler als vorhandene Infrastruktur. Kein neuer Account.

## E-655-002 – Öffentlicher Trigger darf keine neue Steueroberfläche werden

**Risiko:** Ein keyloser öffentlicher Heartbeat wäre untragbar, wenn er Provider, Operation, Konfiguration oder unbegrenzt Facharbeit auslösen könnte.

**Schutz:** Der Endpoint nimmt keine Steuerparameter an, startet ausschließlich bereits fällige interne Standardoperationen, verarbeitet höchstens ein Paket je angenommenem Tick und wird vor Facharbeit auf einen angenommenen Tick je 45 Sekunden begrenzt. Lease/CAS/Checkpoint bleiben unverändert aktiv. Terminal fehlgeschlagene Runs werden nicht automatisch neu gestartet.

## E-655-003 – GitHub-Scheduler darf nicht heimlich `main` verändern

**Schutz:** Der produktive Scheduler wird als getrennte Workflow-Datei vorbereitet. Aufgrund des bindenden Main-Schutzes wird er nicht automatisch in den Default-Branch gemergt. Der Release darf trotzdem technisch PASS sein; die Aktivierung des Schedulers bleibt als ausdrücklich ausgewiesener operativer Schritt offen.

## E-655-004 – Vorgänger-Realtest war hart auf V6.54 gepinnt

**Symptom:** Der erste V6.55-Gesamtlauf bestand Heartbeat, Scheduler, Architektur, Kernworkflow und Produkt-Markup, stoppte aber beim wiederverwendeten V6.54-Real-Produkt-Test mit `FAIL real WordPress loads V6.54.0`.

**Ursache:** Der historische Regressionstest prüfte neben dem Produkt-Markup absichtlich auch die damalige exakte Pluginversion und den V6.54-Runtime-Build. Unter V6.55 ist diese eine Assertion erwartungsgemäß falsch, obwohl alle Produktdarstellungsprüfungen PASS waren.

**Korrektur:** identischer Real-Produkt-Test für V6.55 mit unveränderten Markup-Assertions und aktualisierten Versions-/Build-Assertions. Keine Änderung am Produktionspatch.

**Schutz:** Versionsgebundene Vorgängertests dürfen nicht durch Entfernen der Versionsprüfung grün gemacht werden; sie werden für die neue Releaseversion explizit fortgeschrieben und im vollständigen Workflow erneut ausgeführt.
