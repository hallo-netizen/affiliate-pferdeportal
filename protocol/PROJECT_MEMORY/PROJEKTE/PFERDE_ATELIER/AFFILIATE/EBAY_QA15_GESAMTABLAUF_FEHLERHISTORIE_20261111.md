# Pferdeatelier eBay – Fehlerhistorie, gesamter Testablauf und QA15-Korrektur

**Stand 11.11.2026 | Arbeitsversion 6.72.326 | kein Live-Release.**

## 1. Belegtes Ausgangsproblem

- Tatsächliche WordPress-Screenshots vom 11.11.2026 zeigten wechselnde Phasen, zwischenzeitlich `0/298` in einem neuen, noch nicht bewerteten Gesamtlauf, aber weiterhin **489 gespeicherte eBay-Freigaben** (nicht mit 489 sichtbaren Kacheln verwechseln). Das Backend meldete einen **Protokoll-Speicherfehler**. Es liegt keine echte Datenbank-Trace-Datei vom Server vor.
- Bisherige Tests hatten viel zu oft **Teilwege mit nachgestellten eBay-/WordPress-Antworten** als vollständigen Erfolg dargestellt. Es bestand keine real durchlaufene Abnahme auf dem WordPress-Server.
- Das alte lokale Nachweisprogramm für angeblich **187 offene Familien** benutzte dieselbe hochgeladene Datei, die tatsächlich **138** Familien enthält. Ein solcher alter Test ist **kein valider Nachweis** für den aktuellen 138er Export. Diese Vermischung wurde korrigiert, nicht übergangen.

## 2. Konsolidierte Fehlerhistorie – was bereits gelöst ist, was offen bleibt

| Fehlerbereich / Stand | Bereits vorhanden / früher korrigiert | In QA15 erneut geprüft | Statusgrenze |
|---|---|---|---|
| Run-Cursor, Retry, Timeout, fälschlicher Neustart (311/312 und weitere) | Gespeicherter kanonischer Lauf, begrenzte Pakete, Wiederaufnahme | Durchgehender Start/Worker/Stop/Resume-Simulationslauf; identische Run-ID und Cursor | WordPress-Neustart im realen Betrieb nicht belegt |
| „queued“ = „complete“, UI-Gates (313/314), 0/298-Nachsuchzähler (315, QA12) | Trennung Teillauf/öffentliche Abdeckung; neue laufende Runde ohne sofortigen Nachweis | Provenienz und Ausgabezustand getrennt bewertet | 0/298 zeigt allein keinen gelöschten Bestand |
| Geschlossene Produktfamilien / Versicherungen / eBay Deutschland | 26 Nicht-Waren ausgeschlossen, 298 Warenfamilien; nur gewerbliche EBAY_DE-Angebote | Originalauswahl und 138-Familien-Test, 35 begrenzte Pakete | Keine unendliche Suche nötig, reale 298er-Endbilanz noch offen |
| Bereits gefundene Angebote, Synonyme, Mehrfachzuordnung (QA2–QA7) | Ein zentraler Selector und Wiederverwendung gespeicherter Quellen, harte Ablehnungsregeln | Original-Selector-Tests und 138er Replay, zwei gezielte Einzelfehler übersprungen | Externe einzelne Produktklassifikation nicht pauschal freigegeben |
| Pause/Fortsetzen (QA8/QA11) | Bereits vorhandener Stoppmarker und CAS-Fortsetzung | Echte `run_ebay_canonical_worker`-Steuerfunktion mit simulierten externen Phasen: gleiche UUID, kein Rücksetzen | Externe WP-/Loopback-Scheduler nicht getestet |
| Eine schlechte eBay-Quelle blockiert ganzen letzten Checkpoint (QA11/QA13) | Bereits vorhandene sichere Einzel-Append-Freigabe, Auth-Fehler fail-closed | QA11-Original-Trait mit erfolgreichen/fehlgeschlagenen getItem-Doubles + QA13-SAFE-Append-Test | Kein öffentliches Live-Frontend verifiziert |
| Beitrags-Produktplan startet immer von vorn (QA14) | Cursor bleibt, höchstens ein zusammengefasster Nachlauf | 12 direkte QA14-Artikellisten-Fälle erneut bestanden | Kein echter WP-Cron-Durchlauf |
| Beendetes Produkt/ungeprüfter Nachrücker (QA14) | Ersatz gilt erst nach wirklicher SAFE-Freigabe als publiziert | 12 direkte QA14-Ersatz-/Checkpoint-Fälle erneut bestanden | eBay-Live-Antwort fehlt |
| Recherche vs. unabhängige Verfügbarkeit (QA9) | Bestehender getItem-Refresh getrennt von Discovery | **Originale** `ebay_public_availability_tick`-Methode: Forschung pausiert, eine verfügbar, eine beendet, eine Providerstörung; 2h-Folgezeitpunkt; Suchcursor unverändert | Echte WordPress-Cron-Zeitplanung noch nicht bestätigt |
| Protokollfehler / verschwundene Historie (QA12) | Privates Laufjournal in WordPress-Optionen, Admin-CSV/JSON | **Korrigiert in QA15**, Fehlerfenster nach teilweisem Schreiben im Original reproduziert und Gegenprobe bestanden; 100er-Grenze, älterer Lauf, 106 echte Exportzeilen | Persistenter kompletter DB-Ausfall kann weiterhin Lücken verursachen und wird als solcher markiert |
| Backend/Frontend-Serverlast | Ein Worker, aber lückenlose Selbstfortsetzung und QA12-Protokollmehrarbeit | **Nicht verändert** gemäß Nutzervorgabe | Erst NACH funktionierendem Gesamtworkflow behandeln |

