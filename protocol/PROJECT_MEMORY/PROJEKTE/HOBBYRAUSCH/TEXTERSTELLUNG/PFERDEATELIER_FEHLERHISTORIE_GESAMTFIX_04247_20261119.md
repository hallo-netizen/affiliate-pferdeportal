# 19.11.2026 – Pferdeatelier-Fehlerhistorie ↔ Hobbydepot, EIN 0.4.24.7-Gesamtfix

**Basis:** realer Nutzerlauf `3D-Bogenschießen` (PAA Timeout, 5 Rohkeywords, geparkter Originalauftrag); Diagnosen `texterstellung-diagnose-20261119-100006.json` und `...105348.json`. Der bisherige 0.4.24.6-Button hat zweimal `NOT_READY` geliefert, kein zusätzlicher bezahlter Task-POST.

## Nachgewiesene Altursachen und ihre Behandlung
1. **Timeout vor Anbieterergebnis:** Ursprungscode aus Pferdeatelier 0.4.23 und der Original-0.4.31-abgeleiteten Kopie bytegleich in Hobby 0.4.24.5. In 0.4.24.6 schon korrigiert; Fix bleibt erhalten.
2. **Falscher Einzelstatus:** 0.4.24.6 `PSTE_DataForSEO_Client::peopleAlsoAskTaskReady()` verwendete ausschließlich `GET .../tasks_ready`. Nach DataForSEO-Dokumentation: Dies listet nur **noch nicht abgeholte** fertiggestellte Tasks aus einem begrenzten Zeitfenster. Abwesenheit bedeutet weder `not yet ready` noch `failed`. **Dies ist ein zusätzlich belegter, noch nicht behobener Originalfehler.**
3. **Unvollständige/fremde Anbieterantwort und fehlender Status:** Aus der Pferdeatelier-Recherchehistorie bekannt; ursprünglicher Response-Validator bestand bereits. Neuer direkter Statusleser weist fehlende/abweichende ID, fehlende Ergebnisse, ungewöhnliche Task-Anzahl ab; 40601/40602 = wartet, nur 20000 + exakte ID + Result = fertig, andere Codes = Fehler (nicht `PENDING`).
4. **Erneute bezahlte Recherche / doppelte Entscheidung:** Auftragsarchiv, UUID-/Kategorie-Owner, Sperren und Transport-Outcome-Guard bestanden bereits im Ausgangscode; unverändert lassen und in Negativtests erneut prüfen, keine zweite Architektur oder Prüfregel einführen.
5. Spätere Pferdeatelier-Probleme (Kategoriezuordnung, Titelbescheinigung, MINI/K0/PSERC und Relevanz) sind andere Stationen und ohne aktuellen Hobby-Befund keine legitimen Masseneingriffe. K0/Multi weiterhin separat gesperrt.

## Exakte Quelländerungen
- `Texterstellung_Hobbydepot_0.4.24.7_PAA_BESTANDSFIX_GESAMTPRUEFUNG.zip`.
- SHA256 `1889f9137bba40c0eaf130c47d2866bdfea0ed33850f63a43f0b3e9eb5848d2e` / **509239 Bytes**, WordPress-Verzeichnis `texterstellung-hobbydepot/`, Header Version **0.4.24.7**.
- **83/87 Originaldateien unverändert**, exakt vier vorhandene PHP-Dateien geändert: `class-pste-dataforseo-client.php`, `class-pste-research-job.php`, `class-pste-breadth-research-queue.php`, `texterstellung.php`.
- **Ein gemeinsamer GET-Statusleser** für die gespeicherte Task-ID über `/v3/serp/google/organic/task_get/advanced/{task_id}`. Kein weiterer POST in Wiederaufnahme. Alte Readiness-API wird auf dieselbe Prüfquelle delegiert. Fertiges gültiges Ergebnis wird durch unveränderten Original-PAA- und FINALIZE-Prozess geführt; PENDING/Providerfehler lassen das Archiv unverändert. Bestehende Daten-/Kosten-/Publikationsschutzregeln unverändert.

## Nachweise
- **38/38** Tests der tatsächlichen geänderten Provider-PHP-Klasse mit Mockantworten: READY/40601/40602/Providerfehler/40401/503/falsche ID/fehlende Antwort, nur GET und kein POST, auch ursprünglicher Methodenname.
- **31/31** Tests der echten ursprünglichen PSTE-Archiv-/Queue-/Jobklassen in WordPress-/DB-Mocks: gleicher geparkter Job bis FINALIZE, 1 GET/0 POST, Provider nicht bereit/Fehler ohne Schreibzugriff, Duplikat/falsche Kategorie/UUID/beschädigtes Archiv/zweiter Auftrag abgewiesen, Timeoutprüfung.
- **69/69 gezielte lokale Tests**, **78/78 PHP-Syntax**, **8/8 JSON**, **87/87 ZIP CRC**. Tests lokal, **keine echte WordPress- oder DataForSEO-Live-Abfrage**. Der tatsächliche Anbieterstatus des Nutzers ist weiterhin unbekannt.
- Ausführlicher Bericht inkl. JSON/Testdaten im Hobbydepot-Library-Fachbüro `/hobbydepot/TEXTERSTELLUNG/PRUEFBERICHTE/`, Bericht `Texterstellung_0.4.24.7_PRUEFBERICHT.md`.

## Tatsächliche Büroablage (erfolgreich bestätigt)
- Zentrales Pluginbüro: `/Hobby Depot/Plugin-Büro/Texterstellung_Hobbydepot_0.4.24.7_PAA_BESTANDSFIX_GESAMTPRUEFUNG.zip`.
- Fachbüro: `/hobbydepot/TEXTERSTELLUNG/INSTALLATIONSKANDIDATEN/Texterstellung_Hobbydepot_0.4.24.7_PAA_BESTANDSFIX_GESAMTPRUEFUNG.zip`.
- Eigene Bürodatei `Texterstellung-CURRENT.md` mit diesem Stand überschrieben, Vorgänger **0.4.24.6 archiviert**.

## Einziger Nutzerweg
Sicherung (WPvivid) → 0.4.24.7 per WordPress „Installiertes Plugin ersetzen“ installieren → `Texterstellung → Recherche → Gesperrten Auftrag prüfen und falls fertig fortsetzen` **einmal** klicken. Danach den **neuen echten Einzelstatus** ablesen (wartet / fertig / Anbieterfehler). Nicht `Nächste offene Kategorien recherchieren` drücken, sonst potenziell neue bezahlte Recherche. K0 weiterhin gesperrt.
