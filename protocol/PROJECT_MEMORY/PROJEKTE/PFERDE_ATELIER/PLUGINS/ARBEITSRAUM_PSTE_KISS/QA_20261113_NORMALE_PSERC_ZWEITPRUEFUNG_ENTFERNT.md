# Pferdeatelier – KISS: nachgelagerte doppelte Themenentscheidung im normalen PSERC-Weg entfernt

**Stand 13.11.2026, nur QA / nicht installieren.**

## Ausgang – Originalcode und genaue Notwendigkeit

- Verbindlicher letzter Arbeitsstand ist `KISS_ZENTRALE_DOPPELTHEMEN_KLAERUNG_NUR_QA_20261112.zip`, SHA256 `2fc5b1bd7f37d5be433da4c19acb99c4bd597ddd948b247abfe254e78e47a974`.
- Original-PSTE `.45` und Original-PSERC `.69` liegen unverändert in der neuen Datei, mit identischen SHA256 `d3057946defc035af7abe5522c4845625c98ebd3f2cf621e1b3c5ce019f230a4` und `576e58b51db3f348210dc3d47a894d6551558acc0c6900505be5e11257d2e41b`.
- **Originalfehler nachgewiesen**: `PSERC_SEO_Reader::normalizeCandidate` bindet nur für alte MINI-SEO-Quittungen eine endgültige zentrale Themenentscheidung. Die normal vom PSTE-Themenpool freigegebenen Kandidaten bleiben ungebunden. Danach bewerten `PSERC_Compiler::compile` und `PSERC_Plan_Compile_Job::tickCandidate` deren Themenüberschneidung **erneut**, obwohl der vorhandene `PSTE_Planning_Readiness_Gate` bereits `pre_title_duplicate_gate` und `cannibalization` als PASS entschieden hat. `PSERC_Portal_Topic_Evidence_Gate::evaluate` wiederholt im normalen Weg zusätzlich fachliche Nachweiskriterien.
- Das widerspricht ausdrücklich dem KISS-Zielvertrag **ein fachlicher Entscheider vor den nachfolgenden Workern**. Bloße Freigabe ohne vollständige Quelle wäre aber unsicher.

## Einzige gezielte Änderung im bestehenden Weg

1. `class-pserc-seo-reader.php`: übernimmt die bereits bestehende, finale `PSTE_Planning_Readiness_Gate`-Freigabe als vorhandenen Quellbeleg **nur bei** `PASS`, `YES`, abgeschlossener Recherche, bestehenden PASS-Dubletten-/Kannibalisierungsnachweisen, vollständigem K0-Status und ohne Klärungs-/Sonderfall. Der bereits vorhandene MINI-Einmalentscheid bleibt unverändert.
2. `class-pserc-compiler.php` und `class-pserc-plan-compile-job.php`: wiederholen bei gültigem, aus PSTE übernommenem Beleg den semantischen Doppelthemenvergleich **nicht**. Ohne Beleg läuft die ursprüngliche konservative Prüfung unverändert.
3. `class-pserc-portal-topic-evidence-gate.php`: übernimmt denselben belegten zentralen Endentscheid; prüft weiterhin rein technisch, dass der Auftrag vollständig, freigegeben und weder gesperrt noch zur Klärung vorgesehen ist.
4. Bereits bestehendes `contracts/compiler-package-binding-v1.json` auf tatsächlich geänderte Dateien aktualisiert. Der frühere QA-Ausgangsstand hatte bereits **eine** Paketabweichung in `class-pserc-plan-dependency-fingerprint.php`; dieser vorhandene Drift wird in derselben Dateiliste korrigiert. **Kein** neues Manifest, keine neue Tabelle, kein neues Plugin, kein weiterer Worker, keine Titel-/Kategorie-/SEO-Neuentscheidung.

## Tests und Grenzen

- **24/24** echte Methodenproben `PSERC_SEO_Reader::normalizeCandidate` und `PSERC_Portal_Topic_Evidence_Gate::evaluate`, darunter bewusst: echte Dubletten, Klärung, unvollständige Recherche, fehlende Kategorie, manuelle Freigaben, nicht-K0-Routen, verbotene Daten und beschädigte Ownerbelege. Kein Fehlfall darf den neuen Weg nutzen.
- **8/8** echte `PSERC_Plan_Compile_Job::tickCandidate`-Aufrufe: mit gültiger Quelle Überschneidungs-Nachprüfung übersprungen; ohne Quelle ursprünglicher Vergleich weiter ausgeführt. Weiterverwendung des originalen, fortsetzbaren `candidate_work`-Speichers.
- **11/11** bereits eingeführte echte PSTE-Gegenproben zur Bedeutung „gleiches Keyword, anderer Informationsbedarf“; Sperre bei tatsächlicher Dublette, KLÄRUNG bei bloßer Titelgleichheit.
- **159/159** Originaltest an 87 früher geprüften Keywords und dem echten 1179er-Bestand; weiter **61 FREI / 20 BELEGT / 6 KLÄRUNG**.
- **18/18** bisheriger Offline-Gesamtablauf, dabei sind Titelworker, K0, PPM-Schreibfunktion und WordPress-Daten **nachgebildet**; zwei Mock-Entwürfe, **kein echter Artikel**.
- **126/126** PHP-Syntaxprüfungen; **PSERC_Package_Integrity::validate() PASS** für alle **61** Original-Dateieinträge im existierenden Vertrag.
- Exakter Codevergleich liegt in `QA_PSERC_QUELL_DIFF.patch`, maschinenlesbarer Bericht `QA_ABNAHME.json`, QA-Skripte im Paket. **Nur vier bestehende PHP-Dateien + vorhandene Datei-Integritätsliste geändert.** Keine PSTE- oder PPM-Pluginquelle verändert.

## Nicht erledigt und deshalb nicht für WordPress freigegeben

- Die tatsächliche dauerhafte Buchung eines Canonical-Artikelplatzes in der PPM-Planverwaltung **vor MINI** ist noch nicht umgesetzt oder gegen echte WordPress-Schreibvorgänge getestet.
- MINI exportiert noch Rohkeywords einschließlich der alten JA/NEIN/VIELLEICHT-Rolle; diese Aufgabentrennung ist noch nicht programmiert.
- Ein automatischer echter Titelworker, K0-Artikel, WordPress-Datenbank-Import und vollständiger Produktionslauf wurden nicht ausgeführt.

**Fachliches Ziel unverändert**: zentrale Themenentscheidung einmal → Platz dauerhaft vor MINI reservieren → MINI nur Titel → PSERC nur Metadaten/technische Zuordnung → K0 schreibt → WordPress importiert. Die Änderung ist eine gesicherte Vereinfachung **innerhalb** dieses Ablaufs, keine zusätzliche Schleife.