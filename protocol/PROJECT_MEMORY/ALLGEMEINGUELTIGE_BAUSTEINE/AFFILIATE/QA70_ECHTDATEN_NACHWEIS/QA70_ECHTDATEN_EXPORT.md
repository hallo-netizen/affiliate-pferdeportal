# QA70 — Realdaten-Export innerhalb der bestehenden Affiliate-Zentrale (KISS)

**Status: nur QA, keine Livefreigabe, keine behauptete echte 1:1-Abnahme.**

## Wo stehen wir?

Die alten Exporte enthalten 2.769 echte Laufereignisse und 278 offene Familien, aber keine vollständigen Produkt-/WordPress-Daten. Die Nachsimulation mit erfundenen eBay-Antworten konnte die Liveentscheidung nicht beweisen. Der Live-Lauf mit UUID `97507628-4f4d-4527-bd77-fa573bce7067` ist laut letztem Nutzerbild pausiert.

## Konkrete KISS-Maßnahme

Die **vorhandene** admin-geschützte Protokoll-Exportfunktion besitzt nun neben CSV und JSON **einen zusätzlichen Dateityp**: `Echte Produktdaten für Gesamtprüfung (nur lesen)`. **Gleicher Administrator- und Nonce-Schutz; kein neuer REST-Endpunkt, Cron, Job, Datenbank- oder Entscheidungspfad.** Der Export liest einmalig und paketweise:

- Gespeicherten aktuellen eBay-Lauf einschließlich Auswahlzuständen und Cursor
- Unveränderten öffentlichen SAFE-Checkpoint
- Eingestellte Sachregeln und mitgelieferten Original-Zielkatalog
- Die tatsächlichen bereits gespeicherten eBay-BUSINESS-Produktdatensätze einschließlich `source_payload` (wo vorhanden), Kennung, Quelle, Alter, Freigabe und Ablehnungsgrund
- Die vorhandenen eBay-Ausgabeobjekte, Creative-Zeilen und manuellen Entscheidungen
- WordPress-Status der referenzierten veröffentlichten Kampagnen

Ausgabe ist **NDJSON** (jede Zeile ein eindeutig markierter Datensatz), geschützt und nur durch aktives Klicken eines Administrators. Die Daten werden nicht in einer neuen Tabelle gespeichert. Geheimnisse, Authentifizierung und Kundendaten werden bei der Ausgabe ausgeblendet; Trackinglinks nur als SHA256-Fingerabdruck geliefert.

**Wahrheitsprüfung:** Der letzte Datensatz meldet die Anzahl aller exportierten Elemente, Datenbank-Lesefehler und ob Lauf und Checkpoint vom Start bis zum Ende identisch geblieben sind. Bei Speicheränderung/Lesefehler: kein Abnahme-PASS.

**Grenze:** Der Export kann keine **historischen nicht gespeicherten eBay-HTTP-Antworten** zurückholen. `source_payload.raw` enthält nur *das tatsächlich gespeicherte* Quellenabbild. Eine 1:1-Abnahme der Vergangenheit wird damit nicht erfunden. Ein späterer Live-Gesamtdurchlauf und öffentliche Sichtbarkeit bleiben zusätzliche harte Abnahmebedingungen.

## Prüfung

- Original-PHP-Exportfunktion mit simulierten WP-Datensätzen aufgerufen: **2 eBay-Produkte, 1 Ausgabeobjekt, 1 Creative, 1 manuelle Entscheidung, 1 veröffentlichter Post**; Abschluss mit konsistenter Anzahl. Das ist ein **Funktionstest**, kein echter Produktdatenexport.
- Im Harness alle Schreib-/HTTP-Aufrufe verboten; keine aufgerufen. Geheimnisse und Original-Tracking-URL nicht im Ergebnis. Tracking-Fingerabdruck korrekt.
- Original-PHP-Regression der bereits zuvor korrigierten Auswahl und Veröffentlichung: 5 und 3 Fälle; sieben gesamte PHP-Modellketten, 16 Statusfälle, 11 Startzeitfälle, neun Frischefälle; dort sind WP/eBay-Antworten **nachgestellt**.
- 23/23 PHP-Lints, 66/66 ZIP-Einträge CRC, nur 5 erwartete Dateien gegen 6.72.348 geändert.
- **2.769 Originalereignisse** und 278 Familien erneut unabhängiger Abgleich: 5/283, 153 übersprungene ausgewählte Angebote, 196 vorzeitige Bereinigungstakte.

## Nächster Betriebsschritt

Die vorhandene QA-ZIP **6.72.349** ist für einen kontrollierten Test mit dem *echten* WordPress-Datenbestand vorbereitet; kein selbstständiges Live-Update durchgeführt. Nach Installation in einer solchen Umgebung **einmal** auf `eBay → Echte Produktdaten für Gesamtprüfung (nur lesen)` klicken und die NDJSON-Datei zur echten Modellprüfung verwenden. Bis WordPress-Eingangsdaten und reale Anbieterantworten vorliegen, bleibt die vertragliche Gesamtabnahme **NICHT BESTANDEN**.