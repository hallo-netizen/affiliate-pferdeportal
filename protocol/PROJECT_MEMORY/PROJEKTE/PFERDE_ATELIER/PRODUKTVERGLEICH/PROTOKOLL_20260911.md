# PRODUKTVERGLEICH – ARBEITSPROTOKOLL 2026-09-11

ROLLE: chronologischer Ausführungs-/Testbeleg. Nicht CURRENT, nicht Zielvertrag, nicht Fehlerhauptquelle.

## 0.8.4 – 175er Infrastruktur

Gebaut/geprüft:
- autoritative 175/175 Vergleichsgruppenregistry aus Portalstruktur;
- jede Gruppe sichtbar mit Readiness/Coverage;
- keine Top-N-/Pair-Cap;
- Research-Kandidaten ≠ Markt vollständig;
- Sinn-/Nutzungsebenenprüfung vor SEO.

Harter lokaler Stand:
- 32/32 Tests PASS;
- 48/48 PHP-Lint PASS;
- Source↔ZIP 67/67;
- Report-Hashes 66/66.

WordPress-Live:
- 175/175 sichtbar;
- Regendecken Proofstand erhalten;
- identischer Wiederholungslauf 0 Provider / $0.0000;
- 8 BLOCKED / 0 Dossiers;
- korrekt `NO_ELIGIBLE_COMPARISONS`.

## 0.8.5 – Herstellerfamilien/Fachprofile

Gefundener Ursachenfehler:
Readiness konnte Herstellerlabels statt Herstellerfamilien zählen.

Fix:
Aesculap/Kerbl + Kerbl werden überall als eine Herstellerfamilie behandelt.

Harter lokaler Stand finaler ZIP:
- 35/35 Regression PASS;
- 50/50 PHP-Lint PASS;
- Source↔ZIP 71/71;
- Report-Hashes 70/70;
- drei Herstellerfamilien-Rückfallmutationen korrekt ROT.

Wichtige Testgrenze:
Die lokal berechneten 130 zusätzlichen Cross-Family-Paare waren Potentiale aus der freigegebenen Research-Basis nach synthetischer Testmaterialisierung, keine vorab belegten WordPress-Live-Paarzahlen.

## 0.8.5 WordPress – fail-closed Gegenbeweis

Nach Installation zeigte Winterdecken:
- Research-Katalog 8 Kandidaten / 3 Hersteller;
- echtes Product-Knowledge-Inventar zunächst 0 / 0;
- `PRODUCT_INVENTORY_MISSING`;
- 0 Paare;
- $0.0000 neue Providerkosten.

Bewertung:
UPC 0.8.5 war fail-closed korrekt; die Release-Erwartung war zu optimistisch.

Fehler-ID:
`PV-TEST-085-003`.

## Universal Product Knowledge 0.5.1

KISS-Fix:
Kein neuer Importer/kein neues Datenmodell.
Nur sequenzielle Batch-Orchestrierung über den vorhandenen kanonischen Weg:
`UPK_Research::run_product_group()`.

Finale Kandidaten-ZIP SHA-256:
`17ba686ebbfeac774de5224a042e8ea5fcc472b91774c47271e6b585d74960a1`

Lokal geprüft:
- Positiv/Negativ PASS;
- Nonce/Capability PASS;
- Sequenz PASS;
- kanonischer Gruppenlauf PASS;
- 4 Mutationen korrekt ROT;
- PHP-Lint 5/5;
- Source↔ZIP 8/8;
- Report-Hashes 7/7;
- UPC 0.8.5 komplette Regression gegen exakt finale UPK-0.5.1-ZIP 35/35 PASS.

## UPK 0.5.1 WordPress-Live-Batch

Originaloberfläche:
- Hauptmenü `Produktwissen`;
- Seitentitel `Produktrecherche`;
- Bereich `Freigegebene Recherchebasis gesammelt materialisieren`.

Batch real abgeschlossen:
- 17/17 vorhandene Recherchegruppen;
- PASS 6;
- TEIL-PASS 8;
- BLOCKED 3;
- pairing-ready 9.

