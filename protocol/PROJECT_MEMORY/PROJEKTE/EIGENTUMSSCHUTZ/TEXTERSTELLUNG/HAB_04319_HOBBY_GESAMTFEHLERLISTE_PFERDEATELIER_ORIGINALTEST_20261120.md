# Hab & Bewahr 0.4.31.9 – Verifizierter Hobby-Gesamtfehlerlisten-/Pferdeatelier-Abgleich (20.11.2026)

**ERST ORIGINAL GELESEN:** Funktionsvertrag universelle Texterstellung `ZIELVERTRAG_UNIVERSELLE_TEXTERSTELLUNG_20261118.md`; neuer eigenständiger K-Multi-Lauf `100_NEUER_PRODUKTIONSLAUF_PORTALEIGENE_REGELN_VERBINDLICH_20261119.md`; aktuelle echte Hab-Diagnose Benutzerbild 12:00; originale tatsächlich entpackte ZIP-Quellen Pferdeatelier 0.4.34, Hobbydepot 0.4.24.13 und 0.4.24.15 sowie Hab 0.4.31.8. Original-K0 zu keinem Zeitpunkt geändert.

## 1. Gleiche Ausgangsursache, exakt reproduziert

Benutzerscreenshot nach bereits empfangenen **9 Rohkeywords**: Original Hab `FINALIZE` bleibt stehen, `PSTE_SANDBOX_RECORD_STORE_LEGACY_OPTION_MISSING`, 0 verarbeitbare Themen. **Denselben echten Original-PHP-Methodenaufruf** auf jungfräulicher WordPress-Mock-Datenbank ohne Altoption ausgeführt:
- Pferdeatelier 0.4.34: **FAIL** exakt derselbe Fehler.
- Hab 0.4.31.8: **FAIL** exakt derselbe Fehler.
- Hobbydepot 0.4.24.15: **PASS**: Nur bei wirklich leerer uninitialisierter Quelle bereits vorgesehene signierte Leerstruktur anlegen, vorhandene Daten strikt schützen und alle **5 ursprünglichen** Migrationsschritte abschließen.
- Neue isolierte Hab 0.4.31.9: **derselbe PASS**, einschließlich echter Methoden- und Gegenfalltests (15 Assertions); 0 bezahlte Anbieteranfragen und 0 WordPress-Artikel.

**Deshalb ist simples byteidentisches Kopieren des Pferdeatelier-Codes allein NICHT hinreichend:** Das Pferdeatelier läuft mit einem schon vorhandenen Altbestand; bei einer frischen Portalinstallation fehlt die bislang stillschweigend vorausgesetzte Altquelle. Hobby hat diese reale Abweichung repariert. Bei Hab wurde die Reparatur vorher nicht übernommen.

## 2. Hobbydepot-Fehlerliste kritisch mit allen 3 Systemen verglichen

| Originalfehler | Archivbeleg Hobby | alter Stand Hab 0.4.31.8 | neue 0.4.31.9 |
|---|---|---|---|
| Fehlender Legacy-Sandbox-Speicher | 0.4.24.5-Prüfbericht | FAIL; derselbe Originalfehler wie bei Pferdeatelier | PASS, sicherer Leer-Init + 5 Original-Migrationsphasen |
| Bereits BLOCKED markierter Kontext darf nicht pauschal abbrechen | 0.4.24.5-Prüfbericht | Original-Hab-Fortsetzung unvollständig | isolierte Hobby-Korrektur nur für exakte Wiederaufnahmesituation übernommen |
| `PSTE_EDITORIAL_RULESET_RAW_KEYWORD_INVARIANT_FAILED` bei Nullbestand | 0.4.24.4-Prüfbericht | originale fehleranfällige Null-Verzweigung | Original-Hobby-Nullbasisschritt übernommen; keine Quelldaten überschreiben |
| Fehlerhafte Liste überprüfter Originaldateien | Hobby 0.4.24.15-Audit | **FAIL**, 2 nicht existierende Klassen auch im Pferdeatelier | 15 echte Originalklassen; **92/92 PASS** einschließlich Manipulation/fehlender Datei |
| `PSTE_PAA_TASK_TIMEOUT`, ursprüngliche kostenpflichtige ID archiviert | Hobby 0.4.24.5/0.4.24.7 | Bereits in Hab 0.4.31.8 übernommen | unverändert, 11/11 direktes GET, 8/8 Queue und 11/11 Originalarchivwiederaufnahme PASS |
| Gespeicherter MINI-Auftrag nicht erneut abrufbar | Hobby 0.4.24.13/0.4.24.15 | Horse-Methoden `savedMiniChoices`, `savedMiniDownload` fehlen | Horse-Originalmethoden übertragen, derselbe Auftrag ohne Neubuchung |
| Nachträgliche bewusste manuelle WordPress-Veröffentlichung wird durch zwei Draftfilter verhindert | Hobby Quellaudit 0.4.25/Pferdeatelier 0.4.34 | Original-Hab-Filter blockieren explizite Freigabe | Beide Stellen auf schon vorhandene Horse-Originalprüfung abgestimmt |
| Hab C23-Satz statt Produktseed | Hab v0.4.31.6-Befund | In Hab 0.4.31.7 korrigiert | 48/48 Original-Suggestions/Related/Ideas/Questions-Tests wieder bestanden |
| Hobby MAGAZIN-Blattkategorien | Hobby 0.4.24.15 | Nicht derselbe Hab-Kategorienvertrag | Fremde Hobby-Kategorien nicht kopiert |
| Portalidentität, MINI, K0 fünf Felder, Rückimport | Hobby 0.4.24.13/15 + Pferdeatelier 0.4.34 | Isolierte alte Hab-PHP-Tests PASS | 29/29 originale Hab-Grenztests + 14/14 originale Importprüfungen PASS |

