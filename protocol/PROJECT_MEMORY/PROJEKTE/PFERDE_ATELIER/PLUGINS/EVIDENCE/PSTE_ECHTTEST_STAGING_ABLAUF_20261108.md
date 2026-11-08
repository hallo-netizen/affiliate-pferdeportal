# ECHTTEST – Einmaliger WP→SEO-Owner→PSTE→PSERC-K0-Grenze, 08.11.2026

**Status:** Vorbereitung vollständig, **noch nicht durchgeführt**. Nur WordPress-**TEST**; kein Live-Update. K0 und der gespeicherte Redaktionsplan bleiben unverändert. Genau **ein** externer SEO-Owner; keine doppelte semantische WordPress-/PSERC-Prüfung. Verbindliche Quellen liegen im selben Pferdeatelier-Plugin-Büro.

## A. Vorbereiteter Testeingang (noch nicht verfügbar)

Einmalig aus der vorhandenen Test-WordPress-Instanz (`oliver-beil.de`, tatsächliche Version vorher im Backend ablesen, **nicht raten**) die originale unveränderte Datei über den bereits vorgesehenen MINI-Befehl **„Redaktionsstand für einmalige SEO-Prüfung exportieren“** sichern. Dieser Befehl ist **aktuell nur im isolierten QA-Code enthalten; seine Installation auf der Testseite ist hier nicht nachgewiesen**. Vor jeder kontrollierten Testinstallation beide Original-Plugins/Versionen und Datenbank sichern, nicht das produktive Pferdeatelier anfassen.

Die Datei muss im aktuellen Teststand folgende beiden Teile enthalten:

- **Echte aktuelle Kandidaten**: `seo_subjects[]` aus WordPress mit Original-`pool_key`, `raw_query`, `source_sha256`; zu jedem vorhandener JA-Titel unter `items[]`.
- **Echter aktueller Bestand**: `parkhaus_snapshot` aus WP-Artikel/Seiten/Rassen/Glossar, PSTE-Poolplänen, optionalem PSTE-Redaktionsplan, dem **gesamten** aktiven PSERC-Plan samt HELD sowie dem **schon gespeicherten PPM679-Redaktionsplan** und MINI-Reservierungen. Keine 1.200er-Abkürzung, keine reine Frontend-Sitemap als Ersatz, keine alte synthetische 100er-Liste als vollständiger Plan.

**Prüfbedingung:** `parkhaus_complete=true`, `complete=true`, gesicherter vorhandener PPM679-Plan **vorhanden und nicht leer**, echte WP-Inhalte vorhanden, keine fehlenden/wechselnden Quellidentitäten. Bei unvollständiger/fehlender Datenbasis **STOP**, keine Freigabe.

**Bereitliegender einmaliger Quelltest:**

```bash
D=protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/PLUGINS/QA_ONLY
python3 "$D/test_single_existing_seo_worker_acceptance.py" --preflight ORIGINAL_WORDPRESS_EXPORT.json
```

`REAL_WORDPRESS_EXPORT TECHNICALLY_COMPLETE` zeigt **nur**, dass alle notwendigen Quellen technisch vorhanden sind, nicht dass der SEO-Owner recht hat.

## B. Genau ein externer SEO-Entscheider, echte Abnahme

Dem bereits vorgesehenen **einen** externen SEO-Owner **dieselbe gesamte originale exportierte Datei** plus den [genauen Arbeitsauftrag](PSTE_EIN_SEO_OWNER_ECHTTEST_AUFTRAG_20261108.md) geben. Er entscheidet die Suchabsicht **einmal** für alle im Export enthaltenen JA-Kandidaten. Er gibt die Datei `ECHTE_OWNER_ANTWORT.json` im unveränderten `PSTE_MINI_SEO_DECISIONS_V1`-Format zurück – kein zweiter Owner, kein neues Import-Plugin. Während der Arbeit keine WordPress-Planänderungen freigeben.

Einmalige fachliche Abnahme seines Werks anhand der Originaldaten und der bereits bekannten kritischen Themen (vgl. Arbeitsauftrag). Antworten mit „FREI“ für gleichbedeutende Regendecken-Longtails, ohne nachweisbar andere Suchfrage, werden **nicht** akzeptiert. Bei „BELEGT“ muss tatsächlich ein vorhandener Quellverweis genannt werden. Ungeklärtes bleibt **KLÄRUNG**. Die Titelwerkstatt prüft **nur Titel/Deutsch**, nicht die bereits einmalige SEO-Belegungsentscheidung.

**Vor Rückimport einmaliger Abnahme-/Quellentest:**

```bash
D=protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/PLUGINS/QA_ONLY
python3 "$D/test_single_existing_seo_worker_acceptance.py" --verify \
  ORIGINAL_WORDPRESS_EXPORT.json \
  ECHTE_OWNER_ANTWORT.json \
  "$D/MINI_100_ORIGINAL_EXTERNAL_TITLES_20261106.json"
```

