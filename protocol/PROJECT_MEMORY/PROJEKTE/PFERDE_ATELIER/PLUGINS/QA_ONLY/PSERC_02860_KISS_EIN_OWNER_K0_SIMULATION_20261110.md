# PSERC 0.28.60 – KISS: ein externer SEO-Owner, alter Doppelprüfer nur für Legacy

**Datum:** 10.11.2026. **Status:** Lokale Original-PHP-Gegenproben und Test-ZIP PASS; **kein WordPress-E2E-PASS**. `FULL_WORKFLOW_PASSED=false`. K0 und gespeicherte Originaldaten unverändert.

## Reale Ausgangslage
Auf der Benutzer-Testseite mit PSERC 0.28.59: aktueller aktiver Snapshot PASS; 5016 Themen, 8 geeignet, 5008 zurückgehalten, 0 READY; alle acht als `BLOCKED_PORTAL_TOPIC_EVIDENCE` markiert. Das ist ein sicherer Stop; damit wird keine fertige K0-Datei behauptet.

**Tatsächliche Originalcode-Ursache:** Der bestehende `PSERC_SEO_Reader::normalizeCandidate()` prüft den gebundenen EINZIGEN externen MINI-SEO-Entscheid und gibt `single_external_seo_owner_receipt` an den bestehenden PSERC-Compiler weiter. Dieser überspringt bereits seine zweite semantische Dublettenbewertung. Aber `PSERC_Portal_Topic_Evidence_Gate::evaluate()` verlangt **weiterhin** das alte vollständige Longtail-Recherche-/Semantic-Consensus-/Titel-Gate, **unabhängig vom gültigen externen Entscheid**. Die 0.28.59 Originalklasse wurde mit sieben **tatsächlich extern als FREI geprüften** Titel/Keyword-Paaren (private Original-100er-Datei) direkt ausgeführt und blockiert **7/7** vor Abschluss mit `PORTAL_TOPIC_RESEARCH_JOB_CONTRACT_INVALID`.

**Wichtige Abgrenzung:** Der Screenshot liefert nicht die 8 tatsächlichen Kandidaten-JSONs und deren detaillierte, gespeicherte Gate-Gründe. Deshalb nicht behaupten, dass alle 8 bereits einen validen/weitergegebenen externen Receipt besitzen oder dass die Korrektur in WordPress zwingend 8 READY erzeugt.

## Minimaler KISS-Fix (0.28.60)
Aus **der echten .59-ZIP**, 63/63 unveränderte Dateipfade:
1. `includes/class-pserc-portal-topic-evidence-gate.php`: **vor** dem unveränderten alten Legacy-Prüfweg ein Quellen-verifizierter Pfad für genau ein bereits extern freigegebenes Thema. Der ursprüngliche `PSTE_Mini_Workflow::singleOwnerSeoFor(pool_key, raw_query, true)` prüft **technisch** Quell-/Titelbindung und die **vorhandenen plan_forwarded/plan_queued Checkpoints**, **ohne** eine neue SEO-Fachentscheidung. Kein blindes Vertrauen auf bloß `receipt` im Request. Mit gültiger, weitergegebener Freigabe keine zweite Longtail-, Semantik- oder Titelentscheidung. Kontext, Entscheidstatus, fünf K0-Felder, echte Kategorie, Artikeltyp und bisherige harten Sicherheitsgründe werden weiterhin gesperrt, falls ungültig. **Ohne externen Nachweis bleibt der komplette alte Code bytegleich erhalten.**
2. `includes/class-pserc-admin.php`: statt einer neuen Seite nur die vorhandenen aufklappbaren **„Technische Bindungen anzeigen“** um maximal 25 bereits gespeicherte, aus dem **aktiven Snapshot** rein lesend abgerufene `BLOCKED_PORTAL_TOPIC_EVIDENCE`-Einzelfälle und deren Original-`production_reason_codes` erweitern. Nicht ins Frontend, keine zusätzlichen Datenfelder oder Speicher. Damit sind die acht aktuellen Gründe nach dem Test sichtbar, auch wenn 0 READY verbleibt.
3. Hauptversionsdatei und **vorhandenes** Integritätsmanifest neu gebunden. Keine weitere Datei, kein neuer Worker, keine Datenbank-/Options-/Migrationsänderung. **59 der 63 ZIP-Dateien bytegleich mit .59.** PSERC-Export `exportLivePreview`, Compiler-Finalizer und `PSERC_Metadata_Boundary` **unverändert**, K0/PPM/PSTE/LIVE unberührt.

