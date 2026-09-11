# PRODUKTVERGLEICH – HOBBYRAUM

STAND: 2026-09-11
STATUS: AKTIV

## 1-KLICK-ÜBERSICHT

**WAS IST DAS?**  
Isolierter Arbeitsraum für die laufende Produktvergleichs-Fachskalierung.

**AKTUELL:**  
Der erste Research-Durchlauf über alle 175 Registry-Keys ist abgeschlossen: 97 `EVIDENCE_PRESENT`, 78 `PARTIAL_AMBIGUOUS`, 0 `NO_GROUP_EVIDENCE`. Jetzt wird nicht blind weiterrecherchiert. Der aktive Block ist die harte read-only Prüfung der bestehenden UPC-/UPK-Logik gegen die verbindliche finale Plugin-Autorität und regelmäßige Neubewertung.

**DU DARFST …**  
aktuellen Plugin-/Testcode lesen, vorhandene Paar-/Readiness-/Refresh-Logik gegen Zielvertrag und Fachbelege prüfen, exakt den ersten technischen Gap benennen, danach nur bei belegter Lücke einen KISS-Fix vorbereiten.

**DU DARFST NICHT …**  
Plugin umbauen, bevor die Lücke belegt ist; Research-Funde automatisch zu Product Knowledge erklären; manuell finale Produktpärchen festschreiben; SEO starten; den Nachbarweg ändern; mergen oder veröffentlichen.

**ALS NÄCHSTES …**  
UPC 0.8.5 + UPK 0.5.1 read-only prüfen: finale Paarinstanz, Neubewertung aus aktuellem Product Knowledge, Entfall/Block ungültiger Produkte, Research!=Pair, Nicht-V1-Gruppen fail-closed, keine Pair-Cap, SEO ohne Override.

## BRANCH

`hobbyroom/productvergleich-workflow-v070-20260908`

Aktueller Research-Stand ist source-bound in:
`AKTENSCHRANK/38_MARKTRECHERCHE_COVERAGE_DELTA_K_T_20260911.md`

## SICHERER TECHNISCHER STAND

UPC 0.8.5:
`0174051e6584902142f5be5787642426b30aab6c7ba15ef0b07ccbdb4a5844fd`

UPK 0.5.1:
`17ba686ebbfeac774de5224a042e8ea5fcc472b91774c47271e6b585d74960a1`

Bis zur jetzigen Auditstufe ist **kein neuer technischer Fix** belegt.

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

## NEXT ACTION – READ-ONLY AUDIT

Prüfe im bestehenden Code/Testbestand genau:
1. Wo wird das Produktinventar bezogen und gebunden?
2. Wo entsteht das Paaruniversum?
3. Welche Stelle trifft die letzte `eligible/BLOCKED`-Entscheidung?
4. Wird bei erneutem Lauf das aktuelle Product Knowledge neu gelesen oder nur alter Pair-/Dossierzustand fortgeführt?
5. Werden fehlende/entfallene/ungültige Produkte entfernt bzw. blockiert?
6. Kann bloße Research-Evidence ohne Product Knowledge ein Paar erzeugen? Muss NEIN sein.
7. Können Service/Knowledge/Checklisten-/nicht PRODUCT_COMPARISON-V1-fähige Registry-Keys ein Produktpaar erzwingen? Muss NEIN sein.
8. Kann SEO eine fachliche Sperre überschreiben? Muss NEIN sein.
9. Gibt es irgendeine Top-N-/Pair-Cap? Muss NEIN sein.
10. Bestehende Tests lesen: welche dieser Regeln sind real positiv UND negativ/mutativ belegt?

Nur der **erste tatsächlich offene technische Fehler** wird anschließend bearbeitet.

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
- Plugin-Übergabe ohne exakten Positiv-/Negativ-/Gesamtworkflow-Beweis;
- Änderung an SEO/TEXT/ACM aus diesem Büro;
- Merge oder Publish.

Kein Auto-Publish.
