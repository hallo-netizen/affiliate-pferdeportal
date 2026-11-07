# Pferdeatelier MINI / KISS – ein Parkhaus, genau ein semantischer Eigentümer (Stand 07.11.2026)

## Gesicherter Stand und unverrückbare Grenze
- Rückfallpunkt: `backup/pste-mini-v22-before-kisten-20261107` (unangetastet).
- Getrennte, **nur testbare** Arbeitskopie: `fix/pste-kisten-einmalige-pruefung-20261107`, Draft-PR #682.
- Basis-Plugin: `PSTE-0.57.144.22-NUR-TEST.zip` unverändert und **nicht freigegeben**.
- K0, PSERC-Plugin, WordPress LIVE und geschützte GitHub-Workflows **nicht verändert**.
- Keine neue PHP-Klasse, WordPress-Tabelle, zusätzliche fachliche Prüfstelle oder neue Laufzeitarchitektur im erzeugten QA-Plugin. Ändert ausschließlich die schon existierende Klasse `PSTE_Mini_Workflow` in einer **nicht installierfreigegebenen Arbeits-ZIP**.

## Vollständig durchgeführter vorhandener Quellenabgleich
Das echte PSERC-0.28.53-Paket liegt in der bestehenden Library `/Pferdeatelier/TempVerify/PFERDEATELIER_PSERC_0.28.53_GESAMT_KISS_NUR_TEST.zip`, SHA256 `80340faff2323e5ede86ddd095ac3570a53474ae64771df3bec70fb6f6c6f060`; Paket hier physisch gelesen und Quelle nachgeprüft. Folgende EXISTIERENDE Funktionen/Verträge sind belegt:
- `PSERC_Plan_Snapshot_Store::getActive()`, `verifyHeader()`, `getRecord($generation,'final_item',$index)`, `counts.compiled_items`, aktive Generation, Fingerprint über `PSERC_Plan_Dependency_Fingerprint::isCurrent()`.
- PSERC speichert **alle** finalen Themen, darunter READY, HELD, REVIEW und BLOCKED, nicht nur READY.
- PSERC 0.28.53 macht im Compiler noch **inhaltliche Dublettenvergleiche** für gewisse WordPress-Status und innerhalb seiner Kandidaten; diese dürfen nach einer künftig gültigen zentralen externen Entscheidung **nicht nochmals fachlich durchgeführt** werden. Vor einer verifizierten externen Entscheidung keine ungeschützte Abschaltung vornehmen.
- PSTE v22 `PSTE_Snapshot::inventory()` umfasst nur `post` publish/draft, `manualArticleBrief()` maximal 1200/1200 und PSERC nicht vollständig. Die neue **reine Datenübergabe** nutzt diese Begrenzungen nicht, ohne die globale Produktions-Snapshot-Funktion zu verändern.

## Neue Testintegration – KISS, Aufgaben sauber getrennt
Die vorhandene `PSTE_Mini_Workflow` hat in der aus Original-ZIP gebauten isolierten QA-Fassung:
1. **Relevanz- und Titelstrecke UNVERÄNDERT KLEIN:** `exportKeywords()` erhält KEINEN großvolumigen Parkhausplan. Ein Agent bekommt nur die Daten für seine Aufgabe.
2. **Genau ein vorhandener Exporthandler für den SEO-Eigentümer:** `exportResults()` gibt auf ausdrücklichen bestehenden Admin-Aufruf mit `include_parkhaus` den aktuellen Gesamtbestand dazu; normale Titel-/Korrekturexporte bleiben klein. Keine zweite API, kein zusätzlicher Agent.
3. **WP-Bestand nur LESEN:** Öffentlich erreichbare Inhaltsarten einschließlich post/page/öffentliche eigene Arten, die Zustände publish/draft/future/pending/private; Titel, Focus-Keyword, Überschriften, Status und Identitäten, ohne Volltextpakete an die KI zu verteilen. Seitenweise Abfrage ohne künstlichen 1200er-Cutoff.
4. **PSTE-Plan LESEN:** gültige gespeicherte YES/PROVISIONAL-Planungen mit Originalfrage, Zielsuchbegriff, Artikelart, Kategorie und vorhandener `candidate_id`.
5. **Importierter Redaktionsplan LESEN:** bestehendes `PSTE_Snapshot::editorialPlan()` einschließlich ausdrücklicher Angabe `NOT_AVAILABLE`.
6. **PSERC-Endplan LESEN:** wirklich aktive, quellen- und altersgeprüfte finale Planergebnisse (auch HELD/REVIEW), inklusive vorhandener `seo_topic_id` und `canonical_article_id`. Gleiche PSTE-/PSERC-`seo_topic_id` erlaubt Identifikation **derselben Sache** statt einer erfundenen doppelten Suchabsicht.
7. **Nur technische Vollständigkeit und Version:** Fehlerhafte, geänderte oder unvollständige Quellen `complete=false`; ausdrücklich **kein** SEO-/Suchintent-/Titelentscheid und damit **keine FREI-Freigabe**.
8. **Vorheriger per-Topic-Importfix bleibt enthalten:** eine schlechte Ergebniszeile → vorhandene KLÄRUNG im WP-Optionsbestand; gültige Geschwister laufen weiter. Paketmanipulation/DB-Ausfall bleiben globale technische Sicherheitsstopps.

