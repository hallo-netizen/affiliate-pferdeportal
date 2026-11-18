# Pferdeatelier – Texterstellung KISS: Original-Platzvergabe angebunden, QA 14.11.2026

**Status: NUR QA, nicht installieren, kein Live-Eingriff.** Verbindlicher Betreiber-Zielvertrag bleibt [TEXTERSTELLUNG_KISS_ENDGUELTIGER_WORKFLOW_20261114.md](TEXTERSTELLUNG_KISS_ENDGUELTIGER_WORKFLOW_20261114.md). Dies ist eine technische Fortsetzung der vorhandenen Quelle, kein neuer Plan/Worker oder Entwicklungsneubau.

## Konkret geändert (ein bestehender PHP-Bestand)
- Die bereits in PSERC vorhandene, unveränderte `PSERC_Slot_Allocator::allocate()` vergibt nach dem EINEN fertigen MINI-Entscheid den originalen kanonischen Platz in der **bestehenden** WordPress-Texterstellung-Auftragsliste. Die Kategorie, Artikelart, Absicht und der Titel werden dabei **nicht** nochmal fachlich entschieden.
- Die bestehende `PSERC_Production_Reader::snapshot()` verlangt den originalen signierten PPM-6.7.9-Plan; lokal erfundene TXE-IDs bleiben gesperrt.
- Bei vorübergehend fehlender PPM-Kapazität/Reader bleibt das MINI-Ergebnis **dauerhaft** gespeichert. Beim **bereits vorhandenen** K0-Export wird NUR die fehlende technische Buchung mit dem selben ursprünglichen Ergebnis erneut versucht. Keine neue externe MINI-Runde und keine alte Freigabe revidieren.
- Originale PSTE-/PSERC-/PPM-/K0-Dateien nicht geändert. Keine neuen Datenbanktabellen oder Entscheidungen. Der ursprüngliche PSERC-Fünffelder-K0-Export wird unverändert aufgerufen. WP-Autolock und Schreib-Readback bleiben erhalten.
- Bei gleichzeitigen technischen Buchungen im selben Texterstellungsregal werden bereits dort reservierte Originalplätze ausgenommen. Vor Übergabe an K0 werden unverändert die originalen Kategorie-/Artikelart-/PPM-Platzbelege und die gespeicherte MINI-Eigentümerschaft technisch zugeordnet.
- Die 61 früheren FREI-Entscheidungen bleiben eingefroren; keine nachträgliche Titel-/SEO-Beurteilung. Redaktionsbüro ist ein regulärer Sammelweg, keine zusätzliche Sperrkategorie.

## Nachweisbar ausgeführte Tests
- **56/56** lokale Gegenproben PASS: 13 ursprüngliche Original-PPM-Blockaden, 14 Wiederaufnahme/Abbruch mit 87 Originalentscheidungen und 1.179 historischen WP/PPM-Bestandszeilen, 11 Alttitel-/FREI-Gegenproben (61 Originalthemen), 6 Original-144er-PPM-Archivbefunde, **12 neue** Original-Platzvergabefunktions-/K0-Fünffelder-/Checkpoint-Tests.
- **117/117 PHP-Syntax** PASS.
- Der 12er-Neutest hat `PSERC_Slot_Allocator::allocate()` tatsächlich aufgerufen; *signierter Plan-Leser* und *WordPress-Datenbank* wurden für die lokale Ausführung nachgebildet. Dort erhielten 3 unterschiedliche MINI-FREI-Aufträge 3 unterschiedliche unveränderte originale PSERC-Identitäten. Abbruch nach 2 persistierten Entscheidungen; Neustart ohne erneutes Durchlaufen der 2 bereits abgeschlossenen Entscheidungen; K0-Fünffelder-Paket, identischer Re-Download und Abweisung eines manipulierten Owner-Checkpoints geprüft.
- Test-/Releasegrenze: keine echte laufende WordPress-Testinstallation/PPM-6.7.9-Signatur und kein externer KI-Worker angesteuert. **Ein lokaler Integrations-PASS ist KEIN echter WordPress-/K0-Endlauf.**

## Dauerhaftes Artefakt im schon bestehenden Campus-Büro
`/pferdeatelier/PLUGINS/ARBEITSRAUM_PSTE_KISS/TEXTERSTELLUNG_KISS_20261114_ORIGINAL_PLATZWEG_QA_NICHT_INSTALLIEREN.zip`
- SHA-256: `e6943143a4e2d26a450aa0cb009c10e51b6d0be60c675ca906af30de633ea9b2`; nach privatem Library-Upload erneut materialisiert und **byteidentisch zurückgelesen**; ZIP-CRC gültig, 177 Einträge; alle unter `QA_ONLY/`, `QA_REPORT/`, `QA_TESTS/` – kein WP-Installer.
- Voller lesbarer Bericht: `TEXTERSTELLUNG_KISS_20261114_ORIGINAL_PLATZWEG_QA_BERICHT.md` im selben Library-Arbeitsraum. Keine privaten 87 Originalkeywords in öffentliches GitHub-Dokument kopiert.

## Unverändert offene Pflichtabnahmen
1. Echte Original-PPM-6.7.9-Planlese/Original-Reservierung und Belegung auf einer **verbundenen isolierten WordPress-Testinstallation**.
2. Echte externe GitHub-MINI-Teilworker **inklusive Interrupt nach jedem Worker-Checkpoint**, kein freier KI-Umweg, Titelreparatur ohne zusätzliche Entscheider.
3. End-to-End MINI → WordPress-Sicherung → K0-Text → WordPress-Entwurf mit echtem Abbruch/Wiederanlauf.
4. Vollständige 0.4.5-WIP-Original-ZIP war bisher nicht byteidentisch verfügbar; diese QA baut auf der gesicherten 0.4.3-Originalzip + 0.4.5-WIP-Quelldateien auf.

**NEXT ACTION:** Vorhandenen WordPress-Teststand wirklich anbinden, auslesen und die drei E2E-Stufen mit Absicht unterbrechen. Kein neues Plugin/Produktivpaket vorher. `release_allowed=false`.