Aussagegrenze:
Die Alt-Recherchebasis umfasste nur 17 Gruppen / 102 Kandidaten. Der Lauf materialisierte diese Basis; er war keine 175-Gruppen-Marktrecherche.

Dauerbeleg:
`AKTENSCHRANK/23_UPK051_WORDPRESS_LIVE_BATCH_RECEIPT_20260911.md`.

## Zielkorrektur Skalierung

Verbindlich bestätigt:
- Regendecken war Proofgruppe, nicht Umfang;
- Ziel = 175 autoritative Vergleichsgruppen;
- je Gruppe möglichst viele reale relevante Hersteller/Modelle;
- alle fachlich zulässigen A-vs-B-Paare;
- blindes Kreuzprodukt verboten;
- Sinn-/Nutzungsebenenprüfung vor kostenpflichtigem SEO;
- keine künstliche Top-N-/Pair-Cap.

## Research-Arbeit A–J

Auf dem gleichen Hobbybranch wurden zehn Research-Evidence-Akten A–J gesichert:
`AKTENSCHRANK/13_...` bis `22_...`.

Frischer Compare zeigte:
- 10 Commits;
- ausschließlich diese zehn neuen Research-Akten;
- kein Plugin-Code und keine konkurrierende Status-/Fehler-/Zieländerung in diesen zehn Commits.

Jede Akte bleibt ausdrücklich:
Research Candidate Evidence / nicht Product Knowledge / nicht SEO-freigegeben / keine Markt-Vollständigkeit.

Der gemeinsame A–J-vs-175-Coverage-Abgleich wurde noch nicht erzeugt.
Daher keine erfundene Coverage-Zahl.

Dauerbeleg:
`AKTENSCHRANK/24_MARKTRECHERCHE_PROGRESS_A_J_20260911.md`.

## Nutzer-Hard-Rule zur Plugin-Übergabe

Verbindlich für Folgearbeit:
Keine Plugin-Übergabe ohne Beweis an der **exakt auszugebenden ZIP**:
- lokaler Positivtest;
- lokaler Negativ-/Mutationstest;
- Gegenprüfung gegen den gesamten aktuellen Produktvergleichsworkflow;
- Fresh-ZIP-/Hashbindung nach betroffenem Releaseweg.

Research-/Datenbatch erzeugt nicht automatisch eine neue Pluginversion.

## Abschluss-/Nachholprüfung

Frisch gelesen:
- Campus START_HERE / Eingangsstandard;
- Produktvergleich START_HERE / CURRENT_STATE / HOBBYRAUM / FEHLERQUELLEN / ZIELVERTRAG V2;
- zentrale Fehler-/Ziel-/Änderungs-/Archiv-/Handlungsquellen;
- Branch/Research-Head;
- Nachbarbranch ACM read-only.

Gefundene Nachholpunkte:
- HOBBYRAUM/Fehlerregister noch vor bereits abgeschlossenem 17/17-Live-Batch;
- Zielvertrag enthielt veralteten dynamischen Fortschritt;
- Handlungsverzeichnis enthielt noch abgelösten eigenen Writer-/Draftweg;
- START_HERE verwies nur auf altes Protokoll;
- technischer 0.8.5-Sourcehinweis musste 130-Paare-Interpretation korrigieren.

Diese Punkte werden in der Abschlussnachholung korrigiert.

## Nachbarweg

Frisch gelesen:
`alternative/seo-text-central-machine-20260908`
Head:
`ba511c2caec5e970948cf8e5c0139bcfea017ce2`

Erster echter Realtest-Blocker:
`CODEX_PRODUCTION_ENVIRONMENT_PROOF_MISSING`.

Nachbarbranch nicht verändert.

## Offen

Aktiver erster Produktvergleichs-Arbeitsblock:
A–J gegen autoritative 175er Registry konsolidieren, danach nur ungedeckte Gruppen weiterrecherchieren.

Kein neuer Pluginbau in diesem Researchblock.
Kein SEO-Lauf aus Research-Evidence.
Kein Merge.
Kein Publish.
