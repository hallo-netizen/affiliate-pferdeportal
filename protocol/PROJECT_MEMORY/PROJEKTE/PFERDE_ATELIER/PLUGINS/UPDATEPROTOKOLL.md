# PFERDE-ATELIER – PLUGINS – UPDATEPROTOKOLL

STAND: 2026-09-16
ROLLE: ZENTRALES PLUGIN-ÄNDERUNGS-/SYNC-PROTOKOLL

Regel: Für jede tatsächliche Entwicklungs-/Updatekette genau ein Vorgang `PU-YYYYMMDD-NNN`. Fach-/LIVE-Wahrheit bleibt im zuständigen Fachbüro.

## PU-20260915-001 – Pferderassen Manager
- PLUGIN-ID: PPA-011
- ART/HERKUNFT: UPDATE / EIGENENTWICKLUNG
- FACHBÜRO: `../WISSENSDATENBANK/AKTENSCHRAENKE/PFERDERASSEN/`
- VON/ AUF: 0.2.1 → 0.2.7
- WARUM: Relationslogik reparieren; Same-Group/Self/Unknown-Hardlocks; Doppel-ID-sicherer Backend-Backfill.
- TESTS: lokale 196-Post-Positiv-/Negativ-/Mutationstests PASS; WordPress-LIVE PASS 2026-09-15.
- ARTEFAKT: PPA-011/CURRENT.zip; SHA `5f72308cb922756cac8ffa2a01a27bfc7f1f1cfbabf6fbf5b4a33728fc8e58f1`.
- ERGEBNIS: PASS.

## PU-20260915-002 – Pferde Atelier Design historischer Incident
- PLUGIN-ID: PPA-002
- ART/HERKUNFT: UPDATE / FEHLERREPARATUR / EIGENENTWICKLUNG
- FACHBÜRO: `../DESIGN/`
- KANDIDATEN: 1.50.529, 1.50.530.
- REALER BEFUND: damalige LIVE-Regression Pferderassen/Glossar.
- TESTSTATUS: damalige Abnahme unzureichend; aktueller Fehlerweg später durch nachfolgende geprüfte Stände überholt.
- ARTEFAKT-SYNC DAMALS: BLOCKED.
- HEUTE: historischer Incident; aktueller PPA-002-Stand siehe PU-20260916-016.
- ERGEBNIS: HISTORISCH / CLOSED FÜR AKTUELLEN STAND.

## PU-20260916-001 – Universal Glossary Engine
- PLUGIN-ID: PPA-012
- ART/HERKUNFT: ENTWICKLUNG/UPDATE / EIGENENTWICKLUNG
- FACHBÜRO: `../WISSENSDATENBANK/AKTENSCHRAENKE/GLOSSAR/`
- VON/AUF: 1.4.6 → 1.4.7
- WARUM: fail-closed Glossarbereinigung, Import der 13 freigegebenen Begriffe, expliziter Pferd/Pferde-Text-Hardlock.
- POSITIV/NEGATIV/ROLLBACK: PASS; 149-Wörter-, Heading-, Bodylink-, fehlender-Pferdebezug- und Inventarabweichungs-Tests blockieren korrekt.
- WORDPRESS-LIVE: Endbestand 92 vom Nutzer bestätigt.
- ARTEFAKT: PPA-012/CURRENT.zip; SHA `6db2e5ad78ddbf6242cbca0059c7ab60b0a3f5e5bc68e948acc012e5700f4389`.
- ERGEBNIS: PASS.

## PU-20260916-002 – Design Glossar-Langwortfix
- PLUGIN-ID: **PPA-002** (nicht PPA-013)
- ART/HERKUNFT: UPDATE / EIGENENTWICKLUNG
- FACHBÜRO: `../DESIGN/` + Glossar-Fachstelle
- VON/AUF: 1.50.535 → 1.50.536
- WARUM: lange Glossarbegriffe brachen in Vorschaukarten mitten im Wort.
- TESTS: ZIP/Version/PHP-Lint/Long-XLong/No-midword-break/Scope PASS; Nutzer LIVE PASS.
- ID-KORREKTUR: die zwischenzeitlich verwendete PPA-013 war eine falsche zweite ID für dasselbe Designplugin und wurde aus dem aktiven Artefaktschrank archiviert. Kanonisch bleibt PPA-002.
- ERGEBNIS: PASS / HISTORISCHER ZWISCHENSTAND.

## PU-20260916-003 – Bildzentrale 2.7.0
- PLUGIN-ID: PPA-003 / MOD-002
- ART/HERKUNFT: UPDATE / EIGENENTWICKLUNG / ALLGEMEINGÜLTIGER KERN
- FACHBÜRO: `../BILD/`
- VON/AUF: 2.6.9 → 2.7.0
- WARUM: generischer Custom-Post-Type-Hero-Weg.
- LOCAL: 28/28 Backend-/Workflowtests PASS.
- WORDPRESS-LIVE: FAIL; Tab sichtbar, aber nicht aktivierbar.
- ERGEBNIS: HISTORISCHER LOCAL PASS / LIVE FAIL.

## PU-20260916-004 – Bildzentrale 2.7.1
- PLUGIN-ID: PPA-003 / MOD-002
- ART: FEHLERREPARATUR / UPDATE
- VON/AUF: 2.7.0 → 2.7.1
- WARUM: fehlendes `cpt`-Mapping im JS-Tabregister.
- TESTS: Delta-/Whitelist PASS; 21/21 Struktur/Regression + 12/12 Tab-Runtime PASS; Negativkontrolle reproduziert 2.7.0-Fehler.
- LIVE zum damaligen Zeitpunkt: Retest offen; später durch PU-007 bis PU-011 superseded.
- ERGEBNIS: LOCAL HARD PASS / HISTORISCHER ZWISCHENSTAND.

## PU-20260916-005 – Affiliate-Zentrale Audit
- PLUGIN-ID: PPA-001
- ART: ENTWICKLUNG / FEHLERREPARATUR-AUDIT
- FACHBÜRO: `../AFFILIATE/`
- KANONISCH: 6.72.19; lokale 6.72.20–6.72.27 nicht kanonisch.
- WARUM: ADCELL-/eBay-Ursachenprüfung.
- RELEASE-GRENZE: kein lokaler 6.72.2x-Stand ersetzt CURRENT; read-only Live-Checkpoint-Beleg bleibt Fach-NEXT.
- ARTEFAKT: PPA-001 bleibt 6.72.19 / SHA `72f437e5235aaec53631db052e2184b588366c7f8aa7eb72ae1c9e043cdf157f`.
- ERGEBNIS: BLOCKED / kein neuer Pluginstand.

## PU-20260916-006 – WordPress Speicheranalyse
- PLUGIN-ID: PPA-014
- ART/HERKUNFT: UPDATE / EIGENENTWICKLUNG
- FACHBÜRO: `../TECHNIK/`
- VON/AUF: 1.0.1 → 1.1.0
- WARUM: eng begrenzte manuelle Löschung regulärer Dateien direkt in `wp-content/wpvividbackups/` ohne FTP/SSH.
- TESTS: PHP/ZIP PASS; Positivtest PASS; Traversal/Symlink/außerhalb-Pfad BLOCK PASS.
- ARTEFAKT: PPA-014/CURRENT.zip; SHA `3acb62811ec8e7ea1940ec0968e5b51fc2cb0d1ae2f9e86eeeb6718c11873891`.
- WORDPRESS-LIVE: offen.
- ERGEBNIS: LOCAL HARD PASS / ARTEFAKT-SYNC PASS / LIVE OFFEN.

