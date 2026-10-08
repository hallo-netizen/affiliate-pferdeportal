# HOBBY DEPOT – HOBBY MASTER V2 – CURRENT DATA POINTER

STAND: 2026-10-08
STATUS: AKTIVES 841ER INVENTAR / REGELN 1.5 PRAKTISCH / BATCH 001–003 NUR KALIBRIERUNG / BATCH 004+ GESTRICHEN / 340 CORE + 501 FINDER-EDITORIAL / V1.13.1 FINALZIEL LOKAL PASS / LIVE-DRYRUN OFFEN

## Datenartefakt

Persistente Ablage:
`/hobby rausch/HOBBY_DEPOT_HOBBY_MASTER_V2_20261007.json`

SHA-256:
`a4cae906ce4f9fefcc805b8c83fc746859d508d32f3e2f981f01f6d26f7353b7`

Format:
`hobby-depot-hobby-master`

Schema:
`2.0-draft`

## Bestand

- 908 Rohzeilen;
- 844 exakte unterschiedliche Namen;
- 841 kanonische Identitäten nach aktuell bekannten Alias-Zusammenführungen;
- 329 vorhandene V1.12-Monetarisierungs-/CORE-Regeln übernommen;
- davon 286 DIRECT;
- 43 ASSISTED;
- 512 derzeit monetarisierungsseitig UNKNOWN;
- UNKNOWN bleibt erhalten und wird nicht gelöscht;
- 19 Research-Queue-Kandidaten liegen zusätzlich außerhalb der 841 aktuellen Identitäten;
- Intake-Check: 0 exakte/current-Alias-Kollisionen;
- Fotografie ist als erstes provisorisches Intake-Delta vorbereitet, aber noch nicht in das Quellartefakt materialisiert.

## Rollenmodell

Mögliche spätere Publikationsrollen:
- ORIENTATION_UNIVERSE
- HOBBY_HUB
- EDITORIAL_TOPIC
- ARTICLE_ONLY
- FINDER_ONLY
- OUT_OF_SCOPE

Aktuell ist der Großteil bewusst `UNASSESSED`.
Keine Massenfreigabe aus dem Master ableiten.

## Geschützte Architektur

- Gestalten
- Fertigen
- Technik
- Forschen
- Pflanzen
- Tiere
- Bewegen
- Sammeln

Diese acht Welten bleiben im ersten Integrationslauf geschützt.

## Neue Research Queue

Bekannte/breite Hobby-Kandidaten werden zunächst nur geprüft, nicht automatisch publiziert:
Fotografie, Malen, Zeichnen, Nähen, Stricken, Häkeln, Holzwerken, Heimwerken, Wandern, Radfahren, Camping, Schwimmen, Klettern, Bouldern, Gärtnern, Gemüseanbau, Briefmarken sammeln, Angeln, Plane Spotting.

## Autoritative Konzeptreferenzen

- `KONZEPT/HOBBY_GROESSEN_ROLLENMODELL_20261007.md`
- `SEO_KATEGORIEN/HOBBY_MASTER_V2_INTEGRATION_20261007.md`
- `SEO_KATEGORIEN/HOBBY_MASTER_V2_PILOT_20261007.md`

## Bewertungsartefakte

- Regeln: `../../SEO_KATEGORIEN/HOBBY_MASTER_V2_ASSESSMENT_RULES_20261007.json`
- Batch 001: `../../SEO_KATEGORIEN/HOBBY_MASTER_V2_BATCH_001_RESULTS_20261007.json`
- Research Intake: `../../SEO_KATEGORIEN/HOBBY_MASTER_V2_RESEARCH_INTAKE_20261007.json`
- vorbereitetes Master-Intake-Delta: `../../SEO_KATEGORIEN/HOBBY_MASTER_V2_INTAKE_DELTA_001_20261007.json`
- Fachvorprüfung: `../../SEO_KATEGORIEN/HOBBY_MASTER_V2_BATCH_001_SUBJECT_PREFLIGHT_20261007.json`
- DataForSEO-Request: `../../SEO_KATEGORIEN/HOBBY_MASTER_V2_BATCH_001_DATAFORSEO_REQUEST_20261007.json`
- realer Initialbefund: `../../SEO_KATEGORIEN/HOBBY_MASTER_V2_BATCH_001_REAL_RESULT_20261007.md`
- KISS-Endreplay des echten Ergebnisses: `../../SEO_KATEGORIEN/HOBBY_MASTER_V2_BATCH_001_V125_KISS_REPLAY_20261007.md`
- realer V1.12.6-Readback: `../../SEO_KATEGORIEN/HOBBY_MASTER_V2_BATCH_001_V126_REAL_READBACK_20261007.md`
- finale fachliche Batch-001-Bewertung: `../../SEO_KATEGORIEN/HOBBY_MASTER_V2_BATCH_001_FINAL_ASSESSMENT_20261007.json`
- Depth-Plan: `../../SEO_KATEGORIEN/HOBBY_MASTER_V2_BATCH_001_DEPTH_PLAN_20261007.json`
- WordPress-Bewertungskandidat: HD-001 V1.12.6 / SHA-256 `788b49529216555cba8cd74aae2a3a469f5f386e7ea2dc3d0449555910d55dca`

Batch 001 enthält reproduzierbar 16 aktuelle Master-Identitäten.
Kein Kandidat wurde aus Monetarisierung allein strukturell hochgestuft.
0 Zielbaum-Writes sind aus dem Batch aktuell zulässig.

## Produktionsstatus

Die 841 kanonischen Identitäten bleiben vollständig erhalten.

Sie werden nicht mehr einzeln durch weitere 16er-Batches geschickt.

Batch 001–003:
- 48 Identitäten detailliert geprüft;
- dienen nur als Kalibrierung;
- keine weitere Batchserie.

Finale praktische Zuordnung:
- 340 CORE;
- 501 Finder/Editorial;
- 12 kalibrierte CORE-Promotionen;
- 1 kalibrierte CORE-Demotion.

Finales Zielprofil:
`/hobby rausch/HD001_V1.13.1_PRACTICAL_TARGET_PROFILE_20261008.json`

Profil SHA-256:
`f5c6d9e5be7ee6184c50ded9db40549f4b1e2d2a8c29672f4eb7aa172ea8e014`

Finaler Audit:
`../../SEO_KATEGORIEN/HOBBY_MASTER_V2_PRACTICAL_FINAL_TARGET_AUDIT_20261008.json`

Zielbaum:
- 103 Basis-Logikknoten;
- 440 aufgelöste Logikknoten;
- 431 physische Zielobjekte;
- 8 Welten sind CORE-Roots;
- Hobbywelten ist View, kein Parent.

## Nächster Schritt

Kein Batch 004.

Einziger offener Schritt:
V1.13.1 real installieren und unter Kategorien den Finalen Zielbaum öffnen und den finalen Delta-Dry-Run ausführen.

0 DataForSEO.
0 Strukturwrites im Dry-Run.
Erst den Live-Dry-Run prüfen, dann genau einen Sync.
