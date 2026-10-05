# HOBBYRAUSCH – SEO_KATEGORIEN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-05
STATUS: V1.9.8 FULL-HIERARCHY LOCAL HARD PASS / LIVE-INSTALLATION UND REALER FRONTEND-READBACK OFFEN

## Zielvertrag

`ZIELVERTRAG_HD001_AUTOMATISCHE_SEO_HIERARCHIE_20261003.md`

Ziel:
Konzept → DataForSEO → Hauptportal + Magazin + HivePress → WordPress → Publish → sichtbares Frontend → Readback.

## Live-Wahrheit

Livebestand wurde während der lokalen E2E-Arbeit nicht verändert.

Real zuletzt beobachtet:
- `Buchbinden` ist sichtbar;
- die vier Content-Leafs sind im bisherigen Live-Stand noch nicht sichtbar.

V1.9.7 bleibt verworfen.

## V1.9.8 – lokaler finaler Kandidat

Die bisher offenen technischen Punkte sind lokal geschlossen:

- variable native Page-Hierarchie statt Root+4;
- `Fertigen → Buch & Papier → Buchbinden` als 3-Seiten-Kette;
- keine feste `MAX_CONTENT_CHILDREN_PER_TOPIC=4`-Grenze im Full-Hierarchy-Weg;
- Page→Taxonomy über internen unsichtbaren Bridge-Term;
- sichtbare Leaf-Kategorien nativ darunter;
- wiederholbare kurze Leaf-Namen in getrennten Hobby-Kontexten;
- gemeinsame Strukturplanung für Content, Magazin und HivePress bei technisch getrennten Zielsträngen;
- Magazin über eigene hierarchische `journal_cat`;
- HivePress über `hp_listing_category`;
- Sparse-/Delta-Erweiterungen bleiben erhalten;
- kein automatisches Löschen vorhandener Knoten;
- Publish/Readback bis zum sichtbaren Frontend-Endzustand;
- Idempotenz: zweiter identischer Lauf = 0 unnötige Writes.

## Frisch geprüfte lokale Evidenz

Reale aufgezeichnete Buchbinden-DataForSEO-Evidenz wurde im lokalen Replay verwendet; keine neuen Paid-Calls.

Builder:
- Buchbinden Full-Hierarchy PASS;
- mehrere Hobbys PASS;
- gemeinsames `Fertigen` nur einmal;
- `Einstieg` je Hobby konfliktfrei;
- >4 evidenzbelegte Leafs möglich;
- nicht belegte optionale FAQ wird nicht künstlich erzeugt.

Kompletter POSITIV-E2E:
- Global Coverage PASS;
- Detail Research PASS;
- Spezialisierung PASS;
- FINAL Validator PASS;
- FINAL Evidence PASS;
- Deployment Preflight PASS;
- Write/Publish/technischer Readback PASS;
- native Page-Tiefe 3 PASS;
- Frontend-Readback PASS;
- exakt Einstieg / Ausrüstung / Material / Techniken & Praxis sichtbar;
- kein Bridge-/Magazin-/HivePress-Leak;
- zweiter identischer Lauf: 0 Writes.

Kompletter NEGATIV-E2E:
- unbekannter Parent BLOCKED;
- unbelegtes DataForSEO-Keyword BLOCKED;
- doppelter Leaf unter demselben Hobby BLOCKED;
- fehlender Marketplace-Pillar BLOCKED;
- stilles Entfernen bestehender Knoten BLOCKED;
- Bridge-Manipulation BLOCKED;
- Page-Parent-Drift BLOCKED;
- neue Kategorie ohne neue Research-Evidenz BLOCKED;
- Mutation nach Approval invalidiert Receipt.

Regression/Fresh-Unpack:
- bestehende Suite: 270/270 PASS;
- Fresh-Source: 270/270 PASS;
- Full-Builder-Flex PASS;
- Full-E2E POSITIV PASS;
- Full-E2E NEGATIV PASS;
- Source↔Installer Runtime: 25/25 byteidentisch;
- Installer PHP-Lint: 19/19 PASS.

## Artefakte

Installer:
`AFFILIATE_PORTAL_KATEGORIE_WORKFLOW_V1.9.8_FULL_HIERARCHY_E2E_HARD_PASS.zip`

SHA-256:
`60ea8d4c235805d66e6795223b1bfbd392cc0109556cfbf5631d9d0109b4585c`

Source:
`QUELLCODE_KATEGORIE_WORKFLOW_V1.9.8_FULL_HIERARCHY_E2E_HARD_PASS.zip`

SHA-256:
`340af0e4927971c746d97ba2aad8bab1e7efc269c70e12d21319734e7a363c10`

## Beleggrenze

V1.9.8 ist noch nicht live auf Hobby Depot installiert.
Darum gibt es noch keinen realen WordPress-/Frontend-PASS für V1.9.8.

## ERSTER OFFENER BLOCKER

`HD001_V198_LIVE_INSTALL_AND_FRONTEND_READBACK_OPEN`

## NEXT ACTION

Exakt V1.9.8 über den aktuellen Kategorie-Workflow installieren; keinen Reset und keine neue Konzeptschleife.

Danach den bestehenden Buchbinden-Stand über den vorgesehenen Publish-/Republish-Weg ausführen und real prüfen.

PASS erst, wenn das echte Frontend die erwartete Hierarchie und Leafs zeigt. Bei Abweichung STOP und konkreten Live-Delta prüfen; nicht raten und nicht blind eine neue Version bauen.
