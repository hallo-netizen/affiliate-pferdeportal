# Pferdeatelier MINI – Gesamtsimulation und echte Integrationsgrenzen (07.11.2026)

**Ergebnis:** Technischer MINI→WordPress→Plan→PSERC→5-Felder-K0-Grenze-Weg in getrennten Tests anhand der **tatsächlich vorhandenen Klassen**, unter simulierten externen SEO-Urteilen und nachgestellten WordPress-Daten, geprüft. **Nicht** gleichbedeutend mit bestandenem echten LIVE-WordPress/PSERC/K0-Endlauf oder der Qualität eines echten automatischen externen SEO-Entscheiders. **KEINE Plugin-Installationsfreigabe.**

## Ausgangspunkt und Versionsschutz
- Bewahrter Fallback: `backup/pste-mini-v22-before-kisten-20261107` (ursprüngliche PSTE 0.57.144.22 Test-ZIP unverändert).
- Ausschließlich Arbeitsbranch `fix/pste-kisten-einmalige-pruefung-20261107`, Draft-PR #682. K0, PSERC 0.28.53 aus Library, LIVE, bestehender Plan und Original-GitHub-Sicherheitsdateien nicht geändert.
- Zusätzlich **separat nur lokal geprüftes** PSERC 0.28.54 QA-Archiv aus der byteverifizierten Library-v0.28.53 mit Änderungen ausschließlich an drei **bereits existierenden** PHP-Klassen und Versions-/Paketbindung. Keine neuen Klassen, Tabellen oder Semantikworker. Original PSERC Plan-Snapshot-Verfahren bleibt gleich.

## Einmalige Aufgaben / keine doppelte Inhaltsprüfung
1. Bestehendes MINI gibt originale Recherche-Keywords aus; externer Relevanzworker beurteilt nur Portalbezug, externer Titelworker formuliert Titel (keine WordPress-Sprachbewertung).
2. Einzige externe SEO-Autorität erhält den vollständigen aktuellen lesenden WP/PSTE/importierten Redaktionsplan/PSERC-Endplan plus bestehende Reservierungen (vorhandene Daten, **kein** neuer Parallelplan). Sie unterscheidet `FREI`, `BELEGT`, `KLÄRUNG` **ein einziges Mal**. Kein zweiter Sprach-, SEO- oder Keywordworker.
3. Vorhandener MINI-Admin-Rückimport empfängt dieses Ergebnis **technisch gebunden** an Original-Suchfrage, Titel und Parkhaus-Snapshot. Einzelfehler nach `KLÄRUNG` und die übrigen Fälle weiter. `FREI` nur bei belegbar gleichen Quellen/Intentslots. Fehlender/falscher SEO-Beleg wird **nicht** durch einen selbstständigen WordPress-SEO-Gate ersetzt.
4. Bestehende `PSTE_Planning_Readiness_Gate::apply` **übernimmt** für externe MINI-Entscheidungen das gespeicherte Ergebnis **ohne** `preTitleDuplicate` und `PSTE_Cannibalization::decide`. Für nicht extern entschiedene historische Themen bleibt der ursprüngliche Prüfpfad.
5. Bestehende `PSTE_Mini_Workflow::forwardToPlan` nutzt nur `FREI`. Genau eine **technische** Gesamtstand-Frischekontrolle vor dem Rückweg; bei alter Quelle wird nur der betroffene externe Themenstapel geklärt. Technisch fehlerhafte Einzelbeiträge nicht den ganzen Stapel stoppen; bei keinem freigegebenen Thema ordnungsgemäß ohne Fehlerschleife abschließen. Derselbe bisherige Plan-/Reentry-Weg wird verwendet.
6. In den bestehenden PSERC-Klassen `PSERC_SEO_Reader`, `PSERC_Compiler`, `PSERC_Plan_Compile_Job` wird die extern dokumentierte, aktuell gespeicherte `FREI`-Entscheidung an derselben Quelle/Titel/Slot technisch erkannt und **ohne PSERC-Zweitähnlichkeitsvergleich** übernommen. Nur für diese Fälle; keine Abschaltung der Altpfad-Sicherheit. Bestehende Kategorien-/PPM-/Zielkeyword-/Slot-/Metadatenregeln laufen unverändert.
7. Die ursprüngliche `PSERC_Metadata_Boundary` akzeptiert nur **exakt fünf reine Metadatenfelder** (Titel, Zielkeyword, Kategorie, Beitragsart, Planplatz), keine Artikeltexte oder Veröffentlichungen. K0 bleibt völlig unangetastet.

## Tatsächlich ausgeführte Prüfungen
- **Originalfälle 100/100:** unveränderte externe Quelle `QA_ONLY/MINI_100_ORIGINAL_EXTERNAL_TITLES_20261106.json` (aus `feature/mini-title-gate-independent-v1-20261104`, GitBlob `13051feaef974e57a7ec358cccaeb434679e750b`): 87 JA, 9 VIELLEICHT, 4 NEIN, 97 Originaltitel 1:1 übernommen.
- **Hypothetische externe SEO-Fälle** für alle 87 JA-Originalthemen: 1 FREI, 3 BELEGT, 83 KLÄRUNG (die 83 bedeuten **mangels echtem Live-Bestand unbekannt**, nicht fachlich negativ). Im echten `PSTE_Planning_Readiness_Gate::apply` von v22 **0** Aufrufe des bisherigen WordPress-SEO-/Kannibalisierungsvergleichs für diese 87. Fehlender externer Beleg bleibt zurückgestellt. Eine manipulierte Einzelantwort wird isoliert, **86 weitere** werden nicht angehalten. Veraltetes/fehlendes Gesamtinventar sperrt FREI-Übernahme. GitHub CI **42394799916** und finale **42395796933** (PASS).
- **Echte vorhandene `PSTE_Mini_Workflow::forwardToPlan`** mit nachgestellter DB ausgeführt, drei Fälle im CI **42395796933** (PASS):
  - GOOD: 1 FREI geht genau einmal zur vorhandenen Planung, BELEGT/KLÄRUNG nicht.
  - STALE: 0 weiter, 1 in KLÄRUNG, keine erneute SEO-Bewertung.
  - ONEBAD: 1 gültiges FREI weiter, 1 defektes Einzelthema in KLÄRUNG.
  - 83/83 PSTE-PHP-Syntaxprüfungen bestanden.
