# Pferdeatelier – echter Endtest: Vorbereitung und Checkpoints, 08.11.2026

**Arbeitsort:** strikt isolierter QA-Branch `fix/pste-kisten-einmalige-pruefung-20261107`, Draft-PR #682. **Kein Release, keine Installation, keine Änderung an K0, Sicherheitsworkflows, Produktionsdaten oder gespeichertem Redaktionsplan.**

## Checkpoint 1 – vorhandene Grundlagen tatsächlich geprüft

- Die bereits vorhandene MINI-Runde enthält **100 echte Original-Keywords** und 97 ursprüngliche Titelvorschläge, davon 87 JA, 9 VIELLEICHT, 4 NEIN. Quelle `QA_ONLY/MINI_100_ORIGINAL_EXTERNAL_TITLES_20261106.json`. Die 87 JA sind **keine** echten SEO-FREI-Urteile.
- Die bestehende MINI-Schaltfläche **„Redaktionsstand für einmalige SEO-Prüfung exportieren“** (nur im isolierten QA-Patch, nicht als installiert nachgewiesen) exportiert `seo_subjects` (wirkliche WP-pool_keys, Rohsuchanfrage, Quellenfingerabdruck) plus den unveränderten `parkhaus_snapshot` aus WordPress, PSTE, optionalem PSTE-Redaktionsplan, dem aktiven PSERC-Plan, bereits gespeicherten PPM679-Artikelplätzen und früheren MINI-Reservierungen. **Keine zweite Datenhaltung.**
- Die separate Titelwerkstatt in `mini-title-gate/START_HERE.md` beurteilt **Sprach- und Titelqualität**, nicht die **SEO-Doppelbelegung** gegen den aktuellen Portalplan. Sie darf nicht fälschlich als SEO-Abnahme ausgegeben werden.
- Der vorliegende PSERC-Teststand 0.28.54 ist nur eine isolierte QA-Kopie des Original-0.28.53. Der PSERC-Quellvertrag `class-pserc-seo-source-binding.php` prüft die stabile **Lese-Fähigkeit**, nicht pauschal die Bytegleichheit der PSTE-Dateien. Tatsächlicher gemeinsamer WordPress-Start beider QA-Pakete ist trotzdem **nicht nachgewiesen**.
- Gesicherte letzte technische Gesamtprobe: GitHub Actions `42463449175` SUCCESS, 100 echte MINI-Quellen, simulierte SEO-Urteile, keine zweite WordPress-SEO-Bewertung, geprüfte technische Planweitergabe mit Fehlerfällen, 83/83 PSTE-PHP-Syntax PASS.

## Was genau noch fehlt

**A – Vollständige echte Quelle:** Ein **frischer read-only Export von der vorhandenen Test-WordPress-Instanz**. Der Export muss `parkhaus_complete=true` liefern; vorhandener Redaktionsplan ist nur eine Quelle und darf weder neu erstellt noch gelöscht werden. Kein Teilausschnitt oder veralteter 100er-Mock wird als vollständiger realer Portalbestand akzeptiert.

**B – Genau ein externer SEO-Owner:** Eine **einzige** fachlich verantwortliche Beurteilung aller tatsächlich exportierten JA-Quellen mit `FREI/BELEGT/KLAERUNG`, realem Quellenbeleg für BELEGT, eindeutigem Suchintent/Platz für FREI. Keine neue WordPress-SEO-Prüfung, kein „Titel anders = freier Artikel“. Vermeintliche Mehrfachthemen werden innerhalb derselben einen externen Auswertung zusammengeführt/klärt; erhaltene Titelvorschläge werden nicht von dieser Phase neu formuliert.

**C – Technische Übernahme/Test bis PSERC-K0-Grenze:** Nur gültiger vollbestandgebundener Owner-Rückimport in das **vorhandene** MINI-Importformular und die **vorhandene** Weitergabe. Danach echter Staging-WordPress/PSERC-Leselauf mit **genau fünf Metadatenfeldern** (Titel, Keyword, Kategorie, Artikeltyp, Artikelplatz); keine neue Artikelproduktion und kein K0-Quellumbau. Belegte/veränderte Slots, fehlerhafte Einzelantworten und Stale-State dürfen keine Freigabe erhalten.

## Vereinbarte KISS-Regel

Nach einmaliger fachlicher Abnahme die Qualität des EINEN bestehenden externen SEO-Workers **nicht bei jedem Thema durch einen zweiten Worker wiederholen**. Es bleibt nur die technisch notwendige Quellen-/Versions-/Slot-Prüfung beim Import. Frühere erfolgreiche, unveränderte Stufen werden nicht erneut geprüft.

## Zwischenstände

- **Checkpoint 1: gesichert** – Planung auf Grundlage wirklich vorhandener MINI-, WordPress- und PSERC-Funktionen. Kein Versuch, die noch fehlende echte Bestandsdatei zu erfinden.
- Checkpoint 2: konkreter einmaliger Prüfauftrag und Eingabe-/Ausgabeformat inklusive Abnahme des vorhandenen SEO-Owners.
- Checkpoint 3: vor echtem Import ausführbare technische Quellen-/Versions-Gegenprobe und Fehlerfälle.
- Checkpoint 4: vollständige Simulations-/Kompatibilitätsprobe mit vorhandenen PSERC-Klassen; dann Endbericht zur Staging-Bereitschaft.

**Freigabegrenze:** Unvollständiger WP-Export, fehlende reale Owner-Antwort oder fehlende echte WP→PSERC-Stagingprobe bedeuten **NICHT FREIGEGEBEN**.