## 3. Tatsächlich korrigierte gemeinsame Speicherursache

**Nachgewiesenes QA14-Fehlerfenster:** Das Protokoll schreibt zuerst das Ereignis in einen Chunk und danach den Eintragszähler. Wenn das Ereignis gespeichert wird, der anschließende Zähler aber nicht, bleibt ein „verwaister“ Eintrag. Bei der nächsten Speicherung erkennt QA14 den bereits besetzten Platz und kann den Protokollfortschritt nicht mehr ordnungsgemäß fortsetzen. Der eigentliche eBay-Lauf kann dennoch voranschreiten; deshalb war die rote Warnung nicht dasselbe wie gelöschte Produkte.

**Vorher/Nachher als ausführbarer Test:**

- QA14 6.72.325: Zähler nach wiederholter Speicherung **1**, obwohl Chunk bereits **2** Einträge enthält – Fehler bleibt bestehen.
- QA15 6.72.326: Der vorhandene Eintrag wird an seiner Nummer identifiziert und sein Metadateneintrag verifiziert nachgetragen. Danach **Zähler 3 / 3 gespeicherte Einträge** beim nächsten Fortschritt.
- Bei einem **einmaligen** Fehler beim Chunk-/Meta-Schreiben wird derselbe Protokolleintrag **genau einmal erneut** versucht. Bei anhaltendem Fehler wird die Warnung gesetzt, aber der separat bestätigte Produkt-/Run-Stand bleibt erhalten. Keine unbestätigten Produkte werden freigegeben.
- Derselbe eine Protokoll-Schreibweg wird nun aus Runzustand, CAS-Fortsetzung, öffentlicher SAFE-Freigabe und unabhängiger Verfügbarkeit aufgerufen. Kein zweites Logsystem.

**Bestandsschutz:** Keine Neuaufsetzung, keine Migration, keine `delete_option`-Änderung, keine neuen Tabellen, keine geänderten Such-/Klassifikations-/Marketplace-Regeln, keine neue Cron-Engine, keine geänderte Performance-Taktung. Beim Versionswechsel bleiben vorhandene eBay-Angebote, zugeordnete Produktfamilien, Run-UUID, Cursor und öffentliche SAFE-Checkpoints unangetastet.

## 4. Was wurde vollständig durchgehend simuliert?

**Eine fortlaufende Laufgeschichte** mit dem *echten* kanonischen Runstart, Worker-Einstieg, Lease, Speicherung, Stoppmarker, Fortsetzung, Fehlerprotokoll und einem späteren neuen Lauf; die eBay-/WordPress-Arbeit innerhalb der Phasen wurde kontrolliert **nachgestellt**, damit kein tatsächlicher Marktplatz oder die Website verändert wird.

Die Phasenfolge war:

`reconcile_local → refresh_remote → selection_prepare → business_select → business_materialize → coverage_verify → gapfill_discovery → gapfill_select → public_verify → checkpoint_cleanup_business → completed`

Zwischen Anfang und Ende: fehlgeschlagene Datenbankspeicherung an genau einem Punkt, **kein bestätigter Fortschritt für nicht gespeicherten Cursor**; manuelles Anhalten, Status `paused`, Wiederaufnahme derselben Run-ID und desselben Cursors; ein guter und ein nicht bestätigter Kandidat, alter Logeintrag bleibt erhalten; nach Abschluss beginnt neuer Run und sein Protokoll überschreibt das alte nicht.

**Unabhängige reale Plugin-Funktionen zusätzlich getestet:** Original-Selection, SAFE-Teilfreigabe, 401/403-Sperre, Schlussprüfung, Beitragsplan, Ersatzprodukt, unabhängige Verfügbarkeitsprüfung und CSV-Export. Hier waren eBay-Antworten/WordPress-Datenbankwerte **Testdaten**.

## 5. Prüfergebnis und Testbelege

- **17 von 17 Testprogrammen bestanden**, keine PHP-Fatal/Warnings in Testlogs.
- **138 aktuelle Produktfamilien** in **35** begrenzten Paketen; **2** simulierte fehlerhafte Familien stoppen die anderen **nicht**.
- **106 echte CSV-Datensätze** aus dem Exporthandler: **104 Ereignisse** des alten Runs, **1** Ereignis des neuen, **1 ausdrücklich als unvollständig markierter historischer Kurzbericht**.
- **23/23 PHP-Syntaxprüfungen**, **66/66 ZIP-Einträge CRC**, **62/66 Dateien byteidentisch** zu 6.72.325. Nur die beiden bereits existierenden eBay-Traits und die zwei Versionsdateien sind verändert.
- SHA-256 der TEST-ZIP: `c453831225c0c7d005c66140622abb8e636b9884aa796b363a0e2456ce525b1a`, **5.376.701 Bytes**.

