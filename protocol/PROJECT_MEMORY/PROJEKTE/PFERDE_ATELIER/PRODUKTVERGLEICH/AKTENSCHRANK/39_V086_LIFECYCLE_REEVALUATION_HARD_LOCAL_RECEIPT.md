# PRODUKTVERGLEICH – 0.8.6 LIFECYCLE-NEUBEWERTUNG HARD-LOCAL RECEIPT

STAND: 2026-09-11
STATUS: LOCAL HARD PASS / FRESH-ZIP PASS / WORDPRESS-LIVE OFFEN

## Ausgangsbasis

Autoritative Build-Basis war **nicht** der historische GitHub-Sourceordner, sondern die exakt gebundene und erneut materialisierte Release-Kandidaten-ZIP:

`universal-product-comparison-0.8.5-prototype.zip`

SHA-256:
`0174051e6584902142f5be5787642426b30aab6c7ba15ef0b07ccbdb4a5844fd`

Aktuelles Product Knowledge für die Gegenprüfung:

`universal-product-knowledge-0.5.1-prototype.zip`

SHA-256:
`17ba686ebbfeac774de5224a042e8ea5fcc472b91774c47271e6b585d74960a1`

## Bewiesener Root Cause

UPC 0.8.5 liest bei `plan_group()` das aktuelle Product Knowledge neu ein und bildet daraus das vollständige Cross-Brand-Paaruniversum. Es fehlte jedoch eine Lifecycle-Schranke vor der Paarbildung.

UPK 0.5.1 kennt die Zustände:
- `ACTIVE`;
- `TEMPORARILY_UNAVAILABLE`;
- `DISCONTINUED`;
- `UNKNOWN`.

0.8.5 filterte diese Zustände weder in der Paarbildung noch in der Readiness-Inventarzählung.

Harter gewünschter Negativtest gegen die **unveränderte exakte 0.8.5-Quelle**:

`DISCONTINUED`-Produkt zwischen zwei `ACTIVE`-Produkten blieb im Paaruniversum.

Ergebnis:
- Exit: ROT;
- `candidate_count = 3` statt 1;
- `manufacturer_count = 3` statt 2;
- zwei Paare enthielten das `DISCONTINUED`-Produkt.

Damit war die Zielregel „Abkündigung muss bei Neubewertung zu entfallen/BLOCKED führen“ real verletzt.

Fehler-ID:
`PV-LIFECYCLE-086-001`.

## KISS-Fix

Keine neue Route, kein neues Datenmodell, kein SEO-/Writer-/Draft-/Publishweg.

Nur eine zentrale Lifecycle-Eignung im vorhandenen Planner plus dieselbe Sicht in der vorhandenen Group-Readiness:

Paarbar:
- `ACTIVE`;
- `TEMPORARILY_UNAVAILABLE`.

Fail-closed ausgeschlossen:
- `DISCONTINUED`;
- `UNKNOWN`;
- fehlender/leer unklarer Lifecycle.

Wichtig:
`TEMPORARILY_UNAVAILABLE` bleibt absichtlich paarbar. Temporäre Commerce-Verfügbarkeit ist laut Zielvertrag Aufgabe des AFFILIATE-Wegs und darf die fachliche Modellgültigkeit nicht automatisch zerstören.

Die Reihenfolge ist bewusst:
1. kanonische Produktidentität/doppelte Altzeilen bereinigen;
2. **danach** Lifecycle prüfen.

Damit kann eine ältere `ACTIVE`-Zeile nicht wieder auferstehen, wenn die neueste kanonische Zeile bereits `DISCONTINUED` ist.

## Positiv-/Negativbeweis

Neuer harter Test:
`tests/hard_086_lifecycle_pair_gate.php`

Belegt:
- `ACTIVE` bleibt paarbar;
- `TEMPORARILY_UNAVAILABLE` bleibt paarbar;
- `DISCONTINUED` fliegt aus dem Paaruniversum;
- `UNKNOWN` fliegt aus dem Paaruniversum;
- fehlender Lifecycle fliegt fail-closed aus dem Paaruniversum;
- neuerer `DISCONTINUED`-Duplikatstand verdrängt ältere `ACTIVE`-Zeile und wird danach ausgeschlossen;
- Hersteller-/Produkt-/Kandidaten-Readiness zählt nur das lifecycle-paarbare Inventar.

Mutationstest:
`tests/hard_086_mutation_guards.py`

Zwei Rückfallmutationen werden korrekt ROT:
1. `DISCONTINUED` künstlich wieder erlauben;
2. Lifecycle-Filter aus der Group-Registry entfernen.

## Gesamter Regressionstest – Working Tree

Mit exakt gebundenen Abhängigkeiten:
- UPK 0.5.1;
- PSTE 0.56.25, SHA-256 `8122e3fa2273fe4d8e53476f557ed0ddd99a197e8b1c40302f35db245ebb0f95`;
- Portalstruktur SHA-256 `b86a160e6b8cf720077830422ca6b574203ce171fdc65d357fe9c6bed039c2e0`;
- abgeleiteter Portal-Katalog SHA-256 `4eecef55a3033a4691f8a832eba5fb1657cdb15826ee47d366dccbaabfbb1fa2`.

Ergebnis:
- ausführbare Regression: **38/38 PASS**;
- PHP-Lint: **51/51 PASS**;
- 175/175 Portalparität: PASS;
- synthetische 1000-Pair-No-Cap-Regel: PASS;
- integrierter SEO/Product-Knowledge/Dossier-Korridor: PASS;
- Herstellerfamilien-/130-Paar-Regression: PASS;
- reale PSTE-False-Pair-/Carryforward-Sicherung: PASS;
- SEO-Kostenbindung unverändert PASS.

## Exakt auszugebende Fresh-ZIP

`universal-product-comparison-0.8.6-prototype.zip`

SHA-256:
`6ad160d18fb0973463c214de4356447923cbb728e222725e5407868e580c24f6`

Fresh-Unzip-Beweis:
- Source↔ZIP: **74/74 exakt**;
- Report-Hashbindung: **73/73 exakt**;
- Fresh-ZIP Regression: **38/38 PASS**;
- Fresh-ZIP PHP-Lint: **51/51 PASS**.

Enthaltener Report:
`tests/HARD_LOCAL_TEST_REPORT_0.8.6.json`

## Aussagegrenze

Damit ist ausschließlich `PV-LIFECYCLE-086-001` lokal hart geschlossen.

Noch **nicht** behauptet:
- WordPress-Live-PASS für 0.8.6;
- Merge;
- Publish;
- vollständige V2-Gesamtfreigabe;
- dass alle übrigen Auditpunkte bereits technisch geschlossen sind.

Nach dem KISS-Fix wird der bestehende Read-only-Gesamtaudit ab dem nächsten noch nicht hart belegten Auditpunkt fortgesetzt.
