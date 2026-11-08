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


## Checkpoint 2 – einmaliger SEO-Owner-Auftrag gesichert

**PASS (Vorbereitung):** `EVIDENCE/PSTE_EIN_SEO_OWNER_ECHTTEST_AUFTRAG_20261108.md` dokumentiert den **einen** ursprünglichen externen SEO-Owner, den tatsächlich erforderlichen kompletten WordPress-Export, korrekte Entscheidungsantwort `PSTE_MINI_SEO_DECISIONS_V1`, eindeutige Quellen und konkrete Problem-Keywords. Die unabhängige MINI-Titelwerkstatt wurde anhand ihrer echten `mini-title-gate/START_HERE.md` **nicht** fälschlich als SEO-Doppelbelegungsprüfer behandelt. Keine zweite redaktionelle Dauerschleife.

## Checkpoint 3 – ausführbare einmalige Original-Daten-Abnahme gesichert

**PASS (nur QA-Selbsttest):** Das **schon vorhandene** Testprogramm `QA_ONLY/test_single_existing_seo_worker_acceptance.py` wurde statt eines zusätzlichen Programm-/Runtime-Workers um zwei Aufrufarten ergänzt:

- `--preflight ORIGINAL_WORDPRESS_EXPORT.json` prüft ausschließlich technische Vollständigkeit und unveränderte Originalquellen: `parkhaus_complete`, alle fünf Pflichtquellen, gespeicherter PPM679-Plan als `PRESENT`, PSERC-Planversion, keine verlorenen JA-Quellschlüssel, keine duplizierten Quellidentitäten, korrekte `pool_key|raw_query`-Bindung, Titel vorhanden. Fehlt ein Quellbestand, bricht es ab statt eine SEO-Bewertung zu erfinden.
- `--verify ORIGINAL_WORDPRESS_EXPORT.json ECHTE_OWNER_ANTWORT.json [ORIGINAL_MINI100.json]` vergleicht **nur beim einmaligen Test des Owners** dessen Antwort mit dem echten Original: gleiche Bestandsversion, 1:1 vollständige Antworten, keine erfundenen oder doppelten Quellschlüssel/BELEGT-IDs, korrekte vorhandene Titel/Platzkennungen; das **bestehende** feste Fachfall-Abnahmeprogramm wird lediglich für die tatsächlich im Export vorhandenen 87 Original-JA-Quellen einmal verwendet. Die vorhandene Importfunktion bleibt die einzige spätere technische Produktübernahme; **keine zweite Runtime-Semantikprüfung**.
- `--io-selftest ORIGINAL_MINI100.json` testet die Eingangskontrolle und gezielte Negativfälle nur gegen **synthetische Testquellen**; daraus wird ausdrücklich kein reales SEO-Urteil abgeleitet.

**Tatsächlicher Lauf:** GitHub Actions `42464012917` **SUCCESS** (alte feste Original-Fachfall-Selbsttests + kompletter Quellen-/Antwort-Selbsttest mit 7 gezielten Fehlerfällen); `42464065463` **SUCCESS** zusätzlich gegen die **echten originalen** PSTE-v22-PHP-Klassen `PSTE_Repository::table`, `PSTE_Repository::allCandidates`, `PSTE_Snapshot::editorialPlan`: alle drei tatsächlich **public static** und vom vorhandenen Export verwendbar. Nicht nur angenommene Stub-Methoden. Die provisorische GitHub-Testworkflowdatei wurde **wieder gelöscht**.

**NOCH NICHT PASS:** Es liegt in diesem Arbeitszweig **kein** echter WP-Testexport und **keine** entsprechende reale SEO-Owner-Antwort vor. Der Testcode validiert nur die Bereitschaft des einen einmaligen Qualitätstests, **nicht** die fachliche Leistung des Workers in der Produktion oder einen WP-/K0-Durchlauf.


## Checkpoint 4 – vollständiger echter Testablauf gebündelt und gesichert

**Dokument:** `EVIDENCE/PSTE_ECHTTEST_STAGING_ABLAUF_20261108.md`. Es ist exakt festgelegt, welche Daten und Versionen im Test vorliegen müssen, wie **der eine** externe SEO-Owner einmal geprüft wird, welche beiden bereits vorhandenen Plugins den unveränderten Rückweg tragen, welche fünf Metadaten an PSERC/K0 gelangen dürfen und bei welchen konkreten Fehlern keine Artikel-Weitergabe erlaubt ist. Kein neuer Arbeiter/Plugin/Titelprüfer. Der unveränderte Redaktionsplan bleibt Lesebestand.

**Letzter ausführbarer Kontrolllauf:** GitHub Actions `42464305128` **SUCCESS**: 87 echte alte JA-Suchbegriffe als feste Fallgruppe, 100 Original-Keywords als Grundlage, 8 gezielt fehlerhafte **synthetische** Export-/Antwort-Situationen korrekt erkannt. Originale Methodenzugänglichkeit im echten PSTE-ZIP: `42464065463` PASS. Die Tests lassen die gesamte WP-/PSERC-/K0-Produktionsumgebung unberührt. Die temporären Workflows wurden anschließend aus dem QA-Branch gelöscht.

**NICHT verschweigen:** Der echte Staging-WordPress-Parkhaus-Export existiert in diesem geprüften Branch noch nicht; der tatsächlich angeschlossene externe SEO-Owner hat deshalb noch keine echten `FREI/BELEGT/KLAERUNG`-Entscheidungen geliefert. Ein echter Endlauf durch TEST-WordPress→PSERC→K0-Grenze ist nicht absolviert. Zudem ist der separate GitHub-Hardlock im aktuellen QA-Branch **nicht grün**; er wurde nicht verändert oder umgangen. Deshalb **weiterhin keine Installations-/Merge-/Live-Freigabe**. Der einzige nächste fachlich notwendige Originalinput ist ein vollständiger unveränderter Export aus der echten WordPress-Testinstallation; solange der exportierende QA-Stand dort nicht nachweislich installiert ist, muss vorher genau das eine bestehende Paar aus PSTE/PSERC kontrolliert als Teststand bereitgestellt und gesichert werden.

**Einzelner Prüfstand, keine weiteren Prüfer:** `QA_ONLY/test_single_existing_seo_worker_acceptance.py` kennt `--preflight`, `--verify`, `--io-selftest`. Die ersten beiden warten auf reale Dateien; letzteres wurde bestanden. Prüfergebnisse des externen Owners danach **nicht erneut semantisch in WP oder PSERC bewerten**.