- **Echte PSERC-0.28.53-Library-ZIP**: in lokaler QA-Arbeitskopie nur die drei bestehenden PHP-Klassen angepasst (Original unverändert). `PSERC_SEO_Reader::normalizeCandidate()` mit Originalquellen gebunden getestet, **7 PASS**: gültiger externer SEO-Beleg wird erkannt; geänderter Titel/Slot nicht; fehlende Kategorie, gesperrter Artikel und eingeschmuggelter Artikelinhalt bleiben gesperrt.
- **Echte bestehende `PSERC_Plan_Compile_Job::tickCandidate()`** per PHP ausgeführt, **8 PASS**: bei gültiger Fremd-SEO-Entscheidung direkt in die vorhandene technische Planstufe, **0** zweite semantische PSERC-Vergleiche; vorherige technische und redaktionelle Nachweise bleiben.
- **Original PSERC-`Metadata_Boundary::validateBatch()`** mit tatsächlicher 0.28.53-Quelle, **6 PASS**: fünf Felder, fehlende Kategorie, gleicher Titel/Slot, Inhaltseinschleusung, Veröffentlichen verboten. `PSERC 0.28.54` QA-Bau mit derselben Paketstruktur und neu gebundenen 61 Pflichtdateien: **61/61 Integrität PASS, 43/43 PHP Syntax PASS**, 63 ZIP-Dateien unveränderte Paketstruktur. Nur **QA**, kein Endnutzerpaket.
- Getesteter unveränderter PSERC-Quellplan: der bestehende Plan enthält auch HELD/REVIEW, nicht nur READY. Der neue Parkhausleser nutzt *denselben* PSERC-Snapshotstore; kein weiterer Plan.

## Grenzen / Releaseblocker (nicht vertuschen)
1. Die 87 externen SEO-Urteile sind für die Simulation **als testweise Szenarien gesetzt**, nicht von einem tatsächlich angeschlossenen externen KI-SEO-Agenten aus vollem live Stand autonom entschieden. Die bisherigen semantischen Fehl-PASS bei `2er`/`zwei Pferde`, `0g`/`ungefüttert` sind **in der Fachautorität nicht nachgewiesen behoben**. Der alte v22-Gate ist in der neuen MINI-Lane umgangen, nicht fachlich repariert. Alte Themen laufen weiterhin über den alten Pfad.
2. Der WP/PSTE/PSERC-Bestand wurde auf **nachgestellten** Daten technisch geprüft; die echte WordPress-DB, alle nichtöffentlichen SEO-relevanten Inhaltstypen und die vollständige Live-Kategorien-/Planaktualität sind **nicht durch einen echten Staging-E2E-Test belegt**.
3. Die PR-Schutzprüfung auf den aktuellen GitHub-Branches ist unabhängig von den hier bestandenen PHP-Gegenproben nicht erfolgreich abgeschlossen: bestehender trusted base fehlt der erwartete Pfad `control/paul-scope-gate/paul_scope_gate.py`. Keine eigene Sicherheits-/Hardlock-Umgehung.
4. Kein tatsächlicher K0-Produktionslauf, keine WordPress-Installation, keine Änderung am Redaktionsplan und kein Live-Fix. Die Tests prüfen **die Übergabegrenze**, nicht die Qualität des Artikels.
5. Solange die sichere autonome externe SEO-Prüfung samt echter Bestandsqualität und der reale TEST-Endlauf fehlen, bleibt die gesamte Arbeitsfassung **NICHT INSTALLIEREN**. Keine künstliche Freigabe durch nur synthetische Tests.

## Sicher auffindbare Quellen
- PSTE-QA-Aufbau aus unveränderter Original-v22: `QA_ONLY/apply_existing_mini_kisten_import.py`
- Vorhandenen WP-SEO-Gate nur für externe Fälle ersetzen: `QA_ONLY/apply_wp_single_owner_gate.py`
- Externe Belege und dieselbe bestehende MINI-Option: `QA_ONLY/pste_kisten_one_owner_receipt_methods.inc`
- Portalbestand aus echten vorhandenen Quellen: `QA_ONLY/pste_kisten_complete_parkhaus_method.inc`, `QA_ONLY/pste_kisten_pserc_plan_method.inc`
- Bestehende PSERC-Doppelung für externe Fälle ausschalten: `QA_ONLY/PSERC_EXISTING_OWNER_NO_SECOND_SEMANTIC_QA.patch`
- 100 echte Queries und eigentliche Tests: `QA_ONLY/MINI_100_ORIGINAL_EXTERNAL_TITLES_20261106.json`, `QA_ONLY/test_100_keyword_end_to_end_simulation.php`, `QA_ONLY/test_existing_forward_full_chain.php`.

**Technisches KISS-Fazit:** Das vorgeschlagene System kommt ohne neue Architektur, ohne zweite inhaltliche Prüfung und mit isolierten Fehlern auf den ursprünglichen Einzelstrecken aus. **Die technische Simulation dieser Strecken ist gelungen.** Die Realqualität des externen einzigen SEO-Entscheiders und ein vollständiger installierter WordPress→PSERC→K0-Test sind damit **nicht bewiesen**.
