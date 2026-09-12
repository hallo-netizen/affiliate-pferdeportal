# PRE-CODEX READINESS – STARTMASTER0107 / B01-ONLY – 2026-09-06

ROLLE: technische Vorlaufprüfung vor dem ersten neuen Codex-/Live-Lauf.
Keine zweite Fehlerwahrheit. Keine Fach-/Inhalts-/Architekturänderung.

## HARTE SCOPE-GRENZE

Zulässig:
- technische Hash-/Identitätsbindung;
- Handoff-/Gate-Reihenfolge;
- technische Ein-/Ausgabeartefakte;
- Stage-/Receipt-/Status-Logik;
- bestehende Positiv-/Negativtests;
- Vergleich letzter echter 7/7-Stand vs. aktueller Kandidat.

Tabu:
- Architektur;
- Fach-/Inhaltsregeln;
- Textmaschine;
- SEO;
- Link-/Tabellenregel;
- LanguageTool;
- PPM-/PSERC-/PSTE-Regeln;
- Design;
- Publish-Regeln;
- neuer Runner/Workflow/Gate/Executor.

## 1. KANDIDAT

Bevorzugter kausaler Kandidat:
- PR #141
- Branch: `hobbyroom/b01-only-kiss-20260906`
- Head: `94917596adce04765380c60dd7ade0fb23793393`
- Base/main: `c8a96e7a2f598de69134d90b143257c3559bc98a`
- Draft
- mergeable=true
- kein Merge

Scope:
- 4 Commits
- 4 geänderte Dateien
- keine B15-Signierbereinigung
- keine Fach-/Inhalts-/Regeländerung

Exakte Produktionscodeänderung in `fachworkflow_proof_handoff.py`:
- alter Guard: numerische Kategorie-ID + Slug
- neuer Guard: Name + Slug + Taxonomy=category
- Kopie `$seedItem=$item`
- nur `$seedItem` erhält lokale Test-/Seed-ID `900001`
- `nd_seed_terms([$seedItem])`
- ursprüngliches `$item` bleibt für den nachfolgenden echten Production-Plan unverändert.

Restliche drei Dateien ziehen ausschließlich die notwendige 107007-State-/Bundle-/Root-Hashkette nach.

## 2. GITHUB-BEWEISE AUF #141

### Deterministic Entrance Gate
Run `34042032115`:
- `GITHUB_ENTRANCE_GATE_CI_PASS`
- `CODEX_CLOUD_GATE_CI_PASS`
- positive_negative=PASS
- `PRODUCTION_CONTINUITY_POSITIVE_NEGATIVE_PASS` / 10 Fälle

### Immutable Base Hardlock
Run `34042032325`:
- exakter Candidate-Head `94917596…` gegen Base `c8a96e7…`
- nur die vier erwarteten Pfade geändert
- keine immutable Security-Pfade geändert
- `MONOTONIC_PREBOUND_TRANSITION_PASS`
- Candidate-State mit vertrauenswürdigem Base-Gate geprüft
- Cloud-/Continuity-Tests PASS

### Hash-/Authorized-Input-Bindung
Der unveränderte `cloud_entry.verify()` prüft:
- Root ↔ State SHA
- State ↔ Bundle SHA
- Bundle-Identität
- **jede** `authorized_inputs[].ref`-Datei gegen `authorized_inputs[].sha256`.

#141-`STEP_107007` bindet darunter:
- H8-Boundary
- runtime_entry_gate
- worker_freshness_guard
- Codex environment preflight
- output release gate
- final review visibility guard
- output visibility policy
- optimization policy
- runtime lifecycle
- room bridge
- current action
- DUAL rootfix
- `fachworkflow_proof_handoff.py` SHA `64d2e5…`
- PPM 6.7.9 ZIP SHA `acbda93…`
- PSERC-FIX ZIP SHA `77a14aca…`

Damit ist die gebundene technische Eingabekette auf #141 vor Codex PASS.

