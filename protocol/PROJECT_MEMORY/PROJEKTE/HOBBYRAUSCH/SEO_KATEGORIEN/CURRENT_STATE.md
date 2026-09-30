# HOBBYRAUSCH – SEO_KATEGORIEN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-09-30
STATUS: BUCHBINDEN RESEARCH LIVE COMPLETE / READ_ONLY_PREVIEW LOKAL POSITIV+NEGATIV SIMULIERT / LIVE-STRUKTURIMPORT NÄCHSTES

## Harte Abnahmeregel

**Keine Datei, kein Pluginstand und kein Produktionsschritt gilt als abnahmefähig ohne dokumentierte lokale Positiv- UND Negativsimulation.**

## Live Research

Plugin:
`Affiliate-Portal Kategorie-Workflow V1.9.1`

Live erzeugtes Research-Paket:
`research-specialization-depth-b43e665c-34a5-4672-a486-56f6f9e731ba`

Research:
- Global-Coverage erledigt;
- Detailresearch erledigt;
- Spezialisierungs-Tiefenprüfung 5/5 Content-Knoten erledigt;
- Research-Handoff verlangt jetzt `READ_ONLY_PREVIEW`.

## Finaler READ_ONLY_PREVIEW-Kandidat

Datei:
`HOBBY_DEPOT_BUCHBINDEN_READ_ONLY_PREVIEW_V1.json`

SHA-256:
`78b9db7666d413ba5508f0d59741ff6579e3dca22d8b0078f8c2fccdbeb19bcb`

Aktive Struktur:
- Content: Buchbinden → Einstieg / Ausrüstung / Material / Techniken & Praxis;
- Marketplace: Buchbinden Set;
- Magazine: Buchbinden Online.

Fragen/Probleme und FAQ bleiben bewusst noch ohne eigene Strukturpromotion, weil dafür im gebundenen Pilot-Research keine ausreichende eigenständige Evidenz vorliegt.

## Coverage-/Ownership-Entscheidungen

Cluster-Coverage:
- alle 49 reviewpflichtigen Cluster-Cores explizit entschieden;
- fachfremde Provider-/Online-/Wetter-/Buchhandels-/lokale Dienstleistungs-Cores strukturell ausgeschlossen;
- `buchbinden bücher` als ARTICLE_ONLY im redaktionellen Buchbinden-Online-Raum gebunden.

Explizite Artikel-Owner:
- Einstieg: `buchbinden kurs`, `buchbinden kosten`;
- Ausrüstung: `buchbinden zubehör`, `ahle buchbinden`;
- Material: `papier für buchbinden`, `vorsatzpapier buchbinden`;
- Techniken & Praxis: `buchbinden japanisch`, `buchbinden fadenheftung`, `buchbinden klebebindung`, `buchbinden hardcover`.

Editorial Handoff:
- 11 ARTICLE_ONLY-Zuweisungen;
- 11/11 eindeutig gebunden;
- Status lokal: `READY_FOR_DOWNSTREAM_EDITORIAL_PLANNING`.

## Positivsimulation

Exakter Kandidat gegen V1.9.1:
- Validator PASS;
- Research-Binding PASS;
- Research-Evidence `PASS_WITH_RESEARCH_EVIDENCE`;
- Editorial-Handoff PASS;
- Comparator `PASS_READ_ONLY_PREVIEW`;
- Fresh-Live-Simulation: 7 CREATE_PREVIEW / 0 CONFLICT / 0 BLOCKED.

V1.9.1 Regression zusätzlich:
**248/248 PASS**.

## Negativsimulation

Erwartungsgemäß BLOCKED:
- fehlende Cluster-Core-Entscheidung → `DFS_TOP_KEYWORD_GROUP_UNRESOLVED`;
- ARTICLE_ONLY ohne Owner → `SPECIALIZATION_COVERAGE_OWNER_MISSING`;
- Owner im falschen Cluster → `SPECIALIZATION_COVERAGE_OWNER_CLUSTER_MISMATCH`;
- nicht belegter Spezialisierungsintent → `DFS_SPECIALIZATION_DECISION_NOT_EVIDENCED`;
- fehlende Begründung für `Techniken & Praxis` → `DFS_VISIBLE_NAME_UNRESOLVED` + `DFS_CATEGORY_NAME_CHOICE_UNRESOLVED`;
- falscher Research-Hash → `RESEARCH_BINDING_HASH_MISMATCH`;
- doppelte Spezialisierungsentscheidung → `SPECIALIZATION_COVERAGE_DECISION_DUPLICATE`.

Evidence:
`HOBBY_DEPOT_BUCHBINDEN_READ_ONLY_PREVIEW_POS_NEG_EVIDENCE.json`

## Beleggrenze

Die live erzeugten Research-/Review-HMAC-Signaturen sind an das WordPress-Servergeheimnis gebunden und können offline nicht positiv neu verifiziert werden.

Lokal bestätigt:
- Content-Hash/Binding des Research-Pakets;
- Validator;
- Research-Evidence;
- Comparator;
- Ownership;
- Positiv-/Negativfälle.

Der verbleibende Server-HMAC-Gate wird beim Live-Import durch V1.9.1 erneut geprüft.

## NEXT ACTION

In WordPress `Kategorien` genau den neuen `READ_ONLY_PREVIEW` über `Arbeitsstand übernehmen` hochladen.

Wenn die Seite danach `Read-only Gesamtprüfung PASS.` zeigt:
1. `Finale Struktur freigeben`;
2. `WordPress-Vorschau erstellen`;
3. `Geprüften Plan anwenden`.

Bei irgendeinem BLOCKED/Fehler:
keine Abnahme; Fehler lokal reproduzieren → Positiv-/Negativsimulation → erst danach neuer Kandidat.