Quellcode in `QA_ONLY/pste_kisten_complete_parkhaus_method.inc`, `QA_ONLY/pste_kisten_pserc_plan_method.inc` und einmaliger Build nach `QA_ONLY/apply_existing_mini_kisten_import.py`. Das sind **Entwicklungsquellen**, nicht zusätzliche produktive Plugins/Worker. Die endgültige bestehende Plugin-Klasse wird nur im lokalen TESTZIP geändert.

## Tatsächliche Tests und konkrete Ergebnisse
- GitHub Action `42392148389`: **PASS** für die finale KISS-Quellintegration, inkl. fehlerhafter Einzelzeilen, PSERC READY/HELD, WP custom/private/Überschriften, vorhandener Fokus-Keyword/Canonical-ID, PSTE-/PSERC-Gleich-ID, geändertem WP-Bestand und kaputtem PSERC-Snapshot. **83/83 PHP-Syntaxprüfungen PASS**.
- GitHub Action `42392019818`: **PASS** für unveränderten kleinen Titel-/Relevanzexport, getrennten vorhandenen SEO-Gesamtexport und Nichtfreigabe bei fehlenden Daten.
- Vorherige Aktionsläufe `42389959640` und `42387802824` prüften den isolierten Import und die rein technischen Kistenfälle.
- Sämtliche temporären GitHub-QA-Workflowdateien nach den Tests wieder entfernt. Keine geschützten GitHub-Workflowdateien in finalem Arbeitsdiff.
- Tests sind **echte PHP-Ausführungen mit nachgestellten WordPress-Daten**, plus reale Quellprüfung der gespeicherten PSERC-0.28.53-ZIP. Sie sind **kein 1:1-Test der echten WordPress-Datenbank**, keine Live-Messung, keine semantische KI-Gegenprobe und kein produktiver End-to-End-Lauf.

## Noch offen: Grundursachen, nicht "durch neue Fixes überbauen"
1. Der tatsächliche vollständige Gesamtbestand muss im WordPress-TEST einmal mit echten Daten, Status, WP-Fokus-Keywords und aktiven PSTE/PSERC/Redaktionsplänen nachgewiesen werden. Nur öffentliche bzw. öffentlich abfragbare Inhaltsarten werden derzeit automatisch enumeriert; weitere nichtöffentliche **SEO-relevante** Inhaltstypen müssen anhand der realen WordPress-Registrierung ermittelt werden. Bloßes `complete=true` in einem Mock ist **kein** Live-Vollständigkeitsbeweis.
2. Der **vorhandene externe SEO-Entscheider** muss genau einmal dieselben Themen gegen diesen vollständigen Bestand und andere Themen im selben Stapel fachlich entscheiden, mit Gegenproben `2er`/`zwei Pferde`, `0g`/`ungefüttert`, günstige Regendecken, Vergleich/Test und verschiedenen Horseware-Longtails. Dafür ist eine wirklich ausführbare sprachfähige externe Prüfstelle inkl. automatischem Rückweg weiterhin nicht nachgewiesen.
3. Erst wenn die eine Entscheidung **beweisbar** mit Originalfrage, Bedeutung, Planversion und Quellbeleg zurückkommt, den bisherigen zusätzlichen WP- und PSERC-**semantischen** Prüfpfad für *genau diese* Fälle umgehen und den vorhandenen Status übernehmen. WordPress nur technischer Quellen-/Frische-/Kollisionsempfang; K0/PSERC bestehende Produktionsgrenzen behalten. Bis dahin **nicht** in WordPress die alten Sicherheitsprüfungen abschalten.
4. 87 ursprüngliche MINI-JA-Fälle plus echte WordPress-Stagingfälle und fehlerhafte/unsichere Fälle bis zur bestehenden K0-Grenze durchspielen. Ohne diesen Beleg keinerlei Release oder neue Installerfreigabe.

## Schluss
**Echter Fortschritt an einer Ursache: Der vormals unvollständige Datentransport bekommt jetzt einen aus dem bestehenden System gespeisten, kenntlich vollständigkeitsgeprüften Eingang für EINEN SEO-Eigentümer.** Die Doppel-SEO-Prüfung ist in Produktion noch NICHT beseitigt; sie darf ohne bewiesenen externen Einzelentscheid nicht blind entfernt werden. Bisheriger Rückfallstand und installierte Systeme bleiben unangetastet.
