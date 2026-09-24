# Kategorieintegration – PSTE Resolver-Reklassifikation – 2026-09-24

Status: **RESOLVER_BASELINE_PASS / BLOCKED_STATUS_CAUSE_OPEN**

Rolle: Evidence/Protokoll. Keine zweite CURRENT-/NEXT-ACTION-Wahrheit.

## Scope

Nur Kategorie/Struktur. Kein WordPress-Write. Keine 0.57.9-Installation. Kein PSERC-/Link-/Gesamt-E2E-Abschluss. Keine Bibliothek.

## Autorisierte Prüfbasis

- Branch vor Korrektur: `affiliate-release-current`
- HEAD: `3465ebee137f1e0e8e9162a45639de96cc33c66c`
- Category Integration Hard Baseline Run: `35979825403` = SUCCESS
- Artefakt: `pste-0576-category-map-1149-hardtest`, Artifact ID `10799254853`
- exakter 0.57.6-Rollback-SHA256: `71bae2436fc1c3d52c06cefe551517af32a89eeb005457331e2c44136a1c888f`
- 1149-Map-Datei SHA256: `935a9bef8ceceab9f8f48dc1a0ef0463e98684c77117c465c60859da908840ad`
- logischer Map-SHA256: `518a8d7e7f548503845790ed1a2d5d63278773c66164d13edf1b66af3bcd871b`

Der bereits vorhandene lokale 0.57.8-Stand bleibt:
`PSTE_0.57.8_SEOPORTAL_ADMIN_STABILITY_CATEGORY_1149_INSTALLIEREN.zip`
SHA256 `f2f4f9b4e09d3bb8301f12a3aee1f75e56d3a9f7cc2a750c525f62456367b6c7`.
Dieser Nachtrag behauptet keine neue Bytegleichheit zwischen 0.57.6 und 0.57.8.

## Harte Resolver-Prüfung

Die 1149-Kategorieableitung wurde mit der realen `PSTE_Article_Type_Registry::build()`-/`resolve()`-Logik geprüft. Für den isolierten Registry-Test wurden nur WordPress-unabhängige Hilfswerte gestubbt; die Kategorieauflösung selbst lief durch die echte Registry-Klasse.

Ergebnis:
- Registry-Familien: **256**
- eindeutige Familie+Artikeltyp-Kombinationen: **1149/1149**
- Dubletten Familie+Artikeltyp: **0**
- positive Resolverfälle: **28/28 PASS**
  - `gebisse-beratung`
  - `hafer-beratung`
  - `pferdedecken-winterdecken-beratung`
  - alle 25 Kategorien der fünf neuen Familien `pferdesaettel`, `trensen`, `offenstallbau`, `paddockbau`, `reitplatzbau`
- negativer Fremdfall: **PASS fail-closed**
  - Ergebnis `PSTE_TARGET_CATEGORY_EXACT_MATCH_MISSING`

Damit ist die 1149er Kategorie-/Familie-/Artikeltyp-Ableitung selbst nicht als Fehler reproduziert.

## Wichtige Status-Semantik

Im PSTE-Code bedeutet `BLOCKED_FOR_CATEGORY` nicht ausschließlich „Zielkategorie fehlt“.

Der Status wird ebenfalls gesetzt, wenn unter anderem:
- Planning-Readiness nicht PASS ist,
- der Pre-Title-Duplicate-Gate blockiert,
- Duplicate-/Cannibalization-Gründe greifen, z. B. `ANSWER_EQUIVALENT_EXISTING`, `ANSWER_EQUIVALENT_PLANNED`, `EXACT_EDITORIAL_INTENT_VARIANT` oder `CANONICAL_ARTICLE_OR_PLAN_SLOT_ALREADY_OWNED`.

Die Admin-Oberfläche bezeichnet denselben Status als:
**„Bereits abgedeckt oder blockiert“**.

Folge:
Die bisherige Beobachtung **496/500 `BLOCKED_FOR_CATEGORY`** beweist für sich allein keinen defekten Kategorie-Resolver.

## Fünf neue Familien

`Gesamtbestand neu erfassen` baut die Site-Baseline/Struktur und stößt den Context-Refresh an. Dieser Vorgang startet keine Keywordrecherche und erzeugt keine neuen Topic-Pool-Zeilen.

Folge:
0 Vorkommen der fünf neuen Familien im bereits vorhandenen Keyword-/Topic-Pool direkt nach der Baseline-Neuerfassung beweist ebenfalls nicht, dass die 1149er Kategorieauflösung diese Familien nicht kennt.

