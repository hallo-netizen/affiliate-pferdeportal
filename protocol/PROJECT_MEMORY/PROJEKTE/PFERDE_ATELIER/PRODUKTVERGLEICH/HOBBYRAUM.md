# PRODUKTVERGLEICH – HOBBYRAUM

STAND: 2026-09-11
STATUS: AKTIV

## 1-KLICK-ÜBERSICHT

**WAS IST DAS?**  
Isolierter Arbeitsraum für den laufenden Produktvergleichs-Gesamtaudit.

**AKTUELL:**  
175/175 Registry-Keys wurden im ersten Research-Durchlauf betrachtet: 97 `EVIDENCE_PRESENT`, 78 `PARTIAL_AMBIGUOUS`, 0 `NO_GROUP_EVIDENCE`. Der erste technische Auditfehler `PV-LIFECYCLE-086-001` ist auf Basis der exakt gebundenen 0.8.5-ZIP bewiesen und als 0.8.6-KISS-Fix lokal inklusive Fresh-ZIP hart grün. WordPress-Live für 0.8.6 ist noch offen.

**DU DARFST …**  
den bestehenden Audit ohne Seitensprung am nächsten noch nicht hart belegten Punkt fortsetzen; nur bei realem RED einen weiteren KISS-Fix bauen; denselben Gesamtworkflow danach erneut positiv/negativ prüfen.

**DU DARFST NICHT …**  
einen zweiten Fix aus Vermutung bauen; Research-Funde automatisch zu Product Knowledge erklären; manuell finale Produktpärchen festschreiben; SEO starten; den Nachbarweg ändern; mergen oder veröffentlichen.

**ALS NÄCHSTES …**  
Read-only beweisen, dass bloße Research-Evidence ohne materialisiertes Product Knowledge **kein** Paar erzeugen kann. Danach Nicht-V1-Gruppen fail-closed, SEO-ohne-Override und Dossier-Neuaudit prüfen. Beim ersten realen Fehler stoppen und nur diesen ursachenbasiert bearbeiten.

## BRANCH

`hobbyroom/productvergleich-workflow-v070-20260908`

Research-Stand:
`AKTENSCHRANK/38_MARKTRECHERCHE_COVERAGE_DELTA_K_T_20260911.md`

Lifecycle-Fix-Beleg:
`AKTENSCHRANK/39_V086_LIFECYCLE_REEVALUATION_HARD_LOCAL_RECEIPT.md`

## SICHERER TECHNISCHER STAND

Letzter WordPress-Live-Stand UPC 0.8.5:
`0174051e6584902142f5be5787642426b30aab6c7ba15ef0b07ccbdb4a5844fd`

Aktueller lokal hart geprüfter UPC-0.8.6-Kandidat:
`6ad160d18fb0973463c214de4356447923cbb728e222725e5407868e580c24f6`

UPK 0.5.1:
`17ba686ebbfeac774de5224a042e8ea5fcc472b91774c47271e6b585d74960a1`

0.8.6 Hardbeleg:
- Original-0.8.5 Solltest real ROT: `DISCONTINUED` blieb in 3 Paaren statt nur 1 gültigem Paar;
- Working Tree 38/38 PASS;
- zwei neue Lifecycle-Mutationen korrekt ROT;
- PHP-Lint 51/51 PASS;
- Fresh-ZIP Source↔ZIP 74/74 exakt;
- Report-Hashes 73/73 exakt;
- Fresh-ZIP Regression 38/38 PASS;
- Fresh-ZIP PHP-Lint 51/51 PASS.

Kein WordPress-Write wurde für 0.8.6 ausgeführt.

## GESCHLOSSENER ERSTER TECHNISCHER GAP

`PV-LIFECYCLE-086-001`

0.8.5 las aktuelles UPK neu, filterte aber den Lifecycle nicht vor Pairing/Readiness.

