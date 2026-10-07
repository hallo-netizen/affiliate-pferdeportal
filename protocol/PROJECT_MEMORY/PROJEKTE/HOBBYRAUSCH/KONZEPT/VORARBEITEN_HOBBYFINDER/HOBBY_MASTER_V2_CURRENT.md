# HOBBY DEPOT – HOBBY MASTER V2 – CURRENT DATA POINTER

STAND: 2026-10-07
STATUS: AKTIVE BEWERTUNGSBASIS / REGELVERTRAG GEBUNDEN / BATCH 001 AUSGEFÜHRT / NOCH KEINE GESAMTBEWERTUNG

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

Batch 001 enthält reproduzierbar 16 aktuelle Master-Identitäten.
Kein Kandidat wurde aus Monetarisierung allein strukturell hochgestuft.
0 Zielbaum-Writes sind aus dem Batch aktuell zulässig.

## Nächster Schritt

Fehlende Scope-/Content-Capacity-/Ownership-Evidenz für Batch 001 erzeugen und den identischen Batch danach erneut auswerten.

Keine direkte WordPress-Synchronisierung und kein Zielbaum-Delta vor belastbarer Rollen-/Ownership-Prüfung.
