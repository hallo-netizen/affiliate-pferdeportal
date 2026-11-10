# PSERC 0.28.63 / PSTE – lokale Nachstellung mit echter JSON (10.11.2026)

**Status:** QA ONLY, keine neue ZIP, keine WP-/DB-Schreiboperation, keine Artikelproduktion, aktives K0 und Live unberührt.

## Geprüfte Originale

- Vom Betreiber hochgeladene aktuelle ausführliche JSON (3 READY): 90.640 Byte, SHA256 `29638fef9606925b5b6f322fcde695581999ec0c41bd111bca0bcb655fbf1220`.
- Ursprünglicher 5-Felder-Export der gleichen drei Planplätze: 1.393 Byte, Datei-SHA256 `d943ebe3ab65ca53de04b54aca02321c1b2052b3e30e40ab6ff4d5a4cc9b22c9`.
- Physisch vorliegende Original-PHP-Klassen aus PSERC .28.63 ZIP (SHA256 `c8bde7a453cd8a6b4320fa3d9b2c8e79dce740334bfad959dd54c9d14e3de606`): `PSERC_Stable_Json`, `PSERC_Metadata_Boundary`, `PSERC_Admin`, `PSERC_Plan_Snapshot_Store`, PSERC-Reader und Compiler. `PSTE_Intent_Profile` aus PSTE .57.144.33 verwendet.
- Im Manifest steht `compiler_version=0.28.61` / `created_at_utc=2026-11-10T15:47:48+00:00`. **Das ist die gespeicherte Snapshotherkunft, nicht der Nachweis der derzeit installierten Plugin-Version**.

## Echter Test der aktuellen JSON

Lokaler PHP8.4-Test gegen Originalklassen: **28/28 PASS**. Originaler Manifesthash, unveränderter 5-Felder-Batch samt 3 Bindungen, Original-Metadatenprüfung und originale PSTE-Analysehashes **3/3 PASS**. Die Originale sind intakt.

**Nachgewiesene Sperrursache:**
- Alle drei `items[*].intent_profile` sind `phase=PRE_TYPE` mit `status=PASS`, `ok=true`, gültigem `analysis_sha256`.
- Sie haben **kein** `article_type`, **kein** endgültiges `search_intent`, **kein** `profile_sha256`. `PRE_TYPE/PASS` heißt **nur erste SEO-Analyse erfolgreich**, nicht vollständige Bindung an die endgültige Artikelart.
- Original `PSERC_Admin::existingManifestEnvelopeIsValid` akzeptiert das vollständige Manifest, `existingSeoOwnerProofIsValid` lehnt die drei Profile erwartungsgemäß ab. Die Datei `ohne-suchintent-nachweis` ist daher korrekt markiert.
- Im Original `PSTE_Intent_Profile::bindArticleType` ist der zweite Schritt `phase=BOUND_TYPE` implementiert; erst der setzt `article_type`, `search_intent`, `profile_sha256`. Der PSERC-Reader übernimmt den gespeicherten Kandidaten-`intent_profile` unverändert, der PSERC-Compiler kopiert ihn in `final_item`. Die fehlende Finalisierung entsteht **vor** dem Export. Nur die Export-Oberfläche umzustellen repariert das nicht.
- Die aktuelle JSON enthält **keinen** Original-`BOUND_TYPE`-Nachweis für die drei Artikel. Es darf kein neuer Intent aus Artikelart/Keyword/Providerwert geraten oder in K0 neu entschieden werden.

## Zusätzliche Export- und Negativsimulation

Acht bestehende PHP-Szenarien an der vollständigen PSERC .28.63 Exportfunktion mit lokal simuliertem WP-Speicher, **8/8 erwartetes Verhalten**:
- gültiges Profil → vollständiges Manifest,
- fehlendes/ungültiges Profil → vollständiges Manifest als unbewiesene Diagnose,
- fehlende Detailzeile und abweichende Bindung → explizite Diagnosecodes,
- beschädigter Ready-Index, ungültiger Header oder veralteter Plan → sicherer Stopp.

Weitere Negativproben in obigen 28 Tests: manipulierte Profil-/Manifesthashes, geänderter Intent/Artikeltyp/Planplatz, fehlendes Profil, nicht-READY-Artikel → alle korrekt gesperrt. Positivprobe mit **ausdrücklich synthetischem** `BOUND_TYPE`-Profil beweist nur den technischen Exportpfad, nicht die ursprüngliche fachliche Entscheidung.

## Verbindlicher nächster technischer Schritt

**Kein weiteres Plugin zur Installation anbieten**, solange die komplette lokale Ursachenkette nicht getestet ist. Zuerst den bestehenden PSTE-Weg von `analyzeBeforeType` über `bindArticleType` bis zum gespeicherten Kandidaten in der WordPress-TEST-Kopie mit vorhandenen Daten **lesend** untersuchen. Prüfen, warum der 3-READY-Plan nur `PRE_TYPE` enthält. Falls bereits existierende echte gebundene Originalprofile gespeichert sind, nur diese mit übereinstimmender Themen-/Planplatz-Identität in der bestehenden Übergabe nutzen; sonst keine vorgetäuschte Freigabe und keine automatische Neurecherche. Danach den gesamten lokalen PSTE→PSERC→K0-Quellenweg vor einer neuen Installationsdatei mit Positiv-/Negativtests abnehmen.

**Grenze:** Der Test verwendet echte exportierte WordPress-Daten und Original-PHP, aber keine direkte Verbindung zur tatsächlich installierten WP-Testdatenbank und keinen echten K0-Produktionslauf. Diese beiden Punkte **nicht** als bestanden ausgeben.

**Ergebnis:** `REAL_MANIFEST_VALID=PASS`, `OLD_BATCH_INTACT=PASS`, `UPSTREAM_FINAL_INTENT_PROOF=BLOCKED_PRE_TYPE`, `36_EXPECTED_LOCAL_CASES_PASS`, `INSTALL_RELEASE=NO`.
