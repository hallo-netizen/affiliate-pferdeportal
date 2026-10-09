# HD-001 – PILOT 2.7 / DATAFORSEO BACKEND PLAN

STAND: 2026-10-09
STATUS: LOCAL HARD PASS / LIVE NOCH NICHT AUSGEFÜHRT

## Zweck

Fachlicher 10-Hobby-Pilot nach Zielvertrag 2.7.
DataForSEO wird ausschließlich über das bestehende WordPress-Backend / den vorhandenen APKW_DataForSEO-Client verwendet.

Keine externe Connector-/Ersatzquelle.
Keine WordPress-/HivePress-Strukturwrites.
Kein Zielbaum-Sync aus diesem Research-Schritt.

## Pilot-Hobbys

1. Buchbinden
2. Balance Board
3. Glasmalerei
4. Lasergravieren
5. Fledermausbeobachtung
6. Hydrokultur
7. Riffaquaristik
8. Briefmarken sammeln
9. Geocaching
10. Imkerei

Die bestehenden Live-Leafs sind im gebündelten Pilotprofil eingefroren und werden nicht ersetzt.

## Backend

Neuer read-only Unterpunkt:
Kategorien → Pilot 2.7

Ablauf:
1. kostenlose Vorprüfung;
2. Anzeige exakt 10 geplanter DataForSEO-Aufrufe;
3. ausdrückliche Bestätigung;
4. exakt ein `keyword_ideas`-Aufruf pro Hobby;
5. request-bounded: ein Paid-Call je AJAX-Schritt;
6. Fortschritt nach jedem erfolgreichen Call speichern;
7. Ergebnis ausschließlich als Research-JSON exportieren;
8. keine Strukturwrites.

Pro Hobby werden fünf fachlich neutrale Seeds gebündelt:
- Hobby;
- Hobby + Anfänger;
- Hobby + Ausrüstung;
- Hobby + Kosten;
- Hobby + Fragen.

Maximal 100 Keyword-Ideas je Hobby.

Der Export enthält:
- vollständige normalisierte Provider-Keywords;
- Search Volume / CPC / Competition / Intent / Core Keyword soweit geliefert;
- automatisch erkannte konkrete Fragekandidaten;
- vorhandene Bestands-Leafs als Referenz;
- Provider-Task-/Request-/Response-Hashes;
- tatsächliche Providerkosten;
- `wordpress_structure_writes = 0`.

## Sicherheitsgrenze

Der Research-Build setzt `APKW_TARGET_TREE_MANUAL_ONLY = true`.

Dadurch löst das reine Plugin-Update keinen neuen Target-Tree-Code-Upgrade-Sync aus.
Ein bereits laufender historischer Sync würde weiterhin sauber zu Ende geführt; bei aktuellem COMPLETE-Stand bleibt der Zielbaum unangetastet.

## Lokale Prüfung

Artefakt:
`HD001_V1.14.9_PILOT27_DATAFORSEO_READONLY_LOCAL_HARDPASS.zip`

SHA-256:
`09a8d4b5f8c213ff98b5ea3023ca8c9a6d8560ffa1a2db96f437896ff11eed26`

Pilotprofil SHA-256:
`9c1927ec4b1c98514c51a3bb1fa332d56d714185cd13a007999971c4e11bccc2`

Fresh-Unpack:
- 34/34 PHP-Lint PASS;
- ZIP-Integrität PASS;
- exakt 10 Hobbys PASS;
- exakt 10 Paid-Calls PASS;
- ein Call pro bounded step PASS;
- COMPLETE nach 10 Schritten PASS;
- COMPLETE erneut aufgerufen → 0 weiterer Provider-Call PASS;
- Profil-Drift vor Provider blockiert PASS;
- Providerfehler → Index bleibt unverändert PASS;
- 9-Hobby-Profil → BLOCKED PASS;
- Question-Filter PASS;
- 0 Strukturwrite-Funktionen im neuen Research-Modul;
- MANUAL_ONLY verhindert Code-Update-Target-Revalidation PASS.

## Nächster Schritt

Exakt dieses ZIP live installieren.
Dann nur:
Kategorien → Pilot 2.7 → kostenlose Vorprüfung → exakt 10 DataForSEO-Aufrufe bestätigen → Lauf COMPLETE → Pilot-Research JSON herunterladen.

Erst der heruntergeladene echte DataForSEO-Export wird für die fachliche Entscheidung über zusätzliche FAQ-/Einstiegs-/Ausrüstungs-/Vertiefungs- und hobbiespezifische Leafs verwendet.

Kein Kategorien-/Zielbaum-Write vor dieser Auswertung.