## Tatsächlich ausgeführte Originalcode-Tests
- **7/7** echte Original-FREI-Datensätze: erst vom unveränderten `PSERC_SEO_Reader::normalizeCandidate` mit originaler Quellidentitätsprüfung gebunden, danach vom neuen vorhandenen Gate akzeptiert; der alte Gate blockiert dieselben 7 (negative Regression bestätigt).
- **13 gezielte Negativfälle**: nicht vorwärtsgegebener Entscheid (vorhandener `plan_forwarded`/ `plan_queued`-Checkpoint), manipulierter Titel, Quell-Hash, Intent-Slot, veralteter Kontext, fehlende Kategorie, falsche Rolle, falsche K0-Metadaten, harte Sicherheitssperre, offener Kategorie-Vorschlag, fehlender PASS sowie BELEGT-Verfälschung. Alle korrekt blockiert.
- **5 Legacy-Vergleiche**: die bisherige Original-.59-Klasse und die neue .60-Klasse liefern ohne echten externen Nachweis exakt dieselben Antworten.
- **Originaler Compiler-Finalizer** `PSERC_Compiler::finalizeAllocationRow` wurde für die 7 freigegebenen Originalthemen mit **synthetischen, explizit nur QA-canonical_article_ids** aufgerufen: **7/7 READY** und korrekter Domain-hashgebundener Plan-Slot. Dies ist NICHT der echte WordPress/PPM-Planplatz.
- **Bestehende, unveränderte K0-Vertragsprüfung** `PSERC_Metadata_Boundary::validateBatch`: zusammengefasste 7er-JSON strukturell **PASS**; hinzugefügter Artikeltext **BLOCKED**, leere Produktionsdatei **BLOCKED**. Keine echten K0-Artikel erstellt.
- **Vorhandene PSERC-Admin-PHP-Funktion** mit 8 synthetischen, bereits gespeicherten BLOCKED-Datensätzen ausgeführt: genau acht Einzeldiagnosen im vorhandenen eingeklappten Expertenabschnitt, bisherige Oberfläche und Exportfunktion erhalten.
- **Paket:** 43/43 PHP-Lints PASS, Original `PSERC_Package_Integrity::validate()` **61/61** gebundene Dateien PASS, ZIP-CRC und exakter ZIP-Inhalt/Pfadvergleich **63/63 PASS**, nur vier bestehende Dateien geändert.

## Binärstand / Freigabe
Private Test-ZIP: `/pferdeatelier/PLUGINS/QA/PSERC-0.28.60-KISS-EXTERNER-SEO-OWNER-NUR-TEST.zip`.
SHA256: `c9c7e90b265e650739d2568a7cb807238db7f081ddcf7d8698fe64961b84f22a`.
Kein Merge, keine WordPress-Installation durch den Assistenten, keine Änderung vorhandener Daten. PR #682 bleibt DRAFT.

**EIN erforderlicher WordPress-TEST-Lauf, bevor K0-E2E belegt ist:** .59-TEST sichern, auf TEST .60 aktualisieren, bestehenden Snapshot **einmal** laufen lassen. Falls READY>=1: vorhandenen „Kompakten Produktions-Handoff als JSON herunterladen“ benutzen und Datei gegen den originalen K0-Eingangsvertrag prüfen. Falls READY=0: im **bereits vorhandenen** Abschnitt „Technische Bindungen anzeigen“ die 8 konkreten `blocked_topic_details` ablesen. Keine erneute Keyword-Recherche, keine 5016er Neuentscheidung, keine Live-Installation. Die 8 aktuellen gespeicherten Einzelfälle sind nicht im vorliegenden Chat verfügbar.

**Verschlankung:** Für neue extern geprüfte und weitergegebene Fälle entfällt zur Laufzeit die alte zweite fachliche Komplettprüfung. Keine Funktionen/Altbestände gelöscht; reine Codeentfernung erst nach nachgewiesenen Referenzen und bestandenem echten K0-Endtest. 
