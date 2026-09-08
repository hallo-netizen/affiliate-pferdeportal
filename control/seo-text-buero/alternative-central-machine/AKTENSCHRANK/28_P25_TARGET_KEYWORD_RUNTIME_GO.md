# P25 – TARGET-KEYWORD IM TITEL / RUNTIME-BEWEIS

Datum: 2026-09-08
Status: GO

## Harte Quelle

Im unveränderten PPM:
`includes/content-validator.php`

Regel:
`TITLE_MUST_CONTAIN_TARGET_KEYWORD`

Blocker:
`BLOCKED_CONTENT_TARGET_KEYWORD_TITLE`

Der Validator liest:
`item.target_keyword`

und blockiert, wenn das gebundene Keyword nicht im finalen Titel vorkommt.

Die Regel ist sowohl im normalen technical_check als auch im V5 technical_check vorhanden.

## Echter Normal-Draft-Mutationstest

Gebundenes Target-Keyword:
`Pferdeanhänger`

Originaltitel:
`Was muss vor einer Fahrt mit Pferdeanhänger geprüft werden?`

Baseline:
PASS.

Mutation:
Target-Keyword gezielt aus dem Titel entfernt.

Ergebnis:
- mutated_ok = false
- exakt:
  `BLOCKED_CONTENT_TARGET_KEYWORD_TITLE`

Erreichbarkeit:
`PPM679_Content_Validator::check`

## KISS-Folgerung

Kein neues SEO-Titel-Gate.

SEO ist im relevanten Bereich bereits aufgeteilt in vorhandene feste Komponenten:
- Target-Keyword im Titel -> PPM Content Validator
- Keyword-Ownership / Kannibalisierung -> Editorial Plan Runtime Gate / Systemwide Duplicate Guard

Keine Chat-/Worker-Entscheidung.

## Regression

Im selben Lauf P0 bis P25 vollständig PASS.

## Nächster Schritt P26

Recherche-/Fact-Pack-/PSTE-/PSERC-Kette read-only mappen.

Ziel:
- vorhandene Quelle des Fact-Packs
- Hash-/Schema-/Source-Bindung
- PSTE-Rolle
- PSERC-Rolle
- Übergabe an den bereits geprüften PPM-Normal-Draft-Kern

Keine neue Recherchelogik.