## 3. VERGLEICH MIT LETZTEM ECHTEN 7/7-/107008-PASS

Referenz: `de21f6cd35c60849c551fd82f78e75ce57c99fab`.

Identisch zwischen `de21f6…` und heutigem System:
- Generation 1
- Batch SHA `7f2e3290…`
- Source-Snapshot SHA `be73a986…`
- Source-Manifest SHA `8cb8d86b…`
- Production-Package SHA `6e8bd5b1…`
- Article-Type-Templates SHA `dc79a6d7…`
- Tabellenvertrag SHA `1ab3e892…`
- sieben Metadatenitems / alle Artikeltyp `Beratung`
- Fach-/Inhaltsregeln unverändert.

Entscheidender technische Delta danach:
- echter PPM 6.7.9 wird in 107007 zwingend real ausgeführt;
- PPM-/PSERC-Pakete werden exakt gebunden;
- finaler Artikel ↔ Production-Plan ↔ PPM-content_hash wird hart gebunden;
- Request → echter PPM → erst danach PASS/Receipt;
- Worker-/Context-Bindung wurde gehärtet.

Damit liegt die heutige Regression auf der technischen Kontroll-/Handoff-Strecke, nicht in Batch/Inhalt/Fachregel.

## 4. LIVE BEREITS ÜBERWUNDENER REAL-PPM-KORRIDOR VOR B01

Der letzte echte Lauf auf current main erreichte B01 innerhalb `_real_ppm_stage`.
Daher wurden im selben realen Lauf bereits passiert:

1. PPM-final_article_ref formal gültig;
2. finaler Artikel vorhanden und SHA korrekt;
3. kein vorgefertigter PPM-Report;
4. PPM-ZIP vorhanden und SHA korrekt;
5. PSERC-ZIP vorhanden und SHA korrekt;
6. Fact-Pack / Production-Plan-Item / Header als Kontext vorhanden;
7. `production_plan_item.canonical_article.body_html == finaler Artikel`;
8. finaler Artikeltext == `final_article_sha256`;
9. Canonical Article ID passend;
10. PPM-Slot gefunden;
11. Plan-Slot-Identität passend.

Diese Punkte NICHT erneut als Verdachtsursachen behandeln, solange der nächste reale Lauf keinen gegenteiligen neuen Beleg liefert.

## 5. AKTUELLER B01

Aktueller main-Blocker:
`BOUND_WORDPRESS_CATEGORY_ID_MISSING_FOR_REAL_PPM679_EXECUTION`.

Historischer Vertrag:
- Kategorieidentität = Name + Slug + Taxonomy;
- keine numerische WP-ID als SEO-/Upstream-Feld.

#141:
- prüft Name + Slug + Taxonomy;
- setzt numerische ID ausschließlich in lokaler `$seedItem`-Kopie für `nd_seed_terms`;
- Original-`$item` bleibt ID-los.

Vorhandener dokumentierter lokaler Original-PPM-Test des B01-Fixes:
- ID-los semantisch gültig → PASS
- falscher Name → BLOCKED
- falscher Slug → BLOCKED

Grenze:
Dieser lokale Original-PPM-Test ist dokumentiert, aber heute nicht unabhängig über GitHub Actions erneut ausgeführt worden.

## 6. NACH B01 – BEWUSST NOCH UNBEWIESENER KORRIDOR

Nach erfolgreichem Category-Seeding folgen erstmals im heutigen harten Real-PPM-Weg:

1. realer Fact-Pack-Import;
2. Source-Snapshot-/Source-Hash-Bindung;
3. Aufbau des Einzel-`production_plan_v4`;
4. `PSERC_PPM_Intake_Bridge::execute`;
5. innere PPM-Normal-Draft-Pipeline;
6. PPM-Reportidentität;
7. Technical PASS;
8. Content-Quality PASS;
9. `content_hash == final_article_sha256`;
10. finaler PPM-Stage-Proof;
11. FACHWORKFLOW_PASS;
12. ITEM_RECEIPT.