## Korrekte verbleibende offene Frage

Offen ist nicht mehr bewiesen:
„Kategorie-Resolver 496/500 kaputt“.

Offen ist:
**Warum tragen die 496 vorhandenen Zeilen `BLOCKED_FOR_CATEGORY`?**

Dafür müssen die vorhandenen Zeilen nach ihren tatsächlichen `reason_codes` / Planning-Readiness-/Duplicate-Gründen klassifiziert werden. Erst ein echter `PSTE_TARGET_CATEGORY_EXACT_MATCH_MISSING`-Befund bei einem bekannten gültigen Ziel wäre Beleg für einen Resolverfehler.

Bis dahin:
- 0.57.9 nicht installieren
- keine Kategorie-Resolver-Reparatur erfinden
- kein PSERC-Finalrefresh
- kein Linkrefresh
- kein Gesamt-E2E
- kein Live-Apply


## Live-Reason-Code-Stichprobe 2026-09-24

Quelle: direkte WordPress-PSTE-Themenprüfung, vom Benutzer aus dem aktiven System abgelesen. Read-only.

### Fall 1: `pferde stehlen lumpenpack`

- Fundstellen: 53
- Statusoberfläche: `Bereits abgedeckt` / `BLOCKIERT`
- Reason Codes:
  - `PSTE_PORTAL_RELEVANCE_PROVEN_FAMILY_ASSIGNMENT_NOT_PROVEN`
  - `PSTE_SANDBOX_INTERNAL_CLARIFICATION_REQUIRED`
  - `PSTE_FAMILY_V2_SUBJECT_HEAD_MISSING`
  - `PSTE_CONTEXT_QUERY_MISSING`
- Kontext: `PENDING`
- Befund: **kein** `PSTE_TARGET_CATEGORY_EXACT_MATCH_MISSING`; kein belegter Kategorie-Resolverfehler.

### Fall 2: `Wie alt werden Pferde?`

- Fundstellen: 80
- vorhandener veröffentlichter Beitrag laut Benutzer
- Reason Codes:
  - `PSTE_ARTICLE_TYPE_EXTENSION_ROUTE_PASS`
  - `EXACT_NORMALIZED_QUERY_DUPLICATE`
  - `CROSS_TYPE_ANSWER_EQUIVALENCE`
  - `PSTE_NORMAL_METADATA_PATH_PASS`
  - `EDITORIAL_TITLE_PIPELINE_V5_PASS`
  - `ARTICLE_TYPE_AUTOMATICALLY_RESOLVED`
- Kontext: `PENDING`
- Befund: korrekt als bereits abgedeckt/Duplicate blockiert; **kein** Kategorie-Resolverfehler.

### Fall 3: `Können Pferde schwimmen?`

- Fundstellen: 75
- vorhandener veröffentlichter Beitrag laut Benutzer
- Reason Codes identisch zu Fall 2:
  - `PSTE_ARTICLE_TYPE_EXTENSION_ROUTE_PASS`
  - `EXACT_NORMALIZED_QUERY_DUPLICATE`
  - `CROSS_TYPE_ANSWER_EQUIVALENCE`
  - `PSTE_NORMAL_METADATA_PATH_PASS`
  - `EDITORIAL_TITLE_PIPELINE_V5_PASS`
  - `ARTICLE_TYPE_AUTOMATICALLY_RESOLVED`
- Kontext: `PENDING`
- Befund: korrekt als bereits abgedeckt/Duplicate blockiert; **kein** Kategorie-Resolverfehler.

### Zwischenfazit

3/3 live geprüfte `BLOCKED_FOR_CATEGORY`-Zeilen enthalten **keinen** `PSTE_TARGET_CATEGORY_EXACT_MATCH_MISSING`.
2/3 sind nachweislich bereits veröffentlichte/inhaltlich äquivalente Themen und deshalb korrekt blockiert.
1/3 ist wegen fehlender Familien-/Kontextklärung blockiert, ebenfalls ohne Kategorie-Exact-Match-Fehler.

Der 496er Sammelstatus bleibt daher als Kategorie-Resolverfehler **nicht belegt**.

Nächste gezielte Prüfung:
Suche in der bestehenden `Portalweite Themenprüfung` nach bekannten gültigen Alt-Zielkategorien (`Gebisse`, `Hafer`, `Winterdecken`) und prüfe deren technische Details auf `PSTE_TARGET_CATEGORY_EXACT_MATCH_MISSING`. Keine Zufallsstichprobe.