## 3. Erneut am FERTIGEN Hab-ZIP ausgeführt – Beweis statt bloßer Annahme

`Texterstellung_HAB_UND_BEWAHR_0.4.31.9_HOBBY_FEHLERLISTE_ORIGINAL_GEPRUEFT.zip`:
- SHA256 `c6565150120d2f493d811e2e2185f92cce3a6d46d41f8199bce4d9b4086e222e`, 523447 Bytes.
- 87 ZIP-Dateien, **80/87 bitidentisch** zu Hab 0.4.31.8; nur Haupt-PHP, fünf vorhandene PSTE-Klassen und README angepasst; keine neue PHP-Klasse.
- **78/78 PHP-Syntax bestanden**, 87 ZIP-CRC bestanden.
- Neu extrahiertes finales Paket: **11 Original-PHP-Testprogramme bestanden**, **228 explizite Einzelnachweise**. Zusammen: Sandbox 15, Audit 92, vier Keywordwege 48, Hab-MINI/Manuell-Veröffentlichen 29, Hab-Original-Import 14, PAA GET 11, PAA Queue 8, Original PAA Restore 11. Hinzu drei separate erfolgreiche Original-PHP-Integrationsversuche: zwei **früher real K0-geprüfte** Pferdeartikel in WordPress-MOCK-Drafts, Hobby15 vollständige MINI→K0-Paket→WordPress-MOCK-Kette mit simuliertem Text und Hobby MINI-Parität.
- Keine Änderungen an `class-pste-research-job.php`, `class-pste-dataforseo-client.php`, `class-pste-research-driver.php`, `class-pserc-system4-import.php` oder den Original-K0-GitHub-Dateien. **0 Anbieteraufrufe / 0 reale WordPress-Schreiboperationen** in Tests.
- Lokale maschinenlesbare Ergebnisdateien: `FINAL_FOUR_PORTAL_QA.json`, `release_static_QA.json`, `original_diff_04318_04319.patch` und je Prüffall Original-PHP-Log. Belegpaket im Hab-Büro.

## 4. Kritischer NEGATIVBEWEIS – was ausdrücklich NICHT erfüllt ist

Der ebenfalls tatsächlich gestartete Versuch, das **vollständige Hab-E2E** auf Basis eines bislang unvollständigen WordPress-Mocks durchzuspielen, stoppt am **originalen** Portalrelevanzschutz: `EXTERNAL_REVIEW_REQUIRED`, weil kein verifizierter WordPress-Portalbeleg vorliegt. Die anschließende MINI-Lesestelle verlangt echte R1/R2/R3-Seiten und scheitert an der im unvollständigen Mock fehlenden `get_posts`-Funktion. **Dies ist kein bestandener vollständiger Hab-Lauf**. Kein gefälschter Recherche-PASS, kein K-Multi-Writer, kein LanguageTool 6.8 oder echtes WordPress-Draft-Ergebnis. Auch Hab-Familienfilter `Paketbox` gegen mehrere C23-Geschwister bleibt als nachgelagerter offener semantischer Einzelentscheid. Die gesamte Produktionsstrecke ist NICHT freigegeben.

## 5. Nächster konkreter überprüfbarer Schritt

Nach WordPress-Backup die **bestehende** Hab-Texterstellung 0.4.31.8 als Ersetzung durch 0.4.31.9 aktualisieren, NICHT deinstallieren. Dann unter Texterstellung → Recherche **ausschließlich den bereits existierenden wartenden Auftrag/Status fortsetzen**; kein neuer bezahlter DataForSEO-Job, keine neuen K0-Aufträge. Nach dem tatsächlichen FINALIZE den aktuellen Diagnose-JSON herunterladen. Erst bei positivem Original-Rechercheabschluss in den vorhandenen MINI-Export gehen; erhaltene Daten und Kategoriebesitzer prüfen, KMulti-Writer weiter separat. **Original-K0 bleibt unverändert.**
