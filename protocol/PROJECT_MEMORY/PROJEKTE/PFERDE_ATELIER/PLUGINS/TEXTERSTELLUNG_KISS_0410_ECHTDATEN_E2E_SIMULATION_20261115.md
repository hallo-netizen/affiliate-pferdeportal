# 15.11.2026 – Texterstellung KISS 0.4.10: echte Nutzerdaten, lokaler Gesamtlauftest

**STATUS:** installierbare ZIP ausschließlich für isoliertes WordPress-Testsystem oliver-beil.de. Der echte WP-/MySQL-Test sowie externe K0-Texterstellung wurden NOCH NICHT durchgeführt. Keine Live-Freigabe. Alte Versionen 0.4.8 und 0.4.9 sind zurückgezogen.

## Tatsächlicher Ausgangsfehler
Echte WordPress-Diagnose von oliver-beil.de, `texterstellung-diagnose-20261115-105041.json`, Version 0.4.9: 61 reale Alt-Freigaben (1 FREI, 60 METADATEN_OFFEN); 20 CATEGORY-Entscheidungen tatsächlich um 10:44:44 UTC als `MINI_WORKER_CHECKPOINT_SAVED` importiert, 0 Fehler. Gegen 10:50 UTC `txe_export` => `NO_ORIGINAL_PPM679_BOOKED_ARTICLES`, keine K0-Charge. Es gab KEINEN zweiten echten FINAL-MINI-Import. Frühere behauptete vollständige Prüfung war falsch: vorherige 105 Tests simulierten alte signierte PPM-Plätze und übersahen zwei vertraglich falsche Abhängigkeiten.

## Nachgewiesene KISS-Korrektur
1. LEGACY_CATEGORY_ONLY mit vorher bereits freigegebenem Titel, Inhaltsthema und SEO braucht nur die EINMALIGE CATEGORY-Entscheidung. Sobald CATEGORY-Checkpoint persistent `DONE` ist, erfolgt technische K0-Buchung im gleichen EINEN WordPress-Regal, ohne zweiten Upload/FINAL-Import.
2. Die bereits in 0.4.9 persistent gespeicherten 20 CATEGORY-Checkpoints werden beim nächsten `txe_export` automatisch fertiggestellt. Nichts erneut einlesen oder recherchieren; alle 61 originalen Titel byteidentisch.
3. Technische K0-Identität und 64-stelliger plan_slot einmalig und deterministisch aus der originalen WordPress-Auftrags-ID. Keine zweite redaktionelle Plan-/SEO-Entscheidung. Schutz gegen bereits im eingefrorenen WP-Inventar belegten Slot und gegen andere reservierte Identitäten im zentralen WP-Regal.
4. Historischer PPM-6.7.9-Plan/PSERC_Production_Reader, alter Slotallocator, Artikeltyp-Registry und drei alte Vertragsdateien PHYSISCH aus Plugin entfernt. 0.4.9 96 Dateien, 0.4.10 90 Dateien, 81 PHP. Nur die für K0-Fünffelder-Vertrag und ursprünglichen WordPress-Entwurfsimport weiterhin nötige Technik behalten.
5. Der alte Original-Entwurfsimport (`PSERC_System4_Import`) bleibt nur als WordPress-DRAFT-Schreiber, ohne zweite Format-Normalisierung; Rückgabe kann nicht ohne vorherige K0-Charge neue Aufträge schaffen; Import setzt nie direkt auf public.

## Echte Nutzereingaben, synthetische Testumgebung ausdrücklich unterschieden
Originaldaten: 61 reale WordPress-Aufträge/Titel mit ursprünglichen Keywords und Intents, 20 echte MINI-Positionen des Batches `mini-20261115102911-353bdc69d800`, 20 tatsächliche importierte CATEGORY-Zuordnungen, 1024 echte WordPress-Inventareinträge, 1176 echte WordPress-Kategorien. Titelsätze und Zuordnungen wurden NICHT neu erzeugt oder geändert.
Simuliert (nicht echt): WordPress-PHP- und Datenbankausführung, WordPress-HTTP-Rahmen, K0-ARTIKELTEXTE, die vom echten K0-Worker noch nicht produziert wurden. Kein externer DataForSEO- oder K0-Aufruf; keine Änderungen an oliver-beil.de oder pferde-atelier.de.

