# Pferdeatelier: Originalquellen tatsächlich gefunden, Neustart mit drei echten Profilen getestet (11.11.2026)

**Status:** Echte archivierte WordPress-Quelldaten gefunden; isolierter originaler PSTE-Queue-Wiederanlauf mit drei echten Profilen 25-mal erfolgreich; keine echte WordPress/MySQL-Instanz verwendet; keine neue Plugin-Installation, kein Live-GO.

## Korrektur der früheren falschen Aussage
Die frühere Aussage „es liegen nur die drei Artikel, aber keine WordPress-Quellen vor“ war **falsch**. Die originale Datei **pste-plan-kategorien-pruefstand-2026-11-09.json** ist im Projekt/Library tatsächlich vorhanden, 11.925.212 Bytes, erstellt 2026-11-09 12:22:45 UTC, aus PSTE 0.57.144.27. Sie enthält:
- Original `PSTE_SITE_BASELINE_V1` vom 26.10.2026, 1.176 Kategorien, 1.165 Produktions-Endkategorien; 144 veröffentlichte und 19 Entwurfsartikel.
- Echten Kontext-Auffrischungslauf: `PSTE_CONTEXT_REFRESH_JOB_V9_EQUIVALENT_STRUCTURE_RESUME`, `status=COMPLETE`, 4.488/4.488 Einheiten.
- Echte archivierte Planbindung `editorial_plan_sha256=3986590a30c65c0e749ceec027e5ebdb6f04128f577d1ec32dc89351083c74a0`, Kontextmanifest + Exportmetadaten. Historisch 9 leere Alt-Planhalter, im Original ausdrücklich `NOT_AVAILABLE`.
- Diese Datei ist **eine datierte frühere Bestandsaufnahme** und enthält nicht allein den *aktuellen* 11.11.2026-MySQL-Tabellenzustand.

Zusätzlich physisch vorhanden ist der echte spätere PSERC-Dreierexport, 90.640 Bytes, SHA256 `29638fef9606925b5b6f322fcde695581999ec0c41bd111bca0bcb655fbf1220`: drei bereits freigegebene Regendecken-Artikel und originalsignierte `PRE_TYPE`-Daten mit `primary_user_goal=INFORMATIONAL_FOCUS`.

Die Projektdatei wurde per bestehender Dateien-Suche/Lesefunktion inhaltlich verifiziert. Das direkte Kopieren ihrer 11,9 MB Originalbytes in die lokale Testlaufzeit wurde durch die Projekt-Dateiberechtigung nicht zugelassen. **Deshalb wurde nicht vorgetäuscht, alle 5.016 WordPress-Themenzeilen lokal geöffnet/neu verarbeitet zu haben.** Kein Grund für eine neue Benutzerdatei-Anforderung.

## Original-PHP und Testfehler hart geprüft
Physisch geöffnet und ausgeführt: `PSTE_Breadth_Research_Queue`, `PSTE_Intent_Profile` aus PSTE QA-Paket .57.144.35; `PSTE_Repository::reanalyzeRetainedBacklogBatch` tatsächlich gelesen (Original-Quelldatei). Die echte Klasse prüft:
- signierten vorherigen Abschlussbeleg und Checkpoint vor Bestandswiederanlauf;
- veränderte Normalweglogik, ohne bei nur geänderten Regeln neuen DataForSEO-Aufruf zuzulassen;
- Bestand in begrenzten Paketen, Fortschritt nach Neustart, Gültigkeit der neuen Abschlussquittung.

Die originale Repository-Funktion ist im Lauf **ersetzt durch eine ausdrücklich simulierte persistierende WordPress-Thementabelle** mit drei realen Profildatensätzen, nicht durch reales MySQL.

**Während dieser QA wurde ein REINER TESTFIXTURE-FEHLER gefunden:** Das selbst gebaute JSON-Dateispeichern verwandelte originale Gleitkommazahlen `0.0` in `0`. Damit wurde der originale `analysis_sha256` der zweiten/dritten Zeile beim späteren Lesen ungültig; der Worker stoppte richtig mit `ORIGINAL_PROVENANCE_INVALID`. Die Fixture wurde auf `JSON_PRESERVE_ZERO_FRACTION` gestellt. Der echte PSTE-Repository-Schreibweg benutzt bereits `wp_json_encode(... JSON_PRESERVE_ZERO_FRACTION)` in `encodeJsonValue`; dieser QA-Fehler ist **kein nachgewiesener Produktfehler**.

## Reproduzierbarer kompletter isolierter Wiederanlauf
**25 vollständig unabhängige positive Läufe**, je eigene persistente Zustandsdatei und separater PHP-Start für `init`, `step`, `step`, `step`, `inspect`.
- Vorher: drei PRE_TYPE-Zeilen exakt nach echter Benutzerdatei und unverändert signiert.
- Nachher: `PSTE_Breadth_Research_Queue` STATUS COMPLETE; `existingOnlyAuditCurrent()` true; 3/3 gespeicherte Themen zu `BOUND_TYPE/PASS`, alle originalen `INFORMATIONAL_FOCUS` übernommen, alle drei finale Profil-Hashes mit originaler privater Hashfunktion verifiziert.
- Nochmaliges Lesen der Zustanddatei nach Neustart erfolgreich, 0 Provideraufrufe, keine neuen Artikel/WordPress-Beiträge.

**75 zusätzliche unabhängige Negativfälle**: 25 manipulierte Checkpoint-Quittungen und 25 manipulierte Abschluss-Quittungen jeweils vor Start BLOCK, 25 versuchte Provideraufrufe nach Start mit `PSTE_RECHECK_PROVIDER_CALL_FORBIDDEN` PAUSED_ERROR. Bei den beiden ersten 0 Repo-Schreibversuche, beim dritten 0 Repo-Schreibversuche und 0 echte Provideraufrufe.

Maschinenlesbarer QA-Report lokal: `/mnt/data/psqa/true_queue_replay/replay_report.json`; Test-Runner `run_matrix.py`; PHP-Replay `queue_replay.php`. Alle sind offline; keine Installation erforderlich.

## Verbindliche, ehrlich verbleibende Grenze
Das beweist den **originalen Warteschlangen-Wiederanlauf, signierten Abschluss und die drei originalen Intentprofile** bei einer persistenten lokalen Zustandsnachbildung. Es beweist **nicht**: voller Original-`PSTE_Repository::reanalyzeRetainedBacklogBatch` mit MySQL/WordPress, 5.016 gespeicherte Themen aus der laufenden WordPress-Datenbank, echte Persistenz auf der Test-WordPress-Seite, ein neues echtes PSERC-`mit-suchintent-nachweis`-Manifest oder einen frisch erzeugten K0-Text aus diesem neuen Manifest. Bestehender K0-Writer-/Text-Output aus historischem realem Artikel wurde separat zuvor bestätigt; K0 bleibt unangetastet.

**Freigabe:** NO RELEASE, NO INSTALLATION REQUEST, NO DATAFORSEO API, NO K0 CHANGE. Der reale Fehlerbericht ist weiterhin offener WP/MySQL-Test, nicht ein weiterer blind zu installierender Pluginstand.