**Wichtig:** Die optionale Original-100-Datei nur dann als vollständig nachgewiesene Staging-Testmenge einschließen, wenn die **echten 87 JA** in `seo_subjects` tatsächlich vorhanden sind. Ist das nicht der Fall, **keine erfundenen WP-ID-Zuordnungen herstellen**: zuerst echte Testdaten/Versionen klären. Der Abnahmetest ist **einmalig vor dem realen Lauf**, keine erneute SEO-Dauerprüfung in WordPress.

## C. Kontrollierter *TEST*-Rückweg

**Erst wenn A+B PASS und eine installierbare, gesondert geprüfte QA-Paarversion der zwei bestehenden WordPress-Plugins bereitsteht:**

1. Original-Export und echte Antwort **unverändert** neben dem vorhandenen Plugin-Büro-Nachweis sichern. Backup der TEST-WordPress-Datenbank und der bisherigen zwei Plugin-ZIPs bestätigt. Keine anderen Plugins installieren.
2. Im **bereits existierenden** MINI-Titelkorrektur-Import die externe SEO-Antwort importieren. WordPress prüft nur Quellen-/Versionstreue und wirklich belegte Artikelplätze. Einzelne defekte/unklare Antworten bleiben in **KLÄRUNG**, die übrigen gültigen bleiben erhalten.
3. Den **vorhandenen** `forwardToPlan`-Weg auslösen. Ein `FREI` darf ohne bestätigte bisherige `plan_forwarded` und `plan_queued`-Checkpoint **keine** WordPress-Planfreigabe erhalten. `BELEGT` und `KLÄRUNG` dürfen nicht als Artikel ankommen.
4. Den **vorhandenen** PSERC-Planleser und Compiler **nur kontrolliert im Test** ausführen. Nur technisch fertige Metadaten in genau fünf Feldern: `title`, `target_keyword`, `category`, `article_type`, `plan_slot`. Gespeicherte Planung darf nicht ungefragt überschrieben werden. Keine Artikelproduktion starten; K0 selbst bleibt unangetastet.
5. Proben im **tatsächlichen** TEST-WordPress gegen vorhandene Artikel-/Planplätze: a) einmal FREI und wirklich neu; b) nachträglich belegter Slot (muss sperren); c) falsche Quell-ID (nur eigener Fall sperrt); d) BELEGT und KLÄRUNG bleiben draußen; e) abgestandener Plan führt zu Halt. Der echte Lauf muss seine Ergebnisse aus tatsächlicher WP-/PSERC-DB protokollieren, nicht nur aus unseren bisherigen Mock-Tests.

## Beweisgrenzen

- **Bereits PASS:** Zwei QA-Skripte in einer bestehenden MINI-Klasse/Abnahmedatei, originaler 100er-Datensatz, WordPress-/Plan-Slotkollisionen, atomare Übernahme, bestätigter vorhandener Plantransfer und separate PSERC-Grenzproben (siehe `CURRENT_STATE.md`). Einmaliger technischer Export-/Owner-Datei-Selbsttest mit **8 gezielt erzeugten Fehlerfällen**, GitHub Actions `42464305128` PASS. Die Original-PSTE-Methoden direkt im unmodifizierten ZIP nachgewiesen, GitHub Actions `42464065463` PASS.
- **Nicht PASS:** Echte komplette WordPress-Staging-Exportdatei, echte Auswertung durch den externen SEO-Owner, tatsächlicher Rückimport in TEST-WordPress, voller PSERC-Quell- und K0-Grenztest **mit echten Daten**, aktuell grüne unveränderliche Sicherheitsprüfung. Kein Merge/Installer/Live-Freigabe.
- **Bestehende immutable GitHub-Hardlock-Workflow-Prüfung meldete in isolierter QA wiederholt FAILURE**, obwohl der abschließende PR-Vergleich keine `.github/`, `control/` oder Original-ZIP-Änderungen zeigt. Ursache nicht durch Umgehung oder Sicherheitsdateiänderungen kaschieren. Vor jeder späteren Freigabe separat belastbar klären.

## Minimaler nächster echter Input

**Ein vollständiger, unveränderter Export aus dem wirklichen WordPress-TEST-System.** Ohne ihn ist der fachliche SEO-Owner-Lauf nicht reproduzierbar. Falls die bestehende QA-Exportfunktion dort noch nicht installiert ist, sind zuerst genau die zwei vorhandenen Testplugins als **ein einziges überprüftes Paar** fertigzustellen und separat freizugeben – nicht irgendein Zwischenfix installieren.

**Stoppregel:** Wenn irgendein echter Quellbeleg fehlt oder die Hardware/Version/Staging-Hardlock-Bedingungen nicht nachgewiesen sind, heißt das Ergebnis **TEST NICHT FREIGEGEBEN**, nicht „angenommen“.
