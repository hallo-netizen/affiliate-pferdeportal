# PRODUKTVERGLEICH – UPC 0.8.6 READ-ONLY ARCHITEKTUR-AUDIT

Stand: 2026-09-11
Status: LOCAL READ-ONLY PASS / KEIN WORDPRESS-WRITE

## Gebundene Quelle

Exakt geprüft:
`universal-product-comparison-0.8.6-prototype.zip`

SHA-256:
`6ad160d18fb0973463c214de4356447923cbb728e222725e5407868e580c24f6`

Die ZIP blieb unverändert.

## Audit 1 – Research / Nicht-V1 / SEO-Override

Externer read-only Testharness SHA-256:
`7c64e6149f7fec6470f5a4606f1df5d70773839fc603293c8b2664a4dbc59f28`

Ergebnis:
`UPC_0_8_6_READ_ONLY_AUDIT_RESEARCH_NONV1_SEO_PASS`

Belegt:
- bloße Research-Evidence bei leerem Product Knowledge erzeugt 0 Produkte und 0 Paare;
- zehn Service-/Knowledge-/Checklisten-/nicht-V1-Keys blockieren vor Product-Knowledge-Zugriff mit `UPC_COMPARISON_PROFILE_MISSING`;
- fachlich `BLOCKED` bleibt trotz künstlichem SEO `PASS/PASS` BLOCKED;
- ein fachlich vergleichbares Paar darf mit demselben SEO-PASS positiv READY werden;
- der kostenpflichtige SEO-Korridor lässt nur `COMPARABLE + NO_SIGNALS` weiter und schließt fachlich blockierte/bereits aufgelöste Paare aus.

## Audit 2 – bestehendes Dossier nach Inventardrift

Externer read-only Testharness SHA-256:
`c404431ddae781534340d8bb42f70e4cdc53f7b713b323e39f36ff984bf4e64f`

Ergebnis:
`UPC_0_8_6_DOSSIER_CURRENT_INVENTORY_REAUDIT_PASS`

Belegt:
- zunächst gültiges Paar/Dossier wird READY gebunden;
- danach wird eines der gebundenen Produkte im aktuellen Product Knowledge auf `DISCONTINUED` gesetzt;
- erneuter Audit lässt das alte Dossier nicht READY;
- Grund wird explizit als `UPC_DOSSIER_CURRENT_CANDIDATE_NOT_FOUND` sichtbar;
- alte SEO-Bindung gilt nicht weiter als aktuell.

## Aussagegrenze

Damit sind die read-only Auditpunkte Research≠Pair, Nicht-V1 fail-closed, SEO ohne Fach-Override und Dossier-Neuaudit bei Produktentfall lokal gegen die exakte 0.8.6-Fresh-ZIP PASS.

Keine Pluginänderung.
Kein Product-Knowledge-Import.
Kein WordPress-Live-PASS für 0.8.6.
Kein Merge.
Kein Publish.