**Reproduzierbare Dateien:** `QA15_FULL_REGRESSION_LOG.txt`, `full_workflow_sim.php`, `qa15_audit_matrix.php`, `qa15_availability_while_paused.php`, `QA15_LAST_MILE_REAL_METHOD_TEST.php`, `QA15_AUDIT_EXPORT_REAL_METHOD_TEST.php`, `EBAY_KISS_CURRENT_138_FAMILIEN_REPLAY_TEST_20261111.php`, `QA15_KISS_DURABLE_AUDIT_VS_QA14.patch` und `QA15_PACKAGE_EVIDENCE.json`.

## 6. Offen – NICHT als bestanden bezeichnen

**Ein vollständiger realer WordPress-/MariaDB-/eBay-End-to-End-Test einschließlich Frontend-Kacheln ist nicht durchgeführt.** Die Laufsteuerung wurde gemeinsam simuliert, aber die externen einzelnen Phasen wurden nachgestellt und separat auf echten PHP-Methoden getestet. Dadurch ist kein seriöser Beweis möglich, dass alle live gespeicherten Angebote auf der richtigen Seite erscheinen oder die echten Serverprobleme behoben sind. Der alte QA12-Protokollverlust kann nicht rückwirkend vollständig rekonstruiert werden. Ein hartnäckiger Datenbankausfall kann Protokolle weiterhin unvollständig machen; diese Unvollständigkeit muss erkennbar bleiben.

**Nächste reale Abnahme statt weiterer Mini-ZIPs:** Ein gesicherter WordPress-Test mit repräsentativen Daten und einem beobachteten Gesamtlauf einschließlich eBay-API, öffentlichem SAFE-Checkpoint, Kategorien-/Beitragskacheln, CSV-Historie, Pause/Fortsetzen und unabhängiger Verfügbarkeit. Ein fehlgeschlagener realer Test wird zuerst im selben Fehlerpfad korrigiert. Erst danach Serverlast/Backend-Verschlankung, wie ausdrücklich vereinbart.

Keine Installation in Hobbydepot oder Hab & Bewahr. Transferregister bleibt eine Referenz, kein automatischer Patch.

## Aktueller Stand erneut geprüft – 11.11.2026, nach QA15

Bei erneuter Sichtung der gespeicherten Bibliothek und des physisch vorhandenen Testpakets ist **QA15 6.72.326 weiterhin die neueste identifizierte Pferdeatelier-eBay-Testfassung**. Datei `/mnt/data/Pferdeatelier_Affiliate_6.72.326_QA15_KISS_GESAMTABLAUF_NUR_TEST.zip` ist vorhanden, SHA-256 **c453831225c0c7d005c66140622abb8e636b9884aa796b363a0e2456ce525b1a** stimmt mit `QA15_PACKAGE_EVIDENCE.json` überein. ZIP-Integrität frisch durch `unzip -t` bestätigt: **keine Fehler**. Die alte `QA15_FULL_REGRESSION_LOG.txt` wurde erneut gesichtet; positive Testnachweise für einzelne Providerfehler/401–403, Schlussprüfungs-Wiederaufnahme, read-only Backend sowie verfügbare/beendete/störende Angebote bei pausierter Recherche sind dort enthalten.

**Präzise Begrenzung:** Keine erneute Ausführung aller 17 Tests im Live-WordPress, keine Anmeldung an WordPress/MariaDB und kein realer eBay-API-End-to-End. Der vorliegende Testharness ersetzt WordPress/DB und externe eBay-Antworten. Ein bestehender früherer Fehler `QA14` der Audit-Protokollierung wurde in QA15 im PHP-Code korrigiert, aber auf dem produktiven Datenbankzustand weder live bestätigt noch rückwirkend vollständig rekonstruiert.

**Nicht mit eBay verwechseln:** Zuletzt gespeicherte `PSTE-...` und `PSERC-...` ZIP-Dateien gehören zum **K0/Texterstellungssystem**, nicht zum eBay-Affiliate-Plugin; sie haben keine Aussagekraft für die eBay-Live-Reparatur.

**Verbindlicher Status:** **QA15 TEST / NICHT ABGENOMMEN**. Nächster beweisender Schritt bleibt der echte, gesicherte WordPress-Abnahmetest des Gesamtablaufes (public SAFE-Produkte, Kategorien-/Beitragskacheln, gleicher Cursor bei Pause/Fortsetzung, Verfügbarkeit getrennt, Daten/Logs). Performance-Nacharbeit erst anschließend, wie vom Nutzer festgelegt. Kein neues Plugin im Zuge dieser Statusprüfung erstellt oder installiert.
