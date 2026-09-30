# HOBBYRAUSCH – SEO_KATEGORIEN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-09-30
STATUS: V1.9.1 LIVE-STAGE-TEST PASS / BUCHBINDEN GLOBAL-COVERAGE LIVE COMPLETE / GLOBAL-KORREKTUR POSITIV+NEGATIV SIMULIERT / LIVE-IMPORT NÄCHSTES

## Harte Abnahmeregel

**Keine Datei, kein Pluginstand und kein Produktionsschritt gilt als abnahmefähig ohne dokumentierte lokale Positiv- UND Negativsimulation.**

## Live Global-Coverage

Eingangsdraft:
`hobby-depot-buchbinden-production-pilot-v1`

Global-Coverage:
- V1.9.1;
- 7 Seeds;
- 1000 Ergebnisse;
- DataForSEO-Aufruf COMPLETE;
- Kosten laut Paket: 0.132 USD;
- Global-Paket bleibt serverseitig gespeichert und wird für Detailresearch wiederverwendet.

Der Seed `buchbinden online` erzeugte im globalen Provider-Resultat viele fachfremde Online-Treffer (Wetter/Nachrichten usw.).
Das ist kein WordPress-Fehler; die Global-Stufe verlangt deshalb explizite Master-Entscheidungen pro Review-Core.

## Korrigierter Global-Draft

Datei:
`HOBBY_DEPOT_BUCHBINDEN_GLOBAL_KORRIGIERT_RESEARCH_DRAFT.json`

SHA-256:
`95b19bfc7d50f4d54d09cfa2ccc00c550ce967b024461b2d45e6e0c0a114b42e`

Entscheidungen:
- 26/26 Global-Review-Cores explizit entschieden;
- `buch selber binden` → SUBTOPIC, Owner `Techniken & Praxis`;
- `buch binden lassen online` → OUT_OF_SCOPE für den aktuellen Hobby-Pilot;
- `buch drucken lassen` → OUT_OF_SCOPE;
- `gebrauchte bücher kaufen` → OUT_OF_SCOPE;
- fachfremde Online-/Wetter-/Nachrichten-Cores → OUT_OF_SCOPE;
- keine Architekturmutation durch irrelevante Provider-Treffer.

Global-Bindung:
- Package-ID passend;
- Content-Hash passend;
- Project-ID passend;
- Project-Discovery-Scope passend.

## Positivsimulation

Exakter korrigierter Draft gegen V1.9.1:
- RESEARCH_DRAFT Preflight PASS;
- initialer Review-Scope unverändert/passend;
- gespeicherte Global-Bindung PASS;
- 26 Global-Review-Gruppen vollständig entschieden;
- Global-Coverage-Gate PASS;
- Global-Content-Hash PASS.

## Negativsimulation

Alle erwartungsgemäß BLOCKED:
- eine Global-Entscheidung fehlt → `GLOBAL_COVERAGE_CORE_UNRESOLVED`;
- DEFERRED → `GLOBAL_COVERAGE_CORE_DEFERRED_BLOCKS_DETAIL`;
- falscher Global-Hash → Binding FAIL;
- veränderter Discovery-Scope → Binding FAIL;
- ungültiger Decision-Code → `GLOBAL_COVERAGE_DECISION_VALUE_INVALID`;
- falscher Owner-Cluster → `GLOBAL_COVERAGE_OWNER_CLUSTER_MISMATCH`.

Evidence:
`HOBBY_DEPOT_BUCHBINDEN_GLOBAL_KORRIGIERT_POS_NEG_EVIDENCE.json`

Beleggrenze:
Die WordPress-HMAC-Signatur des bereits live erzeugten Global-Pakets ist servergeheim und kann offline nicht neu berechnet werden. Das Paket wurde live durch V1.9.1 erzeugt und gespeichert; der nächste serverseitige Freigabeschritt prüft diese Signatur erneut.

## NEXT ACTION

In WordPress `Kategorien`:
1. über `Arbeitsstand übernehmen` nur den korrigierten Draft hochladen;
2. danach `Korrigierten Stand freigeben`;
3. danach `Detailresearch starten`.

Das Global-Coverage-Paket NICHT erneut hochladen; es liegt bereits serverseitig vor.

Bei irgendeinem BLOCKED/Fehler:
keine Abnahme, sondern lokal reproduzieren → Positiv-/Negativsimulation → erst danach neuer Kandidat.
