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