## PU-20260916-007 – Bildzentrale 2.7.2
- PLUGIN-ID: PPA-003 / MOD-002
- ART: UPDATE
- VON/AUF: 2.7.1 → 2.7.2
- WARUM: Pferderassen-Hero-Profil/Migration weiterführen.
- TESTS: gebundene lokale Positiv-/Negativ-/Regressionstests PASS.
- ERGEBNIS: PASS / HISTORISCHER ZWISCHENSTAND.

## PU-20260916-008 – Bildzentrale 2.7.3
- PLUGIN-ID: PPA-003 / MOD-002
- ART: FEHLERREPARATUR / UPDATE
- VON/AUF: 2.7.2 → 2.7.3
- WARUM: unnötiger Magnific-GET-Preflight erzeugte real 404; gebundener POST-Weg bleibt maßgeblich.
- TESTS: lokale Positiv-/Negativ-/Mutationstests PASS; WordPress-LIVE vom Nutzer als funktionierend bestätigt.
- ERGEBNIS: PASS / HISTORISCHER ZWISCHENSTAND.

## PU-20260916-009 – Bildzentrale 2.7.4
- PLUGIN-ID: PPA-003 / MOD-002
- ART: UPDATE
- VON/AUF: 2.7.3 → 2.7.4
- WARUM: Framing für vollständigere Pferdemotive.
- TESTS: lokal PASS.
- ERGEBNIS: PASS / HISTORISCHER ZWISCHENSTAND.

## PU-20260916-010 – Bildzentrale 2.7.5
- PLUGIN-ID: PPA-003 / MOD-002
- ART: UPDATE
- VON/AUF: 2.7.4 → 2.7.5
- WARUM: `post_type_hero` nativ 21:9 / 1260×540, kein nachgelagerter lokaler 3:1-Recrop.
- REGRESSION: Kategorie-/HivePress-Wege unverändert; Positiv-/Negativkontrollen PASS.
- ERGEBNIS: PASS / HISTORISCHER ZWISCHENSTAND.

## PU-20260916-011 – Bildzentrale 2.7.6
- PLUGIN-ID: PPA-003 / MOD-002
- ART: UPDATE
- VON/AUF: 2.7.5 → 2.7.6
- WARUM: sicherer serieller Rassen-Batch für die nächsten 10 offenen `pa_breed`.
- HARDLOCKS: nur `pa_breed`; nur ohne Featured Image; genau eine Aufgabe gleichzeitig; kein Überschreiben vorhandener Bilder.
- TESTS: lokal Positiv/Negativ/Regression + PHP/ZIP/Re-Extract PASS.
- WORDPRESS-LIVE: Nutzer `klappt`; sichtbarer 10er-Batch seriell ohne angezeigten Fehler.
- ARTEFAKT: PPA-003/CURRENT.zip + allgemeines Bildzentrale CURRENT; SHA `12edc4405560ac3b149cf76a0b6e65694337b1533c0ea5e3a777d3b6c98ccbf0`.
- GRENZE: kein Beleg vollständiger Bebilderung aller Rassen.
- ERGEBNIS: PASS.

## PU-20260916-012 – Design 1.50.537
- PLUGIN-ID: PPA-002
- ART: UPDATE
- VON/AUF: 1.50.536 → 1.50.537
- WARUM: Rassen-Hero vollständiger sichtbar + Ocker-H2-Linien.
- LOCAL: PASS.
- LIVE/SICHT: Bildwirkung vom Nutzer verworfen; kein CURRENT.
- ERGEBNIS: SUPERSEDED / NICHT CURRENT.

## PU-20260916-013 – Design 1.50.538
- PLUGIN-ID: PPA-002
- ART: UPDATE
- VON/AUF: 1.50.537 → 1.50.538
- WARUM: Hero wieder `cover`, Ocker-H2-Linien erhalten.
- TESTS: lokal/regressiv PASS; weiterer Weg darauf aufgebaut.
- ERGEBNIS: PASS / HISTORISCHER ZWISCHENSTAND.

## PU-20260916-014 – Design 1.50.539
- PLUGIN-ID: PPA-002
- ART: FEHLERREPARATUR / UPDATE
- VON/AUF: 1.50.538 → 1.50.539
- WARUM: lange Pferderassen-Hero-Titel brachen auf Desktop unsauber um.
- TESTS: alter Fehler reproduziert; lang/kurz/xlong/mobile positiv PASS; PHP/ZIP/Regression PASS.
- WORDPRESS-LIVE: Nutzer `pass`.
- SHA historischer Installer: `0924cd3aa98dd9fc4c3239f6d62a2f1dfeb3ddfef2bfdc78b354f5f304330f8b`.
- ERGEBNIS: PASS / HISTORISCHER ZWISCHENSTAND.

## PU-20260916-015 – Design 1.50.540
- PLUGIN-ID: PPA-002
- ART: UPDATE
- VON/AUF: 1.50.539 → 1.50.540
- SCOPE: ausschließlich Journal-Startseite `/journal/`.
- WARUM: Hauptkartentitel fett; weniger Crop; Bildfokus rechts; linker Verlauf erhalten.
- TESTS: lokaler Scope-/Regressionstest PASS.
- WORDPRESS-LIVE: Bildwirkung und Hauptkarten PASS; Referenzkacheln `Glossar`/`Pferderassen` noch nicht fett.
- SHA historischer Installer: `2b32fce1198364b64cf824efaa460dfe1254e5cc8bb258e9f25e90cbec21ccef`.
- ERGEBNIS: PARTIAL LIVE / durch PU-016 abgeschlossen.

## PU-20260916-016 – Design 1.50.541
- PLUGIN-ID: PPA-002
- ART: UPDATE
- VON/AUF: 1.50.540 → 1.50.541
- SCOPE: ausschließlich Journal-Startseite, nur Referenztitel `Glossar` + `Pferderassen` fett.
- TESTS: Delta/Scope/PHP/ZIP/Re-Extract/Version PASS.
- WORDPRESS-LIVE: Nutzer `ok pass`; zuvor bestätigter 1.50.540-Rest bleibt PASS.
- ARTEFAKT: PPA-002/CURRENT.zip; SHA `f93870321df4a989e8ceeb71d6a9b4a0780831184f3b9a36f1e6e29b5e8a6ee6`.
- ID-KORREKTUR: PPA-013 war eine irrtümliche zweite Design-ID; aus aktivem Schrank archiviert, nicht CURRENT.
- ERGEBNIS: PASS.

