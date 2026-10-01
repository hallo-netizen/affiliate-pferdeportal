# K10 Architektur

## 1. Zentrale Wahrheit
`RULE_CATALOG.json` ist der zentrale Regelkatalog. Jede harte Regel hat genau einen `owner`.

## 2. Einmalige Inhaltsprüfung
Der Owner prüft seine Regel gegen genau einen Artikel-Hash. Bei PASS entsteht ein hashgebundener Receipt.

## 3. Keine Mehrfachprüfung
Nachfolgende Stationen dürfen den Inhalt derselben Regel nicht erneut bewerten. Sie prüfen nur Receipt, Owner, Katalog-Hash, Artikel-ID und Artikel-Hash.

## 4. Änderung nach PASS
Ändert sich der Artikel, ändert sich sein Hash. Alle alten Receipts passen dann nicht mehr und der Artikel muss nur für die betroffenen Regeln neu geprüft werden.

## 5. PPM
PPM 6.7.9 wird in K10 nicht mehr als monolithischer Endprüfer verwendet. Seine 89 fachlich reparierbaren Regeln werden in eindeutige Regel-Owner überführt. Die 15 technischen Integritätsregeln bleiben als Integritätsprüfungen sinnvoll.

## 6. LT 6.8
LanguageTool bleibt genau ein externer Sprachprüfer. Sein PASS wird als Receipt gebunden; später wird Sprache nicht nochmal geprüft, solange der Artikel-Hash unverändert ist.

## 7. PSERC / ENDSTEMPEL / WordPress
Diese Stufen prüfen nur ihren eigenen Vertrags-, Signatur- bzw. Importbereich. Sie dürfen bestandene redaktionelle Regeln nicht nochmal neu auswerten.

## 8. K9-Isolation
K10 enthält keine K9-Artikel oder K9-Runtime. Einzige Herkunft ist die unveränderliche Referenz `K9_BASELINE_REFERENCE.json`.