Keiner dieser Punkte wird prophylaktisch verändert.

## 7. PAUL-BEFUNDE – VORAB EINORDNUNG

### F2/A6/A12 – Pre-/Post-Transformation
- technisch realer Systembefund;
- gegenüber bisherigen Reparaturen neu;
- aktueller äußerer 107007-Handoff führt Affiliate-/Placeholder-Zustände nicht als eigene Schnittstelle;
- daher aktuell KEIN vorab belegter STARTMASTER-Blocker.

### F7/A7 – unerfüllbare Tabellenbedingung
- technisch realer Systembefund;
- stärkster vorbereiteter Kandidat innerhalb der inneren PPM-Pipeline;
- Tabellenvertrag und Article-Type-Templates gegenüber letztem 7/7 unverändert;
- kann durch jetzt erstmals zwingend real ausgeführten PPM-Pfad relevant werden;
- aber erst nach B01 erreichbar → **kein Vorab-Fix**.

### A11 – unterschiedliche Hash-Semantik
- realer Systembefund;
- äußerer STARTMASTER-Weg arbeitet bereits mit `final_article_sha256 ↔ PPM content_hash`;
- `validated_content_hash` ist keine sichtbare aktuelle 107007-Schnittstelle;
- zurückstellen bis konkreter innerer PPM-Fehler darauf zeigt.

## 8. M01–M33

Bekannt:
- kompletter bestehender Runner auf breiterem #140-Head `3ed31aa…`: M01–M33 GESAMT PASS.
- #141 ist ein früherer reiner B01-Prefix direkt auf main.

Nicht behaupten:
- kein neuer kompletter M01–M33-Lauf auf exakt #141.

Grund:
Auf #141 existiert kein bestehender GitHub-Workflow, der M01–M33 unverändert ausführt. Ein neuer/temporärer Runner oder Workflow ist durch die Hard Rule verboten. Kein künstlicher PASS.

## 9. ERSTER CODEX-/LIVE-LAUF – STOP-REGEL

Vor Lauf:
- #141 nur nach ausdrücklicher Nutzerfreigabe integrieren;
- danach neuen current-main-SHA notieren;
- Preflight/current-main identity prüfen.

Dann:
- exakt bestehender produktiver 7er-Lauf;
- keine Alternativroute;
- kein neuer Canary-/Runner;
- keine WordPress-Schreibaktion;
- beim **ersten** realen BLOCKED sofort STOP.

Fehlerauswertung nur:
1. exakter Blocker;
2. exakter Ort in obigem Post-B01-Korridor;
3. Gegencheck Fehlerhistorie;
4. Gegencheck Paul-Landkarte;
5. ein KISS-Fix nur bei reproduziertem technischen Widerspruch.

## 10. PRE-CODEX-GESAMTURTEIL

Vor Codex seriös belegt:
- B01-only ist sauber isoliert;
- Hash-/Binding-/Entrance-/Continuity-Kette auf #141 PASS;
- kein Fach-/Inhalts-/Architekturdiff;
- gleicher reale Batch wie letzter erfolgreicher 7/7;
- technischer Regressionskorridor zeitlich eingegrenzt;
- alle bereits live überwundenen Vor-B01-Checks identifiziert;
- Post-B01-Unbekannte vollständig als Beobachtungskorridor kartiert;
- Pauls Befunde gegen bisherige Versuche und aktiven Pfad abgegrenzt.

Nicht seriös vor Codex beweisbar:
- echter B01-Live-PASS;
- echter Post-B01-PPM-PASS;
- kompletter M01–M33-Lauf exakt auf #141 ohne verbotene neue Testhülle;
- 7/7 + 107008.

Daher: **kein weiterer Produktionscode-Fix vor dem ersten realen Lauf.**