0.8.6:
- `ACTIVE` paarbar;
- `TEMPORARILY_UNAVAILABLE` paarbar;
- `DISCONTINUED` ausgeschlossen;
- `UNKNOWN`/fehlend ausgeschlossen;
- Deduplizierung vor Lifecycle-Gate verhindert Wiederbelebung älterer ACTIVE-Zeilen.

Keine neue Route, kein neues Datenmodell, kein Writer/Draft/Publish.

## COVERAGE

Aktueller source-bound Beleg:
`AKTENSCHRANK/38_MARKTRECHERCHE_COVERAGE_DELTA_K_T_20260911.md`

- `EVIDENCE_PRESENT`: 97;
- `PARTIAL_AMBIGUOUS`: 78;
- `NO_GROUP_EVIDENCE`: 0;
- Summe: 175/175.

Das ist keine Markt-Vollständigkeit und kein Pairing-Ready-Beleg.

## FINALE ENTSCHEIDUNGSINSTANZ

Dauerbeleg:
`AKTENSCHRANK/31_ARCHITEKTURENTSCHEIDUNG_PLUGIN_FINAL_AUTHORITY_20260911.md`

Verbindlich:
- Research/Product Knowledge liefert Produkte/Fakten;
- SEO liefert Nachfrage-/Priorisierungssignale;
- PRODUKTVERGLEICH-System/Plugin trifft die letzte Paar-/Dossierentscheidung;
- neue/entfallene/geänderte Produkte müssen aus aktuellem Product Knowledge wiederholt neu bewertet werden;
- Paare dürfen dadurch entstehen, entfallen oder BLOCKED werden.

## NEXT ACTION – GESAMTAUDIT FORTSETZEN

Prüfe im **exakten 0.8.6-Fresh-ZIP-Stand** jetzt nur den nächsten noch nicht hart geschlossenen Punkt:

1. Kann bloße Research-Evidence ohne materialisiertes Product Knowledge ein Paar erzeugen? Muss **NEIN** sein.
2. Falls PASS: Können Service/Knowledge/Checklisten-/nicht PRODUCT_COMPARISON-V1-fähige Registry-Keys ein Produktpaar erzwingen? Muss **NEIN** sein.
3. Falls PASS: Kann SEO eine fachliche Sperre überschreiben? Muss **NEIN** sein.
4. No-Cap bleibt über bestehenden 1000-Pair-Test gebunden.
5. Danach bestehenden Dossier-Neuaudit bei Produktentfall/Profile-/Policy-Drift hart prüfen.

Nur der **erste tatsächlich offene technische Fehler** wird anschließend bearbeitet.
Nach jedem Fix derselbe Gesamtregressionsweg; kein Sammelfix.

## DANACH FACHLICH

Die 78 `PARTIAL_AMBIGUOUS` werden nach Ursache klassifiziert. Nur echte `MORE_MARKET_RESEARCH_REQUIRED`-Fälle gehen erneut in Marktrecherche. Registry-/Artikeltyp-/Profilprobleme werden nicht durch mehr Produkt-Suche zugeschüttet.

## BLOCK-GRENZE

BLOCK bei:
- Fix ohne zuerst belegte technische Lücke;
- Research-Fund wird ohne Product Knowledge zu einem Paar;
- manuell festgeschriebenes finales Produktpaar umgeht Pluginentscheidung;
- SEO erzwingt fachlich unzulässige Paarung;
- alter Vergleich bleibt trotz ungültigem/entfallenem Produkt automatisch gültig;
- Markt-Vollständigkeit wird geschätzt;
- Top-N-/Pair-Cap reduziert Coverage;
- mehrdeutige Registry-Keys werden still zusammengeführt;
- Plugin-Übergabe ohne exakten Positiv-/Negativ-/Gesamtworkflow-/Fresh-ZIP-Beweis;
- Änderung an SEO/TEXT/ACM aus diesem Büro;
- Merge oder Publish.

Kein Auto-Publish.
