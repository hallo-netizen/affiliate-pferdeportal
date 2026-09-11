# PRODUKTVERGLEICH – CURRENT STATE

STAND: 2026-09-11
STATUS: AKTIV / UPC 0.8.5 LIVE FAIL-CLOSED PASS / UPK 0.5.1 LIVE-BATCH 17/17 ABGESCHLOSSEN / MARKTRECHERCHE 175 GRUPPEN OFFEN

## AUTORITÄT

Diese Datei ist die einzige aktuelle Büro-Standzusammenfassung.

- aktuelle Arbeit: `HOBBYRAUM.md`
- Fehlerdetails: `FEHLERQUELLEN.md`
- Ziel: `ZIELVERTRAG_V2.md`
- Fachvertrag: `AKTENSCHRANK/05_FACH_DOSSIER_ARTIKELTYP_VERTRAG_V1.md`
- 0.8.4 Live-Beleg: `AKTENSCHRANK/10_V084_WORDPRESS_LIVE_RECEIPT.md`
- 0.8.5/UPK-Korrekturbeleg: `AKTENSCHRANK/12_V085_LIVE_INVENTORY_GAP_UPK051_HARD_LOCAL_RECEIPT.md`

## TECHNISCHER STAND

UPC 0.8.5 bleibt unverändert installiert und fail-closed.

UPK 0.5.1 hat die vorhandene freigegebene Recherchebasis sequenziell über den kanonischen `UPK_Research::run_product_group()`-Weg live geprüft/materialisiert.

Live-Endstand des Batches:
- 17/17 Recherchegruppen verarbeitet;
- PASS: 6;
- TEIL-PASS: 8;
- BLOCKED: 3;
- `pairing-ready`: 9.

Kein Publish.
Kein künstliches SEO-PASS.

## ENTSCHEIDENDER BEFUND

Die vorhandene Recherchebasis umfasst nur:
- 17 Recherchegruppen;
- 102 vorgegebene Produktkandidaten.

Das ist **keine Markt-Recherche über die 175 Vergleichsgruppen**.
Der Live-Batch hat nur diese kleine Alt-Recherchebasis geprüft/materialisiert.

Darum sind die Ergebnisse erwartbar zu klein.

## VERBINDLICHES GESAMTZIEL

Für jede relevante Produktgruppe:

`möglichst vollständiger Marktbestand -> echte Herstellerfamilien -> aktuelle konkrete Modelle -> Herstellerquellen -> Faktenmatrix -> Sinn-/Vergleichbarkeitsprüfung -> alle fachlich zulässigen A-vs-B-Paare -> erst danach SEO`.

Keine Top-N-/Pair-Cap.
Keine künstliche Mindest- oder Höchstzahl an Vergleichen.
Maximal viele **sinnvolle** Vergleiche.

## AKTUELLER ARBEITSBLOCK

Keine weitere Pluginentwicklung.
Keine neue ZIP.

Jetzt ausschließlich:
1. alle 175 Registry-Gruppen als Recherchewarteschlange behandeln;
2. vorhandene 17 Gruppen nicht doppelt recherchieren, sondern gezielt erweitern;
3. für die übrigen Gruppen echte Hersteller/Modelle über Herstellerquellen recherchieren;
4. nicht-produktartige/ungeeignete Gruppen nur durch die bestehende Sinnprüfung ausschließen, nicht still verschwinden lassen;
5. Research-Vollständigkeit bleibt `UNPROVEN`, bis je Gruppe ein echter Beleg vorliegt;
6. erst nach einem großen belastbaren Datenblock eine gebündelte Aktualisierung des bestehenden Product-Knowledge-Bausteins;
7. diese Aktualisierung vor Ausgabe wieder positiv + negativ + gegen den gesamten UPC-Workflow prüfen.

NEXT ACTION ausschließlich `HOBBYRAUM.md`.
