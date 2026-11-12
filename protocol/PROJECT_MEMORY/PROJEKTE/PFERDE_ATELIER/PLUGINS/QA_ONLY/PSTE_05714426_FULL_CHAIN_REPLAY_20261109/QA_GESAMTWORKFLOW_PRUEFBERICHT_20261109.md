# Pferdeatelier – lokaler Gesamtketten-Replay · 09.11.2026

## Ergebnis in einem Satz
**GESAMT-WORKFLOW: NICHT FREIGEGEBEN.** Die originalen WordPress-Daten beweisen eine Blockade vor der fachlichen Neuprüfung; nach lokaler Korrektur wird der Fehler sicher angehalten statt als fertig gezählt. Es gibt **keinen echten End-to-End-PASS auf WordPress/MySQL** und **keine Plan-/PSERC-/K0-Freigabe**.

## Originale aus dem echten WordPress-Teststand
- PSTE .26 ZIP, originaler MINI-Export 09.11.2026 07:48 UTC, externe 87er SEO-JSON, Betreiber-Stapelbericht vom 09.11.2026 09:22 UTC.
- MINI: 100 Rohfragen; 87 JA-Themen.
- SEO: 61 FREI, 20 BELEGT, 6 KLÄRUNG; alle 61 freigegebenen Intent-Slots eindeutig und disjunkt zu den 144 reservierten PPM679-Plan-Slots.
- Parkhaus: 1179 Datensätze, 144/144 technische PPM-Reservierungen, 141 echte WordPress-Titel, 3 historisch reservierte Post-IDs; neun inhaltslose alte Importplatzhalter weiterhin in der Herkunft enthalten.
- Echter Bericht: 61/61 abgearbeitet gemeldet, 61 zurückgestellt; 60 mal `PSTE_RETAINED_EDITORIAL_PLAN_SNAPSHOT_CHANGED`, 1 mal manuelle Sperre. Dokumentierte sekundäre Alt-Gates: 48 Titel-/Kategorieentscheidungen, 7 Intent-Überschneidungen, 4 Typkandidaten fehlen, 1 rein kommerzieller Suchbegriff, 1 Portalstruktur-Lücke.
- **Wichtig:** Die 48 stammen aus älteren gespeicherten Prüfungen; sie sind nicht 48 neue Kategorieablehnungen. Die 61 im Stapelbericht leeren `keyword`-Anzeigen belegen keinen Suchbegriffsverlust: 61/61 Original-Suchbegriffe sind in der MINI-Ursprungsdatei vorhanden.

## Mit dem echten PHP-Programmcode ausgeführte Kette
1. **Quelle/SEO:** Die echte `PSTE_Mini_Workflow::acceptSingleOwnerSeoDecisions` übernimmt alle 87 Originalentscheidungen korrekt (61/20/6).
2. **Preflight:** Die echte `planHandoffPreflight` validiert 61 eindeutige freie Originaltitel und die eindeutige Original-Fragenbindung.
3. **Titel-Speicherung:** Die echte `PSTE_Repository::saveManualTitleOverride` speichert alle 61 Titel in simulierten PSTE-eigenen Transaktions-Tabellen. Zweiter Durchlauf erkennt 61 mal identische Titel ohne Duplikate. Keine Produktionsfreigabe, keine Änderung der Originalfrage oder der reservierten Slots.
4. **Plan-Kontext:** Die echte `PSTE_Snapshot::editorialPlan` erkennt die neun alten `Array`-Platzhalter als semantisch leeren Altplan. Der originale `PSTE_Repository::reanalyzeRetainedBacklogBatch` wirft bei einer bewusst kontrolliert veralteten Planbindung exakt `PSTE_RETAINED_EDITORIAL_PLAN_SNAPSHOT_CHANGED`. **Die aktuelle tatsächliche WordPress-Planbindungs-Prüfsumme ist nicht exportiert; der genaue Grund der Drift auf dem Server ist damit nicht bewiesen.**
5. **Warteschlange:** Das reale PSTE-.26-Programm markiert 60 dieser globalen Planabbruchfehler plus 1 echten manuellen Stopp als `61 erledigt, 61 gesperrt, 0 offen`, statt den gemeinsamen Vorbedingungsfehler zu pausieren. Exakt das beobachtete WordPress-Fehlerbild ist lokal reproduziert.
6. **Sicherer Gegenlauf:** Der isolierte QA-Patch klassifiziert diese globale Planabweichung als gemeinsamen technischen Fehler und pausiert: 0 abgearbeitet, 61 noch offen. Ein erneuter planidentischer Versuch erhält weiterhin exakt die 61 Quellen und legt nichts doppelt an. **Kein Ersatz für das erforderliche korrekte WordPress-Kontext-Update.**
7. **Nachfolgende Kategorie-/PSERC-/K0-Kette:** **NICHT FREIGEGEBEN.** Ein Test mit passend gemachter künstlicher Plan-Prüfsumme geht über den vorherigen technischen Abbruch hinaus, stößt dann aber an fehlende echte WordPress-Taxonomie- und Baseline-Daten im Export; er darf keine fachlichen PASS-Werte vortäuschen. Kein PSERC-Redaktionsplan und keine K0-Artikel wurden lokal oder produktiv verändert.

## Messbare QA
- PSTE .26 Original: **18/18** lokaler Replay-Prüfungen PASS, darunter die exakte Reproduktion des beobachteten Fehlverhaltens.
- Isolierte geänderte Admin-Fassung: **20/20** PASS, einschließlich sicherer Pause, idempotentem Resume und gleichbleibenden 61 Quellen.
- PSTE-.26-Original: **83/83 PHP-Dateien Syntax PASS**, **121/121 ZIP-Einträge CRC PASS**, sechs bekannte atomare Import-Negativ-/Positivtests PASS. Das beweist **nicht** WordPress-MySQL-End-to-End.
- Die lokal simulierte DB ist eine wohldefinierte In-Memory-WordPress-Attrappe. **Keine aktuelle echte WP-Datenbank, 1.177 WordPress-Kategorien/Seitenstruktur, globaler Baseline-Snapshot oder vollständiger PSERC-Compiler im selben Lauf.**

## Konsequenz / Reihenfolge
1. Keine weitere WordPress-Aktion, kein neuer Import, kein K0-Auftrag.
2. In PSTE die globale Hashabweichung vor der individuellen Titel-/Kategorieprüfung sicher pausieren und im UI wahrheitsgemäß zeigen. Diese minimale Korrektur ist nur **QA**, noch kein Installationspaket.
3. Vor einer Freigabe muss der gebundene WordPress-Plan-/Kontextstand auf der isolierten Testseite mit den aktuellen Ausgangsdaten übereinstimmen, ohne den Schutz der 144 Slots aufzuweichen. Anschließend die 61 Themen erneut **durch die echten Fachprüfungen**, einschließlich gleicher Bedeutung, allen existierenden Magazin- und Hauptkategorien, Kategorie-Neuanlage nur auf belegter Grundlage und PSERC-Handoff, laufen lassen.
4. Erst wenn ein echter WP/MySQL-Endtest grün ist, eine aktualisierte Installation anbieten. Der vorhandene QA-Patch bleibt getrennt. K0, Main, Live, PSERC und 144 Reservierungen nicht ändern.