## PU-20260916-017 – Rassentexte 196 Textpflege Updater
- PLUGIN-ID: PPA-015
- ART/HERKUNFT: EINMALIGE EIGENENTWICKLUNG
- FACHBÜRO: `../WISSENSDATENBANK/AKTENSCHRAENKE/PFERDERASSEN/`
- KANDIDATEN: 1.0.0 verworfen; final 1.1.0.
- WARUM: bestehende 196 veröffentlichte Rassentexte kontrolliert aktualisieren, ausschließlich `post_content`; Identität/Meta/Status/Bilder/Relationen/Rassengruppe schützen.
- TESTS: Text-QA 196/196; Write-Whitelist; Dry-Run/Readback/Rollback; 5/5 Mutationstests; PHP/ZIP PASS.
- WORDPRESS-LIVE: finaler Dry-Run `196 veröffentlicht / würde aktualisieren 0 / bereits Zielstand 196`; Live-Stichproben vom Nutzer bestätigt.
- ARTEFAKT: PPA-015/CURRENT.zip; SHA `4bca49f986da897c4941674bda6646cdf5de26c7a7ea78fa26b3e82aefe6fd37`.
- BETRIEB: Einmalwerkzeug; Nutzer wurde informiert, dass das Plugin nach erfolgreichem Lauf deaktiviert/gelöscht werden kann. Eine tatsächliche Löschung ist nicht bestätigt.
- ERGEBNIS: PASS / AUFTRAG ABGESCHLOSSEN.

## PU-20261017-001 – PPA-005/PPA-006 SEO-Kategorie- und Bestandsworkflow (NACHHOLPROTOKOLL)