## Tatsächlich ausgeführte Qualitätstests am vollständigen 0.4.10 Quellstand
- **51/51** Testbedingungen mit EXAKT echten 61 alten Aufträgen und 20 echten Kategorien: 20 K0-Aufträge direkt aus vorhandenem CATEGORY-Checkpoint, gesamte 61 Alt-Titel unverändert, alle K0-Slots 64-stellig/verschieden, kein PPM-Plan benötigt, originaler WordPress-Draft-Import mit 20 simulierten K0-Bodytexten, Rückgabe-Wiederholung ohne doppelte Entwürfe, geänderte Rückgabe abgewiesen, einzelner fehlerhafter Themenpunkt hält nur diesen an, 19 andere laufen weiter, Abbruch nach 7 gespeicherten CAT-Zeilen und Wiederaufnahme nur verbleibende 13, zwei 10er-K0-Chargen ohne doppelte Vergabe, technische Kollision nur ein Auftrag, erstmaliger Import aller tatsächlichen 61 Originaltitel aus leerem WP-Regal und idempotente Wiederholung.
- **13/13** zusätzlicher neuer Keyword-Ablauf: CATEGORY, EDITORIAL, TITLE, bei FREI/BELEGT/KLAERUNG, keine falschen Fremdtierserien oder neue Fachentscheidungen.
- **30/30** WordPress-Plugin-Startprüfungen unbestätigt, bestätigt und mit Original-Recherche READY. Alte Cron- und Nebenschienen inaktiv.
- **94/94** Funktions-/Startprüfungen bestanden. **Zusätzlich** realer Plugin-`txe_export`-HTTP-Handler unter simuliertem WP mit genau echtem 61/20-Nutzerzustand aufgerufen. Ergebnis: gültige 7346-Byte-JSON, exakt 20 echte Titel und Kategoriezuordnungen, genau fünf K0-Felder, Hash `b42c66f32837264bafcd505dd53f0da797e142274ccaefdc2fe882f3352b323b` durch externe Python-Gegenrechnung identisch.
- **81/81** PHP-Syntax-Prüfungen bestanden; ZIP 90 Dateien, CRC PASS. 6 unbenutzte Altdateien physisch gelöscht, 3 nötige Dateien angepasst, 87 unverändert. Keine Referenz auf gelöschte PPM-Plan-Klassen.

## Installierbares ZIP und Testgrenze
`Texterstellung_KISS_0.4.10_TEST_ZIELVERTRAG_ECHTDATEN.zip`, 535753 Bytes, SHA256 `3cdb22ab1660d09bcdf2dcfedcb417768eb2f3b18e93bbde2ead5879aee53125`.
**TEST-only**, private Pluginablage: `/pferdeatelier/PLUGINS/ARBEITSRAUM_PSTE_KISS/`, zusammen mit QA-JSON, HTTP-Resultat (AUSDRÜCKLICH NUR SIMULATION), umfangreichem Markdown-Bericht, Struktur-JSON. Alte 0.4.9 nicht als funktionierende K0-Version verwenden. Kein GitHub-Merge/Live-Änderung.
**Einziger nächster echter Nutzerklick nach Sicherung und Plugin-Ersatz:** auf oliver-beil.de 0.4.10 bestehende Texterstellung ERSETZEN, NIE löschen, anschließend `Texterstellung -> K0-Export -> 20 -> Freie Aufträge entnehmen und JSON exportieren`. **Kein MINI-, Kategorie-, Titel-, SEO- oder Abschlussimport noch einmal durchführen.** Benutzer kann tatsächliche K0-Ausgabedatei hier zur echten WP-Abnahme hochladen.

**Beweisschranke:** Die lokale Simulation ist erfolgreich, aber nicht gleichbedeutend mit echtem WordPress-End-to-End. `production_release_allowed=false`; `real_wordpress_k0_export_passed=false`; `external_k0_article_generation_passed=false`.