- **Art/Herkunft:** vorhandene WordPress-Eigenplugins; historischer Reparatur- und Regressionsauftrag, **kein neues Plugin, keine neue Architektur**.
- **Scope:** PPA-005 Portal SEO Topic Engine, PPA-006 Portal SEO Editorial Plan Compiler. Lokale Kandidatenkette dieses Chats: PSTE 0.57.96–0.57.102; PSERC 0.28.37–0.28.40. PPM 6.7.9 bleibt für den letztverfolgten Zwei-Plugin-Weg im GitHub-Original byteidentisch, SHA256 `acbda93bd1c4292de7aaf88db2195631103991ff508b36c88cb694714818abd1`.
- **Ziel und Warum:** Nur die eine bestehende zentrale Keyword-/Kategorienprüfung, zuerst inhaltlich geeignet, passender Titel, eine gemeinsame redaktionelle Fach-/Magazin-Entscheidung, fachlich passende vorhandene Kategorie oder verlustfreie Rückstellung zur bestehenden zentralen Kategorieergänzung. Keine Magazin-Sonderzulassung, kein Zwangs-Mapping, mindestens 3–5 artikeltragfähige Themen je sinnvoller neuer Blattkategorie. Echte unveränderte Qualitäts-, Signatur-, Dubletten-, Artikeltyp-, Planplatz- und Publish-Sperren weiter schützen. Fachliches Freeze: `affiliate-release-current:protocol/PFERDE_ATELIER_CATEGORY_CHANGE_MASTER_20260922.md` Abschnitt 29.1–29.3.
- **Tatsächlich gemacht:** vollständige lokale Kandidaten-ZIPs angefertigt und in mehreren kleinen PHP-/Compiler-/Mock-Matrizen positiv und negativ getestet, Ed25519-Journal-Vertragsangleichung geprüft, später bei unverändertem PPM eine Zwei-Plugin-Kompatibilität lokal nachgewiesen; PSTE 0.57.102 bearbeitete Start-/Altauftrag-/Wiederaufnahmepfade. Keine bestätigte DB-1:1-Gesamtprüfung. ZIP-Kandidaten PSTE 0.57.102 SHA256 `ddc05f0f2e05ba21a2acd0a139ac2e6788c6fcfb4b1226a75335a2eaea9d3ba5`, PSERC 0.28.40 SHA256 `e56c3daac97d90f251acf754d00935fc05469b770a6cefa3ec29f37765c555f5`; lokal ZIP-CRC PASS, aber **keine daraus abgeleitete Release-/LIVE-Freigabe**. PPM-Original nicht überschreiben.
- **Korrigierte frühere PASS-Behauptung:** 21/21 kleine Klassenfälle, 13/13 Zustandsfälle, 3/3 künstliche Journal-Beispiele und Pluginstarts beweisen keinen durchlaufenden Gesamtworkflow. Die später lokal reproduzierte PSTE-0.57.102-Fehlzuordnung „Warum leckt mein Pferd viel am Salzleckstein?“ zu `salzlecksteine-faq` (`NORMAL_PASS`, Typ `FAQ`) widerlegt die behauptete uneingeschränkte Gleichberechtigung. Magazinkategorien im WP-Snapshot fehlten in der Produktionskategorienmenge. Compiler `COMPLETE` ist nicht Bestandsautomatik `COMPLETE`.
- **Live-/Nutzerevidenz 16.10.2026:** eigene Diagnose mit Run `50cdce49-683f-4084-a17a-6c56a72de9f9` zeigt `CANCELLED`, 520/5014, `PSTE_EXISTING_EVIDENCE_REENTRY_REVIEW_CANDIDATE_MISMATCH`, Provideraufrufe 0; globaler Compiler 55 Kandidaten, 1 ready, keine globale Bestandsfreigabe. Geprüfter historischer 12.10.-Export: 4501 Themen; kein identischer aktueller 5014er Einzelrecordexport.
- **Weitere offene Negativfälle:** tatsächlich laufende Recherche darf nicht abgebrochen werden; Einzelthema darf nicht globalen Lauf abbrechen; keine künstliche Journalterm-Simulation als DB-Beweis; „DATEI BEREIT“ nicht als Bestandserfolg, solange `processed != total`; schlechte/fremde Keywords, falsche Kategorie, Titel-/Dubletten-/Signaturfehler müssen blockieren; verwertbare Keywords dürfen nicht gelöscht oder unpassend zugeordnet werden.
- **Teststatus:** unabhängiger Workflow-Gegencheck **FAIL**. Kein vollständiges WordPress-/MariaDB-End-to-End; aktueller 5014er Datensatz fehlt als isolierte, hashgebundene Kopie; Tests der aktuellen Installation nicht nachgewiesen. **Kein CURRENT.zip ersetzen, kein neues Download-Plugin anbieten.**
- **Rollback:** die vorhandenen isolierten Plugin-CURRENT-Artefakte unverändert behalten; neue Kandidaten nur nach erneutem, vollständigem Fach-/DB-/Integritäts-PASS und gebundener Quellidentität veröffentlichen. Keine WordPress-Schreibaktion ausgeführt.
- **CURRENT-Status und genau eine NEXT ACTION:** nur `CURRENT_STATE.md` dieses Plugin-Büros. Dieses Protokoll ist ausschließlich **WAS/WARUM/Evidence**, keine zweite Statusautorität.
- **Zusätzlicher GitHub-Read-only-Gegencheck 17.10.2026 (dieser Chat):** Frische PLUGINS-Current SHA `d5cfd343f0253592f07478fcac65b6b00ff8293c`, Fachzielvertrag SHA `c1452bade797eccf70ceaa0d7ca557dd5ef5a594` unverändert. Zentrale `CATEGORY_INTEGRATION_HOBBYRAUM/PFERDEPORTAL_KATEGORIEN/KATEGORIEN.tsv` auf `affiliate-release-current`, Blob SHA `44684b554110560ffccab9ccf50b910a97259a06`: **1160** Datensätze, 4 Spalten je Datensatz, keine doppelten `term_id`-Werte oder `slug`-Werte, keine leeren Pflichtfelder. **Alle neun Journal-Slugs** der zentralen Liste sind vorhanden (Term-IDs 1481, 1487, 1486, 1485, 1482, 1500, 1483, 1484, 1488). `parent_slug` ist dort durchgehend leer; der TSV-Check bestätigt daher **keine** echte WP-Hierarchie oder produktive Kategorienauflösung. GitHub-Actions-Lauf [39013722926](https://github.com/hallo-netizen/affiliate-pferdeportal/actions/runs/39013722926) vom 17.10. (Category Integration Hard Baseline) **FAIL** bei Bindung eines alten PSTE-0.57.6-Prüfartefakts, somit **kein** neuer SEO-Live-Gesamtnachweis. Über den verbundenen GitHub-Zugriff ist kein authentifizierter WordPress-/MariaDB-Readback der aktuellen 5014 Einzelrecords oder installierten PSTE-/PSERC-Bytes verfügbar; letzter belastbarer Gesamtstatus unverändert **BLOCKED**. Keine Plugin- oder WordPress-Änderung.
- **KISS-Fehlerpriorität / Titelmangel, geprüft gegen Fachvertrag 29.1–29.3 am 17.10.2026:** Zielabfolge ist **ein** bestehender Weg: vollständiger Keywordbestand → Eignungs-/Dublettenentscheid → genau ein natürlicher Titel für geeignete eigenständige Themen → **einmalige** fachliche Auswahl aus vorhandenen Fach- **und** Journal-Kategorien → bei fehlender Kategorie unverändertes Keyword samt Titel und Befund im bestehenden Rückstellungsweg → bereits vorhandener PSERC-/PPM-/Datei-Weg. Nur übergreifende redaktionelle Themen ohne spezifischeren Fach-Owner ins Journal; konkrete informative Produkt-/Anwendungsfragen dürfen oben bleiben. Keine zweite Journal-Eignungshürde; fehlende Kategorie ist keine Ablehnung. **Der gemeldete breite Titelmangel ist als eigener End-to-End-Messpunkt offen:** Aus den derzeit belegten Summen `520/5014 CANCELLED` und Compiler `55/1 ready` lässt sich die genaue Position jedes fehlenden Titels **nicht** ableiten. Deshalb auf aktuellem WordPress-Snapshot pro Originalkeyword festhalten: geeignet / inhaltlich abgelehnt (Grund) / Dublette (Referenz) / natürlicher Titel erstellt oder vorhanden / Eigentümer oben oder Journal / Kategorie-ID oder zentrale Rückstellung / nachfolgender Qualitäts-/Planstatus. Vor/nach jedem Übergang Bestandszahlen abgleichen, keine stillen Verluste, kein globales Abbrechen durch einen unpassenden Altbeleg. Keine neuen Heuristiken oder Architektur, kein Sicherheits-/Signatur-/Publish-Gate aufheben, keine voreilige Fertigmeldung. **Dies ist eine Prüfvorgabe, kein implementierter Fix oder LIVE-PASS.**
- **Erweiterte Originaldatenprüfung, 17.10.2026 (gespeicherter WordPress-Export)**: Physischer SEO-Dateibestand im persönlichen `/Pferdeatelier/`-Dateischrank nachgewiesen: `PFERDEATELIER_SEO_THEMENENGINE_0.57.102.zip`, `PFERDEATELIER_SEO_COMPILER_0.28.40.zip`, `_SEO_EXPORT_ARBEITSKOPIE_20261016.json` sowie `pste-kurzweg-diagnose-20261016-162540-utc.json`. **Korrektur früherer Ungenauigkeit:** Diese Dateien existieren; über den jetzigen Dateizugriff konnten ihre ZIP-Rohbytes zwar nicht in die lokale Laufzeit kopiert werden, der 121-MB-JSON-Export hingegen vollständig als Text. Dessen eigener Ursprung ist **12.10.2026, PSTE 0.57.78, 4501 Einträge** und **nicht** die aktuellen 5014. Tatsächlich alle 4501 Datensätze gelesen, Kandidatenkennungen eindeutig, 0 Hauptkeywords leer. Im gespeicherten Status: 4413 `DISCOVERY_PROBE`, 72 `ARTICLE_TOPIC`, 16 ohne Rolle; Metadatenstatus 2730 `SANDBOX_REQUIRED`, 1669 `STRUCTURE_GAP`, 90 `NORMAL_PASS`, 12 `RETAINED_NON_PRODUCING`. 866 `editorial_title`, aber nur 115 `production_title` und 89 `READY_FOR_COMPILER_CAPABILITY_CHECK`; 751 Zwischentitel nicht zu Produktionstiteln weitergereicht. Unter 1669 Strukturlücken 335 Zwischentitel, 0 Produktionstitel. **Alle neun** Journal-Slugs sind in der produktiven 1165er Blattkategorienliste dieses Exports nicht enthalten; fünf Kandidaten verwenden trotzdem Journal-Slugs via separatem Auflösungsweg. 69 der 90 `NORMAL_PASS` erhalten übergeordnete Kandidatenentscheidung `BLOCKED`, darunter 52 mit `ANSWER_EQUIVALENT_EXISTING` – Dublettensperren nicht pauschal ausbauen. Themen-Zusammenfassung: 4428 GREEN, aber Gesamt-PASS 0. Das sind **belegte gespeicherte Fehl-/Haltedaten**, kein Replay der heutigen Installation und kein neuer Release. Die WordPress-Live-Diagnose vom 16.10. bleibt separat **520/5014 CANCELLED**. Aktuelle Original-ZIP-Bytes/aktuelle komplette 5014er DB nur mit berechtigtem direkten WordPress/Datei-Readback 1:1 testbar; keine fälschliche Gleichsetzung mit der Altquelle. Kein WordPress-Write, keine Pluginfreigabe.
- **Konkreter Kurzweg-Endübergang (Originaldiagnose 16.10., erneut gelesen 17.10.):** Drei manuell ausgewählte Themen wurden im selben Lauf geprüft: erste Direktprüfung **1 ready, 2 not ready**; nach PSERC **0 ready, 3 not ready**. „Wie reitet man ohne Steigbügel?“ scheitert im PSERC an `BLOCKED_CATEGORY_ARTICLE_TYPE_MISMATCH` / `EXTENSION_TOPIC_BINDING_INVALID`. „Warum wehrt sich mein Pferd in der Herde?“ sowie „Wie kann ich die Weidehaltung meines Pferdes organisieren?“ bleiben als `NOT_PLANNABLE` wegen `PSTE_PORTAL_RELEVANCE_PROVEN_FAMILY_STRUCTURE_GAP` / `PSTE_STRUCTURE_DECISION_REQUIRED_BEFORE_NORMAL_REENTRY` erhalten. Danach `PSTE_K0_PSERC_NO_READY_ITEMS`; ausdrücklich `changes_to_topics_or_plans=false`, `provider_calls_by_diagnostic=0`. **Damit ist ein echter Übergabeverlust zwischen bereits positiver Vorentscheidung und Compiler in Original-Laufdaten belegt**, nicht nur Magazin-Vorfilter. Quelle: persönlicher Pferdeatelier-Dateischrank `pste-kurzweg-diagnose-20261016-162540-utc.json`. Kein daraus behaupteter aktueller 5014er E2E oder reparierter Pluginstand.


### 2026-10-17 – PSTE Vier-Schritt-Haltestelle im bestehenden Code (LOKAL GETESTET, NICHT INSTALLIEREN)
- Codepatch im bestehenden Pferdeatelier-Pluginbüro: `PSTE_EXISTING_PLUGIN_WORKER_HALTS_20261017.patch` (Basis: authentische PSTE 0.57.102, lokaler weiterentwickelter Kandidat; kein neues Plugin-/Tabellen-/Worker-System). Erkennbar je Keyword: Pferdebezug, Titel, Fach/Magazin, Kategorie, GREEN/YELLOW/RED, tatsächliche Haltestelle, erste noch offene Prüfung, bisher erledigte Schritte und Fehlergrund. Bei vorgelagerten Titelprüfungen bleibt `resume_from` ehrlich getrennt von der erkannten Halteursache. Keine produktive Wiederaufnahme-Abkürzung behauptet.
- Bestehende Sandbox-Datenflussbindung um optionalen SHA-256-Nachweis des Haltepunkts ergänzt; vorhandene ältere Datensätze bleiben lesbar; manipulierte Haltepunkte verweigert. Bestehende WordPress-Sandbox-Tabelle zeigt Haltestelle/nächsten Schritt/erledigte Schritte. Kein neuer Speicher, keine neue Kategorieautorität, keine Qualitäts-/Publikationsfreigabe.
- Echter PHP-Klassen-Replay gegen den gespeicherten *historischen* 4501-Keyword-Export: **4501/4501 mit vorhandenem Vier-Schritt-Zustand; 0 PHP-Fehler, 0 verlorene Datensätze, 0 beobachtete Schreibversuche**. Haltestellen: Kategorie 2017, Pferdebezug 1888, Fach/Magazin 387, Titel 67, grüner Metadaten-PASS 142. Diese 142 sind **keine fertigen Artikel**. Sandbox-Datenfluss Positiv-/Negativ-/Manipulationstest für alle fünf Zustandsklassen bestanden. PHP-Lint 122/122; original PSERC 0.28.40: 17/17 signierte Übergaben, 17/17 Slotprüfungen, jeweils 17/17 Negativfälle Titel, Kategorie, Slot; bestehende sechs Wiedereinstiegs-Negativ/Positiv-Prüfungen bestanden.
- **Harte Grenze:** Es handelt sich um lokalen PHP-/historischen Daten-Replay, **nicht** um den vollständigen aktuellen WordPress-Backend-Lauf mit 5014 Keywords, echter Datenbank, PPM 6.7.9, Artikeldatei und Wiederaufnahme. Kein Plugin zur Installation, kein aktueller Release, kein Update von `CURRENT_STATE.md`, `publish_allowed=false` unverändert. Nächste notwendige technische Arbeit: checkpointsichere Wiederaufnahme und vollständiges Original-Backend-E2E, ohne neue Architektur.

- **17.10.2026 – Fortsetzung am realen automatischen Sandbox-Wiedereinstieg (LOKAL PASS, NICHT LIVE):** `PSTE_WORKER_REENTRY_SAFE_CONTINUE_20261017.patch`, inkrementell auf `PSTE_EXISTING_PLUGIN_WORKER_HALTS_20261017.patch`. Im existierenden `PSTE_Normal_Reentry_Coordinator` behandelt ein fehlerhafter Keywordfall samt gescheiterter Fehlermarkierung den Rest der Charge nicht länger als globalen Abbruch. Die bestehende `automaticReentryEnvelopes()`-Liste prüft optional signierte aktuelle Arbeiter-Haltepunkte vor DB-Anwendung; manipulierte Haltepunkte werden zur Nachprüfung zurückgestellt, Legacy-Datensätze ohne neuen Haltepunkt bleiben kompatibel. Ein Chargefehler ergibt `PARTIAL_FAILURE` statt irreführendem `PASS`, inklusive Cron-Fehlerstatus. Keine Änderung an eigentlicher Fach-/Magazin-/Titel-/Kategorie-Entscheidung, keine neue Architektur/Speicher, keine Produktions- oder Publish-Freigabe.
- **Tests lokal:** 6 simulierte, unabhängige Wiedereintritte (3 angewendet, 3 fehlgeschlagen, spätere Erfolge trotz Fehlern bearbeitet, negative Checkpointprüfung vor DB, fehlerhafte Fehlermarkierung isoliert); Legacy-/Checkpoint-Leseweg PASS; reale `existingEvidenceReentryReview` 6/6 Positiv-/Negativprüfungen PASS; 5 signierte Original-PSERC-Übergaben inkl. Negativfall Titel/Kategorie/Slot PASS; 79/79 PHP-Klassen-Dateien der PSTE includes lint PASS. Patch-Anwendung auf vorherigen bekannten Codestand (`patch --dry-run -p1`) PASS. Keine behauptete 5014er live MariaDB-/PPM-E2E-Abnahme, kein installierbarer Release. **Noch offen:** echtes erneutes Fortsetzen direkt am individuellen Worker-Haltepunkt statt vollumfänglicher Evaluierung des bestehenden monolithischen Normalpfads; echter aktueller Gesamtworkflow.

- **17.10.2026 – automatisches Nachprüfen nur bei echtem Delta:** Bestehende Sandbox-Methode `refreshInternalStructureBacklog` nutzt einen Hash aus aktuellem Struktur-/Kategoriemapping und vorhandener PSTE-/Titelregelsatzversion. Bei unverändertem Hash und frischem Wochenlauf `NOT_DUE`, bei neuer Struktur/Kategorie/Pluginregel sofort vorhandener providerfreier Nachprüfungsweg; keine neue Tabelle, kein neuer Scheduler, keine neue Architektur. Patch `PSTE_SANDBOX_RECHECK_ON_CATEGORY_RULE_CHANGE_20261017.patch` auf dem bereits gesicherten Wiedereinstiegscode, Test `tests/test_pste_sandbox_recheck_when_categories_change.php` im selben Büro. Lokale echte PHP-Methodentests: gleichbleibende Struktur => `NOT_DUE`, geänderte Struktur => `PASS`, unverändert erneut => `NOT_DUE`, geänderte Kategoriebindung => `PASS`, explizite Erzwingung => `PASS`, ohne Provideraufrufe. Inkrementeller Patch vor Anwendung `patch --dry-run -p1` PASS; weiter **nicht live, nicht installierbar**, kein vollumfänglicher 5014er WordPress-/PPM-E2E-Beweis.

- **17.10.2026 – KISS-Nachprüfung gelber Fälle im bestehenden PSTE (nur lokaler Code-/PHP-Backendtest, keine Installation):** Die vorhandene tägliche Sandbox-Wartung mit wöchentlichem internen Rückfalllauf bleibt. Nach gebundenem Kategorien-/Regelwechsel erfolgt die interne Nachprüfung automatisch; ein vorhandener Cron-Hook setzt nötige Portionen bis zum Ende fort. In `Themenprüfung → Sandbox` ist eine manuell auslösbare, kostenfreie **interne** Nachprüfung ergänzt. *Unklare Pferde-Relevanz mit möglicher externer, kostenpflichtiger Recherche bleibt im bereits vorhandenen gesonderten kostenbestätigten Relevanz-Prüfweg; keine neue Providerfreigabe*. Alles im alten PSTE, kein neuer Worker, kein neuer Cron-Hook, keine neue Tabelle. Änderung `PSTE_SANDBOX_HYBRID_RECHECK_BOUNDED_20261017.patch` baut inkrementell auf dem bereits geprüften aktuellen Kandidatenstand auf.
- **Datenbank/KISS:** Nach abgeschlossener vorhandener Record-Store-Migration verarbeitet die interne Nachprüfung je Ausführung max. 25 gelagerte Sandbox-IDs und lädt NICHT mehr den kompletten alten Sandbox-Blob. Fortschritt/Cursor samt Prüfsumme in der **vorhandenen** Maintenance-Health-Option; Bindung an Regeln, Kategorie-Snapshot UND exakte vorhandene Record-ID-Menge. Bei neueingetroffenen Keywords wird nur dieser Nachprüflauf sicher neu begonnen. Fehlerhafte einzelne Fälle bleiben mit Fehlergrund gespeichert; Schreibfehler verhindern Cursorfortschritt; absichtlich veränderte Cursor werden zurückgewiesen; aktive externe Sandbox-Arbeit blockiert parallelen Recheck. Teilbearbeitung zeigt `RUNNING`, nicht irreführend `PASS`/kompletter Erfolg. Bestehende Signatur-, Dubletten-, Veröffentlichungs- und PSERC-Sperren unberührt.
- **Nachweis lokal:** PHP-Syntax 79/79 PSTE-Dateien PASS, `patch --dry-run` auf passgenauer Vorfassung und Byte-Abgleich nach Anwendung PASS. Neue reproduzierbare Tests `tests/test_pste_sandbox_hybrid_bounded.php` (65 Datensätze, 25er Grenzen, kein alter Monolith-Read, automatisch nach Kategorieänderung, wöchentlich, manuell, neue Keywords, defekter Fortschritt, fehlgeschlagenes Schreiben, aktiver Job) und `tests/test_pste_sandbox_hybrid_manual_post.php` (authentifizierter Admin-POST: laufend, Teilfehler, ungültige Berechtigung ohne Wartungsdatenmutation) PASS. Weitere frühere Tests: Sandbox-Strukturwechsel, bestehender Reentry-Positiv/Negativ-Test, Worker-Checkpoint, PSERC-Signatur/Slot/Negativ-Brücke 17 Themen PASS. PHP-/WordPress-Funktionen für die neuen Negativ-/Admin-Szenarien im lokalen Test gemockt, also **kein** vollständiger produktiver MariaDB/WP-Härtetest.
- **Freigabe:** Kein Plugin-Download zur Installation, `CURRENT_STATE.md`/Bürotür/Publish unverändert; voller aktueller 5014er Live-Workflow durch PSTE→PSERC→PPM→Artikeldatei weiterhin **NICHT nachgewiesen**, keine behauptete höhere echte Artikelproduktion. Einzelne Keyword-Halteplätze werden in der vorhandenen Sandbox weiter geführt.


### 17.10.2026 – PSTE 0.57.104 vollständiger Originaldelta-/Bestandslauf; weiterhin KEINE Installationsfreigabe
- Ein **einziger exakt reproduzierbarer Delta-Patch** vom verifizierten Original-PSTE 0.57.102 (ZIP SHA256 `ddc05f0f2e05ba21a2acd0a139ac2e6788c6fcfb4b1226a75335a2eaea9d3ba5`) zur lokal gebauten 0.57.104 unter `PSTE_057104_FULL_ORIGINAL_DIFF.patch`. `patch --dry-run --fuzz=0`, echtes Anwenden und vollständiger Datei-Byte-Vergleich original+Patch gegen Kandidat: PASS. ZIP 0.57.104 intern gebündelt und `testzip`: PASS, SHA256 `f479368bb69bb0ec1b4736c18d736093e1ee5c2b9df325997af7c946f4a17a8a`. Original-PSERC 0.28.40 unverändert, SHA256 `e56c3daac97d90f251acf754d00935fc05469b770a6cefa3ec29f37765c555f5`.
- Neu exakt in bestehender `PSTE_Topic_Policy::classifyRole`: das historisch gespeicherte `discovery_only`-Label darf **nur bei frischem, gebundenem `NORMAL_PASS`**, gutem Titel, existierender Kategorie, echter Rohquery-Bindung, aktueller abgeleiteter Autorität und positivem bestehenden automatischen Poolstatus ein Artikelthema blockieren. 2 Positiv- und 9 negative PHP-Fälle PASS; alte explizite DISCOVERY_ONLY-, Duplicate-, Sandbox-/Category-Gap-/bad-title-/bad-raw- und Readiness-Sperren bleiben wirksam. Keine neue Kategorie oder Produktionsfreigabe.
- Neue ausführbare Tests im Pluginbüro: `tests/test_pste_057104_wordpress_bootstrap.php` (originales Plugin lädt mit vorhandenen PHP-Klassen/WordPress-API-Stubs, 63 Hooks inklusive DataForSEO-Kette, Sandbox, Admin; 0 Bootstrap-Schreibvorgänge), `tests/test_pste_057104_article_from_discovery.php`, `tests/test_pste_057104_historical_replay.php`. Lokale zehn Testgruppen für Bootstrap, Sandbox 25er Batches, manuell, signierte Worker-Haltepunkte, Tamper-/Failure-/Reentry-Fälle, Kategorieregelwechsel sowie originalen PSERC-Signatur-/Slot-Bridge-Pfad PASS; 79/79 PSTE-PHP-Dateien lint PASS.
- Historische **4501/4501** Originaldatensätze (vom **12.10.**, nicht 5014 aktuell) mit **genau den vorhandenen Original-PHP-Klassen** nach normalem `applyToPayload` erneut verarbeitet: **0 Ausnahmen, 0 veränderte Rohfelder, 0 unerlaubte Schreibsignale**. Neu `NORMAL_PASS=142` (davon Journal 40), `SANDBOX_REQUIRED=2736`, `STRUCTURE_GAP=1611`, `RETAINED_NON_PRODUCING=12`. Worker-Haltepunkte: Relevanz 1888, Fach/Magazin 387, Kategorie 2017, Titel 67, Grün 142. **Neue Discovery-Promotions im echten historischen Bestand 0**, daher das ist keine bewiesene Ausbeutesteigerung! Ein historisch `NORMAL_PASS`-Metadateneintrag wird nach heutiger Regel als unklar neu markiert: „weidetore für pferde“, dessen ursprüngliche Gesamtentscheidung bereits `BLOCKED` wegen `ANSWER_EQUIVALENT_EXISTING` war; **kein früher freigegebener Artikel verloren**.
- Harte Testgrenze: WordPress-API-Stubs sind **keine echte WP/MariaDB-/PPM-Backend-Installation**. Der aktuelle echte 5014er-Datenbestand, vollständige Live-WordPress-DB, signierte End-to-End-Wiederaufnahme und **fertige Artikeldatei** wurden nicht als Gesamtlauf nachgewiesen. Also **0.57.104 NICHT INSTALLIEREN, NICHT PUBLIZIEREN, kein Download als Release und CURRENT_STATE bleibt BLOCKED**. Die vorhandene 142/4501 Metadatenquote ist nicht die Artikelausbeute und weiterhin ungenügend für den Zielvertrag. Nächster tatsächlicher Arbeitsschritt: den weiterhin blockierenden Kategorie-/Titel- und Compiler-Gesamtpfad beheben und danach vollständiges Backend-E2E positiv/negativ fahren, ohne weitere Architektur.


- **17.10.2026 – separate Kategoriebedarf-Warteliste im Original-PSTE (KEIN LIVE-RELEASE):** In der bestehenden Original-PSTE-Codebasis 0.57.104 wurde eine konsequent **getrennte Kategoriebedarf-Warteliste** auf Basis der schon vorhandenen `topic_pool.payload_json`-Zeilen umgesetzt. `PSTE_FOUR_WORKER_CATEGORY_ROOM_DELTA_20261017.patch` ist der vollständig gegen diese Basis geprüfte 6-Dateien-Codeunterschied, keine neue Tabelle/Klasse/Architektur. Neue vorhandene Admin-Sicht `Themenprüfung → Kategoriebedarf – fertige Titel ohne Kategorie`, paginiert und read-only. Die echte vorhandene Titelpipeline läuft bei eindeutigem Journalthema jetzt VOR dem vorhandenen WP-Kategorieterm-Abgleich; die echte Kategorie muss danach genau eindeutig vorhanden sein, sonst nur bei `NOT_FOUND` und gutem Titel/PROVEN Pferdebezug/eindeutiger Fach-Magazin-Weiche: `CATEGORY_ROOM_TOPIC_POOL`; keine Sandbox-Aufnahme. Fehlt Titelbeweis, Relevanz, Route oder eindeutig nachgewiesenes Nichtvorhandensein einer Kategorie, bleibt der Fall in bestehender gelber Sandbox/Strukturliste. Bestehender Fachweg und originale signierte PSERC/Publikationssperren unberührt; Kategorie-Neuanlagen **nicht** automatisch.
- Lokaler konkreter Positiv/Negativ-Nachweis mit originalen PHP-Pluginklassen und gespeicherter 4501er WordPress-Exportbasis: Vier konkrete Journalfragen (Salzleckstein, Steigbügel, Weidehaltung, Herde) jeweils bei fehlender WordPress-Termzuordnung -> `STRUCTURE_GAP` + gültiger Titel + exklusive Kategorie-Warteliste; bei vorhandenem Term -> `NORMAL_PASS`, kein Kategoriebedarf. Fach-Produktvergleich zur OP-Versicherung bleibt in beiden Variationen Fach-`NORMAL_PASS`. Zusätzlicher eigener **12-Fälle-Predicate-/Sandbox-Negativtest** PASS (abgelehnte unklare Relevanz, Titel, Route, bereits vorhandene Kategorie, Sandboxpflicht, verfälschter Rohquery-Hash und leerer Titel). Reproduzierbare PHP-Tests unter `tests/test_pste_category_room_four_worker.php` und `tests/test_pste_four_workers_real_missing_journal.php`.
- Gesamt-Originaldaten-Replay in **10 begrenzten PHP-Blöcken** 4501/4501 Fälle ohne PHP-Fehler oder veränderte Rohkeywords, derselbe historisch gespeicherte 12.10.-Stand: 142 `NORMAL_PASS`, 2736 `SANDBOX_REQUIRED`, 1611 `STRUCTURE_GAP`, 12 retained, 40 Journal-PASS. 17/17 signierte echte PSERC-0.28.40-Journalübergaben inkl. Kategorie-/Titel-/Slot-Negativtests bestanden, 79/79 includes PHP-lint fehlerfrei, ursprünglicher Code-Patch gegen Basis `patch --dry-run --fuzz=0` PASS. **WICHTIG** Keine Steigerung der normalen Metadatenausbeute in diesem historischen Baseline-Szenario, weil dort alle Journal-Kategorien für PHP-Mocks als vorhanden behandelt wurden. Der ungelöste echte Flaschenhals ist weiterhin, dass bei familienlosen Keywordtreffern der bisherige Normalpfad schon VOR voll geprüfter Titel- und Lane-Stufe stoppt. Der Vier-Arbeiter-Workflow ist damit **noch nicht end-to-end vereinheitlicht**.
- *Nur lokal gemockte WordPress-Taxonomie; keine aktuelle Live-WordPress-Datenbank mit 5014 Keyworddatensätzen, keine reale WP/PPM-/Artikeldatei-E2E-Abnahme. Kein Plugin zur Installation, `publish_allowed=false`, `CURRENT_STATE.md` bleibt BLOCKED.*


- **17.10.2026 – Fach-/Magazin-Weiche bei nachweislichem Pferdethema ohne Treffer in der Ursprungsfamilie (kein Live-Release):** Vorhandene `PSTE_Journal_Semantic_Router::classifyQuestion` im bestehenden Plugin inkrementell korrigiert, **ohne** neue Tabelle/Klasse/Architektur/Workflow: Ein eindeutig aus dem Originalkeyword erkennbares Fachthema (z. B. Haferflocken oder Weidegang für Pferde) darf nicht allein deshalb scheitern, weil das Original-DataForSEO-Suchthema/Produktfamilie nicht passt. Neue enge Themenbegriffe greifen **ausschließlich beim belegten Familien-Nichttreffer**; vorhandene Fachfamilien-/FAQ-/Vergleichszuordnungen bleiben vorrangig. Spezifische Fütterungsmerkmale schlagen das unspezifische Wort „Weide“, sonst bleiben unklare Mehrfach-Zuordnungen GELB. Die schon bestehende Title-/Risk-/WordPress-Term-/signierte Erweiterungs-/PSERC-Prüfung entscheidet weiterhin. Delta `PSTE_FOUR_WORKER_EQUAL_JOURNAL_ROUTING_20261017.patch` exakt gegen unmittelbar vorangegangenen Kategorie-Raum-Code `patch --dry-run --fuzz=0` + tatsächliche bytegenaue Patch-Anwendung PASS; kein neues installierbares Plugin.
- **Historischer Gesamtnachweis 4501/4501 (Datenstand 12.10., NICHT aktuelle 5014 WordPress-DB):** Metadaten-`NORMAL_PASS` **149** (voriger Kandidat 142), `Journal` **47** (voriger Kandidat 40), `SANDBOX_REQUIRED` 2741, `STRUCTURE_GAP` 1599, 12 nichtproduzierend. In 11 abgegrenzten PHP-Durchläufen **0 PHP-Fehler, 0 Änderungen an Rohquery/ursprünglichem QueryRecord, 0 unzulässige Schreibversuche**. Ein historischer `NORMAL_PASS` mit „weidetore für pferde“ bleibt wie schon vor dieser Änderung wegen inhaltlicher Überlappung auf `SANDBOX_REQUIRED` – ursprünglicher Kandidat `decision=BLOCKED`; **keine neue Regression**. Vier-Arbeiter-Haltestellen: 1888 Relevanz, 2010 Kategorie, 387 Fach/Magazin, 67 Titel, 149 Grün. Die 149 sind **nur Metadatenprüfungen, keine Artikel**. Kein nachgewiesener Zuwachs an produktionsfähigen Discovery-Rollen (`discovery_promoted=0`).
- Lokale Regressionen `tests/test_pste_four_worker_equal_routing.php` (11 Positiv-/Negativprüfungen) PASS: Pferde-Haferflocken => Journal Pferdeernährung, Pferde-Weidegang => Haltungsformen, bestehendes Hafer-FAQ und OP-Versicherung-FAQ unverändert, Weide+Heu weiterhin Ernährung statt fehlerhafter Mehrfachzuordnung, Braun-Rasierer irrelevant, Kolik-Risiko gelb, bei real fehlender WP-Magazinkategorie gültiger Titel **ausschließlich** im Kategoriebedarf statt Sandbox und **keine** Compilerfreigabe. `tests/test_pste_four_worker_pscerc_bridge.php` bestätigt mit **unverändertem Original-PSERC 0.28.40** für drei Journalfragen 3/3 signierte Bindungen und Planplatzbeweise, 3/3 Negativfälle manipulierte Titel, fremde Kategorien und fehlende Slots. 77/77 PSTE-Includes-PHP-Dateien Syntax PASS. Compiler nicht verändert.
- **Nicht behauptet:** vollständige Datenbank-/WordPress-/PPM-/Artikeldatei-E2E-Simulation des aktuellen 5014er Livebestands; kein Publisher-Schreiben, keine Installationsfreigabe und keine Aktualisierung von `CURRENT_STATE.md`. Hauptziel maximaler sinnvoller Artikelausbeute bleibt offen; der frühzeitige Rückstau bei familienlosen Themen ist dadurch erst **teilweise** abgebaut.


- **17.10.2026 – Four-Worker-Titelstufe tatsächlich vor Familienzuordnung (NUR LOKAL TEST, KEINE INSTALLATION):** Vorhandene `PSTE_Normal_Metadata_Path`-Klasse in der *existierenden* PSTE-Themenengine geändert. **Finaler, gegen das vorher gesicherte `PSTE_FOUR_WORKER_EQUAL_JOURNAL_ROUTING_20261017.patch` inkrementeller Patch**: `PSTE_FOUR_WORKERS_TRUE_SEQUENCE_20261017.patch`, Test `tests/test_pste_four_workers_true_sequence_20261017.php`. Kein neuer Worker, kein zweites Plugin, keine neue Datenbank, keine neue Relevanz-/Titel-/Kategorie-Engine. Wenn Pferderelevanz nachweislich PROVEN ist, aber die ursprüngliche DataForSEO-Familie keinen harten Treffer liefert, validiert Arbeiter 2 natürliche Originalfragen mit der **bestehenden** harten Titelprüfung **sowohl unter FAQ als auch Journal**; das benötigte Quellsubjekt wird nur aus von Arbeiter 1 bereits erkannten, tatsächlich im Originalkeyword vorkommenden Pferde-/Reittermen gebunden (z. B. Reitplatz; keine erfundene Kategorie/Familie). Ungeprüfte Titel bleiben gelb. Der vollständig geprüfte Titel bleibt eine **editorial_title**-Zwischeninformation; `title_candidate_only=true`, **keine** freie Produktionstitel-/Kategorie-/Artikeltyp-Zuweisung, kein 5-Felder-/Compiler-/Publish-Handoff. Nächster Arbeiter Fach/Magazin hat bei ungelöstem Typ ausdrücklich `YELLOW`, `next_step=lane`, `storage=EXISTING_SANDBOX`; **kein** falscher Kategoriebedarf. Die einzige vorhandene Kategoriebedarf-Warteliste bleibt bei nachgewiesenem Magazin/Fach + fertigem Titel + **wirklich fehlendem** WordPress-Term. `halted_at` wurde auf den **ersten tatsächlich offenen Arbeiter** vereinfacht; alte technische Ursachencodes bleiben in `halt_reason_codes` separat. Keine neuen Regeln, die Produktvergleich oder sicherheitsrelevante Themen unkontrolliert als Artikel zulassen.
- **Historischer Original-PHP-Quellreplay 4501/4501** gegen 12.10.-Export, in 16 begrenzten 300er-Blöcken, Stand **vor der allerletzten reinen Haltestellenanzeige-Korrektur**: 171 *zusätzliche* streng titelgeprüfte Kandidaten mit `title_precheck_validated=true`, bei denen die ursprüngliche Familie nicht erkannt wurde; bestehende 149 `NORMAL_PASS` (davon 47 Journal) bleiben weiterhin unverändert, 0 neue Normal-PASS, 0 PHP-Ausnahmen, 0 Originalkeyword-Mutationen, 0 ohne Erlaubnis freigegebene Artikel. Gesamtstatus: 2890 `SANDBOX_REQUIRED`, 1450 `STRUCTURE_GAP`, 149 `NORMAL_PASS`, 12 retained. Genau 1 ehemals historischer Metadaten-PASS weicht wegen des schon lange bestehend zu Recht gesperrten Weidetore-Duplikatfalls ab (ursprünglicher Datensatz `decision=BLOCKED`); kein früher freigegebener Artikel verloren. Nach letzter Anzeige-Vereinfachung gezieltes 220er-Originalreplay erneut bestanden, 24 unabhängige Titelprüfungen, 0 Rohfeldänderungen, 0 Ausnahme. Die übrigen 4281 nach reiner Anzeige-Vereinfachung nicht erneut ausgeführt – **keine unredliche Behauptung eines abgeschlossenen 5014er Live-E2E**.
- Bestehende PHP-Tests: 16 Positiv-/Negativbehauptungen zum tatsächlichen Reihenfolge-/Sandbox-/Kategoriebedarf-/Fach- und Magazinpfad PASS; 77/77 Original-PSTE-Includes syntaktisch gültig; originale Journal-Routing-Regression PASS, unveränderte **PSERC 0.28.40**-Signatur-/Slotbrücke 3/3 normal und 3/3 je Negativfall Titel/Kategorie/fehlender Planplatz PASS. Final-Patch **`patch --dry-run --fuzz=0 -p1`, echtes Anwenden und vollständiger Datei-Bytevergleich** PASS. `sha256(Patch)=22eb820adff7f5beed3bc25b414d351a8e0943353761739199c11a139d644051`.
- **Zielvertrag noch NICHT erreicht:** 149/4501 sind Metadaten-PASS, keine fertigen Artikel. Nicht alle nicht-fragenden DataForSEO-Keywordphrasen sind bereits in qualitätsgeprüfte gute Überschriften umgewandelt. Gemeinsame Fach-/Magazinkategorienweiche nach bestandsunabhängiger Titelprüfung muss weiter durchgezogen werden, dabei bestehen Dubletten-/Risk-/PSERC-/PPM- und Publish-Gates unverändert. Aktuelle 5014er WordPress-MariaDB/PPM/Artikeldatei-E2E **NICHT nachgewiesen**; kein Live-Release, kein Paket zur Installation, Current-State weiterhin BLOCKED.
